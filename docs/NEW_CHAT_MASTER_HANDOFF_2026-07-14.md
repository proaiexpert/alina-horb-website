# ALINA HORB WEBSITE — MASTER HANDOFF FOR A NEW CHAT

**Status date:** 2026-07-14 / 2026-07-15 UTC transition  
**Repository:** https://github.com/proaiexpert/alina-horb-website  
**Primary language of project work:** Russian  
**Website languages:** Ukrainian primary, Russian secondary

---

## 1. Purpose of this document

This is the complete operational handoff for continuing the Alina Horb psychologist website project in a new ChatGPT conversation. It records:

- current production and GitHub state;
- approved facts and safety constraints;
- design direction;
- completed work;
- known problems;
- parallel research/editorial work;
- the full V3.2 plan;
- working rules for GitHub, Codex and review.

The new chat should treat this document, `PROJECT_SOURCE_OF_TRUTH.md`, Issue #19 and the current `main` branch as the starting context.

---

## 2. Core project identity

### Person and website

- Name UA: **Аліна Горб**.
- Name RU: **Алина Горб**.
- Profession: psychologist.
- Degree: Master of Psychology.
- Institution: Oles Honchar Dnipro National University.
- Degree year: 2024.
- Practice wording: **since 2016**.

### Website purpose

A premium bilingual personal website for a practicing psychologist. It should function as:

- a trust and positioning layer;
- an explanation of directions and consultation process;
- a safe first-contact path;
- an editorial psychology publication / Notes section;
- a future SEO and AI-search content platform.

### Brand direction

**Premium Editorial Sanctuary**:

- quiet luxury without conspicuous luxury;
- intellectual editorial design;
- calm mature femininity;
- emotional safety, space and clarity;
- ivory / stone / muted sage / terracotta / graphite palette;
- restrained motion;
- one real professional person, real diploma, no fake testimonials or fake metrics.

Reference roles:

1. **Kinfolk** — editorial structure, whitespace, typography, article atmosphere.
2. **Oura** — organic geometry, visual storytelling, restrained motion.
3. **Portland Talk Club** — psychological copy clarity, practical services, FAQ and content depth.

Do not copy any reference literally.

---

## 3. Current GitHub and deployment state

### Main repository

- Repository: `proaiexpert/alina-horb-website`
- Default branch: `main`
- GitHub Pages workflow exists and deploys repository content.
- Static architecture: HTML, CSS and minimal JavaScript.
- UA homepage: `/`
- RU homepage: `/ru/`
- UA Notes: `/notes/`
- RU Notes: `/ru/notes/`

### Latest verified commits

- `93ce7c4a2b8638dc276c60bcada928af28165746` — merged PR #22: standardized navigation, footer and favicon across all pages.
- `870ebf271302a7f3e4d46ed51d680995c72b8dfa` — added `CNAME` with `alinahorb.com` (`Configure production domain`).

Important: `CNAME` is now present. The actual DNS, HTTPS certificate and final public routing must still be verified in a browser / GitHub Pages settings before declaring the production domain fully live.

### Intended URLs

Production target:

- UA: `https://alinahorb.com/`
- RU: `https://alinahorb.com/ru/`

Previous GitHub Pages preview:

- UA: `https://proaiexpert.github.io/alina-horb-website/`
- RU: `https://proaiexpert.github.io/alina-horb-website/ru/`

After a working CNAME, GitHub Pages may redirect preview URLs to the custom domain. Verify rather than assume.

### Old preview repository

There is a separate old repository:

- `proaiexpert/alina-horb-preview`

It was a temporary public preview and is no longer the canonical site. It has one branch and an old failed Pages deployment. It should eventually be archived or deleted, not treated as the active project.

---

## 4. Approved information and content constraints

### Consultation facts

- Languages: Ukrainian and Russian.
- Primary format: online.
- In-person: possible by prior agreement.
- Session duration: 50 minutes.
- Price: 600 UAH.
- No city, office address, map, phone or WhatsApp at this stage.

### Audience wording

Approved safe wording:

- people of different ages;
- couples and families;
- work with minors is agreed separately.

Do not use a blanket claim such as “all ages” without the separate-minor qualification.

### Confirmed areas of work

Use careful professional language. Current site includes:

- psychological support for people affected by war, including internally displaced people;
- acute and chronic stress;
- panic attacks and consequences;
- anxiety states and support with diagnosed anxiety disorders;
- traumatic experience and PTSD symptoms;
- intrusive thoughts, rituals and OCD manifestations;
- domestic violence;
- crises, relationships and family requests;
- primary psychological support during acute stress;
- repeated suicidal or self-harm thoughts with an explicit emergency disclaimer.

### Safety wording

The site and contact form are **not emergency services**.

When there is immediate danger, a concrete suicide/self-harm plan or inability to remain safe, the visitor must be directed to local emergency or crisis services.

Do not promise:

- diagnosis;
- treatment;
- guaranteed results;
- “100% confidentiality”;
- universal legal availability in every country;
- emergency response.

### Contacts

- Email: `alinahorb1991@gmail.com`
- Telegram: `@alina_horb1991`
- Telegram URL: `https://t.me/alina_horb1991`
- Instagram: `@ng_alina_dp`
- Instagram URL: `https://instagram.com/ng_alina_dp`

Telegram is the primary fast contact channel. Email and Instagram are secondary.

---

## 5. Approved visual assets

### Hero

Use the approved professional portrait:

- Alina seated with an open book in a warm ivory interior.
- It is the homepage Hero source.
- Public optimized desktop/mobile derivatives are already in the repository.

### About Alina

Use the separate close portrait:

- ivory blouse;
- direct eye contact;
- closer trust-oriented composition;
- distinct from the Hero image.

### Locked photo decision

- Hero and About must use different images.
- Old outdoor pink-striped-shirt portraits should not return to the homepage.
- Do not generate or alter face, body, hair, hands, clothing or the book.
- Allowed: crop, resize, compression, colour management and restrained sharpening.

### Diploma

- Only the approved public redacted diploma title page may be published.
- Diploma number, registration data and private identifiers remain hidden.
- Unredacted originals, private masters and attachments must never enter the public repository.

---

## 6. Major work already completed

### Foundation and V2.0

- UA root and RU `/ru/` architecture.
- Separate physical URLs; no Google Translate or client-side language substitution.
- Canonical and hreflang foundation.
- Premium Editorial Sanctuary V2.0 structure.
- FAQ, process, directions, About, diploma, Notes and contact sections.
- Four UA and four RU article routes.
- Asset validation workflow.

### Current content and safety update — PR #13

- Current Telegram and Instagram.
- Updated audience wording.
- Confirmed focus areas.
- War / IDP, PTSD symptoms, panic, anxiety, OCD manifestations, domestic violence and crisis wording.
- Suicide/self-harm safety notice.

### Footer and mobile conversion — PR #14

- Compact two-level footer.
- Mobile booking CTA.
- CTA appears after Hero CTA leaves the viewport.
- CTA hides near contact section and footer.

### Repository documentation — PR #16

- Expanded README.
- Roadmap.
- Project history.
- Updated source of truth.

### Homepage V3.1 — PR #17

- New Hero photo with book.
- New About portrait.
- V3.1 homepage CSS.
- Updated UA/RU homepage copy and image derivatives.
- Responsive validation.

### Sticky/safety bug — PR #18

- Fixed safety notice sliding under the sticky topics introduction.

### Readability/stability — PR #20

- Increased critical small text.
- Improved sticky boundaries.
- Disabled problematic sticky behaviour on tablet/mobile.
- Improved form, footer and article readability.

### Portrait tablet and footer layout — PR #21

- Hero stacks on portrait tablets / narrow windows.
- Controlled portrait size.
- Trust strip changed to a balanced 2+2+2+1 layout.
- Footer domain and maker credit aligned.

### Shared navigation/footer/favicon — PR #22

- Branded SVG favicon added.
- Favicon applied across homepage, Notes and all article routes.
- Notes/article header standardized.
- Desktop navigation added.
- Mobile hamburger menu added.
- Links added for homepage, directions, About, process, Notes and contacts.
- Notes/article footer standardized with UA/RU, Email, Telegram, Instagram, copyright, domain and ProAI Expert maker credit.
- Homepage mobile footer aligned with logo and copyright in the first row.

---

## 7. Current page structure

Homepage:

1. Header / language / mobile menu.
2. Hero.
3. Trust strip.
4. When support may be useful.
5. Directions / topics.
6. About Alina.
7. Education and diploma.
8. Consultation process.
9. Principles and professional boundaries.
10. FAQ.
11. Notes preview.
12. Contacts and form.
13. Emotional CTA.
14. Footer.

Article system currently has:

- UA Notes index;
- RU Notes index;
- four UA articles;
- four RU articles.

Existing topics:

1. When usual coping methods stop helping.
2. What happens at the first consultation.
3. How to start a conversation when the request is hard to formulate.
4. Stress, relocation and loss of familiar support.

---

## 8. Current known limitations and unfinished work

### Domain / deployment

- `CNAME` now points to `alinahorb.com`.
- DNS and HTTPS status have not been conclusively verified in this handoff.
- Check GitHub Pages settings and direct production URLs before changing SEO state.

### Indexing

- Preview pages are still intended to remain `noindex, nofollow` until production domain, privacy, form and final QA are approved.
- Do not remove `noindex` casually.

### Form

- Form still uses a `mailto:`-style fallback / client email flow.
- It is not a real server-side submission system.
- Future production replacement needs privacy review, validation, anti-spam and success/error states.

### Notes and articles

This is the largest remaining quality gap.

Current article text and routes exist, but the editorial system is not yet at the target 8.5–9/10 level:

- article pages still rely substantially on the older V2 layout foundation;
- unique article hero images are not implemented;
- Notes cards lack four distinct premium visual concepts;
- article pages need stronger editorial composition;
- visible author/credentials/date-updated system is incomplete;
- contents / related articles / structured practical blocks need redesign;
- Article and Breadcrumb schema need final implementation;
- OG image strategy needs final implementation;
- UA and RU texts must be fully edited as native versions, not mechanical translations;
- SEO intent and safe clinical wording require final expert pass.

### Visual assets beyond portraits

- Repeated vase / books / branch imagery can feel like Pinterest templates.
- Replace repetition with a coherent but varied editorial image family.
- Use books, paper, light, fabric, interior details and restrained landscape imagery.
- Do not use random therapy stock photos or fake clients.

### Branch and repository hygiene

- Merged branches can be deleted after confirming they are no longer active.
- Old `alina-horb-preview` repository should be archived/deleted later.
- Do not remove active research or feature branches before outputs are collected.

---

## 9. Current large project: V3.2

Main tracking issue:

- **Issue #19 — V3.2 Editorial Notes, Article System & Premium Site Polish**
- https://github.com/proaiexpert/alina-horb-website/issues/19

Goal:

Raise the complete website from a strong homepage with weaker editorial pages to a coherent premium psychologist publication at approximately 8.5–9/10.

### V3.2 Workstream A — Deep Research

A separate Deep Research chat was assigned to create a research / SEO / safety pack for the four articles.

Source instructions:

- `docs/V3_2_PARALLEL_WORKSTREAMS.md`
- section `Workstream A — Deep Research`
- `docs/V3_2_RESEARCH_OUTPUT_TEMPLATE.md`
- Issue #19

Expected output:

- search intent;
- user questions;
- reliable sources and citations;
- safe wording;
- claims requiring caution;
- article structure recommendations;
- SEO opportunities;
- AI-search / answer-engine considerations.

Status: task was sent; final report must be brought back to the main coordinating chat.

### V3.2 Workstream B — Editorial writing and visual direction

A second chat was assigned:

- native Ukrainian editorial versions;
- independent natural Russian versions;
- H1/H2/H3 structure;
- quotes and practical blocks;
- CTA;
- four distinct premium image concepts;
- desktop/mobile crop and alt-text guidance.

Source instructions:

- `docs/V3_2_PARALLEL_WORKSTREAMS.md`
- section `Workstream B — Editorial writing and visual article direction`
- `docs/V3_2_EDITORIAL_OUTPUT_TEMPLATE.md`
- Issue #19

Status: task was sent; final package must be returned to the main coordinating chat.

### V3.2 Workstream C — Main coordinating chat

The main chat handles:

- GitHub state;
- small bugs and reversible fixes;
- responsive QA;
- header/footer/menu/favicon;
- integration of research and editorial outputs;
- final Codex technical assignment;
- PR review and live publication.

---

## 10. Planned V3.2 implementation

### Wave 1 — Notes index redesign

- One large featured article.
- Three supporting article cards.
- Four unique editorial covers.
- Category and reading time.
- Premium typography and spacing.
- Subtle image/arrow hover.
- Strong mobile stack, no chaotic horizontal carousel.

### Wave 2 — Premium article template

Each article should include:

- category and reading time;
- large H1 and strong lead;
- unique hero image;
- comfortable reading width;
- clear H2/H3 hierarchy;
- optional contents navigation;
- editorial quote/callout;
- practical block;
- author and credentials;
- publication/update date;
- related articles;
- calm consultation CTA;
- safety disclaimer only where relevant.

### Wave 3 — Content and localization

For every article:

- define one primary search question;
- edit the Ukrainian version natively;
- edit the Russian version independently;
- validate clinical/safety language;
- add internal links;
- avoid keyword stuffing;
- avoid diagnosis/treatment claims.

### Wave 4 — SEO and structured data

- title and description per route;
- canonical and hreflang validation;
- OG/Twitter image per article or coherent article set;
- Article schema;
- Breadcrumb schema;
- author/credentials;
- datePublished/dateModified;
- sitemap and robots review;
- remove `noindex` only after production launch approval.

### Wave 5 — Final premium polish

- typography scale;
- microtext contrast;
- diploma shadow / document treatment;
- more authentic supporting imagery;
- restrained reveal motion;
- active navigation;
- reduced-motion fallback;
- laptop QA at 1280–1440;
- mobile QA at 390 and nearby sizes;
- Chromium and WebKit/Safari checks.

---

## 11. Motion rules

Use:

- soft section reveal;
- 12–20 px vertical movement;
- title mask reveal;
- active navigation marker;
- line-drawing in process sections;
- subtle card hover;
- portrait mask reveal;
- mobile booking CTA;
- `prefers-reduced-motion` fallback.

Do not use:

- strong parallax;
- permanent floating movement;
- scroll hijacking;
- heavy 3D;
- animation that delays reading;
- motion that creates crop or performance problems.

---

## 12. Typography and visual rules

Current type pair is approved:

- Cormorant Garamond;
- Manrope.

Do not replace it without a major design reason.

Target readability:

- normal body: approximately 16–17 px;
- article body: approximately 18 px desktop, 17 px mobile;
- directions: minimum around 15 px;
- safety text: 15–16 px;
- categories/microtext: 12–13 px with sufficient contrast;
- H1/H2 remain expressive and editorial.

Palette:

- ivory / warm off-white;
- stone;
- muted sage;
- restrained terracotta;
- graphite, not pure black.

---

## 13. Footer / header decision

Current direction after PR #22:

- common site header for Notes and articles;
- desktop navigation;
- mobile hamburger menu;
- language switch;
- common footer on all routes;
- logo and copyright grouped on mobile;
- UA/RU, Email, Telegram and Instagram available;
- domain and maker credit in the bottom line;
- branded SVG favicon.

A decorative footer watermark was considered but deliberately not added yet. The existing monogram/logo already performs this role; another large watermark may overload the layout. Reconsider only after article redesign.

---

## 14. Working method with GitHub and Codex

### Small reversible changes

The user approved this workflow:

- make the change directly through GitHub;
- merge it;
- publish to live site;
- user checks the actual website;
- correct or revert individual items later if needed.

This applies to:

- CSS bugs;
- footer/header alignment;
- mobile breakpoints;
- small text sizing;
- menu/favicons;
- isolated safe corrections.

### Large changes

Use Codex for:

- full Notes redesign;
- all article template work;
- multi-page content integration;
- large asset packages;
- major SEO/schema implementation.

Codex should:

- work in a dedicated branch;
- read the GitHub issue and docs;
- not edit `main` directly;
- open one PR;
- provide validation;
- normally leave the PR unmerged until the coordinating chat reviews it.

The user sometimes prefers merging first and checking the live site. For a large multi-page V3.2 change, visual review before final release is still recommended.

---

## 15. Critical no-regression rules

- UA remains primary at `/`.
- RU remains separate at `/ru/`.
- No Google Translate / JS language replacement.
- Preserve language-paired article routes.
- Preserve current contacts.
- Preserve safe audience wording.
- Preserve crisis disclaimer.
- Preserve public redacted diploma only.
- No private source assets in repository.
- No fake testimonials or metrics.
- No phone, WhatsApp, city or address until separately confirmed.
- No medical diagnosis/treatment promises.
- Preserve `prefers-reduced-motion`.
- Preserve mobile CTA behaviour.
- Preserve one H1 per page.
- Broken images, local asset 404, console errors and horizontal overflow must remain zero.

---

## 16. Important repository documents

- `README.md`
- `docs/PROJECT_SOURCE_OF_TRUTH.md`
- `docs/ROADMAP.md`
- `docs/PROJECT_HISTORY.md`
- `docs/ASSET_USAGE.md`
- `docs/V3_1_PORTRAIT_SOURCES.md`
- `docs/V3_2_PARALLEL_WORKSTREAMS.md`
- `docs/V3_2_RESEARCH_OUTPUT_TEMPLATE.md`
- `docs/V3_2_EDITORIAL_OUTPUT_TEMPLATE.md`
- `docs/V3_2_WORKSTREAM_STATUS.md`
- Issue #19

---

## 17. Immediate next actions for the new chat

1. Read this handoff and the listed project documents.
2. Verify the current `main` head and CNAME state.
3. Open the production domain and previous GitHub Pages URL; confirm DNS, HTTPS and routing.
4. Visually QA PR #22 results on:
   - homepage UA/RU;
   - Notes UA/RU;
   - one UA article;
   - one RU article;
   - 390, 768, 1280 and 1440 px;
   - mobile menu, language switch, favicon and footer.
5. Collect the Deep Research report.
6. Collect the editorial/visual package.
7. Reconcile both outputs with `PROJECT_SOURCE_OF_TRUTH.md` and safety rules.
8. Update Issue #19 into one implementation-ready Codex package.
9. Implement V3.2 in a dedicated branch.
10. Review visually, then merge and deploy.
11. Finalize domain, form/privacy, sitemap and indexing only after full QA.

---

## 18. Recommended first message in the new chat

> Continue the Alina Horb website project. Read `docs/NEW_CHAT_MASTER_HANDOFF_2026-07-14.md`, `docs/PROJECT_SOURCE_OF_TRUTH.md`, Issue #19 and the latest `main` state first. Do not restart the project or invent missing facts. First report the exact current GitHub/deployment state and the next three actions.
