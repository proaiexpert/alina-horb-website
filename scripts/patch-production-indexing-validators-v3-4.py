#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ROOT / "scripts/validate-article-v32.py",
    ROOT / "scripts/validate-article-start-conversation.py",
    ROOT / "scripts/validate-article-coping-support.py",
    ROOT / "scripts/validate-article-relocation.py",
    ROOT / "scripts/validate-notes-hub-v32.py",
]

OLD = '''    if '<meta name="robots" content="noindex, nofollow">' not in text:
        fail(f"noindex changed in {rel}")'''

NEW = '''    allowed_robots = (
        '<meta name="robots" content="noindex, nofollow">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
    )
    if not any(marker in text for marker in allowed_robots):
        fail(f"robots directive missing in {rel}")'''

for path in FILES:
    text = path.read_text(encoding="utf-8")
    if text.count(OLD) != 1:
        raise SystemExit(f"Expected one legacy robots assertion in {path.relative_to(ROOT)}")
    updated = text.replace(OLD, NEW, 1)
    if OLD in updated or updated.count(NEW) != 1:
        raise SystemExit(f"Validator patch failed in {path.relative_to(ROOT)}")
    path.write_text(updated, encoding="utf-8")

print(f"Updated {len(FILES)} validators to support source and production indexing states")
