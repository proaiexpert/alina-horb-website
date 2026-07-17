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
    ".editorial-rail",
    ".rail-page-link",
    ".rail-booking-link",
    ".rail-local-link",
    ".editorial-mobile-menu",
    ".editorial-mobile-page",
    ".editorial-mobile-booking",
):
    require(selector in css, f"navigation CSS missing {selector}")

for token in (
    "@media (max-width: 1180px)",
    "--editorial-header-height",
    "body.editorial-menu-open .mobile-booking-cta",
    "grid-template-areas:",
    "prefers-reduced-motion",
):
    require(token in css, f"navigation CSS missing production token: {token}")

for token in (
    "Разделы сайта",
    "Розділи сайту",
    "Материалы",
    "Матеріали",
    "Содержание",
    "Зміст",
    'aria-current="page"',
    "IntersectionObserver",
    "MutationObserver",
    "editorial-menu-open",
    "consultations/#contact",
    "setBackgroundInert",
    "lockPage",
    'event.key === "Tab"',
    'event.key === "Escape"',
    'matchMedia("(max-width: 1180px)")',
):
    require(token in js, f"navigation runtime missing production token: {token}")

require(
    ".editorial-rail::after" in css and "content: none !important" in css,
    "legacy rail progress marker is not neutralized",
)
require("fallbackDesktopNav" in js, "desktop fallback navigation for utility pages is missing")
require(
    'document.body.classList.contains("article-template-v32")' in js,
    "article-specific navigation labeling is missing",
)
require(
    "site.navigation.v1.css?v=20260717-nav2" in js,
    "cache-safe navigation stylesheet version is missing",
)

for relative, text in (
    ("assets/js/site.v2.js", site_js),
    ("assets/js/site.chrome.v3.js", chrome_js),
):
    require(
        text.count("ALINA_EDITORIAL_NAV_LOADER_V1") == 1,
        f"{relative}: navigation loader missing or duplicated",
    )
    require(
        "site.navigation.v1.js?v=20260717-nav1" in text,
        f"{relative}: expected V1 loader reference changed unexpectedly",
    )

rail_pages = (
    "index.html",
    "ru/index.html",
    "about/index.html",
    "ru/about/index.html",
    "consultations/index.html",
    "ru/consultations/index.html",
)
for relative in rail_pages:
    text = (ROOT / relative).read_text(encoding="utf-8")
    require("mobile-navigation" in text, f"{relative}: mobile navigation host missing")
    require("side-navigation" in text, f"{relative}: desktop rail host missing")

for relative in ("notes/index.html", "ru/notes/index.html"):
    text = (ROOT / relative).read_text(encoding="utf-8")
    require("notes-hub-hero-grid" in text, f"{relative}: notes rail host missing")

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r'(site\.(?:v2|chrome\.v3)\.js)([^"\']*)', text):
        require(
            "v=20260717-nav1" in match.group(2),
            f"{path.relative_to(ROOT)}: stale shared script reference",
        )

print("Editorial navigation production validation passed.")
