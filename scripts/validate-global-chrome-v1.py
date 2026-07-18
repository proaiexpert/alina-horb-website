#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260717-ux1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def production_pages() -> list[Path]:
    fixed = [
        ROOT / "index.html",
        ROOT / "ru/index.html",
        ROOT / "about/index.html",
        ROOT / "ru/about/index.html",
        ROOT / "consultations/index.html",
        ROOT / "ru/consultations/index.html",
        ROOT / "privacy/index.html",
        ROOT / "ru/privacy/index.html",
        ROOT / "notes/index.html",
        ROOT / "ru/notes/index.html",
    ]
    articles = sorted((ROOT / "notes").glob("*/index.html")) + sorted((ROOT / "ru/notes").glob("*/index.html"))
    pages = fixed + articles
    require(all(path.is_file() for path in pages), "one or more production HTML files are missing")
    require(len(pages) == 18, f"expected 18 production HTML files, found {len(pages)}")
    return pages


def context(path: Path) -> tuple[bool, str, str, str]:
    relative = path.relative_to(ROOT)
    depth = len(relative.parent.parts)
    root_prefix = "../" * depth
    is_ru = bool(relative.parent.parts and relative.parent.parts[0] == "ru")
    clean_parts = relative.parent.parts[1:] if is_ru else relative.parent.parts
    clean_route = "/".join(clean_parts)
    if clean_route:
        clean_route += "/"
    locale_home = (("../" * max(depth - 1, 0)) or "./") if is_ru else (root_prefix or "./")
    alternate = f"{root_prefix}{clean_route}" if is_ru else f"{root_prefix}ru/{clean_route}"
    return is_ru, root_prefix, locale_home, alternate or "./"


for path in production_pages():
    relative = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    is_ru, root_prefix, locale_home, alternate = context(path)
    asset = f"{root_prefix}assets/"

    require(text.count('<header class="site-header') == 1, f"{relative}: canonical header count is not one")
    require('site-header--canonical' in text, f"{relative}: canonical header class missing")
    require('data-menu-toggle' in text and 'data-mobile-nav' in text, f"{relative}: mobile header controls missing")
    require(text.count('<footer class="site-footer"') == 1, f"{relative}: canonical footer count is not one")
    require('data-site-footer="canonical"' in text, f"{relative}: canonical footer marker missing")

    for token in (
        'footer-editorial-grid', 'footer-identity', 'footer-navigation', 'footer-contact',
        'footer-booking', 'footer-utility', 'maker-credit',
    ):
        require(token in text, f"{relative}: footer token missing: {token}")

    global_css = f'{asset}css/site.global-chrome.v1.css?v={VERSION}'
    nav_css = f'{asset}css/site.navigation.v1.css?v={VERSION}'
    nav_js = f'{asset}js/site.navigation.v1.js?v={VERSION}'
    require(text.count(global_css) == 1, f"{relative}: global chrome CSS missing or duplicated")
    require(text.count(nav_css) == 1, f"{relative}: navigation CSS missing or duplicated")
    require(text.count(nav_js) == 1, f"{relative}: navigation JS missing or duplicated")
    require('site.global-chrome.v1.js' not in text, f"{relative}: runtime chrome renderer remains")
    require('site.chrome.v3.js' not in text, f"{relative}: utility DOM mutation runtime remains")
    require('site.notes-images.v3-1.js' not in text, f"{relative}: Notes image mutation runtime remains")
    require(f'{asset}images/logos/favicon-ag.svg' in text, f"{relative}: canonical SVG favicon missing")
    require(f'href="{locale_home}consultations/#contact"' in text, f"{relative}: canonical booking route missing")
    require(f'href="{alternate}"' in text, f"{relative}: mirrored language route missing")

    if is_ru:
        require('Об Алине' in text and 'Консультации' in text and 'Заметки' in text, f"{relative}: RU navigation labels missing")
        require('Психологические консультации на русском и украинском языках' in text, f"{relative}: RU footer positioning missing")
    else:
        require('Про Аліну' in text and 'Консультації' in text and 'Нотатки' in text, f"{relative}: UA navigation labels missing")
        require('Психологічні консультації українською та російською мовами' in text, f"{relative}: UA footer positioning missing")

    is_notes = relative in {"notes/index.html", "ru/notes/index.html"}
    is_article = "/notes/" in relative and not is_notes
    if is_notes or is_article:
        require('has-editorial-rail' in text, f"{relative}: stable rail grid class missing")
        require('editorial-rail-placeholder' in text, f"{relative}: stable rail placeholder missing")
        require('site.notes-images.v3.css?v=3.1' in text, f"{relative}: static Notes imagery CSS missing")

nav = (ROOT / "assets/js/site.navigation.v1.js").read_text(encoding="utf-8")
for token in (
    "__ALINA_EDITORIAL_NAV_V1__",
    "setMenuOpen",
    "editorial-menu-open",
    "editorial-rail-placeholder",
    "setBackgroundInert",
    "consultations/#contact",
):
    require(token in nav, f"navigation runtime token missing: {token}")
require("appendStylesheet" not in nav and 'createElement("link")' not in nav, "navigation still injects CSS at runtime")

site = (ROOT / "assets/js/site.v2.js").read_text(encoding="utf-8")
for forbidden in (
    "initMobileNavigation",
    "initActiveNavigation",
    "initEditorialNotesImages",
    "ALINA_GLOBAL_CHROME_LOADER_V1",
    "site.global-chrome.v1.js",
):
    require(forbidden not in site, f"primary runtime still contains competing owner: {forbidden}")

css = (ROOT / "assets/css/site.global-chrome.v1.css").read_text(encoding="utf-8")
for token in (
    ".site-header--canonical", ".footer-editorial-grid", ".footer-navigation",
    ".footer-booking", ".footer-utility", "@media (max-width: 620px)",
    "@media (prefers-reduced-motion: reduce)",
):
    require(token in css, f"global chrome CSS token missing: {token}")

ua_articles = {path.parent.name for path in (ROOT / "notes").glob("*/index.html")}
ru_articles = {path.parent.name for path in (ROOT / "ru/notes").glob("*/index.html")}
require(ua_articles == ru_articles and len(ua_articles) == 4, "UA/RU article pairs are not mirrored")

print("Static global chrome and direct navigation validation passed.")
