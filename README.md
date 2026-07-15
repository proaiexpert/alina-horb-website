# Alina Horb — Psychology Practice Website

Premium bilingual website for psychologist **Alina Horb**, designed as a calm editorial environment for learning about her practice, areas of support, consultation process, professional boundaries, Notes, and contact options.

> **Current status:** the production domain is connected and HTTPS is active. The site intentionally remains `noindex, nofollow` until privacy/legal pages, the production contact workflow, final article editing, and SEO launch review are complete.

## Production website

- Ukrainian: https://alinahorb.com/
- Russian: https://alinahorb.com/ru/
- `www`: https://www.alinahorb.com/ redirects to the apex domain

The former GitHub Pages project URL redirects to the production domain.

## Project goals

The project is intended to provide:

- a clear and trustworthy personal website for a practicing psychologist;
- a premium but restrained visual identity without clinical or corporate coldness;
- separate natural Ukrainian and Russian editorial versions;
- transparent information about format, price, duration, professional boundaries, and first contact;
- careful communication around crisis, trauma, anxiety, OCD manifestations, panic attacks, war-related displacement, and domestic violence;
- an editorial Notes layer for educational content and future organic-search visibility;
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
- **Portland Talk Club** — psychological-content clarity, recognizable situations, FAQ, and contact logic.

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

These statements must not be expanded into specialization, diagnosis, treatment, jurisdiction, or outcome claims without explicit confirmation and evidence.

The site and contact form are **not emergency services**. Copy must direct users to local emergency or crisis services when there is immediate danger, a concrete plan, or inability to remain safe.

## Current features

- Ukrainian homepage at `/`
- Russian homepage at `/ru/`
- reciprocal language switching
- shared desktop and mobile navigation
- mobile booking CTA
- accessible FAQ accordions
- restrained reveal and process-line motion
- `prefers-reduced-motion` support
- approved Hero and About portrait derivatives
- public redacted diploma preview
- Notes index and four current article routes per language
- Telegram, Instagram, and email contact paths
- compact bilingual consultation form
- responsive layouts from mobile through wide desktop
- automated GitHub Pages deployment
- local asset-reference validation in CI
- production domain, HTTPS, apex/`www`, and GitHub Pages redirects

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
assets/css/site.v3-1.css           current homepage V3.1 visual layer
assets/css/site.v2.css             older shared Notes/article layer pending V3.2
assets/js/site.v2.js               navigation, FAQ, motion, and form behavior
assets/js/site-config.v2.js        shared contact configuration
assets/images/                     public production assets
favicon.svg                        production favicon copied by Pages workflow
docs/                              governance, research, decisions, QA, and roadmap
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

Do not review pages through `file://` because relative routes, language links, and browser security behavior may differ.

## Contact form status

The current form prepares a localized email message and opens the visitor's configured email client. It does not use a server-side form endpoint and does not store submissions.

Before search launch, the form must move to a privacy-reviewed endpoint with:

- server-side validation;
- anti-spam protection;
- clear success and error states;
- minimal data collection;
- documented provider and retention behavior;
- explicit handling boundaries for crisis or sensitive information.

Telegram remains the preferred direct contact channel.

## Deployment

GitHub Pages deploys from `main` through:

```text
.github/workflows/deploy-pages.yml
```

The deployment publishes website files directly from the repository. It must not depend on Google Drive, local ZIP files, private source assets, or external build artifacts.

Changed public assets should use versioned filenames rather than silently replacing old files under the same URL.

### Production routing

Expected behavior:

- `http://alinahorb.com/` redirects to HTTPS;
- `https://alinahorb.com/` serves the Ukrainian homepage;
- `https://alinahorb.com/ru/` serves the Russian homepage;
- `https://www.alinahorb.com/` redirects to the apex domain;
- the former GitHub Pages project URL redirects to `alinahorb.com`.

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
- local/production asset 404s: `0`
- console/runtime errors: `0`
- horizontal overflow: `0`
- one H1 per page
- logical H2/H3 hierarchy
- keyboard navigation and visible focus
- functional language switching
- functional navigation, FAQ, form, and mobile booking CTA
- reduced-motion behavior
- correct public-only asset usage
- correct HTTPS and redirect behavior

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

The active roadmap is:

- [Issue #19 — V3.2: Editorial Notes, Article System & Premium Site Polish](https://github.com/proaiexpert/alina-horb-website/issues/19)

The V3.1 homepage, responsive stabilization, global navigation/footer, production domain, HTTPS, and favicon deployment are complete.

V3.2 now focuses on:

- Notes-index redesign;
- one shared premium article system for all UA/RU articles;
- native Ukrainian editorial refinement and natural Russian localization;
- article-specific visuals;
- evidence, safety, author, dates, internal links, and structured data;
- privacy/legal pages and a production contact endpoint;
- final SEO and indexing release gate.

## Research and editorial governance

The July 2026 Deep Research Pack has been reduced into an implementation standard:

- [`docs/V3_2_RESEARCH_SYNTHESIS.md`](docs/V3_2_RESEARCH_SYNTHESIS.md)

Key adopted rules:

- no diagnosis from symptom lists;
- no universal time threshold;
- no guaranteed outcome;
- no fixed first-session script unless confirmed by Alina;
- no absolute confidentiality claim;
- no universal migration stages or automatic trauma claims;
- Ukrainian is the primary canonical editorial version;
- Russian is an independent natural localization;
- health and safety claims use primary or authoritative sources;
- `noindex, nofollow` remains until privacy, form, editorial, and SEO gates are approved.

## Roadmap

Detailed project phases and release gates are maintained in:

- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`docs/PROJECT_HISTORY.md`](docs/PROJECT_HISTORY.md)
- [`docs/PROJECT_SOURCE_OF_TRUTH.md`](docs/PROJECT_SOURCE_OF_TRUTH.md)
- [`docs/V3_2_RESEARCH_SYNTHESIS.md`](docs/V3_2_RESEARCH_SYNTHESIS.md)

High-level next order:

1. verify post-domain production deployment and favicon;
2. prepare UA/RU privacy and production form workflow;
3. rebuild Notes under V3.2;
4. implement one article template for all eight routes;
5. complete UA/RU editorial, evidence, safety, and SEO review;
6. finalize sitemap/robots/Search Console and remove `noindex` in a dedicated launch commit;
7. perform post-launch measurement and iteration.

## Governance

Production decisions are governed by:

1. the latest confirmed information from Alina;
2. `docs/PROJECT_SOURCE_OF_TRUTH.md`;
3. `docs/V3_2_RESEARCH_SYNTHESIS.md` for article evidence and safety;
4. approved design and content decisions;
5. reviewed GitHub issues and pull requests.

Large changes are implemented in feature branches and reviewed through pull requests. Small reversible fixes may be merged independently when they do not conflict with active implementation work.

## Credits

- Psychologist and content owner: **Alina Horb**
- Strategy, design direction, implementation coordination: **ProAI Expert**
- Development credit: https://proai-expert.com/
