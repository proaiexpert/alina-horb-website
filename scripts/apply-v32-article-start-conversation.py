#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    ROOT / "notes/how-to-start-the-conversation/index.html": {
        "«Мені важко зібрати думки, але я хотів би почати розмову».": "«Мені важко зібрати думки, але я хочу почати розмову».",
        "«Після змін не можу повернутися до звичного ритму»": "«Після змін не вдається повернутися до звичного ритму»",
        "«я постійно напружений»": "«я майже постійно відчуваю напругу»",
        "«Добрий день. Хотів би дізнатися про онлайн-консультацію українською.": "«Добрий день. Хочу дізнатися про онлайн-консультацію українською.",
        "«Я не впевнений, з чого почати, але хотів би поговорити про свій стан».": "«Я не знаю, з чого почати, але хочу поговорити про свій стан»."
    },
    ROOT / "ru/notes/how-to-start-the-conversation/index.html": {
        "«я постоянно напряжён»": "«я почти постоянно чувствую напряжение»",
        "«Я не уверен, с чего начать, но хочу поговорить о своём состоянии».": "«Я не знаю, с чего начать, но хочу поговорить о своём состоянии»."
    }
}

for path, replacements in REPLACEMENTS.items():
    text = path.read_text(encoding="utf-8")
    changed = False
    for old, new in replacements.items():
        if new in text:
            continue
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"Expected one occurrence in {path.relative_to(ROOT)}: {old!r}; found {count}")
        text = text.replace(old, new, 1)
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)}")
