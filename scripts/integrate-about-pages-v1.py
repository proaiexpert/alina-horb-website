#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{relative}: expected one integration marker, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# Link the existing homepage biography blocks to the new full profile pages.
replace_once(
    "index.html",
    "</blockquote>\n        </div>\n      </div>\n    </section>\n\n    <section class=\"education-section",
    "</blockquote>\n          <a class=\"text-link\" href=\"about/\">Докладніше про професійний шлях</a>\n        </div>\n      </div>\n    </section>\n\n    <section class=\"education-section",
)
replace_once(
    "ru/index.html",
    "</blockquote></div></div></section>\n\n    <section class=\"education-section",
    "</blockquote><a class=\"text-link\" href=\"about/\">Подробнее о профессиональном пути</a></div></div></section>\n\n    <section class=\"education-section",
)

# Add discoverable footer links from both homepages.
replace_once(
    "index.html",
    '<div class="language-switch"><span aria-current="page">UA</span><span>/</span><a href="./ru/" lang="ru" hreflang="ru">RU</a></div>\n        <a href="mailto:hello@alinahorb.com">Email</a>',
    '<div class="language-switch"><span aria-current="page">UA</span><span>/</span><a href="./ru/" lang="ru" hreflang="ru">RU</a></div>\n        <a href="about/">Про Аліну</a>\n        <a href="mailto:hello@alinahorb.com">Email</a>',
)
replace_once(
    "ru/index.html",
    '<div class="language-switch"><a href="../" lang="uk" hreflang="uk">UA</a><span>/</span><span aria-current="page">RU</span></div><a href="mailto:hello@alinahorb.com">Email</a>',
    '<div class="language-switch"><a href="../" lang="uk" hreflang="uk">UA</a><span>/</span><span aria-current="page">RU</span></div><a href="about/">Об Алине</a><a href="mailto:hello@alinahorb.com">Email</a>',
)

# Sitemap order must match the production route contract.
replace_once(
    "sitemap.xml",
    '  <url><loc>https://alinahorb.com/ru/</loc><lastmod>2026-07-15</lastmod></url>\n',
    '  <url><loc>https://alinahorb.com/ru/</loc><lastmod>2026-07-15</lastmod></url>\n  <url><loc>https://alinahorb.com/about/</loc><lastmod>2026-07-16</lastmod></url>\n  <url><loc>https://alinahorb.com/ru/about/</loc><lastmod>2026-07-16</lastmod></url>\n',
)

# Production transforms and favicon normalization must cover both new routes.
for relative in (
    "scripts/apply-indexing-launch-v3-2.py",
    "scripts/apply-social-favicon-v3-3.py",
    "scripts/validate-favicon-social-v3-3.py",
):
    replace_once(
        relative,
        '    "ru/index.html",\n',
        '    "ru/index.html",\n    "about/index.html",\n    "ru/about/index.html",\n',
    )

# Release validation: canonical and reciprocal language mapping for all 16 routes.
replace_once(
    "scripts/validate-release-readiness.py",
    '    ("ru/index.html", f"{BASE}/ru/", f"{BASE}/", f"{BASE}/ru/"),\n',
    '    ("ru/index.html", f"{BASE}/ru/", f"{BASE}/", f"{BASE}/ru/"),\n    ("about/index.html", f"{BASE}/about/", f"{BASE}/about/", f"{BASE}/ru/about/"),\n    ("ru/about/index.html", f"{BASE}/ru/about/", f"{BASE}/about/", f"{BASE}/ru/about/"),\n',
)

# GitHub Pages deployment and artifact assertions.
replace_once(
    ".github/workflows/deploy-pages.yml",
    "          python3 scripts/validate-assets.py\n",
    "          python3 scripts/validate-assets.py\n          python3 scripts/validate-about-pages-v1.py\n",
)
replace_once(
    ".github/workflows/deploy-pages.yml",
    "          cp -R assets _site/\n          cp -R notes _site/\n",
    "          cp -R assets _site/\n          cp -R about _site/\n          cp -R notes _site/\n",
)
replace_once(
    ".github/workflows/deploy-pages.yml",
    "          test -f _site/assets/css/site.notes-hub.v3-2.css\n",
    "          test -f _site/assets/css/site.notes-hub.v3-2.css\n          test -f _site/assets/css/site.about.v1.css\n",
)
replace_once(
    ".github/workflows/deploy-pages.yml",
    "          test -f _site/notes/index.html\n",
    "          test -f _site/about/index.html\n          test -f _site/notes/index.html\n",
)
replace_once(
    ".github/workflows/deploy-pages.yml",
    "          test -f _site/ru/index.html\n",
    "          test -f _site/ru/index.html\n          test -f _site/ru/about/index.html\n",
)
replace_once(
    ".github/workflows/deploy-pages.yml",
    "          grep -q 'content=\"index, follow, max-image-preview:large\"' _site/ru/index.html\n",
    "          grep -q 'content=\"index, follow, max-image-preview:large\"' _site/ru/index.html\n          grep -q 'content=\"index, follow, max-image-preview:large\"' _site/about/index.html\n          grep -q 'content=\"index, follow, max-image-preview:large\"' _site/ru/about/index.html\n",
)

print("Integrated bilingual About pages into navigation, sitemap, transforms, validation and deployment")
