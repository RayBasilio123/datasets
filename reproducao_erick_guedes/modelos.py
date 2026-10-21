"""Reproduz os modelos de Guedes (2020, cap. 3-4) para o teor de Fe do concentrado.

Protocolo da dissertacao:
  - treino em marco (358 amostras), divisao aleatoria 70/15/15 refeita a cada 5 ciclos,
    200 divisoes x 5 ciclos = 1000 treinos por modelo;
  - RNA MLP 1 camada oculta com 20 neuronios tanh, treino Levenberg-Marquardt (trainlm),
    parada apos 6 epocas sem melhora na validacao, maximo de 1000 epocas;
  - RF com 500 arvores e folha minima 3, treinada em treino + validacao;
  - entradas: 15 variaveis do RReliefF ou 10 componentes do PCA sobre 21 variaveis;
  - modelos escolhidos pelo maior R e pelo menor MSE no teste; aplicados de janeiro a maio
    e avaliados pelo MAE de cada mes.

O MATLAB do Erick nao esta disponivel: a RNA aqui e uma implementacao propria de LM em numpy
(mapminmax nas entradas e saidas, inicializacao Nguyen-Widrow) e a RF e o sklearn com 1/3 das
variaveis por divisao (padrao do bagging de regressao no MATLAB). O SCG (trainscg) segue o
algoritmo de Moller (1993) com os parametros padrao do MATLAB (sigma 5e-5, lambda 5e-7).

Uso: python modelos.py --atraso 0 [--divisoes 200 --ciclos 5 --workers 8]
"""
import argparse, json, os, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor

from prep import ETAPA3_21, MESES, SEL15

ROOT = Path(__file__).resolve().parent
ERICK = {  # MAE por mes (Figuras 4.8-4.11 e texto da sec. 4.5)
    "rna": {"modelo": "RNA LM, RReliefF, menor MSE", "mar": 0.6132, "jan": 1.8890, "fev": 2.3933, "abr": 2.1705, "mai": 2.1016},
    "rf": {"modelo": "RF, PCA, maior R", "mar": 0.5904, "jan": 0.9645, "fev": 1.0625, "abr": 1.3007, "mai": 1.1816},
}


# ---------------------------------------------------------------- RNA (Levenberg-Marquardt)
class MapMinMax:
    def __init__(self, X):
        self.lo, self.hi = X.min(0), X.max(0)
        self.rng = np.where(self.hi > self.lo, self.hi - self.lo, 1.0)

    def __call__(self, X):
        return 2 * (X - self.lo) / self.rng - 1

    def inv(self, Y):
        return (Y + 1) * self.rng / 2 + self.lo


def nguyen_widrow(n_in, n_hid, rng):
    beta = 0.7 * n_hid ** (1.0 / n_in)
    W = rng.uniform(-1, 1, (n_hid, n_in))
    W = beta * W / np.linalg.norm(W, axis=1, keepdims=True)
    b = beta * np.linspace(-1, 1, n_hid) * np.sign(W[:, 0])
    return W, b


class MLP:
    def __init__(self, treino="lm", n_hid=20, max_epocas=1000, max_falhas=6, min_grad=1e-9, seed=0, saida="linear"):
        """saida="tansig" reproduz o networ1_train001_code.m do Erick (net.layers{2}.transferFcn = 'tansig')."""
        self.treino, self.n_hid, self.max_epocas, self.max_falhas, self.min_grad = treino, n_hid, max_epocas, max_falhas, min_grad
        self.saida = saida
        self.rng = np.random.default_rng(seed)

    def _unpack(self, p):
        h, d = self.n_hid, self.d
        W1 = p[: h * d].reshape(h, d)
        b1 = p[h * d: h * d + h]
        w2 = p[h * d + h: h * d + 2 * h]
        return W1, b1, w2, p[-1]

    def _fwd(self, p, X):
        W1, b1, w2, b2 = self._unpack(p)
        H = np.tanh(X @ W1.T + b1)
        z = H @ w2 + b2
        return (np.tanh(z) if self.saida == "tansig" else z), H

    def _jac(self, p, X, H, y):
        _, _, w2, _ = self._unpack(p)
        dH = (1 - H ** 2) * w2
        J_W1 = (dH[:, :, None] * X[:, None, :]).reshape(len(X), -1)
        J = np.hstack([J_W1, dH, H, np.ones((len(X), 1))])
        return J * (1 - y ** 2)[:, None] if self.saida == "tansig" else J

    def fit(self, Xtr, ytr, Xva, yva):
        self.mx, self.my = MapMinMax(Xtr), MapMinMax(ytr[:, None])
        Xt, Xv = self.mx(Xtr), self.mx(Xva)
        yt, yv = self.my(ytr[:, None])[:, 0], self.my(yva[:, None])[:, 0]
        self.d = Xt.shape[1]
        W1, b1 = nguyen_widrow(self.d, self.n_hid, self.rng)
        p = np.concatenate([W1.ravel(), b1, self.rng.uniform(-0.5, 0.5, self.n_hid), [0.0]])
        self.p = self._lm(p, Xt, yt, Xv, yv) if self.treino == "lm" else self._scg(p, Xt, yt, Xv, yv)
        return self

    def _lm(self, p, Xt, yt, Xv, yv):
        mu, best_val, best_p, falhas = 1e-3, np.inf, p.copy(), 0
        y, H = self._fwd(p, Xt)
        e = yt - y
        sse = e @ e
        for _ in range(self.max_epocas):
            J = self._jac(p, Xt, H, y)
            g = J.T @ e
            if np.linalg.norm(g) < self.min_grad:
                break
            JtJ = J.T @ J
            while mu <= 1e10:
                try:
                    dp = np.linalg.solve(JtJ + mu * np.eye(len(p)), g)
                except np.linalg.LinAlgError:           # mu pequeno demais com JtJ singular: conta como passo ruim
                    mu *= 10
                    continue
                y2, H2 = self._fwd(p + dp, Xt)
                e2 = yt - y2
                if e2 @ e2 < sse:
                    p, y, H, e, sse = p + dp, y2, H2, e2, e2 @ e2
                    mu *= 0.1
                    break
                mu *= 10
            if mu > 1e10:
                break
            val = np.mean((yv - self._fwd(p, Xv)[0]) ** 2)
            if val < best_val:
                best_val, best_p, falhas = val, p.copy(), 0
            else:
                falhas += 1
                if falhas >= self.max_falhas:
                    break
        return best_p

    def _scg(self, p, Xt, yt, Xv, yv, sigma0=5e-5, lam=5e-7, min_grad=1e-6):
        """Scaled Conjugate Gradient (Moller, 1993), como o trainscg do MATLAB."""
        n = len(yt)

        def perf_grad(q):
            y, H = self._fwd(q, Xt)
            e = yt - y
            return e @ e / n, -(2 / n) * (self._jac(q, Xt, H, y).T @ e)

        E, g = perf_grad(p)
        r = -g
        d = r.copy()
        lam_bar, sucesso, delta = 0.0, True, 0.0
        best_val, best_p, falhas = np.mean((yv - self._fwd(p, Xv)[0]) ** 2), p.copy(), 0
        for k in range(1, self.max_epocas + 1):
            dd = d @ d
            if dd == 0 or np.linalg.norm(g) < min_grad:
                break
            if sucesso:
                sig = sigma0 / np.sqrt(dd)
                delta = d @ ((perf_grad(p + sig * d)[1] - g) / sig)
            delta += (lam - lam_bar) * dd
            if delta <= 0:
                lam_bar = 2 * (lam - delta / dd)
                delta = -delta + lam * dd
                lam = lam_bar
            mu = d @ r
            alpha = mu / delta
            E_novo, g_novo = perf_grad(p + alpha * d)
            Delta = 2 * delta * (E - E_novo) / mu ** 2
            if Delta >= 0:
                p = p + alpha * d
                r_ant, E, g = r, E_novo, g_novo
                r = -g
                lam_bar, sucesso = 0.0, True
                d = r.copy() if k % len(p) == 0 else r + ((r @ r - r @ r_ant) / mu) * d
                if Delta >= 0.75:
                    lam *= 0.25
            else:
                lam_bar, sucesso = lam, False
            if Delta < 0.25:
                lam += delta * (1 - Delta) / dd
            val = np.mean((yv - self._fwd(p, Xv)[0]) ** 2)
            if val < best_val:
                best_val, best_p, falhas = val, p.copy(), 0
            elif val > best_val:
                falhas += 1
                if falhas >= self.max_falhas:
                    break
        return best_p

    def predict(self, X):
        return self.my.inv(self._fwd(self.p, self.mx(X))[0][:, None])[:, 0]


# ---------------------------------------------------------------- dados e protocolo
def entradas(df, conjunto, tag):
    """rrelieff15/pca10: listas da dissertacao. auto_rrelieff/auto_pca: selecao refeita do zero (prep.py)."""
    mar = (df["mes"] == "mar").to_numpy()
    if conjunto.startswith("auto"):                       # auto_rrelieff, auto_disp_pca, ...
        prefixo, tipo = conjunto.rsplit("_", 1)
        sel = json.load(open(ROOT / f"dados/selecao_{tag}{prefixo[4:]}.json"))
        vars_rrf, vars_pca, n_pca = sel["etapa4_rrelieff"], sel["etapa3_correlacao"], sel["etapa4_pca_componentes"]
    else:
        tipo = "rrelieff" if conjunto == "rrelieff15" else "pca"
        vars_rrf, vars_pca, n_pca = SEL15, ETAPA3_21, 10
    if tipo == "rrelieff":
        return df[vars_rrf].to_numpy(float), {"variaveis": vars_rrf}
    X = df[vars_pca].to_numpy(float)
    lo, hi = X[mar].min(0), X[mar].max(0)
    Xn = (X - lo) / np.where(hi > lo, hi - lo, 1)              # normalizacao 0-1 pela faixa de marco
    pca = PCA(n_components=n_pca).fit(Xn[mar])
    return pca.transform(Xn), {"variaveis": vars_pca, "componentes": n_pca,
                               "variancia": float(pca.explained_variance_ratio_.sum())}


def dividir(n, seed, razoes=(70, 15, 15)):
    """Como o dividerand do MATLAB: as razoes sao normalizadas pela soma (o Erick usou 75/15/15)."""
    idx = np.random.default_rng(seed).permutation(n)
    n_va, n_te = round(razoes[1] / sum(razoes) * n), round(razoes[2] / sum(razoes) * n)
    return idx[: n - n_va - n_te], idx[n - n_va - n_te: n - n_te], idx[n - n_te:]


def avaliar(y_true, y_pred):
    r = float(np.corrcoef(y_true, y_pred)[0, 1])
    return r, float(np.mean((y_true - y_pred) ** 2))


def rodar_divisao(args):
    s, ciclos, X_all, y_all, meses, mar_idx, protocolo = args
    matlab = protocolo == "matlab"            # tansig na saida e divisao 75/15/15, como no MATLAB do Erick
    Xm, ym = X_all[mar_idx], y_all[mar_idx]
    tr, va, te = dividir(len(ym), seed=1000 + s, razoes=(75, 15, 15) if matlab else (70, 15, 15))
    trva, todos = np.r_[tr, va], np.arange(len(ym))
    linhas = []
    for c in range(ciclos):
        seed = s * 100 + c
        modelos = {
            "rna": MLP("lm", seed=seed, saida="tansig" if matlab else "linear").fit(Xm[tr], ym[tr], Xm[va], ym[va]),
            "rna_scg": MLP("scg", seed=seed, saida="tansig" if matlab else "linear").fit(Xm[tr], ym[tr], Xm[va], ym[va]),
            "rf": RandomForestRegressor(n_estimators=500, min_samples_leaf=3, max_features=1 / 3,
                                        random_state=seed, n_jobs=1).fit(Xm[trva], ym[trva]),
        }
        for nome, m in modelos.items():
            pm = m.predict(Xm)
            subconj = {"treino": tr, "validacao": va, "teste": te, "todos": todos} if nome != "rf" else \
                {"treino": trva, "teste": te, "todos": todos}
            linha = {"divisao": s, "ciclo": c, "modelo": nome}
            for k, ix in subconj.items():
                linha[f"R_{k}"], linha[f"MSE_{k}"] = avaliar(ym[ix], pm[ix])
            pred = m.predict(X_all)
            for mes in MESES.values():
                k = meses == mes
                linha[f"MAE_{mes}"] = float(np.mean(np.abs(y_all[k] - pred[k])))
            linhas.append(linha)
    return linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atraso", type=float, default=0)
    ap.add_argument("--divisoes", type=int, default=200)
    ap.add_argument("--ciclos", type=int, default=5)
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    ap.add_argument("--conjuntos", nargs="+", default=["rrelieff15", "pca10"])
    ap.add_argument("--saida", default="resumo.json")
    ap.add_argument("--fonte", choices=["i_conceicao", "originais"], default="originais")
    ap.add_argument("--protocolo", choices=["antigo", "matlab"], default="matlab",
                    help="matlab = como os .m do Erick: saida tansig e divisao 75/15/15")
    args = ap.parse_args()
    tag = f"{'orig_' if args.fonte == 'originais' else ''}atraso{args.atraso:g}h"
    df = pd.read_parquet(ROOT / f"dados/preenchidos_{tag}.parquet")
    y_all, meses = df["fe"].to_numpy(float), df["mes"].to_numpy()
    mar_idx = np.flatnonzero(meses == "mar")
    out = ROOT / "resultados" / (tag + ("_matlab" if args.protocolo == "matlab" else ""))
    out.mkdir(parents=True, exist_ok=True)
    resumo = {"atraso_h": args.atraso, "divisoes": args.divisoes, "ciclos": args.ciclos, "erick": ERICK}

    base_media = {f"MAE_{m}": float(np.mean(np.abs(y_all[meses == m] - y_all[mar_idx].mean()))) for m in MESES.values()}
    resumo["referencia_media_de_marco"] = base_media

    for conjunto in args.conjuntos:
        X_all, info = entradas(df, conjunto, tag)
        t0 = time.time()
        tarefas = [(s, args.ciclos, X_all, y_all, meses, mar_idx, args.protocolo) for s in range(args.divisoes)]
        with ProcessPoolExecutor(args.workers) as ex:
            linhas = [l for bloco in ex.map(rodar_divisao, tarefas) for l in bloco]
        res = pd.DataFrame(linhas).assign(conjunto=conjunto)
        res.to_csv(out / f"treinos_{conjunto}.csv", index=False)
        bloco = {"info": info, "segundos": round(time.time() - t0)}
        for nome, g in res.groupby("modelo"):
            # o MATLAB do Erick mede o MSE em todas as amostras de marco (perform(net,t,net(x)) e immse(y_geral,target))
            sel = {"maior_R": g.loc[g["R_teste"].idxmax()], "menor_MSE": g.loc[g["MSE_todos"].idxmin()],
                   "menor_MSE_teste": g.loc[g["MSE_teste"].idxmin()]}
            cols = [f"MAE_{m}" for m in MESES.values()]
            met = [c for c in g.columns if c.startswith(("R_", "MSE_")) and g[c].notna().any()]
            bloco[nome] = {
                "escolhidos": {k: {c: round(float(v[c]), 4) for c in met + cols} for k, v in sel.items()},
                "todos_os_treinos_mediana": {c: round(float(g[c].median()), 4) for c in met + cols},
                "todos_os_treinos_p10_p90": {c: [round(float(g[c].quantile(q)), 4) for q in (0.1, 0.9)] for c in cols},
            }
        resumo[conjunto] = bloco
        print(f"[{tag}] {conjunto} pronto em {bloco['segundos']}s", flush=True)
    json.dump(resumo, open(out / args.saida, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
