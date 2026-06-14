#!/usr/bin/env bash
# Build do motor Quarto. Gera reveal HTML, PPTX e (via decktape) PDF.
# Uso:
#   ./build.sh [report.qmd]          # html + pptx + pdf
#   ./build.sh report.qmd html       # só um formato (html|pptx|pdf|revealjs)
set -euo pipefail
cd "$(dirname "$0")"

DECK="${1:-report.example.qmd}"
ONLY="${2:-all}"

if ! command -v quarto >/dev/null 2>&1; then
  echo "erro: 'quarto' não encontrado." >&2
  echo "  message: o motor Quarto precisa do binário Quarto CLI." >&2
  echo "  suggestion: instale em https://quarto.org/docs/get-started/ (1 binário)," >&2
  echo "              ou escolha o motor HTML/Marp se não puder instalar." >&2
  exit 1
fi
[ -f "$DECK" ] || { echo "erro: deck '$DECK' não existe." >&2; exit 1; }
BASE="${DECK%.qmd}"

render_html(){ echo "→ reveal HTML"; quarto render "$DECK" --to revealjs; }
render_pptx(){ echo "→ PPTX (pandoc nativo)"; quarto render "$DECK" --to pptx; }
render_pdf(){
  echo "→ PDF (reveal → decktape)"
  [ -f "$BASE.html" ] || quarto render "$DECK" --to revealjs
  if command -v decktape >/dev/null 2>&1; then
    decktape reveal "$BASE.html" "$BASE.pdf"
  elif command -v npx >/dev/null 2>&1; then
    npx --yes decktape reveal "$BASE.html" "$BASE.pdf"
  else
    echo "  aviso: decktape/npx ausentes — abra $BASE.html?print-pdf e imprima como PDF." >&2
  fi
}

case "$ONLY" in
  html|revealjs) render_html ;;
  pptx) render_pptx ;;
  pdf)  render_pdf ;;
  all)  render_html; render_pptx; render_pdf ;;
  *) echo "erro: formato '$ONLY' inválido (html|pptx|pdf|all)" >&2; exit 1 ;;
esac
echo "OK: $BASE.* gerado(s)."
echo "nota: PPTX do Quarto é nativo (pandoc) — o tema SCSS NÃO se aplica ao PPTX;"
echo "      para PPTX com a identidade, use um reference-doc .pptx (ver README)."
