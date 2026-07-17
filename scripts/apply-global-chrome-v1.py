#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CHANGED: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write_if_changed(path: Path, revised: str) -> None:
    current = path.read_text(encoding="utf-8")
    if revised == current:
        return
    path.write_text(revised, encoding="utf-8")
    CHANGED.append(path.relative_to(ROOT).as_posix())


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


def context(path: Path) -> dict[str, str | bool]:
    relative = path.relative_to(ROOT)
    parent_parts = relative.parent.parts
    root_prefix = "../" * len(parent_parts)
    is_ru = bool(parent_parts and parent_parts[0] == "ru")
    clean_parts = parent_parts[1:] if is_ru else parent_parts
    clean_route = "/".join(clean_parts)
    if clean_route:
        clean_route += "/"
    locale_home = f"{root_prefix}{'ru/' if is_ru else ''}" or "./"
    alternate = f"{root_prefix}{clean_route}" if is_ru else f"{root_prefix}ru/{clean_route}"
    if not alternate:
        alternate = "./"
    page_key = "home" if not clean_route else (
        "about" if clean_route.startswith("about/") else
        "consultations" if clean_route.startswith("consultations/") else
        "notes" if clean_route.startswith("notes/") else
        "privacy" if clean_route.startswith("privacy/") else
        "other"
    )
    return {
        "root_prefix": root_prefix,
        "asset_prefix": f"{root_prefix}assets/",
        "is_ru": is_ru,
        "clean_route": clean_route,
        "locale_home": locale_home,
        "alternate": alternate,
        "page_key": page_key,
    }


def current_attr(key: str, page_key: str) -> str:
    return ' aria-current="page"' if key == page_key else ""


def language_switch(is_ru: bool, alternate: str) -> str:
    if is_ru:
        return f'<div class="language-switch" aria-label="Выбор языка"><a href="{alternate}" lang="uk" hreflang="uk">UA</a><span aria-hidden="true">/</span><span aria-current="page">RU</span></div>'
    return f'<div class="language-switch" aria-label="Вибір мови"><span aria-current="page">UA</span><span aria-hidden="true">/</span><a href="{alternate}" lang="ru" hreflang="ru">RU</a></div>'


def header_markup(data: dict[str, str | bool]) -> str:
    is_ru = bool(data["is_ru"])
    page_key = str(data["page_key"])
    locale_home = str(data["locale_home"])
    asset_prefix = str(data["asset_prefix"])
    alternate = str(data["alternate"])
    name = "Алина Горб" if is_ru else "Аліна Горб"
    brand = "Алина Горб — главная" if is_ru else "Аліна Горб — головна"
    nav_label = "Основные разделы сайта" if is_ru else "Основні розділи сайту"
    open_label = "Открыть меню" if is_ru else "Відкрити меню"
    pages = [
        ("about", "Об Алине" if is_ru else "Про Аліну", f"{locale_home}about/"),
        ("consultations", "Консультации" if is_ru else "Консультації", f"{locale_home}consultations/"),
        ("notes", "Заметки" if is_ru else "Нотатки", f"{locale_home}notes/"),
    ]
    sticky = page_key in {"notes", "privacy", "other"}
    classes = "site-header site-header--canonical" + (" inner-page-header" if sticky else "")
    switch = language_switch(is_ru, alternate)
    desktop = "".join(
        f'<a href="{href}"{current_attr(key, page_key)}>{label}</a>' for key, label, href in pages
    )
    booking_short = "Записаться" if is_ru else "Записатися"
    return f'''<header class="{classes}" id="top">
    <div class="page-shell header-row">
      <a class="brand" href="{locale_home}" aria-label="{brand}"><img src="{asset_prefix}images/logos/alina-horb-logo-{'ru' if is_ru else 'ua'}-dark.png" width="512" height="156" alt="{name}"></a>
      <nav class="inner-desktop-nav" aria-label="{nav_label}">{desktop}<a class="editorial-header-booking" href="{locale_home}consultations/#contact">{booking_short}</a></nav>
      <div class="header-tools">{switch}<button class="mobile-nav-toggle" type="button" aria-label="{open_label}" aria-expanded="false" aria-controls="mobile-navigation" data-menu-toggle><span class="menu-icon" aria-hidden="true"></span></button></div>
      <nav class="mobile-navigation" id="mobile-navigation" aria-label="{nav_label}" data-mobile-nav hidden></nav>
    </div>
  </header>'''


def footer_markup(data: dict[str, str | bool]) -> str:
    is_ru = bool(data["is_ru"])
    page_key = str(data["page_key"])
    locale_home = str(data["locale_home"])
    asset_prefix = str(data["asset_prefix"])
    alternate = str(data["alternate"])
    name = "Алина Горб" if is_ru else "Аліна Горб"
    brand = "Алина Горб — главная" if is_ru else "Аліна Горб — головна"
    nav_label = "Основные разделы сайта" if is_ru else "Основні розділи сайту"
    sections = "Разделы" if is_ru else "Розділи"
    contact = "Первый контакт" if is_ru else "Перший контакт"
    positioning = "Психологические консультации на русском и украинском языках · онлайн." if is_ru else "Психологічні консультації українською та російською мовами · онлайн."
    booking = "Записаться на консультацию" if is_ru else "Записатися на консультацію"
    privacy = "Конфиденциальность" if is_ru else "Конфіденційність"
    language = "Язык" if is_ru else "Мова"
    developed = "Разработано" if is_ru else "Розроблено"
    copyright_text = "© Алина Горб, 2026" if is_ru else "© Аліна Горб, 2026"
    pages = [
        ("home", "Главная" if is_ru else "Головна", locale_home),
        ("about", "Об Алине" if is_ru else "Про Аліну", f"{locale_home}about/"),
        ("consultations", "Консультации" if is_ru else "Консультації", f"{locale_home}consultations/"),
        ("notes", "Заметки" if is_ru else "Нотатки", f"{locale_home}notes/"),
    ]
    nav_links = "".join(
        f'<a href="{href}"{current_attr(key, page_key)}>{label}</a>' for key, label, href in pages
    )
    switch = language_switch(is_ru, alternate)
    privacy_current = ' aria-current="page"' if page_key == "privacy" else ""
    return f'''<footer class="site-footer" data-site-footer="canonical">
    <div class="page-shell footer-editorial-grid">
      <div class="footer-identity"><a class="footer-brand" href="{locale_home}" aria-label="{brand}"><img src="{asset_prefix}images/logos/alina-horb-logo-{'ru' if is_ru else 'ua'}-dark.png" width="512" height="156" alt="{name}"></a><p>{positioning}</p></div>
      <nav class="footer-navigation" aria-label="{nav_label}"><p class="footer-label">{sections}</p>{nav_links}</nav>
      <div class="footer-contact"><p class="footer-label">{contact}</p><a class="footer-booking" href="{locale_home}consultations/#contact"><span>{booking}</span><span aria-hidden="true">→</span></a><div class="footer-contact-links"><a href="mailto:hello@alinahorb.com">Email</a><a href="https://t.me/alina_horb1991" target="_blank" rel="noopener noreferrer">Telegram</a><a href="https://instagram.com/ng_alina_dp" target="_blank" rel="noopener noreferrer">Instagram</a></div></div>
    </div>
    <div class="page-shell footer-utility"><div class="footer-utility-links"><a href="{locale_home}">alinahorb.com</a><a href="{locale_home}privacy/"{privacy_current}>{privacy}</a><span class="footer-language-label">{language}</span>{switch}</div><div class="footer-legal"><span>{copyright_text}</span><span class="maker-credit"><small>{developed}</small><a href="https://proai-expert.com/" target="_blank" rel="noopener noreferrer">ProAI Expert</a></span></div></div>
  </footer>'''


header_pattern = re.compile(r'<header\b[^>]*class="[^"]*\bsite-header\b[^"]*"[^>]*>.*?</header>', re.DOTALL)
footer_pattern = re.compile(r'<footer\b[^>]*class="[^"]*\bsite-footer\b[^"]*"[^>]*>.*?</footer>', re.DOTALL)

for path in production_pages():
    text = path.read_text(encoding="utf-8")
    data = context(path)
    relative = path.relative_to(ROOT).as_posix()

    text, header_count = header_pattern.subn(header_markup(data), text, count=1)
    require(header_count == 1, f"{relative}: expected one site header to replace")
    text, footer_count = footer_pattern.subn(footer_markup(data), text, count=1)
    require(footer_count == 1, f"{relative}: expected one site footer to replace")

    text = re.sub(r'\s*<link rel="stylesheet" href="[^"]*site\.footer\.v3-2\.css">\s*', "\n", text)
    text = re.sub(r'\s*<link rel="stylesheet" href="[^"]*site\.global-chrome\.v1\.css(?:\?v=[^"]*)?">\s*', "\n", text)
    global_link = f'  <link rel="stylesheet" href="{data["asset_prefix"]}css/site.global-chrome.v1.css?v=20260717-chrome1">\n'
    script_index = text.find("  <script")
    require(script_index >= 0, f"{relative}: no script tag available for global CSS insertion")
    text = text[:script_index] + global_link + text[script_index:]

    text = re.sub(r'(site\.v2\.js)(?:\?v=[^"]*)?', r'\1?v=20260717-chrome1', text)
    text = re.sub(r'(site\.chrome\.v3\.js)(?:\?v=[^"]*)?', r'\1?v=20260717-chrome1', text)
    text = re.sub(r'\n{3,}', "\n\n", text)
    write_if_changed(path, text)

site_js_path = ROOT / "assets/js/site.v2.js"
site_js = site_js_path.read_text(encoding="utf-8")
site_js = site_js.replace("/* ALINA_EDITORIAL_NAV_LOADER_V1 */", "/* ALINA_GLOBAL_CHROME_LOADER_V1 */")
site_js = site_js.replace("data-editorial-navigation-v1", "data-global-chrome-v1")
site_js = site_js.replace("navigationScript", "globalChrome")
site_js = site_js.replace("site.navigation.v1.js?v=20260717-nav1", "site.global-chrome.v1.js?v=20260717-chrome1")
site_js = site_js.replace("dataset.editorialNavigationV1", "dataset.globalChromeV1")
require("ALINA_GLOBAL_CHROME_LOADER_V1" in site_js, "site.v2 global chrome loader was not installed")
require("site.global-chrome.v1.js?v=20260717-chrome1" in site_js, "site.v2 global chrome source was not installed")
write_if_changed(site_js_path, site_js)

print("Global chrome V1 migration applied:")
for relative in CHANGED:
    print(f"- {relative}")
