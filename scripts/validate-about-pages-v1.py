#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROBOTS = '<meta name="robots" content="index, follow, max-image-preview:large">'
GATED_ROBOTS = '<meta name="robots" content="noindex, nofollow">'

PAGES = {
    "about/index.html": {
        "lang": "uk",
        "canonical": "https://alinahorb.com/about/",
        "alternate": "https://alinahorb.com/ru/about/",
        "title": "Про Аліну Горб — освіта, досвід і підхід психолога",
        "h1": "Психологічна підтримка,",
        "person": "Аліна Горб",
        "degree": "Магістр психології",
        "practice": "Практика з 2016 року",
        "cta": "Записатися на консультацію",
        "og": "alina-horb-og-ua-v2.jpg",
    },
    "ru/about/index.html": {
        "lang": "ru",
        "canonical": "https://alinahorb.com/ru/about/",
        "alternate": "https://alinahorb.com/about/",
        "title": "Об Алине Горб — образование, опыт и подход психолога",
        "h1": "Психологическая поддержка,",
        "person": "Алина Горб",
        "degree": "Магистр психологии",
        "practice": "Практика с 2016 года",
        "cta": "Записаться на консультацию",
        "og": "alina-horb-og-ru-v2.jpg",
    },
}

REQUIRED_IDS = (
    "about", "path", "position", "methods", "education", "scope",
    "boundaries", "contact", "main-content",
)

REQUIRED_CLASSES = (
    "profile-hero", "profile-hero-portrait", "profile-hero-facts",
    "profile-timeline", "position-principles", "profile-method-list",
    "profile-diploma", "scope-index", "boundaries-card", "profile-final",
)

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


for relative, expected in PAGES.items():
    path = ROOT / relative
    require(path.is_file(), f"Missing About page: {relative}")
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")

    require(f'<html lang="{expected["lang"]}"' in text, f"{relative}: wrong html lang")
    require(text.count(f'<title>{expected["title"]}</title>') == 1, f"{relative}: title mismatch")
    require(len(re.findall(r'<meta name="description" content="[^"]+">', text)) == 1, f"{relative}: description missing")
    robots_count = text.count(GATED_ROBOTS) + text.count(PUBLIC_ROBOTS)
    require(robots_count == 1, f"{relative}: expected exactly one supported robots directive")
    require(text.count(f'<link rel="canonical" href="{expected["canonical"]}">') == 1, f"{relative}: canonical mismatch")
    require(f'hreflang="uk" href="https://alinahorb.com/about/"' in text, f"{relative}: UA hreflang missing")
    require(f'hreflang="ru" href="https://alinahorb.com/ru/about/"' in text, f"{relative}: RU hreflang missing")
    require('hreflang="x-default" href="https://alinahorb.com/about/"' in text, f"{relative}: x-default missing")
    require(f'<meta property="og:url" content="{expected["canonical"]}">' in text, f"{relative}: OG URL mismatch")
    require(expected["og"] in text, f"{relative}: localized OG image missing")
    require('"@type": "ProfilePage"' in text, f"{relative}: ProfilePage schema missing")
    require('"@type": "Person"' in text, f"{relative}: Person schema missing")
    require('"@type": "BreadcrumbList"' in text, f"{relative}: BreadcrumbList schema missing")
    require(len(re.findall(r'<h1\b', text, flags=re.I)) == 1, f"{relative}: expected one H1")
    require(expected["h1"] in text, f"{relative}: H1 copy missing")
    require(expected["person"] in text, f"{relative}: person name missing")
    require(expected["degree"] in text, f"{relative}: degree missing")
    require(expected["practice"] in text, f"{relative}: practice fact missing")
    require(expected["cta"] in text, f"{relative}: CTA missing")
    require("Дніпровський національний університет імені Олеся Гончара" in text or "Днепровский национальный университет имени Олеся Гончара" in text, f"{relative}: university missing")
    require("site.about.v1.css" in text, f"{relative}: page stylesheet missing")
    require("site.v2.js" in text, f"{relative}: site JS missing")
    require("alina-horb-about-v3-1.webp" in text, f"{relative}: portrait missing")
    require("alina-horb-diploma-public-1600.webp" in text, f"{relative}: diploma missing")
    require("hello@alinahorb.com" in text, f"{relative}: public email missing")
    require("alinahorb1991@gmail.com" not in text, f"{relative}: legacy Gmail found")
    require("TODO" not in text and "placeholder" not in text.lower(), f"{relative}: unfinished marker found")

    ids = re.findall(r'\bid="([^"]+)"', text)
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    require(not duplicates, f"{relative}: duplicate IDs {duplicates}")
    for identifier in REQUIRED_IDS:
        require(identifier in ids, f"{relative}: required id missing: {identifier}")
    for class_name in REQUIRED_CLASSES:
        require(class_name in text, f"{relative}: required component missing: {class_name}")

    section_count = len(re.findall(r'<section\b', text, flags=re.I))
    require(section_count >= 9, f"{relative}: profile page is structurally incomplete ({section_count} sections)")

ua = (ROOT / "about/index.html").read_text(encoding="utf-8") if (ROOT / "about/index.html").is_file() else ""
ru = (ROOT / "ru/about/index.html").read_text(encoding="utf-8") if (ROOT / "ru/about/index.html").is_file() else ""
if ua and ru:
    require(len(re.findall(r'<section\b', ua, flags=re.I)) == len(re.findall(r'<section\b', ru, flags=re.I)), "UA/RU section count mismatch")
    require(ua.count('class="profile-method-list"') == ru.count('class="profile-method-list"') == 1, "UA/RU method structure mismatch")
    require(ua.count('class="scope-index"') == ru.count('class="scope-index"') == 1, "UA/RU scope structure mismatch")

css_path = ROOT / "assets/css/site.about.v1.css"
require(css_path.is_file(), "About page stylesheet missing")
if css_path.is_file():
    css = css_path.read_text(encoding="utf-8")
    for selector in (
        ".profile-hero-layout", ".profile-section-grid", ".position-principles",
        ".profile-method-list", ".profile-education-layout", ".scope-index",
        ".boundaries-layout", ".profile-final-inner",
    ):
        require(selector in css, f"About CSS missing selector: {selector}")
    require("@media (max-width: 900px)" in css, "About CSS tablet breakpoint missing")
    require("@media (max-width: 700px)" in css, "About CSS mobile breakpoint missing")
    require("prefers-reduced-motion" in css, "About CSS reduced-motion support missing")

for asset in (
    "assets/images/portrait/alina-horb-about-v3-1.webp",
    "assets/images/portrait/alina-horb-about-v3-1.jpg",
    "assets/images/diploma/alina-horb-diploma-public-1600.webp",
    "assets/images/diploma/alina-horb-diploma-public-1600.jpg",
):
    require((ROOT / asset).is_file(), f"Required About asset missing: {asset}")

if errors:
    print("About page validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Bilingual premium About pages: OK")
