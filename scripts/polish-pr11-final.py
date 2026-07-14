#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
css_path = root / 'assets' / 'css' / 'site.v2.css'
css = css_path.read_text(encoding='utf-8')

replacements = {
'''  color: var(--muted);\n  font-size: 9px;\n  text-transform: uppercase;''': '''  color: #555750;\n  font-size: 12px;\n  line-height: 1.35;\n  letter-spacing: .015em;\n  text-transform: uppercase;''',
'''.side-navigation b { color: var(--terracotta); font-size: 10px; font-weight: 500; }''': '''.side-navigation b { color: var(--terracotta); font-size: 12px; font-weight: 600; }''',
'''  background: linear-gradient(rgba(21, 30, 18, .18), rgba(21, 30, 18, .18)), url("../images/portrait/alina-horb-portrait-hero-v3.webp") center / cover no-repeat;\n  filter: blur(18px) saturate(.82) brightness(.76);\n  transform: scale(1.08);''': '''  background: linear-gradient(rgba(30, 42, 27, .06), rgba(30, 42, 27, .06)), url("../images/portrait/alina-horb-portrait-hero-v3.webp") center / cover no-repeat;\n  filter: blur(12px) saturate(.96) brightness(.92);\n  transform: scale(1.045);''',
'''  background: linear-gradient(90deg, rgba(26, 35, 23, .34), transparent 18%, transparent 82%, rgba(26, 35, 23, .34));''': '''  background: linear-gradient(90deg, rgba(29, 42, 26, .12), transparent 12%, transparent 88%, rgba(29, 42, 26, .12));''',
'''.hero-portrait picture { position: relative; z-index: 1; display: grid; place-items: center; width: 100%; height: 100%; }''': '''.hero-portrait picture { position: relative; z-index: 1; display: grid; place-items: start center; width: 100%; height: 100%; }''',
'''.hero-portrait img { width: auto; height: 100%; max-width: none; object-fit: contain; object-position: center top; }''': '''.hero-portrait img { width: 80%; height: auto; max-width: none; object-fit: contain; object-position: center top; }'''
}

for old, new in replacements.items():
    if old not in css:
        raise SystemExit(f'Expected CSS fragment not found:\n{old}')
    css = css.replace(old, new, 1)

# Keep mobile portrait balanced: narrower ambient side fields without returning to a close-up.
mobile_old = '''  .hero-portrait img { height: 100%; width: auto; max-width: none; }'''
mobile_new = '''  .hero-portrait img { width: 80%; height: auto; max-width: none; }'''
if mobile_old in css:
    css = css.replace(mobile_old, mobile_new, 1)

css_path.write_text(css, encoding='utf-8')
print('Applied final portrait and navigation polish.')
