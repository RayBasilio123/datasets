# Metodologia de Guedes (2020) para o teor de SiO₂ do concentrado, por base

Gerado por `bases_silica.py`. Treino em um mês (o mais perto do meio do período), 1000 treinos por modelo
(200 divisões 75/15/15 × 5 ciclos), modelos e critérios de escolha do MATLAB do Erick.
**Mês de treino**: todas as análises do mês (inclui as usadas no ajuste), como o MSE e o R "todos" do Erick.
**Outros meses**: todos os meses fora do treino juntos. R² = 1 − SQE/SQT (não é R ao quadrado); negativo = erra mais do que a média do próprio período.

## B5

- 1668 análises de 2019-01 a 2019-05; treino em **2019-03** (358 análises), teste nos outros 4 meses.
- Seleção: 65 variáveis de processo → disponibilidade 32 (Erick) → qualitativa 26 (Erick) → correlação 21 → RReliefF 18 | PCA 10 componentes (91,0%).
- RReliefF (pesos > 0, em ordem): `CR_densidade`, `CR_vazao_vol`, `CA_vazao_amina`, `RC_espuma`, `CA_densidade`, `CA_vazao_amido`, `R2_espuma`, `S1B2_espuma`, `S2B3_ar`, `S1B3_espuma`, `C1_dardo1`, `C1_espuma`, `CA_nivel`, `CA_vazao_vol`, `S1B2_dardo1`, `R1_espuma`, `R1_ar`, `S1B1_espuma`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,893 | 1,135 | 0,788 | 0,563 | 0,022 | 43,887 | -12,320 | 4,190 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,845 | 2,396 | 0,553 | 0,779 | 0,140 | 4,051 | -0,230 | 1,487 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,609 | 3,676 | 0,314 | 1,091 | 0,079 | 18,227 | -4,532 | 2,494 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,402 | 4,553 | 0,151 | 1,181 | 0,152 | 4,248 | -0,289 | 1,208 |
| RF, RReliefF: mediana dos 1000 treinos | 0,841 | 2,094 | 0,610 | 0,732 | 0,111 | 7,364 | -1,235 | 2,182 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,505 | 4,265 | 0,204 | 1,181 | 0,026 | 20,441 | -5,204 | 2,644 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,383 | 4,614 | 0,140 | 1,185 | 0,093 | 4,730 | -0,436 | 1,320 |
| RF, PCA: mediana dos 1000 treinos | 0,820 | 2,422 | 0,548 | 0,777 | 0,129 | 4,208 | -0,277 | 1,516 |
| Referência: média do mês de treino | — | 5,362 | 0,000 | 1,278 | — | 3,311 | -0,005 | 1,141 |
| Referência: último resultado de laboratório | 0,398 | 6,459 | -0,205 | 1,212 | 0,462 | 3,549 | -0,076 | 0,928 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2019-01 | 338 | 2,699 / -3,933 | 1,584 / -0,061 | 1,314 / -0,000 | 0,991 / 0,091 |
| 2019-02 | 311 | 5,767 / -11,695 | 1,409 / 0,121 | 1,392 / -0,000 | 1,103 / -0,058 |
| 2019-03* | 358 | 0,563 / 0,788 | 0,779 / 0,553 | 1,278 / 0,000 | 1,212 / -0,205 |
| 2019-04 | 324 | 4,302 / -35,574 | 1,448 / -1,324 | 0,888 / -0,081 | 0,703 / -0,193 |
| 2019-05 | 337 | 4,121 / -17,058 | 1,499 / -0,864 | 0,980 / -0,014 | 0,920 / -0,436 |

Cada célula: MAE / R². \* mês de treino.

</details>

## B1

- 6807 análises de 2023-05 a 2025-06; treino em **2024-05** (313 análises), teste nos outros 25 meses.
- Seleção: 33 variáveis de processo → disponibilidade 30 → qualitativa 30 → correlação 30 → RReliefF 26 | PCA 16 componentes (90,8%).
- RReliefF (pesos > 0, em ordem): `TO_LI6412_01`, `TO_LI6421_01`, `TO_LI6412_02`, `TO_LI6432_01`, `TO_LI6411_01`, `TO_LI6431_01`, `TO_AI6401_01`, `TO_DI6311_01`, `TO_LI6402_01`, `TO_LI6422_01`, `TO_PHY4804_02`, `TO_LI6402_02`, `TO_PHY4814_02`, `TO_SIMF6431`, `TO_SIMF6421`, `TO_LI6401_02`, `TO_SIMF641101`, `TO_SIMF6422`, `TO_SIMF641201`, `TO_LI6401_01`, `TO_FI8271_01`, `TO_SIMF640202`, `TO_LI6411_02`, `TO_FY6104_01`, `TO_WI4804_01`, `TO_FI6311_01`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,934 | 0,151 | 0,870 | 0,252 | 0,049 | 36,544 | -6,410 | 5,363 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,870 | 0,412 | 0,643 | 0,364 | 0,007 | 5,935 | -0,204 | 1,879 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,722 | 0,606 | 0,475 | 0,491 | 0,014 | 11,820 | -1,397 | 2,602 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,573 | 0,790 | 0,316 | 0,582 | 0,005 | 8,290 | -0,681 | 2,224 |
| RF, RReliefF: mediana dos 1000 treinos | 0,887 | 0,340 | 0,706 | 0,324 | 0,019 | 5,538 | -0,123 | 1,583 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,707 | 0,616 | 0,467 | 0,512 | 0,011 | 10,778 | -1,185 | 2,479 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,581 | 0,775 | 0,329 | 0,583 | 0,007 | 8,454 | -0,714 | 2,281 |
| RF, PCA: mediana dos 1000 treinos | 0,852 | 0,434 | 0,624 | 0,370 | 0,003 | 6,105 | -0,238 | 1,927 |
| Referência: média do mês de treino | — | 1,155 | 0,000 | 0,681 | — | 5,143 | -0,043 | 1,270 |
| Referência: último resultado de laboratório | 0,731 | 0,622 | 0,461 | 0,457 | 0,694 | 3,016 | 0,388 | 0,894 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2023-05 | 86 | 6,885 / -2,703 | 2,385 / -0,044 | 1,630 / -0,064 | 2,002 / -0,194 |
| 2023-06 | 275 | 6,143 / -6,123 | 1,938 / -0,134 | 1,520 / -0,180 | 1,450 / -0,131 |
| 2023-07 | 283 | 6,945 / -14,298 | 2,054 / -0,644 | 1,214 / -0,009 | 0,868 / 0,198 |
| 2023-08 | 173 | 5,576 / -16,134 | 1,664 / -0,754 | 0,945 / -0,022 | 0,926 / -0,254 |
| 2023-09 | 138 | 3,965 / -14,251 | 1,793 / -1,502 | 0,919 / -0,013 | 0,986 / -0,716 |
| 2023-10 | 320 | 4,269 / -3,032 | 2,012 / -0,142 | 1,699 / -0,198 | 1,172 / 0,490 |
| 2023-11 | 309 | 3,910 / -5,697 | 1,728 / -0,451 | 1,008 / -0,005 | 0,616 / 0,293 |
| 2023-12 | 324 | 2,595 / -28,654 | 1,274 / -3,614 | 0,731 / -0,609 | 0,323 / 0,332 |
| 2024-01 | 287 | 5,378 / -6,974 | 1,472 / -0,193 | 1,117 / -0,138 | 0,823 / 0,399 |
| 2024-02 | 273 | 5,656 / -5,726 | 1,970 / -0,090 | 1,508 / -0,154 | 1,014 / 0,478 |
| 2024-03 | 325 | 7,062 / -22,437 | 1,799 / -1,043 | 0,778 / -0,002 | 0,570 / 0,256 |
| 2024-04 | 314 | 4,806 / -36,281 | 1,374 / -2,097 | 0,723 / -0,191 | 0,366 / 0,303 |
| 2024-05* | 313 | 0,252 / 0,870 | 0,364 / 0,643 | 0,681 / 0,000 | 0,457 / 0,461 |
| 2024-06 | 126 | 1,344 / -0,479 | 1,054 / -0,144 | 1,062 / -0,328 | 0,620 / 0,559 |
| 2024-07 | 163 | 4,240 / -0,889 | 2,610 / -0,254 | 3,178 / -0,761 | 1,498 / 0,599 |
| 2024-08 | 293 | 5,438 / -3,092 | 1,903 / -0,043 | 1,958 / -0,380 | 1,468 / 0,321 |
| 2024-09 | 298 | 5,089 / -5,754 | 1,797 / -0,243 | 1,253 / -0,107 | 1,013 / 0,209 |
| 2024-10 | 252 | 2,913 / -2,606 | 1,715 / -0,089 | 1,289 / -0,027 | 0,875 / 0,327 |
| 2024-11 | 262 | 4,684 / -7,974 | 1,705 / -0,320 | 1,105 / -0,000 | 0,797 / 0,252 |
| 2024-12 | 254 | 6,530 / -13,992 | 1,970 / -0,599 | 1,116 / -0,005 | 0,729 / 0,446 |
| 2025-01 | 298 | 5,903 / -5,232 | 2,145 / -0,057 | 1,816 / -0,178 | 1,316 / 0,391 |
| 2025-02 | 293 | 6,479 / -7,141 | 2,116 / -0,169 | 1,507 / -0,090 | 1,214 / 0,309 |
| 2025-03 | 318 | 5,832 / -3,857 | 2,103 / -0,102 | 1,420 / -0,053 | 1,023 / 0,472 |
| 2025-04 | 303 | 6,214 / -22,712 | 2,050 / -1,681 | 0,950 / -0,010 | 0,547 / 0,356 |
| 2025-05 | 312 | 7,387 / -28,646 | 2,356 / -2,244 | 0,957 / -0,086 | 0,510 / 0,348 |
| 2025-06 | 215 | 6,845 / -19,723 | 2,181 / -1,230 | 1,086 / -0,011 | 0,682 / 0,347 |

Cada célula: MAE / R². \* mês de treino.

</details>

## B2

- 3651 análises de 2017-03 a 2017-09; treino em **2017-06** (662 análises), teste nos outros 6 meses.
- Seleção: 19 variáveis de processo → disponibilidade 19 → qualitativa 19 → correlação 17 → RReliefF 11 | PCA 10 componentes (91,3%).
- RReliefF (pesos > 0, em ordem): `Flotation Column 01 Level`, `Flotation Column 02 Air Flow`, `Ore Pulp Flow`, `Ore Pulp pH`, `Flotation Column 06 Level`, `Flotation Column 02 Level`, `Flotation Column 06 Air Flow`, `Amina Flow`, `Flotation Column 03 Level`, `Flotation Column 07 Level`, `Flotation Column 04 Level`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,615 | 0,489 | 0,370 | 0,524 | 0,057 | 2,191 | -0,592 | 1,144 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,870 | 0,327 | 0,578 | 0,398 | 0,096 | 1,435 | -0,042 | 0,941 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,400 | 0,659 | 0,150 | 0,595 | 0,082 | 1,697 | -0,232 | 1,005 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,293 | 0,710 | 0,084 | 0,612 | 0,121 | 1,558 | -0,132 | 0,943 |
| RF, RReliefF: mediana dos 1000 treinos | 0,842 | 0,324 | 0,582 | 0,397 | 0,188 | 1,410 | -0,024 | 0,921 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,370 | 0,680 | 0,123 | 0,608 | 0,051 | 1,727 | -0,254 | 1,024 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,215 | 0,741 | 0,044 | 0,630 | 0,064 | 1,593 | -0,157 | 0,952 |
| RF, PCA: mediana dos 1000 treinos | 0,844 | 0,332 | 0,572 | 0,401 | 0,113 | 1,429 | -0,038 | 0,940 |
| Referência: média do mês de treino | — | 0,775 | 0,000 | 0,648 | — | 1,518 | -0,103 | 0,936 |
| Referência: último resultado de laboratório | 0,651 | 0,541 | 0,303 | 0,469 | 0,755 | 0,675 | 0,510 | 0,531 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2017-03 | 181 | 1,385 / -0,920 | 1,012 / -0,059 | 1,023 / -0,188 | 0,726 / 0,220 |
| 2017-04 | 639 | 1,237 / -0,778 | 1,000 / -0,228 | 1,021 / -0,320 | 0,553 / 0,501 |
| 2017-05 | 688 | 1,074 / -0,283 | 0,979 / -0,061 | 0,992 / -0,127 | 0,515 / 0,574 |
| 2017-06* | 662 | 0,524 / 0,370 | 0,398 / 0,578 | 0,648 / 0,000 | 0,469 / 0,303 |
| 2017-07 | 651 | 0,930 / -0,524 | 0,782 / -0,023 | 0,758 / -0,000 | 0,542 / 0,260 |
| 2017-08 | 619 | 1,245 / -0,887 | 0,971 / -0,013 | 0,927 / -0,058 | 0,472 / 0,622 |
| 2017-09 | 211 | 1,248 / -1,015 | 0,977 / -0,174 | 1,007 / -0,336 | 0,498 / 0,528 |

Cada célula: MAE / R². \* mês de treino.

</details>

## B3

- 4868 análises de 2022-01 a 2023-07; treino em **2022-09** (289 análises), teste nos outros 18 meses.
- Seleção: 43 variáveis de processo → disponibilidade 42 → qualitativa 32 → correlação 32 → RReliefF 16 | PCA 14 componentes (90,4%).
- RReliefF (pesos > 0, em ordem): `pH alim. Flot (ph)`, `1Rougher Nível (cm)`, `2Cleaner Ar (m³/h)`, `1Cleaner Nível (cm)`, `2Rougher Ar (m³/h)`, `Amido flot (g/t)`, `Recleaner (cm)`, `2º Scav (cm)`, `Recleaner Ar (m³/h)`, `2Rougher Nível (cm)`, `1Cleaner Ar (m³/h)`, `Nível CX1490CN10 (%)`, `Pressão desl 2ª P (kgf/cm²)`, `2Cleaner (cm)`, `Nível CX1430CN02 (%)`, `1Rougher AR (m³/h)`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,873 | 0,794 | 0,749 | 0,517 | 0,006 | 27,269 | -5,105 | 3,895 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,860 | 1,245 | 0,607 | 0,725 | 0,027 | 5,318 | -0,191 | 1,676 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,550 | 2,337 | 0,262 | 1,034 | 0,053 | 11,130 | -1,492 | 2,254 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,376 | 2,749 | 0,132 | 1,131 | 0,062 | 6,266 | -0,403 | 1,632 |
| RF, RReliefF: mediana dos 1000 treinos | 0,849 | 1,139 | 0,640 | 0,676 | 0,064 | 5,617 | -0,258 | 1,824 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,533 | 2,450 | 0,227 | 1,034 | 0,047 | 9,326 | -1,088 | 1,921 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,390 | 2,713 | 0,143 | 1,124 | 0,078 | 5,630 | -0,261 | 1,495 |
| RF, PCA: mediana dos 1000 treinos | 0,839 | 1,231 | 0,611 | 0,715 | 0,023 | 5,306 | -0,188 | 1,663 |
| Referência: média do mês de treino | — | 3,168 | 0,000 | 1,245 | — | 4,467 | -0,000 | 1,245 |
| Referência: último resultado de laboratório | 0,510 | 3,102 | 0,021 | 1,034 | 0,471 | 4,727 | -0,058 | 1,083 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2022-01 | 196 | 4,794 / -16,126 | 1,988 / -1,403 | 1,172 / -0,186 | 0,804 / -0,372 |
| 2022-02 | 198 | 3,796 / -8,184 | 1,897 / -0,688 | 1,185 / -0,022 | 0,943 / 0,027 |
| 2022-03 | 270 | 3,251 / -8,784 | 1,811 / -0,981 | 1,152 / -0,194 | 0,771 / -0,569 |
| 2022-04 | 254 | 3,547 / -27,323 | 1,141 / -1,009 | 0,968 / -0,431 | 0,644 / -0,393 |
| 2022-05 | 305 | 5,577 / -4,497 | 1,863 / -0,048 | 1,500 / -0,032 | 1,492 / -0,265 |
| 2022-06 | 286 | 3,562 / -1,604 | 2,094 / -0,021 | 1,791 / -0,094 | 1,746 / -0,074 |
| 2022-07 | 137 | 2,044 / -1,786 | 1,554 / -0,247 | 1,168 / -0,002 | 1,266 / -0,485 |
| 2022-08 | 313 | 2,248 / -3,099 | 1,226 / -0,219 | 1,041 / -0,006 | 0,935 / 0,073 |
| 2022-09* | 289 | 0,517 / 0,749 | 0,725 / 0,607 | 1,245 / 0,000 | 1,034 / 0,021 |
| 2022-10 | 236 | 3,189 / -5,031 | 1,398 / -0,146 | 1,157 / -0,015 | 1,076 / -0,021 |
| 2022-11 | 305 | 3,110 / -3,888 | 1,646 / -0,125 | 1,369 / -0,001 | 1,151 / 0,003 |
| 2022-12 | 255 | 3,282 / -6,107 | 1,406 / -0,192 | 1,110 / -0,088 | 1,107 / -0,049 |
| 2023-01 | 238 | 4,489 / -3,285 | 2,182 / -0,136 | 1,470 / -0,007 | 1,359 / -0,222 |
| 2023-02 | 267 | 3,409 / -6,236 | 1,762 / -0,473 | 1,236 / -0,025 | 1,029 / -0,272 |
| 2023-03 | 282 | 4,473 / -2,903 | 2,161 / -0,214 | 1,383 / -0,001 | 1,069 / 0,167 |
| 2023-04 | 155 | 4,077 / -11,781 | 1,615 / -0,676 | 1,029 / -0,019 | 0,967 / -0,007 |
| 2023-05 | 303 | 4,071 / -4,451 | 1,469 / -0,038 | 1,260 / -0,015 | 1,225 / -0,138 |
| 2023-06 | 322 | 3,757 / -4,602 | 1,332 / 0,018 | 1,160 / -0,005 | 1,055 / -0,007 |
| 2023-07 | 257 | 7,040 / -37,061 | 1,765 / -1,459 | 1,028 / -0,120 | 0,676 / 0,140 |

Cada célula: MAE / R². \* mês de treino.

</details>

## B4

- 1909 análises de 2024-11 a 2025-06; treino em **2025-03** (299 análises), teste nos outros 7 meses.
- Seleção: 20 variáveis de processo → disponibilidade 20 → qualitativa 20 → correlação 20 → RReliefF 10 | PCA 11 componentes (90,5%).
- RReliefF (pesos > 0, em ordem): `nivel_celula_li641101`, `nivel_celula_li640101`, `nivel_celula_li642201`, `nivel_celula_li643101`, `vazao_alimentacao_flotacao`, `nivel_celula_li640201`, `ph_flotacao`, `nivel_celula_li640202`, `nivel_celula_li642101`, `nivel_celula_li640102`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,896 | 2,318 | 0,803 | 0,954 | 0,110 | 40,466 | -6,348 | 3,256 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,813 | 6,302 | 0,465 | 1,185 | 0,129 | 6,648 | -0,207 | 1,979 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,413 | 10,577 | 0,102 | 1,764 | 0,011 | 37,120 | -5,741 | 3,050 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,203 | 11,486 | 0,025 | 1,829 | -0,015 | 15,871 | -1,882 | 2,434 |
| RF, RReliefF: mediana dos 1000 treinos | 0,762 | 6,778 | 0,425 | 1,280 | 0,111 | 8,966 | -0,628 | 2,395 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,466 | 10,273 | 0,128 | 1,731 | 0,047 | 37,071 | -5,732 | 3,462 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,300 | 10,826 | 0,081 | 1,718 | 0,058 | 10,603 | -0,925 | 2,217 |
| RF, PCA: mediana dos 1000 treinos | 0,804 | 6,059 | 0,486 | 1,208 | 0,104 | 8,182 | -0,486 | 2,297 |
| Referência: média do mês de treino | — | 11,785 | 0,000 | 1,857 | — | 5,757 | -0,045 | 1,730 |
| Referência: último resultado de laboratório | 0,434 | 13,336 | -0,132 | 1,642 | 0,359 | 7,069 | -0,283 | 1,373 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2024-11 | 65 | 3,687 / -33,060 | 2,079 / -1,712 | 1,459 / -0,543 | 0,991 / -0,653 |
| 2024-12 | 219 | 3,463 / -7,906 | 2,236 / -0,374 | 1,625 / -0,049 | 1,335 / -0,331 |
| 2025-01 | 275 | 4,220 / -4,872 | 2,282 / 0,031 | 2,194 / -0,015 | 2,221 / -0,348 |
| 2025-02 | 271 | 2,635 / -1,587 | 2,254 / -0,126 | 1,906 / -0,000 | 1,903 / -0,384 |
| 2025-03* | 299 | 0,954 / 0,803 | 1,185 / 0,465 | 1,857 / 0,000 | 1,642 / -0,132 |
| 2025-04 | 288 | 2,727 / -10,395 | 1,502 / -0,493 | 1,478 / -0,240 | 0,928 / -0,321 |
| 2025-05 | 293 | 2,946 / -12,878 | 1,730 / -1,020 | 1,566 / -0,519 | 0,834 / -0,367 |
| 2025-06 | 199 | 3,619 / -13,019 | 1,928 / -0,496 | 1,655 / -0,195 | 1,078 / -0,293 |

Cada célula: MAE / R². \* mês de treino.

</details>

