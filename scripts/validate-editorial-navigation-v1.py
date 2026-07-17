#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

css = (ROOT / "assets/css/site.navigation.v1.css").read_text(encoding="utf-8")
js = (ROOT / "assets/js/site.navigation.v1.js").read_text(encoding="utf-8")
site_js = (ROOT / "assets/js/site.v2.js").read_text(encoding="utf-8")
chrome_js = (ROOT / "assets/js/site.chrome.v3.js").read_text(encoding="utf-8")

for selector in (
    ".editorial-rail", ".rail-page-link", ".rail-booking-link",
    ".rail-local-link", ".editorial-mobile-menu", ".editorial-mobile-page",
):
    require(selector in css, f"navigation CSS missing {selector}")

for token in (
    "Разделы сайта", "Розділи сайту", "На этой странице", "На цій сторінці",
    "aria-current=\"page\"", "IntersectionObserver", "editorial-menu-open",
    "consultations/#contact",
):
    require(token in js, f"navigation runtime missing {token}")

for relative, text in (("assets/js/site.v2.js", site_js), ("assets/js/site.chrome.v3.js", chrome_js)):
    require(text.count("ALINA_EDITORIAL_NAV_LOADER_V1") == 1, f"{relative}: navigation loader missing or duplicated")
    require("site.navigation.v1.js?v=20260717-nav1" in text, f"{relative}: cache-safe navigation runtime missing")

core_pages = (
    "index.html", "ru/index.html", "about/index.html", "ru/about/index.html",
    "consultations/index.html", "ru/consultations/index.html",
    "notes/index.html", "ru/notes/index.html",
)
for relative in core_pages:
    text = (ROOT / relative).read_text(encoding="utf-8")
    require("mobile-navigation" in text, f"{relative}: mobile navigation host missing")
    if "notes/" not in relative:
        require("side-navigation" in text, f"{relative}: desktop rail host missing")

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r'(site\.(?:v2|chrome\.v3)\.js)([^"\']*)', text):
        require("v=20260717-nav1" in match.group(2), f"{path.relative_to(ROOT)}: stale shared script reference")

require("inner-desktop-nav") in chrome_js, "site.chrome.v3.js structure unexpectedly changed")
print("Editorial navigation V1 validation passed.")
