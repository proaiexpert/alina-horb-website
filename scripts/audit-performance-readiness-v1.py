#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
STRICT = os.environ.get("AUDIT_STRICT") == "1"

PUBLIC_PAGES = (
    "index.html", "ru/index.html",
    "about/index.html", "ru/about/index.html",
    "consultations/index.html", "ru/consultations/index.html",
    "notes/index.html", "ru/notes/index.html",
    "notes/first-consultation/index.html", "ru/notes/first-consultation/index.html",
    "notes/how-to-start-the-conversation/index.html", "ru/notes/how-to-start-the-conversation/index.html",
    "notes/when-coping-stops-helping/index.html", "ru/notes/when-coping-stops-helping/index.html",
    "notes/stress-relocation-and-lost-support/index.html", "ru/notes/stress-relocation-and-lost-support/index.html",
)

LCP_EXPECTATIONS = {
    "index.html": (
        "assets/images/portrait/alina-horb-hero-v3-1-desktop.webp",
        "assets/images/portrait/alina-horb-hero-v3-1-mobile.webp",
    ),
    "ru/index.html": (
        "../assets/images/portrait/alina-horb-hero-v3-1-desktop.webp",
        "../assets/images/portrait/alina-horb-hero-v3-1-mobile.webp",
    ),
    "about/index.html": ("../assets/images/portrait/alina-horb-about-v3-1.webp",),
    "ru/about/index.html": ("../../assets/images/portrait/alina-horb-about-v3-1.webp",),
    "notes/index.html": ("../assets/images/notes/alina-horb-note-first-consultation-v3.webp",),
    "ru/notes/index.html": ("../../assets/images/notes/alina-horb-note-first-consultation-v3.webp",),
}

class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {k.lower(): (v or "") for k, v in attrs}
        if tag == "img":
            self.images.append(values)
        elif tag == "script" and values.get("src"):
            self.scripts.append(values)
        elif tag == "link":
            self.links.append(values)

def local_path(value: str, source: Path) -> Path | None:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    return (ROOT / clean.lstrip("/")) if clean.startswith("/") else (source.parent / clean)

critical: list[str] = []
warnings: list[str] = []
info: list[str] = []

for relative in PUBLIC_PAGES:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(text)

    # Rendering stability and eager-resource sanity.
    for image in parser.images:
        src = image.get("src", "")
        if not image.get("width") or not image.get("height"):
            critical.append(f"{relative}: image lacks explicit width/height: {src}")
        target = local_path(src, path)
        if target and target.is_file() and image.get("loading", "").lower() != "lazy":
            size = target.stat().st_size
            if size > 500_000:
                critical.append(f"{relative}: eager image exceeds 500 KB: {src} ({size} bytes)")
            elif size > 150_000:
                warnings.append(f"{relative}: eager image exceeds 150 KB: {src} ({size} bytes)")

    # Scripts must not block HTML parsing.
    for script in parser.scripts:
        if not (script.get("defer") == "" and "defer" in script or script.get("async") == "" and "async" in script or script.get("type") == "module"):
            critical.append(f"{relative}: blocking script: {script.get('src', '')}")

    # CSS/JS file-size guardrails.
    for link in parser.links:
        if "stylesheet" not in link.get("rel", "").lower().split():
            continue
        target = local_path(link.get("href", ""), path)
        if target and target.is_file() and target.stat().st_size > 100_000:
            warnings.append(f"{relative}: stylesheet exceeds 100 KB: {link.get('href')} ({target.stat().st_size} bytes)")
    for script in parser.scripts:
        target = local_path(script.get("src", ""), path)
        if target and target.is_file() and target.stat().st_size > 100_000:
            warnings.append(f"{relative}: script exceeds 100 KB: {script.get('src')} ({target.stat().st_size} bytes)")

    # Known image-led first screens must advertise their likely LCP resource.
    expected = LCP_EXPECTATIONS.get(relative)
    if expected:
        preloads = {
            link.get("href", "")
            for link in parser.links
            if "preload" in link.get("rel", "").lower().split() and link.get("as") == "image"
        }
        for href in expected:
            if href not in preloads:
                critical.append(f"{relative}: missing LCP image preload: {href}")

        high_priority = [
            image for image in parser.images
            if image.get("fetchpriority", "").lower() == "high"
        ]
        if not high_priority:
            critical.append(f"{relative}: no fetchpriority=high image for image-led first screen")
        for image in high_priority:
            if image.get("loading", "").lower() == "lazy":
                critical.append(f"{relative}: high-priority image must not be lazy-loaded: {image.get('src','')}")

    eager_bytes = 0
    eager_files: set[Path] = set()
    for image in parser.images:
        if image.get("loading", "").lower() == "lazy":
            continue
        target = local_path(image.get("src", ""), path)
        if target and target.is_file():
            eager_files.add(target.resolve())
    for link in parser.links:
        rel = set(link.get("rel", "").lower().split())
        if "stylesheet" in rel or ("preload" in rel and link.get("as") in {"image", "style", "script"}):
            target = local_path(link.get("href", ""), path)
            if target and target.is_file():
                eager_files.add(target.resolve())
    for script in parser.scripts:
        target = local_path(script.get("src", ""), path)
        if target and target.is_file():
            eager_files.add(target.resolve())
    eager_bytes = sum(p.stat().st_size for p in eager_files)
    info.append(f"{relative}: conservative local first-load inventory {eager_bytes/1024:.1f} KiB across {len(eager_files)} files")
    if eager_bytes > 2_000_000:
        critical.append(f"{relative}: conservative first-load inventory exceeds 2 MB ({eager_bytes} bytes)")
    elif eager_bytes > 1_000_000:
        warnings.append(f"{relative}: conservative first-load inventory exceeds 1 MB ({eager_bytes} bytes)")

print("Performance/CWV readiness audit V1")
print(f"Pages checked: {len(PUBLIC_PAGES)}")
print(f"Critical findings: {len(critical)}")
print(f"Warnings: {len(warnings)}")
print("")
print("Critical:")
print("\n".join(f"- {x}" for x in critical) if critical else "- none")
print("")
print("Warnings:")
print("\n".join(f"- {x}" for x in warnings) if warnings else "- none")
print("")
print("Inventory:")
print("\n".join(f"- {x}" for x in info))

if STRICT and critical:
    sys.exit(1)
