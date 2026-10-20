# Bases de flotação reversa de minério de ferro (B1–B5)

Bases usadas no artigo Basilio2026 (previsão do teor de sílica no concentrado com
Time Series Foundation Models e predição conformal). Este repositório guarda os
arquivos brutos com **todas as variáveis de processo** e as séries processadas
exatamente como entram nos experimentos.

> **Repositório privado.** B1, B3, B4 e B5 são dados privados extraídos do PIMS de
> usinas industriais. Não torne este repositório público nem redistribua os
> arquivos. Apenas a B2 é pública (Kaggle, *Quality Prediction in a Mining Process*).

## Estrutura

```
raw/                  arquivos brutos, com todas as variáveis
processed/silica/     série-alvo SiO2 do concentrado, formato GluonTS (usada no artigo)
processed/ferro/      série Fe do concentrado, mesmo formato e mesma grade temporal
processed/covariaveis/ alvo + variáveis de processo já juntados na grade do alvo (B5)
scripts/              código que gerou os arquivos da B5 a partir do xlsx original
datasets.json         metadados de cada base (colunas-alvo, frequência, cuidados)
SHA256SUMS            checksums de todos os arquivos de dados
```

Os parquets precisam de `pyarrow` (o `venv_test` do Basilio2026 já tem).

## Resumo

| Base | Tecnologia | Período (bruto) | Freq. alvo | Linhas brutas | Variáveis além de SiO2/Fe | Pontos processados |
|---|---|---|---|---|---|---|
| B1 | Células mecânicas | 2023-05-23 – 2025-06-22 | 2h | 7.244 | 49 | 9.124 |
| B2 | Colunas (pública, Kaggle) | 2017-03-10 – 2017-09-09 | 1h | 4.097 | 21 | 4.415 |
| B3 | Colunas | 2022-01-01 – 2023-07-25 | 2h (bruto 1h) | 13.704 | 58 | 6.852 |
| B4 | Células mecânicas (subconjunto da B1) | 2024-11-23 – 2025-06-21 | 2h | 1.909 | 38 | 2.523 |
| B5 | Células mecânicas | 2019-01-01 – 2019-05-31 | 2h | 1.668 | 65 (arquivo separado, ver seção B5) | 1.812 |

As séries processadas saíram de `Basilio2026/csv_to_gluonts.py`, que:

1. remove toda linha em que **qualquer** coluna numérica tem |z-score| > 3;
2. interpola linearmente o que ficou faltando;
3. reamostra pela média numa grade regular (`resample(freq).mean()`), com o rótulo
   no início da janela: a amostra das 00:29 vira o ponto das 00:00 numa base de 2h;
4. interpola linearmente as janelas vazias. Por isso não há `NaN`, e há mais
   pontos processados do que linhas brutas. Na B5, por exemplo, 144 das 1.812
   janelas de 2h não tinham amostra e foram interpoladas.

Colunas-alvo em cada arquivo bruto:

| Base | SiO2 do concentrado | Fe do concentrado |
|---|---|---|
| B1, B4 | `P_CONFLTTO_QQ_GLOBAL_SIO2` | `P_CONFLTTO_QQ_GLOBAL_FE` |
| B2 | `% Silica Concentrate` | `% Iron Concentrate` |
| B3 | `SiO2 C flot (%)` | `Fe C flot (%)` |
| B5 | `P_PF1CN_QQ_GLOBAL_SIO2` | `P_PF1CN_QQ_GLOBAL_FE` |

## Como carregar

Arquivo bruto (todas as variáveis):

```python
import json, pandas as pd

meta = json.load(open("datasets.json"))["B1"]
df = pd.read_csv(meta["bruto"]["arquivo"], parse_dates=[meta["bruto"]["coluna_data"]])
y = df[meta["alvo"]["silica"]]
```

Série processada (a mesma que entra nos experimentos):

```python
row = pd.read_parquet("processed/silica/B1.parquet").iloc[0]
y = pd.Series(
    row["target"],
    index=pd.date_range(pd.Timestamp(str(row["start"])), periods=len(row["target"]), freq=meta["frequencia"]),
)
```

O parquet processado está no formato GluonTS: uma única linha com as colunas
`start`, `target` (a série inteira numa lista) e `item_id`. A frequência também
fica gravada nos metadados do arquivo (`freq`).

## Cuidados antes de usar as variáveis como covariáveis

- **B1**: 9 colunas são estados discretos de motores e bomba (valores de 1 a 6:
  `TO_MF64xx_M1_EST1`, `TO_BO6311_EST1`). 6 colunas são análises de laboratório
  da alimentação e do rejeito (`P_A6302FN_*`, `P_A4412TO_*`, `P_ACM4181_*`), com
  a mesma defasagem de laboratório do alvo.
- **B2**: `% Iron Feed` e `% Silica Feed` ficam constantes por longos períodos.
- **B3**: há valores absurdos que precisam de limpeza (amido até 5e36, velocidade
  superficial até 4e16, tempos de residência até 3e6 min). O bruto é horário; a
  série processada é agregada em 2h.
- **B4**: é a B1 num período contínuo, com as tags renomeadas. `conc_silica_MM` e
  `conc_fe_MM` são médias móveis do próprio alvo e **vazam o alvo**. As demais
  colunas `*_MM` também são médias móveis: confirme se a janela é só para trás
  antes de usá-las. `grupo_mudanca` é um contador, não uma variável. 9 colunas são
  estados de motor em texto (`Funcionando Remoto` etc.).

## B5: variáveis de processo

O alvo da B5 (`raw/B5_T_Conceicao.csv`) é uma análise de laboratório a cada 2h,
sempre às HH:29 de horas pares. As 65 variáveis de processo vieram de outro
arquivo, em que cada variável tem a própria coluna de data e hora e a própria
frequência (de 15 s a ~1,5 h). Elas estão aqui em três arquivos:

| Arquivo | O que é |
|---|---|
| `raw/B5_I_Conceicao_longo.parquet` | **Bruto sem perda.** Uma linha por medição (11,5 milhões): `variavel`, `data_hora`, `valor`, `valor_texto`. |
| `raw/B5_I_Conceicao_variaveis.csv` | Dicionário: nome original, coluna no xlsx, nº de amostras, período, intervalo mediano, mín./máx. |
| `processed/covariaveis/B5_2h.parquet` | **Pronto para modelar.** 1.812 linhas na mesma grade de `processed/silica/B5.parquet`: `data_hora`, `silica`, `ferro` e as 65 variáveis (`v01_nivel` … `v65_abertura_valvula_ar`). |

```python
import pandas as pd

b5 = pd.read_parquet("processed/covariaveis/B5_2h.parquet")
y = b5["silica"]
X = b5.filter(regex=r"^v\d\d_")

# bruto de uma variável
longo = pd.read_parquet("raw/B5_I_Conceicao_longo.parquet", filters=[("variavel", "==", "v10_vazao_massica")])
```

**Regra da junção em 2h.** A linha rotulada `L` (ex.: 00:00) recebe a média das
amostras em `(L − 1h31, L + 0h29]`, ou seja, as 2h que **terminam** na análise de
laboratório das HH:29. Assim nenhuma informação do processo posterior à amostra
entra na linha dela. `silica` e `ferro` são cópias exatas dos parquets
processados (com a interpolação descrita acima). As covariáveis **não** são
interpoladas: janela sem amostra fica `NaN`.

Cuidados:

- **Cobertura desigual**: 14 das 65 variáveis ficam com mais de 50% de `NaN` na
  grade de 2h. Todas são aberturas de válvula (de ar ou dardo), registradas com
  pouca frequência. Veja `amostras` no dicionário.
- **Horário de verão**: a hora 2019-02-16 23:00–23:59 aparece duas vezes. No
  arquivo longo, as linhas de cada variável estão na ordem original, então dá
  para distinguir as duas passagens pela posição.
- **Data e hora truncadas no minuto** na maioria das variáveis: várias medições
  dividem o mesmo `data_hora`. Isso é do arquivo original.
- **Valores inválidos**: 67 medições `Bad` (marcação de qualidade do PIMS) viram
  `valor = NaN`, com o texto preservado em `valor_texto`. 4 células sem data
  nem valor (só espaço, na variável 16) foram descartadas.
- **Conversão**: a data e hora do Excel (número serial) foi arredondada ao
  segundo; os valores foram copiados sem arredondamento.

## Proveniência

| Arquivo aqui | Arquivo original |
|---|---|
| `raw/B1_dados_2h_aggregado_final.csv` | `Basilio2026/dados_2h_aggregado_final.csv` |
| `raw/B2_data_hourly.csv` | `Basilio2026/data_hourly.csv` (agregação horária do dataset do Kaggle) |
| `raw/B3_flotacao_conceicao.csv` | `Basilio2026/Flotação_conceicao_f.csv` |
| `raw/B4_dados_consolidados_com_MM.csv` | `IEEE_SAS_2026/dados_consolidados_com_MM.csv` |
| `raw/B5_T_Conceicao.csv` | `Basilio2026/T_Conceicao_erickguedes.csv` |
| `processed/silica/B1.parquet` | `Basilio2026/data/processed_gluonts_usina/aggregated_mechanical_b1.parquet` |
| `processed/silica/B2.parquet` | `.../hourly_silica.parquet` |
| `processed/silica/B3.parquet` | `.../flotacao_silica.parquet` |
| `processed/silica/B4.parquet` | `.../mechanical_b4.parquet` |
| `processed/silica/B5.parquet` | `.../erickguedes_silica.parquet` |
| `processed/ferro/Bn.parquet` | `Basilio2026/data/processed_gluonts_usina_ferro/Bn_ferro.parquet` |
| `raw/B5_I_Conceicao_longo.parquet`, `raw/B5_I_Conceicao_variaveis.csv`, `processed/covariaveis/B5_2h.parquet` | `eguedes/mestrado_itv/dados/I_Conceicao.xlsx` (dissertação de Erick Guedes, ITV), aba `Dados_Flotacao_ConceicaoII_mod4` |

Os parquets antigos `aggregated_silica.parquet` (B1 constante, todo igual a 4.0) e
`jvale2h_silica.parquet` (B4 com sub-séries espúrias) estavam corrompidos e **não**
estão aqui.

## Pendências

- **Equipamento de cada variável da B5**: os nomes originais se repetem
  ("Nivel de espuma" aparece 10 vezes). O mapeamento para célula/banco está nos
  notebooks e na dissertação de Erick Guedes; até lá, use o número `vNN`.
- **Tabela 3 do artigo**: diz 52 colunas para a B4 (o bruto tem 41) e 73 para a
  B5. Conferir.
