---
name: report
description: Gera reports/apresentações executivas no padrão visual Forest Editorial (fundo branco, marca DevOps&SRE, tri-stack IBM Plex) em 3 motores — HTML custom (teto estético máximo, PDF p/ Canva), Marp (Markdown → HTML/PDF/PPTX, compatível com Notion) e Quarto (Markdown/notebook + código, Mermaid/Graphviz nativos). Cada motor traz scripts prontos de build e de exportação (html, pdf, markdown, pptx). SEMPRE pergunte qual motor o usuário quer. Gatilhos: report, relatório, apresentação, deck, slides, gerar report, gerar apresentação, presentation, pptx, reveal, marp, quarto.
user-invocable: true
---

# report — gerador de reports/apresentações (3 motores, 1 estética)

Gera apresentações executivas no padrão **Forest Editorial** (ver `reference/aesthetic.md`):
fundo branco, marca **DevOps&SRE** (logo bússola + wordmark + indicador verde),
tri-stack **IBM Plex**, verde-floresta + terracota. Um único padrão estético, **três
motores de saída** — cada um com scripts prontos de construção e de exportação.

## ⚠ Passo 0 — SEMPRE pergunte o motor primeiro

Antes de qualquer coisa, pergunte ao usuário qual motor deseja (use `AskUserQuestion`)
e explique brevemente a melhor aplicação de cada um:

- **HTML custom** — *teto estético máximo* (CSS livre). Report executivo de alto
  acabamento, importável no **Canva via PDF**; GIF/Plotly/Mermaid nativos. 1 arquivo
  leve. **Não** vai para o Notion. → Saídas: **HTML, PDF**.
- **Marp** — Markdown puro + tema. Quer **PPTX** (PowerPoint) e fonte versionável;
  pipeline simples (1 CLI). Texto **compatível com Notion**. Estética consistente,
  menos livre. → Saídas: **HTML, PDF, PPTX**.
- **Quarto** — Markdown/notebook **+ código** (py/R). Report **técnico reprodutível**;
  Mermaid/Graphviz nativos; gráficos gerados por código. **Compatível com Notion**.
  Requer o binário Quarto. → Saídas: **reveal HTML, PPTX, PDF**.

Detalhes e a matriz completa (Canva/Notion/peso): `reference/export-matrix.md`.

Se o usuário não souber decidir: **HTML** para deck executivo bonito p/ Canva;
**Marp** se exige PPTX/Notion com esforço mínimo; **Quarto** se há análise em código.

## Passo 1 — Colete os requisitos (enxuto)
1. **Nome/tema** do report e **período**.
2. **Roteiro/conteúdo** (texto, bullets, seções) — cada seção/divisória vira ~1 slide.
3. **Dados/visuais** disponíveis (imagens, GIFs, áudio, números p/ gráfico, diagramas).
4. **Saídas** desejadas (HTML/PDF/PPTX) e **destino** dos arquivos.
5. Confirme identidade visual: **Forest Editorial** (default) — só desvie com motivo.

## Passo 2 — Scaffold do motor escolhido
```bash
SKILL=modules/ai-tools/skills/report          # ajuste ao caminho real da skill
$SKILL/scripts/new-report.sh <html|marp|quarto> ./<dir-do-report>
```
Isso copia o motor + assets compartilhados e cria um deck inicial pronto para editar.
Coloque imagens/áudio em `<dir-do-report>/assets/`.

## Passo 3 — Edite o conteúdo e construa
Siga o README do motor (em `engines/<motor>/README.md`). Resumo:

| Motor | Editar | Construir | Exportar |
|---|---|---|---|
| **html** | `deck.json` (modelo de conteúdo) | `python3 build.py deck.json` → `deck.html` | `./setup.sh` (1×) + `./export.sh deck.html` → PDF + screenshots |
| **marp** | `deck.md` (Markdown + diretivas) | `./build.sh deck.md` | mesmo comando gera HTML+PDF+PPTX |
| **quarto** | `report.qmd` | `./build.sh report.qmd` | mesmo comando gera HTML+PPTX+PDF |

- Componentes e classes do tema: `reference/aesthetic.md`.
- Gráficos (Plotly embutido / imagem / código): `reference/charts.md`.
- Diagramas (Mermaid/Graphviz): `reference/diagrams.md`.

## Passo 4 — QA visual (obrigatório)
- **HTML:** o `export.py` já salva screenshots por slide em `preview/`. Inspecione-os
  (renderize via Playwright se precisar) — confira fundo branco, cabeçalho DevOps&SRE,
  ausência de overflow, gráficos/diagramas renderizados.
- **Marp/Quarto:** abra o HTML/PDF e confira a 1ª e a última página + um slide de tabela/gráfico.
- Checklists: `reference/aesthetic.md` §6, `reference/charts.md` §6, `reference/diagrams.md` §5.

## Passo 5 — Entrega
- Reúna os artefatos (HTML/PDF/PPTX + assets) e informe os caminhos.
- Para **Canva**: entregue o **PDF** (fiel) ou **PPTX** (Marp/Quarto).
- Para **Notion**: entregue o **Markdown** (Marp/Quarto) e/ou o PDF anexo.
- GIF anima só no HTML aberto no browser (estático em PDF/PPTX).

## Estrutura da skill
```
report/
  SKILL.md                      ← este guia
  shared/                       forest-editorial.css · compass-logo.svg · brand.json
  engines/
    html/    build.py · export.py · export.sh · setup.sh · slides.example.json · README
    marp/    theme.css · deck.example.md · build.sh · README
    quarto/  theme.scss · report.example.qmd · build.sh · README
  scripts/   new-report.sh      ← scaffold de um novo report
  reference/ aesthetic.md · charts.md · diagrams.md · export-matrix.md
```

## Princípios (mantidos)
- **Uma estética, três motores** — não divirja do Forest Editorial sem motivo.
- **Scripts prontos** — não improvise pipeline; use `new-report.sh` + os `build/export` do motor.
- **Sempre pergunte o motor** antes de gerar (Passo 0).
- **QA visual sempre** antes de entregar.
- Erros dos scripts seguem `{erro, message/suggestion}` — leia a sugestão antes de retry.
