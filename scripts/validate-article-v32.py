#!/usr/bin/env python3
"""Validate the canonical V3.2 article template and bilingual pilot article."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets/css/site.article.v3-2.css"

PAGES = {
    ROOT / "notes/first-consultation/index.html": {
        "lang": "uk",
        "canonical": "https://alinahorb.com/notes/first-consultation/",
        "alternate": "https://alinahorb.com/ru/notes/first-consultation/",
        "title_fragment": "Що відбувається на першій консультації",
        "privacy_href": "../../privacy/",
    },
    ROOT / "ru/notes/first-consultation/index.html": {
        "lang": "ru",
        "canonical": "https://alinahorb.com/ru/notes/first-consultation/",
        "alternate": "https://alinahorb.com/notes/first-consultation/",
        "title_fragment": "Что происходит на первой консультации",
        "privacy_href": "../../privacy/",
    },
}

REQUIRED_IDS = {"main-content", "direct-answer-title", "purpose", "start", "questions", "ending", "prepare", "author-title", "source-note-title", "related-title", "article-cta-title"}


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_page(path: Path, expected: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)

    if f'<html lang="{expected["lang"]}">' not in text:
        fail(f"Wrong html language in {rel}")
    allowed_robots = (
        '<meta name="robots" content="noindex, nofollow">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
    )
    if not any(marker in text for marker in allowed_robots):
        fail(f"robots directive missing in {rel}")
    if f'<link rel="canonical" href="{expected["canonical"]}">' not in text:
        fail(f"Wrong canonical in {rel}")
    if expected["alternate"] not in text:
        fail(f"Missing reciprocal hreflang in {rel}")
    if "hello@alinahorb.com" not in text or "alinahorb1991@gmail.com" in text:
        fail(f"Public email regression in {rel}")
    if "site.article.v3-2.css" not in text:
        fail(f"V3.2 article stylesheet missing in {rel}")
    if expected["title_fragment"] not in text:
        fail(f"Expected title fragment missing in {rel}")
    if expected["privacy_href"] not in text:
        fail(f"Privacy link missing in {rel}")

    if len(re.findall(r"<h1\b", text, flags=re.I)) != 1:
        fail(f"Expected one H1 in {rel}")

    ids = re.findall(r'\bid="([^"]+)"', text)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        fail(f"Duplicate IDs in {rel}: {duplicates}")
    missing_ids = sorted(REQUIRED_IDS - set(ids))
    if missing_ids:
        fail(f"Missing required IDs in {rel}: {missing_ids}")

    card_match = re.search(r'<div class="article-answer-card">(.*?)</div>\s*</div>\s*</section>', text, flags=re.S)
    if not card_match:
        fail(f"Direct-answer card missing in {rel}")
    paragraphs = re.findall(r"<p\b[^>]*>(.*?)</p>", card_match.group(1), flags=re.S)
    if len(paragraphs) < 2:
        fail(f"Direct-answer text missing in {rel}")
    direct_answer = strip_tags(paragraphs[-1])
    word_count = len(re.findall(r"[\w’'-]+", direct_answer, flags=re.UNICODE))
    if not 80 <= word_count <= 120:
        fail(f"Direct answer in {rel} has {word_count} words; expected 80–120")

    if len(re.findall(r'class="article-related-card"', text)) != 2:
        fail(f"Expected two related cards in {rel}")
    if len(re.findall(r'<li><a href="#(?:purpose|start|questions|ending|prepare)"', text)) != 5:
        fail(f"Expected five contents links in {rel}")
    for marker in ("article-hero-visual", "article-pullquote", "article-info-grid", "article-checklist", "article-author-card", "article-source-note", "article-cta-band"):
        if marker not in text:
            fail(f"Missing {marker} in {rel}")

    if 'https://alinahorb.com/assets/images/notes/alina-horb-note-first-consultation-v3.webp' not in text:
        fail(f"Production social image missing in {rel}")

    scripts = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, flags=re.S)
    if len(scripts) != 1:
        fail(f"Expected one JSON-LD block in {rel}")
    payload = json.loads(scripts[0])
    graph = payload.get("@graph", [])
    types = {item.get("@type") for item in graph if isinstance(item, dict)}
    if not {"Article", "BreadcrumbList"}.issubset(types):
        fail(f"Structured data types missing in {rel}: {types}")
    article = next(item for item in graph if item.get("@type") == "Article")
    if article.get("dateModified") != "2026-07-15":
        fail(f"Unexpected dateModified in {rel}")
    if article.get("inLanguage") != expected["lang"]:
        fail(f"Wrong structured-data language in {rel}")


def main() -> None:
    if not CSS.exists():
        fail("Missing assets/css/site.article.v3-2.css")
    css = CSS.read_text(encoding="utf-8")
    for selector in (".article-hero-grid", ".article-answer-card", ".article-layout--v32", ".article-author-card", ".article-related-grid", ".article-cta-band"):
        if selector not in css:
            fail(f"Missing article selector: {selector}")
    for path, expected in PAGES.items():
        validate_page(path, expected)
    print("V3.2 article template and first-consultation pilot: OK")


if __name__ == "__main__":
    main()
