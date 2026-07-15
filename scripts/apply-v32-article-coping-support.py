#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "ru/notes/when-coping-stops-helping/index.html"
old = "При непосредственной угрозе безопасности нужна местная экстренная помощь."
new = "При непосредственной угрозе безопасности нужна немедленная местная экстренная помощь."
text = path.read_text(encoding="utf-8")
if old in text:
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.relative_to(ROOT)}")
elif new in text:
    print("Direct answer already normalized")
else:
    raise SystemExit("Expected Russian direct-answer sentence was not found")
