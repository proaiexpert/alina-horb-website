# Alina Horb — Psychology Practice Website

A calm, human-first bilingual website for psychologist **Alina Horb**, designed around trust, clear professional boundaries, natural Ukrainian and Russian localization, and a low-pressure first-contact experience.

**Status:** Live client project · UA/RU  
**Live website:** [Ukrainian](https://alinahorb.com/) · [Russian](https://alinahorb.com/ru/)  
**ProAI Expert case study:** [Alina Horb](https://proai-expert.com/case-studies/alina-horb/)

![Alina Horb psychology practice website](assets/images/social/alina-horb-og-ua-v1.jpg)

## Project overview

The project translates a personal psychology practice into a restrained editorial digital experience rather than a generic clinic template. The site helps visitors understand Alina’s approach, consultation format, areas of support, professional boundaries, educational materials, and available contact paths without using pressure-based conversion tactics.

The production domain is live with HTTPS. Search indexing remains intentionally disabled in the current source through `noindex, nofollow` until a separate launch review confirms that the editorial, privacy, contact, and SEO gates are ready.

## Business and user goals

- establish a credible personal brand for an independent psychologist;
- make the consultation format and first step easier to understand;
- support Ukrainian- and Russian-speaking visitors with natural localized experiences;
- communicate sensitive topics carefully without diagnostic or outcome claims;
- provide a readable educational Notes layer;
- maintain a lightweight system that is accessible, auditable, and inexpensive to operate.

## What was delivered

- premium **Editorial Sanctuary** brand and interface direction;
- Ukrainian primary experience and independent Russian localization;
- responsive homepage architecture from mobile through wide desktop;
- clear consultation, process, FAQ, professional-boundary, and contact sections;
- bilingual Notes hubs and localized article routes;
- structured first-contact pathways and direct contact options;
- approved portrait, logo, diploma, and editorial asset system;
- keyboard support, visible focus states, reduced-motion handling, and no-JavaScript fallbacks;
- custom-domain GitHub Pages deployment with apex and `www` routing.

## Language and search architecture

The Ukrainian version is the primary editorial source. Russian pages are maintained as natural localizations rather than mechanical line-by-line copies.

The implementation includes:

- separate UA and RU routes;
- reciprocal language switching;
- page-specific titles and descriptions;
- self-referencing canonicals;
- reciprocal `hreflang` relationships;
- `x-default` pointing to the Ukrainian experience;
- localized Notes and article paths;
- a controlled indexing gate that remains closed until launch approval.

## Trust, privacy, and safety boundaries

The public experience is designed for ordinary first contact and educational reading. It is **not an emergency service or crisis-response system**.

The repository must not introduce:

- diagnosis from symptom lists;
- guaranteed outcomes or treatment claims;
- unsupported credentials or specializations;
- absolute confidentiality promises;
- invented client results, reviews, or rankings;
- private client, medical, intake, or credential data.

Immediate-danger language must direct visitors to appropriate local emergency or crisis services rather than implying that the website or contact form can provide urgent support.

## Technical approach

The site intentionally uses a small static stack:

- semantic HTML5;
- shared responsive CSS;
- minimal vanilla JavaScript;
- no framework, CMS, database, npm dependency, or build step;
- optimized local production assets;
- GitHub-based review and GitHub Pages deployment.

This approach keeps the implementation transparent, fast, maintainable, and easy to audit.

## Accessibility and responsive behavior

Major changes should preserve:

- logical heading structure and one H1 per page;
- keyboard navigation and visible focus;
- readable contrast and typography;
- complete content with JavaScript disabled;
- `prefers-reduced-motion` behavior;
- mobile, tablet, desktop, and low-height landscape usability;
- working language, navigation, FAQ, and contact paths.

## Current repository status

This repository is the canonical production source for `alinahorb.com`.

The live website, bilingual structure, responsive homepage, Notes routes, custom domain, and public asset system are implemented. Indexing remains deliberately paused until a dedicated launch decision is made. Planned work must not be described as already implemented.

Detailed governance and implementation records remain under `docs/`, including:

- [`docs/PROJECT_SOURCE_OF_TRUTH.md`](docs/PROJECT_SOURCE_OF_TRUTH.md)
- [`docs/V3_2_RESEARCH_SYNTHESIS.md`](docs/V3_2_RESEARCH_SYNTHESIS.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`docs/PROJECT_HISTORY.md`](docs/PROJECT_HISTORY.md)

## Role of ProAI Expert

**ProAI Expert** led the project’s positioning, information architecture, visual direction, bilingual system design, responsive implementation coordination, technical governance, and quality-review framework.

- ProAI Expert: https://proai-expert.com/
- Project case study: https://proai-expert.com/case-studies/alina-horb/

## Credits

- Psychologist and content owner: **Alina Horb**
- Strategy, design direction, and implementation coordination: **ProAI Expert**
