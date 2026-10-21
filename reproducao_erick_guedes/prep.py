"""Reproduz o pre-processamento de Guedes (2020) para o teor de Fe do concentrado (B5).

Passos, como na dissertacao (sec. 3.1-3.2) e nos notebooks 06/04b do Erick:
  1. Para cada analise de laboratorio no instante t, a janela de processo e
     (t - 2h - atraso, t - atraso]. A dissertacao usa atraso 0 (conferido pela correlacao
     de 0,32 com o Fe); a pasta "Delay" do Erick e um experimento posterior com atraso de 1 h.
  2. Descarta medicoes iguais a 0 ou invalidas (`Bad`), como o notebook 06.
  3. Mediana de cada janela; janela sem dado fica NaN ("agrupados").
  4. Preenche cada sequencia de NaN com a media do ultimo valor anterior e do
     proximo valor valido (ou com o unico que existir), mes a mes, como o 04b.
  5. Confere a reducao de variaveis em marco: disponibilidade > 85%,
     correlacoes da Tabela 3.3 e o RReliefF (k = 53) sobre as 21 variaveis.

Uso: python prep.py [--atrasos 0] [--fonte originais]
"""
import argparse, json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent                       # raiz do repositorio datasets (pasta raw/)
MESES = {1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai"}

# Ordem das 65 variaveis do I_Conceicao.xlsx (confirmada com a dissertacao)
CELULAS = ["R1", "R2", "C1", "C2", "RC", "S1B1", "S1B2", "S1B3", "S2B1", "S2B2", "S2B3"]
NOMES = (["CA_nivel", "CA_densidade", "CA_vazao_vol", "CA_vazao_mas", "CA_vazao_amina", "CA_vazao_amido",
          "CR_nivel", "CR_densidade", "CR_vazao_vol", "CR_vazao_mas"]
         + [f"{c}_{v}" for c in CELULAS for v in ["espuma", "ar", "dardo1", "dardo2", "valv_ar"]])

# Variaveis da dissertacao: 15 escolhidas pelo RReliefF (na ordem de peso da sec. 4.1),
# 21 que chegaram a 4a etapa e 26 que restaram apos a 2a etapa (Figura 3.4)
SEL15 = ["CR_densidade", "CA_vazao_amina", "CR_vazao_vol", "CA_densidade", "RC_espuma", "CA_vazao_amido",
         "R2_espuma", "CA_nivel", "C1_dardo1", "S1B2_espuma", "R1_espuma", "S1B3_espuma", "CA_vazao_vol",
         "S2B3_ar", "C1_espuma"]
# Na S1B1 o Erick ficou com a dardo 2 (rotulo da Figura 3.4; a dardo 1 tem so 67% de janelas em marco)
ETAPA3_21 = SEL15 + ["CR_nivel", "R1_ar", "C1_ar", "S1B1_espuma", "S1B1_dardo2", "S1B2_dardo1"]
ETAPA2_26 = ETAPA3_21 + ["R2_ar", "C2_espuma", "C2_ar", "C2_dardo1", "RC_dardo1"]
TABELA_3_3 = [("R1_ar", "R2_ar", 0.98), ("C1_espuma", "C2_espuma", 0.92), ("C1_ar", "C2_ar", 0.98),
              ("C1_dardo1", "C2_dardo1", 0.93), ("C1_dardo1", "RC_dardo1", 0.92)]


def carregar(fonte="originais"):
    """fonte="originais": raw/B5_processo_originais_longo.parquet (Dados_Conceicao_*.xlsx do Erick, com segundos);
    fonte="i_conceicao": raw/B5_I_Conceicao_longo.parquet (mesmos valores, hora truncada no minuto)."""
    if fonte == "originais":
        longo = pd.read_parquet(DATA / "raw/B5_processo_originais_longo.parquet")
        longo["variavel"] = longo["variavel"].astype(str)
    else:
        longo = pd.read_parquet(DATA / "raw/B5_I_Conceicao_longo.parquet")
        longo["variavel"] = longo["variavel"].cat.codes.map(dict(enumerate(NOMES)))
    validas = longo["valor"].notna() & (longo["valor"] != 0)
    longo = longo[validas]
    alvo = pd.read_csv(DATA / "raw/B5_T_Conceicao.csv")
    alvo["data_hora"] = pd.to_datetime(alvo["date"], format="%d-%b-%y %H:%M:%S")
    alvo = alvo.rename(columns={"P_PF1CN_QQ_GLOBAL_FE": "fe", "P_PF1CN_QQ_GLOBAL_SIO2": "si"})
    alvo = alvo[alvo["data_hora"].dt.month.isin(MESES)][["data_hora", "fe", "si"]].reset_index(drop=True)
    return longo, alvo


def agrupar(longo, alvo, atraso_h):
    """Mediana de cada variavel na janela (t - 2h - atraso, t - atraso]."""
    t = alvo["data_hora"].values
    hi = t - np.timedelta64(int(atraso_h * 60), "m")
    lo = hi - np.timedelta64(120, "m")
    out = {}
    for nome, g in longo.groupby("variavel", sort=False):
        g = g.sort_values("data_hora", kind="stable")
        ts, v = g["data_hora"].values, g["valor"].values
        a = np.searchsorted(ts, lo, side="right")
        b = np.searchsorted(ts, hi, side="right")
        out[nome] = [np.median(v[i:j]) if j > i else np.nan for i, j in zip(a, b)]
    # variaveis sempre zero (vazao de ar de S1B1, S1B3, S2B1) somem ao descartar os zeros
    return pd.DataFrame(out).reindex(columns=NOMES)


def preencher(col):
    """Regra do notebook 04b: cada sequencia de NaN recebe a media do anterior e do proximo."""
    v = col.to_numpy(dtype=float).copy()
    isna = np.isnan(v)
    i, n = 0, len(v)
    while i < n:
        if not isna[i]:
            i += 1
            continue
        j = i
        while j < n and isna[j]:
            j += 1
        ant = v[i - 1] if i > 0 else np.nan
        prox = v[j] if j < n else np.nan
        viz = [x for x in (ant, prox) if not np.isnan(x)]
        v[i:j] = np.mean(viz) if viz else np.nan
        i = j
    return pd.Series(v, index=col.index)


def rrelieff(X, y, k=53, sigma=50.0):
    """RReliefF (Robnik-Sikonja & Kononenko, 2003), como o relieff do MATLAB para regressao."""
    rng_x = X.max(0) - X.min(0)
    rng_x[rng_x == 0] = 1
    Xn = (X - X.min(0)) / rng_x
    yn = (y - y.min()) / (y.max() - y.min())
    D = np.abs(Xn[:, None, :] - Xn[None, :, :]).sum(2)
    np.fill_diagonal(D, np.inf)
    viz = np.argsort(D, axis=1, kind="stable")[:, :k]
    w = np.exp(-((np.arange(1, k + 1) / sigma) ** 2))
    w /= w.sum()
    dy = np.abs(yn[:, None] - yn[viz])                       # n x k
    dA = np.abs(Xn[:, None, :] - Xn[viz])                     # n x k x a
    NdC = (dy * w).sum()
    NdA = (dA * w[None, :, None]).sum((0, 1))
    NdCdA = (dy[:, :, None] * dA * w[None, :, None]).sum((0, 1))
    m = X.shape[0]
    return NdCdA / NdC - (NdA - NdCdA) / (m - NdC)


def checar_reducao(ag, pre, alvo):
    mar = (alvo["data_hora"].dt.month == 3).to_numpy()
    disp = ag[mar].notna().mean()
    ficam = disp[disp > 0.85].index.tolist()
    rel = {"amostras_marco": int(mar.sum()),
           "etapa1_ficam": len(ficam), "etapa1_esperado": 32,
           "etapa1_lista": ficam,
           "etapa2_26_fora_da_etapa1": [v for v in ETAPA2_26 if v not in ficam]}
    X = pre[mar]
    fe = alvo.loc[mar, "fe"].to_numpy()
    rel["tabela_3_3"] = [{"par": [a, b], "erick": r, "nosso": round(float(np.corrcoef(X[a], X[b])[0, 1]), 3)}
                         for a, b, r in TABELA_3_3]
    corr_fe = {v: round(float(np.corrcoef(X[v], fe)[0, 1]), 3) for v in ETAPA2_26}
    rel["corr_fe"] = dict(sorted(corr_fe.items(), key=lambda kv: -abs(kv[1])))
    rel["max_abs_corr_fe"] = {"erick": 0.32, "nosso": max(abs(c) for c in corr_fe.values())}
    W = rrelieff(X[ETAPA3_21].to_numpy(), fe)
    ordem = sorted(zip(ETAPA3_21, W), key=lambda kv: -kv[1])
    rel["rrelieff"] = [{"var": v, "peso": round(float(p), 5)} for v, p in ordem]
    positivos = [v for v, p in ordem if p > 0]
    rel["rrelieff_positivos"] = len(positivos)
    rel["rrelieff_iguais_aos_15_do_erick"] = len(set(positivos) & set(SEL15))
    return rel


def selecao_automatica(ag, pre, alvo, criterio="marco"):
    """Reducao de variaveis da sec. 3.2 aplicada do zero, com as regras escritas na dissertacao.

    1. disponibilidade: fica a variavel com no maximo 15% de janelas vazias. criterio="marco" olha so
       o mes de treino; criterio="marco_e_periodo" exige isso em marco e tambem em jan-mai inteiro
       (a variavel precisa estar disponivel para o soft sensor ser aplicado nos outros meses);
    2. redundancia qualitativa: sai a vazao massica (calculada) e, na mesma celula, a valvula
       dardo 2 (mesmo setpoint da dardo 1) e a abertura da valvula de ar (redundante com a vazao de ar);
    3. redundancia quantitativa: em pares com |r| >= 0,90 fica a variavel mais a montante
       (R1 antes de R2, C1 antes de C2 e RC), como nos pares da Tabela 3.3;
    4. relevancia: RReliefF (k = 53) mantem os pesos positivos; PCA mantem os componentes que
       somam mais de 90% da variancia.
    """
    mar = (alvo["data_hora"].dt.month == 3).to_numpy()
    disp = ag[mar].notna().mean()
    if criterio == "marco_e_periodo":
        disp = np.minimum(disp, ag.notna().mean())
    e1 = [v for v in NOMES if disp[v] > 0.85]
    e2 = []
    for v in e1:
        cel, var = v.split("_", 1)
        if var == "vazao_mas":
            continue
        if var == "dardo2" and f"{cel}_dardo1" in e1:
            continue
        if var == "valv_ar" and f"{cel}_ar" in e1:
            continue
        e2.append(v)
    X = pre.loc[mar, e2]
    C = X.corr().abs()
    e3, pares = [], []
    for v in e2:                                   # NOMES segue a ordem do processo
        par = next((k for k in e3 if C.loc[v, k] >= 0.90), None)
        if par is None:
            e3.append(v)
        else:
            pares.append({"mantida": par, "removida": v, "r": round(float(C.loc[v, par]), 3)})
    fe = alvo.loc[mar, "fe"].to_numpy()
    W = rrelieff(pre.loc[mar, e3].to_numpy(), fe)
    pesos = sorted(zip(e3, W), key=lambda kv: -kv[1])
    e4 = [v for v, p in pesos if p > 0]
    Xn = pre.loc[mar, e3].to_numpy()
    Xn = (Xn - Xn.min(0)) / np.where(Xn.max(0) > Xn.min(0), Xn.max(0) - Xn.min(0), 1)
    ev = np.linalg.svd(Xn - Xn.mean(0), compute_uv=False) ** 2
    acum = np.cumsum(ev) / ev.sum()
    n_pca = int(np.searchsorted(acum, 0.90, side="right") + 1)
    comp = lambda a, b: {"so_aqui": [v for v in a if v not in b], "so_erick": [v for v in b if v not in a]}
    return {
        "criterio_disponibilidade": criterio,
        "disponibilidade_pct": {v: round(100 * float(disp[v]), 1) for v in NOMES},
        "etapa1_disponibilidade": e1, "etapa2_qualitativa": e2, "etapa3_correlacao": e3,
        "etapa3_pares_removidos": pares, "etapa4_rrelieff": e4,
        "etapa4_pesos": [{"var": v, "peso": round(float(p), 5)} for v, p in pesos],
        "etapa4_pca_componentes": n_pca, "etapa4_pca_variancia": round(float(acum[n_pca - 1]), 4),
        "contagens": {"aqui": [len(e1), len(e2), len(e3), len(e4), n_pca], "erick": [32, 26, 21, 15, 10]},
        "diferencas_etapa2_vs_erick": comp(e2, ETAPA2_26),
        "diferencas_etapa3_vs_erick": comp(e3, ETAPA3_21),
        "diferencas_rrelieff_vs_erick": comp(e4, SEL15),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atrasos", type=float, nargs="+", default=[0])
    ap.add_argument("--fonte", choices=["i_conceicao", "originais"], default="originais")
    args = ap.parse_args()
    longo, alvo = carregar(args.fonte)
    prefixo = "orig_" if args.fonte == "originais" else ""   # nao sobrescreve a rodada com o I_Conceicao
    (ROOT / "dados").mkdir(exist_ok=True)
    relatorio = {"amostras_por_mes": alvo["data_hora"].dt.month.map(MESES).value_counts().to_dict()}
    for atraso in args.atrasos:
        ag = agrupar(longo, alvo, atraso)
        mes = alvo["data_hora"].dt.month
        pre = ag.groupby(mes, group_keys=False).apply(lambda d: d.apply(preencher))
        tag = f"{prefixo}atraso{atraso:g}h"
        base = alvo.assign(mes=mes.map(MESES))
        pd.concat([base, ag], axis=1).to_parquet(ROOT / f"dados/agrupados_{tag}.parquet", index=False)
        pd.concat([base, pre], axis=1).to_parquet(ROOT / f"dados/preenchidos_{tag}.parquet", index=False)
        relatorio[tag] = checar_reducao(ag, pre, alvo)
        r = relatorio[tag]
        print(f"[{tag}] etapa1 ficam {r['etapa1_ficam']} (Erick 32) | max|corr Fe| {r['max_abs_corr_fe']['nosso']} "
              f"(Erick 0.32) | RReliefF positivos {r['rrelieff_positivos']}, {r['rrelieff_iguais_aos_15_do_erick']} dos 15 do Erick")
        for t in r["tabela_3_3"]:
            print(f"    {t['par']}: Erick {t['erick']} nosso {t['nosso']}")
        # "" = so marco (como escrito na dissertacao); "_disp" = marco e jan-mai
        for sufixo, kw in [("", {}), ("_disp", {"criterio": "marco_e_periodo"})]:
            sel = selecao_automatica(ag, pre, alvo, **kw)
            relatorio[tag]["ponta_a_ponta" + sufixo] = sel
            json.dump(sel, open(ROOT / f"dados/selecao_{tag}{sufixo}.json", "w"), ensure_ascii=False, indent=1)
            print(f"    ponta a ponta{sufixo or ' (so marco)'}: etapas {sel['contagens']['aqui']} "
                  f"(Erick {sel['contagens']['erick']}) | etapa 2 {sel['diferencas_etapa2_vs_erick']} | "
                  f"RReliefF {sel['diferencas_rrelieff_vs_erick']}")
    (ROOT / "resultados").mkdir(exist_ok=True)
    json.dump(relatorio, open(ROOT / f"resultados/prep_relatorio{'_orig' if prefixo else ''}.json", "w"),
              ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    main()
