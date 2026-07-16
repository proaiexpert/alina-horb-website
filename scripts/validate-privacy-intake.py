#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_EMAIL = "hello@alinahorb.com"
OLD_EMAIL = "alinahorb1991@gmail.com"
FORM_ENDPOINT = "https://formspree.io/f/mvzezana"
TURNSTILE_SITE_KEY = "0x4AAAAAAD2wlldaSXK8Bp9f"


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
        '<meta name="robots" content="noindex, nofollow">',
        'href="assets/css/site.privacy.v3-2.css"',
        'href="assets/css/site.intake.v3-2.css"',
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
        '<meta name="robots" content="noindex, nofollow">',
        'href="../assets/css/site.privacy.v3-2.css"',
        'href="../assets/css/site.intake.v3-2.css"',
    )
    require(
        ROOT / "privacy/index.html",
        PUBLIC_EMAIL,
        'href="https://alinahorb.com/privacy/"',
        'hreflang="ru" href="https://alinahorb.com/ru/privacy/"',
        "Неекстрений характер сайту",
        '<meta name="robots" content="noindex, nofollow">',
    )
    require(
        ROOT / "ru/privacy/index.html",
        PUBLIC_EMAIL,
        'href="https://alinahorb.com/ru/privacy/"',
        'hreflang="uk" href="https://alinahorb.com/privacy/"',
        "Неэкстренный характер сайта",
        '<meta name="robots" content="noindex, nofollow">',
    )
    require(
        ROOT / "assets/js/site.v2.js",
        PUBLIC_EMAIL,
        "elapsed < 1500",
        "[name='website']",
        'document.querySelector("#about")',
        '"cf-turnstile-response": turnstileToken',
    )
    require(
        ROOT / "assets/js/site.chrome.v3.js",
        PUBLIC_EMAIL,
        "privacyHref",
        'privacy: "Конфіденційність"',
        'privacy: "Конфиденциальность"',
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
        ROOT / "assets/js/site.chrome.v3.js",
    ]
    for path in production_files:
        text = path.read_text(encoding="utf-8")
        if OLD_EMAIL in text:
            raise AssertionError(f"Old public Gmail remains in {path.relative_to(ROOT)}")

    if ua.count('name="website"') != 1 or ru.count('name="website"') != 1:
        raise AssertionError("Expected exactly one honeypot per homepage form")
    if ua.count('href="privacy/"') < 2 or ru.count('href="privacy/"') < 2:
        raise AssertionError("Privacy link must appear in both form consent and footer")
    if 'formEndpoint: "https://formspree.io/f/mvzezana"' not in config:
        raise AssertionError("Approved Formspree endpoint must remain explicit")
    if 'turnstileSiteKey: "0x4AAAAAAD2wlldaSXK8Bp9f"' not in config:
        raise AssertionError("Approved public Turnstile site key must remain explicit")

    print("Privacy, public email, safe intake and Turnstile validation: OK")


if __name__ == "__main__":
    main()
