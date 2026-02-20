#!/usr/bin/env bash
set -euo pipefail
# Prosty skrypt bootstrap instalujący wirtualne środowisko i zależności
PYTHON=${PYTHON:-python3}
VENV_DIR=${VENV_DIR:-.venv}
echo "Creating venv at ${VENV_DIR} using ${PYTHON}"
$PYTHON -m venv "${VENV_DIR}"
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip setuptools wheel || true
if [ -f requirements.txt ]; then
  pip install -r requirements.txt || true
fi
echo "Bootstrap complete. Activate with: source ${VENV_DIR}/bin/activate"
