# Motor HTML — deck custom (teto estético máximo)

Slides fixos 1280×720 (16:9), sem navegação (análogo a `.pptx`), tema **Forest
Editorial** branco com a marca DevOps&SRE. **CSS livre** — o teto estético dos três
motores. Saídas: **HTML** (interativo, GIF/Plotly/Mermaid nativos) e **PDF** (uma
página por slide, importável no **Canva**).

## Quando escolher
- Report executivo de alto acabamento, importável no Canva via PDF.
- Precisa de GIF animado, gráfico interativo (Plotly) ou diagrama (Mermaid) nativos.
- 1 arquivo standalone; libs externas só entram por CDN quando o slide usa gráfico/diagrama.
- **Não** serve para colar no Notion (Notion não importa HTML interativo) → nesse caso use Marp/Quarto.

## Arquivos
| Arquivo | Papel |
|---|---|
| `build.py` | Lê `deck.json` (modelo de conteúdo) → emite o HTML standalone |
| `slides.example.json` | Exemplo completo (capa, bullets, gráficos, mermaid, fechamento) |
| `export.py` / `export.sh` | HTML → PDF + screenshots (Playwright; fallback `npx decktape`) |
| `setup.sh` | Cria `.venv` + instala Playwright/Chromium (one-shot) |
| `forest-editorial.css`, `compass-logo.svg` | Assets do tema (copiados pelo `new-report.sh`) |

## Fluxo
```bash
# 1. scaffold (copia engine + assets para um diretório de trabalho)
../../scripts/new-report.sh html ./meu-report
cd ./meu-report

# 2. edite o conteúdo
$EDITOR deck.json            # comece a partir do slides.example.json

# 3. gere o HTML
python3 build.py deck.json   # → deck.html

# 4. gere o PDF (uma vez: ./setup.sh para instalar o Playwright)
./setup.sh                   # one-shot
./export.sh deck.html        # → deck.pdf + preview/slide_*.png
```

## Modelo de conteúdo (`deck.json`)
```jsonc
{
  "meta": { "title", "lang", "brand": { "wordmark": "DevOps&SRE" }, "footer" },
  "slides": [
    { "kind": "cover", "indicator", "title", "lede",
      "byline": [ { "label", "value" } ],
      "thesis": { "label", "h3", "acts": [ { "num", "title", "sub", "accent?" } ] } },
    { "kind": "content", "section", "indicator", "sub", "html": "<...>" }
  ]
}
```
- **`kind:"cover"`** → capa (marca grande + título + tese). Sem número de página.
- **`kind:"content"`** → cabeçalho DevOps&SRE (indicador verde) + `sub` opcional + `html` livre.
  - `section` → tag de seção no canto superior direito (numerada automaticamente).
  - `indicator` → título verde do slide (papel do "Indicador …" da referência).
  - `html` → corpo livre usando os componentes do tema (ver `reference/aesthetic.md`).

## Componentes embutidos (use no `html` do slide)
- **Gráfico Plotly:** `<div class="chart" style="height:300px" data-plotly='{"data":[…],"layout":{…}}'></div>`
  — herda fundo transparente + fontes IBM Plex; passe cores da paleta (`#1a7a48`, `#bd5f29`, `#0c3a25`, `#3aa564`).
- **Diagrama Mermaid:** `<div class="diagram" style="height:430px"><pre class="mermaid">flowchart TD …</pre></div>`
- **Áudio:** `<div class="audiobar" id="a1"><span class="play">…</span>…<audio src="assets/x.mp3" preload="none"></audio></div>`
- **Imagem/GIF:** `<div class="frame"><img src="assets/x.gif"></div>` (GIF anima no HTML; no PDF aparece o 1º quadro).
- Layout: `.cols` (grid), cards `.card[.warn|.note]`, `.callout[.terra|.blue]`, `.bullets`, `.tags`,
  `.matrix`/`<table>`, `.kpis`/`.kpi`, `.pillars`/`.pillar`, `.statement`, `.link-card`.

## Notas
- O PDF é 16:9 (1280×720 → 960×540 pt). GIFs ficam estáticos no PDF (limitação do formato).
- `export.py` espera `window.__ready` (fontes + charts + mermaid) antes de capturar — não reduza o timeout sem motivo.
- Sem internet, Plotly/Mermaid (CDN) não carregam; o HTML continua válido, só os gráficos/diagramas ficam vazios. Para offline, baixe as libs e ajuste os `<script src>`.
