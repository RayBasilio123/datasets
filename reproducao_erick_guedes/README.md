# Como reproduzir Guedes (2020): soft sensor do teor de Fe (base B5)

Reprodução, do dado bruto até as tabelas e figuras, da dissertação

> GUEDES, É. V. O. *Aplicação de soft sensor baseado em redes neurais artificiais e random forest para predição em
> tempo real do teor de ferro no concentrado da flotação de minério de ferro*. Mestrado Profissional (PROFICAM),
> UFOP/ITV, 2020.

O trabalho estima o **teor de Fe do concentrado** (análise de laboratório a cada 2 h) a partir das variáveis de processo
de uma linha de flotação de Conceição (11 células mecânicas), de janeiro a maio de 2019. Treina em março e testa nos
outros meses. Esta pasta refaz tudo em Python, seguindo os notebooks do Erick (`github.com/eguedes/mestrado_itv`) e o
código MATLAB dele (`matlab_original/`).

## Como rodar

```bash
python3 -m venv .venv && .venv/bin/pip install -r reproducao_erick_guedes/requirements.txt
PY=.venv/bin/python WORKERS=8 bash reproducao_erick_guedes/run.sh
```

Leva cerca de 5 minutos com 16 processos (o treino é o mais pesado: 1000 treinos de cada modelo por conjunto de
entradas). Os resultados são determinísticos: rodar de novo dá exatamente os mesmos números.

**Entradas** (da pasta `raw/` deste repositório):
- `B5_processo_originais_longo.parquet`: as 65 variáveis de processo, uma linha por medição, com data e hora em
  segundos, convertidas dos `Dados_Conceicao_*.xlsx` originais do Erick;
- `B5_T_Conceicao.csv`: as análises de Fe e SiO₂ do concentrado (o alvo).

## Passo a passo e onde cada um está

| # | Passo da dissertação | Onde | Confere com a dissertação? |
|---|---|---|---|
| 1 | Janela de 2 h antes de cada análise, `(t − 2h, t]` (Tab. 3.1) | `prep.py` `agrupar` | sim: maior correlação com o Fe 0,321 (Erick 0,32) |
| 2 | Descarta medições 0 e `Bad` (notebook 06) | `prep.py` `carregar` | — |
| 3 | Mediana de cada janela (Fig. 3.2) | `prep.py` `agrupar` | sim: Fig. 3.2 idêntica; medianas iguais às do Erick em 358 de 359 janelas* |
| 4 | Preenche janelas vazias com a média do valor anterior e do seguinte (notebook 04b) | `prep.py` `preencher` | sim* |
| 5 | Normalização 0–1 | `modelos.py` (`mapminmax` dentro da RNA; mín./máx. de março no PCA) | sim: entradas do MATLAB iguais (14 de 15 variáveis)* |
| 6 | Disponibilidade > 85% (etapa 1, Fig. 3.3) | `prep.py` `selecao_automatica` | ver "Seleção de variáveis" |
| 7 | Redundância qualitativa: sai vazão mássica e válvula dardo 2 (Tab. 3.2) | idem | sim |
| 8 | Correlação ≥ 0,90 entre entradas (Tab. 3.3) | idem | sim: 0,982 / 0,920 / 0,984 / 0,930 / 0,916 (Erick 0,98 / 0,92 / 0,98 / 0,93 / 0,92) |
| 9 | RReliefF, k = 53, pesos > 0 (Fig. 4.1) | `prep.py` `rrelieff` | sim: as mesmas 15 variáveis; pesos 0,0307 / 0,0153 / 0,0147 / 0,0117 … |
| 10 | PCA com > 90% da variância (Fig. 4.2) | `modelos.py` `entradas` | sim: 10 componentes, 90,9% |
| 11 | RNA MLP 20 neurônios, LM e SCG, 1000 treinos (sec. 3.3) | `modelos.py` `MLP` | protocolo dos `.m` (abaixo) |
| 12 | RF 500 árvores, folha mínima 3 (sec. 3.4) | `modelos.py` | protocolo dos `.m` |
| 13 | Escolha por maior R e menor MSE; Tabelas 4.1–4.8, Figs. 4.4–4.7 | `metricas.py` | ver "Resultados" |
| 14 | Aplicação em jan, fev, abr e mai; MAE por mês (Figs. 4.8–4.11) | `modelos.py`, `graficos.py` | ver "Resultados" |

\* Conferido contra os arquivos finais do Erick (pasta `Delay/03-Marco` do OneDrive dele: medianas, entradas do MATLAB em
`dados.mat`). Esses arquivos não estão no repositório; a conferência está em `eguedes/reproducao_fe/` no servidor.

**Protocolo dos modelos, tirado do código MATLAB do Erick** (`matlab_original/`):
- `networ1_train001_code.m`: `fitnet(20)`, transferência **`tansig` também na camada de saída**, `mapminmax` nas entradas e
  saídas, `dividerand` 75/15/15 (o MATLAB normaliza para ≈ 71/14/14), `max_fail` 6; `trainlm` ou `trainscg`.
- `Loop.m`: nova divisão aleatória a cada 5 treinos.
- `forest_code_15.m`, `DadosTreinamento_RF15.m`: `fitrensemble` com `'Bag'`, 500 árvores, `MinLeafSize` 3, treinada em
  treino + validação da mesma divisão da RNA.
- `Salva_R_Experimento.m`, `DadosTreinamento_RF15.m`: **o MSE da RNA e da RF é calculado em todas as amostras de março**
  (`perform(net,t,net(x))`, `immse(y_geral,target)`); o R é calculado no treino, no teste e em todos.

## Resultados (MAE do Fe por mês, treino em março)

| Modelo | Mar* | Jan | Fev | Abr | Mai |
|---|---|---|---|---|---|
| **RF, PCA, maior R — Erick** | 0,59 | 0,96 | 1,06 | 1,30 | 1,18 |
| RF, PCA, maior R — aqui | 0,61 | 0,84 | 0,97 | 1,18 | 1,12 |
| RF, PCA — mediana dos 1000 treinos | 0,63 | 0,94 | 0,99 | 1,15 | 1,13 |
| **RNA LM, RReliefF, menor MSE — Erick** | 0,61 | 1,89 | 2,39 | 2,17 | 2,10 |
| RNA LM, RReliefF, menor MSE — aqui | 0,52 | 4,77 | 2,88 | 1,67 | 1,84 |
| RNA LM, RReliefF — mediana dos 1000 treinos | 0,90 | 1,81 | 1,84 | 1,62 | 1,78 |
| Repetir a média de Fe de março (referência) | 1,01 | 0,92 | 1,02 | 0,73 | 0,72 |

\* mês de treino: o MAE inclui as amostras usadas no ajuste.

| Tabela / figura | Erick | Aqui |
|---|---|---|
| RF: 5 maiores R no teste (RReliefF / PCA) — Tab. 4.5 | 0,73–0,74 / 0,74–0,77 | 0,74–0,76 / 0,73–0,76 |
| RF: treinos com MSE < 1 e < 2 — Tab. 4.8 | 0 e 1000 | 0 e 1000 |
| RF RReliefF, menor MSE: R treino / teste / todos, MSE — Fig. 4.7 | 0,898 / 0,434 / 0,878, 1,018 | 0,895 / 0,343 / 0,877, 1,046 |
| RF PCA, maior R: R treino / teste / todos — Fig. 4.6 | 0,881 / 0,771 / 0,863 | 0,872 / 0,762 / 0,862 |
| RNA LM RReliefF: treinos com R > 0,7 / > 0,6 — Tab. 4.2 | 13 / 50 | 16 / 58 |
| RNA LM RReliefF: 5 menores MSE — Tab. 4.3 | 0,75–1,02 | 0,80–0,87 |
| RNA LM RReliefF, menor MSE: R treino / val. / teste / todos, MSE — Fig. 4.5 | 0,944 / 0,388 / 0,601 / 0,871, 0,750 | 0,963 / 0,664 / 0,796 / 0,865, 0,795 |
| RNA SCG RReliefF: 5 maiores R no teste — Tab. 4.1 | 0,62–0,67 | 0,79–0,83 |

Todas as tabelas, lado a lado: `resultados/orig_atraso0h_matlab/metricas.md`. MAE, MSE, R e R² de cada modelo escolhido,
por conjunto e por mês: `resultados/orig_atraso0h_matlab/metricas_escolhidos.md` (`python metricas_escolhidos.py`).

**O que se reproduz e o que não:**
- **Dados e tratamento:** reproduzidos valor a valor.
- **RF:** reproduzida (tabelas, figuras e MAE mensal a até 0,12).
- **RNA com LM:** reproduzida na faixa. O MAE mensal do modelo escolhido depende muito do sorteio inicial (em janeiro vai
  de 1,1 a 7,1 nos 1000 treinos); a saída `tansig` satura nos valores mínimo e máximo de Fe do treino.
- **RNA com SCG:** os MSE ficam na faixa do Erick, mas os R saem bem melhores; a conclusão "LM melhor que SCG" não se reproduz.
- **Leitura dos resultados:** nos meses fora do treino, a RF fica perto de simplesmente repetir a média de março em
  janeiro e fevereiro e perde em abril e maio; a RNA perde em todos os meses. O MSE das tabelas inclui as amostras de
  treino e os "melhores" modelos vêm de sorte na divisão (mediana do R no teste nos 1000 treinos: 0,23–0,44).

## Seleção de variáveis refeita do zero

`prep.py` também aplica as etapas 1–4 sem usar as listas da dissertação (`--conjuntos auto_disp_*` em `modelos.py`).
A disponibilidade precisa ser exigida em março **e** no período jan–mai: variáveis com muitos buracos fora de março
(vazão de ar do Recleaner, válvulas dardo da S1B3) foram tiradas pelo Erick.

| Etapa | Erick | Aqui |
|---|---|---|
| Disponibilidade > 85% | 32 | 33 (+ espuma da S2B1, com 85,3% no período, no limite do corte) |
| Redundância qualitativa | 26 | 27 |
| Correlação ≥ 0,90 | 21 | 22 |
| RReliefF, pesos > 0 | 15 | 18 (as 15 + espuma da S2B1, vazão de ar do R1 e do C1) |
| PCA, > 90% | 10 | 10 |

Detalhes e MAE: `resultados/orig_atraso0h_matlab/metricas_ponta_a_ponta_disp.md` e `figuras/ponta_a_ponta/`.

## Saídas

| Pasta | Conteúdo |
|---|---|
| `dados/` (não versionada) | medianas por janela (`agrupados_*`), preenchidas (`preenchidos_*`), seleção de variáveis (`selecao_*.json`) |
| `resultados/prep_relatorio_orig.json` | conferências dos dados (correlações, RReliefF, etapas da seleção) |
| `resultados/orig_atraso0h_matlab/` | `treinos_*.csv` (os 1000 treinos de cada modelo), `resumo*.json`, `metricas*.md` |
| `figuras/` | Figs. 3.2, 3.4, 4.1, 4.2, 4.4–4.11 refeitas e a distribuição do MAE mensal nos 1000 treinos |

## Diferenças que restam

- Não há MATLAB: LM e SCG são implementações próprias em numpy; o sorteio dos pesos e das divisões é outro.
- O número de variáveis sorteadas por divisão na RF não está nos `.m`; usado 1/3 das variáveis.
- As faixas fixas do `00-Faixas.xlsx` não entram: a RNA normaliza internamente (`mapminmax`) e o PCA usa mín./máx. de março.
- A pasta `Delay` do OneDrive do Erick é um experimento posterior à dissertação (janela com 1 h de atraso, exceto no
  Cleaner 1); não é o que está no texto.
- `matlab_original/` traz os `.m` do Erick só como referência; os `.mat` (redes e divisões) não foram incluídos.
