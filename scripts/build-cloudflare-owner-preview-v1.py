#!/usr/bin/env python3
"""TASK 045: build an isolated, noindex Cloudflare Pages artifact.

This NEVER deploys, modifies main or production, changes the accepted content,
or reads Cloudflare credentials. Publish only via a separate Pages project.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "cloudflare-owner-preview-dist"
BRANCH = "agent/alina-article02-bilingual-premium-v21-r1"
REPO = "proaiexpert/alina-horb-website"
DIRS = ("assets", "about", "consultations", "notes", "privacy", "ru")
FILES = ("index.html", "404.html", "favicon.svg", "favicon.ico",
         "favicon-16x16.png", "favicon-32x32.png")
NOINDEX = "noindex, nofollow, noarchive"
HERO_SHA256 = "ccbca2d604acab73f840d8dada91c31a66bb036842e26d42577e70bed7e3bb17"
REQUIRED = (
    "index.html",
    "notes/fear-of-another-panic-attack/index.html",
    "ru/notes/fear-of-another-panic-attack/index.html",
    "assets/css/site.article.panic.v1.css",
    "assets/js/site.navigation.v1.js",
    "assets/js/site.article.reading.v2.js",
    "assets/images/notes/alina-horb-article02-hero-4x3.webp",
    "assets/images/notes/alina-horb-article02-home-card-800x500.webp",
    "assets/images/notes/alina-horb-article02-notes-card-800x600.webp",
    "assets/images/social/alina-horb-article02-og.png",
    "notes/index.html",
    "ru/index.html",
    "ru/notes/index.html",
)
META = re.compile(r'(<meta\s+name="robots"\s+content=")[^"]*(")', re.I)
HEAD = re.compile(r"<head(?:\s[^>]*)?>", re.I)

def fail(msg):
    raise SystemExit("TASK045 PREVIEW BUILD FAILED: " + msg)

def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    branch = os.getenv("CF_PAGES_BRANCH", BRANCH)
    if branch != BRANCH:
        fail("Refusing to build branch " + repr(branch) + "; only " + BRANCH)
    # GitHub CI uses PREVIEW_SOURCE_SHA, Cloudflare Pages uses CF_PAGES_COMMIT_SHA.
    cf_sha = os.getenv("CF_PAGES_COMMIT_SHA", "")
    ci_sha = os.getenv("PREVIEW_SOURCE_SHA", "")
    if cf_sha and ci_sha and cf_sha != ci_sha:
        fail("Commit identities disagree")
    commit_sha = cf_sha or ci_sha
    if not re.fullmatch(r"[0-9a-f]{40}", commit_sha):
        fail("Missing verified 40-character source commit SHA")
    original = ROOT / "assets/images/notes/alina-horb-article02-hero-4x3.webp"
    if not original.is_file() or file_sha256(original) != HERO_SHA256:
        fail("Approved Hero source hash mismatch")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name in FILES:
        src = ROOT / name
        if not src.is_file():
            fail("Missing static entrypoint " + name)
        shutil.copy2(src, OUT / name)
    for name in DIRS:
        src = ROOT / name
        if not src.is_dir():
            fail("Missing static directory " + name)
        shutil.copytree(src, OUT / name)
    # No source-side robots, sitemap or production build configuration is copied.
    # Add defense-in-depth noindex META in output-only HTML, not in accepted source.
    count = 0
    for html in OUT.rglob("*.html"):
        source = html.read_text(encoding="utf-8")
        replaced, n = META.subn(lambda m: m.group(1) + NOINDEX + m.group(2), source)
        if n == 0:
            if not HEAD.search(replaced):
                fail("HTML without head: " + str(html.relative_to(OUT)))
            replaced = HEAD.sub(lambda m: m.group(0) + '\n<meta name="robots" content="' + NOINDEX + '">', replaced, count=1)
        if not re.search(r'<meta\s+name="robots"\s+content="noindex, nofollow, noarchive"', replaced, re.I):
            fail("HTML missing noindex: " + str(html.relative_to(OUT)))
        html.write_text(replaced, encoding="utf-8")
        count += 1
    (OUT / "_headers").write_text(
        "/*\n"
        "  X-Robots-Tag: noindex, nofollow, noarchive\n"
        "  X-Content-Type-Options: nosniff\n",
        encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (OUT / "preview-build-info.json").write_text(
        json.dumps({"repository": REPO, "commit_sha": commit_sha, "branch": branch,
                    "mode": "isolated-cloudflare-pages-noindex"},
                   indent=2) + "\n", encoding="utf-8")
    for relative in REQUIRED:
        if not (OUT / relative).is_file():
            fail("Preview missing: " + relative)
    # Verify both languages and companion cards against exact checked-in assets.
    for lang, path in (("UA", "notes/fear-of-another-panic-attack/index.html"),
                       ("RU", "ru/notes/fear-of-another-panic-attack/index.html")):
        html = (OUT / path).read_text(encoding="utf-8")
        if "alina-horb-article02-hero-4x3.webp" not in html:
            fail(lang + " Hero does not reference approved WebP")
    for relative, card in (
        ("index.html", "alina-horb-article02-home-card-800x500.webp"),
        ("ru/index.html", "alina-horb-article02-home-card-800x500.webp"),
        ("notes/index.html", "alina-horb-article02-notes-card-800x600.webp"),
        ("ru/notes/index.html", "alina-horb-article02-notes-card-800x600.webp"),
    ):
        if card not in (OUT / relative).read_text(encoding="utf-8"):
            fail("Wrong article card at " + relative)
    print(json.dumps({"status": "PASS", "source_commit": commit_sha, "branch": branch,
                      "html_noindex": count, "required_assets": len(REQUIRED),
                      "output_dir": OUT.name, "headers": NOINDEX}, indent=2))

if __name__ == "__main__":
    main()
