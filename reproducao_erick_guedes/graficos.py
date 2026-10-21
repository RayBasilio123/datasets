"""Refaz as figuras de Guedes (2020) com os resultados desta reproducao.

Uso: python graficos.py --variante listas_erick      (conjuntos rrelieff15 / pca10)
     python graficos.py --variante ponta_a_ponta     (conjuntos auto_rrelieff / auto_pca)

Saida em plots/<variante>/ (200 dpi). As figuras de dados (3.2) vao em plots/dados/.
"""
import argparse, json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from sklearn.ensemble import RandomForestRegressor

from modelos import MLP, dividir, entradas
from prep import DATA, ETAPA2_26, ETAPA3_21, MESES, NOMES, rrelieff

ROOT = Path(__file__).resolve().parent
TAG = "atraso0h"           # trocado por --dados (ex.: orig_atraso0h)
PROTOCOLO = "antigo"       # trocado por --protocolo; "matlab" = saida tansig e divisao 75/15/15
DPI = 200
# paleta de referencia (skill dataviz): 3 primeiras cores categoricas validadas em todos os pares
AZUL, LARANJA, VERDE_AGUA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA2, CINZA, GRADE = "#0b0b0b", "#52514e", "#b5b4ae", "#e6e5e1"
DIVERGENTE = LinearSegmentedColormap.from_list("div", ["#2a78d6", "#f0efec", "#e34948"])
ROTULO = {"rna": "RNA LM", "rna_scg": "RNA SCG", "rf": "RF"}
NOME_MES = {"jan": "Janeiro", "fev": "Fevereiro", "mar": "Março", "abr": "Abril", "mai": "Maio"}
ERICK_MAE = {("rrelieff15", "rna"): {"mar": 0.6132, "jan": 1.8890, "fev": 2.3933, "abr": 2.1705, "mai": 2.1016},
             ("pca10", "rf"): {"mar": 0.5904, "jan": 0.9645, "fev": 1.0625, "abr": 1.3007, "mai": 1.1816}}

plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": CINZA, "axes.labelcolor": TINTA2, "xtick.color": TINTA2,
    "ytick.color": TINTA2, "axes.titlecolor": TINTA, "axes.grid": True, "grid.color": GRADE,
    "grid.linewidth": 0.6, "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
})


def salvar(fig, pasta, nome):
    pasta.mkdir(parents=True, exist_ok=True)
    fig.savefig(pasta / nome, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("  ", pasta.relative_to(ROOT) / nome)


def rotulo_var(v):
    return v.replace("_", " ")


# ---------------------------------------------------------------- figura 3.2
def fig_media_mediana(pasta):
    """Densidade na caixa de alimentacao: boxplot por janela de 2h + media e mediana (24 janelas de marco)."""
    longo = pd.read_parquet(DATA / "raw/B5_processo_originais_longo.parquet", filters=[("variavel", "==", "CA_densidade")])
    longo = longo[longo["valor"].notna() & (longo["valor"] != 0)].sort_values("data_hora")
    df = pd.read_parquet(ROOT / f"dados/agrupados_{TAG}.parquet")
    t = df.loc[df["mes"] == "mar", "data_hora"].head(24).to_numpy()
    grupos = [longo.loc[(longo["data_hora"] > ti - np.timedelta64(2, "h")) & (longo["data_hora"] <= ti), "valor"].to_numpy()
              for ti in t]
    fig, ax = plt.subplots(figsize=(10, 4))
    pos = np.arange(1, len(grupos) + 1)
    ax.boxplot(grupos, positions=pos, widths=0.6, showfliers=True, patch_artist=True,
               boxprops=dict(facecolor="#cde2fb", edgecolor=TINTA2, linewidth=0.8),
               medianprops=dict(color=TINTA2, linewidth=0.8), whiskerprops=dict(color=TINTA2, linewidth=0.8),
               capprops=dict(color=TINTA2, linewidth=0.8), flierprops=dict(marker="o", markersize=2, markerfacecolor=CINZA,
                                                                          markeredgecolor=CINZA))
    ax.plot(pos, [np.median(g) for g in grupos], color=AZUL, lw=2, marker="o", ms=4, label="Mediana da janela")
    ax.plot(pos, [np.mean(g) for g in grupos], color=LARANJA, lw=2, marker="o", ms=4, label="Média da janela")
    ax.set_xticks(pos, [pd.Timestamp(x).strftime("%d/%m %H:%M") for x in t], rotation=60, ha="right")
    ax.set_ylabel("Densidade na caixa de alimentação (t/m³)")
    ax.set_title("Fig. 3.2 — Densidade por janela de 2 h antes de cada análise (24 primeiras janelas de março)")
    ax.legend(loc="lower right")
    salvar(fig, pasta, "fig3_2_densidade_media_mediana.png")


# ---------------------------------------------------------------- figura 3.4
def fig_heatmap(pasta, variaveis, df, titulo):
    mar = df["mes"] == "mar"
    cols = variaveis + ["fe"]
    C = df.loc[mar, cols].corr().to_numpy()
    n = len(cols)
    fig, ax = plt.subplots(figsize=(0.42 * n + 2, 0.42 * n + 1))
    im = ax.imshow(C, cmap=DIVERGENTE, vmin=-1, vmax=1)
    nomes = [rotulo_var(c) if c != "fe" else "Fe (lab.)" for c in cols]
    ax.set_xticks(range(n), nomes, rotation=90)
    ax.set_yticks(range(n), nomes)
    ax.grid(False)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{C[i, j]:.2f}".replace("0.", ".").replace("-.", "−."), ha="center", va="center",
                    fontsize=5.5, color=TINTA if abs(C[i, j]) < 0.6 else "#fcfcfb")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label="Correlação de Pearson (março)")
    ax.set_title(titulo)
    salvar(fig, pasta, "fig3_4_correlacoes.png")


# ---------------------------------------------------------------- figuras 4.1 e 4.2
def fig_rrelieff(pasta, variaveis, df):
    mar = (df["mes"] == "mar").to_numpy()
    W = rrelieff(df.loc[mar, variaveis].to_numpy(), df.loc[mar, "fe"].to_numpy())
    ordem = np.argsort(-W)
    fig, ax = plt.subplots(figsize=(9, 4))
    cores = [AZUL if W[i] > 0 else CINZA for i in ordem]
    ax.bar(range(len(W)), W[ordem], color=cores, width=0.7)
    ax.axhline(0, color=TINTA2, lw=0.8)
    ax.set_xticks(range(len(W)), [rotulo_var(variaveis[i]) for i in ordem], rotation=60, ha="right")
    ax.set_ylabel("Peso de importância (RReliefF, k = 53)")
    n_pos = int((W > 0).sum())
    ax.set_title(f"Fig. 4.1 — Pesos do RReliefF: {n_pos} de {len(W)} variáveis com peso positivo (azul; Erick: 15 de 21)")
    salvar(fig, pasta, "fig4_1_pesos_rrelieff.png")


def fig_pca(pasta, variaveis, df):
    mar = (df["mes"] == "mar").to_numpy()
    X = df.loc[mar, variaveis].to_numpy(float)
    X = (X - X.min(0)) / np.where(X.max(0) > X.min(0), X.max(0) - X.min(0), 1)
    ev = np.linalg.svd(X - X.mean(0), compute_uv=False) ** 2
    pct = 100 * ev / ev.sum()
    acum = np.cumsum(pct)
    k = int(np.searchsorted(acum, 90, side="right") + 1)
    x = np.arange(1, len(pct) + 1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(x, pct, color=[AZUL if i <= k else CINZA for i in x], width=0.7, label="Variância de cada componente")
    ax.plot(x, acum, color=LARANJA, lw=2, marker="o", ms=4, label="Variância acumulada")
    ax.axhline(90, color=TINTA2, lw=0.8, ls="--")
    ax.text(len(x), 91.5, "90%", ha="right", color=TINTA2)
    ax.set_ylim(0, 102)
    ax.set_xlabel("Componente principal")
    ax.set_ylabel("Variância explicada (%)")
    ax.set_title(f"Fig. 4.2 — PCA sobre {len(variaveis)} variáveis: {k} componentes somam {acum[k - 1]:.1f}%")
    ax.legend(loc="center right")
    salvar(fig, pasta, "fig4_2_variancia_pca.png")


# ---------------------------------------------------------------- figuras 4.4-4.11 (modelos escolhidos)
def retreinar(df, conjunto, modelo, divisao, ciclo):
    """Refaz exatamente o treino (mesmas sementes de modelos.py) e devolve previsoes e indices."""
    X_all, _ = entradas(df, conjunto, TAG)
    y_all, meses = df["fe"].to_numpy(float), df["mes"].to_numpy()
    mar_idx = np.flatnonzero(meses == "mar")
    Xm, ym = X_all[mar_idx], y_all[mar_idx]
    matlab = PROTOCOLO == "matlab"           # tem que ser igual ao de modelos.py, senao o modelo refeito e outro
    tr, va, te = dividir(len(ym), seed=1000 + divisao, razoes=(75, 15, 15) if matlab else (70, 15, 15))
    seed = divisao * 100 + ciclo
    if modelo == "rf":
        m = RandomForestRegressor(n_estimators=500, min_samples_leaf=3, max_features=1 / 3, random_state=seed,
                                  n_jobs=4).fit(Xm[np.r_[tr, va]], ym[np.r_[tr, va]])
        sub = {"Treinamento": np.r_[tr, va], "Teste": te}
    else:
        m = MLP("lm" if modelo == "rna" else "scg", seed=seed, saida="tansig" if matlab else "linear").fit(
            Xm[tr], ym[tr], Xm[va], ym[va])
        sub = {"Treinamento": tr, "Validação": va, "Teste": te}
    sub["Todos"] = np.arange(len(ym))
    return m.predict(X_all), y_all, meses, mar_idx, sub


def fig_regressao(pasta, nome, titulo, pred, y, mar_idx, sub):
    pm, ym = pred[mar_idx], y[mar_idx]
    fig, axs = plt.subplots(1, len(sub), figsize=(3.3 * len(sub), 3.4), sharex=True, sharey=True)
    lo, hi = min(ym.min(), pm.min()) - 0.5, max(ym.max(), pm.max()) + 0.5
    for ax, (rot, ix) in zip(axs, sub.items()):
        r = np.corrcoef(ym[ix], pm[ix])[0, 1]
        a, b = np.polyfit(ym[ix], pm[ix], 1)
        ax.plot([lo, hi], [lo, hi], color=TINTA2, lw=0.8, ls=":", label="Previsão = alvo")
        ax.scatter(ym[ix], pm[ix], s=10, facecolors="none", edgecolors=AZUL, linewidths=0.8, label="Amostras")
        ax.plot([lo, hi], [a * lo + b, a * hi + b], color=LARANJA, lw=2, label="Reta ajustada")
        ax.set_title(f"{rot}: R = {r:.3f}".replace(".", ","))
        ax.text(0.03, 0.97, f"previsão ≈ {a:.2f}·alvo + {b:.0f}".replace(".", ","), transform=ax.transAxes,
                va="top", color=TINTA2, fontsize=8)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_xlabel("Fe no laboratório (%)")
    axs[0].set_ylabel("Fe previsto (%)")
    axs[-1].legend(loc="lower right", fontsize=7)
    fig.suptitle(titulo, color=TINTA, y=1.03)
    salvar(fig, pasta, nome)


def com_quebras(t, *series):
    """Insere NaN onde falta analise (intervalo > 2 h) para a linha nao ligar buracos."""
    t = np.asarray(t)
    quebra = np.flatnonzero(np.diff(t) > np.timedelta64(150, "m")) + 1
    t2 = np.insert(t.astype("datetime64[m]"), quebra, t[quebra - 1].astype("datetime64[m]") + np.timedelta64(1, "m"))
    return [t2] + [np.insert(np.asarray(v, float), quebra, np.nan) for v in series]


def fig_mensal(pasta, nome, titulo, pred, y, meses, df):
    tempo = df["data_hora"].to_numpy()
    media_mar = y[meses == "mar"].mean()
    ordem = ["mar", "jan", "fev", "abr", "mai"]
    fig, axs = plt.subplots(len(ordem), 1, figsize=(10, 2.2 * len(ordem)), sharey=True)
    for ax, mes in zip(axs, ordem):
        k = meses == mes
        mae = np.mean(np.abs(y[k] - pred[k]))
        mae_base = np.mean(np.abs(y[k] - media_mar))
        tq, yq, pq = com_quebras(tempo[k], y[k], pred[k])
        ax.plot(tq, yq, color=AZUL, lw=1.4, label="Laboratório")
        ax.plot(tq, pq, color=LARANJA, lw=1.4, label="Soft sensor")
        ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(bymonthday=[1, 5, 9, 13, 17, 21, 25, 29]))
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d/%m"))
        ax.axhline(media_mar, color=VERDE_AGUA, lw=1.4, ls="--", label="Média de março")
        ax.set_title(f"{NOME_MES[mes]}{' (mês de treino)' if mes == 'mar' else ''} — MAE soft sensor {mae:.2f}, "
                     f"MAE média de março {mae_base:.2f}".replace(".", ","), loc="left", fontsize=9)
        ax.set_ylabel("Fe (%)")
    axs[0].legend(loc="lower left", ncol=3, fontsize=8)
    fig.suptitle(titulo, color=TINTA, y=1.0)
    fig.tight_layout()
    salvar(fig, pasta, nome)


# ---------------------------------------------------------------- distribuicao dos 1000 treinos
def fig_distribuicao(pasta, conjunto, res, base, rotulo_conj):
    ordem = ["mar", "jan", "fev", "abr", "mai"]
    modelos = ["rna", "rna_scg", "rf"]
    cores = {"rna": AZUL, "rna_scg": LARANJA, "rf": VERDE_AGUA}
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.2), sharey=True)
    larg = 0.25
    for ax, tipo in zip(axs, ["boxplot", "violino"]):
        for j, mod in enumerate(modelos):
            dados = [res.loc[res.modelo == mod, f"MAE_{m}"].to_numpy() for m in ordem]
            pos = np.arange(len(ordem)) + (j - 1) * larg
            if tipo == "boxplot":
                ax.boxplot(dados, positions=pos, widths=larg * 0.8, showfliers=False, patch_artist=True,
                           boxprops=dict(facecolor=cores[mod], edgecolor=cores[mod], alpha=0.85),
                           medianprops=dict(color="#fcfcfb", lw=1.2), whiskerprops=dict(color=cores[mod]),
                           capprops=dict(color=cores[mod]))
            else:
                v = ax.violinplot(dados, positions=pos, widths=larg * 0.9, showmedians=True, showextrema=False)
                for b in v["bodies"]:
                    b.set_facecolor(cores[mod]); b.set_alpha(0.75); b.set_edgecolor("none")
                v["cmedians"].set_color(TINTA)
            ax.plot([], [], color=cores[mod], lw=6, label=ROTULO[mod])
        for i, m in enumerate(ordem):
            ax.hlines(base[f"MAE_{m}"], i - 0.42, i + 0.42, color=TINTA2, lw=1.2, ls="--",
                      label="Média de março" if i == 0 else None)
            for (c, mod), vals in ERICK_MAE.items():
                if c == conjunto:
                    j = modelos.index(mod)
                    ax.plot(i + (j - 1) * larg, vals[m], marker="D", ms=5, color=TINTA,
                            label="Modelo adotado pelo Erick" if i == 0 else None)
        ax.set_xticks(range(len(ordem)), [NOME_MES[m] + ("\n(treino)" if m == "mar" else "") for m in ordem])
        ax.set_title(tipo.capitalize())
        ax.set_ylim(0, None)
    axs[0].set_ylabel("MAE do Fe no mês (%)")
    y_max = np.nanpercentile(res[[f"MAE_{m}" for m in ordem]].to_numpy(), 97)
    axs[0].set_ylim(0, max(3.0, y_max))
    h, l = axs[1].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=len(l), fontsize=8, bbox_to_anchor=(0.5, -0.06))
    corte = f"{axs[0].get_ylim()[1]:.1f}".replace(".", ",")
    fig.suptitle(f"MAE mensal dos 1000 treinos ({rotulo_conj}); valores acima de {corte} cortados", color=TINTA)
    salvar(fig, pasta, f"distribuicao_mae_mensal_{conjunto}.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variante", choices=["listas_erick", "ponta_a_ponta"], default="listas_erick")
    ap.add_argument("--dados", default="orig_atraso0h", help="sufixo dos parquets em dados/")
    ap.add_argument("--dir", default="orig_atraso0h_matlab", help="pasta em resultados/")
    ap.add_argument("--plots", default="figuras", help="pasta de saida das figuras")
    ap.add_argument("--protocolo", choices=["antigo", "matlab"], default="matlab")
    args = ap.parse_args()
    global TAG, PROTOCOLO
    TAG, PROTOCOLO = args.dados, args.protocolo
    pasta = ROOT / args.plots / args.variante
    df = pd.read_parquet(ROOT / f"dados/preenchidos_{TAG}.parquet")
    res_dir = ROOT / "resultados" / (args.dir or TAG)
    if args.variante == "listas_erick":
        conj_rrf, conj_pca = "rrelieff15", "pca10"
        v_heat, v_sel = ETAPA2_26, ETAPA3_21
        base = json.load(open(res_dir / "resumo.json"))["referencia_media_de_marco"]
        fig_media_mediana(ROOT / args.plots / "dados")
    else:
        # ponta a ponta com disponibilidade em marco e jan-mai (o criterio que reproduz o Erick)
        conj_rrf, conj_pca = "auto_disp_rrelieff", "auto_disp_pca"
        sel = json.load(open(ROOT / f"dados/selecao_{TAG}_disp.json"))
        v_heat, v_sel = sel["etapa2_qualitativa"], sel["etapa3_correlacao"]
        base = json.load(open(res_dir / "resumo_ponta_a_ponta_disp.json"))["referencia_media_de_marco"]
    rot = {"listas_erick": "variáveis da dissertação", "ponta_a_ponta": "variáveis selecionadas do zero"}[args.variante]
    fig_heatmap(pasta, v_heat, df, f"Fig. 3.4 — Correlações em março após a 2ª etapa ({len(v_heat)} variáveis, {rot})")
    fig_rrelieff(pasta, v_sel, df)
    fig_pca(pasta, v_sel, df)

    res = {c: pd.read_csv(res_dir / f"treinos_{c}.csv") for c in (conj_rrf, conj_pca)}
    escolhas = [  # (figura, conjunto, modelo, criterio)
        ("fig4_4", conj_rrf, "rna", "R_teste", False, "RNA LM com RReliefF — maior R no teste"),
        ("fig4_5", conj_rrf, "rna", "MSE_todos", True, "RNA LM com RReliefF — menor MSE em todo março"),
        ("fig4_6", conj_pca, "rf", "R_teste", False, "RF com PCA — maior R no teste"),
        ("fig4_7", conj_rrf, "rf", "MSE_todos", True, "RF com RReliefF — menor MSE em todo março"),
    ]
    for fig_id, conj, mod, col, asc, titulo in escolhas:
        g = res[conj][res[conj].modelo == mod].sort_values(col, ascending=asc).iloc[0]
        pred, y, meses, mar_idx, sub = retreinar(df, conj, mod, int(g.divisao), int(g.ciclo))
        fig_regressao(pasta, f"{fig_id}_regressao_{mod}_{conj}.png",
                      f"{titulo.replace('—', '(Fig. ' + fig_id[3:].replace('_', '.') + ') —')} [treino {int(g.divisao)}.{int(g.ciclo)}]",
                      pred, y, mar_idx, sub)
        if fig_id in ("fig4_5", "fig4_6"):        # modelos adotados pelo Erick (Figs. 4.8-4.11)
            nome = "fig4_8_4_9_teor_fe_mensal_rna.png" if mod == "rna" else "fig4_10_4_11_teor_fe_mensal_rf.png"
            fig_mensal(pasta, nome, f"Teor de Fe: laboratório vs. soft sensor — {titulo}", pred, y, meses, df)
    for conj, rotc in ((conj_rrf, "entradas RReliefF"), (conj_pca, "entradas PCA")):
        fig_distribuicao(pasta, conj, res[conj], base, f"{rotc}, {rot}")


if __name__ == "__main__":
    main()
