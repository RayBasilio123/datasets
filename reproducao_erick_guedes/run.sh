#!/usr/bin/env bash
# Reproduz Guedes (2020) do zero: dados -> selecao de variaveis -> RNA e RF -> metricas -> figuras.
# Uso (da raiz do repositorio ou de qualquer lugar):  bash reproducao_erick_guedes/run.sh
# Variaveis opcionais: PY (interpretador python), WORKERS (processos paralelos, padrao 8).
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-python3}
W=${WORKERS:-8}
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p resultados
{
  echo "inicio $(date)"
  "$PY" prep.py                                                   # passos 1-5 (janelas, mediana, preenchimento, selecao)
  "$PY" modelos.py --workers "$W"                                 # 1000 treinos com as variaveis da dissertacao
  "$PY" modelos.py --workers "$W" --conjuntos auto_disp_rrelieff auto_disp_pca --saida resumo_ponta_a_ponta_disp.json
  "$PY" metricas.py
  "$PY" metricas.py --conjuntos auto_disp_rrelieff auto_disp_pca --saida metricas_ponta_a_ponta_disp.md
  "$PY" graficos.py --variante listas_erick
  "$PY" graficos.py --variante ponta_a_ponta
  echo "fim $(date)"
} 2>&1 | tee resultados/run.log
