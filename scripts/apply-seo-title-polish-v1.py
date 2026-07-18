#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLACEMENTS = {
    "ru/notes/first-consultation/index.html": (
        "<title>Первая консультация с психологом: как проходит и что подготовить — Алина Горб</title>",
        "<title>Первая консультация с психологом: как всё проходит — Алина Горб</title>",
    ),
    "ru/notes/how-to-start-the-conversation/index.html": (
        "<title>Как начать разговор с психологом, когда трудно сформулировать запрос — Алина Горб</title>",
        "<title>Как начать разговор с психологом без готового запроса — Алина Горб</title>",
    ),
}

for relative, (old, new) in REPLACEMENTS.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if old in text:
        text = text.replace(old, new, 1)
    elif new not in text:
        raise SystemExit(f"{relative}: expected title was not found")
    path.write_text(text, encoding="utf-8")

print("Russian search titles polished.")
