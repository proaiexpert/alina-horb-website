# CODEX TASK — V3.2 bilingual social previews for Telegram and social platforms

## Objective

Make shared links generate a reliable language-specific preview:

- `https://alinahorb.com/` → Ukrainian title, description and Ukrainian preview image;
- `https://alinahorb.com/ru/` → Russian title, description and Russian preview image.

The immediate reported problem is that Telegram currently shows no useful preview. The current homepage metadata still points at the former GitHub Pages image URL and uses a vertical portrait rather than a dedicated social card.

## Repository

`proaiexpert/alina-horb-website`

Start from the latest `main` after the documentation and favicon merges.

Create branch:

`fix/v32-bilingual-social-previews`

Open one PR. Do not merge automatically.

## Approved design sources

Use the committed 1200 × 630 SVG sources:

- `docs/design/og/alina-horb-og-ua-v1.svg`
- `docs/design/og/alina-horb-og-ru-v1.svg`

Render them to optimized JPEG files:

- `assets/images/social/alina-horb-og-ua-v1.jpg`
- `assets/images/social/alina-horb-og-ru-v1.jpg`

Requirements:

- exact output size: 1200 × 630;
- JPEG, sRGB, progressive where supported;
- target file size below 350 KB each without visible text degradation;
- preserve Cyrillic characters correctly;
- do not substitute unrelated stock imagery;
- do not alter the approved site portraits or logos;
- versioned filenames must remain as specified.

The SVG files are design sources only. Production metadata must reference JPEG, not SVG.

## Ukrainian homepage metadata

Update `index.html` so the `<head>` includes one coherent Open Graph set:

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Аліна Горб — психолог">
<meta property="og:locale" content="uk_UA">
<meta property="og:locale:alternate" content="ru_RU">
<meta property="og:title" content="Аліна Горб — психолог">
<meta property="og:description" content="Психологічна підтримка українською та російською мовами. Онлайн; очно — за попереднім погодженням.">
<meta property="og:url" content="https://alinahorb.com/">
<meta property="og:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg">
<meta property="og:image:secure_url" content="https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Аліна Горб — психологічні консультації українською та російською">
```

Twitter-compatible tags:

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Аліна Горб — психолог">
<meta name="twitter:description" content="Психологічна підтримка українською та російською мовами. Онлайн; очно — за попереднім погодженням.">
<meta name="twitter:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg">
<meta name="twitter:image:alt" content="Аліна Горб — психологічні консультації українською та російською">
```

## Russian homepage metadata

Update `ru/index.html` with a separate Russian set:

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Алина Горб — психолог">
<meta property="og:locale" content="ru_RU">
<meta property="og:locale:alternate" content="uk_UA">
<meta property="og:title" content="Алина Горб — психолог">
<meta property="og:description" content="Психологическая поддержка на украинском и русском языках. Онлайн; очно — по предварительному согласованию.">
<meta property="og:url" content="https://alinahorb.com/ru/">
<meta property="og:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg">
<meta property="og:image:secure_url" content="https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Алина Горб — психологические консультации на украинском и русском">
```

Twitter-compatible tags:

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Алина Горб — психолог">
<meta name="twitter:description" content="Психологическая поддержка на украинском и русском языках. Онлайн; очно — по предварительному согласованию.">
<meta name="twitter:image" content="https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg">
<meta name="twitter:image:alt" content="Алина Горб — психологические консультации на украинском и русском">
```

## Head cleanup

For both homepages:

- remove the old `proaiexpert.github.io/alina-horb-website/...` social image URLs;
- ensure there is exactly one `og:title`, `og:type`, `og:url`, `og:description`, `og:image`, and `twitter:image`;
- retain existing canonical and reciprocal hreflang values;
- retain `noindex, nofollow` for now;
- retain production favicon references;
- do not change visible homepage content in this PR.

## Validation

Add or extend repository validation so CI fails when:

- homepage OG image URLs use the old GitHub Pages host;
- UA and RU homepages reference the same social image by mistake;
- referenced social images are missing;
- image dimensions are not 1200 × 630;
- the production URLs are not HTTPS.

A small Python validation script is acceptable if it has no third-party dependency. Pillow must not become a CI dependency. JPEG dimensions can be checked with a minimal parser, existing standard-library tooling, or validation performed during generation and asserted by file metadata plus a lightweight check.

## Production QA after deployment

Verify:

1. `https://alinahorb.com/assets/images/social/alina-horb-og-ua-v1.jpg` → 200, `image/jpeg`.
2. `https://alinahorb.com/assets/images/social/alina-horb-og-ru-v1.jpg` → 200, `image/jpeg`.
3. UA homepage source contains only the UA preview image.
4. RU homepage source contains only the RU preview image.
5. No old GitHub Pages OG image URL remains in either homepage.
6. HTTP redirects and HTTPS remain unchanged.
7. No network 404 or console regression is introduced.

## Telegram cache verification

Telegram may retain an earlier URL preview. After the new production deployment:

- first test in a fresh chat or Saved Messages;
- test the canonical URLs exactly;
- if an old cached card persists, test once with a temporary cache-busting query, for example `https://alinahorb.com/?v=20260715` and `https://alinahorb.com/ru/?v=20260715`;
- do not add the query parameter to canonical, hreflang or public navigation links.

Record whether Telegram displays:

- Ukrainian image/title/description for `/`;
- Russian image/title/description for `/ru/`.

If live Telegram interaction is unavailable, state that clearly and provide raw HTML/HTTP evidence instead of claiming success.

## Guardrails

Do not:

- remove `noindex, nofollow`;
- change DNS, CNAME or GitHub Pages settings;
- redesign visible pages;
- change article routes;
- reuse one image for both languages;
- use SVG as `og:image`;
- merge automatically.

## Deliverable

Return:

- PR URL;
- commit SHA;
- exact changed files;
- rendered UA/RU image sizes and byte sizes;
- metadata QA result;
- production or preview screenshots where available;
- Telegram verification result or an explicit statement that Telegram could not be tested.
