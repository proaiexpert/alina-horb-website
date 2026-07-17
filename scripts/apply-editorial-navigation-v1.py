#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKER = "ALINA_EDITORIAL_NAV_LOADER_V1"
LOADER = r'''

  /* ALINA_EDITORIAL_NAV_LOADER_V1 */
  (() => {
    if (document.querySelector('script[data-editorial-navigation-v1]')) return;
    const projectMarker = "/alina-horb-website/";
    const rootPath = window.location.pathname.includes(projectMarker) ? projectMarker : "/";
    const navigationScript = document.createElement("script");
    navigationScript.src = `${rootPath}assets/js/site.navigation.v1.js?v=20260717-nav1`;
    navigationScript.defer = true;
    navigationScript.dataset.editorialNavigationV1 = "";
    document.head.appendChild(navigationScript);
  })();
'''

for relative in ("assets/js/site.v2.js", "assets/js/site.chrome.v3.js"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if MARKER not in text:
        index = text.rfind("})();")
        if index < 0:
            raise SystemExit(f"{relative}: closing IIFE not found")
        text = text[:index] + LOADER + text[index:]
        path.write_text(text, encoding="utf-8")

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")
    updated = re.sub(r'(site\.v2\.js)(?:\?[^"\']*)?', r'\1?v=20260717-nav1', text)
    updated = re.sub(r'(site\.chrome\.v3\.js)(?:\?[^"\']*)?', r'\1?v=20260717-nav1', updated)
    if updated != text:
        path.write_text(updated, encoding="utf-8")

print("Editorial navigation loader and cache-safe script references applied.")
