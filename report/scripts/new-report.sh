#!/usr/bin/env bash
# Scaffold de um novo report. Copia o motor escolhido + assets compartilhados
# para um diretório de trabalho, já com um deck inicial pronto para editar.
#
# Uso: ./new-report.sh <html|marp|quarto> <diretório-destino>
set -euo pipefail

TYPE="${1:-}"
DEST="${2:-}"
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SHARED="$SKILL_ROOT/shared"

usage(){ echo "uso: $0 <html|marp|quarto> <diretório-destino>" >&2; exit 1; }
[ -n "$TYPE" ] && [ -n "$DEST" ] || usage
case "$TYPE" in html|marp|quarto) ;; *) echo "erro: tipo '$TYPE' inválido." >&2; usage ;; esac

ENGINE="$SKILL_ROOT/engines/$TYPE"
[ -d "$ENGINE" ] || { echo "erro: motor '$TYPE' não encontrado em $ENGINE" >&2; exit 1; }

mkdir -p "$DEST/assets"
cp -r "$ENGINE/." "$DEST/"
cp "$SHARED/compass-logo.svg" "$DEST/" 2>/dev/null || true

case "$TYPE" in
  html)
    cp "$SHARED/forest-editorial.css" "$DEST/"
    [ -f "$DEST/deck.json" ] || cp "$DEST/slides.example.json" "$DEST/deck.json"
    NEXT=$'  $EDITOR deck.json\n  python3 build.py deck.json\n  ./setup.sh && ./export.sh deck.html   # PDF'
    ;;
  marp)
    [ -f "$DEST/deck.md" ] || cp "$DEST/deck.example.md" "$DEST/deck.md"
    NEXT=$'  $EDITOR deck.md\n  ./build.sh deck.md            # html + pdf + pptx'
    ;;
  quarto)
    [ -f "$DEST/report.qmd" ] || cp "$DEST/report.example.qmd" "$DEST/report.qmd"
    NEXT=$'  $EDITOR report.qmd\n  ./build.sh report.qmd        # html + pptx + pdf'
    ;;
esac

chmod +x "$DEST"/*.sh 2>/dev/null || true
echo "OK: report '$TYPE' criado em  $DEST/"
echo "coloque imagens/áudio em  $DEST/assets/"
echo "próximos passos:"
echo "$NEXT"
