#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

pages = {
    ROOT / "index.html": {
        "favicon": '  <link rel="icon" type="image/svg+xml" href="assets/images/logos/favicon-ag.svg">',
        "v2": "alina-horb-og-ua-v2.jpg",
        "v1": "alina-horb-og-ua-v1.jpg",
    },
    ROOT / "ru/index.html": {
        "favicon": '  <link rel="icon" type="image/svg+xml" href="../assets/images/logos/favicon-ag.svg">',
        "v2": "alina-horb-og-ru-v2.jpg",
        "v1": "alina-horb-og-ru-v1.jpg",
    },
}

for path, cfg in pages.items():
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'^\s*<link rel="icon" href="/favicon\.ico" sizes="any">\n', '', text, flags=re.M)
    text = re.sub(r'^\s*<link rel="icon" type="image/svg\+xml" href="/assets/images/logos/favicon-ag\.svg">\n', '', text, flags=re.M)
    text = re.sub(r'^\s*<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32\.png">\n', '', text, flags=re.M)
    text = re.sub(r'^\s*<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16\.png">\n', '', text, flags=re.M)
    text = re.sub(r'^\s*<link rel="shortcut icon" href="/favicon\.ico">\n', '', text, flags=re.M)
    text = re.sub(r'^\s*<meta name="theme-color" content="#f5f0e8">\n', '', text, flags=re.M)
    text = text.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, nofollow">')
    text = text.replace(cfg["v2"], cfg["v1"])
    text = re.sub(r'^\s*<meta property="og:image:url"[^>]*>\n', '', text, flags=re.M)
    text = re.sub(r'^\s*<link rel="image_src"[^>]*>\n', '', text, flags=re.M)
    text = re.sub(r'^<link rel="preconnect" href="https://fonts\.googleapis\.com">', '  <link rel="preconnect" href="https://fonts.googleapis.com">', text, flags=re.M)
    marker = '  <link rel="preconnect" href="https://fonts.googleapis.com">'
    if cfg["favicon"] not in text:
        if marker not in text:
            raise SystemExit(f"Google Fonts preconnect marker missing in {path.relative_to(ROOT)}")
        text = text.replace(marker, cfg["favicon"] + "\n" + marker, 1)
    path.write_text(text, encoding="utf-8")

for path, cfg in pages.items():
    text = path.read_text(encoding="utf-8")
    assert '<meta name="robots" content="noindex, nofollow">' in text
    assert cfg["v1"] in text and cfg["v2"] not in text
    assert cfg["favicon"] in text
    assert '/favicon.ico' not in text
    assert 'og:image:url' not in text
    assert 'rel="image_src"' not in text

print("Homepage source metadata normalized; bilingual quote preserved")
