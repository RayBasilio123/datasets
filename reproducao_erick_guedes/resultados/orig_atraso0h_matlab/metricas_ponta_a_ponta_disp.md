# Métricas dos 1000 treinos vs. Guedes (2020) — janela com atraso 0 h

Conjuntos de entrada comparados: auto_disp_rrelieff (coluna RReliefF) e auto_disp_pca (coluna PCA).

Formato das células: valor do Erick / valor desta reprodução. MSE em %² de Fe.

## Redes neurais

### Tabela 4.1 — maiores R no teste

| Pos. | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| 1 | 0,774 / 0,776 | 0,669 / 0,840 | 0,716 / 0,854 | 0,554 / 0,771 |
| 2 | 0,773 / 0,758 | 0,648 / 0,804 | 0,707 / 0,814 | 0,532 / 0,746 |
| 3 | 0,771 / 0,746 | 0,640 / 0,798 | 0,692 / 0,760 | 0,510 / 0,741 |
| 4 | 0,770 / 0,728 | 0,639 / 0,782 | 0,689 / 0,751 | 0,507 / 0,736 |
| 5 | 0,751 / 0,721 | 0,617 / 0,777 | 0,686 / 0,737 | 0,501 / 0,729 |

### Tabela 4.2 — treinos com R alto no teste

| | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| R > 0,7 | 13 / 9 | 0 / 23 | 2 / 11 | 0 / 10 |
| R > 0,6 | 50 / 38 | 8 / 53 | 15 / 38 | 0 / 47 |

### Tabela 4.3 — menores MSE (aqui: MSE no teste)

| Pos. | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| 1 | 0,750 / 0,658 | 1,577 / 0,589 | 0,927 / 0,527 | 2,261 / 0,493 |
| 2 | 0,858 / 0,876 | 1,795 / 0,603 | 1,358 / 0,703 | 2,279 / 0,508 |
| 3 | 0,958 / 0,949 | 1,857 / 0,624 | 1,401 / 0,851 | 2,296 / 0,603 |
| 4 | 1,019 / 1,014 | 1,870 / 0,664 | 1,439 / 0,910 | 2,364 / 0,636 |
| 5 | 1,020 / 1,020 | 1,908 / 0,681 | 1,475 / 0,935 | 2,395 / 0,649 |

### Tabela 4.4 — treinos com MSE baixo (aqui: MSE no teste)

| | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| MSE < 1,0 | 3 / 3 | 0 / 39 | 1 / 6 | 0 / 49 |
| MSE < 2,0 | 43 / 141 | 6 / 374 | 14 / 136 | 0 / 366 |

### Tabela 4.3 — menores MSE (aqui: MSE em todo março)

| Pos. | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| 1 | 0,750 / 0,690 | 1,577 / 1,844 | 0,927 / 0,755 | 2,261 / 1,691 |
| 2 | 0,858 / 0,770 | 1,795 / 1,855 | 1,358 / 0,941 | 2,279 / 1,796 |
| 3 | 0,958 / 0,795 | 1,857 / 1,874 | 1,401 / 0,976 | 2,296 / 1,815 |
| 4 | 1,019 / 0,801 | 1,870 / 1,878 | 1,439 / 0,994 | 2,364 / 1,959 |
| 5 | 1,020 / 0,819 | 1,908 / 2,031 | 1,475 / 1,021 | 2,395 / 1,981 |

### Tabela 4.4 — treinos com MSE baixo (aqui: MSE em todo março)

| | RReliefF LM (Erick / aqui) | RReliefF SCG (Erick / aqui) | PCA LM (Erick / aqui) | PCA SCG (Erick / aqui) |
|---|---|---|---|---|
| MSE < 1,0 | 3 / 15 | 0 / 0 | 1 / 4 | 0 / 0 |
| MSE < 2,0 | 43 / 428 | 6 / 4 | 14 / 337 | 0 / 5 |

## Random Forest

### Tabela 4.5 — maiores R no teste

| Pos. | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| 1 | 0,744 / 0,778 | 0,771 / 0,711 |
| 2 | 0,741 / 0,762 | 0,754 / 0,703 |
| 3 | 0,734 / 0,761 | 0,752 / 0,682 |
| 4 | 0,731 / 0,755 | 0,739 / 0,681 |
| 5 | 0,726 / 0,748 | 0,738 / 0,679 |

### Tabela 4.6 — treinos com R alto no teste

| | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| R > 0,7 | 10 / 21 | 19 / 2 |
| R > 0,6 | 77 / 81 | 74 / 86 |

### Tabela 4.7 — menores MSE (aqui: MSE no teste)

| Pos. | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| 1 | 1,018 / 0,490 | 1,083 / 0,587 |
| 2 | 1,021 / 0,504 | 1,093 / 0,589 |
| 3 | 1,023 / 0,510 | 1,093 / 0,605 |
| 4 | 1,024 / 0,516 | 1,094 / 0,606 |
| 5 | 1,024 / 0,518 | 1,106 / 0,608 |

### Tabela 4.8 — treinos com MSE baixo (aqui: MSE no teste)

| | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| MSE < 1,0 | 0 / 71 | 0 / 78 |
| MSE < 2,0 | 1000 / 451 | 1000 / 443 |

### Tabela 4.7 — menores MSE (aqui: MSE em todo março)

| Pos. | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| 1 | 1,018 / 1,052 | 1,083 / 1,185 |
| 2 | 1,021 / 1,056 | 1,093 / 1,192 |
| 3 | 1,023 / 1,059 | 1,093 / 1,195 |
| 4 | 1,024 / 1,059 | 1,094 / 1,195 |
| 5 | 1,024 / 1,064 | 1,106 / 1,196 |

### Tabela 4.8 — treinos com MSE baixo (aqui: MSE em todo março)

| | RReliefF RF (Erick / aqui) | PCA RF (Erick / aqui) |
|---|---|---|
| MSE < 1,0 | 0 / 0 | 0 / 0 |
| MSE < 2,0 | 1000 / 1000 | 1000 / 1000 |

## Modelos escolhidos (Figuras 4.4–4.7)

| Figura | Modelo | Critério | R treino | R validação | R teste | R todos | MSE | Origem |
|---|---|---|---|---|---|---|---|---|
| Fig. 4.4 | LM RReliefF | maior R no teste | 0,886 | 0,211 | 0,770 | 0,782 | 1,240 | Erick |
| | | | 0,856 | 0,197 | 0,776 | 0,777 | 2,413 | aqui |
| Fig. 4.5 | LM RReliefF | menor MSE | 0,944 | 0,388 | 0,601 | 0,871 | 0,750 | Erick |
| | | | 0,854 | 0,515 | 0,559 | 0,771 | 0,658 | aqui (MSE no teste) |
| | | | 0,953 | 0,873 | 0,581 | 0,884 | 0,690 | aqui (MSE em todo março) |
| Fig. 4.6 | RF PCA | maior R no teste | 0,881 | — | 0,771 | 0,863 | 1,238 | Erick |
| | | | 0,858 | — | 0,711 | 0,840 | 1,662 | aqui |
| Fig. 4.7 | RF RReliefF | menor MSE | 0,898 | — | 0,434 | 0,878 | 1,018 | Erick |
| | | | 0,884 | — | 0,599 | 0,872 | 0,490 | aqui (MSE no teste) |
| | | | 0,898 | — | 0,371 | 0,875 | 1,052 | aqui (MSE em todo março) |
