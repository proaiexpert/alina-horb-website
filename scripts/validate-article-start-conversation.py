#!/usr/bin/env python3
"""Validate the bilingual V3.2 article about starting a difficult conversation."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_CSS = ROOT / "assets/css/site.article.v3-2.css"
THEME_CSS = ROOT / "assets/css/site.article.conversation.v3-2.css"

PAGES = {
    ROOT / "notes/how-to-start-the-conversation/index.html": {
        "lang": "uk",
        "canonical": "https://alinahorb.com/notes/how-to-start-the-conversation/",
        "alternate": "https://alinahorb.com/ru/notes/how-to-start-the-conversation/",
        "title": "Як почати розмову, коли важко сформулювати запит",
        "privacy": "../../privacy/",
    },
    ROOT / "ru/notes/how-to-start-the-conversation/index.html": {
        "lang": "ru",
        "canonical": "https://alinahorb.com/ru/notes/how-to-start-the-conversation/",
        "alternate": "https://alinahorb.com/notes/how-to-start-the-conversation/",
        "title": "Как начать разговор, когда трудно сформулировать запрос",
        "privacy": "../../privacy/",
    },
}

REQUIRED_IDS = {
    "main-content", "direct-answer-title", "request", "begin", "phrases",
    "limits", "send", "author-title", "source-note-title", "related-title",
    "article-cta-title",
}

FORBIDDEN_INTERPRETATIONS = (
    "алекситим", "диссоци", "сопротивлен", "вытеснен", "подавленное",
    "алекситим", "дисоці", "опір є", "витіснен", "прихована травма",
    "психолог зрозуміє без слів", "психолог поймёт без слов",
)


def strip_tags(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_page(path: Path, expected: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    lower = text.lower()

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
    if expected["title"] not in text:
        fail(f"Expected title missing in {rel}")
    if expected["privacy"] not in text:
        fail(f"Privacy link missing in {rel}")
    if "hello@alinahorb.com" not in text or "alinahorb1991@gmail.com" in text:
        fail(f"Public email regression in {rel}")
    for stylesheet in ("site.article.v3-2.css", "site.article.conversation.v3-2.css"):
        if stylesheet not in text:
            fail(f"Missing {stylesheet} in {rel}")
    if "article-theme-conversation" not in text:
        fail(f"Distinct conversation theme missing in {rel}")

    if len(re.findall(r"<h1\b", text, flags=re.I)) != 1:
        fail(f"Expected one H1 in {rel}")
    ids = re.findall(r'\bid="([^"]+)"', text)
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        fail(f"Duplicate IDs in {rel}: {duplicates}")
    missing = sorted(REQUIRED_IDS - set(ids))
    if missing:
        fail(f"Missing required IDs in {rel}: {missing}")

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

    if len(re.findall(r'<li><a href="#(?:request|begin|phrases|limits|send)"', text)) != 5:
        fail(f"Expected five contents links in {rel}")
    if len(re.findall(r'class="article-opening-card"', text)) != 4:
        fail(f"Expected four opening phrase cards in {rel}")
    if len(re.findall(r'class="article-soft-step"', text)) != 3:
        fail(f"Expected three soft steps in {rel}")
    if len(re.findall(r'class="article-related-card"', text)) != 2:
        fail(f"Expected two related cards in {rel}")

    for marker in (
        "article-hero-visual--conversation", "article-conversation-note",
        "article-pullquote", "article-opening-grid", "article-message-example",
        "article-soft-steps", "article-author-card", "article-source-note",
        "article-cta-band",
    ):
        if marker not in text:
            fail(f"Missing {marker} in {rel}")

    for forbidden in FORBIDDEN_INTERPRETATIONS:
        if forbidden in lower:
            fail(f"Unsupported interpretation {forbidden!r} in {rel}")

    if 'https://alinahorb.com/assets/images/notes/alina-horb-note-conversation-v3.webp' not in text:
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
    for css_path in (BASE_CSS, THEME_CSS):
        if not css_path.exists():
            fail(f"Missing stylesheet: {css_path.relative_to(ROOT)}")
    theme = THEME_CSS.read_text(encoding="utf-8")
    for selector in (
        ".article-hero-visual--conversation", ".article-conversation-note",
        ".article-opening-grid", ".article-message-example", ".article-soft-steps",
    ):
        if selector not in theme:
            fail(f"Missing conversation selector: {selector}")
    for path, expected in PAGES.items():
        validate_page(path, expected)
    print("V3.2 difficult-to-formulate-request article: OK")


if __name__ == "__main__":
    main()
