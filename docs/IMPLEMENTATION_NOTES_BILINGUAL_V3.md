# Bilingual UA/RU Preview Implementation Notes

## Routing

- `index.html`: Ukrainian primary page.
- `ru/index.html`: Russian page.
- Internal language and asset links are relative so both pages work under the GitHub Pages project path and later on the root production domain.

## Shared implementation

- Both pages use the same CSS files.
- Language-specific body classes select the approved UA or RU logo.
- `assets/js/site-config.js` stores shared contact settings.
- `assets/js/main.js` manages the mobile menu, Telegram activation, and localized mailto form.

## Contact behavior

- Email is active.
- Telegram remains disabled while the username is empty.
- The form performs native validation, builds a localized subject/body, and opens the user’s email application.
- No submitted data is stored or transmitted to an external backend.

## Preview SEO

- Canonical and hreflang target `alinahorb.com`.
- Both preview pages use `noindex, nofollow`.
- Social preview images use the working GitHub Pages project asset URL.

## Deployment

The Pages workflow builds `_site` only from repository content:

- `index.html`;
- `ru/`;
- `assets/`;
- `.nojekyll`.

No Google Drive files, external ZIP archives, or separate preview repository are used.
