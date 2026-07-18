#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_EMAIL = "hello@alinahorb.com"
OLD_EMAIL = "alinahorb1991@gmail.com"
FORM_ENDPOINT = "https://formspree.io/f/mvzezana"
TURNSTILE_SITE_KEY = "0x4AAAAAAD2wlldaSXK8Bp9f"
PUBLIC_ROBOTS = '<meta name="robots" content="index, follow, max-image-preview:large">'
PRIVATE_ROBOTS = '<meta name="robots" content="noindex, follow">'
# The public privacy pages must identify every external processor used by the production form and typography stack.


def require(path: Path, *needles: str) -> str:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise AssertionError(f"Missing {needle!r} in {path.relative_to(ROOT)}")
    return text


def main() -> None:
    ua = require(
        ROOT / "index.html",
        PUBLIC_EMAIL,
        'data-contact-form data-locale="uk"',
        'name="website"',
        'name="startedAt"',
        'maxlength="600"',
        'href="privacy/"',
        "Сайт і форма не є екстреною службою",
        PUBLIC_ROBOTS,
        'href="assets/css/site.privacy.v3-2.css"',
        'href="assets/css/site.intake.v3-2.css"',
        'href="./privacy/">Конфіденційність</a>',
        'site.navigation.v1.js?v=20260717-ux1',
    )
    ru = require(
        ROOT / "ru/index.html",
        PUBLIC_EMAIL,
        'data-contact-form data-locale="ru"',
        'name="website"',
        'name="startedAt"',
        'maxlength="600"',
        'href="privacy/"',
        "Сайт и форма не являются экстренной службой",
        PUBLIC_ROBOTS,
        'href="../assets/css/site.privacy.v3-2.css"',
        'href="../assets/css/site.intake.v3-2.css"',
        'href="./privacy/">Конфиденциальность</a>',
        'site.navigation.v1.js?v=20260717-ux1',
    )
    require(
        ROOT / "privacy/index.html",
        PUBLIC_EMAIL,
        'href="https://alinahorb.com/privacy/"',
        'hreflang="ru" href="https://alinahorb.com/ru/privacy/"',
        "Неекстрений характер сайту",
        "Formspree",
        "Cloudflare Turnstile",
        "Google Fonts",
        PRIVATE_ROBOTS,
        'data-site-footer="canonical"',
        'href="../">alinahorb.com</a>',
    )
    require(
        ROOT / "ru/privacy/index.html",
        PUBLIC_EMAIL,
        'href="https://alinahorb.com/ru/privacy/"',
        'hreflang="uk" href="https://alinahorb.com/privacy/"',
        "Неэкстренный характер сайта",
        "Formspree",
        "Cloudflare Turnstile",
        "Google Fonts",
        PRIVATE_ROBOTS,
        'data-site-footer="canonical"',
        'href="../">alinahorb.com</a>',
    )
    require(
        ROOT / "assets/js/site.v2.js",
        PUBLIC_EMAIL,
        "elapsed < 1500",
        "[name='website']",
        'document.querySelector("#about")',
        '"cf-turnstile-response": turnstileToken',
    )
    config = require(
        ROOT / "assets/js/site-config.v2.js",
        PUBLIC_EMAIL,
        FORM_ENDPOINT,
        TURNSTILE_SITE_KEY,
        'formMode: "formspree"',
    )
    require(ROOT / "assets/css/site.intake.v3-2.css", ".form-honeypot", ".form-guidance", ".form-consent a")
    require(ROOT / "assets/css/site.privacy.v3-2.css", ".privacy-main", ".privacy-content")

    production_files = [
        ROOT / "index.html",
        ROOT / "ru/index.html",
        ROOT / "privacy/index.html",
        ROOT / "ru/privacy/index.html",
        ROOT / "assets/js/site.v2.js",
        ROOT / "assets/js/site-config.v2.js",
        ROOT / "assets/js/site.navigation.v1.js",
    ]
    for path in production_files:
        text = path.read_text(encoding="utf-8")
        if OLD_EMAIL in text:
            raise AssertionError(f"Old public Gmail remains in {path.relative_to(ROOT)}")

    for path in (ROOT / "index.html", ROOT / "ru/index.html"):
        text = path.read_text(encoding="utf-8")
        if "noindex" in text.lower():
            raise AssertionError(f"Indexing remains blocked in {path.relative_to(ROOT)}")
    for path in (ROOT / "privacy/index.html", ROOT / "ru/privacy/index.html"):
        text = path.read_text(encoding="utf-8")
        if PRIVATE_ROBOTS not in text:
            raise AssertionError(f"Privacy indexing policy mismatch in {path.relative_to(ROOT)}")

    if ua.count('name="website"') != 1 or ru.count('name="website"') != 1:
        raise AssertionError("Expected exactly one honeypot per homepage form")
    if ua.count('href="privacy/"') < 1 or ru.count('href="privacy/"') < 1:
        raise AssertionError("Privacy link must remain in both form-consent blocks")
    if 'formEndpoint: "https://formspree.io/f/mvzezana"' not in config:
        raise AssertionError("Approved Formspree endpoint must remain explicit")
    if 'turnstileSiteKey: "0x4AAAAAAD2wlldaSXK8Bp9f"' not in config:
        raise AssertionError("Approved public Turnstile site key must remain explicit")

    print("Privacy, public email, safe intake, Turnstile and indexing validation: OK")


if __name__ == "__main__":
    main()
