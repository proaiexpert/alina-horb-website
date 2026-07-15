#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UA_SCHEMA = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": "https://alinahorb.com/#website",
        "url": "https://alinahorb.com/",
        "name": "Аліна Горб — психолог",
        "inLanguage": ["uk", "ru"],
        "publisher": {"@id": "https://alinahorb.com/#person"}
      },
      {
        "@type": "Person",
        "@id": "https://alinahorb.com/#person",
        "name": "Аліна Горб",
        "alternateName": "Алина Горб",
        "url": "https://alinahorb.com/",
        "jobTitle": "Психолог, магістр психології",
        "email": "mailto:hello@alinahorb.com",
        "knowsLanguage": ["uk", "ru"],
        "sameAs": [
          "https://t.me/alina_horb1991",
          "https://instagram.com/ng_alina_dp"
        ]
      }
    ]
  }
  </script>
'''

RU_SCHEMA = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": "https://alinahorb.com/#website",
        "url": "https://alinahorb.com/",
        "name": "Алина Горб — психолог",
        "inLanguage": ["ru", "uk"],
        "publisher": {"@id": "https://alinahorb.com/#person"}
      },
      {
        "@type": "Person",
        "@id": "https://alinahorb.com/#person",
        "name": "Алина Горб",
        "alternateName": "Аліна Горб",
        "url": "https://alinahorb.com/ru/",
        "jobTitle": "Психолог, магистр психологии",
        "email": "mailto:hello@alinahorb.com",
        "knowsLanguage": ["ru", "uk"],
        "sameAs": [
          "https://t.me/alina_horb1991",
          "https://instagram.com/ng_alina_dp"
        ]
      }
    ]
  }
  </script>
'''

PAGES = {
    ROOT / "index.html": {
        "old_favicon": '<link rel="icon" type="image/png" href="assets/images/logos/alina-horb-logo-ua-dark.png">',
        "new_favicon": '<link rel="icon" type="image/svg+xml" href="assets/images/logos/favicon-ag.svg">',
        "old_css": '  <link rel="stylesheet" href="assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="assets/css/site.notes-hub.v3-2.css">',
        "new_css": '  <link rel="stylesheet" href="assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="assets/css/site.v3-1-stability.css">\n  <link rel="stylesheet" href="assets/css/site.footer.v3-2.css">\n  <link rel="stylesheet" href="assets/css/site.privacy.v3-2.css">\n  <link rel="stylesheet" href="assets/css/site.intake.v3-2.css">\n  <link rel="stylesheet" href="assets/css/site.notes-hub.v3-2.css">',
        "schema": UA_SCHEMA,
    },
    ROOT / "ru/index.html": {
        "old_favicon": '<link rel="icon" type="image/png" href="../assets/images/logos/alina-horb-logo-ru-dark.png">',
        "new_favicon": '<link rel="icon" type="image/svg+xml" href="../assets/images/logos/favicon-ag.svg">',
        "old_css": '  <link rel="stylesheet" href="../assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="../assets/css/site.notes-hub.v3-2.css">',
        "new_css": '  <link rel="stylesheet" href="../assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="../assets/css/site.v3-1-stability.css">\n  <link rel="stylesheet" href="../assets/css/site.footer.v3-2.css">\n  <link rel="stylesheet" href="../assets/css/site.privacy.v3-2.css">\n  <link rel="stylesheet" href="../assets/css/site.intake.v3-2.css">\n  <link rel="stylesheet" href="../assets/css/site.notes-hub.v3-2.css">',
        "schema": RU_SCHEMA,
    },
}

for path, replacements in PAGES.items():
    text = path.read_text(encoding="utf-8")

    if replacements["new_favicon"] not in text:
        if replacements["old_favicon"] not in text:
            raise SystemExit(f"Cannot locate legacy favicon in {path.relative_to(ROOT)}")
        text = text.replace(replacements["old_favicon"], replacements["new_favicon"], 1)

    if replacements["new_css"] not in text:
        if replacements["old_css"] not in text:
            raise SystemExit(f"Cannot locate legacy stylesheet block in {path.relative_to(ROOT)}")
        text = text.replace(replacements["old_css"], replacements["new_css"], 1)

    if '"@type": "WebSite"' not in text:
        if "</head>" not in text:
            raise SystemExit(f"Cannot locate closing head in {path.relative_to(ROOT)}")
        text = text.replace("</head>", replacements["schema"] + "</head>", 1)

    path.write_text(text, encoding="utf-8")
    print(f"Normalized {path.relative_to(ROOT)}")
