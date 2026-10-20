"""Gera os arquivos de variáveis de processo da B5 a partir de I_Conceicao.xlsx.

Uso:
    python scripts/b5_juntar_variaveis.py <I_Conceicao.xlsx> [pasta_saida]

Lê o xlsx em streaming (biblioteca padrão; o arquivo tem 227 MB e ~1,1 GB de XML)
e grava, na pasta de saída (padrão: a raiz deste repositório):

- raw/B5_I_Conceicao_longo.parquet: uma linha por medição, sem perda;
- raw/B5_I_Conceicao_variaveis.csv: dicionário das 65 variáveis;
- processed/covariaveis/B5_2h.parquet: alvo + variáveis na grade de
  processed/silica/B5.parquet.

Regra da janela de 2h: o alvo é uma análise de laboratório às HH:29 (horas
pares), rotulada HH:00 no parquet processado. A linha L recebe a média das
amostras em (L - 1h31m, L + 29m], as 2h que terminam na amostra, para que nada
do processo posterior à análise entre na linha dela.
"""
import re, sys, time, unicodedata, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[1]
XLSX = sys.argv[1]
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else REPO
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REF = re.compile(r"([A-Z]+)")
FONTE = b"I_Conceicao.xlsx (Erick Guedes, mestrado ITV), aba Dados_Flotacao_ConceicaoII_mod4"


def col_index(ref):
    n = 0
    for ch in REF.match(ref).group(1):
        n = n * 26 + ord(ch) - 64
    return n - 1


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def series(path):
    r = pd.read_parquet(path).iloc[0]
    return pd.Series(np.asarray(r["target"], float),
                     index=pd.date_range(r["start"], periods=len(r["target"]), freq="2h"))


t0 = time.time()
z = zipfile.ZipFile(XLSX)
ss = [
    "".join(t.text or "" for t in el.iter(NS + "t"))
    for _, el in ET.iterparse(z.open("xl/sharedStrings.xml"))
    if el.tag == NS + "si"
]

# A planilha tem pares de colunas (DataHora, valor), um por variável.
header = None
var_k, var_ts, var_val, var_txt = [], [], [], []
sem_data = []
with z.open("xl/worksheets/sheet1.xml") as fh:
    for _, el in ET.iterparse(fh):
        if el.tag != NS + "row":
            continue
        cells = {}
        for c in el.iter(NS + "c"):
            v = c.find(NS + "v")
            if v is None or v.text is None:
                continue
            val = v.text
            if c.get("t") == "s":
                val = ss[int(val)]
            cells[col_index(c.get("r"))] = val
        el.clear()
        if header is None:
            header = [cells.get(j, "") for j in range(max(cells) + 1)]
            nvar = len(header) // 2
            assert all(header[2 * k] == "DataHora" for k in range(nvar)), header
            continue
        for k in range(nvar):
            d, v = cells.get(2 * k), cells.get(2 * k + 1)
            if d is None and v is None:
                continue
            try:
                t = float(d)
            except (TypeError, ValueError):
                sem_data.append((k + 1, d, v))
                continue
            try:
                x, txt = float(v), None
            except (TypeError, ValueError):
                x, txt = np.nan, (v if v is not None else "")
            var_k.append(k)
            var_ts.append(t)
            var_val.append(x)
            var_txt.append(txt)
print(f"lido em {time.time() - t0:.0f}s: {len(var_k)} medições; células sem data descartadas: {sem_data}", flush=True)

names = [header[2 * k + 1] for k in range(nvar)]
cols = [f"v{k + 1:02d}_{slug(n)}" for k, n in enumerate(names)]

# Serial do Excel -> data e hora, arredondada ao segundo.
k = np.asarray(var_k, dtype=np.int16)
secs = np.rint(np.asarray(var_ts) * 86400).astype("int64")
order = np.argsort(k, kind="stable")  # agrupa por variável mantendo a ordem original de cada uma
k, secs = k[order], secs[order]
ts = np.datetime64("1899-12-30T00:00:00", "s") + secs.astype("timedelta64[s]")
val = np.asarray(var_val, dtype="float64")[order]
txt = pd.array(np.asarray(var_txt, dtype=object)[order], dtype="string")

table = pa.table({
    "variavel": pa.DictionaryArray.from_arrays(pa.array(k.astype("int32")), pa.array(cols)),
    "data_hora": pa.array(ts, type=pa.timestamp("s")),
    "valor": pa.array(val, from_pandas=True),  # NaN (texto `Bad`) vira nulo
    "valor_texto": pa.array(txt),
}).replace_schema_metadata({
    b"fonte": FONTE,
    b"conversao": b"serial Excel -> data_hora arredondada ao segundo; valores nao numericos -> valor NaN com o texto em valor_texto",
    b"ordem": b"linhas na ordem original de cada variavel (importa na hora repetida do fim do horario de verao, 2019-02-16 23:00-23:59)",
})
(OUT / "raw").mkdir(parents=True, exist_ok=True)
pq.write_table(table, OUT / "raw/B5_I_Conceicao_longo.parquet", compression="zstd", compression_level=9,
               use_dictionary=["variavel", "valor_texto"],
               column_encoding={"data_hora": "DELTA_BINARY_PACKED", "valor": "PLAIN"})

dic = []
bounds = np.searchsorted(k, np.arange(nvar + 1))
for i, (c, n) in enumerate(zip(cols, names)):
    a, b = bounds[i], bounds[i + 1]
    s, x = secs[a:b], val[a:b]
    d = np.diff(s)
    dic.append({
        "coluna": c,
        "nome_original": n,
        "coluna_xlsx": i * 2 + 2,
        "amostras": int(b - a),
        "nao_numericos": int(pd.Series(txt[a:b]).notna().sum()),
        "inicio": ts[a:b].min(),
        "fim": ts[a:b].max(),
        "intervalo_mediano_s": float(np.median(d[d > 0])),
        "min": np.nanmin(x),
        "max": np.nanmax(x),
    })
pd.DataFrame(dic).to_csv(OUT / "raw/B5_I_Conceicao_variaveis.csv", index=False)

# Tabela larga de 2h na grade exata de processed/silica/B5.parquet.
si = series(REPO / "processed/silica/B5.parquet")
fe = series(REPO / "processed/ferro/B5.parquet")
assert si.index.equals(fe.index)

long = pd.DataFrame({"variavel": pd.Categorical.from_codes(k, categories=cols),
                     "data_hora": pd.to_datetime(secs, unit="s", origin="1899-12-30"),
                     "valor": val})
rotulo = (long["data_hora"] - pd.Timedelta(minutes=29)).dt.ceil("2h")
wide = (long.assign(rotulo=rotulo)
            .groupby(["rotulo", "variavel"], observed=True)["valor"].mean()
            .unstack("variavel")
            .reindex(index=si.index, columns=cols))
wide.index.name = "data_hora"
wide.insert(0, "ferro", fe.values)
wide.insert(0, "silica", si.values)
wide = wide.reset_index()
wide.columns.name = None

wt = pa.Table.from_pandas(wide, preserve_index=False)
wt = wt.replace_schema_metadata({
    **(wt.schema.metadata or {}),
    b"freq": b"2h",
    b"janela": b"cada linha L = media das amostras em (L-1h31m, L+29m], as 2h que terminam na amostra de laboratorio das HH:29",
    b"alvo": b"silica e ferro copiados de processed/silica/B5.parquet e processed/ferro/B5.parquet (interpolados)",
    b"fonte": FONTE,
})
(OUT / "processed/covariaveis").mkdir(parents=True, exist_ok=True)
pq.write_table(wt, OUT / "processed/covariaveis/B5_2h.parquet", compression="zstd", compression_level=9)
print(f"pronto em {time.time() - t0:.0f}s: longo {table.num_rows} linhas, 2h {wide.shape}")
