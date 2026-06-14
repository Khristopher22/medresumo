#!/usr/bin/env bash
# Bootstrap do exportador HTML→PDF: cria .venv local e instala playwright+chromium.
# One-shot — rode uma vez por diretório de report. O runtime do report (o HTML)
# NÃO depende disto; só a exportação de PDF de alta fidelidade depende.
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
if [ ! -d .venv ]; then
  echo "→ criando .venv"
  "$PY" -m venv .venv
fi
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install --quiet --upgrade pip
python -m pip install --quiet playwright
echo "→ instalando Chromium (playwright)"
python -m playwright install chromium
echo "OK: .venv pronto. Agora rode  ./export.sh  para gerar o PDF."
