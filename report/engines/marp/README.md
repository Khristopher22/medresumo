# Motor Marp — Markdown → HTML / PDF / PPTX

Slides escritos em **Markdown puro** com o tema Forest Editorial. Um CLI (`marp-cli`
via `npx`), três saídas. Teto estético ★★★☆ (consistente, menos livre que o HTML),
mas o fonte é texto — fácil de versionar, revisar e **adaptar ao Notion**.

## Quando escolher
- Quer **PPTX** (PowerPoint) — mesmo que rasterizado (slides viram imagem).
- Quer fonte em Markdown versionável; pipeline simples (1 CLI, sem build próprio).
- Conteúdo majoritariamente texto/tabela/imagem; gráficos entram como **imagem**.
- Vai reaproveitar o texto no **Notion** (Markdown cola direto).

## Arquivos
| Arquivo | Papel |
|---|---|
| `theme.css` | Tema Marp Forest Editorial (marca DevOps&SRE embutida via data-URI) |
| `deck.example.md` | Deck de exemplo (capa `lead`, listas, tabela, slide `invert`) |
| `build.sh` | `npx marp-cli` → HTML, PDF e PPTX (opcional: `--mermaid` pré-renderiza) |

## Fluxo
```bash
../../scripts/new-report.sh marp ./meu-report
cd ./meu-report
$EDITOR deck.md
./build.sh deck.md            # → deck.html + deck.pdf + deck.pptx
./build.sh deck.md html       # só HTML
```

## Convenções do deck
- Front-matter: `marp: true`, `theme: forest-editorial`, `paginate: true`, `size: 16:9`,
  `footer: '◆ …'`.
- **Indicador verde** por slide: `<!-- _header: 'Título do slide' -->` (a marca
  DevOps&SRE é fixa pelo tema; o `_header` vira o indicador verde abaixo dela).
- **Capa/divisória:** `<!-- _class: lead -->` (centraliza) + `<!-- _paginate: false -->`.
- **Slide de destaque:** `<!-- _class: invert -->` (fundo verde-floresta).
- Separador de slide: `---`.
- Ênfase: `**negrito**` (verde) e `*itálico*` (terracota) — em h1/h2 o `**`/`*` fica terracota.

## Gráficos e diagramas
- Marp **não** renderiza Mermaid nem gráficos nativamente. Opções:
  1. **Gráfico como imagem:** gere PNG por código (matplotlib/plotly — ver `reference/charts.md`) e use `![w:900](grafico.png)`.
  2. **Mermaid pré-renderizado:** `./build.sh --mermaid deck.md` converte blocos ```` ```mermaid ```` em imagem (via `@mermaid-js/mermaid-cli`, requer rede na 1ª vez).
- Dimensione imagens com a sintaxe Marp: `![w:1100](x.png)`, `![h:420](x.png)`.

## Notas
- **PDF/PPTX** exigem Chromium — `marp-cli` baixa automaticamente na 1ª execução (ou defina `CHROME_PATH`).
- **PPTX = slides rasterizados** (cada slide é uma imagem dentro do .pptx; não é editável como texto). Para PPTX com formas editáveis, esse não é o caminho — use um gerador python-pptx dedicado.
- `--allow-local-files` é necessário para imagens locais (já incluso no `build.sh`).
- Importar no **Canva**: use o PDF (fiel) ou o PPTX.
