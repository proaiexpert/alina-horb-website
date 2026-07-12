# Bilingual UA/RU Preview QA Report

## Scope

Feature branch: `feat/bilingual-ua-ru-v3`

Routes:

- Ukrainian primary page: `/`
- Russian page: `/ru/`

## Responsive browser QA

Both language versions were checked at:

- 320 px
- 360 px
- 375 px
- 390 px
- 430 px
- 768 px
- 1024 px
- 1280 px
- 1440 px

Results:

- `document.documentElement.scrollWidth <= window.innerWidth`: PASS at every width;
- horizontal overflow: none;
- one H1 per page;
- duplicate IDs: none;
- broken images: none;
- console errors: 0;
- page/runtime errors: 0;
- mobile menu opens, closes after navigation, and closes with Escape;
- FAQ controls are keyboard accessible;
- language switch works in header and footer;
- portrait keeps its approved crop and is not distorted;
- contact form remains within the viewport;
- Telegram remains disabled until an exact username is configured.

## HTTP and link checks

A local static server returned HTTP 200 for:

- `/`
- `/ru/`
- shared CSS and JavaScript;
- portrait WebP and JPEG;
- diploma WebP and JPEG;
- UA and RU logo assets;
- decorative SVG assets.

Relative URLs were also resolved under the GitHub Pages project path `/alina-horb-website/`. No root-absolute local asset or language-route references were found.

## Functional checks

- Ukrainian page language: `uk`.
- Russian page language: `ru`.
- UA is active on the root page; RU links to `./ru/`.
- RU is active on `/ru/`; UA links to `../`.
- Contact form uses native HTML validation and prepares a localized `mailto:` message.
- Form data is not stored or sent to a third-party service.
- Active Telegram links are generated only when `telegramUsername` is populated in `assets/js/site-config.js`.
- Preview pages use `noindex, nofollow`.

## Environment note

Direct Chromium navigation to localhost was blocked by the execution environment with `ERR_BLOCKED_BY_ADMINISTRATOR`. Static-server HTTP checks and browser rendering checks were therefore performed separately: real HTTP requests validated server paths, while browser QA used the exact production HTML, CSS, JavaScript, and image bytes in an in-memory document.
