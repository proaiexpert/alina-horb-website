# Alina Horb Website

Bilingual static website for psychologist Alina Horb.

## Current preview architecture

- Ukrainian primary page: `/` (`index.html`)
- Russian page: `/ru/` (`ru/index.html`)
- Preview target after merge: `https://proaiexpert.github.io/alina-horb-website/`
- Future production domain: `https://alinahorb.com/`

The preview pages currently use `noindex, nofollow`. Remove that directive only in a separate production commit after the official domain is connected and verified.

## Stack

- semantic HTML5;
- shared modern CSS;
- minimal vanilla JavaScript;
- no framework, CMS, database, npm dependency, or build step.

## Local launch

```bash
python3 -m http.server 8080
```

Open:

- `http://127.0.0.1:8080/`
- `http://127.0.0.1:8080/ru/`

## Contact configuration

Shared contact settings are stored in:

`assets/js/site-config.js`

The Telegram username is intentionally empty until confirmed. The temporary form prepares a localized `mailto:` message and does not transmit or store form data.

## Assets

Only approved public production assets are committed:

- localized RU/UA logos;
- optimized public portrait derivatives;
- public redacted diploma derivatives;
- decorative SVG files.

Never commit original/private portrait files, original or unredacted diploma files, private masters, credentials, cookies, tokens, or ZIP archives.

## Deployment

GitHub Pages deploys directly from the repository through `.github/workflows/deploy-pages.yml`. The workflow copies `index.html`, `ru/`, and `assets/` into the Pages artifact. It does not use Google Drive or external ZIP files.

## Pending before production launch

- exact Telegram username;
- privacy policy and legal review;
- removal of preview `noindex, nofollow` after the official domain is connected;
- final production SEO and Open Graph verification.
