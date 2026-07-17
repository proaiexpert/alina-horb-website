#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "scripts/audit-final-ux-v1.mjs"
text = path.read_text(encoding="utf-8")

old_observer = '''      await page.addInitScript(() => {
        window.__UX_AUDIT_CLS__ = 0;
        try {
          new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
              if (!entry.hadRecentInput) window.__UX_AUDIT_CLS__ += entry.value;
            }
          }).observe({ type: "layout-shift", buffered: true });
        } catch {}
      });
'''
new_observer = '''      await page.addInitScript(() => {
        window.__UX_AUDIT_CLS__ = 0;
        window.__UX_AUDIT_SHIFTS__ = [];
        try {
          new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
              if (entry.hadRecentInput) continue;
              window.__UX_AUDIT_CLS__ += entry.value;
              const sources = (entry.sources || []).map((source) => {
                const node = source.node;
                let selector = null;
                if (node instanceof Element) {
                  selector = node.id ? `#${node.id}` : `${node.tagName.toLowerCase()}${node.classList.length ? `.${[...node.classList].join(".")}` : ""}`;
                }
                const serializeRect = (rect) => rect ? ({ x: rect.x, y: rect.y, width: rect.width, height: rect.height }) : null;
                return { selector, previousRect: serializeRect(source.previousRect), currentRect: serializeRect(source.currentRect) };
              });
              window.__UX_AUDIT_SHIFTS__.push({ value: entry.value, sources });
            }
          }).observe({ type: "layout-shift", buffered: true });
        } catch {}
      });
'''
if old_observer not in text:
    if new_observer not in text:
        raise SystemExit("CLS observer patch contract missing")
else:
    text = text.replace(old_observer, new_observer, 1)

old_metric = '          cls: Number(window.__UX_AUDIT_CLS__ || 0),\n          bodyClass: document.body.className\n'
new_metric = '          cls: Number(window.__UX_AUDIT_CLS__ || 0),\n          shiftSources: window.__UX_AUDIT_SHIFTS__ || [],\n          bodyClass: document.body.className\n'
if old_metric not in text:
    if new_metric not in text:
        raise SystemExit("CLS metric patch contract missing")
else:
    text = text.replace(old_metric, new_metric, 1)

path.write_text(text, encoding="utf-8")
print("CLS source diagnostics added to final UX audit")
