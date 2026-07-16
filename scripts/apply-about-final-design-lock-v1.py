#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "assets/css/site.about.v1.css"
text = path.read_text(encoding="utf-8")
marker = "/* Final editorial design lock: navigation, depth and micro-interactions. */"

if marker in text:
    print("Final About design lock already applied")
    raise SystemExit(0)

block = r'''

/* Final editorial design lock: navigation, depth and micro-interactions. */
.page-about-profile {
  --profile-header-height: 86px;
}

.page-about-profile ::selection {
  background: rgba(198, 83, 63, .2);
  color: var(--graphite);
}

.page-about-profile .site-header {
  position: sticky;
  z-index: 70;
  top: 0;
  border-bottom-color: rgba(47, 48, 45, .13);
  box-shadow: 0 10px 32px rgba(47, 48, 45, .045);
}

.profile-hero,
.profile-path,
.profile-position,
.profile-methods,
.profile-education,
.profile-scope,
.profile-boundaries,
.profile-format,
.profile-final {
  scroll-margin-top: calc(var(--profile-header-height) + 22px);
}

.profile-side-navigation a {
  position: relative;
}

.profile-side-navigation a::after {
  position: absolute;
  right: 0;
  bottom: -5px;
  left: 30px;
  height: 1px;
  background: currentColor;
  content: "";
  opacity: .42;
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform .28s var(--ease);
}

.profile-side-navigation a:is(:hover, .is-active)::after {
  transform: scaleX(1);
}

.profile-hero-portrait::after {
  position: absolute;
  top: 48%;
  right: -78px;
  color: rgba(47, 48, 45, .48);
  content: "ALINA HORB · PROFILE";
  font-size: 10px;
  font-weight: 600;
  letter-spacing: .18em;
  line-height: 1;
  pointer-events: none;
  text-transform: uppercase;
  transform: rotate(90deg) translateY(-50%);
  transform-origin: center;
}

.profile-hero-facts span,
.timeline-year,
.method-index,
.scope-index span,
.position-principles span,
.education-year {
  font-variant-numeric: tabular-nums;
}

.profile-section-heading--sticky {
  top: calc(var(--profile-header-height) + 28px);
}

.boundaries-card,
.profile-diploma a {
  will-change: transform;
}

@media (hover: hover) and (pointer: fine) {
  .position-principles article,
  .profile-method-list article,
  .scope-index article,
  .boundaries-card {
    transition: background-color .3s ease, border-color .3s ease, box-shadow .3s ease, transform .3s var(--ease);
  }

  .position-principles article:hover {
    background: rgba(250, 247, 241, .055);
    transform: translateY(-5px);
  }

  .profile-method-list article:hover {
    background: rgba(135, 146, 127, .065);
    box-shadow: inset 3px 0 0 rgba(198, 83, 63, .55);
    transform: translateX(6px);
  }

  .scope-index article:hover {
    background: rgba(135, 146, 127, .08);
  }

  .scope-index article:hover span {
    transform: translateX(4px);
  }

  .scope-index span {
    transition: transform .3s var(--ease);
  }

  .boundaries-card:hover {
    border-color: rgba(47, 48, 45, .3);
    box-shadow: 0 38px 84px rgba(47, 48, 45, .11);
    transform: translateY(-4px);
  }
}

@media (max-width: 900px) {
  .page-about-profile { --profile-header-height: 72px; }
  .profile-section-heading--sticky { top: auto; }
  .profile-hero-portrait::after { display: none; }
}

@media (max-width: 620px) {
  .profile-hero,
  .profile-path,
  .profile-position,
  .profile-methods,
  .profile-education,
  .profile-scope,
  .profile-boundaries,
  .profile-format,
  .profile-final {
    scroll-margin-top: 86px;
  }

  .profile-hero-heading h1 {
    text-wrap: balance;
  }

  .profile-hero-copy > p,
  .profile-path-copy,
  .profile-method-list p,
  .format-copy p,
  .profile-final p {
    text-wrap: pretty;
  }
}

@media (prefers-reduced-motion: reduce) {
  .profile-side-navigation a::after,
  .position-principles article,
  .profile-method-list article,
  .scope-index article,
  .scope-index span,
  .boundaries-card,
  .profile-diploma a {
    transition: none !important;
  }
}
'''

path.write_text(text.rstrip() + block + "\n", encoding="utf-8")
print("Applied final About editorial design lock")
