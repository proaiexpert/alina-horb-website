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
    'providerPayloadFrom(payload)',
    'showSuccessConfirmation();',
    'form.hidden = true;',
    'successPanel.hidden = false;',
    'subject: text.subject',
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

for forbidden in ('source: window.location.href', 'data.get("language")', 'data.get("format")', 'locale, subject'):
    if forbidden in js:
        raise SystemExit(f"Noisy form payload remains: {forbidden}")

if js.count('form.addEventListener("submit"') != 1:
    raise SystemExit("Expected exactly one form submit handler")
if 'formEndpoint: "https://formspree.io/f/mvzezana"' not in config:
    raise SystemExit("Approved Formspree endpoint is not configured")
if 'formMode: "formspree"' not in config:
    raise SystemExit("Production form mode is not enabled")
if 'turnstileSiteKey: "0x4AAAAAAD2wlldaSXK8Bp9f"' not in config:
    raise SystemExit("Approved public Turnstile site key is not configured")

for relative in ("index.html", "ru/index.html", "consultations/index.html", "ru/consultations/index.html"):
    html = (ROOT / relative).read_text(encoding="utf-8")
    if 'data-form-success' not in html:
        raise SystemExit(f"{relative}: visible success confirmation missing")
    if 'name="language"' in html:
        raise SystemExit(f"{relative}: redundant language field remains")
    if html.count('field-required') < 3 or html.count('field-optional') < 4:
        raise SystemExit(f"{relative}: required/optional field labels are incomplete")

for relative in ("index.html", "ru/index.html"):
    html = (ROOT / relative).read_text(encoding="utf-8")
    if robots_meta not in html or "noindex" in html.lower():
        raise SystemExit(f"{relative}: public indexing directive is not active")

print("Production Formspree, compact email payload, confirmation UX and Turnstile integration: OK")
