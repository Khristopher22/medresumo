# Matriz de motores, saídas e compatibilidade

## Resumo
| Motor | Como se escreve | Teto estético | Imagens / Diagramas / Gráficos | Saídas | Canva | Notion | Peso |
|---|---|---|---|---|---|---|---|
| **HTML custom** | HTML + CSS | ★★★★★ (CSS livre) | `<img>`/GIF · Mermaid/SVG · Plotly/ECharts/Chart.js | HTML, PDF | via **PDF** | ✗ (HTML não cola) | ★ (1 arquivo / libs por CDN) |
| **Marp** | Markdown + tema CSS | ★★★☆ | img · Mermaid (pré-render) · gráfico como imagem | HTML, PDF, **PPTX** | PPTX/PDF (PPTX rasterizado) | ✓ (Markdown) | ★ (1 CLI npx) |
| **Quarto** | Markdown/notebook + código | ★★★★ (tema reveal) | img · Mermaid/Graphviz nativos · gráficos por código (py/R) | reveal HTML, **PPTX**, PDF | PPTX/PDF | ✓ (Markdown) | ★★ (1 binário) |

## Como decidir (diga isto ao usuário)
- **HTML** → *report executivo de maior acabamento*, importável no **Canva via PDF**;
  melhor para GIF/gráfico/diagrama nativos. **Não** vai para o Notion. Mais versátil visualmente.
- **Marp** → *quer PPTX (PowerPoint)* e fonte em Markdown versionável; pipeline simples
  (1 CLI). Texto **compatível com Notion**. Estética consistente, porém menos livre.
- **Quarto** → *report técnico reprodutível*: gráficos/números vindos de **código** (py/R),
  Mermaid/Graphviz nativos. Saídas reveal/PPTX/PDF. Markdown **compatível com Notion**.
  Requer instalar o binário Quarto.

## Caminho para o Canva
- **PDF** (qualquer motor) → import direto, 1 página = 1 slide (fiel; edição limitada).
- **PPTX** (Marp/Quarto) → import como slides; Marp = imagens, Quarto = pandoc nativo.
- **Imagens** (screenshots/PNG) → quando só se quer um quadro.
- **GIF** fica **estático** em PDF/PPTX/Canva (anima só no HTML aberto no browser).

## Compatibilidade com Notion
- Notion **não importa HTML** interativo. Para Notion, prefira **Marp/Quarto** (o fonte é
  Markdown e cola/adapta direto) ou exporte para PDF e anexe.

## Ferramental por motor
| Motor | Requisitos | Export tooling |
|---|---|---|
| HTML | Python 3 (build) · Playwright p/ PDF (`setup.sh`) | `export.sh` (Playwright; fallback `npx decktape`) |
| Marp | Node/npx · Chromium p/ PDF/PPTX (auto via marp-cli) | `npx @marp-team/marp-cli` (`--html/--pdf/--pptx`) |
| Quarto | binário Quarto · (decktape p/ PDF; py/R p/ gráfico por código) | `quarto render --to revealjs/pptx` + `decktape` |
