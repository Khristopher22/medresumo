#!/usr/bin/env python3
"""Deriva PDF (+ screenshots de QA) do deck HTML via Chromium headless (Playwright).

Cada .slide (1280x720) vira uma página 16:9 no PDF — pronto para importar no
Canva. Plotly e Mermaid renderizam via JS antes da captura (espera window.__ready).

Requer playwright instalado (rode ./setup.sh uma vez). Uso:
    python export.py [deck.html] [--no-shots]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ModuleNotFoundError:
    sys.exit("erro: playwright ausente.\n"
             "  message: o exportador PDF de alta fidelidade usa Chromium headless.\n"
             "  suggestion: rode  ./setup.sh   (cria .venv e instala playwright+chromium),\n"
             "              ou use  ./export.sh  que tenta o fallback decktape (npx).")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", nargs="?", default="deck.html")
    ap.add_argument("--no-shots", action="store_true", help="não gerar screenshots de QA")
    args = ap.parse_args()

    html = Path(args.html).resolve()
    if not html.exists():
        sys.exit(f"erro: '{html}' não encontrado — gere com  python build.py  antes.")
    pdf = html.with_suffix(".pdf")
    shots = html.parent / "preview"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=2)
        page.goto(html.as_uri(), wait_until="networkidle")
        try:
            page.wait_for_function("window.__ready === true", timeout=40000)
        except Exception:
            print("aviso: window.__ready não sinalizou em 40s — capturando assim mesmo.")
        page.wait_for_timeout(600)

        if not args.no_shots:
            shots.mkdir(exist_ok=True)
            slides = page.query_selector_all(".slide")
            for i, sl in enumerate(slides, 1):
                sl.screenshot(path=str(shots / f"slide_{i:02d}.png"))
            print(f"screenshots: {len(slides)} → {shots}/")

        page.emulate_media(media="print")
        page.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
        browser.close()

    print(f"OK: {pdf.name}  ({pdf.stat().st_size/1024/1024:.1f} MB)")


if __name__ == "__main__":
    main()
