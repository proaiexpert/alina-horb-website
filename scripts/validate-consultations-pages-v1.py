#!/usr/bin/env python3
from pathlib import Path
import json
import re
from html.parser import HTMLParser

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


# HTMLParser handles case-insensitive HTML tag/attribute names and flexible quoting.
PUBLIC_ROBOTS = "index, follow, max-image-preview:large"
ROBOT_META_NAMES = {"robots", "googlebot", "googlebot-news"}


class RobotsMetaParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.robots_tags = []

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        names = [value for key, value in attrs if key == "name"]
        if any((value or "").strip().casefold() in ROBOT_META_NAMES for value in names):
            contents = [value for key, value in attrs if key == "content"]
            self.robots_tags.append(
                (contents[0] or "").strip()
                if len(names) == 1 and len(contents) == 1
                and (names[0] or "").strip().casefold() == "robots"
                else None
            )


def has_exact_public_robots(html: str) -> bool:
    parser = RobotsMetaParser()
    parser.feed(html)
    parser.close()
    return parser.robots_tags == [PUBLIC_ROBOTS]


# Match the standalone 600 грн price with Unicode spaces, excluding grouped thousands.
LEGACY_600_UAH = re.compile(r'\b600[ \u00A0\u202F]+грн\b')
THOUSANDS_PREFIX = re.compile(r'\d[ \u00A0\u202F]+$')
OBSOLETE_270_EUR = re.compile(r'(?<!\d)270\s*€')


def has_standalone_600_uah(text: str) -> bool:
    return any(
        not THOUSANDS_PREFIX.search(text[:match.start()])
        for match in LEGACY_600_UAH.finditer(text)
    )


approved = '<meta name="robots" content="index, follow, max-image-preview:large">'
for label, sample, expected_result in (
    ("approved", approved, True),
    ("approved alternate HTML spelling", "<META CONTENT='index, follow, max-image-preview:large' NAME='ROBOTS'>", True),
    ("approved padded name whitespace", '<MeTa NAME = " robots " CONTENT = "index, follow, max-image-preview:large">', True),
    ("unrelated description and viewport", '<meta name="description" content="Example"><meta name="viewport" content="width=device-width">' + approved, True),
    ("unrelated alternate meta", approved + '<meta property="og:title" content="Test"><meta name="theme-color" content="#fff">', True),
    ("missing", '<meta name="description" content="example">', False),
    ("legacy noindex", '<meta name="robots" content="noindex, nofollow">', False),
    ("extra nofollow", approved + '<meta name="robots" content="nofollow">', False),
    ("extra noindex", approved + '<meta name="robots" content="noindex">', False),
    ("duplicate approved", approved + approved, False),
    ("reordered conflict", approved + '<meta content="nofollow" name="robots">', False),
    ("single-quoted uppercase conflict", approved + "<META CONTENT='noindex, nofollow' NAME='ROBOTS'>", False),
    ("duplicate name attribute", '<meta name="robots" name="description" content="index, follow, max-image-preview:large">', False),
    ("only nofollow", '<meta name="robots" content="nofollow">', False),
    ("duplicate content attribute", '<meta name="robots" content="index, follow, max-image-preview:large" content="noindex">', False),
    ("missing content", '<meta name="robots">', False),
    ("googlebot none", approved + '<meta name="googlebot" content="none">', False),
    ("googlebot noindex", approved + '<meta name="googlebot" content="noindex">', False),
    ("googlebot nofollow", approved + '<meta name="googlebot" content="nofollow">', False),
    ("googlebot-news noindex", approved + '<meta name="googlebot-news" content="noindex">', False),
    ("googlebot-news none", approved + '<meta name="googlebot-news" content="none">', False),
    ("googlebot harmless all", approved + '<meta name="googlebot" content="all">', False),
    ("googlebot-news harmless all", approved + '<meta name="googlebot-news" content="all">', False),
    ("uppercase crawler", approved + "<META CONTENT='none' NAME='GOOGLEBOT'>", False),
    ("reordered crawler", approved + '<meta content="noindex" name="googlebot-news">', False),
    ("padded crawler", approved + '<meta NAME = " googlebot-news " CONTENT = " all ">', False),
    ("unquoted crawler attributes", approved + '<meta name=googlebot content=noindex>', False),
    ("crawler in body", '<head>' + approved + '</head><body><meta name="googlebot" content="none"></body>', False),
    ("duplicate crawler name", approved + '<meta name="googlebot" name="description" content="none">', False),
    ("duplicate crawler content", approved + '<meta name="googlebot-news" content="all" content="none">', False),
):
    require(has_exact_public_robots(sample) == expected_result,
            f"Robots-meta regression: {label}")

for sample, expected_match in (
    ("600 грн", True),
    ("Ціна: 600 грн.", True),
    ("600\u00a0грн", True),
    ("600\u202fгрн", True),
    ("1 600 грн", False),
    ("1\u00a0600 грн", False),
    ("1\u202f600 грн", False),
    ("1  600 грн", False),
    ("1\u202f600\u202fгрн", False),
    ("1 600 грн; 600 грн", True),
    ("1\u00a0600\u202fгрн; 600\u202fгрн", True),
):
    require(has_standalone_600_uah(sample) == expected_match,
            f"Standalone legacy price matcher regression: {sample!r}")

for sample, expected_match in (
    ("270 €", True),
    ("240 € and 270 €", True),
    ("270\u00a0€", True),
    ("270\u202f€", True),
    ("240 €", False),
    ("35 €", False),
):
    require(bool(OBSOLETE_270_EUR.search(sample)) == expected_match,
            f"Obsolete 270 EUR matcher regression: {sample!r}")


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
    require(has_exact_public_robots(text), f"{relative}: public robots-meta must occur exactly once with approved indexing policy")
    require('"@type": "Service"' in text, f"{relative}: Service schema missing")
    require('"@type": "Person"' in text, f"{relative}: Person schema missing")
    require('"provider": {' in text and '"@id": "https://alinahorb.com/#person"' in text, f"{relative}: Service provider identity mismatch")
    require('"url": "https://alinahorb.com/"' in text, f"{relative}: canonical Person URL missing")
    require('"@type": "FAQPage"' in text, f"{relative}: FAQPage schema missing")
    require('"@type": "BreadcrumbList"' in text, f"{relative}: BreadcrumbList schema missing")
    require('priceCurrency": "EUR"' in text and '"price": "35"' in text, f"{relative}: price schema mismatch")
    require('data-contact-form' in text and 'data-form-status' in text and 'data-form-success' in text, f"{relative}: form or success state missing")
    require('name="service"' in text and 'name="message"' in text and 'name="availability"' in text, f"{relative}: compact consultation fields missing")
    require('name="language"' not in text and 'name="format"' not in text, f"{relative}: redundant intake fields remain")
    require(text.count('field-required') >= 3 and text.count('field-optional') >= 4, f"{relative}: required/optional labels missing")
    require('name="channel" required' not in text and 'name="service" required' not in text and 'name="timezone" required' not in text and 'name="availability" required' not in text, f"{relative}: optional field is still required")
    require('site-config.v2.js' in text and 'site.v2.js' in text, f"{relative}: form runtime missing")
    require('site.consultations.v1.css' in text, f"{relative}: page stylesheet missing")
    require('50' in text and '35 €' in text and '1 600 грн' in text and '12 320 грн' in text and '240 €' in text, f"{relative}: confirmed duration/price missing")
    require(all(token not in text for token in ('20 €', '1 000 грн', '770 грн', '7 700 грн', '"price": "20"', '"price": "600"')), f"{relative}: legacy price remains")
    require(not OBSOLETE_270_EUR.search(text), f"{relative}: obsolete 270 € package remains")
    require(not has_standalone_600_uah(text), f"{relative}: standalone legacy 600 грн remains")
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
