#!/usr/bin/env python3
"""Ensure only the branded public email is exposed by production text files."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "alinahorb1991@gmail.com"
NEW = "hello@alinahorb.com"
TEXT_SUFFIXES = {".html", ".js", ".md", ".json", ".xml", ".txt", ".yml", ".yaml"}
SKIP_PARTS = {".git", "_site", "node_modules", "qa-artifacts"}


def main() -> None:
    old_hits = []
    new_hits = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if OLD in text:
            old_hits.append(path.relative_to(ROOT).as_posix())
        if NEW in text:
            new_hits.append(path.relative_to(ROOT).as_posix())

    if old_hits:
        raise SystemExit("Legacy Gmail address remains in: " + ", ".join(old_hits))
    if not new_hits:
        raise SystemExit("Canonical public email is missing from repository text files")

    print(f"Canonical public email OK in {len(new_hits)} files; legacy address absent.")


if __name__ == "__main__":
    main()
