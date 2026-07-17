#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260717-ux1-cls1"

FIXED = [
    Path("index.html"), Path("ru/index.html"),
    Path("about/index.html"), Path("ru/about/index.html"),
    Path("consultations/index.html"), Path("ru/consultations/index.html"),
    Path("privacy/index.html"), Path("ru/privacy/index.html"),
    Path("notes/index.html"), Path("ru/notes/index.html"),
]
ARTICLES = sorted(Path("notes").glob("*/index.html")) + sorted(Path("ru/notes").glob("*/index.html"))
PAGES = FIXED + ARTICLES

for relative in PAGES:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Missing production page: {relative}")
    text = path.read_text(encoding="utf-8")
    text = text.replace("&display=swap", "&display=optional")
    text = re.sub(r"site\.navigation\.v1\.css\?v=[^\"\s]+", f"site.navigation.v1.css?v={VERSION}", text)
    if "fonts.googleapis.com/css2" not in text or "display=optional" not in text:
        raise SystemExit(f"Optional font delivery policy missing in {relative}")
    path.write_text(text, encoding="utf-8")

css_path = ROOT / "assets/css/site.navigation.v1.css"
css = css_path.read_text(encoding="utf-8")
marker = "/* CLS stability V1: reserve the final editorial rail before deferred enhancement. */"
block = r'''

/* CLS stability V1: reserve the final editorial rail before deferred enhancement. */
@media (min-width: 1181px) {
  .notes-hub-hero-grid.has-editorial-rail > .editorial-rail-placeholder,
  .article-hero-grid.has-editorial-rail > .editorial-rail-placeholder {
    min-height: 560px;
    contain: layout paint;
    contain-intrinsic-size: 184px 560px;
  }

  .notes-hub-hero-grid.has-editorial-rail,
  .article-hero-grid.has-editorial-rail {
    align-items: stretch;
  }

  .notes-hub-hero-grid.has-editorial-rail > .notes-hub-heading,
  .notes-hub-hero-grid.has-editorial-rail > .notes-hub-index,
  .article-hero-grid.has-editorial-rail > .article-hero-copy,
  .article-hero-grid.has-editorial-rail > .article-hero-visual {
    min-width: 0;
  }
}
'''
if marker not in css:
    css += block
css_path.write_text(css, encoding="utf-8")

print(f"CLS stability V1 applied to {len(PAGES)} production pages")
