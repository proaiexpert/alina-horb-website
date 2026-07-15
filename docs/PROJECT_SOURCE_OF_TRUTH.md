# Alina Horb Website — Project Source of Truth

Last updated: 2026-07-14

## Current approved language architecture

- Ukrainian is the primary website language.
- Ukrainian route: `/` (`index.html`, `<html lang="uk">`).
- Russian route: `/ru/` (`ru/index.html`, `<html lang="ru">`).
- Both versions are manually prepared and complete.
- Google Translate, automatic JavaScript translation, and mixed-language pages are prohibited.
- Ukrainian is the primary canonical editorial version.
- Russian content must be a natural independent localization, not mechanical translation.

## Confirmed identity and education

- Ukrainian name: Аліна Горб.
- Russian name: Алина Горб.
- Profession: psychologist.
- Degree: Master of Psychology.
- Institution: Oles Honchar Dnipro National University.
- Degree year: 2024.
- Practice wording: since 2016.

Do not add titles such as psychotherapist, clinical psychologist, medical psychologist, trauma therapist, licensed psychologist, or PTSD expert without explicit evidence and approval.

## Confirmed service information

- Consultation languages: Ukrainian and Russian.
- Primary format: online consultations.
- In-person consultations: possible only by prior agreement.
- No city, address, Germany, Khust, phone, WhatsApp, map, or office hours may be published at this stage.
- Audience wording: people of different ages, couples, and families; work with minors is agreed separately.
- Session duration: 50 minutes.
- Price: 600 UAH for online and in-person formats.

## Confirmed focus areas

Use careful professional wording without diagnosis or treatment guarantees:

- psychological support for people affected by war, including internally displaced persons;
- acute and chronic stress;
- panic attacks and their consequences;
- anxiety states and psychological support with diagnosed anxiety disorders;
- traumatic experience and PTSD symptoms;
- intrusive thoughts, rituals, and OCD manifestations;
- domestic violence;
- crises, relationships, and family requests;
- primary psychological support during acute stress;
- repeated suicidal or self-harm thoughts with a clear emergency disclaimer.

These confirmed website topics are not permission to claim clinical specialization, medical treatment, universal client eligibility, cross-border legal authority, or guaranteed outcomes.

## Safety and claim rules

The website and form are not emergency services. When there is immediate danger, a concrete suicide/self-harm plan, violence, inability to remain safe, or loss of contact with reality, users must be directed to local emergency or crisis services.

Do not publish:

- diagnosis from a symptom list;
- universal time thresholds for when help is required;
- treatment or improvement guarantees;
- fear-based conversion language;
- a fixed first-consultation script unless confirmed by Alina;
- absolute confidentiality claims;
- universal migration stages;
- statements that relocation itself always equals trauma;
- unsupported statements about methods, testing, diagnostics, risk assessment, jurisdiction, or record keeping.

Preferred language uses qualification such as `може / может`, `іноді / иногда`, `залежно від ситуації / в зависимости от ситуации`, and `не є діагнозом / не является диагнозом`.

The adopted article evidence and safety standard is:

- [`V3_2_RESEARCH_SYNTHESIS.md`](V3_2_RESEARCH_SYNTHESIS.md)

## Contact information

- Email: `alinahorb1991@gmail.com`.
- Telegram: `@alina_horb1991` / `https://t.me/alina_horb1991`.
- Instagram: `@ng_alina_dp` / `https://instagram.com/ng_alina_dp`.
- Telegram is the primary direct channel; Instagram and email are additional channels.
- Shared contact configuration: `assets/js/site-config.v2.js`.

## Contact form and privacy status

- The current form opens a localized `mailto:` message.
- The current form is temporary and does not store submissions.
- Before search launch, the project requires UA/RU privacy pages and a privacy-reviewed form endpoint.
- The production form must use minimal data collection, validation, anti-spam, clear success/error states, provider disclosure, and documented retention behavior.
- The form must warn users not to submit sensitive medical, crisis, or emergency information.
- `noindex, nofollow` remains until privacy, form, editorial, and SEO release gates are explicitly approved.

## Portrait decisions for V3.1

- Hero source: seated portrait with a book in a warm ivory interior.
- About source: close portrait in an ivory blouse.
- The two roles must remain distinct.
- Old pink-shirt outdoor portraits are not used on the homepage after V3.1.
- Do not generate or alter face, body, hair, or clothing. Only crop, resize, compression, and color management are allowed.

## Diploma safety

- The current public redacted diploma title page is approved for website use.
- Diploma number, registration identifiers, and other personal identifiers must remain hidden.
- Original diploma, unredacted version, private master, attachments, and source archives must never be committed.

## Brand and design

- Visual direction: Premium Editorial Sanctuary.
- Reference mix: Kinfolk for editorial structure, Oura for organic geometry and restrained motion, Portland Talk Club for psychological-content clarity.
- Ukrainian pages use the approved UA dark logo on light surfaces.
- Russian pages use the approved RU dark logo on light surfaces.
- Motion must remain restrained and respect `prefers-reduced-motion`.
- Broad redesigns must not be presented as minor polish.

## Production domain and deployment

- Primary production domain: `https://alinahorb.com/`.
- Russian production route: `https://alinahorb.com/ru/`.
- `https://www.alinahorb.com/` redirects to the apex domain.
- HTTP redirects to HTTPS.
- The former GitHub Pages project URL redirects to `alinahorb.com`.
- GitHub Pages DNS and HTTPS are active.
- GitHub Pages deployment must use repository files directly and must not depend on Google Drive or ZIP files.
- The project remains publicly accessible but intentionally excluded from search indexing until the release gate.

## Editorial article system

The current four UA and four RU article routes cover:

1. when familiar coping strategies stop helping;
2. what happens during the first consultation;
3. how to begin when the request is difficult to formulate;
4. stress, relocation, and loss of familiar support.

Current routes should remain stable unless a route inventory and redirect plan approve a change.

Final articles require:

- direct answer near the beginning;
- visible author and confirmed credential;
- meaningful publication/update dates;
- native UA and RU editing;
- clear educational/diagnostic boundary;
- contextual internal links;
- calm CTA;
- authoritative sources for sensitive claims;
- accurate Article/BlogPosting, BreadcrumbList, Person, and WebSite structured data only where visible facts support it.

## Outstanding confirmation gates

Before final article publication and search launch, confirm with Alina:

- professional jurisdiction and permitted client locations;
- exact first-session process;
- cancellation/rescheduling/payment rules;
- confidentiality limits and informed-consent process;
- record/notes and personal-data handling;
- testing, diagnostic, referral, and risk-assessment practices;
- acute-risk procedure;
- actual competence and scope for sensitive focus areas;
- crisis routing by client country/location.

## Decision authority

The main coordinating project chat and repository governance documents hold final production decisions. Feature work must be reviewed through a pull request before merge to `main`.

Priority order:

1. latest confirmed information from Alina;
2. this source-of-truth document;
3. `V3_2_RESEARCH_SYNTHESIS.md` for article evidence and safety;
4. approved design/content decisions;
5. reviewed GitHub issues and pull requests.

## V3.2 — Author voice and working approach

Approved homepage content:

- author quote about inner support, faith, close relationships and attentive self-care;
- client-centred approach as the interaction foundation;
- selected gestalt-oriented tools and metaphorical associative cards as optional instruments;
- metaphorical cards are not diagnostic and are used only with client consent;
- faith, spiritual experience, values and meaning may be discussed only when relevant to the client, without imposing religious views;
- audience additions: mothers raising children without partner support and people of older age;
- no public claim of gestalt certification, psychotherapy status, clinical qualification or regular supervision unless separately confirmed.

Responsive requirement: the About section must not overflow at 844 px landscape and must remain readable when the three approach rows are added.
