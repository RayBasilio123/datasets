# Métricas dos 1000 treinos vs. Guedes (2020) — janela com atraso 0 h

Conjuntos de entrada comparados: rrelieff15 (coluna RReliefF) e pca10 (coluna PCA).

Formato das células: valor do Erick / valor desta reprodução. MSE em %² de Fe.

## Redes neurais

### Tabela 4.1 — maiores R no teste

| Pos. | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| 1 | 0,774 / 0,832 | 0,669 / 0,832 | 0,716 / 0,848 | 0,554 / 0,836 |
| 2 | 0,773 / 0,815 | 0,648 / 0,819 | 0,707 / 0,835 | 0,532 / 0,761 |
| 3 | 0,771 / 0,808 | 0,640 / 0,810 | 0,692 / 0,799 | 0,510 / 0,761 |
| 4 | 0,770 / 0,798 | 0,639 / 0,793 | 0,689 / 0,798 | 0,507 / 0,760 |
| 5 | 0,751 / 0,796 | 0,617 / 0,789 | 0,686 / 0,776 | 0,501 / 0,747 |

### Tabela 4.2 — treinos com R alto no teste

| | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| R > 0,7 | 13 / 16 | 0 / 19 | 2 / 7 | 0 / 10 |
| R > 0,6 | 50 / 58 | 8 / 54 | 15 / 28 | 0 / 38 |

### Tabela 4.3 — menores MSE (aqui: MSE no teste)

| Pos. | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| 1 | 0,750 / 0,661 | 1,577 / 0,518 | 0,927 / 0,941 | 2,261 / 0,564 |
| 2 | 0,858 / 0,816 | 1,795 / 0,561 | 1,358 / 0,945 | 2,279 / 0,588 |
| 3 | 0,958 / 0,857 | 1,857 / 0,595 | 1,401 / 0,946 | 2,296 / 0,589 |
| 4 | 1,019 / 0,901 | 1,870 / 0,623 | 1,439 / 0,963 | 2,364 / 0,592 |
| 5 | 1,020 / 0,915 | 1,908 / 0,661 | 1,475 / 0,967 | 2,395 / 0,624 |

### Tabela 4.4 — treinos com MSE baixo (aqui: MSE no teste)

| | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| MSE < 1,0 | 3 / 7 | 0 / 42 | 1 / 7 | 0 / 51 |
| MSE < 2,0 | 43 / 151 | 6 / 367 | 14 / 143 | 0 / 361 |

### Tabela 4.3 — menores MSE (aqui: MSE em todo março)

| Pos. | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| 1 | 0,750 / 0,795 | 1,577 / 1,422 | 0,927 / 1,090 | 2,261 / 1,924 |
| 2 | 0,858 / 0,824 | 1,795 / 1,554 | 1,358 / 1,123 | 2,279 / 2,013 |
| 3 | 0,958 / 0,846 | 1,857 / 1,662 | 1,401 / 1,183 | 2,296 / 2,058 |
| 4 | 1,019 / 0,852 | 1,870 / 1,674 | 1,439 / 1,231 | 2,364 / 2,068 |
| 5 | 1,020 / 0,867 | 1,908 / 1,674 | 1,475 / 1,231 | 2,395 / 2,126 |

### Tabela 4.4 — treinos com MSE baixo (aqui: MSE em todo março)

| | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| MSE < 1,0 | 3 / 13 | 0 / 0 | 1 / 0 | 0 / 0 |
| MSE < 2,0 | 43 / 447 | 6 / 18 | 14 / 238 | 0 / 1 |

## Random Forest

### Tabela 4.5 — maiores R no teste

| Pos. | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| 1 | 0,744 / 0,755 | 0,771 / 0,762 |
| 2 | 0,741 / 0,752 | 0,754 / 0,762 |
| 3 | 0,734 / 0,742 | 0,752 / 0,759 |
| 4 | 0,731 / 0,740 | 0,739 / 0,754 |
| 5 | 0,726 / 0,739 | 0,738 / 0,728 |

### Tabela 4.6 — treinos com R alto no teste

| | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| R > 0,7 | 10 / 6 | 19 / 5 |
| R > 0,6 | 77 / 66 | 74 / 63 |

### Tabela 4.7 — menores MSE (aqui: MSE no teste)

| Pos. | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| 1 | 1,018 / 0,489 | 1,083 / 0,562 |
| 2 | 1,021 / 0,494 | 1,093 / 0,606 |
| 3 | 1,023 / 0,504 | 1,093 / 0,609 |
| 4 | 1,024 / 0,513 | 1,094 / 0,621 |
| 5 | 1,024 / 0,521 | 1,106 / 0,624 |

### Tabela 4.8 — treinos com MSE baixo (aqui: MSE no teste)

| | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| MSE < 1,0 | 0 / 68 | 0 / 105 |
| MSE < 2,0 | 1000 / 463 | 1000 / 447 |

### Tabela 4.7 — menores MSE (aqui: MSE em todo março)

| Pos. | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| 1 | 1,018 / 1,046 | 1,083 / 1,189 |
| 2 | 1,021 / 1,063 | 1,093 / 1,194 |
| 3 | 1,023 / 1,070 | 1,093 / 1,200 |
| 4 | 1,024 / 1,075 | 1,094 / 1,206 |
| 5 | 1,024 / 1,075 | 1,106 / 1,214 |

### Tabela 4.8 — treinos com MSE baixo (aqui: MSE em todo março)

| | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| MSE < 1,0 | 0 / 0 | 0 / 0 |
| MSE < 2,0 | 1000 / 1000 | 1000 / 1000 |

## Modelos escolhidos (Figuras 4.4–4.7)

| Figura | Modelo | Critério | R treino | R validação | R teste | R todos | MSE | Origem |
|---|---|---|---|---|---|---|---|---|
| Fig. 4.4 | LM RReliefF | maior R no teste | 0,886 | 0,211 | 0,770 | 0,782 | 1,240 | Erick |
| | | | 0,733 | 0,303 | 0,832 | 0,701 | 1,916 | aqui |
| Fig. 4.5 | LM RReliefF | menor MSE | 0,944 | 0,388 | 0,601 | 0,871 | 0,750 | Erick |
| | | | 0,825 | 0,421 | 0,808 | 0,749 | 0,661 | aqui (MSE no teste) |
| | | | 0,963 | 0,664 | 0,796 | 0,865 | 0,795 | aqui (MSE em todo março) |
| Fig. 4.6 | RF PCA | maior R no teste | 0,881 | — | 0,771 | 0,863 | 1,238 | Erick |
| | | | 0,872 | — | 0,762 | 0,862 | 1,126 | aqui |
| Fig. 4.7 | RF RReliefF | menor MSE | 0,898 | — | 0,434 | 0,878 | 1,018 | Erick |
| | | | 0,885 | — | 0,641 | 0,877 | 0,489 | aqui (MSE no teste) |
| | | | 0,895 | — | 0,343 | 0,877 | 1,046 | aqui (MSE em todo março) |
