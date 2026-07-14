#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
css_path = root / 'assets' / 'css' / 'site.v2.css'
css = css_path.read_text(encoding='utf-8')
old = '.hero-portrait img { width: auto; height: 100%; max-width: 100%; object-fit: contain; object-position: center top; }'
new = '.hero-portrait img { width: auto; height: 100%; max-width: none; object-fit: contain; object-position: center top; }'
count = css.count(old)
if count < 1:
    raise SystemExit('Expected portrait image rule was not found')
css = css.replace(old, new)
old_mobile = '.hero-portrait img { height: 100%; width: auto; max-width: 100%; }'
new_mobile = '.hero-portrait img { height: 100%; width: auto; max-width: none; }'
css = css.replace(old_mobile, new_mobile)
css_path.write_text(css, encoding='utf-8')
print(f'Updated {count} base portrait rule(s).')
