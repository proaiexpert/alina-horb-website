# TASK 001 — INDEPENDENT REVIEW OF PR #103
**Project:** ProAI Expert / Alina Horb Website
**Date / priority:** 2026-10-07 Pacific / P1 NOW
**Use:** Attach this file to a FRESH ChatGPT chat that has GitHub access. This is a complete isolated task brief, not permission for production changes.
**Controller tracking:** https://github.com/proaiexpert/alina-horb-website/issues/105

## Role and execution mode

You are a senior independent GitHub Reviewer / CI QA engineer auditing an existing **production-safe validator fix**. **READ-ONLY**. You are not the original Builder. Do not modify, commit, merge, publish, push, rebase, rename PR, mark ready for review, or change GitHub settings. Do not rewrite the site or initiate separate unrelated SEO work. Do NOT ask for Search Console credentials: owner lacks Google account access.

**Repository:** `proaiexpert/alina-horb-website`
**PR:** https://github.com/proaiexpert/alina-horb-website/pull/103
**Checkpoint ONLY, not authority:** main `06aaf3d101a57e4419cc8f566fdc9cf2f511e442`; PR head `efd6949aa0410217f3b8244035db57fdc503e998`; OPEN/DRAFT; 2 files and 5/5 green actions at handoff. REFRESH this all yourself.

## Mandatory independent verification

1. Read in canonical order `AI_START_HERE.md`, `AGENTS.md`, `AI_CURRENT_HANDOFF.md`, `README.md`, `docs/PROJECT_SOURCE_OF_TRUTH.md`, `docs/ROADMAP.md`. Fetch fresh GitHub main/PR SHA, full actual #103 patch, all changed filenames, current CI statuses and any relevant comments/conflicts.
2. Confirm exactly these scoped files:
   - `.github/workflows/audit-seo-launch-indexing-v1.yml`
   - `scripts/validate-consultations-pages-v1.py`
   **No UA/RU page HTML, prices, content, layout, forms, or production config changed.**
3. Review regression case #1: regex catches isolated legacy `600 грн` incl surrounding punctuation, but NOT current `1 600 грн` or `1\u00a0600 грн` (NBSP). Analyze word boundaries/Unicode carefully; independently exercise mutation-positive and mutation-negative inputs if local execution available. The old regex escaped incorrectly; do not assume a passing test is sufficient if the test repeats a wrong assumption.
4. Review case #2: validator now rejects public consultation `noindex, nofollow` and requires **exactly correct** public `index, follow, max-image-preview:large`. Consider duplicate/ambiguous robots declarations and whether the assertion meaningfully prevents bad indexing.
5. Review case #3: rejects simultaneous obsolete `270 €` even when the intended package `240 €` is present. Preserve confirmed 50-min 35 €/1 600 грн and 10-session 240 €/12 320 грн values; verify only approved values on BOTH consultation pages.
6. Review case #4: relevant SEO audit workflow has PR/push path triggers for modified validator and invokes it in its active job. Verify workflow syntax and that successful status refers to the right SHA.
7. Look for accidental regression, false positives, hidden scope change or failure mode in the actual patch. Validate with verifiable evidence (code, test output, current GitHub Actions), not generic SEO advice. Do not confuse validator reliability gaps with a live Google indexing incident.
8. Determine if #103 is ready to recommend for owner's **separate merge authorization**. Leave PR as Draft. Independent review here is a written assessment, NOT an official GitHub approval or merge.

## Exact return contract — send SHORT Russian report to owner/controller (target 200–350 words)

`VERDICT: ACCEPT | TARGETED CORRECTION | REJECT`

- **GitHub:** current main SHA, PR head SHA, draft/mergeability, exact 2 files.
- **Tests/evidence:** 4 checklist results, 5/5 or current CI truth, URLs to diff/workflow run; distinguish own executed tests vs reading CI.
- **Risks:** only demonstrated defects or meaningful unknowns; severity.
- **Decision:** recommend owner authorizes controlled squash merge OR one narrow correction; **never perform it**.
- **No noise:** do not produce a broad website audit, huge transcript, or a second master handoff. Preserve owner control.

If actual fresh GitHub differs from supplied checkpoint, report it as a blocker with exact refs instead of guessing.
