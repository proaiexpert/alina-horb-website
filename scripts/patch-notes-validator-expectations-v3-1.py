#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_required(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"Expected validator contract not found in {path.relative_to(ROOT)}: {old}")
    path.write_text(text.replace(old, new), encoding="utf-8")


hub = ROOT / "scripts/validate-notes-hub-v32.py"
replace_required(hub, '"social": "alina-horb-og-ua-v1.jpg"', '"social": "alina-horb-note-first-consultation-v3.webp"')
replace_required(hub, '"social": "alina-horb-og-ru-v1.jpg"', '"social": "alina-horb-note-first-consultation-v3.webp"')
replace_required(
    hub,
    '    if \'<meta name="robots" content="noindex, nofollow">\' not in text:\n        fail(f"noindex changed in {rel}")',
    '    allowed_robots = (\'<meta name="robots" content="noindex, nofollow">\', \'<meta name="robots" content="index, follow, max-image-preview:large">\')\n    if not any(marker in text for marker in allowed_robots):\n        fail(f"robots directive missing in {rel}")',
)
replace_required(
    hub,
    '    if text.count("alina-horb-notes-editorial-v2") != 2:\n        fail(f"Featured photography must appear once as source+fallback in {rel}")',
    '    if "alina-horb-note-first-consultation-v3.webp" not in text:\n        fail(f"Static featured photography missing in {rel}")',
)
replace_required(
    hub,
    '    if text.count("alina-horb-notes-editorial-v2") != 2:\n        fail(f"Homepage featured photography must appear once as source+fallback in {rel}")',
    '    if "alina-horb-note-first-consultation-v3.webp" not in text:\n        fail(f"Static homepage featured photography missing in {rel}")',
)

article_images = {
    "scripts/validate-article-v32.py": "alina-horb-note-first-consultation-v3.webp",
    "scripts/validate-article-start-conversation.py": "alina-horb-note-conversation-v3.webp",
    "scripts/validate-article-coping-support.py": "alina-horb-note-observation-v3.webp",
    "scripts/validate-article-relocation.py": "alina-horb-note-transition-v3.webp",
}
old = "https://alinahorb.com/assets/images/notes/alina-horb-notes-editorial-v2.jpg"
for rel, filename in article_images.items():
    replace_required(ROOT / rel, old, f"https://alinahorb.com/assets/images/notes/{filename}")

print("Legacy validators aligned with static Notes image assets and either indexing state")
