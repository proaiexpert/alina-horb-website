#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    ROOT / "index.html": {
        "old_favicon": '<link rel="icon" type="image/png" href="assets/images/logos/alina-horb-logo-ua-dark.png">',
        "new_favicon": '<link rel="icon" type="image/svg+xml" href="assets/images/logos/favicon-ag.svg">',
        "old_css": '  <link rel="stylesheet" href="assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="assets/css/site.notes-hub.v3-2.css">',
        "new_css": '  <link rel="stylesheet" href="assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="assets/css/site.v3-1-stability.css">\n  <link rel="stylesheet" href="assets/css/site.footer.v3-2.css">\n  <link rel="stylesheet" href="assets/css/site.privacy.v3-2.css">\n  <link rel="stylesheet" href="assets/css/site.intake.v3-2.css">\n  <link rel="stylesheet" href="assets/css/site.notes-hub.v3-2.css">',
    },
    ROOT / "ru/index.html": {
        "old_favicon": '<link rel="icon" type="image/png" href="../assets/images/logos/alina-horb-logo-ru-dark.png">',
        "new_favicon": '<link rel="icon" type="image/svg+xml" href="../assets/images/logos/favicon-ag.svg">',
        "old_css": '  <link rel="stylesheet" href="../assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="../assets/css/site.notes-hub.v3-2.css">',
        "new_css": '  <link rel="stylesheet" href="../assets/css/site.v3-1.css">\n  <link rel="stylesheet" href="../assets/css/site.v3-1-stability.css">\n  <link rel="stylesheet" href="../assets/css/site.footer.v3-2.css">\n  <link rel="stylesheet" href="../assets/css/site.privacy.v3-2.css">\n  <link rel="stylesheet" href="../assets/css/site.intake.v3-2.css">\n  <link rel="stylesheet" href="../assets/css/site.notes-hub.v3-2.css">',
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

    path.write_text(text, encoding="utf-8")
    print(f"Normalized {path.relative_to(ROOT)}")
