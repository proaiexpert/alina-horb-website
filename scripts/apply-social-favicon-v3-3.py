#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

ROUTES = [
    "index.html",
    "ru/index.html",
    "notes/index.html",
    "ru/notes/index.html",
    "notes/first-consultation/index.html",
    "ru/notes/first-consultation/index.html",
    "notes/how-to-start-the-conversation/index.html",
    "ru/notes/how-to-start-the-conversation/index.html",
    "notes/when-coping-stops-helping/index.html",
    "ru/notes/when-coping-stops-helping/index.html",
    "notes/stress-relocation-and-lost-support/index.html",
    "ru/notes/stress-relocation-and-lost-support/index.html",
    "privacy/index.html",
    "ru/privacy/index.html",
]

ICON_BLOCK = """  <link rel=\"icon\" href=\"/favicon.ico\" sizes=\"any\">\n  <link rel=\"icon\" type=\"image/svg+xml\" href=\"/assets/images/logos/favicon-ag.svg\">\n  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/favicon-32x32.png\">\n  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/favicon-16x16.png\">\n  <link rel=\"shortcut icon\" href=\"/favicon.ico\">\n  <meta name=\"theme-color\" content=\"#f5f0e8\">"""

SOCIAL = {
    "index.html": (
        "https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg",
        "https://alinahorb.com/assets/images/social/alina-horb-og-ua-v2.jpg",
    ),
    "ru/index.html": (
        "https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg",
        "https://alinahorb.com/assets/images/social/alina-horb-og-ru-v2.jpg",
    ),
}

for relative in ROUTES:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Missing public route: {relative}")
    text = path.read_text(encoding="utf-8")

    # Normalize all favicon declarations to absolute, crawler-safe URLs.
    text = re.sub(r"\n?\s*<link\s+rel=\"(?:shortcut\s+)?icon\"[^>]*>\s*", "\n", text, flags=re.I)
    text = re.sub(r"\n?\s*<meta\s+name=\"theme-color\"[^>]*>\s*", "\n", text, flags=re.I)
    viewport = re.search(r'(^\s*<meta\s+name="viewport"[^>]*>\s*$)', text, flags=re.I | re.M)
    if not viewport:
        raise SystemExit(f"Viewport marker missing in {relative}")
    text = text[: viewport.end()] + "\n" + ICON_BLOCK + text[viewport.end():]

    if relative in SOCIAL:
        old, new = SOCIAL[relative]
        text = text.replace(old, new)
        og_image = f'  <meta property="og:image" content="{new}">'
        og_url = f'  <meta property="og:image:url" content="{new}">'
        if og_image not in text:
            raise SystemExit(f"Localized og:image missing in {relative}")
        if og_url not in text:
            text = text.replace(og_image, og_image + "\n" + og_url, 1)
        image_src = f'  <link rel="image_src" href="{new}">'
        if image_src not in text:
            twitter_marker = f'  <meta name="twitter:image" content="{new}">'
            if twitter_marker not in text:
                raise SystemExit(f"Localized twitter:image missing in {relative}")
            text = text.replace(twitter_marker, twitter_marker + "\n" + image_src, 1)

    path.write_text(text, encoding="utf-8")

print(f"Social preview cache version and favicon fallbacks applied to {len(ROUTES)} routes")
