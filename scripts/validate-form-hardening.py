#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
js = (ROOT / "assets/js/site.v2.js").read_text(encoding="utf-8")
config = (ROOT / "assets/js/site-config.v2.js").read_text(encoding="utf-8")
robots_meta = '<meta name="robots" content="index, follow, max-image-preview:large">'

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
    'const turnstileSiteKey = String(config.turnstileSiteKey || "").trim();',
    'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit',
    '"cf-turnstile-response": turnstileToken',
    'window.turnstile.render',
    'resetTurnstile();',
    'text.verification',
]

missing = [needle for needle in required if needle not in js]
if missing:
    raise SystemExit("Missing form hardening contracts:\n- " + "\n- ".join(missing))

if js.count('form.addEventListener("submit"') != 1:
    raise SystemExit("Expected exactly one form submit handler")
if 'formEndpoint: "https://formspree.io/f/mvzezana"' not in config:
    raise SystemExit("Approved Formspree endpoint is not configured")
if 'formMode: "formspree"' not in config:
    raise SystemExit("Production form mode is not enabled")
if 'turnstileSiteKey: "0x4AAAAAAD2wlldaSXK8Bp9f"' not in config:
    raise SystemExit("Approved public Turnstile site key is not configured")

for relative in ("index.html", "ru/index.html"):
    html = (ROOT / relative).read_text(encoding="utf-8")
    if robots_meta not in html or "noindex" in html.lower():
        raise SystemExit(f"{relative}: public indexing directive is not active")

print("Production Formspree and Cloudflare Turnstile integration: OK; indexing enabled")
