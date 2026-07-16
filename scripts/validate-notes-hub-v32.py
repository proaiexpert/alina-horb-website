#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets/css/site.notes-hub.v3-2.css"

ROUTES = [
    "first-consultation/",
    "how-to-start-the-conversation/",
    "when-coping-stops-helping/",
    "stress-relocation-and-lost-support/",
]

HUBS = {
    ROOT / "notes/index.html": {
        "lang": "uk",
        "canonical": "https://alinahorb.com/notes/",
        "alternate": "https://alinahorb.com/ru/notes/",
        "og_locale": "uk_UA",
        "og_url": "https://alinahorb.com/notes/",
        "social": "alina-horb-og-ua-v1.jpg",
        "home": "../",
    },
    ROOT / "ru/notes/index.html": {
        "lang": "ru",
        "canonical": "https://alinahorb.com/ru/notes/",
        "alternate": "https://alinahorb.com/notes/",
        "og_locale": "ru_RU",
        "og_url": "https://alinahorb.com/ru/notes/",
        "social": "alina-horb-og-ru-v1.jpg",
        "home": "../",
    },
}

HOMES = {
    ROOT / "index.html": {"prefix": "notes/", "css": "assets/css/site.notes-hub.v3-2.css"},
    ROOT / "ru/index.html": {"prefix": "notes/", "css": "../assets/css/site.notes-hub.v3-2.css"},
}


def fail(message: str) -> None:
    raise AssertionError(message)


def duplicate_ids(text: str) -> list[str]:
    ids = re.findall(r'\bid="([^"]+)"', text)
    return sorted({value for value in ids if ids.count(value) > 1})


def validate_common(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT)
    allowed_robots = (
        '<meta name="robots" content="noindex, nofollow">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
    )
    if not any(marker in text for marker in allowed_robots):
        fail(f"robots directive missing in {rel}")
    if len(re.findall(r"<h1\b", text, flags=re.I)) != 1:
        fail(f"Expected one H1 in {rel}")
    duplicates = duplicate_ids(text)
    if duplicates:
        fail(f"Duplicate IDs in {rel}: {duplicates}")
    if "hello@alinahorb.com" not in text or "alinahorb1991@gmail.com" in text:
        fail(f"Public email regression in {rel}")


def validate_hub(path: Path, expected: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    validate_common(path, text)

    required = [
        f'<html lang="{expected["lang"]}">',
        f'<link rel="canonical" href="{expected["canonical"]}">',
        expected["alternate"],
        '<link rel="alternate" hreflang="x-default" href="https://alinahorb.com/notes/">',
        f'<meta property="og:locale" content="{expected["og_locale"]}">',
        f'<meta property="og:url" content="{expected["og_url"]}">',
        expected["social"],
        "site.notes-hub.v3-2.css",
        "notes-hub-main-v32",
        "notes-hub-hero-v32",
        "notes-hub-feature",
        "notes-hub-card-grid",
    ]
    for marker in required:
        if marker not in text:
            fail(f"Missing {marker!r} in {rel}")

    if len(re.findall(r'class="notes-hub-card"', text)) != 3:
        fail(f"Expected three supporting cards in {rel}")
    if len(re.findall(r'class="notes-hub-feature"', text)) != 1:
        fail(f"Expected one featured story in {rel}")
    if text.count("alina-horb-notes-editorial-v2") != 2:
        fail(f"Featured photography must appear once as source+fallback in {rel}")

    for modifier in ("note-identity--conversation", "note-identity--observation", "note-identity--transition"):
        if text.count(modifier) != 1:
            fail(f"Expected one distinct {modifier} visual in {rel}")

    for route in ROUTES:
        if route not in text:
            fail(f"Missing article route {route} in {rel}")

    required_ids = {
        "main-content",
        "notes-hub-title",
        "featured-article",
        "featured-title",
        "supporting-title",
        "conversation-article",
        "observation-article",
        "relocation-article",
    }
    ids = set(re.findall(r'\bid="([^"]+)"', text))
    missing = sorted(required_ids - ids)
    if missing:
        fail(f"Missing required hub IDs in {rel}: {missing}")


def validate_home(path: Path, expected: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    validate_common(path, text)

    if expected["css"] not in text:
        fail(f"Notes stylesheet missing in {rel}")
    if text.count('class="notes-section notes-section--v32 section-block"') != 1:
        fail(f"Expected one V3.2 Notes section in {rel}")
    if text.count('class="home-note-feature"') != 1:
        fail(f"Expected one homepage featured story in {rel}")
    if text.count('class="home-note-entry"') != 3:
        fail(f"Expected three homepage supporting stories in {rel}")
    if text.count("alina-horb-notes-editorial-v2") != 2:
        fail(f"Homepage featured photography must appear once as source+fallback in {rel}")
    if 'class="note-featured"' in text or 'class="notes-compact"' in text:
        fail(f"Legacy repeated-card system remains in {rel}")

    for modifier in ("note-identity--conversation", "note-identity--observation", "note-identity--transition"):
        if text.count(modifier) != 1:
            fail(f"Expected one distinct {modifier} homepage visual in {rel}")
    for route in ROUTES:
        if expected["prefix"] + route not in text:
            fail(f"Missing homepage article route {route} in {rel}")


def main() -> None:
    if not CSS.exists():
        fail("Missing assets/css/site.notes-hub.v3-2.css")
    css = CSS.read_text(encoding="utf-8")
    selectors = [
        ".notes-hub-hero-grid",
        ".notes-hub-feature",
        ".notes-hub-card-grid",
        ".note-identity--conversation",
        ".note-identity--observation",
        ".note-identity--transition",
        ".notes-section--v32",
        ".home-notes-editorial",
        ".home-note-feature",
        ".home-note-entry",
    ]
    for selector in selectors:
        if selector not in css:
            fail(f"Missing Notes selector {selector}")

    for path, expected in HUBS.items():
        validate_hub(path, expected)
    for path, expected in HOMES.items():
        validate_home(path, expected)

    print("V3.2 Notes hub and homepage article-card system: OK")


if __name__ == "__main__":
    main()
