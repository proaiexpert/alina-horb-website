#!/usr/bin/env python3
from pathlib import Path
import struct

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

REQUIRED_TAGS = (
    '<link rel="icon" href="/favicon.ico" sizes="any">',
    '<link rel="icon" type="image/svg+xml" href="/assets/images/logos/favicon-ag.svg">',
    '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">',
    '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">',
    '<link rel="shortcut icon" href="/favicon.ico">',
    '<meta name="theme-color" content="#f5f0e8">',
)


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssertionError(f"Not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


for relative in ROUTES:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for tag in REQUIRED_TAGS:
        if text.count(tag) != 1:
            raise AssertionError(f"{relative}: expected one favicon contract: {tag}")
    if "assets/images/logos/favicon-ag.svg" not in text:
        raise AssertionError(f"{relative}: SVG favicon missing")

favicon = ROOT / "favicon.ico"
if not favicon.is_file() or favicon.read_bytes()[:4] != b"\x00\x00\x01\x00":
    raise AssertionError("favicon.ico is missing or invalid")
if png_size(ROOT / "favicon-16x16.png") != (16, 16):
    raise AssertionError("favicon-16x16.png has wrong dimensions")
if png_size(ROOT / "favicon-32x32.png") != (32, 32):
    raise AssertionError("favicon-32x32.png has wrong dimensions")

print(f"Favicon fallbacks validated for {len(ROUTES)} public routes")
