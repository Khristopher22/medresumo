#!/usr/bin/env bash
# Exporta o deck HTML para PDF. Estratégia de fallback:
#   1) .venv local com Playwright (alta fidelidade — respeita @page + __ready)
#   2) python do sistema com Playwright disponível
#   3) npx decktape (fallback sem Python; melhor para decks reveal.js)
# Uso: ./export.sh [deck.html]
set -euo pipefail
cd "$(dirname "$0")"
HTML="${1:-deck.html}"

if [ ! -f "$HTML" ]; then
  echo "erro: '$HTML' não existe — rode  python build.py  antes." >&2
  exit 1
fi

if [ -x .venv/bin/python ] && .venv/bin/python -c "import playwright" 2>/dev/null; then
  echo "→ exportando via .venv/playwright"
  exec .venv/bin/python export.py "$HTML"
fi

if python3 -c "import playwright" 2>/dev/null; then
  echo "→ exportando via python3/playwright do sistema"
  exec python3 export.py "$HTML"
fi

if command -v npx >/dev/null 2>&1; then
  echo "→ playwright ausente; tentando fallback  npx decktape"
  echo "  (dica: ./setup.sh instala o Playwright para fidelidade máxima)"
  OUT="${HTML%.html}.pdf"
  exec npx --yes decktape generic --pause 600 --size 1280x720 \
       --file-pattern '.slide' "file://$(pwd)/$HTML" "$OUT" || {
    echo "erro: decktape falhou. suggestion: rode ./setup.sh e use Playwright." >&2
    exit 1
  }
fi

echo "erro: nenhum exportador disponível." >&2
echo "  suggestion: rode ./setup.sh (Playwright) ou instale node/npx para decktape." >&2
exit 1
