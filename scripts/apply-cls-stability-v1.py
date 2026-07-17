#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FIXED = [
    Path("index.html"), Path("ru/index.html"),
    Path("about/index.html"), Path("ru/about/index.html"),
    Path("consultations/index.html"), Path("ru/consultations/index.html"),
    Path("privacy/index.html"), Path("ru/privacy/index.html"),
    Path("notes/index.html"), Path("ru/notes/index.html"),
]
PAGES = FIXED + sorted(Path("notes").glob("*/index.html")) + sorted(Path("ru/notes").glob("*/index.html"))

for relative in PAGES:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if "fonts.googleapis.com/css2" not in text:
        raise SystemExit(f"Google Fonts stylesheet missing in {relative}")
    if "&display=swap" in text:
        text = text.replace("&display=swap", "&display=optional", 1)
    elif "&display=optional" not in text:
        raise SystemExit(f"Font display policy not recognized in {relative}")
    path.write_text(text, encoding="utf-8")

css_path = ROOT / "assets/css/site.global-chrome.v1.css"
css = css_path.read_text(encoding="utf-8")
css = css.replace(
    '''.site-header--canonical .brand {
  width: 198px;
  flex: none;
}''',
    '''.site-header--canonical .brand {
  grid-column: 1;
  width: 198px;
  flex: none;
}''',
    1,
)
css = css.replace(
    '''.site-header--canonical .inner-desktop-nav {
  min-width: 0;''',
    '''.site-header--canonical .inner-desktop-nav {
  grid-column: 2;
  min-width: 0;''',
    1,
)
css = css.replace(
    '''.site-header--canonical .header-tools {
  display: flex;''',
    '''.site-header--canonical .header-tools {
  grid-column: 3;
  justify-self: end;
  display: flex;''',
    1,
)
for token in ("grid-column: 1;", "grid-column: 2;", "grid-column: 3;", "justify-self: end;"):
    if token not in css:
        raise SystemExit(f"Header stability token missing after patch: {token}")
css_path.write_text(css, encoding="utf-8")

# Keep the empty middle grid track stable when the rail becomes the primary desktop navigation.
nav_path = ROOT / "assets/js/site.navigation.v1.js"
nav = nav_path.read_text(encoding="utf-8")
old = '''  if (rail) {
    fallbackDesktopNav?.remove();
  } else if (fallbackDesktopNav) {'''
new = '''  if (rail) {
    fallbackDesktopNav?.setAttribute("hidden", "");
  } else if (fallbackDesktopNav) {'''
if old in nav:
    nav = nav.replace(old, new, 1)
elif new not in nav:
    raise SystemExit("Fallback desktop navigation ownership block not found")
nav_path.write_text(nav, encoding="utf-8")

release = ROOT / "scripts/validate-release-readiness.py"
release_text = release.read_text(encoding="utf-8")
needle = '    require("favicon-ag.svg" in text, f"{relative}: SVG favicon missing")\n'
addition = needle + '    require("&display=optional" in text and "&display=swap" not in text, f"{relative}: stable font-display policy missing")\n'
if addition not in release_text:
    if needle not in release_text:
        raise SystemExit("Release font policy insertion point missing")
    release_text = release_text.replace(needle, addition, 1)
release.write_text(release_text, encoding="utf-8")

print(f"Stable header tracks and optional font-swap policy applied to {len(PAGES)} pages")
