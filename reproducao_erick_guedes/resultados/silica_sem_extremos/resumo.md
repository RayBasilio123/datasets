# Metodologia de Guedes (2020) para o teor de SiO₂ do concentrado, por base

Gerado por `bases_silica.py`. Treino em um mês (o mais perto do meio do período), 1000 treinos por modelo
(200 divisões 75/15/15 × 5 ciclos), modelos e critérios de escolha do MATLAB do Erick.
**Mês de treino**: todas as análises do mês (inclui as usadas no ajuste), como o MSE e o R "todos" do Erick.
**Outros meses**: todos os meses fora do treino juntos. R² = 1 − SQE/SQT (não é R ao quadrado); negativo = erra mais do que a média do próprio período.

## B5

- 1630 análises (38 com |z| > 3 removidas) de 2019-01 a 2019-05; treino em **2019-03** (347 análises), teste nos outros 4 meses.
- Seleção: 65 variáveis de processo → disponibilidade 32 (Erick) → qualitativa 26 (Erick) → correlação 21 → RReliefF 14 | PCA 10 componentes (91,2%).
- RReliefF (pesos > 0, em ordem): `CR_vazao_vol`, `C1_ar`, `S2B3_ar`, `CR_densidade`, `CA_vazao_amina`, `S1B3_espuma`, `RC_espuma`, `C1_espuma`, `R2_espuma`, `R1_espuma`, `CA_vazao_vol`, `CA_nivel`, `CR_nivel`, `CA_densidade`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,790 | 0,568 | 0,604 | 0,424 | -0,035 | 12,182 | -7,322 | 2,721 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,874 | 0,543 | 0,621 | 0,481 | 0,107 | 1,638 | -0,119 | 0,962 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,524 | 1,095 | 0,236 | 0,732 | 0,041 | 4,532 | -2,096 | 1,569 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,428 | 1,182 | 0,175 | 0,742 | 0,087 | 2,390 | -0,633 | 1,165 |
| RF, RReliefF: mediana dos 1000 treinos | 0,852 | 0,547 | 0,618 | 0,475 | 0,293 | 1,396 | 0,046 | 0,892 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,542 | 1,061 | 0,260 | 0,716 | 0,078 | 3,193 | -1,182 | 1,268 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,444 | 1,159 | 0,191 | 0,746 | 0,134 | 1,779 | -0,215 | 0,887 |
| RF, PCA: mediana dos 1000 treinos | 0,835 | 0,571 | 0,602 | 0,485 | 0,130 | 1,668 | -0,139 | 0,981 |
| Referência: média do mês de treino | — | 1,433 | 0,000 | 0,829 | — | 1,464 | -0,000 | 0,822 |
| Referência: último resultado de laboratório | 0,383 | 1,767 | -0,234 | 0,841 | 0,474 | 1,540 | -0,052 | 0,740 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2019-01 | 328 | 2,356 / -4,323 | 1,331 / -0,385 | 0,915 / -0,001 | 0,795 / -0,053 |
| 2019-02 | 300 | 3,038 / -6,894 | 0,941 / 0,097 | 0,912 / -0,000 | 0,752 / 0,082 |
| 2019-03* | 347 | 0,424 / 0,604 | 0,481 / 0,621 | 0,829 / 0,000 | 0,841 / -0,234 |
| 2019-04 | 322 | 2,817 / -12,011 | 0,755 / -0,045 | 0,700 / -0,001 | 0,639 / -0,101 |
| 2019-05 | 333 | 2,703 / -9,174 | 0,818 / -0,041 | 0,767 / -0,005 | 0,773 / -0,206 |

Cada célula: MAE / R². \* mês de treino.

</details>

## B1

- 6636 análises (171 com |z| > 3 removidas) de 2023-05 a 2025-06; treino em **2024-05** (311 análises), teste nos outros 25 meses.
- Seleção: 33 variáveis de processo → disponibilidade 30 → qualitativa 30 → correlação 30 → RReliefF 27 | PCA 16 componentes (90,8%).
- RReliefF (pesos > 0, em ordem): `TO_LI6421_01`, `TO_LI6412_01`, `TO_LI6431_01`, `TO_AI6401_01`, `TO_LI6432_01`, `TO_LI6411_01`, `TO_LI6412_02`, `TO_LI6422_01`, `TO_LI6402_01`, `TO_DI6311_01`, `TO_SIMF6431`, `TO_LI6401_02`, `TO_LI6402_02`, `TO_SIMF6422`, `TO_SIMF641101`, `TO_FI8271_01`, `TO_SIMF640202`, `TO_PHY4814_02`, `TO_SIMF6421`, `TO_SIMF641201`, `TO_PHY4804_02`, `TO_LI6411_02`, `TO_WI4804_01`, `TO_LI6401_01`, `TO_SIMF640101`, `TO_SIMF641202`, `TO_FI6311_01`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,930 | 0,114 | 0,859 | 0,158 | -0,024 | 5,757 | -1,528 | 1,711 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,903 | 0,235 | 0,710 | 0,324 | 0,004 | 2,635 | -0,157 | 1,322 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,714 | 0,422 | 0,478 | 0,441 | -0,002 | 5,547 | -1,436 | 1,838 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,597 | 0,527 | 0,348 | 0,511 | -0,011 | 3,726 | -0,636 | 1,469 |
| RF, RReliefF: mediana dos 1000 treinos | 0,896 | 0,224 | 0,723 | 0,296 | 0,005 | 2,573 | -0,130 | 1,221 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,692 | 0,448 | 0,446 | 0,465 | -0,001 | 4,779 | -1,099 | 1,681 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,583 | 0,539 | 0,333 | 0,518 | -0,020 | 3,640 | -0,599 | 1,476 |
| RF, PCA: mediana dos 1000 treinos | 0,875 | 0,264 | 0,674 | 0,328 | -0,000 | 2,616 | -0,149 | 1,308 |
| Referência: média do mês de treino | — | 0,809 | 0,000 | 0,624 | — | 2,341 | -0,028 | 1,028 |
| Referência: último resultado de laboratório | 0,706 | 0,475 | 0,412 | 0,422 | 0,644 | 1,623 | 0,287 | 0,741 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2023-05 | 82 | 1,528 / -1,024 | 1,345 / -0,120 | 0,987 / -0,051 | 1,209 / -0,653 |
| 2023-06 | 267 | 1,921 / -1,264 | 1,357 / -0,027 | 1,256 / -0,216 | 1,140 / 0,007 |
| 2023-07 | 276 | 1,301 / -1,053 | 1,379 / -0,438 | 1,028 / -0,000 | 0,701 / 0,238 |
| 2023-08 | 172 | 1,454 / -1,415 | 1,187 / -0,247 | 0,895 / -0,027 | 0,874 / -0,236 |
| 2023-09 | 138 | 2,580 / -6,385 | 1,294 / -0,513 | 0,905 / -0,006 | 0,964 / -0,579 |
| 2023-10 | 305 | 2,212 / -1,331 | 1,492 / -0,101 | 1,356 / -0,180 | 1,027 / 0,353 |
| 2023-11 | 306 | 2,158 / -5,028 | 1,286 / -0,646 | 0,860 / -0,037 | 0,506 / 0,366 |
| 2023-12 | 324 | 1,959 / -14,968 | 1,134 / -2,504 | 0,698 / -0,503 | 0,323 / 0,332 |
| 2024-01 | 283 | 1,957 / -2,072 | 1,051 / -0,102 | 0,956 / -0,224 | 0,684 / 0,340 |
| 2024-02 | 261 | 1,850 / -1,112 | 1,344 / -0,026 | 1,188 / -0,131 | 0,876 / 0,263 |
| 2024-03 | 322 | 1,181 / -1,744 | 1,044 / -0,869 | 0,665 / -0,000 | 0,475 / 0,233 |
| 2024-04 | 313 | 0,930 / -2,181 | 0,961 / -1,155 | 0,668 / -0,239 | 0,357 / 0,146 |
| 2024-05* | 311 | 0,158 / 0,859 | 0,324 / 0,710 | 0,624 / 0,000 | 0,422 / 0,412 |
| 2024-06 | 124 | 1,499 / -1,982 | 0,900 / -0,311 | 0,957 / -0,491 | 0,557 / 0,436 |
| 2024-07 | 135 | 2,917 / -2,441 | 1,581 / -0,448 | 1,887 / -0,936 | 1,067 / 0,307 |
| 2024-08 | 276 | 2,360 / -1,702 | 1,287 / -0,135 | 1,437 / -0,526 | 1,123 / 0,098 |
| 2024-09 | 292 | 1,801 / -1,452 | 1,184 / -0,031 | 1,055 / -0,133 | 0,810 / 0,229 |
| 2024-10 | 245 | 2,276 / -3,092 | 1,333 / -0,108 | 1,051 / -0,009 | 0,715 / 0,282 |
| 2024-11 | 258 | 1,344 / -1,078 | 1,331 / -0,304 | 0,951 / -0,003 | 0,690 / 0,142 |
| 2024-12 | 251 | 1,252 / -0,734 | 1,446 / -0,345 | 0,997 / -0,002 | 0,681 / 0,304 |
| 2025-01 | 284 | 2,088 / -1,136 | 1,671 / -0,053 | 1,470 / -0,150 | 1,170 / 0,223 |
| 2025-02 | 283 | 1,635 / -0,933 | 1,604 / -0,218 | 1,211 / -0,071 | 1,040 / 0,013 |
| 2025-03 | 305 | 1,632 / -1,736 | 1,336 / -0,255 | 0,958 / -0,027 | 0,700 / 0,286 |
| 2025-04 | 300 | 1,496 / -3,159 | 1,403 / -0,948 | 0,858 / -0,023 | 0,479 / 0,440 |
| 2025-05 | 310 | 0,906 / -1,263 | 1,542 / -1,488 | 0,861 / -0,165 | 0,450 / 0,186 |
| 2025-06 | 213 | 1,315 / -1,584 | 1,560 / -0,656 | 0,986 / -0,023 | 0,646 / 0,183 |

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

- 4765 análises (103 com |z| > 3 removidas) de 2022-01 a 2023-07; treino em **2022-09** (284 análises), teste nos outros 18 meses.
- Seleção: 43 variáveis de processo → disponibilidade 42 → qualitativa 32 → correlação 32 → RReliefF 18 | PCA 14 componentes (90,4%).
- RReliefF (pesos > 0, em ordem): `pH alim. Flot (ph)`, `2Cleaner Ar (m³/h)`, `1Rougher Nível (cm)`, `Recleaner Ar (m³/h)`, `2Rougher Ar (m³/h)`, `Recleaner (cm)`, `1Cleaner Nível (cm)`, `2º Scav (cm)`, `Amido flot (g/t)`, `1Cleaner Ar (m³/h)`, `2Rougher Nível (cm)`, `2Cleaner (cm)`, `Nível CX1430CN02 (%)`, `Pressão desl 1ª P (kgf/cm²)`, `Vazão de alimentação da flotação (m³/h)`, `Pressão desl 2ª P (kgf/cm²)`, `1Rougher AR (m³/h)`, `Nível CX1490CN10 (%)`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,814 | 0,792 | 0,655 | 0,466 | -0,031 | 17,613 | -8,676 | 3,311 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,868 | 0,883 | 0,615 | 0,619 | 0,032 | 2,044 | -0,123 | 1,115 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,573 | 1,622 | 0,293 | 0,889 | 0,038 | 5,903 | -2,243 | 1,725 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,396 | 1,952 | 0,149 | 0,980 | 0,045 | 3,094 | -0,700 | 1,271 |
| RF, RReliefF: mediana dos 1000 treinos | 0,847 | 0,843 | 0,632 | 0,592 | 0,067 | 2,691 | -0,478 | 1,417 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,546 | 1,696 | 0,261 | 0,892 | 0,018 | 4,839 | -1,659 | 1,517 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,380 | 1,982 | 0,136 | 0,984 | 0,030 | 2,707 | -0,487 | 1,158 |
| RF, PCA: mediana dos 1000 treinos | 0,845 | 0,901 | 0,607 | 0,628 | 0,034 | 2,141 | -0,176 | 1,169 |
| Referência: média do mês de treino | — | 2,294 | 0,000 | 1,078 | — | 1,826 | -0,003 | 1,001 |
| Referência: último resultado de laboratório | 0,480 | 2,384 | -0,040 | 0,925 | 0,497 | 1,831 | -0,006 | 0,845 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2022-01 | 192 | 4,381 / -33,450 | 1,259 / -1,716 | 0,960 / -0,603 | 0,562 / -0,077 |
| 2022-02 | 196 | 3,579 / -10,050 | 1,302 / -0,329 | 1,042 / -0,027 | 0,846 / -0,050 |
| 2022-03 | 267 | 4,162 / -31,142 | 1,119 / -1,137 | 0,944 / -0,624 | 0,565 / -0,422 |
| 2022-04 | 253 | 1,795 / -10,731 | 0,846 / -0,465 | 0,853 / -0,422 | 0,584 / -0,151 |
| 2022-05 | 291 | 3,645 / -9,117 | 1,255 / -0,226 | 1,037 / -0,009 | 0,923 / 0,082 |
| 2022-06 | 267 | 2,965 / -4,243 | 1,321 / -0,022 | 1,216 / -0,059 | 1,214 / -0,258 |
| 2022-07 | 135 | 1,696 / -1,554 | 1,141 / -0,131 | 1,012 / -0,003 | 1,042 / -0,309 |
| 2022-08 | 310 | 2,010 / -3,421 | 0,988 / -0,101 | 0,944 / -0,016 | 0,852 / 0,129 |
| 2022-09* | 284 | 0,466 / 0,655 | 0,619 / 0,615 | 1,078 / 0,000 | 0,925 / -0,040 |
| 2022-10 | 233 | 2,818 / -5,167 | 1,094 / -0,062 | 1,044 / -0,025 | 1,005 / -0,105 |
| 2022-11 | 298 | 2,951 / -5,590 | 1,125 / 0,002 | 1,138 / -0,000 | 0,973 / -0,042 |
| 2022-12 | 252 | 4,288 / -10,804 | 1,118 / -0,081 | 1,043 / -0,133 | 1,004 / -0,006 |
| 2023-01 | 228 | 3,782 / -10,749 | 1,340 / -0,367 | 1,005 / -0,008 | 0,898 / -0,186 |
| 2023-02 | 264 | 2,815 / -7,521 | 1,206 / -0,204 | 1,057 / -0,049 | 0,822 / -0,067 |
| 2023-03 | 274 | 3,787 / -15,099 | 1,204 / -0,495 | 0,964 / -0,102 | 0,706 / 0,057 |
| 2023-04 | 154 | 4,373 / -16,906 | 1,016 / -0,179 | 0,903 / -0,018 | 0,901 / -0,302 |
| 2023-05 | 296 | 2,328 / -4,148 | 0,943 / -0,004 | 0,978 / -0,009 | 0,905 / -0,083 |
| 2023-06 | 315 | 3,447 / -10,175 | 0,922 / 0,004 | 0,915 / -0,002 | 0,789 / 0,084 |
| 2023-07 | 256 | 5,145 / -22,478 | 1,010 / -0,214 | 0,926 / -0,084 | 0,667 / 0,039 |

Cada célula: MAE / R². \* mês de treino.

</details>

## B4

- 1864 análises (45 com |z| > 3 removidas) de 2024-11 a 2025-06; treino em **2025-03** (291 análises), teste nos outros 7 meses.
- Seleção: 20 variáveis de processo → disponibilidade 20 → qualitativa 20 → correlação 20 → RReliefF 8 | PCA 11 componentes (90,2%).
- RReliefF (pesos > 0, em ordem): `vazao_amina_flotacao`, `nivel_celula_li641101`, `vazao_alimentacao_flotacao`, `nivel_celula_li640202`, `nivel_celula_li643101`, `nivel_celula_li641201`, `nivel_celula_li641202`, `nivel_celula_li643201`.

| Modelo | Mês de treino: R | MSE | R² | MAE | Outros meses: R | MSE | R² | MAE |
|---|---|---|---|---|---|---|---|---|
| RNA LM, RReliefF, menor MSE (adotada pelo Erick) | 0,754 | 1,470 | 0,534 | 0,763 | 0,020 | 14,162 | -4,310 | 2,541 |
| RF, PCA, maior R no teste (adotada pelo Erick) | 0,884 | 1,140 | 0,639 | 0,690 | 0,179 | 2,729 | -0,023 | 1,248 |
| RNA LM, RReliefF: mediana dos 1000 treinos | 0,377 | 2,825 | 0,104 | 1,123 | 0,098 | 5,651 | -1,119 | 1,605 |
| RNA SCG, RReliefF: mediana dos 1000 treinos | 0,294 | 2,902 | 0,080 | 1,146 | 0,125 | 3,363 | -0,261 | 1,346 |
| RF, RReliefF: mediana dos 1000 treinos | 0,793 | 1,522 | 0,517 | 0,788 | 0,154 | 3,189 | -0,196 | 1,439 |
| RNA LM, PCA: mediana dos 1000 treinos | 0,476 | 2,571 | 0,185 | 1,081 | 0,066 | 4,932 | -0,849 | 1,527 |
| RNA SCG, PCA: mediana dos 1000 treinos | 0,415 | 2,629 | 0,167 | 1,086 | 0,160 | 3,049 | -0,143 | 1,263 |
| RF, PCA: mediana dos 1000 treinos | 0,845 | 1,245 | 0,605 | 0,702 | 0,184 | 2,710 | -0,016 | 1,227 |
| Referência: média do mês de treino | — | 3,155 | 0,000 | 1,224 | — | 2,758 | -0,034 | 1,256 |
| Referência: último resultado de laboratório | 0,299 | 4,425 | -0,403 | 1,233 | 0,325 | 3,600 | -0,349 | 1,102 |

<details><summary>MAE e R² mês a mês</summary>

| Mês | Análises | RNA adotada | RF adotada | Média do treino | Último resultado |
|---|---|---|---|---|---|
| 2024-11 | 65 | 1,472 / -2,211 | 1,287 / -0,389 | 1,121 / -0,159 | 0,991 / -0,653 |
| 2024-12 | 215 | 3,698 / -8,399 | 1,201 / -0,024 | 1,163 / -0,027 | 1,041 / -0,220 |
| 2025-01 | 261 | 3,209 / -2,999 | 1,605 / -0,006 | 1,616 / -0,020 | 1,711 / -0,426 |
| 2025-02 | 260 | 2,525 / -2,655 | 1,438 / -0,006 | 1,364 / -0,000 | 1,473 / -0,587 |
| 2025-03* | 291 | 0,763 / 0,534 | 0,690 / 0,639 | 1,224 / 0,000 | 1,233 / -0,403 |
| 2025-04 | 285 | 2,529 / -8,325 | 0,948 / -0,042 | 1,092 / -0,165 | 0,790 / -0,151 |
| 2025-05 | 290 | 1,911 / -7,958 | 1,047 / -0,496 | 1,110 / -0,544 | 0,706 / -0,580 |
| 2025-06 | 197 | 1,708 / -2,714 | 1,294 / -0,156 | 1,235 / -0,132 | 0,939 / -0,400 |

Cada célula: MAE / R². \* mês de treino.

</details>

