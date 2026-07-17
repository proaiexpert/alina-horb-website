#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed: list[str] = []


def write(path: Path, text: str) -> None:
    current = path.read_text(encoding="utf-8")
    if current == text:
        return
    path.write_text(text, encoding="utf-8")
    changed.append(path.relative_to(ROOT).as_posix())


# Keep every static RU fallback inside /ru/ using locale-relative routes.
ru_pages = [ROOT / "ru/index.html", *sorted((ROOT / "ru").glob("*/index.html")), *sorted((ROOT / "ru/notes").glob("*/index.html"))]
seen: set[Path] = set()
for path in ru_pages:
    if path in seen or not path.is_file():
        continue
    seen.add(path)
    relative = path.relative_to(ROOT)
    depth = len(relative.parent.parts)
    old_locale_home = "../" * depth + "ru/"
    new_locale_home = "../" * (depth - 1) if depth > 1 else "./"
    text = path.read_text(encoding="utf-8")
    if old_locale_home not in text:
        raise SystemExit(f"{relative.as_posix()}: generated RU locale root not found: {old_locale_home}")
    write(path, text.replace(old_locale_home, new_locale_home))


# The global validator must use the same locale-relative RU contract.
global_validator = ROOT / "scripts/validate-global-chrome-v1.py"
text = global_validator.read_text(encoding="utf-8")
old = '    locale_home = f"{root_prefix}{\'ru/\' if is_ru else \'\'}" or "./"\n'
new = '    locale_home = (("../" * max(depth - 1, 0)) or "./") if is_ru else (root_prefix or "./")\n'
if old not in text:
    raise SystemExit("global chrome validator locale-home pattern missing")
write(global_validator, text.replace(old, new))


# Interlinking ownership moved from the Notes utility runtime to global chrome.
interlinking = ROOT / "scripts/validate-interlinking-v1.py"
text = interlinking.read_text(encoding="utf-8")
old_block = '''# Shared chrome fallbacks must not point global traffic to legacy homepage anchors.
chrome = read("assets/js/site.chrome.v3.js")
require('[text.about, `${homeHref}about/`]' in chrome, "shared About route missing")
require('[text.contact, `${homeHref}consultations/#contact`]' in chrome, "shared booking route missing")
require('[text.about, `${homeHref}#about`]' not in chrome, "legacy shared About anchor remains")
require('[text.contact, `${homeHref}#contact`]' not in chrome, "legacy shared Contact anchor remains")
'''
new_block = '''# Canonical global chrome owns global routes; the Notes utility runtime only delegates.
global_chrome = read("assets/js/site.global-chrome.v1.js")
require('href: `${localeRoot}about/`' in global_chrome, "global About route missing")
require('const bookingHref = `${localeRoot}consultations/#contact`;' in global_chrome, "global booking route missing")
require('`${localeRoot}#about`' not in global_chrome, "legacy global About anchor remains")
require('`${localeRoot}#contact`' not in global_chrome, "legacy global Contact anchor remains")
chrome = read("assets/js/site.chrome.v3.js")
require('site.global-chrome.v1.js?v=20260717-chrome1' in chrome, "Notes utility runtime does not delegate to global chrome")
'''
if old_block not in text:
    raise SystemExit("interlinking ownership block missing")
write(interlinking, text.replace(old_block, new_block))


# Privacy metadata and footer routes now live in the canonical global runtime.
privacy = ROOT / "scripts/validate-privacy-intake.py"
text = privacy.read_text(encoding="utf-8")
old_runtime = '''    require(
        ROOT / "assets/js/site.chrome.v3.js",
        PUBLIC_EMAIL,
        "privacyHref",
        'privacy: "Конфіденційність"',
        'privacy: "Конфиденциальность"',
    )
'''
new_runtime = '''    require(
        ROOT / "assets/js/site.global-chrome.v1.js",
        PUBLIC_EMAIL,
        "privacyHref",
        'privacy: "Конфіденційність"',
        'privacy: "Конфиденциальность"',
    )
    require(
        ROOT / "assets/js/site.chrome.v3.js",
        'site.global-chrome.v1.js?v=20260717-chrome1',
    )
'''
if old_runtime not in text:
    raise SystemExit("privacy runtime ownership block missing")
text = text.replace(old_runtime, new_runtime)
text = text.replace(
'''        ROOT / "assets/js/site.chrome.v3.js",
    ]
''',
'''        ROOT / "assets/js/site.chrome.v3.js",
        ROOT / "assets/js/site.global-chrome.v1.js",
    ]
''')
old_count = '''    if ua.count('href="privacy/"') < 2 or ru.count('href="privacy/"') < 2:
        raise AssertionError("Privacy link must appear in both form consent and footer")
'''
new_count = '''    if ua.count('href="privacy/"') < 1 or ru.count('href="privacy/"') < 1:
        raise AssertionError("Privacy link must remain in both form-consent blocks")
    for locale, page in (("UA", ua), ("RU", ru)):
        if 'data-site-footer="canonical"' not in page or 'href="./privacy/"' not in page:
            raise AssertionError(f"{locale} canonical footer privacy route missing")
'''
if old_count not in text:
    raise SystemExit("privacy footer-count block missing")
write(privacy, text.replace(old_count, new_count))

print("Final global chrome compatibility migration applied:")
for item in changed:
    print(f"- {item}")
