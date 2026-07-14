# Alina Horb Website — Project History

This document records major project milestones and decisions. It is intentionally higher level than the Git commit log.

## 2026-07 — Initial repository and preview

### Repository setup

- Created the public repository `proaiexpert/alina-horb-website`.
- Established Ukrainian as the primary language and Russian under `/ru/`.
- Added GitHub Pages deployment.
- Kept preview pages `noindex, nofollow` until the official domain and final SEO release.

### Bilingual implementation

Major outcomes:

- separate UA and RU HTML pages;
- reciprocal language switching;
- localized logos and interface copy;
- responsive layout across mobile, tablet, laptop, and desktop;
- public-only asset rules;
- semantic structure and basic accessibility.

Reference milestone:

- PR #7 — bilingual UA/RU website preview.

---

## 2026-07 — Asset and deployment stabilization

The first live preview exposed several production-specific issues:

- damaged or missing binary image assets;
- portrait crop inconsistencies;
- diploma and logo loading failures;
- confusion between the Alina preview and the ProAI Expert domain;
- stale browser cache after asset replacement.

Corrections included:

- validated public portrait and diploma derivatives;
- restored UA/RU logo assets;
- asset filename versioning;
- deployment workflow checks;
- removal of incorrect domain assumptions;
- direct GitHub Pages preview URLs.

Reference milestones:

- PR #8 — Pages binary assets and domain correction;
- PR #9 — portrait and desktop contact-form correction;
- PR #10 — portrait framing and compact contact-form correction.

---

## 2026-07 — Premium Editorial Sanctuary V2

A full visual and structural redesign replaced the earlier static prototype.

Delivered:

- Premium Editorial Sanctuary design system;
- editorial hero and numbered navigation;
- trust strip;
- support-needs index;
- areas-of-work section;
- About, diploma, consultation process, principles, FAQ, Notes, contacts, final CTA, and footer;
- Cormorant Garamond + Manrope typography;
- restrained ivory, graphite, terracotta, and sage palette;
- responsive mobile navigation;
- subtle motion and reduced-motion fallback;
- editorial Notes index;
- four article routes in Ukrainian and Russian;
- asset validator and route QA.

Reference milestone:

- PR #11 — Premium Editorial Sanctuary V2.0.

---

## 2026-07 — Visual QA and portrait correction

The V2 review identified two recurring portrait problems:

1. aggressive `cover` crops produced an oversized face;
2. `contain` displayed unwanted side fields because the source image was narrow.

The project established a stricter portrait rule:

- composition must be prepared in the image derivative, not guessed through repeated CSS patches;
- desktop and mobile may use different crops;
- portrait QA must verify head, shoulders, clothing, and intended context;
- versioned filenames are required when changing visible image content.

A temporary review branch and PR were used only for Chromium/WebKit screenshot QA and were closed without merge.

Reference milestone:

- PR #12 — temporary visual QA only.

---

## 2026-07 — Confirmed contacts and expanded practice information

New confirmed information from Alina was added:

- Telegram `@alina_horb1991`;
- Instagram `@ng_alina_dp`;
- email `alinahorb1991@gmail.com`;
- work with people of different ages, couples, and families;
- work with minors agreed separately;
- support for people affected by war and internally displaced persons;
- acute and chronic stress;
- panic attacks;
- anxiety states and disorders;
- traumatic experience and PTSD symptoms;
- intrusive thoughts and OCD manifestations;
- domestic violence;
- crisis and family requests;
- repeated suicidal or self-harm thoughts.

Editorial safety decisions:

- no diagnosis or treatment guarantees;
- no claim that the website is emergency care;
- “first emergency help” reframed as primary psychological support during acute stress;
- immediate danger directs users to local emergency or crisis services.

Reference milestone:

- PR #13 — contacts, audience, and safety-information update.

---

## 2026-07 — Footer and mobile conversion polish

Corrections included:

- reduced footer logo size;
- compact contact and language grouping;
- restrained ProAI Expert maker credit;
- reduced mobile footer whitespace;
- mobile booking CTA;
- CTA shown only after the hero CTA leaves the viewport;
- CTA hidden near Contacts and Footer;
- iPhone safe-area support.

Reference milestone:

- PR #14 — footer and mobile booking CTA.

---

## 2026-07 — V3.1 planning and design consolidation

A large review combined:

- current live implementation;
- previous deep research;
- Premium Editorial Sanctuary direction;
- Kinfolk, Oura, and Portland Talk Club references;
- filtered Gemini recommendations;
- updated confirmed information from Alina;
- mobile, accessibility, deployment, and SEO constraints.

The project rejected:

- heavy portrait parallax;
- scroll hijacking;
- excessive 3D effects;
- generic handwritten fonts;
- random stock photography;
- automatic removal of the sage principles section;
- final SEO indexing before legal and content completion.

The project retained or strengthened:

- editorial typography;
- controlled section reveals;
- process-line animation;
- active navigation;
- FAQ motion;
- editorial Notes layout;
- public redacted diploma;
- separate natural UA/RU pages;
- mobile booking CTA;
- restrained visual rhythm.

Reference milestone:

- Issue #15 — Homepage Content & Visual Polish V3.1.

---

## V3.1 portrait decision

The original outdoor portrait series in the pink striped shirt is being retired from the homepage.

Approved pair:

- **Hero:** seated portrait with an open book in a warm ivory interior;
- **About:** separate close portrait in an ivory blouse.

The two photographs serve different roles:

- Hero communicates professional context, calmness, and consultation atmosphere;
- About creates direct personal trust and eye contact.

No face, body, hair, hand, book, or clothing generation is permitted. Only crop, resize, compression, color management, and restrained sharpening are allowed.

---

## Current state

- Public preview is live.
- Ukrainian and Russian versions are available.
- Preview remains `noindex, nofollow`.
- V3.1 homepage work is active.
- Article pages remain structural/editorial drafts.
- Production form, privacy/legal pages, official domain, and final SEO release remain pending.

For the current approved facts, use `PROJECT_SOURCE_OF_TRUTH.md` rather than this historical summary.
