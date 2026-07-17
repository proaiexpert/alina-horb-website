#!/usr/bin/env python3
# Production gate for every canonical UA/RU header and footer template.
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


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


def page_context(path: Path) -> tuple[bool, str, str, str]:
    relative = path.relative_to(ROOT)
    parent_parts = relative.parent.parts
    depth = len(parent_parts)
    root_prefix = "../" * depth
    is_ru = bool(parent_parts and parent_parts[0] == "ru")
    clean_parts = parent_parts[1:] if is_ru else parent_parts
    clean_route = "/".join(clean_parts)
    if clean_route:
        clean_route += "/"
    locale_home = (("../" * max(depth - 1, 0)) or "./") if is_ru else (root_prefix or "./")
    alternate = f"{root_prefix}{clean_route}" if is_ru else f"{root_prefix}ru/{clean_route}"
    if not alternate:
        alternate = "./"
    return is_ru, root_prefix, locale_home, alternate


for path in production_pages():
    relative = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    is_ru, root_prefix, locale_home, alternate = page_context(path)
    asset_prefix = f"{root_prefix}assets/"

    require(text.count('<header class="site-header') == 1, f"{relative}: canonical header count is not one")
    require('site-header--canonical' in text, f"{relative}: canonical header class missing")
    require('data-menu-toggle' in text and 'data-mobile-nav' in text, f"{relative}: canonical mobile header controls missing")
    require(text.count('<footer class="site-footer"') == 1, f"{relative}: canonical footer count is not one")
    require('data-site-footer="canonical"' in text, f"{relative}: canonical footer marker missing")

    for token in (
        'footer-editorial-grid',
        'footer-identity',
        'footer-navigation',
        'footer-contact',
        'footer-booking',
        'footer-utility',
        'maker-credit',
    ):
        require(token in text, f"{relative}: footer token missing: {token}")

    require('footer-row' not in text, f"{relative}: legacy footer-row remains")
    require('class="footer-main"' not in text, f"{relative}: legacy footer-main remains")
    require('class="footer-bottom"' not in text, f"{relative}: legacy footer-bottom remains")
    require('site.footer.v3-2.css' not in text, f"{relative}: legacy footer stylesheet remains")

    global_css = f'{asset_prefix}css/site.global-chrome.v1.css?v=20260717-chrome1'
    require(text.count(global_css) == 1, f"{relative}: global chrome stylesheet missing or duplicated")
    require('site.v2.js?v=20260717-chrome1' in text or 'site.chrome.v3.js?v=20260717-chrome1' in text, f"{relative}: cache-safe runtime version missing")
    require(f'href="{locale_home}consultations/#contact"' in text, f"{relative}: canonical booking route missing")
    require(f'href="{alternate}"' in text, f"{relative}: mirrored language route missing")

    if is_ru:
        require('Об Алине' in text and 'Консультации' in text and 'Заметки' in text, f"{relative}: RU global navigation labels missing")
        require('Психологические консультации на русском и украинском языках' in text, f"{relative}: RU footer positioning missing")
    else:
        require('Про Аліну' in text and 'Консультації' in text and 'Нотатки' in text, f"{relative}: UA global navigation labels missing")
        require('Психологічні консультації українською та російською мовами' in text, f"{relative}: UA footer positioning missing")


global_js = (ROOT / "assets/js/site.global-chrome.v1.js").read_text(encoding="utf-8")
for token in (
    "__ALINA_GLOBAL_CHROME_V1__",
    "site.global-chrome.v1.css?v=20260717-chrome1",
    "footer.dataset.siteFooter = \"canonical\"",
    "footer-editorial-grid",
    "footer-booking",
    "data-menu-toggle",
    "site.navigation.v1.js?v=20260717-chrome1",
):
    require(token in global_js, f"global chrome runtime token missing: {token}")

site_js = (ROOT / "assets/js/site.v2.js").read_text(encoding="utf-8")
require("ALINA_GLOBAL_CHROME_LOADER_V1" in site_js, "site.v2 global chrome loader marker missing")
require("site.global-chrome.v1.js?v=20260717-chrome1" in site_js, "site.v2 global chrome source missing")
require("site.navigation.v1.js?v=20260717-nav1" not in site_js, "site.v2 legacy navigation loader remains")

chrome_js = (ROOT / "assets/js/site.chrome.v3.js").read_text(encoding="utf-8")
require("site.global-chrome.v1.js?v=20260717-chrome1" in chrome_js, "utility chrome global loader missing")
require("footer.innerHTML" not in chrome_js, "utility chrome still owns footer rendering")
require("header.innerHTML" not in chrome_js, "utility chrome still owns header rendering")
require("site.footer.v3-2.css" not in chrome_js, "utility chrome still loads legacy footer CSS")

css = (ROOT / "assets/css/site.global-chrome.v1.css").read_text(encoding="utf-8")
for token in (
    ".site-header--canonical",
    ".footer-editorial-grid",
    ".footer-navigation",
    ".footer-booking",
    ".footer-utility",
    "@media (max-width: 620px)",
    "@media (prefers-reduced-motion: reduce)",
):
    require(token in css, f"global chrome CSS token missing: {token}")

ua_articles = {path.parent.name for path in (ROOT / "notes").glob("*/index.html")}
ru_articles = {path.parent.name for path in (ROOT / "ru/notes").glob("*/index.html")}
require(ua_articles == ru_articles and len(ua_articles) == 4, "UA/RU article pairs are not mirrored")

print("Global chrome V1 validation passed.")
