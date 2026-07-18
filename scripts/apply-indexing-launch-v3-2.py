#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INDEXABLE = [
    "index.html", "ru/index.html", "about/index.html", "ru/about/index.html",
    "consultations/index.html", "ru/consultations/index.html", "notes/index.html", "ru/notes/index.html",
    "notes/first-consultation/index.html", "ru/notes/first-consultation/index.html",
    "notes/how-to-start-the-conversation/index.html", "ru/notes/how-to-start-the-conversation/index.html",
    "notes/when-coping-stops-helping/index.html", "ru/notes/when-coping-stops-helping/index.html",
    "notes/stress-relocation-and-lost-support/index.html", "ru/notes/stress-relocation-and-lost-support/index.html",
]
PRIVATE = ["privacy/index.html", "ru/privacy/index.html"]
SOURCE = '<meta name="robots" content="noindex, nofollow">'
PUBLIC = '<meta name="robots" content="index, follow, max-image-preview:large">'
PRIVATE_META = '<meta name="robots" content="noindex, follow">'

for relative in INDEXABLE:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Missing public route: {relative}")
    text = path.read_text(encoding="utf-8")
    if SOURCE in text and PUBLIC not in text:
        text = text.replace(SOURCE, PUBLIC, 1)
    if text.count(PUBLIC) != 1 or "noindex" in text.lower():
        raise SystemExit(f"{relative}: public indexing directive was not applied")
    path.write_text(text, encoding="utf-8")

for relative in PRIVATE:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Missing privacy route: {relative}")
    text = path.read_text(encoding="utf-8")
    text = text.replace(SOURCE, PRIVATE_META, 1).replace(PUBLIC, PRIVATE_META, 1)
    if text.count(PRIVATE_META) != 1:
        raise SystemExit(f"{relative}: privacy noindex policy was not applied")
    path.write_text(text, encoding="utf-8")

print(f"Production indexing enabled for {len(INDEXABLE)} search routes; {len(PRIVATE)} privacy routes remain noindex, follow")
