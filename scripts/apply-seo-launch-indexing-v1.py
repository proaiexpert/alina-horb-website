#!/usr/bin/env python3
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = 'index, follow, max-image-preview:large'
PRIVATE = 'noindex, follow'

INDEXABLE_PATHS = [
    'index.html', 'ru/index.html',
    'about/index.html', 'ru/about/index.html',
    'consultations/index.html', 'ru/consultations/index.html',
    'notes/index.html', 'ru/notes/index.html',
    'notes/first-consultation/index.html', 'ru/notes/first-consultation/index.html',
    'notes/how-to-start-the-conversation/index.html', 'ru/notes/how-to-start-the-conversation/index.html',
    'notes/when-coping-stops-helping/index.html', 'ru/notes/when-coping-stops-helping/index.html',
    'notes/stress-relocation-and-lost-support/index.html', 'ru/notes/stress-relocation-and-lost-support/index.html',
]
PRIVACY_PATHS = ['privacy/index.html', 'ru/privacy/index.html']
ARTICLE_PATHS = [path for path in INDEXABLE_PATHS if '/notes/' in f'/{path}' and path not in {'notes/index.html', 'ru/notes/index.html'}]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding='utf-8')


def write(relative: str, text: str) -> None:
    (ROOT / relative).write_text(text, encoding='utf-8')


def replace_once(text: str, old: str, new: str, relative: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{relative}: expected exactly one occurrence of {old!r}, found {count}')
    return text.replace(old, new, 1)


# Privacy and legal pages remain crawlable but are not search-result landing pages.
for relative in PRIVACY_PATHS:
    text = read(relative)
    text = re.sub(
        r'<meta name="robots" content="(?:noindex, nofollow|index, follow, max-image-preview:large)">',
        f'<meta name="robots" content="{PRIVATE}">',
        text,
        count=1,
    )
    if text.count(f'<meta name="robots" content="{PRIVATE}">') != 1:
        raise SystemExit(f'{relative}: privacy robots policy was not applied')
    write(relative, text)


# Article social-preview MIME must match the actual WebP resource.
for relative in ARTICLE_PATHS:
    text = read(relative)
    image_match = re.search(r'<meta property="og:image" content="([^"]+)">', text)
    if not image_match or not image_match.group(1).endswith('.webp'):
        raise SystemExit(f'{relative}: expected a WebP Open Graph image')
    text = replace_once(
        text,
        '<meta property="og:image:type" content="image/jpeg">',
        '<meta property="og:image:type" content="image/webp">',
        relative,
    )
    write(relative, text)


UA_HUB_SCHEMA = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "CollectionPage",
        "@id": "https://alinahorb.com/notes/#page",
        "url": "https://alinahorb.com/notes/",
        "name": "Нотатки про психологічну підтримку — Аліна Горб",
        "description": "Редакційні матеріали Аліни Горб про першу консультацію, складний запит, самоспостереження, стрес, переїзд і відновлення опори.",
        "inLanguage": "uk",
        "isPartOf": {"@id": "https://alinahorb.com/#website"},
        "mainEntity": {"@id": "https://alinahorb.com/notes/#list"}
      },
      {
        "@type": "ItemList",
        "@id": "https://alinahorb.com/notes/#list",
        "numberOfItems": 4,
        "itemListElement": [
          {"@type":"ListItem","position":1,"name":"Що відбувається на першій консультації","url":"https://alinahorb.com/notes/first-consultation/"},
          {"@type":"ListItem","position":2,"name":"Як почати розмову, коли важко сформулювати запит","url":"https://alinahorb.com/notes/how-to-start-the-conversation/"},
          {"@type":"ListItem","position":3,"name":"Коли звичні способи справлятися більше не допомагають","url":"https://alinahorb.com/notes/when-coping-stops-helping/"},
          {"@type":"ListItem","position":4,"name":"Стрес, переїзд і втрата звичної опори","url":"https://alinahorb.com/notes/stress-relocation-and-lost-support/"}
        ]
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          {"@type":"ListItem","position":1,"name":"Головна","item":"https://alinahorb.com/"},
          {"@type":"ListItem","position":2,"name":"Нотатки","item":"https://alinahorb.com/notes/"}
        ]
      }
    ]
  }
  </script>
'''

RU_HUB_SCHEMA = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "CollectionPage",
        "@id": "https://alinahorb.com/ru/notes/#page",
        "url": "https://alinahorb.com/ru/notes/",
        "name": "Заметки о психологической поддержке — Алина Горб",
        "description": "Редакционные материалы Алины Горб о первой консультации, сложном запросе, самонаблюдении, стрессе, переезде и восстановлении опоры.",
        "inLanguage": "ru",
        "isPartOf": {"@id": "https://alinahorb.com/#website"},
        "mainEntity": {"@id": "https://alinahorb.com/ru/notes/#list"}
      },
      {
        "@type": "ItemList",
        "@id": "https://alinahorb.com/ru/notes/#list",
        "numberOfItems": 4,
        "itemListElement": [
          {"@type":"ListItem","position":1,"name":"Что происходит на первой консультации","url":"https://alinahorb.com/ru/notes/first-consultation/"},
          {"@type":"ListItem","position":2,"name":"Как начать разговор, когда трудно сформулировать запрос","url":"https://alinahorb.com/ru/notes/how-to-start-the-conversation/"},
          {"@type":"ListItem","position":3,"name":"Когда привычные способы справляться больше не помогают","url":"https://alinahorb.com/ru/notes/when-coping-stops-helping/"},
          {"@type":"ListItem","position":4,"name":"Стресс, переезд и потеря привычной опоры","url":"https://alinahorb.com/ru/notes/stress-relocation-and-lost-support/"}
        ]
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          {"@type":"ListItem","position":1,"name":"Главная","item":"https://alinahorb.com/ru/"},
          {"@type":"ListItem","position":2,"name":"Заметки","item":"https://alinahorb.com/ru/notes/"}
        ]
      }
    ]
  }
  </script>
'''

for relative, schema in [('notes/index.html', UA_HUB_SCHEMA), ('ru/notes/index.html', RU_HUB_SCHEMA)]:
    text = read(relative)
    og_image = re.search(r'(<meta property="og:image" content="([^"]+)">)', text)
    if not og_image or not og_image.group(2).endswith('.webp'):
        raise SystemExit(f'{relative}: expected Notes hub WebP OG image')
    if 'og:image:secure_url' not in text:
        insertion = (
            og_image.group(1)
            + f'\n  <meta property="og:image:secure_url" content="{og_image.group(2)}">'
            + '\n  <meta property="og:image:type" content="image/webp">'
        )
        text = text.replace(og_image.group(1), insertion, 1)
    if 'type="application/ld+json"' not in text:
        marker = '  <link rel="icon" type="image/svg+xml"'
        if marker not in text:
            raise SystemExit(f'{relative}: favicon marker missing for schema insertion')
        text = text.replace(marker, schema + marker, 1)
    write(relative, text)


# Remove one Ukrainian phrase that leaked into the Russian Notes hub.
relative = 'ru/notes/index.html'
text = read(relative)
text = text.replace(
    'Как начать разговор, коли важко сформулювати запит',
    'Как начать разговор, когда трудно сформулировать запрос',
)
if 'коли важко сформулювати запит' in text:
    raise SystemExit('ru/notes/index.html: Ukrainian phrase remains')
write(relative, text)


# Sitemap contains only canonical URLs intended to appear in search results.
sitemap = ROOT / 'sitemap.xml'
tree = ET.parse(sitemap)
root = tree.getroot()
namespace = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
privacy_urls = {'https://alinahorb.com/privacy/', 'https://alinahorb.com/ru/privacy/'}
for node in list(root.findall('sm:url', namespace)):
    loc = node.find('sm:loc', namespace)
    if loc is not None and loc.text in privacy_urls:
        root.remove(node)
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
tree.write(sitemap, encoding='UTF-8', xml_declaration=True)


# Production indexing builder: 16 search landing pages, 2 crawlable legal pages.
apply_indexing = '''#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INDEXABLE = [
    "index.html", "ru/index.html", "about/index.html", "ru/about/index.html",
    "consultations/index.html", "ru/consultations/index.html", "notes/index.html", "ru/notes/index.html",
    "notes/first-consultation/index.html", "ru/notes/first-consultation/index.html",
    "notes/how-to-start-the-conversation/index.html", "ru/notes/how-to-start-the-conversation/index.html",
    "notes/when-coping-stops-helping/index.html", "ru/notes/when-coping-stops-helping/index.html",
    "notes/stress-relocation-and-lost-support/index.html", "ru/notes/stress-relocation-and-lost-support/index.html",
]
PRIVATE = ["privacy/index.html", "ru/privacy/index.html"]
SOURCE = '<meta name="robots" content="noindex, nofollow">'
PUBLIC = '<meta name="robots" content="index, follow, max-image-preview:large">'
PRIVATE_META = '<meta name="robots" content="noindex, follow">'

for relative in INDEXABLE:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Missing public route: {relative}")
    text = path.read_text(encoding="utf-8")
    if SOURCE in text and PUBLIC not in text:
        text = text.replace(SOURCE, PUBLIC, 1)
    if text.count(PUBLIC) != 1 or "noindex" in text.lower():
        raise SystemExit(f"{relative}: public indexing directive was not applied")
    path.write_text(text, encoding="utf-8")

for relative in PRIVATE:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"Missing privacy route: {relative}")
    text = path.read_text(encoding="utf-8")
    text = text.replace(SOURCE, PRIVATE_META, 1).replace(PUBLIC, PRIVATE_META, 1)
    if text.count(PRIVATE_META) != 1:
        raise SystemExit(f"{relative}: privacy noindex policy was not applied")
    path.write_text(text, encoding="utf-8")

print(f"Production indexing enabled for {len(INDEXABLE)} search routes; {len(PRIVATE)} privacy routes remain noindex, follow")
'''
write('scripts/apply-indexing-launch-v3-2.py', apply_indexing)


# Release validator indexing and sitemap contract.
relative = 'scripts/validate-release-readiness.py'
text = read(relative)
text = replace_once(text, 'ROBOTS_META = "index, follow, max-image-preview:large"', 'PUBLIC_ROBOTS = "index, follow, max-image-preview:large"\nPRIVATE_ROBOTS = "noindex, follow"', relative)
text = text.replace(
    'ARTICLE_PATHS = {path for path, *_ in ROUTES if "notes/" in path and path not in {"notes/index.html", "ru/notes/index.html"}}',
    'ARTICLE_PATHS = {path for path, *_ in ROUTES if "notes/" in path and path not in {"notes/index.html", "ru/notes/index.html"}}\nPRIVACY_PATHS = {"privacy/index.html", "ru/privacy/index.html"}\nINDEXABLE_PATHS = {path for path, *_ in ROUTES} - PRIVACY_PATHS',
)
old = '''    require(text.count(f'<meta name="robots" content="{ROBOTS_META}">') == 1, f"{relative}: public indexing directive missing")
    require("noindex" not in text.lower(), f"{relative}: noindex remains after launch")'''
new = '''    expected_robots = PRIVATE_ROBOTS if relative in PRIVACY_PATHS else PUBLIC_ROBOTS
    require(text.count(f'<meta name="robots" content="{expected_robots}">') == 1, f"{relative}: indexing directive mismatch")
    if relative in INDEXABLE_PATHS:
        require("noindex" not in text.lower(), f"{relative}: noindex remains after launch")'''
text = replace_once(text, old, new, relative)
text = text.replace(
    '        require(count(r\'<meta\\s+property="og:image:height"\\s+content="\\d+"\\s*/?>\', text) == 1, f"{relative}: OG image height missing")',
    '        require(count(r\'<meta\\s+property="og:image:height"\\s+content="\\d+"\\s*/?>\', text) == 1, f"{relative}: OG image height missing")\n        require(\'<meta property="og:image:type" content="image/webp">\' in text, f"{relative}: OG image MIME mismatch")',
)
text = text.replace(
    '    expected = [canonical for _, canonical, _, _ in ROUTES]',
    '    expected = [canonical for path, canonical, _, _ in ROUTES if path in INDEXABLE_PATHS]',
)
text = text.replace(
    'print(f"Release readiness validation passed for {len(ROUTES)} publicly indexable routes")',
    'print(f"Release readiness validation passed for {len(INDEXABLE_PATHS)} indexable routes and {len(PRIVACY_PATHS)} noindex privacy routes")',
)
write(relative, text)


# Privacy validator must assert the deliberate noindex, follow policy.
relative = 'scripts/validate-privacy-intake.py'
text = read(relative)
text = text.replace(
    'PUBLIC_ROBOTS = \'<meta name="robots" content="index, follow, max-image-preview:large">\'',
    'PUBLIC_ROBOTS = \'<meta name="robots" content="index, follow, max-image-preview:large">\'\nPRIVATE_ROBOTS = \'<meta name="robots" content="noindex, follow">\'',
)
# Only the two privacy-page require blocks occur after the homepage blocks.
privacy_start = text.index('ROOT / "privacy/index.html"')
head, tail = text[:privacy_start], text[privacy_start:]
tail = tail.replace('PUBLIC_ROBOTS,', 'PRIVATE_ROBOTS,', 2)
text = head + tail
old_loop = '''    for path in (ROOT / "index.html", ROOT / "ru/index.html", ROOT / "privacy/index.html", ROOT / "ru/privacy/index.html"):
        text = path.read_text(encoding="utf-8")
        if "noindex" in text.lower():
            raise AssertionError(f"Indexing remains blocked in {path.relative_to(ROOT)}")'''
new_loop = '''    for path in (ROOT / "index.html", ROOT / "ru/index.html"):
        text = path.read_text(encoding="utf-8")
        if "noindex" in text.lower():
            raise AssertionError(f"Indexing remains blocked in {path.relative_to(ROOT)}")
    for path in (ROOT / "privacy/index.html", ROOT / "ru/privacy/index.html"):
        text = path.read_text(encoding="utf-8")
        if PRIVATE_ROBOTS not in text:
            raise AssertionError(f"Privacy indexing policy mismatch in {path.relative_to(ROOT)}")'''
text = replace_once(text, old_loop, new_loop, relative)
write(relative, text)


# Live forensic audit expects privacy pages to remain crawlable but excluded from search.
relative = 'scripts/audit-post-refactor-tails-v1.py'
text = read(relative)
if 'NOINDEX_ROUTES =' not in text:
    text = text.replace(
        ']\n\nSTALE_ASSET_CANDIDATES =',
        ']\nNOINDEX_ROUTES = {"/privacy/", "/ru/privacy/"}\n\nSTALE_ASSET_CANDIDATES =',
        1,
    )
old_live = '''        robots = (parser.meta_robots or "").lower()
        if "noindex" in robots or "index" not in robots:
            add_issue(critical, "live-indexing", f"Live robots meta is {parser.meta_robots!r}", route)'''
new_live = '''        robots = (parser.meta_robots or "").lower()
        expected_robots = "noindex, follow" if route in NOINDEX_ROUTES else "index, follow, max-image-preview:large"
        if robots != expected_robots:
            add_issue(critical, "live-indexing", f"Expected {expected_robots!r}, found {parser.meta_robots!r}", route)'''
text = replace_once(text, old_live, new_live, relative)
write(relative, text)


# External launch audit follows the same indexing contract and sitemap scope.
relative = 'scripts/audit-launch-readiness-v1.py'
text = read(relative)
text = text.replace(
    'PUBLIC_ROBOTS = "index, follow, max-image-preview:large"',
    'PUBLIC_ROBOTS = "index, follow, max-image-preview:large"\nPRIVATE_ROBOTS = "noindex, follow"',
)
if 'NOINDEX_ROUTES =' not in text:
    text = text.replace(
        ']\n\n\ndef fetch_text',
        ']\nNOINDEX_ROUTES = {"/privacy/", "/ru/privacy/"}\nINDEXABLE_ROUTES = [route for route in ROUTES if route not in NOINDEX_ROUTES]\n\n\ndef fetch_text',
        1,
    )
text = text.replace(
    '        "expected": [canonical_for(route) for route in ROUTES],',
    '        "expected": [canonical_for(route) for route in INDEXABLE_ROUTES],',
)
text = text.replace(
    '        if apex.get("robots") != PUBLIC_ROBOTS:\n            report["critical"].append(f"{route}: live robots meta is {apex.get(\'robots\')!r}")',
    '        expected_robots = PRIVATE_ROBOTS if route in NOINDEX_ROUTES else PUBLIC_ROBOTS\n        if apex.get("robots") != expected_robots:\n            report["critical"].append(f"{route}: live robots meta is {apex.get(\'robots\')!r}; expected {expected_robots!r}")',
)
write(relative, text)


# Deployment runs the permanent production SEO contract after all build transforms.
relative = '.github/workflows/deploy-pages.yml'
text = read(relative)
needle = '          python3 scripts/validate-release-readiness.py\n'
if 'python3 scripts/audit-seo-launch-v1.py' not in text:
    text = replace_once(text, needle, needle + '          python3 scripts/audit-seo-launch-v1.py\n', relative)
write(relative, text)

print('SEO launch indexing patch applied.')
