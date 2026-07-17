#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace_required(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"Expected patch contract missing in {path.relative_to(ROOT)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# Measure actual rendered text lines rather than the width of their grid cells.
audit = ROOT / "scripts/audit-final-ux-v1.mjs"
replace_required(
    audit,
    '''        const paragraphs = [...document.querySelectorAll("main p, main li")]
          .filter(visible)
          .map((element) => ({ width: element.getBoundingClientRect().width, text: element.textContent.trim().slice(0, 90) }))
          .sort((a, b) => b.width - a.width);''',
    '''        const textLineWidth = (element) => {
          const range = document.createRange();
          range.selectNodeContents(element);
          const widths = [...range.getClientRects()].map((value) => value.width).filter((value) => value > 0);
          return widths.length ? Math.max(...widths) : 0;
        };
        const paragraphs = [...document.querySelectorAll("main p, main li")]
          .filter(visible)
          .map((element) => ({ width: textLineWidth(element), text: element.textContent.trim().slice(0, 90) }))
          .sort((a, b) => b.width - a.width);''',
)

privacy = ROOT / "scripts/validate-privacy-intake.py"
replace_required(privacy, 'href="./">alinahorb.com</a>', 'href="../">alinahorb.com</a>')
replace_required(privacy, 'href="../../ru/">alinahorb.com</a>', 'href="../">alinahorb.com</a>')

print("Final UX audit and validator precision patches applied")
