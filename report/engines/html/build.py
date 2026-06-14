#!/usr/bin/env python3
"""Monta um deck HTML standalone (Forest Editorial) a partir de um deck.json.

Motor HTML — teto estético máximo (CSS livre). Cada slide é uma página fixa
1280x720 (16:9), sem navegação, análoga a um slide .pptx. O cabeçalho da marca
DevOps&SRE (logo bússola + wordmark + indicador verde) é montado automaticamente;
o corpo de cada slide é HTML livre usando os componentes do forest-editorial.css.

Uso:
    python build.py [deck.json] [-o saida.html]

Modelo de conteúdo (deck.json) — ver slides.example.json:
    {
      "meta": {"title","lang","brand":{"wordmark"},"footer","assets_dir"},
      "slides": [
        {"kind":"cover","indicator","title","lede","byline":[{label,value}],
         "thesis":{"label","h3","acts":[{num,title,sub}]},"footer"},
        {"kind":"content","section","indicator","sub","html"},
        {"kind":"content", ...}
      ]
    }

Gráficos: no html de um slide use
    <div class="chart" style="height:220px" data-plotly='{"data":[...],"layout":{...}}'></div>
Diagramas: <div class="diagram"><pre class="mermaid">flowchart TD ...</pre></div>
Áudio:    <div class="audiobar" id="a1">...<audio src="..."></audio></div>
"""
from __future__ import annotations
import argparse
import html as _html
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def _find(name: str) -> Path:
    """Resolve um asset compartilhado: ao lado do script (cenário scaffold) ou
    no shared/ da skill (cenário rodando in-place)."""
    for cand in (BASE / name, BASE.parent.parent / "shared" / name):
        if cand.exists():
            return cand
    raise FileNotFoundError(
        f"Asset '{name}' não encontrado. Rode scripts/new-report.sh para "
        f"copiar os assets compartilhados para junto do build.py.")


# Marca DevOps&SRE inline (espelha shared/compass-logo.svg) -------------------
def _compass() -> str:
    return (
        '<svg class="compass" viewBox="0 0 100 100" aria-hidden="true">'
        '<circle cx="50" cy="50" r="45" fill="#0c3a25" stroke="#3aa564" stroke-width="6"/>'
        '<path d="M50 18 L59 41 L82 50 L59 59 L50 82 L41 59 L18 50 L41 41 Z" '
        'fill="#48c47f" stroke="#0c3a25" stroke-width="2" stroke-linejoin="round"/>'
        '<circle cx="50" cy="50" r="4.5" fill="#0c3a25"/></svg>')


def _brand(wordmark: str, indicator: str, large: bool = False) -> str:
    bcls = "brand brand-lg" if large else "brand"
    mcls = "mark mark-lg" if large else "mark"
    return (
        f'<header class="{bcls}"><span class="{mcls}"><i class="tab"></i>'
        f'{_compass()}</span><div class="bt"><b class="wm">{_html.escape(wordmark)}</b>'
        f'<span class="ind">{indicator}</span></div></header>')


def _cover(s: dict, meta: dict) -> str:
    wm = meta["brand"]["wordmark"]
    byline = "".join(
        f'<div><b>{_html.escape(b["label"])}</b>{_html.escape(b["value"])}</div>'
        for b in s.get("byline", []))
    thesis = ""
    th = s.get("thesis")
    if th:
        acts = "".join(
            f'<div class="act-row"><span class="num{" t" if a.get("accent") else ""}">'
            f'{_html.escape(a["num"])}</span><span class="tt"><b>{a["title"]}</b>'
            f'<span>{a["sub"]}</span></span></div>' for a in th.get("acts", []))
        thesis = (
            f'<div class="thesis"><span class="lbl">{_html.escape(th["label"])}</span>'
            f'<h3>{th["h3"]}</h3><div class="acts">{acts}</div></div>')
    solo = "" if thesis else " solo"
    left = (f'<div>{_brand(wm, s.get("indicator", ""), large=True)}'
            f'<h1>{s["title"]}</h1><p class="lede">{s["lede"]}</p>'
            f'<div class="byline">{byline}</div></div>')
    foot = s.get("footer", meta.get("footer", ""))
    return (f'<section class="slide hero{solo}"><div class="pad">{left}{thesis}</div>'
            f'<div class="foot">{foot}</div></section>')


def _content(s: dict, meta: dict, nn: int, total: int, sect_no: int) -> str:
    wm = meta["brand"]["wordmark"]
    sectag = ""
    if s.get("section"):
        sectag = (f'<span class="sectag"><span class="nn">{sect_no:02d}</span> · '
                  f'{s["section"]}</span>')
    sub = f'<p class="sub">{s["sub"]}</p>' if s.get("sub") else ""
    foot = s.get("footer", meta.get("footer", ""))
    return (
        f'<section class="slide"><div class="pad">{sectag}'
        f'<div class="head">{_brand(wm, s.get("indicator", ""))}{sub}</div>'
        f'{s.get("html", "")}</div>'
        f'<div class="foot">{foot}</div><div class="pg">{nn:02d} / {total:02d}</div></section>')


# Runtime (charts/mermaid/audio + sinal __ready para o exportador) ------------
RUNTIME = r"""
const BRAND={ink:"#1b2a22",g900:"#0c3a25",g700:"#1a7a48",g500:"#3aa564",terra:"#bd5f29",
  muted:"#566159",line:"#e2e8e3",sans:"IBM Plex Sans, sans-serif",mono:"IBM Plex Mono, monospace"};

async function buildCharts(){
  if(typeof Plotly==="undefined") return;
  const nodes=document.querySelectorAll('.chart[data-plotly]');
  for(const el of nodes){
    let spec; try{ spec=JSON.parse(el.getAttribute('data-plotly')); }catch(e){ console.error('chart json',e); continue; }
    const layout=Object.assign({
      paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
      font:{family:BRAND.sans, size:13, color:BRAND.muted},
      margin:{t:10,b:24,l:40,r:20}, showlegend:spec.layout&&spec.layout.showlegend||false
    }, spec.layout||{});
    await Plotly.newPlot(el, spec.data||[], layout,
      {displayModeBar:false, staticPlot:true, responsive:false});
  }
}

async function buildMermaid(){
  if(typeof mermaid==="undefined" || !document.querySelector('.mermaid')) return;
  mermaid.initialize({startOnLoad:false, securityLevel:'loose', theme:'base',
    fontFamily:BRAND.sans,
    flowchart:{useMaxWidth:false, htmlLabels:true, curve:'basis', nodeSpacing:40, rankSpacing:46},
    sequence:{useMaxWidth:false, mirrorActors:false, boxMargin:8},
    themeVariables:{
      fontFamily:BRAND.sans, fontSize:'15px',
      primaryColor:'#e7f1ea', primaryTextColor:'#0c3a25', primaryBorderColor:'#1a7a48',
      lineColor:'#566159', secondaryColor:'#f7e8da', tertiaryColor:'#ffffff',
      actorBkg:'#0c3a25', actorTextColor:'#f4efe4', actorBorder:'#1a7a48', actorLineColor:'#9fb3a3',
      signalColor:'#1b2a22', signalTextColor:'#1b2a22',
      labelBoxBkgColor:'#f7e8da', labelBoxBorderColor:'#ecc8a8', labelTextColor:'#9d4d1f',
      noteBkgColor:'#f7e8da', noteTextColor:'#9d4d1f', noteBorderColor:'#ecc8a8',
      altSectionBkgColor:'rgba(189,95,41,.05)'
    }});
  await mermaid.run({querySelector:'.mermaid'});
}

function wireAudio(){
  document.querySelectorAll('.audiobar').forEach(bar=>{
    const a=bar.querySelector('audio'); if(!a) return;
    bar.addEventListener('click',()=>{ if(a.paused){a.play();bar.style.opacity=.85;} else {a.pause();bar.style.opacity=1;} });
  });
}

(async()=>{
  try{ if(document.fonts&&document.fonts.ready) await document.fonts.ready; }catch(e){}
  try{ await buildCharts(); }catch(e){ console.error(e); }
  try{ await buildMermaid(); }catch(e){ console.error(e); }
  wireAudio();
  setTimeout(()=>{ window.__ready=true; document.body.setAttribute('data-ready','1'); }, 500);
})();
"""


def build(deck: dict, css: str) -> str:
    meta = deck.get("meta", {})
    meta.setdefault("brand", {}).setdefault("wordmark", "DevOps&SRE")
    lang = meta.get("lang", "pt-BR")
    title = meta.get("title", "Report")
    body_blocks, sect_no = [], 0
    slides = deck["slides"]
    total = len(slides)
    for i, s in enumerate(slides, 1):
        kind = s.get("kind", "content")
        if kind == "cover":
            body_blocks.append(_cover(s, meta))
        else:
            sect_no += 1
            body_blocks.append(_content(s, meta, i, total, sect_no))
    body = "\n".join(body_blocks)

    need_plotly = "data-plotly" in body
    need_mermaid = 'class="mermaid"' in body or "class='mermaid'" in body
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600'
             '&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">')
    libs = ""
    if need_plotly:
        libs += '<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>'
    if need_mermaid:
        libs += '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>'

    return (
        f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="UTF-8" />\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        f'<title>{_html.escape(title)}</title>\n{fonts}\n{libs}\n'
        f'<style>\n{css}\n</style>\n</head>\n<body>\n<div class="deck">\n{body}\n</div>\n'
        f'<script>\n{RUNTIME}\n</script>\n</body>\n</html>\n')


def main() -> None:
    ap = argparse.ArgumentParser(description="Monta deck HTML Forest Editorial.")
    ap.add_argument("deck", nargs="?", default="deck.json", help="caminho do deck.json")
    ap.add_argument("-o", "--out", default=None, help="arquivo HTML de saída")
    args = ap.parse_args()

    deck_path = Path(args.deck)
    if not deck_path.exists():
        sys.exit(f"erro: deck '{deck_path}' não encontrado. Edite o slides.example.json "
                 f"ou passe o caminho. sugestão: python build.py meu-deck.json")
    deck = json.loads(deck_path.read_text(encoding="utf-8"))
    css = _find("forest-editorial.css").read_text(encoding="utf-8")
    out = Path(args.out) if args.out else deck_path.with_suffix(".html")
    out.write_text(build(deck, css), encoding="utf-8")
    print(f"OK: {out}  ({out.stat().st_size/1024:.0f} KB, {len(deck['slides'])} slides)")
    print("PDF: python export.py  (ou ./export.sh)")


if __name__ == "__main__":
    main()
