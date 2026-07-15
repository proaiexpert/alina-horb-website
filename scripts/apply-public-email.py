#!/usr/bin/env python3
"""Replace the legacy public Gmail address with the branded domain email."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "alinahorb1991@gmail.com"
NEW = "hello@alinahorb.com"
TEXT_SUFFIXES = {".html", ".js", ".md", ".json", ".xml", ".txt", ".yml", ".yaml"}
SKIP_PARTS = {".git", "_site", "node_modules", "qa-artifacts"}


def main() -> None:
    changed = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if OLD not in text:
            continue
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

    if not changed:
        print("No legacy public email occurrences found.")
        return

    print("Updated public email in:")
    for item in changed:
        print(f"- {item}")


if __name__ == "__main__":
    main()
