#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROUTES = [
    "index.html",
    "ru/index.html",
    "about/index.html",
    "ru/about/index.html",
    "consultations/index.html",
    "ru/consultations/index.html",
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

GATED = '<meta name="robots" content="noindex, nofollow">'
PUBLIC = '<meta name="robots" content="index, follow, max-image-preview:large">'

for relative in ROUTES:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Missing public route: {relative}")

    text = path.read_text(encoding="utf-8")
    gated_count = text.count(GATED)
    public_count = text.count(PUBLIC)

    if gated_count == 1 and public_count == 0:
        text = text.replace(GATED, PUBLIC, 1)
        path.write_text(text, encoding="utf-8")
    elif gated_count == 0 and public_count == 1:
        pass
    else:
        raise SystemExit(
            f"{relative}: expected exactly one indexing directive; "
            f"noindex={gated_count}, public={public_count}"
        )

    final = path.read_text(encoding="utf-8")
    if final.count(PUBLIC) != 1 or GATED in final:
        raise SystemExit(f"{relative}: production indexing directive was not applied")

print(f"Production indexing enabled for {len(ROUTES)} public routes")
