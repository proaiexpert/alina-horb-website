#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "assets/js/site.v2.js"
text = path.read_text(encoding="utf-8")
required = (
    'let submitting = false;',
    'const controller = new AbortController();',
    'controller.abort(), 10000',
    '"Accept": "application/json"',
    'signal: controller.signal',
    'statusCode >= 500',
    'mailtoFallback(payload)',
)
missing = [needle for needle in required if needle not in text]
if missing:
    raise SystemExit("Hardened form runtime is incomplete: " + ", ".join(missing))
print("Hardened form runtime is present")
