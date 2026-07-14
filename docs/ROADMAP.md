# Alina Horb Website — Roadmap

Last updated: 2026-07-14

This roadmap separates completed foundations, active work, production gates, and post-launch improvements. It is not a marketing promise or release-date commitment.

## Status legend

- **Complete** — merged into `main` and available in the public preview
- **Active** — implementation or review currently in progress
- **Planned** — approved direction, not yet completed
- **Release gate** — must be complete before production indexing

---

## Phase 1 — Repository and bilingual foundation

**Status: Complete**

Delivered:

- public GitHub repository;
- Ukrainian primary route at `/`;
- Russian route at `/ru/`;
- separate manually maintained language versions;
- GitHub Pages deployment;
- public preview URLs;
- preview `noindex, nofollow` safeguards;
- responsive base layout;
- language switching;
- public-only asset policy.

Key milestone: bilingual preview implementation and deployment stabilization.

---

## Phase 2 — Premium Editorial Sanctuary V2

**Status: Complete**

Delivered:

- approved editorial visual direction;
- hero, trust strip, support, topics, About, diploma, process, principles, FAQ, Notes, contacts, CTA, and footer;
- Cormorant Garamond + Manrope typography;
- ivory, graphite, terracotta, and muted sage palette;
- responsive navigation and FAQ;
- restrained section motion;
- public redacted diploma display;
- editorial Notes preview and article routes;
- asset validation and responsive QA.

Known limitation addressed during this phase:

- repeated portrait framing and cache problems were stabilized through versioned assets and revised CSS behavior.

---

## Phase 3 — Contacts, safety, and mobile conversion

**Status: Complete**

Delivered:

- confirmed Telegram `@alina_horb1991`;
- confirmed Instagram `@ng_alina_dp`;
- current email contact;
- expanded confirmed areas of support;
- careful wording around PTSD, OCD manifestations, anxiety disorders, panic attacks, war-related displacement, domestic violence, and suicidal thoughts;
- emergency-service disclaimer;
- updated audience wording and separate agreement for work with minors;
- compact footer;
- restrained ProAI Expert credit;
- mobile booking CTA with safe-area handling;
- CTA suppression near Contacts and Footer.

---

## Phase 4 — Homepage V3.1

**Status: Active**

Tracking issue:

- [Issue #15 — V3.1 Wave 1: Homepage Content & Visual Polish](https://github.com/proaiexpert/alina-horb-website/issues/15)

Scope:

- replace the old outdoor Hero portrait with the approved seated-with-book portrait;
- add a separate close portrait to About Alina;
- natural Ukrainian homepage editorial pass;
- separate natural Russian homepage editorial pass;
- typography and microtext audit;
- diploma depth and trust-object refinement;
- principles-section balance;
- restrained motion refinement;
- review generic decorative assets;
- preserve accessibility, footer, mobile CTA, contact channels, and `noindex` safeguards;
- Chromium and WebKit responsive QA.

Acceptance gate:

- one reviewed PR;
- no direct edits to `main` during implementation;
- no broken local assets;
- no console errors;
- no horizontal overflow;
- approved desktop and mobile portrait crops;
- natural fact-consistent UA/RU copy;
- PR remains unmerged until visual review.

---

## Phase 5 — Notes and article editorial production

**Status: Planned**

Current article routes exist as structural drafts. This phase will turn them into publishable content.

Initial subjects:

1. When familiar coping strategies stop helping
2. What happens during the first consultation
3. How to begin when the request is difficult to formulate
4. Stress, relocation, and loss of familiar support

Required work:

- four complete Ukrainian articles;
- four independent Russian editorial versions;
- article-specific H1/H2 structures;
- author information and qualification context;
- updated dates;
- careful health and crisis wording;
- relevant emergency disclaimers;
- article-specific original or approved editorial visuals;
- internal links to consultation process, FAQ, and contact paths;
- article-page responsive and accessibility QA.

---

## Phase 6 — SEO and AI-search architecture

**Status: Planned**

Required work:

- final homepage and article titles;
- meta descriptions;
- canonical URLs;
- reciprocal hreflang verification;
- Open Graph and social preview assets;
- Organization/Person/Article/Breadcrumb schema where appropriate;
- author identity consistency;
- internal-link architecture;
- sitemap and robots review;
- concise question-answer structures for AI search;
- no keyword stuffing or fabricated expertise claims.

Preview pages remain `noindex, nofollow` during this phase.

---

## Phase 7 — Privacy, legal, and production form

**Status: Release gate**

Required work:

- privacy policy;
- terms or service-information page where appropriate;
- contact-form provider review;
- minimal data collection;
- server-side validation;
- anti-spam protection;
- success and error states;
- retention and provider disclosure;
- crisis-data warning;
- review of minors, couples, and cross-border consultation wording;
- confirmation that no medical records or sensitive crisis details are requested through the form.

The current mail-client form remains a preview fallback only.

---

## Phase 8 — Domain and production release

**Status: Release gate**

Required work:

- purchase and configure `alinahorb.com`;
- connect the domain without affecting ProAI Expert infrastructure;
- verify HTTPS;
- update canonical, hreflang, Open Graph, sitemap, and internal absolute URLs;
- verify both language routes;
- remove `noindex, nofollow` in a dedicated release commit;
- submit sitemap;
- connect Search Console;
- verify production form delivery;
- perform final mobile, laptop, desktop, Safari, and Chromium QA;
- verify direct URLs for all versioned assets.

---

## Phase 9 — Post-launch iteration

**Status: Planned**

Potential work after stable launch:

- privacy-conscious analytics;
- Search Console review;
- article expansion based on real search questions;
- conversion-path refinement;
- accessibility follow-up;
- performance budget review;
- authentic photography expansion;
- appointment or CRM integration only after the basic contact workflow is stable.

## Non-goals

The project should not become:

- a generic medical portal;
- an over-animated agency showcase;
- a diagnosis or treatment-claim website;
- an emergency-service substitute;
- a collection of random stock imagery;
- a framework-heavy application without a clear operational need.
