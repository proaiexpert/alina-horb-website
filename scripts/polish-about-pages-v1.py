#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "assets/css/site.about.v1.css"
text = path.read_text(encoding="utf-8")

old_hero = """.profile-hero {
  position: relative;
  padding: clamp(46px, 6vw, 84px) 0 clamp(64px, 7vw, 104px);
  border-bottom: 1px solid var(--line);
}"""
new_hero = """.profile-hero {
  position: relative;
  overflow: hidden;
  padding: clamp(46px, 6vw, 84px) 0 clamp(64px, 7vw, 104px);
  border-bottom: 1px solid var(--line);
}"""

old_diploma = """.profile-diploma a {
  display: block;
  border: 1px solid rgba(47,48,45,.2);
  padding: 18px;
  background: rgba(255,255,255,.58);
  box-shadow: 0 28px 70px rgba(47,48,45,.12);
  transition: transform .3s var(--ease), box-shadow .3s ease;
}"""
new_diploma = """.profile-diploma a {
  aspect-ratio: 4 / 5;
  display: grid;
  place-items: center;
  overflow: hidden;
  border: 1px solid rgba(47,48,45,.2);
  padding: 18px;
  background: rgba(255,255,255,.58);
  box-shadow: 0 28px 70px rgba(47,48,45,.12);
  transition: transform .3s var(--ease), box-shadow .3s ease;
}

.profile-diploma picture {
  display: block;
  width: 100%;
  height: 100%;
}

.profile-diploma img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}"""

for old, new, label in ((old_hero, new_hero, "hero overflow"), (old_diploma, new_diploma, "diploma frame")):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one {label} block, found {count}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Applied final About page overflow and diploma polish")
