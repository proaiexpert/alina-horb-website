#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for relative in ("about/index.html", "ru/about/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    old = '<nav class="side-navigation profile-side-navigation" aria-label='
    start = text.find(old)
    if start < 0:
        raise SystemExit(f"{relative}: side navigation not found")
    nav_end = text.find('</nav>', start)
    block = text[start:nav_end]
    polished = block.replace('\n                <a href="#path">', '\n        <a href="#path">', 1)
    if polished == block:
        raise SystemExit(f"{relative}: expected indentation pattern not found")
    text = text[:start] + polished + text[nav_end:]
    path.write_text(text, encoding="utf-8")

css_path = ROOT / "assets/css/site.about.v1.css"
css = css_path.read_text(encoding="utf-8")
css = css.replace('\n\n\n/* About-page mobile booking CTA:', '\n\n/* About-page mobile booking CTA:', 1)
css_path.write_text(css, encoding="utf-8")

print("About cleanup formatting polished.")
