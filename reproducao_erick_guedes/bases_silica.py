"""Metodologia de Guedes (2020) aplicada ao teor de SiO2 do concentrado, na B5 e nas outras bases (B1-B4).

Os passos e os modelos sao os da dissertacao (prep.py e modelos.py, protocolo do MATLAB do Erick). O que muda
de base para base, porque os dados sao diferentes:
  - amostras: uma por analise de laboratorio. Na B5 a janela de 2 h e refeita dos dados de 20 s (prep.py).
    B1 e B4 ja vem em janelas de 2 h e a B2 em janelas de 1 h (nao ha o dado bruto para refazer a mediana);
    a B3 vem por hora e cada analise vale para 2 registros, que viram uma janela pela mediana. Valor de
    laboratorio igual ao do registro anterior e preenchimento, nao analise nova, e sai;
  - entradas: so variaveis de processo medidas em tempo real. Saem as analises de laboratorio (como na
    dissertacao, sec. 3.1), os estados de motor (categoricos), as medias moveis de analises e contadores;
  - medicoes invalidas: zero (como o notebook 06) e valores absurdos, fora de [Q1 - 10 IQR, Q3 + 10 IQR];
  - mes de treino: o mes com pelo menos 75% das analises esperadas mais perto do meio do periodo, como marco
    na B5 ("no centro do intervalo disponivel", sec. 3.2). Os outros meses sao o teste;
  - etapa 2 (redundancia qualitativa): na B5, a lista do Erick. Na B3 saem o tempo de residencia e a
    velocidade superficial do ar, calculados da vazao e da vazao de ar. Nas outras bases nao ha variavel
    calculada identificavel pelo nome e a etapa 3 (correlacao >= 0,90) cobre a redundancia.
Na B5 as etapas 1-3 nao dependem do alvo e ficam as do Erick (21 variaveis); so o RReliefF e refeito.

Referencias: repetir a media do mes de treino (como no README) e repetir o ultimo resultado de laboratorio.

Uso: python bases_silica.py --bases B5 B1 B2 B3 B4 [--alvo si] [--workers 32]
"""
import argparse, json, os, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor

from modelos import MLP, avaliar, dividir
from prep import ETAPA3_21, NOMES, preencher, rrelieff

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent

BASES = {
    "B1": dict(arquivo="raw/B1_dados_2h_aggregado_final.csv", data="Data", freq_h=2,
               alvo={"si": "P_CONFLTTO_QQ_GLOBAL_SIO2", "fe": "P_CONFLTTO_QQ_GLOBAL_FE"},
               fora=lambda c: c.startswith("P_") or c.endswith("_EST1")),          # laboratorio e estados
    "B2": dict(arquivo="raw/B2_data_hourly.csv", data="date", freq_h=1,
               alvo={"si": "% Silica Concentrate", "fe": "% Iron Concentrate"},
               fora=lambda c: c.startswith("%")),                                    # laboratorio
    "B3": dict(arquivo="raw/B3_flotacao_conceicao.csv", data="date", freq_h=2, agrupar_2h=True,
               alvo={"si": "SiO2 C flot (%)", "fe": "Fe C flot (%)"},
               fora=lambda c: c.endswith("(%)") and not c.startswith("Nível"),      # granulometria e quimica
               calculadas=lambda c: c.startswith(("Tem Res", "Est Esp"))),
    "B4": dict(arquivo="raw/B4_dados_consolidados_com_MM.csv", data="Data", freq_h=2,
               alvo={"si": "P_CONFLTTO_QQ_GLOBAL_SIO2", "fe": "P_CONFLTTO_QQ_GLOBAL_FE"},
               fora=lambda c: c.startswith(("P_", "estado_")) or c.endswith("_MM")
               or c in ("silica_alimentacao_geral", "grupo_mudanca")),
    "B5": dict(freq_h=2),
}
NOMES_MODELO = {"rna": "RNA LM", "rna_scg": "RNA SCG", "rf": "RF"}


def carregar(b, alvo):
    """Uma linha por analise: data e hora, alvo e variaveis de processo (NaN onde a medicao e invalida)."""
    if b == "B5":
        ag = pd.read_parquet(ROOT / "dados/agrupados_orig_atraso0h.parquet")   # prep.py: janelas e zeros
        return ag["data_hora"], ag[alvo].to_numpy(float), ag[NOMES]
    cfg = BASES[b]
    df = pd.read_csv(DATA / cfg["arquivo"], low_memory=False)
    t = pd.to_datetime(df[cfg["data"]])
    y = df[cfg["alvo"][alvo]].astype(float)
    X = df[[c for c in df.columns if c != cfg["data"] and not cfg["fora"](c)]].apply(pd.to_numeric, errors="coerce")
    X = X.where(X != 0)
    for c in X:
        q1, q3 = X[c].quantile([0.25, 0.75])
        if q3 > q1:
            X[c] = X[c].where(X[c].between(q1 - 10 * (q3 - q1), q3 + 10 * (q3 - q1)))
    if cfg.get("agrupar_2h"):
        bloco = t.dt.floor("2h").to_numpy()
        X, y = X.groupby(bloco).median(), y.groupby(bloco).first()
        t = pd.Series(X.index)
    nova = (y.ne(y.shift()) & y.notna()).to_numpy()
    return (t[nova].reset_index(drop=True), y[nova].to_numpy(float), X[nova].reset_index(drop=True))


def mes_de_treino(t, freq_h):
    mes = t.dt.to_period("M")
    n = mes.value_counts()
    ok = [m for m in n.index if n[m] >= 0.75 * m.days_in_month * 24 / freq_h]
    meio = t.min() + (t.max() - t.min()) / 2
    return str(min(ok, key=lambda m: abs(m.start_time + (m.end_time - m.start_time) / 2 - meio)))


def selecionar(b, ag, pre, y, mtr):
    """Etapas 1-4 da sec. 3.2 (ver prep.selecao_automatica)."""
    if b == "B5":
        e1 = e2 = None
        e3, pares = list(ETAPA3_21), []
    else:
        disp = np.minimum(ag[mtr].notna().mean(), ag.notna().mean())
        e1 = [v for v in ag if disp[v] > 0.85 and pre.loc[mtr, v].std() > 0]
        calc = BASES[b].get("calculadas", lambda c: False)
        e2 = [v for v in e1 if not calc(v)]
        C = pre.loc[mtr, e2].corr().abs()
        e3, pares = [], []
        for v in e2:                                   # fica a primeira do par, na ordem do arquivo
            par = next((k for k in e3 if C.loc[v, k] >= 0.90), None)
            if par is None:
                e3.append(v)
            else:
                pares.append({"mantida": par, "removida": v, "r": round(float(C.loc[v, par]), 3)})
    W = rrelieff(pre.loc[mtr, e3].to_numpy(), y[mtr])
    pesos = sorted(zip(e3, W), key=lambda kv: -kv[1])
    e4 = [v for v, p in pesos if p > 0]
    Xn = pre.loc[mtr, e3].to_numpy()
    Xn = (Xn - Xn.min(0)) / np.where(Xn.max(0) > Xn.min(0), Xn.max(0) - Xn.min(0), 1)
    ev = np.linalg.svd(Xn - Xn.mean(0), compute_uv=False) ** 2
    acum = np.cumsum(ev) / ev.sum()
    n_pca = int(np.searchsorted(acum, 0.90, side="right") + 1)
    return {"variaveis_de_processo": list(ag.columns), "etapa1_disponibilidade": e1, "etapa2_qualitativa": e2,
            "etapa3_correlacao": e3, "etapa3_pares_removidos": pares, "etapa4_rrelieff": e4,
            "etapa4_pesos": [{"var": v, "peso": round(float(p), 5)} for v, p in pesos],
            "etapa4_pca_componentes": n_pca, "etapa4_pca_variancia": round(float(acum[n_pca - 1]), 4),
            "contagens": [ag.shape[1]] + [len(e) if e is not None else None for e in (e1, e2, e3, e4)] + [n_pca]}


def entradas(pre, sel, conjunto, mtr):
    """Como modelos.entradas: variaveis do RReliefF, ou PCA das variaveis da etapa 3 normalizadas pelo mes de treino."""
    if conjunto == "rrelieff":
        return pre[sel["etapa4_rrelieff"]].to_numpy(float)
    X = pre[sel["etapa3_correlacao"]].to_numpy(float)
    lo, hi = X[mtr].min(0), X[mtr].max(0)
    Xn = (X - lo) / np.where(hi > lo, hi - lo, 1)
    return PCA(n_components=sel["etapa4_pca_componentes"]).fit(Xn[mtr]).transform(Xn)


def metricas(y, p):
    e = y - p
    sqt = np.sum((y - y.mean()) ** 2)
    r = np.corrcoef(y, p)[0, 1] if np.ptp(p) > 0 and np.ptp(y) > 0 else np.nan
    return {"MAE": np.mean(np.abs(e)), "MSE": np.mean(e ** 2), "R": r, "R2": 1 - np.sum(e ** 2) / sqt}


def avaliacoes(y, p, mes, fora):
    """Metricas fora do mes de treino (todos os outros meses juntos) e mes a mes."""
    out = {}
    for k, ix in [("fora", fora)] + [(m, mes == m) for m in sorted(set(mes))]:
        out.update({f"{n}_{k}": float(v) for n, v in metricas(y[ix], p[ix]).items()})
    return out


def rodar_divisao(args):
    """Como modelos.rodar_divisao com protocolo "matlab": 5 ciclos por divisao 75/15/15 do mes de treino."""
    s, ciclos, X, y, mes, idx_tr = args
    Xm, ym = X[idx_tr], y[idx_tr]
    tr, va, te = dividir(len(ym), seed=1000 + s, razoes=(75, 15, 15))
    trva, todos = np.r_[tr, va], np.arange(len(ym))
    fora = ~np.isin(np.arange(len(y)), idx_tr)
    linhas = []
    for c in range(ciclos):
        seed = s * 100 + c
        modelos = {
            "rna": MLP("lm", seed=seed, saida="tansig").fit(Xm[tr], ym[tr], Xm[va], ym[va]),
            "rna_scg": MLP("scg", seed=seed, saida="tansig").fit(Xm[tr], ym[tr], Xm[va], ym[va]),
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
            pt = metricas(ym, pm)
            linha["MAE_todos"], linha["R2_todos"] = float(pt["MAE"]), float(pt["R2"])
            linha.update(avaliacoes(y, m.predict(X), mes, fora))
            linhas.append(linha)
    return linhas


def rodar_base(b, alvo, divisoes, ciclos, workers, saida, sem_extremos=False):
    t0 = time.time()
    t, y, ag = carregar(b, alvo)
    n_extremos = 0
    if sem_extremos:                                 # como o csv_to_gluonts.py do Basilio2026: |z| > 3 sai
        ok = np.abs(y - y.mean()) <= 3 * y.std()
        n_extremos = int((~ok).sum())
        t, y, ag = t[ok].reset_index(drop=True), y[ok], ag[ok].reset_index(drop=True)
    mes = t.dt.strftime("%Y-%m").to_numpy()
    m_tr = mes_de_treino(t, BASES[b]["freq_h"])
    mtr = mes == m_tr
    pre = pd.concat([g.apply(preencher) for _, g in ag.groupby(mes)]).loc[ag.index]   # 04b, mes a mes
    pre = pre.apply(preencher)                       # mes inteiro sem dado: vizinhos dos meses ao lado
    sel = selecionar(b, ag, pre, y, mtr)
    idx_tr, fora = np.flatnonzero(mtr), ~mtr
    out = saida / b
    out.mkdir(parents=True, exist_ok=True)
    resumo = {"base": b, "alvo": alvo, "extremos_removidos": n_extremos,
              "mes_treino": m_tr, "amostras": int(len(y)), "amostras_treino": int(mtr.sum()),
              "meses": {m: int((mes == m).sum()) for m in sorted(set(mes))}, "divisoes": divisoes, "ciclos": ciclos,
              "selecao": sel}
    media_tr = np.full(len(y), y[mtr].mean())
    anterior = np.r_[np.nan, y[:-1]]                    # ultimo resultado de laboratorio antes desta analise
    ok = ~np.isnan(anterior)
    resumo["referencias"] = {
        "media_do_mes_de_treino": {**{f"{n}_treino": float(v) for n, v in metricas(y[mtr], media_tr[mtr]).items()},
                                   **avaliacoes(y, media_tr, mes, fora)},
        "ultimo_resultado": {**{f"{n}_treino": float(v) for n, v in metricas(y[mtr & ok], anterior[mtr & ok]).items()},
                             **avaliacoes(y[ok], anterior[ok], mes[ok], fora[ok])},
    }
    for conjunto in ["rrelieff", "pca"]:
        X = entradas(pre, sel, conjunto, mtr)
        tarefas = [(s, ciclos, X, y, mes, idx_tr) for s in range(divisoes)]
        with ProcessPoolExecutor(workers) as ex:
            res = pd.DataFrame([l for bloco in ex.map(rodar_divisao, tarefas) for l in bloco])
        res.to_parquet(out / f"treinos_{conjunto}.parquet", index=False)
        bloco = {}
        for nome, g in res.groupby("modelo"):
            esc = {"maior_R": g.loc[g["R_teste"].idxmax()], "menor_MSE": g.loc[g["MSE_todos"].idxmin()]}
            met = [c for c in g.columns if c not in ("divisao", "ciclo", "modelo") and g[c].notna().any()]
            bloco[nome] = {"escolhidos": {k: {"divisao": int(v["divisao"]), "ciclo": int(v["ciclo"]),
                                              **{c: round(float(v[c]), 4) for c in met}} for k, v in esc.items()},
                           "mediana_dos_treinos": {c: round(float(g[c].median()), 4) for c in met}}
        resumo[conjunto] = bloco
    resumo["segundos"] = round(time.time() - t0)
    json.dump(resumo, open(out / "resumo.json", "w"), ensure_ascii=False, indent=1)
    print(f"[{b}] alvo {alvo}, treino {m_tr} ({mtr.sum()} analises), etapas {sel['contagens']}, "
          f"{resumo['segundos']}s", flush=True)
    return resumo


# ---------------------------------------------------------------- relatorio
def f(x, n=3):
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{n}f}".replace(".", ",")


def linhas_modelos(r):
    """(rotulo, dicionario de metricas) na ordem do relatorio."""
    ref = r["referencias"]
    yield "RNA LM, RReliefF, menor MSE (adotada pelo Erick)", r["rrelieff"]["rna"]["escolhidos"]["menor_MSE"]
    yield "RF, PCA, maior R no teste (adotada pelo Erick)", r["pca"]["rf"]["escolhidos"]["maior_R"]
    for conj, nome_c in [("rrelieff", "RReliefF"), ("pca", "PCA")]:
        for mod in ["rna", "rna_scg", "rf"]:
            yield f"{NOMES_MODELO[mod]}, {nome_c}: mediana dos 1000 treinos", r[conj][mod]["mediana_dos_treinos"]
    for k, nome in [("media_do_mes_de_treino", "Referência: média do mês de treino"),
                    ("ultimo_resultado", "Referência: último resultado de laboratório")]:
        d = ref[k]
        yield nome, {"MAE_todos": d["MAE_treino"], "MSE_todos": d["MSE_treino"], "R_todos": d["R_treino"],
                     "R2_todos": d["R2_treino"], **{c: v for c, v in d.items() if not c.endswith("_treino")}}


def relatorio(resumos, saida, alvo):
    nome_alvo = {"si": "SiO₂", "fe": "Fe"}[alvo]
    md = [f"# Metodologia de Guedes (2020) para o teor de {nome_alvo} do concentrado, por base", "",
          "Gerado por `bases_silica.py`. Treino em um mês (o mais perto do meio do período), 1000 treinos por modelo",
          "(200 divisões 75/15/15 × 5 ciclos), modelos e critérios de escolha do MATLAB do Erick.",
          "**Mês de treino**: todas as análises do mês (inclui as usadas no ajuste), como o MSE e o R \"todos\" do Erick.",
          "**Outros meses**: todos os meses fora do treino juntos. R² = 1 − SQE/SQT (não é R ao quadrado); "
          "negativo = erra mais do que a média do próprio período.", ""]
    for r in resumos:
        s = r["selecao"]
        c = s["contagens"]
        meses = [m for m in r["meses"] if m != r["mes_treino"]]
        extremos = f" ({r['extremos_removidos']} com |z| > 3 removidas)" if r.get("extremos_removidos") else ""
        md += [f"## {r['base']}", "",
               f"- {r['amostras']} análises{extremos} de {min(r['meses'])} a {max(r['meses'])}; treino em "
               f"**{r['mes_treino']}** ({r['amostras_treino']} análises), teste nos outros {len(meses)} meses.",
               f"- Seleção: {c[0]} variáveis de processo → disponibilidade {f(c[1], 0) if c[1] is not None else '32 (Erick)'}"
               f" → qualitativa {f(c[2], 0) if c[2] is not None else '26 (Erick)'} → correlação {c[3]} → "
               f"RReliefF {c[4]} | PCA {c[5]} componentes ({f(100 * s['etapa4_pca_variancia'], 1)}%).",
               f"- RReliefF (pesos > 0, em ordem): {', '.join('`' + v + '`' for v in s['etapa4_rrelieff'])}.", "",
               "| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |",
               "|---|---|---|---|---|---|---|---|---|"]
        for rot, d in linhas_modelos(r):
            md.append(f"| {rot} | {f(d.get('R_todos'))} | {f(d.get('MSE_todos'))} | {f(d.get('R2_todos'))} | "
                      f"{f(d.get('MAE_todos'))} | {f(d.get('R_fora'))} | {f(d.get('MSE_fora'))} | "
                      f"{f(d.get('R2_fora'))} | {f(d.get('MAE_fora'))} |")
        md += ["", "<details><summary>MAE e R² mês a mês</summary>", "",
               "| Mês | Análises | " + " | ".join(n for n in ["RNA adotada", "RF adotada", "Média do treino",
                                                                  "Último resultado"]) + " |",
               "|---|---|---|---|---|---|"]
        sel_rows = [r["rrelieff"]["rna"]["escolhidos"]["menor_MSE"], r["pca"]["rf"]["escolhidos"]["maior_R"],
                    r["referencias"]["media_do_mes_de_treino"], r["referencias"]["ultimo_resultado"]]
        for m, n in r["meses"].items():
            marca = "*" if m == r["mes_treino"] else ""
            md.append(f"| {m}{marca} | {n} | " + " | ".join(f"{f(d.get('MAE_' + m))} / {f(d.get('R2_' + m))}"
                                                           for d in sel_rows) + " |")
        md += ["", "Cada célula: MAE / R². \\* mês de treino.", "", "</details>", ""]
    (saida / "resumo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bases", nargs="+", default=["B5", "B1", "B2", "B3", "B4"])
    ap.add_argument("--alvo", choices=["si", "fe"], default="si")
    ap.add_argument("--divisoes", type=int, default=200)
    ap.add_argument("--ciclos", type=int, default=5)
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    ap.add_argument("--sem-extremos", action="store_true",
                    help="tira as analises com |z| > 3 no alvo, como o csv_to_gluonts.py do Basilio2026")
    ap.add_argument("--saida", default=None, help="padrao: resultados/silica[_sem_extremos] (ou ferro_bases)")
    args = ap.parse_args()
    nome = ("silica" if args.alvo == "si" else "ferro_bases") + ("_sem_extremos" if args.sem_extremos else "")
    saida = Path(args.saida) if args.saida else ROOT / "resultados" / nome
    saida.mkdir(parents=True, exist_ok=True)
    resumos = []
    for b in args.bases:
        resumos.append(rodar_base(b, args.alvo, args.divisoes, args.ciclos, args.workers, saida, args.sem_extremos))
    relatorio(resumos, saida, args.alvo)


if __name__ == "__main__":
    main()
