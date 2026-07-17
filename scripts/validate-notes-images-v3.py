#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets" / "images" / "notes"
FILES = (
    "alina-horb-note-first-consultation-v3.webp",
    "alina-horb-note-conversation-v3.webp",
    "alina-horb-note-observation-v3.webp",
    "alina-horb-note-transition-v3.webp",
)

missing = [name for name in FILES if not (IMAGES / name).is_file()]
if missing:
    raise SystemExit("Missing Notes images:\n- " + "\n- ".join(missing))

for name in FILES:
    size = (IMAGES / name).stat().st_size
    if size <= 0 or size > 160_000:
        raise SystemExit(f"Unexpected image size for {name}: {size} bytes")

css = (ROOT / "assets/css/site.notes-images.v3.css").read_text(encoding="utf-8")
for token in (
    "note-photo--conversation",
    "note-photo--observation",
    "note-photo--transition",
    ".article-hero-visual",
    "prefers-reduced-motion",
):
    if token not in css:
        raise SystemExit(f"Missing static Notes image CSS contract: {token}")

pages = [
    ROOT / "index.html",
    ROOT / "ru/index.html",
    ROOT / "notes/index.html",
    ROOT / "ru/notes/index.html",
    *sorted((ROOT / "notes").glob("*/index.html")),
    *sorted((ROOT / "ru/notes").glob("*/index.html")),
]
combined = "\n".join(path.read_text(encoding="utf-8") for path in pages)
for name in FILES:
    if name not in combined:
        raise SystemExit(f"Static image is not referenced by production markup: {name}")
for forbidden in ("initEditorialNotesImages", "site.notes-images.v3-1.js"):
    if forbidden in combined or forbidden in (ROOT / "assets/js/site.v2.js").read_text(encoding="utf-8"):
        raise SystemExit(f"Runtime Notes image mutation remains: {forbidden}")

print("Static Notes editorial image validation: OK")
