# Alina Horb Website — Project Source of Truth

## Current approved language architecture

- Ukrainian is the primary website language.
- Ukrainian route: `/` (`index.html`, `<html lang="uk">`).
- Russian route: `/ru/` (`ru/index.html`, `<html lang="ru">`).
- Both versions are manually prepared and complete.
- Google Translate, automatic JavaScript translation, and mixed-language pages are prohibited.

## Confirmed identity and education

- Ukrainian name: Аліна Горб.
- Russian name: Алина Горб.
- Profession: psychologist.
- Degree: Master of Psychology.
- Institution: Oles Honchar Dnipro National University.
- Degree year: 2024.
- Practice wording: since 2016.

## Confirmed service information

- Consultation languages: Ukrainian and Russian.
- Primary format: online consultations.
- In-person consultations: possible only by prior agreement.
- No city, address, Germany, Khust, phone, WhatsApp, map or office hours may be published at this stage.
- Audience wording: people of different ages, couples and families; work with minors is agreed separately.
- Session duration: 50 minutes.
- Price: 600 UAH for online and in-person formats.

## Confirmed focus areas

Use careful professional wording without diagnosis or treatment guarantees:

- psychological support for people affected by war, including internally displaced persons;
- acute and chronic stress;
- panic attacks and their consequences;
- anxiety states and psychological support with diagnosed anxiety disorders;
- traumatic experience and PTSD symptoms;
- intrusive thoughts, rituals and OCD manifestations;
- domestic violence;
- crises, relationships and family requests;
- primary psychological support during acute stress;
- repeated suicidal or self-harm thoughts with a clear emergency disclaimer.

The website and form are not emergency services. When there is immediate danger, a concrete plan, or inability to remain safe, the user must be directed to local emergency or crisis services.

## Contact information

- Email: `alinahorb1991@gmail.com`.
- Telegram: `@alina_horb1991` / `https://t.me/alina_horb1991`.
- Instagram: `@ng_alina_dp` / `https://instagram.com/ng_alina_dp`.
- Telegram is the primary direct channel; Instagram and email are additional channels.
- Shared contact configuration: `assets/js/site-config.v2.js`.

## Portrait decisions for V3.1

- Hero source: seated portrait with a book in a warm ivory interior.
- About source: close portrait in an ivory blouse.
- The two roles must remain distinct.
- Old pink-shirt outdoor portraits are not used on the homepage after V3.1.
- Do not generate or alter face, body, hair or clothing. Only crop, resize, compression and color management are allowed.

## Diploma safety

- The current public redacted diploma title page is approved for website use.
- Diploma number, registration identifiers, and other personal identifiers must remain hidden.
- Original diploma, unredacted version, private master, attachments, and source archives must never be committed.

## Brand and design

- Visual direction: Premium Editorial Sanctuary.
- Reference mix: Kinfolk for editorial structure, Oura for organic geometry and restrained motion, Portland Talk Club for psychological content clarity.
- Ukrainian pages use the approved UA dark logo on light surfaces.
- Russian pages use the approved RU dark logo on light surfaces.
- Motion must remain restrained and respect `prefers-reduced-motion`.

## Domain and preview

- Future production domain: `https://alinahorb.com/`.
- Temporary preview target: `https://proaiexpert.github.io/alina-horb-website/`.
- Russian preview route: `https://proaiexpert.github.io/alina-horb-website/ru/`.
- Preview pages must use `noindex, nofollow`.
- Remove preview robots directives only in a separate production commit after domain connection.
- GitHub Pages deployment must use repository files directly and must not depend on Google Drive or ZIP files.

## Decision authority

The main coordinating project chat and the repository governance documents hold final production decisions. Feature work must be reviewed through a pull request before merge to `main`.
