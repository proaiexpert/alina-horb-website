# Alina Horb Website — Roadmap

Last updated: 2026-07-14

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

The site is publicly available but intentionally remains `noindex, nofollow` until the release gates below are complete.

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

**Status: Active release gate**

Required work:

- Ukrainian privacy-policy page;
- Russian privacy-policy page;
- review of service-information or terms content where appropriate;
- confirmation of jurisdiction and client-location limits;
- review of minors, couples, confidentiality, records, and acute-risk procedures;
- replace temporary `mailto:` form with a privacy-reviewed endpoint;
- minimal data collection;
- server-side validation;
- anti-spam protection;
- clear success and error states;
- provider and retention disclosure;
- warning not to submit medical, crisis, or emergency information.

Telegram remains the primary direct channel.

`noindex, nofollow` must remain until this phase is approved.

---

## Phase 8 — Notes index V3.2

**Status: Planned**

Required work:

- editorial Notes hero and short positioning copy;
- one featured article plus three supporting cards;
- unique optimized image for each article;
- category and reading time;
- strong hover/focus states;
- consistent UA/RU layouts;
- responsive behavior without horizontal carousel;
- homepage header/footer parity;
- internal links to consultation process, FAQ, support areas, and contact;
- accessibility and reduced-motion QA.

---

## Phase 9 — Shared article template V3.2

**Status: Planned**

Implement one shared article system for all four UA and four RU routes.

Required:

- category, reading time, and strong deck;
- direct answer in the first 80–120 words;
- unique editorial hero image;
- 680–740 px comfortable reading measure on desktop;
- structured H2/H3 hierarchy;
- contents rail on desktop and static contents block on mobile where useful;
- pull quote or explanatory block;
- practical preparation/self-observation section where appropriate;
- educational/diagnostic boundary;
- author block with confirmed credential;
- publication and meaningful update dates;
- related articles;
- contextual links to process, FAQ, support areas, Notes, and contact;
- calm CTA;
- article-specific safety notice only where relevant;
- keyboard/focus accessibility and `prefers-reduced-motion` support.

Existing routes should remain stable unless a redirect plan explicitly approves changes.

---

## Phase 10 — Article editorial production

**Status: Planned**

Recommended editing order:

1. What happens during the first consultation
2. How to begin when the request is difficult to formulate
3. When familiar coping strategies stop helping
4. Stress, relocation, and loss of familiar support

Required work:

- Ukrainian as the primary canonical editorial version;
- natural independent Russian localization;
- remove generic AI phrasing and repetition;
- verify terminology, evidence, and safety boundaries;
- article-specific title, H1, H2/H3, meta description, and anchor text;
- calm non-manipulative CTA;
- source ledger for clinically sensitive claims;
- final confirmation of factual statements about Alina's process and scope.

---

## Phase 11 — SEO and AI-search readiness

**Status: Planned release gate**

Required work:

- unique title and meta description for every route;
- canonical and reciprocal hreflang verification;
- Open Graph and social-preview assets;
- accurate `Article`/`BlogPosting`, `BreadcrumbList`, `Person`, and `WebSite` structured data;
- visible author identity and meaningful dates;
- contextual internal-link architecture;
- representative image dimensions and alt text;
- concise answer blocks written for humans first;
- sitemap coverage;
- robots review;
- no keyword stuffing, fabricated expertise, diagnosis, or treatment promises.

Do not use medical schema types that misrepresent Alina or the site.

---

## Phase 12 — Search launch

**Status: Release gate**

Only after privacy/form/editorial/SEO approval:

- finalize `robots.txt`;
- finalize `sitemap.xml`;
- remove `noindex, nofollow` in a dedicated release commit;
- submit sitemap to Google Search Console;
- verify canonical selection and indexing;
- verify social previews;
- run final mobile, tablet, laptop, desktop, Safari, Chromium, and WebKit QA;
- confirm production form delivery and anti-spam behavior;
- verify direct URLs for all versioned assets.

---

## Phase 13 — Post-launch iteration

**Status: Planned**

Potential work after stable launch:

- privacy-conscious analytics;
- Search Console review;
- article expansion based on real search questions;
- conversion-path refinement;
- accessibility follow-up;
- performance-budget review;
- authentic photography expansion;
- appointment or CRM integration only after the contact workflow is stable.

## Non-goals

The project should not become:

- a generic medical portal;
- an over-animated agency showcase;
- a diagnosis or treatment-claim website;
- an emergency-service substitute;
- a collection of random stock imagery;
- a framework-heavy application without a clear operational need;
- a mass-produced SEO or AI-content system.
