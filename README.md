# Alina Horb — Psychology Practice Website

Premium bilingual website for psychologist **Alina Horb**, designed as a calm editorial environment for learning about her practice, areas of support, consultation process, professional boundaries, notes, and contact options.

> **Current status:** public review preview. The site is intentionally served with `noindex, nofollow` until the official domain, final editorial review, legal pages, and production SEO are complete.

## Live preview

- Ukrainian: https://proaiexpert.github.io/alina-horb-website/
- Russian: https://proaiexpert.github.io/alina-horb-website/ru/
- Planned production domain: https://alinahorb.com/

## Project goals

The project is intended to provide:

- a clear and trustworthy personal website for a practicing psychologist;
- a premium but restrained visual identity without clinical or corporate coldness;
- separate natural Ukrainian and Russian editorial versions;
- transparent information about format, price, duration, professional boundaries, and first contact;
- careful communication around crisis, trauma, anxiety, OCD manifestations, panic attacks, war-related displacement, and domestic violence;
- an editorial notes layer for future long-form educational content and organic search visibility;
- a lightweight, accessible, maintainable static implementation.

## Brand direction

The approved visual system is called **Premium Editorial Sanctuary**.

Its core principles are:

- quiet luxury rather than decorative luxury;
- warm ivory surfaces, graphite typography, restrained terracotta, and muted sage;
- editorial serif typography paired with a clean sans-serif interface layer;
- generous spacing, asymmetric composition, thin rules, and numbered navigation;
- one authentic personal brand rather than a generic clinic template;
- restrained motion that supports reading and respects `prefers-reduced-motion`.

Reference roles:

- **Kinfolk** — editorial composition, typography, pacing, and whitespace;
- **Oura** — organic geometry, visual storytelling, and controlled interaction;
- **Portland Talk Club** — psychological content clarity, recognizable situations, FAQ, and contact logic.

## Current information architecture

1. Hero
2. Trust strip
3. When support may be needed
4. Areas of work
5. About Alina
6. Education and public redacted diploma
7. Consultation process
8. Principles and professional boundaries
9. FAQ
10. Notes
11. Contacts and consultation form
12. Final call to action
13. Footer

The Ukrainian homepage is primary. The Russian version is maintained as a separate editorial page, not generated through JavaScript translation.

## Confirmed practice information

- Practice wording: **since 2016**
- Degree: **Master of Psychology**
- Consultation languages: **Ukrainian and Russian**
- Main format: **online**
- In-person format: **by prior agreement**
- Duration: **50 minutes**
- Price: **600 UAH**
- Audience wording: **people of different ages, couples, and families**
- Work with minors: **agreed separately**

Current contact channels:

- Telegram: `@alina_horb1991`
- Instagram: `@ng_alina_dp`
- Email: `alinahorb1991@gmail.com`

## Areas of support

The website currently presents careful, non-diagnostic wording around:

- people affected by war, including internally displaced persons;
- acute and chronic stress;
- panic attacks and their consequences;
- anxiety states and support with diagnosed anxiety disorders;
- traumatic experience and PTSD symptoms;
- intrusive thoughts, rituals, and OCD manifestations;
- domestic violence;
- crises, relationships, and family requests;
- primary psychological support during acute stress;
- repeated suicidal or self-harm thoughts with a clear emergency disclaimer.

The site and contact form are **not emergency services**. The copy directs users to local emergency or crisis services when there is immediate danger, a concrete plan, or inability to remain safe.

## Current features

- Ukrainian homepage at `/`
- Russian homepage at `/ru/`
- reciprocal language switching
- semantic section navigation
- mobile hamburger navigation
- mobile booking CTA that appears after the hero CTA leaves the viewport
- accessible FAQ accordions
- restrained section reveal and process-line animation
- `prefers-reduced-motion` support
- public redacted diploma preview
- editorial Notes index and four current draft article routes per language
- Telegram, Instagram, and email contact paths
- compact bilingual consultation form
- responsive layouts from mobile through wide desktop
- automated GitHub Pages deployment
- local asset validation in CI

## Technical architecture

The project intentionally uses a minimal static stack:

- semantic HTML5;
- shared CSS;
- minimal vanilla JavaScript;
- no framework;
- no CMS;
- no database;
- no npm dependency;
- no build step.

This keeps the site fast, transparent, inexpensive to host, and easy to audit.

### Main files

```text
index.html                         Ukrainian homepage
ru/index.html                      Russian homepage
notes/                             Ukrainian Notes index and articles
ru/notes/                          Russian Notes index and articles
assets/css/site.v2.css             shared visual system
assets/js/site.v2.js               navigation, FAQ, motion, form behavior
assets/js/site-config.v2.js        shared contact configuration
assets/images/                     public production assets
docs/                              governance, decisions, QA, and roadmap
scripts/validate-assets.py         local asset-reference validator
.github/workflows/deploy-pages.yml GitHub Pages deployment
```

## Local development

Run a local static server from the repository root:

```bash
python3 -m http.server 8080
```

Open:

- http://127.0.0.1:8080/
- http://127.0.0.1:8080/ru/

Do not review the pages through `file://` because relative routes, language links, and browser security behavior may differ.

## Contact form status

The current preview form prepares a localized email message and opens the visitor's configured email client. It does not yet use a server-side form endpoint and does not store submissions.

Before production release, the form must move to a privacy-reviewed endpoint with:

- server-side validation;
- anti-spam protection;
- clear success and error states;
- minimal data collection;
- documented provider and retention behavior.

Telegram remains the preferred direct contact channel.

## Deployment

GitHub Pages deploys from `main` through:

```text
.github/workflows/deploy-pages.yml
```

The deployment publishes the website files directly from the repository. It must not depend on Google Drive, local ZIP files, private source assets, or external build artifacts.

Changed public assets should use versioned filenames rather than silently replacing old files under the same URL.

## QA expectations

Major visual or structural changes are reviewed at:

- 390 px
- 768 px
- 1024 px
- 1280 px
- 1366 px
- 1440 px

Required checks include:

- broken images: `0`
- local asset 404s: `0`
- console/runtime errors: `0`
- horizontal overflow: `0`
- one H1 per page
- logical H2/H3 hierarchy
- keyboard navigation and visible focus
- functional language switching
- functional hamburger navigation and mobile booking CTA
- reduced-motion behavior
- correct public-only asset usage

## Public asset policy

Allowed in the repository:

- approved localized logos;
- optimized public portrait derivatives;
- public redacted diploma derivatives;
- editorial and decorative website assets.

Never commit:

- private portrait originals unless explicitly approved as public production sources;
- unredacted diploma files;
- diploma numbers or registration identifiers;
- credentials, tokens, cookies, or private configuration;
- source archives or private ZIP packages;
- medical or client information.

## Current development wave

The active large implementation task is:

- [Issue #15 — V3.1 Wave 1: Homepage Content & Visual Polish](https://github.com/proaiexpert/alina-horb-website/issues/15)

V3.1 includes:

- a new seated-with-book Hero portrait;
- a separate close About portrait;
- natural UA/RU homepage editing;
- typography and readability refinement;
- diploma and principles-section polish;
- restrained motion refinement;
- preservation of footer, mobile CTA, accessibility, and preview safeguards.

## Roadmap

Detailed project phases and release gates are maintained in:

- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`docs/PROJECT_HISTORY.md`](docs/PROJECT_HISTORY.md)
- [`docs/PROJECT_SOURCE_OF_TRUTH.md`](docs/PROJECT_SOURCE_OF_TRUTH.md)

High-level next waves:

1. **Homepage V3.1** — content and visual polish
2. **Notes and articles** — full UA/RU editorial rewrite and article-specific visuals
3. **SEO and AI-search** — titles, descriptions, schema, internal linking, author data, and content QA
4. **Privacy and production form** — legal pages and real form delivery
5. **Domain and release** — connect `alinahorb.com`, verify deployment, remove preview `noindex`, submit sitemap
6. **Post-launch iteration** — analytics-informed improvements without weakening privacy or editorial quality

## Governance

Production decisions are governed by:

1. the latest confirmed information from Alina;
2. `docs/PROJECT_SOURCE_OF_TRUTH.md`;
3. approved design and content decisions;
4. reviewed GitHub issues and pull requests.

Large changes are implemented in feature branches and reviewed through pull requests. Small reversible fixes may be merged independently when they do not conflict with an active implementation branch.

## Credits

- Psychologist and content owner: **Alina Horb**
- Strategy, design direction, implementation coordination: **ProAI Expert**
- Development credit: https://proai-expert.com/
