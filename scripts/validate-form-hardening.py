#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
js = (ROOT / "assets/js/site.v2.js").read_text(encoding="utf-8")
config = (ROOT / "assets/js/site-config.v2.js").read_text(encoding="utf-8")

required = [
    'let submitting = false;',
    'if (submitting) return;',
    'const controller = new AbortController();',
    'controller.abort(), 10000',
    '"Accept": "application/json"',
    'signal: controller.signal',
    'requestError.status = response.status',
    'error?.name === "AbortError"',
    'statusCode >= 500',
    'mailtoFallback(payload)',
    'setState("success", text.sent)',
    'source: window.location.href',
]

missing = [needle for needle in required if needle not in js]
if missing:
    raise SystemExit("Missing form hardening contracts:\n- " + "\n- ".join(missing))

if js.count('form.addEventListener("submit"') != 1:
    raise SystemExit("Expected exactly one form submit handler")
if 'formEndpoint: ""' not in config or 'formMode: "mailto"' not in config:
    raise SystemExit("Endpoint must remain disabled until the approved provider URL is supplied")
if 'noindex, nofollow' not in (ROOT / "index.html").read_text(encoding="utf-8"):
    raise SystemExit("Indexing gate changed unexpectedly")
if 'noindex, nofollow' not in (ROOT / "ru/index.html").read_text(encoding="utf-8"):
    raise SystemExit("RU indexing gate changed unexpectedly")

print("Production form hardening validation: OK")
