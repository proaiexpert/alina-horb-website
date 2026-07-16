#!/usr/bin/env python3
"""Validate bilingual homepage social metadata and JPEG card dimensions."""

from __future__ import annotations

import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROBOTS = '<meta name="robots" content="index, follow, max-image-preview:large">'
EXPECTED = {
    ROOT / "index.html": {
        "image": "https://alinahorb.com/assets/images/social/alina-horb-og-ua-v2.jpg",
        "other_image": "alina-horb-og-ru-v2.jpg",
        "legacy_image": "alina-horb-og-ua-v1.jpg",
        "title": "Аліна Горб — психолог",
        "description_fragment": "українською та російською",
        "hero": "Психологічна підтримка,",
        "supporting": "Коли переживань стає надто багато",
    },
    ROOT / "ru/index.html": {
        "image": "https://alinahorb.com/assets/images/social/alina-horb-og-ru-v2.jpg",
        "other_image": "alina-horb-og-ua-v2.jpg",
        "legacy_image": "alina-horb-og-ru-v1.jpg",
        "title": "Алина Горб — психолог",
        "description_fragment": "на русском и украинском",
        "hero": "Психологическая поддержка,",
        "supporting": "Когда переживаний становится слишком много",
    },
}
IMAGES = (
    ROOT / "assets/images/social/alina-horb-og-ua-v2.jpg",
    ROOT / "assets/images/social/alina-horb-og-ru-v2.jpg",
)


def jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        raise AssertionError(f"Not a JPEG: {path}")
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        marker = data[i]
        i += 1
        if marker in {0xD8, 0xD9}:
            continue
        length = struct.unpack(">H", data[i : i + 2])[0]
        if marker in {
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        }:
            height, width = struct.unpack(">HH", data[i + 3 : i + 7])
            return width, height
        i += length
    raise AssertionError(f"Could not read JPEG dimensions: {path}")


def one(text: str, pattern: str, label: str) -> str:
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    if len(matches) != 1:
        raise AssertionError(f"Expected one {label}; found {len(matches)}")
    return matches[0]


def validate_page(path: Path, expected: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    assert "proaiexpert.github.io/alina-horb-website" not in text, f"Old social host remains in {path}"
    assert expected["other_image"] not in text, f"Wrong-language social image appears in {path}"
    assert expected["legacy_image"] not in text, f"Legacy cached social image remains in {path}"
    assert expected["hero"] in text, f"Approved Hero H1 missing in {path}"
    assert expected["supporting"] in text, f"Approved Hero supporting text missing in {path}"
    assert PUBLIC_ROBOTS in text and "noindex" not in text.lower(), f"Public indexing is not active in {path}"

    og_title = one(text, r'<meta property="og:title" content="([^"]+)">', f"og:title in {path}")
    assert og_title == expected["title"]
    og_description = one(text, r'<meta property="og:description" content="([^"]+)">', f"og:description in {path}")
    assert expected["description_fragment"] in og_description

    image = expected["image"]
    required = (
        f'<meta property="og:image" content="{image}">',
        f'<meta property="og:image:url" content="{image}">',
        f'<meta property="og:image:secure_url" content="{image}">',
        f'<meta name="twitter:image" content="{image}">',
        f'<link rel="image_src" href="{image}">',
        '<meta property="og:image:type" content="image/jpeg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
    )
    for tag in required:
        assert text.count(tag) == 1, f"Missing or duplicate social tag in {path}: {tag}"


for page, expected in EXPECTED.items():
    validate_page(page, expected)
for image in IMAGES:
    assert image.exists(), f"Missing social preview: {image}"
    assert jpeg_size(image) == (1200, 630), f"Wrong dimensions for {image}: {jpeg_size(image)}"
    assert image.stat().st_size < 350_000, f"Social image exceeds 350 KB: {image.stat().st_size}"

print("Bilingual Telegram/Open Graph previews: OK")
