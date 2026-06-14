# Gráficos — seleção, boas práticas e como gerar por motor

## 1. Seleção de gráfico (por tipo de dado)
| Dados | Recomendado | Alternativa |
|---|---|---|
| Tendência temporal | **Line** | Area (poucas séries) |
| Contagem diária/semanal | **Barra vertical** + média móvel | Stacked bar |
| Ranking ordenado | **Barra horizontal** | Lollipop |
| Proporção de um total | **Donut** (2–5 partes) | Stacked bar 100% (>5) |
| Distribuição | **Box/Violin** | Histograma |
| Correlação cat×cat | **Heatmap** | Bubble |
| KPI único | **KPI card** (não gráfico) | Bullet (com meta) |
| Antes/depois · variação | **Waterfall** | Paired bar |
| ≤4 categorias | **KPI cards** | — |

Regras condicionais: pie de 1 categoria → KPI card; outlier > 2× P95 → broken axis ou
truncar+nota; ranking >10 → Top 10 maiores + Top 10 menores; <3 pontos → não fazer
gráfico (use texto/KPI).

## 2. Boas práticas (todos os motores)
- **Eixos formatados por tipo:** tempo humano (`25m`, `1.2h`, `2d 3h`), moeda (`R$ 1.234`), `45.2%`, inteiro com milhar, data `dd/mm` (curto) ou `mmm/yy` (longo).
- **Legendas enriquecidas:** inclua o valor calculado — `"P50 (média: 42m)"`, não `"Série 1"`.
- **Títulos com contexto:** `"[Métrica] [por Dimensão] (filtro) — [KPI resumo]"`.
- **Rodapé de fonte:** `Fonte: [sistema] | Filtro: [...]`.
- **Rótulos de dado** quando <15 pontos; **média móvel 7d** em barras diárias; **linha de meta/SLA** tracejada quando houver alvo; **faixa P25–P75** com `alpha 0.10–0.15`.
- **Paleta da marca**, ordem fixa `g900 → g700 → terra → g500 → blue`. Fundo transparente.

## 3. HTML — Plotly embutido (recomendado)
No `html` de um slide:
```html
<div class="chart" style="height:300px"
     data-plotly='{"data":[ ... ],"layout":{ ... }}'></div>
```
O runtime injeta defaults da marca (fundo transparente, fonte IBM Plex, `staticPlot:true`).
Passe cores explícitas da paleta. **Donut canônico:**
```json
{"data":[{"type":"pie","hole":0.62,"labels":["PII","Prompt injection"],"values":[2,1],
 "sort":false,"marker":{"colors":["#1a7a48","#bd5f29"],"line":{"color":"#ffffff","width":2}},
 "textinfo":"label+value","textposition":"outside",
 "textfont":{"family":"IBM Plex Mono, monospace","size":12,"color":"#1b2a22"}}],
 "layout":{"annotations":[{"text":"<b>3</b><br>evaluators","showarrow":false,
 "font":{"family":"IBM Plex Sans, sans-serif","size":18,"color":"#0c3a25"}}]}}
```
**Barra horizontal canônica:**
```json
{"data":[{"type":"bar","orientation":"h","x":[7,5,3,2],"y":["Acessos","MCP","Evaluators","Contextos"],
 "marker":{"color":["#0c3a25","#1a7a48","#bd5f29","#3aa564"]},"text":["7","5","3","2"],
 "textposition":"outside","cliponaxis":false,"width":0.62}],
 "layout":{"margin":{"t":6,"b":22,"l":90,"r":30},
 "xaxis":{"range":[0,8],"gridcolor":"#e2e8e3","zeroline":false,"dtick":2},
 "yaxis":{"autorange":"reversed"}}}
```
Alternativas (ECharts/Chart.js) funcionam, mas Plotly é o default documentado (estático,
sem barra de modo, ótimo no PDF). Para ECharts, inclua o CDN e inicialize em script próprio.

## 4. Marp — gráfico como imagem
Marp não tem gráfico nativo. Gere um **PNG** por código e inclua:
```bash
# matplotlib → PNG (use backend Agg, fundo transparente, paleta da marca)
python3 gen_chart.py            # salva assets/superficie.png
```
```markdown
![w:1000](assets/superficie.png)
```
Snippet matplotlib (paleta da marca, sem spines):
```python
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,3.4))
ax.barh(["Contextos","Evaluators","MCP","Acessos"], [2,3,5,7],
        color=["#3aa564","#bd5f29","#1a7a48","#0c3a25"])
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.patch.set_alpha(0); ax.set_facecolor("none")
plt.tight_layout(); fig.savefig("assets/superficie.png", dpi=200, transparent=True)
```
(Plotly também serve: `fig.write_image("x.png", scale=3)` — requer `kaleido`.)

## 5. Quarto — gráfico por código (diferencial)
Bloco executável gera o gráfico na renderização:
````markdown
```{python}
#| echo: false
#| fig-align: center
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9,3.2))
ax.barh(["Acessos","MCP","Evaluators","Contextos"][::-1],[2,3,5,7],
        color=["#3aa564","#bd5f29","#1a7a48","#0c3a25"])
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.patch.set_alpha(0); plt.tight_layout(); plt.show()
```
````
Em R: ```` ```{r} ```` com ggplot2 (mesma paleta). Plotly interativo também é suportado no reveal.

## 6. Checklist de QA do gráfico
- [ ] Cor na paleta + ordem fixa de séries
- [ ] Eixo formatado por tipo (tempo/%/moeda/inteiro)
- [ ] Legenda/àrótulo com valor calculado
- [ ] Título com contexto + rodapé de fonte
- [ ] Rótulos só se <15 pontos; nada com <3 pontos
- [ ] Fundo transparente; fontes IBM Plex
