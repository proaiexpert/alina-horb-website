# Alina Horb Website

Production website project for psychologist Alina Horb.

## Status

Approved static homepage package imported for review.

No deployment, GitHub Pages, DNS, or production launch has been configured.

## Official domain

alinahorb.com

## Project workflow

1. Source assets and private originals are stored in Google Drive.
2. The homepage implementation is prepared as a reviewed static package.
3. Approved code is imported through a GitHub feature branch and pull request.
4. Technical and visual QA is completed before merge.
5. Deployment is configured only after content and legal review.

## Stack

- semantic HTML5;
- modern CSS;
- minimal vanilla JavaScript;
- no framework, npm dependencies, CMS, database, or build step.

## Local launch

From this directory:

```bash
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080/`.

## Production assets

Only approved public website assets are included. The portrait uses an optimized JPEG production derivative created from the private high-resolution master; the master itself is not included.

Only the public redacted diploma is included.

## Fonts

The prototype loads Cormorant Garamond and Manrope from Google Fonts with `display=swap` and fallback stacks. Self-hosting/privacy should be decided before production launch. Font files are not included.

## Current limitations

- exact Telegram URL is pending, so CTAs use `mailto:alinahorb1991@gmail.com`;
- approved Ukrainian copy and UA route are not yet available;
- privacy policy is shown as inactive text to avoid a broken link;
- some working homepage copy is pending final client confirmation.

## Important

Private source assets, original diploma files and archives must never be committed to this repository.

## QA evidence

Full-page responsive screenshots are retained in the verified Google Drive delivery package rather than committed to the production repository.
