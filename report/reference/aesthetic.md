# Forest Editorial — especificação estética canônica

O padrão visual dos três motores. Fonte única de verdade: `shared/brand.json`
(tokens) + `shared/forest-editorial.css` (implementação HTML) + `shared/compass-logo.svg`.
Mantenha este padrão em qualquer report; desvios precisam de motivo explícito.

## 1. Princípio
Editorial minimalism técnico em **fundo branco**, ancorado em verde-floresta com
acento terracota. Tri-stack tipográfico sans/mono. Marca **DevOps&SRE** (logo bússola
+ wordmark + indicador verde) no cabeçalho de cada slide. Bordas finas, cantos
arredondados (8–16px), sombras sutis (nunca decorativas pesadas).

## 2. Paleta (tokens)
| Token | Hex | Uso |
|---|---|---|
| `paper` / `card` | `#ffffff` | fundo de página e cards |
| `card2` | `#f6f8f6` | superfície tênue (thesis, statement) |
| `ink` | `#1b2a22` | texto principal / wordmark |
| `muted` | `#566159` | texto secundário |
| `faint` | `#8a948c` | captions, rodapé, nº de página |
| `g900` | `#0c3a25` | verde-floresta âncora (títulos, barras escuras) |
| `g700` | `#1a7a48` | verde primário (acentos, borda esquerda) |
| `g600` | `#22824f` | indicador verde do cabeçalho |
| `g500` | `#3aa564` | verde claro (anel do logo, marcadores) |
| `terra` / `terra2` | `#bd5f29` / `#9d4d1f` | terracota — acento secundário, ênfase |
| `blue` | `#2a6aa8` | terciário ocasional (notas) |
| `line` | `#e2e8e3` | bordas e divisores |

**Ordem fixa de séries** (gráficos): `g900 → g700 → terra → g500 → blue`.
Proibido: azul/roxo/rosa genéricos, amarelo de fundo, gradientes decorativos pesados.

## 3. Tipografia (tri-stack)
- **Sans** `IBM Plex Sans` — títulos e corpo. Títulos 700, corpo 400/500.
- **Mono** `IBM Plex Mono` — eyebrows, tags, nº de página, rodapé, captions de dado (uppercase, tracking `.1–.16em`).
- Display (capa) h1 ~56px peso 700 `letter-spacing:-.022em`; ênfase `<em>` em terracota.
- Sem serif. Sem Inter/Roboto/Arial como display.

Escala de referência (slide 1280×720): h1 56 · wordmark 28 · indicador 18.5 · h2 32 ·
sub 14.5 · corpo 13.5 · mono eyebrow 11.5.

## 4. Anatomia do cabeçalho (marca DevOps&SRE)
```
[aba verde][● logo bússola]  DevOps&SRE            01 · Seção (mono, canto sup. dir.)
                             Indicador do slide  ← verde (g600), papel de "título"
Subtítulo descritivo em cinza (muted), opcional.
```
- Logo: círculo `g900` com anel `g500`, estrela de 4 pontas `#48c47f`, ponto central `g900`, e uma aba `g500` à esquerda. Arquivo: `shared/compass-logo.svg` (HTML inline no `build.py`; Marp/Quarto via data-URI no tema).
- Wordmark: `DevOps&SRE`, peso 700, grafite (`ink`).
- **Indicador**: o título específico do slide, em verde `g600` — é o elemento que muda por slide (equivalente ao "Indicador …" da referência).
- Faixa verde `g700` de 5–6px na borda esquerda de cada slide.

## 5. Catálogo de componentes (classes do `forest-editorial.css`)
| Componente | Classe | Nota |
|---|---|---|
| Capa | `.slide.hero` + `.brand-lg` + `.thesis` | título + tese + atos |
| Cabeçalho | `.brand` (`.mark`+`.wm`+`.ind`) + `.sectag` | montado pelo `build.py` |
| Subtítulo | `.head .sub` | cinza, ≤82ch |
| Grid | `.cols` (defina `grid-template-columns` inline) | layout de 2–3 colunas |
| Eyebrow de bloco | `.subhead` | mono uppercase verde |
| Tags | `.tags > .tag[.t|.b]` | verde / terracota / azul |
| Card | `.card[.warn|.note]` + `.topline` | título + texto |
| Callout | `.callout[.terra|.blue]` | barra lateral colorida |
| Bullets | `.bullets[.t] > li > .mk` | marcador circular numerado/✓/▸ |
| Tabela | `.matrix > table` | header verde-escuro, 1ª coluna forte |
| KPIs | `.kpis > .kpi` | número grande tabular |
| Pilares | `.pillars > .pillar[.p2|.p3|.p4]` | topo colorido |
| Statement | `.statement` (`<em>` terracota) | frase de fechamento |
| Moldura img/GIF | `.frame > img` + `.cap` | object-fit contain |
| Diagrama | `.diagram > pre.mermaid` | ver `diagrams.md` |
| Gráfico | `.chart[data-plotly]` | ver `charts.md` |
| Áudio | `.audiobar > audio` | play terracota, fundo verde-escuro |
| Link | `.link-card[.g|.t]` | rótulo mono + url terracota |

## 6. Regras (do / don't)
- **Faça:** fundo branco; 1 ideia por slide; respiro generoso; ênfase com terracota; números tabulares; rodapé com `◆` e contexto.
- **Não faça:** parede de texto; mais de ~6 bullets; cores fora da paleta; emoji como ícone de marca (use ◆/✓/▸); sombras pesadas; serif de display.
- **Acessibilidade:** contraste AA (texto sobre branco usa `ink`/`g900`/`muted`); não comunicar só por cor.

## 7. Onde cada motor herda isto
- **HTML:** usa `forest-editorial.css` direto (fidelidade total). Teto ★★★★★.
- **Marp:** `engines/marp/theme.css` replica tokens + componentes essenciais em CSS de tema. Teto ★★★☆.
- **Quarto:** `engines/quarto/theme.scss` mapeia tokens para variáveis reveal. Teto ★★★★.
