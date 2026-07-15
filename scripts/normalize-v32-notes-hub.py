#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "ru/notes/index.html"
text = path.read_text(encoding="utf-8")
replacements = {
    '<meta property="og:locale" content="uk_UA">': '<meta property="og:locale" content="ru_RU">',
    '<meta property="og:locale:alternate" content="ru_RU">': '<meta property="og:locale:alternate" content="uk_UA">',
    '<meta property="og:url" content="https://alinahorb.com/notes/">': '<meta property="og:url" content="https://alinahorb.com/ru/notes/">',
}
for old, new in replacements.items():
    if new in text:
        continue
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one occurrence of {old!r}; found {count}")
    text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("Normalized RU Notes hub metadata")
