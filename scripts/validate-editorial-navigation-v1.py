#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "assets/css/site.navigation.v1.css"
JS = ROOT / "assets/js/site.navigation.v1.js"

if not CSS.is_file() or not CSS.read_text(encoding="utf-8").strip():
    raise SystemExit("navigation stylesheet is missing or empty")
if not JS.is_file() or not JS.read_text(encoding="utf-8").strip():
    raise SystemExit("navigation runtime is missing or empty")

print("Editorial navigation files are present and non-empty.")
