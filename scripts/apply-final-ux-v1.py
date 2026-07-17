#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260717-ux1"

FIXED = [
    Path("index.html"),
    Path("ru/index.html"),
    Path("about/index.html"),
    Path("ru/about/index.html"),
    Path("consultations/index.html"),
    Path("ru/consultations/index.html"),
    Path("privacy/index.html"),
    Path("ru/privacy/index.html"),
    Path("notes/index.html"),
    Path("ru/notes/index.html"),
]
ARTICLES = sorted(Path("notes").glob("*/index.html")) + sorted(Path("ru/notes").glob("*/index.html"))
PAGES = FIXED + ARTICLES


def asset_prefix(relative: Path) -> str:
    return "../" * len(relative.parent.parts) + "assets/"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing {label}: {old}")
    return text.replace(old, new, 1)


def insert_after(text: str, marker: str, insertion: str, label: str) -> str:
    if insertion.strip() in text:
        return text
    if marker not in text:
        raise SystemExit(f"Missing insertion marker for {label}: {marker}")
    return text.replace(marker, marker + insertion, 1)


def normalize_page(relative: Path) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    prefix = asset_prefix(relative)

    text = re.sub(
        rf'{re.escape(prefix)}css/site\.global-chrome\.v1\.css\?v=[^"\s]+',
        f'{prefix}css/site.global-chrome.v1.css?v={VERSION}',
        text,
        count=1,
    )
    global_css = f'<link rel="stylesheet" href="{prefix}css/site.global-chrome.v1.css?v={VERSION}">'
    if global_css not in text:
        raise SystemExit(f"{relative}: global chrome stylesheet normalization failed")

    nav_css = f'  <link rel="stylesheet" href="{prefix}css/site.navigation.v1.css?v={VERSION}">\n'
    text = insert_after(text, global_css, "\n" + nav_css.rstrip("\n"), f"navigation CSS in {relative}")

    text = re.sub(
        rf'{re.escape(prefix)}js/site\.v2\.js\?v=[^"\s]+',
        f'{prefix}js/site.v2.js?v={VERSION}',
        text,
        count=1,
    )

    text = re.sub(
        rf'\s*<script\s+src="{re.escape(prefix)}js/site\.chrome\.v3\.js[^\"]*"\s+defer></script>',
        "",
        text,
    )
    text = re.sub(
        rf'\s*<script\s+src="{re.escape(prefix)}js/site\.notes-images\.v3-1\.js[^\"]*"\s+defer></script>',
        "",
        text,
    )

    nav_js = f'  <script src="{prefix}js/site.navigation.v1.js?v={VERSION}" defer></script>\n'
    if nav_js.strip() not in text:
        text = text.replace("</head>", nav_js + "</head>", 1)

    favicon = f'  <link rel="icon" type="image/svg+xml" href="{prefix}images/logos/favicon-ag.svg">'
    text, count = re.subn(r'\s*<link\s+rel="icon"[^>]*>', "\n" + favicon, text, count=1)
    if count != 1:
        raise SystemExit(f"{relative}: favicon could not be normalized")

    is_hub = relative in {Path("notes/index.html"), Path("ru/notes/index.html")}
    is_article = relative in ARTICLES
    if is_hub:
        text = text.replace('class="page-shell notes-hub-hero-grid"', 'class="page-shell notes-hub-hero-grid has-editorial-rail"', 1)
        host = '<div class="page-shell notes-hub-hero-grid has-editorial-rail">'
        placeholder = '\n        <nav class="side-navigation editorial-rail editorial-rail-placeholder" aria-hidden="true"></nav>'
        if placeholder.strip() not in text:
            text = replace_once(text, host, host + placeholder, f"Notes rail placeholder in {relative}")
    elif is_article:
        text = text.replace('class="page-shell article-hero-grid"', 'class="page-shell article-hero-grid has-editorial-rail"', 1)
        host = '<div class="page-shell article-hero-grid has-editorial-rail">'
        placeholder = '\n        <nav class="side-navigation editorial-rail editorial-rail-placeholder" aria-hidden="true"></nav>'
        if placeholder.strip() not in text:
            text = replace_once(text, host, host + placeholder, f"article rail placeholder in {relative}")

    path.write_text(text, encoding="utf-8")


for page in PAGES:
    if not (ROOT / page).is_file():
        raise SystemExit(f"Missing production page: {page}")
    normalize_page(page)

# Navigation owns the responsive menu and is loaded directly with its stylesheet.
nav_path = ROOT / "assets/js/site.navigation.v1.js"
nav = nav_path.read_text(encoding="utf-8")
nav = re.sub(
    r'\n\s*const script = document\.currentScript;\n\s*if \(!script\) return;\n\n\s*const stylesheetHref = .*?document\.head\.appendChild\(link\);\n\s*}\n',
    "\n",
    nav,
    count=1,
    flags=re.S,
)
nav = nav.replace(
    '    if (existingRail) {\n      source = [...existingRail.querySelectorAll(\'a[href^="#"]\')].map((link) => ({\n        href: link.getAttribute("href"),\n        label: link.querySelector("span")?.textContent?.trim() || link.textContent.trim()\n      }));\n    } else if (isNotesHub) {',
    '    if (existingRail) {\n      source = [...existingRail.querySelectorAll(\'a[href^="#"]\')].map((link) => ({\n        href: link.getAttribute("href"),\n        label: link.querySelector("span")?.textContent?.trim() || link.textContent.trim()\n      }));\n    }\n    if (!source.length && isNotesHub) {',
)
nav = nav.replace('    } else if (isArticle) {', '    } else if (!source.length && isArticle) {', 1)
nav = nav.replace(
    '    rail.classList.add("editorial-rail");\n    rail.setAttribute("aria-label", text.nav);',
    '    rail.classList.add("editorial-rail");\n    rail.classList.remove("editorial-rail-placeholder");\n    rail.removeAttribute("aria-hidden");\n    rail.setAttribute("aria-label", text.nav);',
    1,
)
nav = nav.replace(
    '  const inertTargets = [...document.querySelectorAll("main, .site-footer, [data-mobile-booking-cta]")];',
    '  const inertTargets = [...document.body.children].filter((element) => element !== header && !["SCRIPT", "STYLE", "LINK"].includes(element.tagName));',
    1,
)
old_close = '''  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!mobileToggle || !mobileMenu) return;
    mobileMenu.hidden = true;
    mobileToggle.setAttribute("aria-expanded", "false");
    syncMenuState();
    if (restoreFocus) mobileToggle.focus({ preventScroll: true });
  };

  if (mobileToggle && mobileMenu) {
    new MutationObserver(() => syncMenuState()).observe(mobileToggle, {
      attributes: true,
      attributeFilter: ["aria-expanded"]
    });
    new MutationObserver(() => syncMenuState()).observe(mobileMenu, {
      attributes: true,
      attributeFilter: ["hidden"]
    });
    syncMenuState();
  }
'''
new_close = '''  const setMenuOpen = (open, { restoreFocus = false, focusFirst = false } = {}) => {
    if (!mobileToggle || !mobileMenu) return;
    mobileMenu.hidden = !open;
    mobileToggle.setAttribute("aria-expanded", String(open));
    syncMenuState({ focusFirst });
    if (!open && restoreFocus) mobileToggle.focus({ preventScroll: true });
  };

  const closeMenu = ({ restoreFocus = false } = {}) => setMenuOpen(false, { restoreFocus });

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener("click", () => {
      const open = mobileToggle.getAttribute("aria-expanded") === "true" && !mobileMenu.hidden;
      setMenuOpen(!open, { focusFirst: !open });
    });
    syncMenuState();
  }
'''
if old_close not in nav:
    raise SystemExit("Navigation menu ownership block changed unexpectedly")
nav = nav.replace(old_close, new_close, 1)
nav_path.write_text(nav, encoding="utf-8")

# The primary runtime no longer competes for mobile menu or rail state and no longer swaps Notes imagery.
site_path = ROOT / "assets/js/site.v2.js"
site = site_path.read_text(encoding="utf-8")
site = re.sub(r'\n\s*const initMobileNavigation = \(\) => \{.*?\n\s*};\n', "\n", site, count=1, flags=re.S)
site = re.sub(r'\n\s*const initActiveNavigation = \(\) => \{.*?\n\s*};\n', "\n", site, count=1, flags=re.S)
site = re.sub(r'\n\s*const initEditorialNotesImages = \(\) => \{.*?\n\s*};\n', "\n", site, count=1, flags=re.S)
site = site.replace("    initMobileNavigation();\n", "")
site = site.replace("    initEditorialNotesImages();\n", "")
site = site.replace("    initActiveNavigation();\n", "")
site = re.sub(r'\n\n\s*/\* ALINA_GLOBAL_CHROME_LOADER_V1 \*/.*?\n\s*}\)\(\);\n(?=\}\)\(\);)', "\n", site, count=1, flags=re.S)
site_path.write_text(site, encoding="utf-8")

# Static Notes markup is now the source of truth; deployment must not re-inject a runtime.
notes_apply_path = ROOT / "scripts/apply-notes-images-v3-1.py"
notes_apply = notes_apply_path.read_text(encoding="utf-8")
notes_apply = notes_apply.replace('    js_src = f\'{asset_prefix}js/site.notes-images.v3-1.js\'\n', "")
notes_apply = re.sub(r'\n\s*if js_src not in text:\n\s*text = text\.replace\("</body>", f\'.*?</body>\', 1\)', "", notes_apply, count=1, flags=re.S)
notes_apply_path.write_text(notes_apply, encoding="utf-8")

# Legacy utility runtime remains syntax-compatible for historical tooling but performs no DOM mutation.
(ROOT / "assets/js/site.chrome.v3.js").write_text(
    '(() => {\n  "use strict";\n  window.__ALINA_STATIC_UTILITY_CHROME_V1__ = true;\n})();\n',
    encoding="utf-8",
)

# Placeholder occupies the final rail geometry before deferred enhancement.
nav_css_path = ROOT / "assets/css/site.navigation.v1.css"
nav_css = nav_css_path.read_text(encoding="utf-8")
placeholder_css = '''\n.editorial-rail-placeholder {\n  visibility: hidden;\n  pointer-events: none;\n}\n'''
if ".editorial-rail-placeholder" not in nav_css:
    nav_css = nav_css.replace(".editorial-rail {", placeholder_css + "\n.editorial-rail {", 1)
nav_css_path.write_text(nav_css, encoding="utf-8")

print(f"Final UX V1 production migration applied to {len(PAGES)} pages")
