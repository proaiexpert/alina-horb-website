#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
css_path = root / 'assets' / 'css' / 'site.v2.css'
css = css_path.read_text(encoding='utf-8')
marker = '/* PR11 final portrait positioning fix */'
if marker in css:
    print('Final portrait positioning fix already present.')
    raise SystemExit(0)
css += '''

/* PR11 final portrait positioning fix */
.hero-portrait picture {
  position: absolute;
  z-index: 1;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
}
.hero-portrait img {
  position: absolute;
  top: 0;
  left: 50%;
  width: auto;
  height: 100%;
  max-width: none;
  object-fit: contain;
  object-position: center top;
  transform: translateX(-50%);
}
@media (max-width: 620px) {
  .hero-portrait img {
    position: absolute;
    top: 0;
    left: 50%;
    width: auto;
    height: 100%;
    max-width: none;
    transform: translateX(-50%);
  }
}
'''
css_path.write_text(css, encoding='utf-8')
print('Appended final absolute portrait positioning rules.')
