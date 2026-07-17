#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing file: {relative}")
    return path.read_text(encoding="utf-8")


# Canonical homepage chrome exposes the real About page while local content keeps its anchors.
ua_home = read("index.html")
ru_home = read("ru/index.html")
require('<a href="./about/">Про Аліну</a>' in ua_home, "UA home canonical About route missing")
require('<a href="./about/">Об Алине</a>' in ru_home, "RU home canonical About route missing")

# About pages use the canonical conversion destination and still connect to Notes.
for relative in ("about/index.html", "ru/about/index.html"):
    text = read(relative)
    require('href="../consultations/#contact"' in text, f"{relative}: canonical booking CTA missing")
    require('href="../notes/"' in text, f"{relative}: Notes link missing")

# Consultation pages connect specialist context, the first-consultation article, privacy and booking.
for relative in ("consultations/index.html", "ru/consultations/index.html"):
    text = read(relative)
    require('href="../about/"' in text, f"{relative}: About link missing")
    require('href="../notes/first-consultation/"' in text, f"{relative}: first-consultation link missing")
    require('href="../privacy/"' in text, f"{relative}: privacy link missing")
    require('href="#contact"' in text, f"{relative}: local consultation form route missing")

# Notes catalog has a clear editorial bridge into the canonical form.
for relative in ("notes/index.html", "ru/notes/index.html"):
    text = read(relative)
    require('class="notes-hub-conversion"' in text, f"{relative}: conversion bridge missing")
    require('href="../consultations/#contact"' in text, f"{relative}: consultation CTA missing")

css = read("assets/css/site.notes-hub.v3-2.css")
for token in (
    "Interlinking V1: editorial bridge",
    ".notes-hub-conversion-inner",
    ".notes-hub-conversion-copy",
    "@media (max-width: 800px)",
):
    require(token in css, f"Notes conversion CSS missing: {token}")

# Article pairs must stay mirrored by slug. Both locale trees navigate two levels
# upward to their own locale root: /notes/<slug>/ -> / and /ru/notes/<slug>/ -> /ru/.
ua_articles = {path.parent.name: path for path in (ROOT / "notes").glob("*/index.html")}
ru_articles = {path.parent.name: path for path in (ROOT / "ru/notes").glob("*/index.html")}
require(ua_articles, "no UA articles found")
require(ua_articles.keys() == ru_articles.keys(), "UA/RU article slug sets are not mirrored")
require(len(ua_articles) == 4, f"expected 4 article pairs, found {len(ua_articles)}")

for slug in sorted(ua_articles):
    for is_ru, path in ((False, ua_articles[slug]), (True, ru_articles[slug])):
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        prefix = "../../"
        absolute_about = "https://alinahorb.com/ru/about/" if is_ru else "https://alinahorb.com/about/"

        require(f'href="{prefix}about/"' in text, f"{relative}: author About link missing")
        require(f'href="{prefix}consultations/#contact"' in text, f"{relative}: canonical article CTA missing")
        require(absolute_about in text, f"{relative}: structured author URL missing")
        require(f'href="{prefix}#about"' not in text, f"{relative}: stale About anchor remains")
        require(f'href="{prefix}#contact"' not in text, f"{relative}: stale Contact anchor remains")
        require(f'href="{prefix}#process"' not in text, f"{relative}: stale Process anchor remains")
        require("https://alinahorb.com/#about" not in text, f"{relative}: stale absolute About anchor remains")
        require("https://alinahorb.com/ru/#about" not in text, f"{relative}: stale RU absolute About anchor remains")

# The first-consultation article specifically connects its service explanation to Consultations.
require('href="../../consultations/#process"' in read("notes/first-consultation/index.html"), "UA first article process link missing")
require('href="../../consultations/#process"' in read("ru/notes/first-consultation/index.html"), "RU first article process link missing")

# Canonical global chrome owns global routes; the Notes utility runtime only delegates.
global_chrome = read("assets/js/site.global-chrome.v1.js")
require('href: `${localeRoot}about/`' in global_chrome, "global About route missing")
require('const bookingHref = `${localeRoot}consultations/#contact`;' in global_chrome, "global booking route missing")
require('`${localeRoot}#about`' not in global_chrome, "legacy global About anchor remains")
require('`${localeRoot}#contact`' not in global_chrome, "legacy global Contact anchor remains")
chrome = read("assets/js/site.chrome.v3.js")
require('site.global-chrome.v1.js?v=20260717-chrome1' in chrome, "Notes utility runtime does not delegate to global chrome")

print("Interlinking V1 validation passed.")
