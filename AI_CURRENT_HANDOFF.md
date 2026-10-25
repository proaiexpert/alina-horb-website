# AI Current Handoff — Alina Horb Website

## Repository Purpose
Primary bilingual website for psychologist Alina Horb.

## Current Stable Direction
- Ukrainian is primary.
- Russian is a full localized counterpart.
- The site should remain calm, human-centred, editorial, personal, readable, and privacy-conscious.
- The website and the ProAI Expert portfolio case are separate repositories and should not be confused.

## Current Priority
Article #2 UA/RU was published on 2026-10-24 via PR #109 (squash commit `25818efd01002a44f42a8680cf80ae2666c6a086`). The accepted design retains the arched Hero and adaptive five-step map. Production now has 20 indexable UA/RU routes plus two noindex privacy routes. Post-release audit now checks both Article #1 and Article #2.

The non-Google technical hardening pass is complete: public indexing controls, sitemap/robots/canonical/hreflang, structured data, SERP-title cleanup, live post-deploy SEO checks, performance-readiness checks, and automated accessibility checks are implemented. Google Search Console coverage remains a separate external verification task that requires account access.

## Canonical Entry Files
1. `AGENTS.md`
2. `AI_START_HERE.md`
3. `AI_CURRENT_HANDOFF.md`
4. `README.md` when present
5. task-specific pages and documents named by the owner

## Critical Invariants
- No invented credentials, clinical claims, rankings, leads, or outcomes.
- Preserve Ukrainian-primary and Russian-localized architecture.
- Preserve canonical/hreflang/x-default and separate localized content.
- Keep the 20 public UA/RU routes indexable; keep only the two privacy-policy routes `noindex, follow` unless the owner explicitly changes that policy.
- Preserve privacy, boundaries, and natural professional language.

## Do Not Touch Without Explicit Scope
- production `main`;
- language architecture;
- contact/intake behavior;
- professional claims and credentials;
- merge/publication, rollback, force-push, deletion, or destructive operations.

## Next Approved Action
Do not start another broad redesign or speculative SEO rewrite by default. When Google Search Console access is restored, inspect sitemap processing, Google-selected canonicals, and per-URL indexing for the 20 public routes. Separately, any changes to jurisdiction, minors/couples policy, confidentiality/records practice, or acute-risk procedures require confirmed client/professional input before publication.

## Mechanical State Rule
Always fetch current refs and SHAs. Do not assume an old chat or handoff contains current mechanical Git state.
