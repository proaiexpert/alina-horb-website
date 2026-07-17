#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_required(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"Expected polish contract missing in {path.relative_to(ROOT)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


navigation_css = ROOT / "assets/css/site.navigation.v1.css"
placement_marker = '''  .article-hero-grid.has-editorial-rail {
    grid-template-columns: 184px minmax(0, .82fr) minmax(360px, 1.08fr);
    gap: clamp(28px, 3.1vw, 48px);
  }
'''
placement_rules = placement_marker + '''
  .notes-hub-hero-grid.has-editorial-rail > .editorial-rail,
  .article-hero-grid.has-editorial-rail > .editorial-rail {
    grid-column: 1;
    grid-row: 1;
  }

  .notes-hub-hero-grid.has-editorial-rail > .notes-hub-heading,
  .article-hero-grid.has-editorial-rail > .article-hero-copy {
    grid-column: 2;
    grid-row: 1;
  }

  .notes-hub-hero-grid.has-editorial-rail > .notes-hub-index,
  .article-hero-grid.has-editorial-rail > .article-hero-visual {
    grid-column: 3;
    grid-row: 1;
  }
'''
replace_required(navigation_css, placement_marker, placement_rules)

consult_css = ROOT / "assets/css/site.consultations.v1.css"
replace_required(
    consult_css,
    '.agreement-note > p:last-child { max-width: 860px; margin: 0; color: var(--muted); font-size: 16px; line-height: 1.78; }',
    '.agreement-note > p:last-child { max-width: 760px; margin: 0; color: var(--muted); font-size: 16px; line-height: 1.78; }',
)

# The browser gate must reject desktop headings accidentally squeezed into the 184px rail.
audit = ROOT / "scripts/audit-final-ux-v1.mjs"
replace_required(
    audit,
    '      if (metrics.h1Overflows) pushIssue(critical, viewport, route, "H1 extends outside the viewport");\n',
    '      if (metrics.h1Overflows) pushIssue(critical, viewport, route, "H1 extends outside the viewport");\n      if (viewport.width >= 1181 && metrics.h1Rect?.width < 280) pushIssue(critical, viewport, route, `desktop H1 is squeezed into ${Math.round(metrics.h1Rect.width)}px`);\n',
)

print("Final editorial placement, readable measure and audit guard applied")
