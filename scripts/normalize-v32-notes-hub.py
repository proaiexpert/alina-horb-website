#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "ru/notes/index.html"
text = path.read_text(encoding="utf-8")
replacements = {
    '<meta property="og:locale" content="uk_UA">': '<meta property="og:locale" content="ru_RU">',
    '<meta property="og:locale:alternate" content="ru_RU">': '<meta property="og:locale:alternate" content="uk_UA">',
    '<meta property="og:url" content="https://alinahorb.com/notes/">': '<meta property="og:url" content="https://alinahorb.com/ru/notes/">',
    'aria-label="Вибір мови"': 'aria-label="Выбор языка"',
}

for old, new in replacements.items():
    old_count = text.count(old)
    if old_count == 1:
        text = text.replace(old, new, 1)
        continue
    if old_count == 0 and new in text:
        continue
    raise SystemExit(f"Expected one old occurrence or an already-normalized value for {old!r}; found {old_count}")

path.write_text(text, encoding="utf-8")
print("Normalized RU Notes hub metadata and accessibility labels")
