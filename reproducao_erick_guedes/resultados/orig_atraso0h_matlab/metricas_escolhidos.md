# MAE, MSE, R e R² dos modelos escolhidos vs. dissertação

R² aqui = coeficiente de determinação (1 − SQE/SQT) em cada conjunto; não é R ao quadrado.
R² do Erick (não reportado) estimado como 1 − MSE/variância do Fe de março (variância = 3,084).
Nos meses, o R² usa a média do próprio mês: negativo = erra mais do que a média do mês.

## Fig. 4.4 — RNA LM, RReliefF, maior R no teste

Treino escolhido: divisão 11, ciclo 4.

| Conjunto | R Erick | R aqui | MSE Erick | MSE aqui | R² Erick (estimado) | R² aqui | MAE aqui |
|---|---|---|---|---|---|---|---|
| treino (março) | 0,886 | 0,733 | — | 1,620 | — | 0,537 | 0,914 |
| validacao (março) | 0,211 | 0,303 | — | 1,634 | — | -0,429 | 1,037 |
| teste (março) | 0,770 | 0,832 | — | 1,916 | — | 0,343 | 0,977 |
| todos (março) | 0,782 | 0,701 | 1,240 | 1,664 | 0,598 | 0,460 | 0,940 |

| Mês | MAE Erick | MAE aqui | MSE aqui | R aqui | R² aqui |
|---|---|---|---|---|---|
| Mar* | — | 0,940 | 1,664 | 0,701 | 0,460 |
| Jan | — | 1,433 | 3,931 | 0,060 | -0,994 |
| Fev | — | 1,548 | 5,466 | 0,168 | -0,881 |
| Abr | — | 2,288 | 12,360 | 0,170 | -13,603 |
| Mai | — | 2,653 | 17,420 | 0,228 | -13,969 |

## Fig. 4.5 / 4.8–4.9 — RNA LM, RReliefF, menor MSE (adotada)

Treino escolhido: divisão 167, ciclo 3.

| Conjunto | R Erick | R aqui | MSE Erick | MSE aqui | R² Erick (estimado) | R² aqui | MAE aqui |
|---|---|---|---|---|---|---|---|
| treino (março) | 0,944 | 0,963 | — | 0,181 | — | 0,926 | 0,303 |
| validacao (março) | 0,388 | 0,664 | — | 2,685 | — | 0,411 | 1,073 |
| teste (março) | 0,601 | 0,796 | — | 1,986 | — | 0,583 | 1,024 |
| todos (março) | 0,871 | 0,865 | 0,750 | 0,795 | 0,757 | 0,742 | 0,515 |

| Mês | MAE Erick | MAE aqui | MSE aqui | R aqui | R² aqui |
|---|---|---|---|---|---|
| Mar* | 0,613 | 0,515 | 0,795 | 0,865 | 0,742 |
| Jan | 1,889 | 4,766 | 36,281 | 0,142 | -17,402 |
| Fev | 2,393 | 2,882 | 17,204 | 0,045 | -4,919 |
| Abr | 2,171 | 1,667 | 5,555 | 0,017 | -5,564 |
| Mai | 2,102 | 1,844 | 6,086 | 0,050 | -4,230 |

## Fig. 4.6 / 4.10–4.11 — RF, PCA, maior R no teste (adotada)

Treino escolhido: divisão 52, ciclo 2.

| Conjunto | R Erick | R aqui | MSE Erick | MSE aqui | R² Erick (estimado) | R² aqui | MAE aqui |
|---|---|---|---|---|---|---|---|
| treino (março) | 0,881 | 0,872 | — | 1,310 | — | 0,598 | 0,592 |
| teste (março) | 0,771 | 0,762 | — | 1,126 | — | 0,449 | 0,706 |
| todos (março) | 0,863 | 0,862 | 1,238 | 1,284 | 0,598 | 0,584 | 0,608 |

| Mês | MAE Erick | MAE aqui | MSE aqui | R aqui | R² aqui |
|---|---|---|---|---|---|
| Mar* | 0,590 | 0,608 | 1,284 | 0,862 | 0,584 |
| Jan | 0,965 | 0,840 | 1,810 | 0,290 | 0,082 |
| Fev | 1,062 | 0,969 | 2,667 | 0,298 | 0,083 |
| Abr | 1,301 | 1,178 | 1,984 | 0,105 | -1,344 |
| Mai | 1,182 | 1,122 | 2,145 | 0,035 | -0,844 |

## Fig. 4.7 — RF, RReliefF, menor MSE

Treino escolhido: divisão 64, ciclo 3.

| Conjunto | R Erick | R aqui | MSE Erick | MSE aqui | R² Erick (estimado) | R² aqui | MAE aqui |
|---|---|---|---|---|---|---|---|
| treino (março) | 0,898 | 0,895 | — | 1,110 | — | 0,680 | 0,584 |
| teste (março) | 0,434 | 0,343 | — | 0,667 | — | -0,202 | 0,667 |
| todos (março) | 0,878 | 0,877 | 1,018 | 1,046 | 0,670 | 0,661 | 0,596 |

| Mês | MAE Erick | MAE aqui | MSE aqui | R aqui | R² aqui |
|---|---|---|---|---|---|
| Mar* | — | 0,596 | 1,046 | 0,877 | 0,661 |
| Jan | — | 1,195 | 2,356 | 0,221 | -0,195 |
| Fev | — | 1,013 | 2,430 | 0,423 | 0,164 |
| Abr | — | 1,035 | 1,691 | 0,161 | -0,998 |
| Mai | — | 1,188 | 2,405 | 0,102 | -1,066 |

\* março é o mês de treino (inclui as amostras usadas no ajuste).
