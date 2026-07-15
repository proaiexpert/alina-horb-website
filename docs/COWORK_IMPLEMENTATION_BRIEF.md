# Cowork Implementation Brief — Alina Horb Homepage v1

## Objective

Build the complete first production-quality homepage implementation for `alinahorb.com` from the approved desktop visual direction.

This is an implementation task, not a redesign.

## Source workspace

Google Drive root:

https://drive.google.com/drive/folders/1AycAWP2nHi97SHovYvmQ8GZE4q3rbeLh

Project folder:

`AlinaHorbwebsite/alina-horb-website/`

## Required source-of-truth files

Read before writing code:

- `02_BRIEF_AND_CONTENT/source-of-truth/PROJECT_SOURCE_OF_TRUTH.md`
- `02_BRIEF_AND_CONTENT/source-of-truth/CONTENT_STATUS.md`
- `02_BRIEF_AND_CONTENT/source-of-truth/UNRESOLVED_QUESTIONS.md`
- `02_BRIEF_AND_CONTENT/visual-direction/VISUAL_DIRECTION.md`
- `02_BRIEF_AND_CONTENT/visual-direction/alina-horb-final-desktop-visual-direction-v1.jpg`
- `00_PROJECT_ADMIN/reports/ALINA_HORB_ASSET_MANIFEST.md`
- `00_PROJECT_ADMIN/reports/ALINA_HORB_LOGO_ASSET_MANIFEST`

## Public assets allowed

Use only files from `web-ready` folders.

### Logo

`01_INPUT_ASSETS/logo/web-ready/`

- `alina-horb-logo-ru-dark.png`
- `alina-horb-logo-ru-light.png`
- `alina-horb-logo-ua-dark.png`
- `alina-horb-logo-ua-light.png`

### Portrait

`01_INPUT_ASSETS/portrait/web-ready/`

- `alina-horb-portrait-hero-1600.webp`
- `alina-horb-portrait-hero-1600.jpg`

### Diploma

`01_INPUT_ASSETS/diploma/web-ready/`

- `alina-horb-diploma-public-1600.webp`
- `alina-horb-diploma-public-1600.jpg`

Never use or copy private/original diploma files into the site project.

## Technical stack

Use:

- Astro with TypeScript;
- static output;
- semantic HTML;
- plain scoped/global CSS;
- no React, Vue or heavy UI framework;
- no CMS;
- no database;
- no external form service at this stage.

The finished project must build with:

```bash
npm install
npm run dev
npm run build
```

## Project structure

Use a clear structure similar to:

```text
src/
  components/
    BrandHeader.astro
    Hero.astro
    TrustRow.astro
    SupportIndex.astro
    About.astro
    Education.astro
    Process.astro
    PrinciplesFaq.astro
    FinalCta.astro
    Footer.astro
  data/
    site.ru.ts
    site.ua.ts
  layouts/
    BaseLayout.astro
  pages/
    index.astro
    ua/
      index.astro
  styles/
    global.css
public/
  assets/
    logo/
    portrait/
    diploma/
README.md
QA_REPORT.md
```

The exact structure may differ slightly, but content must remain separate from layout components.

## Language implementation

Phase 1 priority is the Russian homepage at `/`.

Prepare the Ukrainian route architecture at `/ua/`, but do not invent final Ukrainian copy and do not use unreviewed machine translation as approved content.

Requirements:

- RU/UA switch is visible in the approved position;
- Russian page links to `/`;
- Ukrainian route may use clearly marked working copy internally;
- all UA text must be isolated in `site.ua.ts` for later replacement;
- no browser-language auto-redirect;
- no automatic translation widget.

## Homepage sections

Implement the full approved sequence:

1. Editorial hero with integrated navigation.
2. Typographic trust row.
3. Numbered support-needs index 01–05.
4. About section and quote.
5. Education and public redacted diploma.
6. Four-step consultation process.
7. Principles of work and FAQ.
8. Final CTA.
9. Minimal footer with maker credit.

Do not add new sections or reorder existing sections.

## Critical visual rules

- Follow `Final Desktop Visual Direction v1.0` closely.
- Preserve the asymmetric editorial hero.
- Preserve the arched portrait treatment.
- Do not introduce a standard full-width navigation bar.
- Do not turn support items into generic cards.
- Do not compress the page vertically.
- Preserve generous whitespace and a slow editorial rhythm.
- Use warm ivory, graphite, muted sage and restrained terracotta.
- Avoid gradients, glassmorphism, heavy shadows, neon, gold effects and generic icon grids.
- Use thin rules and restrained oval/arch motifs only where present in the approved direction.
- Do not rasterize the mockup or build the page as one image.

## Typography

Use a high-contrast editorial serif for display headings and a restrained sans-serif for UI/body copy.

Preferred implementation:

- Cormorant Garamond for display typography;
- Manrope for sans-serif text;
- self-host through package/local assets rather than remote Google Fonts requests.

Use fluid typography with `clamp()` and preserve readable body sizes.

## Content rules

Use working text from the approved mockup and source-of-truth files.

Do not publish or introduce:

- `7 years of experience` until confirmed;
- work with children, adolescents, couples or families;
- trauma-specialist claims;
- emergency-service claims;
- worldwide-service claims;
- fixed offline location;
- diagnoses, treatment or guaranteed outcomes;
- testimonials, ratings or invented proof;
- unconfirmed certificates or licenses.

For the trust row, replace the unconfirmed numbered experience claim with a neutral phrase such as `практический опыт`, keeping similar visual width.

Keep all copy in data files so it can be replaced without rebuilding components.

## CTA behavior

The confirmed booking channel is Telegram, but the exact Telegram URL is pending.

Until supplied:

- centralize the CTA destination in one config/data value;
- use `mailto:hello@alinahorb.com` as the temporary functional fallback;
- add a source-code TODO for replacement with the exact Telegram URL;
- do not display a fake Telegram username.

## Footer

Include:

- approved Alina Horb logo;
- RU / UA switch;
- `alinahorb.com`;
- `hello@alinahorb.com`;
- privacy-policy link placeholder;
- `© Алина Горб, 2026`;
- thin premium ProAI Expert maker credit;
- maker-credit link: `https://proai-expert.com/`.

Do not add phone, address, social-media icons or extra promotional text.

## Editorial image placeholders

The approved mockup contains neutral vase/books editorial imagery that is not yet supplied as a separate production asset.

For this first implementation:

- create restrained CSS placeholder surfaces with the same approximate composition and aspect ratio;
- do not download random stock photography;
- do not generate synthetic client/therapy imagery;
- keep replacement points clearly named in code;
- do not crop those images from the low-resolution mockup for production use.

## Responsive requirements

Implement and test at:

- 320 px;
- 360 px;
- 375 px;
- 390 px;
- 430 px;
- 768 px;
- 1024 px;
- 1280 px;
- 1440 px.

Requirements:

- no horizontal overflow;
- `document.documentElement.scrollWidth <= viewport width`;
- typography remains readable;
- hero hierarchy remains clear;
- portrait crop remains natural;
- navigation becomes a compact accessible mobile control;
- sections stack without becoming generic cards;
- timeline remains understandable;
- FAQ controls remain touch-friendly;
- footer does not become cramped.

## Accessibility

- one clear H1;
- semantic section headings;
- keyboard-accessible navigation and FAQ;
- visible focus states;
- sufficient contrast;
- descriptive alt text;
- width/height attributes for images;
- reduced-motion support;
- buttons and links must have accessible names;
- no important text embedded in images.

## Performance

- use `<picture>` with WebP plus JPEG fallback;
- preload only the hero image when justified;
- lazy-load below-the-fold images;
- avoid unnecessary JavaScript;
- avoid layout shifts;
- optimize font loading;
- target a static, lightweight build.

## SEO foundation

Prepare:

- page title and description placeholders from the content source of truth;
- canonical placeholder for `https://alinahorb.com/`;
- RU/UA alternate-link structure;
- Open Graph placeholders;
- semantic headings;
- JSON-LD placeholder only for confirmed facts;
- no ranking promises;
- no unconfirmed LocalBusiness address.

Do not configure final deployment or domain DNS.

## Output location

Save the complete project to:

`AlinaHorbwebsite/alina-horb-website/03_COWORK_OUTPUT/current/alina-horb-site-v1/`

Also create:

- `README.md` with setup/build instructions;
- `QA_REPORT.md` with completed checks, remaining TODOs and known limitations;
- `ASSET_USAGE.md` listing every copied public asset and confirming that no private files were included.

Do not save only a ZIP. Save the complete unpacked project folder.

A ZIP archive may be added as a secondary backup after the unpacked project exists.

## Final verification

Before reporting completion:

- run the development build;
- run the production build;
- verify all referenced local assets exist;
- verify no private assets were copied;
- verify the diploma number is not visible;
- verify no horizontal overflow at required widths;
- verify all links and controls behave predictably;
- verify no lorem ipsum;
- verify no invented facts;
- verify the desktop result remains recognizably faithful to the approved mockup.

## Final report

Report:

1. status: SUCCESS / PARTIAL / FAILED;
2. exact output path;
3. technical stack and versions used;
4. build commands and results;
5. files created;
6. public assets copied;
7. confirmation that private assets were excluded;
8. responsive widths tested;
9. unresolved visual/content TODOs;
10. links to the project folder, README and QA report.

Do not push to GitHub, configure deployment or change the approved design without a separate instruction.
