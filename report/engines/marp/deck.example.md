---
marp: true
theme: forest-editorial
paginate: true
size: 16:9
header: ''
footer: '◆ Plataforma DevOps · RD Saúde'
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: 'Plataforma DevOps · RD Saúde' -->

# Report Mensal · **Exemplo**

Modelo de capa do motor **Marp** — Markdown puro, exporta HTML, PDF e PPTX.
Edite este arquivo e rode `./build.sh`.

`Período: mai/2026` · `Direção: Forest Editorial`

---

<!-- _header: 'O que este modelo entrega' -->

## Conteúdo em Markdown

- **Capa** com classe `lead`
- **Listas**, **tabelas** e **citações** estilizadas pelo tema
- **Código** com realce e blocos verde-floresta
- Exporta **PPTX** (slides rasterizados) — bom para quem exige PowerPoint

> **Teto estético médio:** o visual é consistente, mas menos livre que o motor HTML — em troca, o fonte é texto puro, fácil de versionar e adaptar ao Notion.

---

<!-- _header: 'Tabela & métricas' -->

## Superfície entregue

| Item              | Qtde | Observação                 |
| ----------------- | ---- | -------------------------- |
| Acessos read-only | 7    | GitLab, ArgoCD, Datadog…   |
| Servidores MCP    | 5    | instrumentados             |
| Evaluators        | 3    | PII + prompt injection     |
| Contextos         | 2    | Head Count · RACI          |

Gráficos entram como **imagem** (`![](grafico.png)`) — gere o PNG por código
(matplotlib/plotly) ou pré-renderize um diagrama Mermaid (ver README).

---

<!-- _class: invert -->
<!-- _header: 'Valor entregue' -->

## Do roteiro ao deck

Com **identidade, leveza e portabilidade** — Markdown que vira
HTML, PDF e PowerPoint num único comando.
