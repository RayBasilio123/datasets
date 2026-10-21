"""MAE, MSE, R e R2 dos modelos escolhidos (Figs. 4.4-4.11) contra os valores da dissertacao.

O Erick reporta R (treino, validacao, teste, todos), MSE em todas as amostras de marco e MAE por mes; nao reporta R2.
Para comparar, o R2 dele e estimado como 1 - MSE / variancia do Fe de marco (o MSE dele e em todas as amostras).
Aqui o R2 e o coeficiente de determinacao, 1 - SQE/SQT, calculado em cada conjunto (nao e R ao quadrado).

Uso: python metricas_escolhidos.py   -> resultados/orig_atraso0h_matlab/metricas_escolhidos.md
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from modelos import MLP, dividir, entradas

ROOT = Path(__file__).resolve().parent
TAG, DIR = "orig_atraso0h", ROOT / "resultados" / "orig_atraso0h_matlab"
MESES = ["mar", "jan", "fev", "abr", "mai"]
NOME_MES = {"mar": "Mar*", "jan": "Jan", "fev": "Fev", "abr": "Abr", "mai": "Mai"}
ESCOLHAS = [  # figura, conjunto, modelo, criterio, crescente, valores do Erick
    ("Fig. 4.4", "rrelieff15", "rna", "R_teste", False, "RNA LM, RReliefF, maior R no teste",
     dict(R_treino=0.88569, R_validacao=0.21095, R_teste=0.77021, R_todos=0.78218, MSE_todos=1.2395)),
    ("Fig. 4.5 / 4.8–4.9", "rrelieff15", "rna", "MSE_todos", True, "RNA LM, RReliefF, menor MSE (adotada)",
     dict(R_treino=0.9436, R_validacao=0.38838, R_teste=0.60117, R_todos=0.87122, MSE_todos=0.749783,
          MAE_mar=0.6132, MAE_jan=1.8890, MAE_fev=2.3933, MAE_abr=2.1705, MAE_mai=2.1016)),
    ("Fig. 4.6 / 4.10–4.11", "pca10", "rf", "R_teste", False, "RF, PCA, maior R no teste (adotada)",
     dict(R_treino=0.88099, R_teste=0.77097, R_todos=0.86341, MSE_todos=1.2382,
          MAE_mar=0.5904, MAE_jan=0.9645, MAE_fev=1.0625, MAE_abr=1.3007, MAE_mai=1.1816)),
    ("Fig. 4.7", "rrelieff15", "rf", "MSE_todos", True, "RF, RReliefF, menor MSE",
     dict(R_treino=0.89788, R_teste=0.43437, R_todos=0.87808, MSE_todos=1.0181)),
]


def metricas(y, p):
    e = y - p
    sqt = np.sum((y - y.mean()) ** 2)
    return {"MAE": np.mean(np.abs(e)), "MSE": np.mean(e ** 2), "R": np.corrcoef(y, p)[0, 1], "R2": 1 - np.sum(e ** 2) / sqt}


def f(x, n=3):
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{n}f}".replace(".", ",")


def main():
    df = pd.read_parquet(ROOT / f"dados/preenchidos_{TAG}.parquet")
    y_all, meses = df["fe"].to_numpy(float), df["mes"].to_numpy()
    mar_idx = np.flatnonzero(meses == "mar")
    var_mar = np.var(y_all[mar_idx])
    md = ["# MAE, MSE, R e R² dos modelos escolhidos vs. dissertação", "",
          "R² aqui = coeficiente de determinação (1 − SQE/SQT) em cada conjunto; não é R ao quadrado.",
          f"R² do Erick (não reportado) estimado como 1 − MSE/variância do Fe de março (variância = {f(var_mar)}).",
          "Nos meses, o R² usa a média do próprio mês: negativo = erra mais do que a média do mês.", ""]
    for fig, conj, mod, col, asc, titulo, erick in ESCOLHAS:
        res = pd.read_csv(DIR / f"treinos_{conj}.csv")
        g = res[res.modelo == mod].sort_values(col, ascending=asc).iloc[0]
        s, c = int(g.divisao), int(g.ciclo)
        X_all, _ = entradas(df, conj, TAG)
        Xm, ym = X_all[mar_idx], y_all[mar_idx]
        tr, va, te = dividir(len(ym), seed=1000 + s, razoes=(75, 15, 15))
        seed = s * 100 + c
        if mod == "rf":
            m = RandomForestRegressor(n_estimators=500, min_samples_leaf=3, max_features=1 / 3, random_state=seed,
                                      n_jobs=4).fit(Xm[np.r_[tr, va]], ym[np.r_[tr, va]])
            sub = {"treino": np.r_[tr, va], "teste": te}
        else:
            m = MLP("lm", seed=seed, saida="tansig").fit(Xm[tr], ym[tr], Xm[va], ym[va])
            sub = {"treino": tr, "validacao": va, "teste": te}
        sub["todos"] = np.arange(len(ym))
        p_all = m.predict(X_all)
        pm = p_all[mar_idx]
        md += [f"## {fig} — {titulo}", "", f"Treino escolhido: divisão {s}, ciclo {c}.", "",
               "| Conjunto | R Erick | R aqui | MSE Erick | MSE aqui | R² Erick (estimado) | R² aqui | MAE aqui |",
               "|---|---|---|---|---|---|---|---|"]
        for k, ix in sub.items():
            q = metricas(ym[ix], pm[ix])
            mse_e = erick.get("MSE_todos") if k == "todos" else None
            r2_e = 1 - mse_e / var_mar if mse_e is not None else None
            md.append(f"| {k} (março) | {f(erick.get('R_' + k))} | {f(q['R'])} | {f(mse_e)} | {f(q['MSE'])} | "
                      f"{f(r2_e)} | {f(q['R2'])} | {f(q['MAE'])} |")
        md += ["", "| Mês | MAE Erick | MAE aqui | MSE aqui | R aqui | R² aqui |", "|---|---|---|---|---|---|"]
        for mes in MESES:
            k = meses == mes
            q = metricas(y_all[k], p_all[k])
            md.append(f"| {NOME_MES[mes]} | {f(erick.get('MAE_' + mes))} | {f(q['MAE'])} | {f(q['MSE'])} | "
                      f"{f(q['R'])} | {f(q['R2'])} |")
        md.append("")
    md.append("\\* março é o mês de treino (inclui as amostras usadas no ajuste).")
    (DIR / "metricas_escolhidos.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
