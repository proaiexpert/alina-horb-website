# TASK 045 — Cloudflare Pages Owner Preview (isolated, noindex)

**Repository:** `proaiexpert/alina-horb-website`  
**Existing PR:** #109, must remain OPEN / DRAFT  
**Build source branch:** `agent/alina-article02-bilingual-premium-v21-r1`  
**Do not reuse:** `proaiexpert-github-io` (belongs to a different repo).

## Readiness

`scripts/build-cloudflare-owner-preview-v1.py` creates an output-only static distribution `cloudflare-owner-preview-dist/` from the existing accepted HTML/CSS/JS/WebP files. It **never deploys** and never modifies author-approved Article #2 or production files. It fails closed if `CF_PAGES_BRANCH` is not the exact source branch or if neither `CF_PAGES_COMMIT_SHA` nor `PREVIEW_SOURCE_SHA` provides a valid 40-digit Git commit.

Every output HTML file receives `robots=noindex, nofollow, noarchive`. The output root includes `_headers` containing:

```text
/*
  X-Robots-Tag: noindex, nofollow, noarchive
  X-Content-Type-Options: nosniff
```

and preview-only `robots.txt` containing `Disallow: /`. These files exist only in the Cloudflare output directory; the main/production robots rules remain untouched.

Cloudflare Pages interprets the static `_headers` in the **build output** as HTTP response headers. This protection is not proof of live HTTP delivery: verify headers against the actual Pages URLs before sending them to Owner. Do not add Pages Functions or `_worker.js`, as they can bypass static `_headers`.

## ONE owner authorization / project setup action (if no Cloudflare connector exists)

In the **existing Cloudflare account**, open [Cloudflare Dashboard → Workers & Pages](https://dash.cloudflare.com/) → **Create application / Pages → Connect to Git**. Authorize GitHub access to **only** `proaiexpert/alina-horb-website`, choose that repository, and configure a **new** free Pages project:

| Cloudflare Pages setting | Required exact value |
|---|---|
| Project name | `alina-horb-owner-preview` (or free equivalent if occupied) |
| Production branch *of this preview-only Pages project* | `agent/alina-article02-bilingual-premium-v21-r1` |
| Framework preset | `None` |
| Build command | `python3 scripts/build-cloudflare-owner-preview-v1.py` |
| Build output directory | `cloudflare-owner-preview-dist` |
| Root directory | repository root / blank |
| Environment variables | None |
| Custom domain | None |
| Separate existing project `proaiexpert-github-io` | DO NOT MODIFY |

The branch is designated **production inside the separate preview-only Pages project** solely to avoid deploying source repo `main` as a production hostname. Both the project's default `*.pages.dev` hostname and all versioned URLs will serve the same noindex artifact. Do not point the Pages project to repository `main`: the branch guard intentionally rejects it.

Cloudflare Git integration deploys future commits to the connected source branch automatically. No API tokens, GitHub repo secrets, Vercel, Codex, or Work are required. If the Pages project already exists with the correct repository and build configuration, reuse it rather than duplicate it.

**Required Owner reply:** "Подключил Cloudflare Pages" plus the real Pages host shown in the Cloudflare UI. No passwords or tokens. This is required because ChatGPT Direct in the present session has neither an authenticated Cloudflare connector nor a browser session that can interact with Cloudflare Dashboard.

## Live release verification (mandatory before handing URLs to Owner)

1. In Cloudflare Pages deployment details confirm `CF_PAGES_COMMIT_SHA` or `/preview-build-info.json` equals the **current** PR HEAD, not the older accepted SHA.
2. Verify HTTPS and HTTP 200 for:
   - `https://<verified-pages-host>/notes/fear-of-another-panic-attack/`
   - `https://<verified-pages-host>/ru/notes/fear-of-another-panic-attack/`
3. Check HTTP `X-Robots-Tag` on **both URLs**, the project root hostname, and one image asset. It must contain `noindex`. Check actual responses, not just the source `_headers`.
4. Confirm HTTP 200 for `/assets/images/notes/alina-horb-article02-hero-4x3.webp`, `/assets/images/notes/alina-horb-article02-home-card-800x500.webp`, `/assets/images/notes/alina-horb-article02-notes-card-800x600.webp`, `/assets/images/social/alina-horb-article02-og.png`, relevant CSS and JS.
5. Browser inspect UA/RU at 390px (iPhone) and 1440px (desktop), header/footer language switch, mobile menu, 10-section TOC, FAQ, CTA. Do not submit the production Formspree form.
6. Confirm that `main`, production website, approved Article #1 and PR Draft status remain untouched.

`QA Cloudflare Owner Preview / Article 02` GitHub Actions workflow runs the staged build and real Chromium language-switch test without publishing. It uploads staging artifact for debugging. **This CI preflight does not replace step 3's real external HTTP header check.**

### Acceptance

Only when live HTTPS URLs and noindex response headers are verified return both direct iPhone-usable links, deployment SHA, browser QA, and owner review guide. Otherwise report `BLOCKED: Cloudflare account authorization` and the single Cloudflare Dashboard action above. Never invent a Pages URL.
