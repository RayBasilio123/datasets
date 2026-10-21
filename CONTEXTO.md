# Contexto do trabalho (até 21/10/2026)

Nota de passagem para retomar o trabalho em outra sessão (Cowork, Claude Code, outra pessoa do projeto). Resume o que
foi feito com as bases B1–B5, o que foi conferido e o que está pendente. Os detalhes estão nos arquivos indicados.

> Dados privados (PIMS da Vale). Este repositório é privado; não compartilhe esta nota nem os arquivos fora do projeto.

## 1. O repositório

Bases de flotação reversa de minério de ferro usadas no artigo **Basilio2026** (previsão da sílica do concentrado com
Time Series Foundation Models e predição conformal). Guarda os brutos com todas as variáveis, as séries processadas
exatamente como entram no artigo (`processed/`), os metadados (`datasets.json`) e a reprodução da dissertação de
Érick Guedes (`reproducao_erick_guedes/`). Ver `README.md`.

## 2. As bases: de onde vem cada uma e se é célula ou coluna

| Base | Origem | Equipamento (pelos dados) | No artigo | Período | Freq. |
|---|---|---|---|---|---|
| B1 | Vale, Timbopeba (Ouro Preto) | células mecânicas | células ✔ | 05/2023–06/2025 | 2h |
| B2 | Kaggle, *Quality Prediction in a Mining Process* (pública) | colunas | colunas ✔ | 03–09/2017 | 1h |
| B3 | Vale, Conceição II (Itabira), inferido | células mecânicas | **colunas ✘** | 01/2022–07/2023 | 2h (bruto 1h) |
| B4 | Vale, Timbopeba: base do TCC de Júlia S. Reis (UFOP, 2026) | células mecânicas | células ✔ | 11/2024–06/2025 | 2h |
| B5 | Vale, Conceição II: dissertação de Érick Guedes (PROFICAM UFOP/ITV, 2020) | células mecânicas | células ✔ | 01–05/2019 | 2h |

Como se sabe:
- **B5:** a dissertação diz "circuito de flotação de minério de ferro composto de 11 células mecânicas" e "usina de
  Conceição, em Itabira". A seção sobre colunas é só revisão bibliográfica.
- **B4:** é o `dados_consolidados_com_MM.csv` gerado pelo notebook de limpeza da Júlia (renomeia `TO_LI64…` para
  `nivel_celula_…`). O TCC descreve Timbopeba com 2 linhas de 6 células (rotor e estator), dados de 22/11/2024 a
  26/07/2025.
- **B1:** mesmas tags `TO_…` da B4, com nome original e período maior.
- **B3:** nenhuma variável diz célula ou coluna. Mas tem as mesmas 11 unidades da B5 (2 Rougher, 2 Cleaner,
  Recleaner, 6 Scavengers), caixas da mesma área de tags (`CX1430CN`), arquivo original `Flotacao_conceicao_II_all.csv`
  e nenhuma variável típica de coluna (água de lavagem, nível de interface). Provavelmente é a mesma linha da B5 em
  2022–2023. **Confirmar com quem forneceu.**

## 3. Reprodução da dissertação do Erick (Fe do concentrado, B5)

Pasta `reproducao_erick_guedes/` (README com o passo a passo; `bash run.sh` refaz tudo em ~5 min).

- Dados e tratamento reproduzidos valor a valor contra os arquivos dele: janela de 2 h antes de cada análise,
  mediana, descarte de zeros, preenchimento pela média do anterior e do seguinte.
- Seleção de variáveis: 32 → 26 → 21 → **15 (RReliefF)** → **10 componentes (PCA)**, iguais às dele. Refeita do zero
  sem as listas dele, dá 33 → 27 → 22 → 18 → 10.
- Modelos pelo código MATLAB dele (`matlab_original/`): MLP 20 neurônios com saída `tansig`, LM e SCG, divisão
  75/15/15 refeita a cada 5 treinos; RF 500 árvores, folha mínima 3. São 1000 treinos de cada modelo, treino em março e
  aplicação em jan, fev, abr e mai.

Modelos adotados por ele (março = mês de treino; o MSE dele inclui as amostras do ajuste):

| | R treino / teste / todos | MSE março | R² março | MAE mar / jan / fev / abr / mai |
|---|---|---|---|---|
| RF PCA, Erick | 0,881 / 0,771 / 0,863 | 1,238 | ~0,60 (estimado) | 0,59 / 0,96 / 1,06 / 1,30 / 1,18 |
| RF PCA, reprodução | 0,872 / 0,762 / 0,862 | 1,284 | 0,58 | 0,61 / 0,84 / 0,97 / 1,18 / 1,12 |
| RNA LM RReliefF, Erick | 0,944 / 0,601 / 0,871 | 0,750 | ~0,76 (estimado) | 0,61 / 1,89 / 2,39 / 2,17 / 2,10 |
| RNA LM RReliefF, reprodução | 0,963 / 0,796 / 0,865 | 0,795 | 0,74 | 0,52 / 4,77 / 2,88 / 1,67 / 1,84 |
| Repetir a média de março | — | — | 0 | 1,01 / 0,92 / 1,02 / 0,73 / 0,72 |

- O Erick reporta R e MSE (em todas as amostras de março) e o MAE por mês; R² não. A RF se reproduz. A RNA LM se
  reproduz na faixa, mas depende muito do sorteio. Os R da RNA SCG saem melhores que os dele.
- Fora de março o R² é negativo ou perto de zero: a RF ganha da média de março em jan e fev e perde em abr e mai.
- A pasta `Delay` do OneDrive do Erick é um experimento posterior (1 h de atraso), não o que está no texto.

## 4. A mesma metodologia para a sílica, em B1–B5

Script `reproducao_erick_guedes/bases_silica.py`. Com `--bases B5 --alvo fe` ele reproduz os treinos de Fe acima
exatamente (diferença 1e-16). Resultados em `reproducao_erick_guedes/resultados/silica/resumo.md` e
`resultados/silica_sem_extremos/resumo.md`. Os 1000 treinos (`treinos_*.parquet`) não vão para o git; rodar o script
regenera em ~6 min.

Treino em **um mês**, o mais perto do meio do período e com ≥ 75% das análises (o critério do Erick para março):
B5 mar/2019, B1 mai/2024, B2 jun/2017, B3 set/2022, B4 mar/2025. Teste em todos os outros meses.
Adaptações: B1, B4 e B2 já vêm agregadas (2 h, 2 h e 1 h); a B3 é juntada em 2 h. Saem análises de laboratório,
estados de motor e médias móveis. Análise repetida no registro seguinte é preenchimento e sai.

Variáveis em cada etapa (processo → disponibilidade → qualitativa → correlação → RReliefF | PCA):
B5 65 → 32 → 26 → 21 (listas do Erick) → 18 | 10; B1 33 → 30 → 30 → 30 → 26 | 16; B2 19 → 19 → 19 → 17 → 11 | 10;
B3 43 → 42 → 32 → 32 → 16 | 14; B4 20 → 20 → 20 → 20 → 10 | 11.

MAE da SiO₂ (pontos percentuais), mês de treino → outros meses:

| Base | RF adotada | RNA LM adotada | Média do mês de treino | Último resultado de laboratório |
|---|---|---|---|---|
| B5 | 0,78 → 1,49 | 0,56 → 4,19 | 1,28 → 1,14 | 1,21 → 0,93 |
| B1 | 0,36 → 1,88 | 0,25 → 5,36 | 0,68 → 1,27 | 0,46 → 0,89 |
| B2 | 0,40 → 0,94 | 0,52 → 1,14 | 0,65 → 0,94 | 0,47 → 0,53 |
| B3 | 0,73 → 1,68 | 0,52 → 3,90 | 1,25 → 1,25 | 1,03 → 1,08 |
| B4 | 1,19 → 1,98 | 0,95 → 3,26 | 1,86 → 1,73 | 1,64 → 1,37 |

Conclusões:
- Em todas as bases o modelo se ajusta bem ao mês de treino (R da RF 0,8–0,9) e não generaliza. Fora do treino, o R
  fica entre 0 e 0,18 e o R² é negativo. Nenhum modelo ganha de repetir a média do mês de treino.
- Repetir o último resultado de laboratório tem o menor MAE fora do treino em todas as bases. Isso conversa com o Naive
  competitivo do Basilio2026.
- O R alto no "teste" do Erick vem de sortear 15% das amostras dentro do mesmo mês: as vizinhas de 2 h ficam no treino.
- "Sem extremos" = segunda rodada sem as análises com |z| > 3 (sílica de ~8% a 38%, ~2% das análises; a B2 não tem
  nenhuma), como faz o `csv_to_gluonts.py` do Basilio2026. Os erros caem, mas a conclusão é a mesma.
- Pontos não causais repetidos do Erick ou do artigo: disponibilidade conferida também no período todo, preenchimento
  com o valor seguinte, corte de |z| com a média da base inteira.

## 5. Pendências

1. **Artigo `Basilio2026/Artigo_base/artigo_expandido/ojim_source/ojim.tex`:** a B3 está como colunas (linha 833 e
   Tabela 3, linha 895); pelos dados é célula. A linha 829 diz que a B5 testa uma "unseen plant", o que não se sustenta
   se B3 e B5 forem a mesma linha de Conceição II. Não corrigido; esperando decisão.
2. Confirmar com quem forneceu a B3 que ela é Conceição II.
3. Próximo passo possível: treinar a metodologia do Erick num período maior (divisão cronológica, como no
   Basilio2026), em vez de um mês, para comparar com os modelos de previsão do artigo.
4. RNA SCG do Erick: os R dele não se reproduzem (os daqui saem melhores); sem o MATLAB não dá para ir além.

## 6. Onde está cada coisa

| O quê | Onde |
|---|---|
| Bases, origem, colunas-alvo | `README.md`, `datasets.json` |
| Variáveis da B5 com tags do PIMS | `raw/B5_I_Conceicao_variaveis.csv`, `raw/B5_processo_originais_longo.parquet` |
| Reprodução do Erick (Fe) | `reproducao_erick_guedes/README.md`, `resultados/orig_atraso0h_matlab/metricas_escolhidos.md` |
| Sílica em B1–B5 | `reproducao_erick_guedes/resultados/silica/resumo.md` (e `silica_sem_extremos/`) |
| Dissertação do Erick, TCC da Júlia | fora do repositório: `eguedes/mestrado_itv/` no servidor do grupo |
