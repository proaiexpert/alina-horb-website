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

home_js = (ROOT / "assets" / "js" / "site.v2.js").read_text(encoding="utf-8")
inner_js = (ROOT / "assets" / "js" / "site.chrome.v3.js").read_text(encoding="utf-8")
css = (ROOT / "assets" / "css" / "site.notes-images.v3.css").read_text(encoding="utf-8")

for name in FILES:
    if name not in home_js and name not in inner_js:
        raise SystemExit(f"Image is not referenced by runtime: {name}")

required = (
    "initEditorialNotesImages",
    "site.notes-images.v3.css",
    "note-photo--conversation",
    "note-photo--observation",
    "note-photo--transition",
)
combined = home_js + inner_js + css
missing_contracts = [value for value in required if value not in combined]
if missing_contracts:
    raise SystemExit("Missing Notes image contracts:\n- " + "\n- ".join(missing_contracts))

print("Notes editorial image validation: OK")
