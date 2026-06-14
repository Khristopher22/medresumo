#!/usr/bin/env bash
# Build do motor Marp via marp-cli (npx — sem instalação global).
# Gera HTML, PDF e PPTX a partir de um deck Markdown + theme.css.
# Uso:
#   ./build.sh [deck.md]            # gera html + pdf + pptx
#   ./build.sh deck.md html         # só um formato (html|pdf|pptx)
#   ./build.sh --mermaid deck.md    # pré-renderiza ```mermaid``` em PNG antes
set -euo pipefail
cd "$(dirname "$0")"

MERMAID=0
if [ "${1:-}" = "--mermaid" ]; then MERMAID=1; shift; fi
DECK="${1:-deck.example.md}"
ONLY="${2:-all}"

if ! command -v npx >/dev/null 2>&1; then
  echo "erro: npx (Node.js) não encontrado." >&2
  echo "  suggestion: instale Node 18+ — marp-cli roda via 'npx @marp-team/marp-cli'." >&2
  exit 1
fi
[ -f "$DECK" ] || { echo "erro: deck '$DECK' não existe." >&2; exit 1; }

MARP="npx --yes @marp-team/marp-cli@latest"
BASE="${DECK%.md}"
COMMON=(--theme theme.css --allow-local-files)

# Chromium p/ PDF/PPTX. No WSL, o marp-cli tenta achar o Chrome do Windows e falha
# (spawn cmd.exe ENOENT) — então auto-detectamos um Chromium Linux e exportamos CHROME_PATH.
if [ -z "${CHROME_PATH:-}" ]; then
  for c in "$(command -v chromium 2>/dev/null)" "$(command -v chromium-browser 2>/dev/null)" \
           "$(command -v google-chrome 2>/dev/null)" \
           $(ls -d "$HOME"/.cache/ms-playwright/chromium-*/chrome-linux*/chrome 2>/dev/null | sort -r); do
    if [ -n "$c" ] && [ -x "$c" ]; then export CHROME_PATH="$c"; break; fi
  done
fi
[ -n "${CHROME_PATH:-}" ] && echo "→ CHROME_PATH=$CHROME_PATH"

# Pré-renderização opcional de blocos ```mermaid``` → PNG (Marp não tem Mermaid nativo)
if [ "$MERMAID" = "1" ]; then
  echo "→ pré-renderizando Mermaid (mermaid-cli) — requer rede na 1ª vez"
  npx --yes @mermaid-js/mermaid-cli -i "$DECK" -o "$DECK" 2>/dev/null \
    && echo "  blocos mermaid convertidos em <img>" \
    || echo "  aviso: mermaid-cli indisponível; mantenha gráficos como imagem."
fi

run(){ echo "→ $1"; $MARP "$DECK" "${COMMON[@]}" "$2" -o "$BASE.$3"; }

case "$ONLY" in
  html) run "HTML" --html html ;;
  pdf)  run "PDF"  --pdf  pdf ;;
  pptx) run "PPTX" --pptx pptx ;;
  all)
    run "HTML" --html html
    run "PDF"  --pdf  pdf
    run "PPTX" --pptx pptx ;;
  *) echo "erro: formato '$ONLY' inválido (html|pdf|pptx|all)" >&2; exit 1 ;;
esac
echo "OK: $BASE.* gerado(s)."
echo "nota: PDF/PPTX usam Chromium (marp-cli baixa na 1ª execução; ou defina CHROME_PATH)."
