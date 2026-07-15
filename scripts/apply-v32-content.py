#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "scripts/v32-content"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new and new in text:
        return text
    if not new and old not in text:
        return text
    count = text.count(old)
    if count == 1:
        return text.replace(old, new, 1)
    raise RuntimeError(f"Expected one {label}; found {count}")


def apply_replacements(config_name: str) -> None:
    config = json.loads((DATA / config_name).read_text(encoding="utf-8"))
    path = ROOT / config["path"]
    text = path.read_text(encoding="utf-8")
    for item in config["replacements"]:
        text = replace_once(text, item["old"], item["new"], item["label"])
    path.write_text(text, encoding="utf-8")


def append_once(target: str, fragment: str, marker: str) -> None:
    path = ROOT / target
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    addition = (DATA / fragment).read_text(encoding="utf-8")
    path.write_text(text.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


def main() -> None:
    for config in ("ua.json", "ru-topics.json", "ru-about.json", "ua-principles.json", "ru-principles.json"):
        apply_replacements(config)
    append_once("assets/css/site.v3-1-stability.css", "approach.css", "V3.2 author voice and working approach")
    append_once("docs/PROJECT_SOURCE_OF_TRUTH.md", "source-of-truth.md", "V3.2 — Author voice and working approach")
    print("Applied V3.2 author voice and working approach.")


if __name__ == "__main__":
    main()
