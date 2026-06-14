# Motor Quarto — Markdown/notebook + código

Slides em Markdown com **código embutido** (Python/R), **Mermaid e Graphviz nativos**.
Teto estético ★★★★ (tema reveal). Saídas: **reveal HTML**, **PPTX**, **PDF**.

## Quando escolher
- Report **técnico e reprodutível**: os números/gráficos vêm de análise em código.
- Quer Mermaid/Graphviz nativos sem pré-renderizar.
- Vai versionar o fonte e reaproveitar texto no **Notion** (Markdown).
- **Requer** o binário Quarto instalado (≠ HTML/Marp, que rodam só com Python/Node).

## Arquivos
| Arquivo | Papel |
|---|---|
| `theme.scss` | Tema reveal Forest Editorial (marca DevOps&SRE fixa via data-URI) |
| `report.example.qmd` | Deck de exemplo (mermaid nativo, tabela, callout, bloco `{python}` opcional) |
| `build.sh` | `quarto render` → revealjs HTML, PPTX e PDF (via decktape) |

## Fluxo
```bash
../../scripts/new-report.sh quarto ./meu-report
cd ./meu-report
$EDITOR report.qmd
./build.sh report.qmd            # → .html + .pptx + .pdf
./build.sh report.qmd html       # só reveal HTML
```

## Convenções
- Cada `##` vira um slide; o título do slide é o **indicador verde** (a marca
  DevOps&SRE é fixada pelo tema no topo-esquerdo).
- `#` cria slide de seção (divisória).
- `{.smaller}` reduz a fonte do slide; `{.callout-note}` para destaques.
- Ênfase: `**negrito**` (verde) e `*itálico*` (terracota).

## Gráficos por código (diferencial do Quarto)
Descomente o bloco `{python}` no exemplo (requer Python + matplotlib no ambiente):
```python
#| echo: false
import matplotlib.pyplot as plt
# … use a paleta da marca: #0c3a25 #1a7a48 #bd5f29 #3aa564
```
Para R, use blocos ```` ```{r} ````. Veja `reference/charts.md` para padrões de gráfico.

## Diagramas nativos
- Mermaid: bloco ```` ```{mermaid} ```` (tema `base`, cores da marca via `classDef`).
- Graphviz: bloco ```` ```{dot} ````.

## Saídas e Canva
- **reveal HTML** — apresentação interativa (tema completo aplicado).
- **PDF** — via `decktape` sobre o HTML; importável no **Canva**.
- **PPTX** — `quarto render --to pptx` é **nativo do pandoc**: vira PowerPoint
  editável, porém o **tema SCSS não se aplica**. Para identidade no PPTX, gere um
  `reference-doc` (`quarto render --to pptx -M reference-doc:rd-template.pptx`)
  a partir de um modelo .pptx com a marca RD nos layouts.

## Notas
- Sem Quarto instalado, `build.sh` falha com instrução de instalação — prefira HTML/Marp nesse caso.
- O tema usa Google Fonts (IBM Plex) via `@import`; offline, cai para a fonte de sistema.
