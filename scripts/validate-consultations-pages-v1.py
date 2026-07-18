#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "consultations/index.html": {
        "lang": "uk",
        "canonical": "https://alinahorb.com/consultations/",
        "ua": "https://alinahorb.com/consultations/",
        "ru": "https://alinahorb.com/ru/consultations/",
        "title": "Консультації психолога Аліни Горб",
    },
    "ru/consultations/index.html": {
        "lang": "ru",
        "canonical": "https://alinahorb.com/ru/consultations/",
        "ua": "https://alinahorb.com/consultations/",
        "ru": "https://alinahorb.com/ru/consultations/",
        "title": "Консультации психолога Алины Горб",
    },
}

errors = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


for relative, expected in PAGES.items():
    path = ROOT / relative
    require(path.is_file(), f"Missing page: {relative}")
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    require(f'<html lang="{expected["lang"]}"' in text, f"{relative}: language mismatch")
    require(text.count("<h1") == 1, f"{relative}: expected one H1")
    require(expected["title"] in text, f"{relative}: title copy missing")
    require(text.count(f'<link rel="canonical" href="{expected["canonical"]}">') == 1, f"{relative}: canonical mismatch")
    require(text.count(f'<link rel="alternate" hreflang="uk" href="{expected["ua"]}">') == 1, f"{relative}: UA hreflang mismatch")
    require(text.count(f'<link rel="alternate" hreflang="ru" href="{expected["ru"]}">') == 1, f"{relative}: RU hreflang mismatch")
    require(text.count('<meta name="robots" content="noindex, nofollow">') + text.count('<meta name="robots" content="index, follow, max-image-preview:large">') == 1, f"{relative}: indexing directive mismatch")
    require('"@type": "Service"' in text, f"{relative}: Service schema missing")
    require('"@type": "FAQPage"' in text, f"{relative}: FAQPage schema missing")
    require('"@type": "BreadcrumbList"' in text, f"{relative}: BreadcrumbList schema missing")
    require('priceCurrency": "UAH"' in text and '"price": "600"' in text, f"{relative}: price schema mismatch")
    require('data-contact-form' in text and 'data-form-status' in text and 'data-form-success' in text, f"{relative}: form or success state missing")
    require('name="service"' in text and 'name="message"' in text and 'name="availability"' in text, f"{relative}: compact consultation fields missing")
    require('name="language"' not in text and 'name="format"' not in text, f"{relative}: redundant intake fields remain")
    require(text.count('field-required') >= 3 and text.count('field-optional') >= 4, f"{relative}: required/optional labels missing")
    require('name="channel" required' not in text and 'name="service" required' not in text and 'name="timezone" required' not in text and 'name="availability" required' not in text, f"{relative}: optional field is still required")
    require('site-config.v2.js' in text and 'site.v2.js' in text, f"{relative}: form runtime missing")
    require('site.consultations.v1.css' in text, f"{relative}: page stylesheet missing")
    require('50' in text and '600' in text, f"{relative}: confirmed duration/price missing")
    require('financialstreamllc@gmail.com' not in text and 'alinahorb1991@gmail.com' not in text, f"{relative}: legacy email found")
    require(not re.search(r'\b(TODO|TBD)\b', text, re.I), f"{relative}: unfinished content token found")
    ids = re.findall(r'\bid="([^"]+)"', text)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    require(not duplicates, f"{relative}: duplicate IDs {duplicates}")
    for script in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S):
        try:
            json.loads(script)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON-LD: {exc}")

css = ROOT / "assets/css/site.consultations.v1.css"
require(css.is_file(), "Consultations stylesheet missing")
if css.is_file():
    content = css.read_text(encoding="utf-8")
    for token in (".consult-hero", ".condition-ledger", ".consult-faq", "@media (max-width: 620px)"):
        require(token in content, f"Consultations stylesheet missing {token}")

if errors:
    print("Consultations pages validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Consultations pages validation passed for compact UA and RU intake forms")
