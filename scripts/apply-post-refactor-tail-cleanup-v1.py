#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REMOVE = [
    "assets/js/site.global-chrome.v1.js",
    "assets/js/site.chrome.v3.js",
    "assets/js/site.notes-images.v3-1.js",
    "assets/css/site.footer.v3-2.css",
    "assets/css/site.chrome.v3.css",
    "assets/images/notes/alina-horb-notes-editorial-v2.webp",
    "assets/images/portrait/alina-horb-portrait-hero-v3.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-desktop.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-desktop.webp",
    "assets/images/portrait/alina-horb-portrait-v4-mobile.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-mobile.webp",
]

WORKFLOWS = [
    ".github/workflows/deploy-pages.yml",
    ".github/workflows/qa-about-pages-v1.yml",
    ".github/workflows/qa-editorial-navigation-v1.yml",
    ".github/workflows/qa-global-chrome-v1.yml",
    ".github/workflows/qa-interlinking-v1.yml",
    ".github/workflows/qa-notes-images-v3.yml",
]

LEGACY_BASENAMES = {
    "site.global-chrome.v1.js",
    "site.chrome.v3.js",
    "site.notes-images.v3-1.js",
}

for relative in REMOVE:
    path = ROOT / relative
    if path.exists():
        path.unlink()
        print(f"removed {relative}")

for relative in WORKFLOWS:
    path = ROOT / relative
    if not path.is_file():
        continue
    lines = path.read_text(encoding="utf-8").splitlines()
    filtered = [line for line in lines if not any(name in line for name in LEGACY_BASENAMES)]
    path.write_text("\n".join(filtered) + "\n", encoding="utf-8")
    print(f"cleaned {relative}")

validator = ROOT / "scripts/validate-global-chrome-v1.py"
text = validator.read_text(encoding="utf-8")
obsolete_block = '''utility = (ROOT / "assets/js/site.chrome.v3.js").read_text(encoding="utf-8")
require("__ALINA_STATIC_UTILITY_CHROME_V1__" in utility, "utility compatibility marker missing")
require("innerHTML" not in utility and "appendStylesheet" not in utility, "utility runtime still mutates page chrome")

'''
if obsolete_block not in text:
    raise SystemExit("obsolete utility validator block was not found")
validator.write_text(text.replace(obsolete_block, "", 1), encoding="utf-8")
print("cleaned scripts/validate-global-chrome-v1.py")

audit = ROOT / "scripts/audit-post-refactor-tails-v1.py"
text = audit.read_text(encoding="utf-8")
text = text.replace("import subprocess\nimport sys\n", "import subprocess\nimport sys\nimport time\n", 1)
text = text.replace(
'''STALE_ASSET_CANDIDATES = [
    "assets/js/site.global-chrome.v1.js",
    "assets/js/site.chrome.v3.js",
    "assets/js/site.notes-images.v3-1.js",
    "assets/css/site.footer.v3-2.css",
]''',
'''STALE_ASSET_CANDIDATES = [
    "assets/js/site.global-chrome.v1.js",
    "assets/js/site.chrome.v3.js",
    "assets/js/site.notes-images.v3-1.js",
    "assets/css/site.footer.v3-2.css",
    "assets/css/site.chrome.v3.css",
    "assets/images/notes/alina-horb-notes-editorial-v2.webp",
    "assets/images/portrait/alina-horb-portrait-hero-v3.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-desktop.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-desktop.webp",
    "assets/images/portrait/alina-horb-portrait-v4-mobile.jpg",
    "assets/images/portrait/alina-horb-portrait-v4-mobile.webp",
]''',
1,
)
old_fetch = '''def fetch(url: str, timeout: int = 30) -> tuple[dict, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "AlinaHorbTailAudit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(2_000_000)
            text = body.decode("utf-8", errors="replace")
            return ({
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "final_url": response.geturl(),
                "content_type": response.headers.get("content-type", ""),
                "bytes": len(body),
            }, text)
    except urllib.error.HTTPError as error:
        return ({"ok": False, "status": error.code, "final_url": error.geturl(), "error": str(error)}, "")
    except Exception as error:  # noqa: BLE001
        return ({"ok": False, "status": None, "final_url": None, "error": str(error)}, "")
'''
new_fetch = '''def fetch(url: str, timeout: int = 30) -> tuple[dict, str]:
    last: tuple[dict, str] | None = None
    for attempt in range(3):
        request = urllib.request.Request(url, headers={"User-Agent": "AlinaHorbTailAudit/1.1"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read(2_000_000)
                text = body.decode("utf-8", errors="replace")
                return ({
                    "ok": 200 <= response.status < 400,
                    "status": response.status,
                    "final_url": response.geturl(),
                    "content_type": response.headers.get("content-type", ""),
                    "bytes": len(body),
                }, text)
        except urllib.error.HTTPError as error:
            last = ({"ok": False, "status": error.code, "final_url": error.geturl(), "error": str(error)}, "")
            if error.code not in {429, 500, 502, 503, 504}:
                return last
        except Exception as error:  # noqa: BLE001
            last = ({"ok": False, "status": None, "final_url": None, "error": str(error)}, "")
        if attempt < 2:
            time.sleep(1.5 * (attempt + 1))
    return last or ({"ok": False, "status": None, "final_url": None, "error": "unknown fetch failure"}, "")
'''
if old_fetch not in text:
    raise SystemExit("fetch function patch point missing")
text = text.replace(old_fetch, new_fetch, 1)
text = text.replace(
'''            production_refs = [
                line for line in refs
                if line.split(":", 1)[0].endswith(".html")
            ]
            if not production_refs:
                add_issue(warnings, "stale-asset", "Tracked legacy asset has no production HTML reference", candidate)
''',
'''            add_issue(critical, "stale-asset", "Obsolete post-refactor asset is still tracked", candidate)
''',
1,
)
text = text.replace(
'''        if route in {"/consultations/", "/ru/consultations/"}:
            if "challenges.cloudflare.com/turnstile" not in body:
                add_issue(critical, "live-form", "Turnstile API is absent from consultation page", route)
            if "formspree.io/f/mvzezana" not in body and "site-config.v2.js" not in body:
                add_issue(critical, "live-form", "Production form configuration is absent", route)
''',
'''        if route in {"/consultations/", "/ru/consultations/"} and "site-config.v2.js" not in body:
            add_issue(critical, "live-form", "Production form configuration script is absent", route)
''',
1,
)
needle = '''    broken_live_assets: list[dict] = []
'''
insertion = '''    config_meta, config_body = fetch(f"{LIVE_ORIGIN}/assets/js/site-config.v2.js")
    runtime_meta, runtime_body = fetch(f"{LIVE_ORIGIN}/assets/js/site.v2.js")
    if not config_meta.get("ok") or "https://formspree.io/f/mvzezana" not in config_body or "0x4AAAAAAD2wlldaSXK8Bp9f" not in config_body:
        add_issue(critical, "live-form", "Production Formspree or Turnstile configuration is missing")
    if not runtime_meta.get("ok") or "challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" not in runtime_body or "cf-turnstile-response" not in runtime_body:
        add_issue(critical, "live-form", "Production Turnstile runtime is missing")

    broken_live_assets: list[dict] = []
'''
if needle not in text:
    raise SystemExit("live asset insertion point missing")
text = text.replace(needle, insertion, 1)
audit.write_text(text, encoding="utf-8")
print("strengthened scripts/audit-post-refactor-tails-v1.py")

# Remove one-time cleanup machinery from the branch before committing the result.
for relative in (
    "scripts/apply-post-refactor-tail-cleanup-v1.py",
    ".github/workflows/apply-post-refactor-tail-cleanup-v1.yml",
):
    path = ROOT / relative
    if path.exists():
        path.unlink()
        print(f"removed one-time machinery {relative}")
