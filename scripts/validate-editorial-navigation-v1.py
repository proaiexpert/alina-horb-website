#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


css_path = ROOT / "assets/css/site.navigation.v1.css"
js_path = ROOT / "assets/js/site.navigation.v1.js"

require(css_path.is_file(), "navigation stylesheet is missing")
require(js_path.is_file(), "navigation runtime is missing")

css = css_path.read_text(encoding="utf-8")
js = js_path.read_text(encoding="utf-8")

for token in (
    ".editorial-rail",
    ".rail-page-link",
    ".rail-booking-link",
    ".rail-local-link",
    ".editorial-mobile-menu:not([hidden])",
    ".editorial-mobile-page",
    ".editorial-mobile-booking",
    "@media (max-width: 1180px)",
    "--editorial-header-height",
    "body.editorial-menu-open .mobile-booking-cta",
    "prefers-reduced-motion",
):
    require(token in css, f"navigation CSS missing: {token}")

for token in (
    "Разделы сайта",
    "Розділи сайту",
    "Материалы",
    "Матеріали",
    "Содержание",
    "Зміст",
    "consultations/#contact",
    "fallbackDesktopNav",
    "setBackgroundInert",
    "lockPage",
    "MutationObserver",
    "IntersectionObserver",
    'event.key === "Tab"',
    'event.key === "Escape"',
    'matchMedia("(max-width: 1180px)")',
):
    require(token in js, f"navigation runtime missing: {token}")

print("Editorial navigation production validation passed.")
