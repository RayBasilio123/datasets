"""B5: analises de laboratorio (mod3.csv) e tags do PIMS (Dados_Conceicao_*.xlsx) do Erick Guedes.

Uso:
    python scripts/b5_laboratorio_e_tags.py <pasta_com_os_originais>

A pasta deve ter Dados_Flotacao_ConceicaoII_mod3.csv e os 13 Dados_Conceicao_*.xlsx.
Grava:
- raw/B5_laboratorio.csv: 9 analises (variavel, tag_pims, data_hora, valor), formato longo;
- raw/B5_I_Conceicao_variaveis.csv: o dicionario ganha equipamento, nome descritivo e tag do PIMS.
"""
import sys
from pathlib import Path

import openpyxl
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
ORIG = Path(sys.argv[1])

# tag do PIMS -> nome. ALFTCN1 = alimentacao da flotacao, RJFTCN1 = rejeito, PF1CN = produto (concentrado final);
# SC1CN = carga circulante (as 3 analises "de alimentacao, carga circulante e rejeito" da dissertacao, sec. 3.1).
LAB = {
    "P_ALFTCN1_FG_GLOBAL_+0.15MM": "alimentacao_granulometria_+0.15mm",
    "P_ALFTCN1_QQ_GLOBAL_FE": "alimentacao_fe",
    "P_ALFTCN1_QQ_GLOBAL_SIO2": "alimentacao_sio2",
    "P_SC1CN_QQ_GLOBAL_FE": "carga_circulante_fe",
    "P_SC1CN_QQ_GLOBAL_SiO2": "carga_circulante_sio2",
    "P_RJFTCN1_QQ_GLOBAL_FE": "rejeito_fe",
    "P_RJFTCN1_QQ_GLOBAL_SIO2": "rejeito_sio2",
    "P_PF1CN_QQ_GLOBAL_FE": "concentrado_fe",
    "P_PF1CN_QQ_GLOBAL_SIO2": "concentrado_sio2",
}
CELULAS = ["R1", "R2", "C1", "C2", "RC", "S1B1", "S1B2", "S1B3", "S2B1", "S2B2", "S2B3"]
ARQ_CEL = {"Caixa_Alimentacao": "CA", "Caixa_Recirculacao": "CR", "Rougher1": "R1", "Rougher2": "R2",
           "Cleaner1": "C1", "Cleaner2": "C2", "Recleaner": "RC", "Scavenger1_B1": "S1B1", "Scavenger1_B2": "S1B2",
           "Scavenger1_B3": "S1B3", "Scavenger2_B1": "S2B1", "Scavenger2_B2": "S2B2", "Scavenger2_B3": "S2B3"}


def laboratorio():
    arq = ORIG / "Dados_Flotacao_ConceicaoII_mod3.csv"
    cab = pd.read_csv(arq, sep=";", nrows=0).columns
    n = 2 * len(LAB)
    assert [c for c in cab[1:n:2]] == list(LAB), cab[:n]
    df = pd.read_csv(arq, sep=";", decimal=",", usecols=range(n), dtype=str, encoding="latin1")
    partes = []
    for k, (tag, nome) in enumerate(LAB.items()):
        d = pd.DataFrame({"data_hora": df.iloc[:, 2 * k], "valor": df.iloc[:, 2 * k + 1]}).dropna(how="all")
        d["data_hora"] = pd.to_datetime(d["data_hora"], format="%d/%m/%Y %H:%M")
        d["valor"] = pd.to_numeric(d["valor"].str.replace(",", "."), errors="coerce")
        partes.append(d.assign(variavel=nome, tag_pims=tag)[["variavel", "tag_pims", "data_hora", "valor"]])
    lab = pd.concat(partes, ignore_index=True)
    lab.to_csv(REPO / "raw/B5_laboratorio.csv", index=False)
    print(lab.groupby("variavel", sort=False).agg(n=("valor", "size"), inicio=("data_hora", "min"),
                                                  fim=("data_hora", "max"), media=("valor", "mean")))
    return lab


def tags():
    linhas = []
    for chave, cel in ARQ_CEL.items():
        ws = openpyxl.load_workbook(ORIG / f"Dados_Conceicao_{chave}.xlsx", read_only=True, data_only=True).worksheets[0]
        it = ws.iter_rows(values_only=True, max_row=3)
        titulo, nomes, tg = next(it)[0], next(it), next(it)
        for k in range(len(nomes) // 2):
            linhas.append({"equipamento": titulo.strip(), "nome_arquivo_original": nomes[2 * k + 1], "tag_pims": tg[2 * k + 1]})
    t = pd.DataFrame(linhas)
    dic = pd.read_csv(REPO / "raw/B5_I_Conceicao_variaveis.csv")
    assert len(dic) == len(t) == 65
    descr = (["CA_nivel", "CA_densidade", "CA_vazao_vol", "CA_vazao_mas", "CA_vazao_amina", "CA_vazao_amido",
              "CR_nivel", "CR_densidade", "CR_vazao_vol", "CR_vazao_mas"]
             + [f"{c}_{v}" for c in CELULAS for v in ["espuma", "ar", "dardo1", "dardo2", "valv_ar"]])
    dic = dic.drop(columns=[c for c in ["nome_descritivo", "equipamento", "tag_pims"] if c in dic.columns])
    dic.insert(1, "nome_descritivo", descr)
    dic.insert(2, "equipamento", t["equipamento"])
    dic.insert(3, "tag_pims", t["tag_pims"])
    dic.to_csv(REPO / "raw/B5_I_Conceicao_variaveis.csv", index=False)
    print(dic[["coluna", "nome_descritivo", "equipamento", "tag_pims"]].to_string())


if __name__ == "__main__":
    lab = laboratorio()
    tags()
