"""Compara os 1000 treinos de cada modelo com as metricas das Tabelas 4.1-4.8 e Figuras 4.4-4.7
de Guedes (2020). Le resultados/<tag>/treinos_*.csv e grava resultados/<tag>/metricas.md.

O MSE do Erick nao diz em qual conjunto foi calculado, entao cada tabela de MSE sai duas vezes:
no conjunto de teste e em todas as amostras de marco.

Uso: python metricas.py [--atraso 0]
"""
import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
COLS = [("rrelieff15", "rna"), ("rrelieff15", "rna_scg"), ("pca10", "rna"), ("pca10", "rna_scg")]
COLS_RF = [("rrelieff15", "rf"), ("pca10", "rf")]
ROT = {"rna": "LM", "rna_scg": "SCG", "rf": "RF", "rrelieff15": "RReliefF", "pca10": "PCA"}

ERICK = {
    "t4_1": {("rrelieff15", "rna"): [0.773509, 0.772578, 0.771459, 0.770209, 0.750907],
             ("rrelieff15", "rna_scg"): [0.669, 0.648349, 0.640266, 0.63914, 0.617288],
             ("pca10", "rna"): [0.715647, 0.707473, 0.69202, 0.688717, 0.685685],
             ("pca10", "rna_scg"): [0.553992, 0.53162, 0.510408, 0.507486, 0.500885]},
    "t4_2": {("rrelieff15", "rna"): (13, 50), ("rrelieff15", "rna_scg"): (0, 8),
             ("pca10", "rna"): (2, 15), ("pca10", "rna_scg"): (0, 0)},
    "t4_3": {("rrelieff15", "rna"): [0.749783, 0.857617, 0.957877, 1.018666, 1.020206],
             ("rrelieff15", "rna_scg"): [1.577013, 1.795156, 1.857298, 1.869756, 1.90809],
             ("pca10", "rna"): [0.926836, 1.358046, 1.401384, 1.439002, 1.475373],
             ("pca10", "rna_scg"): [2.260513, 2.278756, 2.295989, 2.364107, 2.3946]},
    "t4_4": {("rrelieff15", "rna"): (3, 43), ("rrelieff15", "rna_scg"): (0, 6),
             ("pca10", "rna"): (1, 14), ("pca10", "rna_scg"): (0, 0)},
    "t4_5": {("rrelieff15", "rf"): [0.74358, 0.740575, 0.734437, 0.731023, 0.726223],
             ("pca10", "rf"): [0.770967, 0.753743, 0.752114, 0.738834, 0.73813]},
    "t4_6": {("rrelieff15", "rf"): (10, 77), ("pca10", "rf"): (19, 74)},
    "t4_7": {("rrelieff15", "rf"): [1.018065, 1.020555, 1.023036, 1.024267, 1.0245],
             ("pca10", "rf"): [1.082903, 1.092677, 1.092994, 1.094296, 1.106025]},
    "t4_8": {("rrelieff15", "rf"): (0, 1000), ("pca10", "rf"): (0, 1000)},
    # figuras: R treino / validacao / teste / todos e MSE do modelo escolhido
    "figuras": [
        ("Fig. 4.4", "rrelieff15", "rna", "maior R no teste", dict(treino=0.88569, validacao=0.21095, teste=0.77021, todos=0.78218, MSE=1.2395)),
        ("Fig. 4.5", "rrelieff15", "rna", "menor MSE", dict(treino=0.9436, validacao=0.38838, teste=0.60117, todos=0.87122, MSE=0.749783)),
        ("Fig. 4.6", "pca10", "rf", "maior R no teste", dict(treino=0.88099, teste=0.77097, todos=0.86341, MSE=1.2382)),
        ("Fig. 4.7", "rrelieff15", "rf", "menor MSE", dict(treino=0.89788, teste=0.43437, todos=0.87808, MSE=1.0181)),
    ],
}


def f(x, n=3):
    return "—" if x is None or pd.isna(x) else f"{x:.{n}f}".replace(".", ",")


def top5(df, conj, mod, col, asc):
    g = df[(df.conjunto == conj) & (df.modelo == mod)]
    return g.sort_values(col, ascending=asc)[col].head(5).tolist()


def tabela_top(df, chave, cols, col, asc, titulo):
    linhas = [f"### {titulo}", "", "| Pos. | " + " | ".join(f"{ROT[c]} {ROT[m]} (Erick / aqui)" for c, m in cols) + " |",
              "|---|" + "---|" * len(cols)]
    nossos = {k: top5(df, *k, col, asc) for k in cols}
    for i in range(5):
        linhas.append(f"| {i + 1} | " + " | ".join(f"{f(ERICK[chave][k][i])} / {f(nossos[k][i])}" for k in cols) + " |")
    return linhas + [""]


def tabela_contagem(df, chave, cols, col, limites, maior, titulo):
    sinal = ">" if maior else "<"
    linhas = [f"### {titulo}", "", "| | " + " | ".join(f"{ROT[c]} {ROT[m]} (Erick / aqui)" for c, m in cols) + " |",
              "|---|" + "---|" * len(cols)]
    for j, lim in enumerate(limites):
        cel = []
        for k in cols:
            g = df[(df.conjunto == k[0]) & (df.modelo == k[1])][col]
            n = int((g > lim).sum() if maior else (g < lim).sum())
            cel.append(f"{ERICK[chave][k][j]} / {n}")
        linhas.append(f"| {col.split('_')[0]} {sinal} {f(lim, 1)} | " + " | ".join(cel) + " |")
    return linhas + [""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--atraso", type=float, default=0)
    ap.add_argument("--conjuntos", nargs=2, default=["rrelieff15", "pca10"],
                    help="conjuntos comparados com as colunas RReliefF e PCA do Erick, nessa ordem")
    ap.add_argument("--saida", default="metricas.md")
    ap.add_argument("--dir", default="orig_atraso0h_matlab", help="pasta em resultados/")
    args = ap.parse_args()
    out = ROOT / "resultados" / (args.dir or f"atraso{args.atraso:g}h")
    df = pd.concat([pd.read_csv(out / f"treinos_{c}.csv") for c in args.conjuntos], ignore_index=True)
    df["conjunto"] = df["conjunto"].map(dict(zip(args.conjuntos, ["rrelieff15", "pca10"])))
    md = [f"# Métricas dos 1000 treinos vs. Guedes (2020) — janela com atraso {args.atraso:g} h", "",
          f"Conjuntos de entrada comparados: {args.conjuntos[0]} (coluna RReliefF) e {args.conjuntos[1]} (coluna PCA).", "",
          "Formato das células: valor do Erick / valor desta reprodução. MSE em %² de Fe.", ""]
    md += ["## Redes neurais", ""]
    md += tabela_top(df, "t4_1", COLS, "R_teste", False, "Tabela 4.1 — maiores R no teste")
    md += tabela_contagem(df, "t4_2", COLS, "R_teste", [0.7, 0.6], True, "Tabela 4.2 — treinos com R alto no teste")
    for conj_mse, nome in [("MSE_teste", "no teste"), ("MSE_todos", "em todo março")]:
        md += tabela_top(df, "t4_3", COLS, conj_mse, True, f"Tabela 4.3 — menores MSE (aqui: MSE {nome})")
        md += tabela_contagem(df, "t4_4", COLS, conj_mse, [1, 2], False, f"Tabela 4.4 — treinos com MSE baixo (aqui: MSE {nome})")
    md += ["## Random Forest", ""]
    md += tabela_top(df, "t4_5", COLS_RF, "R_teste", False, "Tabela 4.5 — maiores R no teste")
    md += tabela_contagem(df, "t4_6", COLS_RF, "R_teste", [0.7, 0.6], True, "Tabela 4.6 — treinos com R alto no teste")
    for conj_mse, nome in [("MSE_teste", "no teste"), ("MSE_todos", "em todo março")]:
        md += tabela_top(df, "t4_7", COLS_RF, conj_mse, True, f"Tabela 4.7 — menores MSE (aqui: MSE {nome})")
        md += tabela_contagem(df, "t4_8", COLS_RF, conj_mse, [1, 2], False, f"Tabela 4.8 — treinos com MSE baixo (aqui: MSE {nome})")

    md += ["## Modelos escolhidos (Figuras 4.4–4.7)", "",
           "| Figura | Modelo | Critério | R treino | R validação | R teste | R todos | MSE | Origem |",
           "|---|---|---|---|---|---|---|---|---|"]
    for fig, conj, mod, crit, e in ERICK["figuras"]:
        g = df[(df.conjunto == conj) & (df.modelo == mod)]
        md.append(f"| {fig} | {ROT[mod]} {ROT[conj]} | {crit} | {f(e['treino'])} | {f(e.get('validacao'))} | "
                  f"{f(e['teste'])} | {f(e['todos'])} | {f(e['MSE'])} | Erick |")
        escolhas = [("R_teste", False, "MSE_teste")] if crit.startswith("maior") else \
            [("MSE_teste", True, "MSE_teste"), ("MSE_todos", True, "MSE_todos")]
        for col, asc, col_mse in escolhas:
            v = g.sort_values(col, ascending=asc).iloc[0]
            rot = "aqui" if crit.startswith("maior") else f"aqui ({'MSE no teste' if col == 'MSE_teste' else 'MSE em todo março'})"
            md.append(f"| | | | {f(v['R_treino'])} | {f(v.get('R_validacao'))} | {f(v['R_teste'])} | "
                      f"{f(v['R_todos'])} | {f(v[col_mse])} | {rot} |")
    md.append("")
    (out / args.saida).write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
