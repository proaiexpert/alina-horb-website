# Alina Horb Website — Roadmap

Last updated: 2026-10-06

This roadmap separates completed foundations, active work, release gates, and post-launch improvements. It is not a marketing promise or release-date commitment.

## Status legend

- **Complete** — merged into `main` and available on the production domain
- **Active** — implementation or review currently in progress
- **Planned** — approved direction, not yet completed
- **Release gate** — must be complete before search indexing

---

## Phase 1 — Repository and bilingual foundation

**Status: Complete**

Delivered:

- public GitHub repository;
- Ukrainian primary route at `/`;
- Russian route at `/ru/`;
- separate manually maintained language versions;
- GitHub Pages deployment;
- responsive base layout;
- language switching;
- public-only asset policy;
- asset-reference validation.

---

## Phase 2 — Premium Editorial Sanctuary V2

**Status: Complete**

Delivered:

- approved editorial visual direction;
- Hero, trust strip, support, topics, About, diploma, process, principles, FAQ, Notes, contacts, CTA, and footer;
- Cormorant Garamond + Manrope typography;
- ivory, graphite, terracotta, and muted sage palette;
- responsive navigation and FAQ;
- restrained section motion;
- public redacted diploma display;
- initial Notes and article routes.

---

## Phase 3 — Contacts, safety, and mobile conversion

**Status: Complete**

Delivered:

- Telegram `@alina_horb1991`;
- Instagram `@ng_alina_dp`;
- current email contact;
- expanded confirmed areas of support;
- careful wording around PTSD, OCD manifestations, anxiety disorders, panic attacks, war-related displacement, domestic violence, and suicidal thoughts;
- emergency-service disclaimer;
- audience wording and separate agreement for work with minors;
- compact footer;
- restrained ProAI Expert credit;
- mobile booking CTA with safe-area handling;
- CTA suppression near Contacts and Footer.

---

## Phase 4 — Homepage V3.1 and production stabilization

**Status: Complete**

Delivered:

- approved seated-with-book Hero portrait;
- separate About portrait;
- natural UA/RU homepage editing;
- typography and readability refinement;
- portrait-tablet layout correction;
- sticky overlap correction;
- footer and facts-grid refinement;
- global navigation/footer/favicon standardization;
- direct asset and responsive QA;
- favicon deployment fix.

Completed through PRs including #17, #18, #20, #21, #22, and #23.

Do not reopen the homepage as a broad redesign without a concrete production regression.

---

## Phase 5 — Production domain and HTTPS

**Status: Complete**

Delivered:

- `alinahorb.com` purchase and connection;
- apex DNS configuration;
- `www` redirect to apex;
- HTTP redirect to HTTPS;
- valid TLS for apex and `www`;
- former GitHub Pages URL redirect to the production domain;
- canonical and hreflang production-domain references;
- favicon included in the Pages artifact.

The site is publicly available and the 16 public UA/RU routes are technically indexable. The two privacy-policy routes remain intentionally `noindex, follow`.

---

## Phase 6 — V3.2 research and editorial governance

**Status: Complete**

Tracking:

- [Issue #19 — V3.2: Editorial Notes, Article System & Premium Site Polish](https://github.com/proaiexpert/alina-horb-website/issues/19)
- [`V3_2_RESEARCH_SYNTHESIS.md`](V3_2_RESEARCH_SYNTHESIS.md)

Delivered:

- research-backed editorial sequence for the four article topics;
- four-level safety model;
- claim and language restrictions;
- source hierarchy and maintenance policy;
- article-specific intent, structure, and safety guidance;
- localization, author, dates, internal-link, and structured-data requirements;
- Alina confirmation gates.

The raw research pack is supporting material. The synthesis document is the adopted implementation standard.

---


## Phase 7 — Privacy, legal, and production form

**Status: Active — technical implementation complete; client/professional confirmations remain**

Delivered:

- Ukrainian and Russian privacy-policy pages;
- production Formspree endpoint;
- minimal intake fields, client-side validation, honeypot/timing protections and request timeout;
- Cloudflare Turnstile anti-spam protection;
- localized success/error/fallback states;
- provider and retention disclosure;
- warnings not to submit medical documents, payment data or detailed crisis information;
- automated form/runtime QA.

Remaining external confirmations:

- jurisdiction and client-location limits;
- detailed minors and couples policy;
- confidentiality exceptions and records/notes practice;
- acute-risk and emergency escalation procedures;
- final confirmation of production mailbox delivery where account-level verification is required.

Telegram remains a direct contact channel. Public search routes remain indexable; privacy-policy routes remain intentionally `noindex, follow`.
---


## Phase 8 — Notes index V3.2

**Status: Complete**

Delivered:

- bilingual editorial Notes hubs;
- one featured article plus three supporting cards;
- unique optimized imagery for all four topics;
- category and reading-time metadata;
- responsive editorial layouts without a horizontal carousel;
- global header/footer parity;
- contextual links to consultations and related content;
- keyboard/focus and reduced-motion support;
- Notes image QA and performance/LCP prioritization.
---


## Phase 9 — Shared article template V3.2

**Status: Complete**

Delivered across all four UA and four RU article routes:

- category, reading time, deck and clear H1;
- direct-answer opening;
- unique editorial hero image;
- controlled desktop reading measure;
- structured H2/H3 hierarchy and contents navigation;
- pull quotes/explanatory blocks and practical sections;
- educational/diagnostic boundaries;
- canonical Alina Horb author entity;
- evidence-backed publication/update dates;
- related articles and contextual links;
- calm consultation CTA;
- relevant safety language;
- keyboard/focus and `prefers-reduced-motion` support.

Existing article routes remain stable.
---


## Phase 10 — Article editorial production

**Status: Complete for the current four-article set**

Published in Ukrainian and independently localized in Russian:

1. What happens during the first consultation
2. How to begin when the request is difficult to formulate
3. When familiar coping strategies stop helping
4. Stress, relocation, and loss of familiar support

The current set includes article-specific metadata, internal links, structured author/date data, safety boundaries, source governance and non-manipulative CTAs. Future article expansion should be driven by verified user/search demand rather than mass content production.
---


## Phase 11 — SEO and AI-search readiness

**Status: Complete technical baseline; ongoing only when evidence justifies changes**

Delivered:

- unique titles and meta descriptions across public routes;
- self-canonical and reciprocal UA/RU hreflang with Ukrainian x-default;
- localized Open Graph/Twitter metadata and images;
- accurate WebSite, Person, ProfilePage, Service, Article, FAQ and Breadcrumb structured data where appropriate;
- one canonical Alina Horb Person entity across the site;
- visible author identity and meaningful publication/update dates;
- contextual internal linking;
- explicit image dimensions and descriptive alt text;
- sitemap and robots controls;
- mobile-SERP title cleanup;
- automated SEO/indexing validation and post-deploy live-domain checks.

Do not use medical schema types, keyword stuffing, unsupported expertise, diagnosis claims or outcome promises.
---


## Phase 12 — Search launch

**Status: Technical launch complete; Google Search Console verification pending**

Completed technical launch:

- `robots.txt` and `sitemap.xml` finalized;
- 16 public source and production routes are indexable;
- two privacy-policy routes remain `noindex, follow`;
- source-level indexability no longer depends solely on a deployment transform;
- sitemap freshness and route inventory are validated;
- canonical/hreflang and structured-data checks are enforced in CI;
- strict live-production guard checks the real domain after successful deployment;
- DNS, HTTPS/TLS, redirects and production-form assets are included in live checks;
- responsive/browser regression, performance-readiness and accessibility release gates are in place.

Remaining external verification when account access is available:

- submit/verify the sitemap in Google Search Console;
- inspect coverage for all 16 public URLs;
- confirm Google-selected canonicals and any excluded/crawled-not-indexed reasons;
- request re-indexing only where Search Console evidence shows it is useful.
---

## Phase 13 — Post-launch iteration

**Status: Active maintenance baseline**

Already implemented:

- strict post-deploy live-production SEO guard;
- performance-readiness release gate and Notes LCP prioritization;
- automated axe-core accessibility audit across all 18 UA/RU routes at mobile and desktop sizes;
- WCAG contrast remediation with zero reported accessibility violations in the current audit;
- broad responsive/browser regression QA.

Future work should be evidence-led:

- Google Search Console review once access is restored;
- privacy-conscious analytics only if the owner wants measurement;
- content expansion based on real search/user questions;
- conversion-path refinements based on observed behavior;
- authentic photography expansion when useful;
- appointment/CRM integration only after the contact workflow and business need justify it.


## Non-goals

The project should not become:

- a generic medical portal;
- an over-animated agency showcase;
- a diagnosis or treatment-claim website;
- an emergency-service substitute;
- a collection of random stock imagery;
- a framework-heavy application without a clear operational need;
- a mass-produced SEO or AI-content system.
