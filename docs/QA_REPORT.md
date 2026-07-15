# QA Report — GitHub-Ready Package V1

## Final status

**PASS WITH NOTES**

The package passed code-level, static-server, responsive, asset, keyboard, and browser-runtime checks. Chromium in this environment blocks direct navigation to localhost with `ERR_BLOCKED_BY_ADMINISTRATOR`; therefore local-path HTTP responses were verified separately and browser QA used an in-memory bundle containing the exact production HTML, CSS, JavaScript, and image bytes. External Google Fonts were excluded from the QA bundle because outbound font requests are unavailable in the runtime; production HTML remains unchanged and retains `display=swap` plus fallback stacks.

## Environment

- Browser: Chromium `144.0.7559.96`
- Static server command: `python3 -m http.server 8125 --bind 127.0.0.1`
- Direct Chromium/static-server navigation: **blocked by environment policy**
- Browser QA mode: exact in-memory local bundle

## Responsive results

| Requested viewport | `innerWidth` | `clientWidth` | `scrollWidth` | Page height | Overflow |
|---:|---:|---:|---:|---:|---|
| 1440 | 1440 | 1440 | 1440 | 3236 | PASS |
| 1280 | 1280 | 1280 | 1280 | 3231 | PASS |
| 1024 | 1024 | 1024 | 1024 | 3292 | PASS |
| 768 | 768 | 768 | 768 | 4453 | PASS |
| 430 | 430 | 430 | 430 | 5537 | PASS |
| 390 | 390 | 390 | 390 | 5627 | PASS |
| 375 | 375 | 375 | 375 | 5701 | PASS |
| 360 | 360 | 360 | 360 | 5686 | PASS |
| 320 | 320 | 320 | 320 | 5867 | PASS |

All requested widths satisfy:

`document.documentElement.scrollWidth <= window.innerWidth`

## Screenshots

Full-page QA screenshots were generated at 1440, 390 and 320 px and remain in the verified Google Drive delivery package. They are intentionally excluded from the production branch to keep the repository lightweight.

## Portrait verification

- JPEG production image dimensions: `1200 × 2538`
- Browser-reported natural dimensions: `1200 × 2538`
- `object-fit`: `cover`
- object positions verified:
  - desktop: `50% 43%`;
  - tablet: `50% 42%`;
  - mobile: `50% 41%`.

## Typography verification

| Text category | Desktop 1440 | Mobile 390 | Status |
|---|---:|---:|---|
| Body | 15px | 16px | PASS |
| Hero/body introduction | 15px | 15px | PASS |
| About body | 15px | 16px | PASS |
| Process descriptions | 14px | 14px | PASS |
| FAQ answers | 15px | 15px | PASS |
| Footer | 12px | 12px | PASS |
| Secondary label | 11px | 11px | PASS |

Support-index copy is `12px` on desktop as a compact secondary index label and `15px` on mobile.

## Functional and accessibility checks

- Mobile menu opens with Enter: **PASS**
- `aria-expanded` updates: **PASS**
- Mobile menu closes after anchor selection: **PASS**
- FAQ opens with keyboard: **PASS**
- Native `<details>/<summary>` remains usable without JavaScript: **PASS**
- No-JS mobile navigation remains visible: **PASS**
- Skip link exists: **PASS**
- Focus outline on menu and CTA: **2 px solid — PASS**
- Reduced-motion rules applied: **PASS**
- One H1: **1 — PASS**
- Duplicate IDs: **0**

## Errors and assets

- Console errors: **0**
- Runtime/page errors: **0**
- Browser request failures in QA bundle: **0**
- Missing rendered images after eager QA loading: **0**
- Static-server HTTP errors: **0**
- Missing local references in HTML: **0**
- Broken internal anchors: **0** across all viewports

## SEO and link checks

- Canonical: `https://alinahorb.com/` — PASS
- Email: `hello@alinahorb.com` — PASS
- Maker credit: `ProAI Expert` — PASS
- Maker URL: `https://proai-expert.com` — PASS
- Fabricated Telegram link: **not present**
- UA route: **not created**
- Privacy policy: inactive text, not a 404 link

## Packaging and privacy

- High-resolution source portrait master: **not included**
- Previous low-resolution portrait files: **not included**
- Original/private/unredacted diploma: **not included**
- V1/V2/V2.1 ZIP files: **not included**
- `.env`, credentials, cookies, tokens, cache, browser profiles, and `node_modules`: **not included**
- The package was produced without direct GitHub writes and is imported through a separate review branch.
