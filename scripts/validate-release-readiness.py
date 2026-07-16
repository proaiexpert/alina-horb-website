#!/usr/bin/env python3
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://alinahorb.com"
ROBOTS_META = "index, follow, max-image-preview:large"

ROUTES = [
    ("index.html", f"{BASE}/", f"{BASE}/", f"{BASE}/ru/"),
    ("ru/index.html", f"{BASE}/ru/", f"{BASE}/", f"{BASE}/ru/"),
    ("about/index.html", f"{BASE}/about/", f"{BASE}/about/", f"{BASE}/ru/about/"),
    ("ru/about/index.html", f"{BASE}/ru/about/", f"{BASE}/about/", f"{BASE}/ru/about/"),
    ("notes/index.html", f"{BASE}/notes/", f"{BASE}/notes/", f"{BASE}/ru/notes/"),
    ("ru/notes/index.html", f"{BASE}/ru/notes/", f"{BASE}/notes/", f"{BASE}/ru/notes/"),
    ("notes/first-consultation/index.html", f"{BASE}/notes/first-consultation/", f"{BASE}/notes/first-consultation/", f"{BASE}/ru/notes/first-consultation/"),
    ("ru/notes/first-consultation/index.html", f"{BASE}/ru/notes/first-consultation/", f"{BASE}/notes/first-consultation/", f"{BASE}/ru/notes/first-consultation/"),
    ("notes/how-to-start-the-conversation/index.html", f"{BASE}/notes/how-to-start-the-conversation/", f"{BASE}/notes/how-to-start-the-conversation/", f"{BASE}/ru/notes/how-to-start-the-conversation/"),
    ("ru/notes/how-to-start-the-conversation/index.html", f"{BASE}/ru/notes/how-to-start-the-conversation/", f"{BASE}/notes/how-to-start-the-conversation/", f"{BASE}/ru/notes/how-to-start-the-conversation/"),
    ("notes/when-coping-stops-helping/index.html", f"{BASE}/notes/when-coping-stops-helping/", f"{BASE}/notes/when-coping-stops-helping/", f"{BASE}/ru/notes/when-coping-stops-helping/"),
    ("ru/notes/when-coping-stops-helping/index.html", f"{BASE}/ru/notes/when-coping-stops-helping/", f"{BASE}/notes/when-coping-stops-helping/", f"{BASE}/ru/notes/when-coping-stops-helping/"),
    ("notes/stress-relocation-and-lost-support/index.html", f"{BASE}/notes/stress-relocation-and-lost-support/", f"{BASE}/notes/stress-relocation-and-lost-support/", f"{BASE}/ru/notes/stress-relocation-and-lost-support/"),
    ("ru/notes/stress-relocation-and-lost-support/index.html", f"{BASE}/ru/notes/stress-relocation-and-lost-support/", f"{BASE}/notes/stress-relocation-and-lost-support/", f"{BASE}/ru/notes/stress-relocation-and-lost-support/"),
    ("privacy/index.html", f"{BASE}/privacy/", f"{BASE}/privacy/", f"{BASE}/ru/privacy/"),
    ("ru/privacy/index.html", f"{BASE}/ru/privacy/", f"{BASE}/privacy/", f"{BASE}/ru/privacy/"),
]

ARTICLE_PATHS = {
    path for path, *_ in ROUTES
    if "notes/" in path and path not in {"notes/index.html", "ru/notes/index.html"}
}
errors = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.I | re.S))


for relative, canonical, ua_url, ru_url in ROUTES:
    path = ROOT / relative
    require(path.is_file(), f"Missing route file: {relative}")
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")

    require(count(r"<title>.*?</title>", text) == 1, f"{relative}: expected one title")
    require(count(r'<meta\s+name="description"\s+content="[^"]+"\s*/?>', text) == 1, f"{relative}: expected one meta description")
    require(text.count(f'<meta name="robots" content="{ROBOTS_META}">') == 1, f"{relative}: public indexing directive missing")
    require("noindex" not in text.lower(), f"{relative}: noindex remains after launch")
    require(text.count(f'<link rel="canonical" href="{canonical}">') == 1, f"{relative}: canonical mismatch")
    require(text.count(f'<link rel="alternate" hreflang="uk" href="{ua_url}">') == 1, f"{relative}: UA hreflang mismatch")
    require(text.count(f'<link rel="alternate" hreflang="ru" href="{ru_url}">') == 1, f"{relative}: RU hreflang mismatch")
    require(count(r"<h1\b", text) == 1, f"{relative}: expected one H1")

    ids = re.findall(r'\bid="([^"]+)"', text)
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    require(not duplicates, f"{relative}: duplicate IDs {duplicates}")
    require("financialstreamllc@gmail.com" not in text and "alinahorb1991@gmail.com" not in text, f"{relative}: legacy Gmail found")

    if relative in ARTICLE_PATHS:
        require('"@type": "Article"' in text, f"{relative}: Article schema missing")
        require('"@type": "BreadcrumbList"' in text, f"{relative}: BreadcrumbList schema missing")
        require('"@type": "Person"' in text, f"{relative}: Person author schema missing")
        require('<meta property="og:type" content="article">' in text, f"{relative}: article OG type missing")
        require(f'<meta property="og:url" content="{canonical}">' in text, f"{relative}: OG URL mismatch")
        require(count(r'<meta\s+property="og:image"\s+content="https://alinahorb\.com/[^"]+"\s*/?>', text) == 1, f"{relative}: OG image missing")
        require(count(r'<meta\s+property="og:image:width"\s+content="\d+"\s*/?>', text) == 1, f"{relative}: OG image width missing")
        require(count(r'<meta\s+property="og:image:height"\s+content="\d+"\s*/?>', text) == 1, f"{relative}: OG image height missing")

for home in (ROOT / "index.html", ROOT / "ru/index.html"):
    if home.is_file():
        text = home.read_text(encoding="utf-8")
        for css_name in (
            "site.v3-1.css",
            "site.v3-1-stability.css",
            "site.footer.v3-2.css",
            "site.privacy.v3-2.css",
            "site.intake.v3-2.css",
            "site.notes-hub.v3-2.css",
        ):
            require(css_name in text, f"{home.relative_to(ROOT)}: explicit stylesheet missing: {css_name}")
        require("favicon-ag.svg" in text, f"{home.relative_to(ROOT)}: SVG favicon missing")
        require('"@type": "WebSite"' in text, f"{home.relative_to(ROOT)}: WebSite schema missing")
        require('"@type": "Person"' in text, f"{home.relative_to(ROOT)}: Person schema missing")

for css_relative in ("assets/css/site.v2.css", "assets/css/site.v3-1.css"):
    css = (ROOT / css_relative).read_text(encoding="utf-8")
    require(":focus-visible" in css and "outline:" in css, f"{css_relative}: visible focus rule missing")
    require(".skip-link:focus" in css and "translateY(0)" in css, f"{css_relative}: skip-link focus reveal missing")

config = (ROOT / "assets/js/site-config.v2.js").read_text(encoding="utf-8")
require("appendStylesheet" not in config and 'createElement("link")' not in config, "site-config: runtime CSS/favicon injection remains")
require('formEndpoint: "https://formspree.io/f/mvzezana"' in config, "site-config: approved Formspree endpoint missing")
require('formMode: "formspree"' in config, "site-config: production form mode missing")
require('turnstileSiteKey: "0x4AAAAAAD2wlldaSXK8Bp9f"' in config, "site-config: approved Turnstile site key missing")
require('email: "hello@alinahorb.com"' in config, "site-config: public email mismatch")

sitemap_path = ROOT / "sitemap.xml"
require(sitemap_path.is_file(), "sitemap.xml missing")
if sitemap_path.is_file():
    root = ET.parse(sitemap_path).getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [node.text for node in root.findall("sm:url/sm:loc", namespace)]
    expected = [canonical for _, canonical, _, _ in ROUTES]
    require(locations == expected, f"sitemap route/order mismatch: {locations}")
    require(len(locations) == len(set(locations)) == len(expected), "sitemap duplicates or missing URLs")

robots_path = ROOT / "robots.txt"
require(robots_path.is_file(), "robots.txt missing")
if robots_path.is_file():
    robots = robots_path.read_text(encoding="utf-8")
    require("User-agent: *" in robots, "robots.txt user-agent missing")
    require("Allow: /" in robots, "robots.txt allow policy missing")
    require(f"Sitemap: {BASE}/sitemap.xml" in robots, "robots.txt sitemap directive missing")
    require("Disallow:" not in robots, "robots.txt contains a blocking directive")

workflow = (ROOT / ".github/workflows/deploy-pages.yml").read_text(encoding="utf-8")
require("python3 scripts/apply-turnstile-v3-2.py" in workflow, "Turnstile runtime builder not wired into deployment")
require("python3 scripts/apply-indexing-launch-v3-2.py" in workflow, "indexing launch step not wired into deployment")
require("python3 scripts/validate-release-readiness.py" in workflow, "deployment validator not wired")
require("cp sitemap.xml _site/" in workflow and "cp robots.txt _site/" in workflow, "deployment does not copy sitemap/robots")
require("test -f _site/sitemap.xml" in workflow and "test -f _site/robots.txt" in workflow, "deployment does not assert sitemap/robots")

if errors:
    print("Release readiness validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"Release readiness validation passed for {len(ROUTES)} publicly indexable routes")
