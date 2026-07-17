#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    Path("index.html"): ("assets/", None),
    Path("ru/index.html"): ("../assets/", None),
    Path("notes/index.html"): ("../assets/", None),
    Path("ru/notes/index.html"): ("../../assets/", None),
}

SLUGS = {
    "first-consultation": "first-consultation",
    "how-to-start-the-conversation": "conversation",
    "when-coping-stops-helping": "observation",
    "stress-relocation-and-lost-support": "transition",
}
for slug, key in SLUGS.items():
    PAGES[Path("notes") / slug / "index.html"] = ("../../assets/", key)
    PAGES[Path("ru/notes") / slug / "index.html"] = ("../../../assets/", key)

FILES = {
    "first-consultation": "alina-horb-note-first-consultation-v3.webp",
    "conversation": "alina-horb-note-conversation-v3.webp",
    "observation": "alina-horb-note-observation-v3.webp",
    "transition": "alina-horb-note-transition-v3.webp",
}

for name in FILES.values():
    path = ROOT / "assets/images/notes" / name
    if not path.is_file() or path.stat().st_size <= 0:
        raise SystemExit(f"Missing or empty image: {path}")

for page, (asset_prefix, article_key) in PAGES.items():
    path = ROOT / page
    text = path.read_text(encoding="utf-8")
    css = f'{asset_prefix}css/site.notes-images.v3.css?v=3.1'
    if css not in text:
        raise SystemExit(f"Missing versioned static Notes CSS in {page}: {css}")
    if "site.notes-images.v3-1.js" in text:
        raise SystemExit(f"Runtime Notes image replacement remains in {page}")

    note_sources = re.findall(r'(?:src|srcset)="([^"]*assets/images/notes/[^"]+)"', text)
    if page in (Path("index.html"), Path("ru/index.html"), Path("notes/index.html"), Path("ru/notes/index.html")):
        expected = set(FILES.values())
        found = {Path(src).name for src in note_sources}
        if not expected.issubset(found):
            raise SystemExit(f"Not all four Notes images are static in {page}: {sorted(found)}")
        for forbidden in ("note-identity-quote", "note-observation-bars", "note-transition-route"):
            if forbidden in text:
                raise SystemExit(f"Legacy decorative illustration remains in {page}: {forbidden}")

    if article_key:
        filename = FILES[article_key]
        expected_relative = f'{asset_prefix}images/notes/{filename}'
        expected_absolute = f'https://alinahorb.com/assets/images/notes/{filename}'
        if expected_relative not in text:
            raise SystemExit(f"Wrong article hero source in {page}: expected {expected_relative}")
        if expected_absolute not in text:
            raise SystemExit(f"Wrong article metadata image in {page}: expected {expected_absolute}")
        data_note = "first" if article_key == "first-consultation" else article_key
        if f'data-note="{data_note}"' not in text:
            raise SystemExit(f"Missing article data-note in {page}")

apply_script = (ROOT / "scripts/apply-notes-images-v3-1.py").read_text(encoding="utf-8")
if "site.notes-images.v3-1.js" in apply_script:
    raise SystemExit("Deployment still injects the obsolete Notes image runtime")

print("Static Notes image integration and paths: OK")
