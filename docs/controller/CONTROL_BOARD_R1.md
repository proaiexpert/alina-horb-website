# PROAI EXPERT / ALINA HORB — CONTROLLER BOARD R1

Updated: 2026-10-07 (America/Los_Angeles).
**Governance status: PROPOSED / DOCUMENTATION DRAFT.** Do not treat this branch as deployed or as an override of current project authority.

## Durable entrypoint

**[GitHub Control Hub Issue #105](https://github.com/proaiexpert/alina-horb-website/issues/105)** = current stage tracker and decision journal.
**[Task 001](TASK_001_PR103_READONLY_REVIEW.md)** = complete brief to hand to a separate, FRESH ChatGPT Reviewer chat.
**[PR #103](https://github.com/proaiexpert/alina-horb-website/pull/103)** / **[PR #104](https://github.com/proaiexpert/alina-horb-website/pull/104)** = detailed technical changes and their actual checks.

### Operating model — explicit owner instruction

- **OWNER** makes final policy/editorial/release decisions; approval for merge and publication is explicit.
- **CONTROLLER = primary ChatGPT chat with the owner.** Owns priorities, task assignment, dependency tracking, concise QA of worker findings and go/no-go recommendations. Does not routinely perform extensive technical implementation or wide forensic audits that should live in specialist chats.
- **WORKER REVIEWER = new independent ChatGPT conversation, initially READ-ONLY.** Fetches real repo state, evidence, diff, tests; returns ACCEPT / TARGETED CORRECTION / REJECT in a short structured report. Never merge, publish, or edit.
- **WORKER BUILDER = different ChatGPT conversation, for one scoped implementation PR.** Reports base/head SHA, exact files, CI, proof; never merge without explicit permission.
- **OWNER relays work briefs and short reports between conversations.** There is no automatic cross-chat communication or background execution.
- Preserve separate Builder and Reviewer for medium-risk, UA/RU content, forms, public SEO and production-facing changes.

### Authority/read order for every chat

Fetch current `main` SHA (do not blindly trust this checkpoint). Read `AI_START_HERE.md`, `AGENTS.md`, `AI_CURRENT_HANDOFF.md`, `README.md`, `docs/PROJECT_SOURCE_OF_TRUTH.md`, `docs/ROADMAP.md`, relevant PR files and current GitHub checks. Fresh verified source has priority over this proposed coordination board. This file is a management plan, **not** new approval for clinical statements, credentials, privacy policy, or cross-border legality.

### Last mechanically verified checkpoint (2026-10-07 Pacific)

| Item | Verified state |
|---|---|
| Repository | `proaiexpert/alina-horb-website` |
| Production main | `06aaf3d101a57e4419cc8f566fdc9cf2f511e442` |
| PR #103 | OPEN / DRAFT; `efd6949aa0410217f3b8244035db57fdc503e998`; 2 files; 5/5 GitHub Actions success; **NOT MERGED** |
| PR #104 | OPEN / DRAFT; `72cd6c2d18333f7b9bc66825dd3f108efb7374c5`; 2 files; 12/12 Actions success; **NOT MERGED**, content wording **HOLD** |
| Main branch-protection | Off at last check. Risk to address with owner/governance. |
| Public website | https://alinahorb.com/ ; Ukrainian primary, Russian counterpart |
| Pricing | 35 €/1 600 UAH per 50 min; 240 €/12 320 UAH for 10 sessions |
| Indexing | 16 public technical indexable routes; two privacy routes intentionally noindex. Google-selected index status **UNKNOWN**. |
| Google access | Owner currently lacks client's Google sign-in; no login-gated tasks now. |

Prior audits are evidence, not substitutes for fresh checks. Passing CI is not professional-claim, legal, end-to-end email-delivery or production authorization.

## Prioritized queue and gates

| Stage | Priority | Who / what | Release/acceptance gate |
|---|---|---|---|
| **01** | **P1 NOW** | **Independent Reviewer** of PR #103; task file attached below | Verify validator's 4 defects are fixed, workflow coverage, SHA, clean 2-file scope; return verdict. Controller reviews; owner **separately approves** merge. |
| **02** | P1 next | Separate Content Builder/Reviewer on PR #104: online consultation from different countries, positively but conditionally expressed. | Owner/Alina factual approval, UA/RU + visible FAQ/JSON-LD parity, all 12 applicable checks, independent review, owner merge approval. **Do not merge current wording.** |
| **03** | P1 | Independent read-only full SEO/YMYL/a11y/mobile/form forensic audit of 16 public routes + two privacy + 404. | Defect/risk/opportunity register, evidence and focused follow-on tickets/PRs; no cosmetic churn. |
| **04** | P1 | Strategy chat: content gaps vs existing 4 UA/RU article pairs, ranking intent, topical clusters. | 2–3 distinct approved editorial briefs, internal links plan, sourcing/YMYL checks. |
| **05** | P1 | Builder+Reviewer: publish up to 2 excellent UA/RU article pairs after approvals. | Native localization, author/evidence, schema, canonical/hreflang, correct sitemap, tests, owner merge approval. |
| **06** | P2 | Public search/discovery + trust & ethical partnerships, 30/60/90 day plan. | Measurable non-Google-login metrics, no invented traffic/ranking, no spam. |
| **07** | Deferred | Search Console after owner confirms account access restored. | Real Google index coverage, selected canonicals, performance; never ask for credentials now. |

## Risk and claims register

1. **#103 proven validator false pass (P1 process, not proven live SEO outage).** Error: regex missed standalone 600 грн; validator tolerated public noindex; stale 270 € not blocked; SEO workflow missing this file/path execution. Scope restricted to two QA/CI files.
2. **#104 claim accuracy vs marketing clarity (P1 content).** Current draft phrases "география уточняется" are too restrictive. Candidate UA: "Так, звернутися можна й з іншої країни. Онлайн-консультації можливі; під час запису узгодимо часовий пояс, формат зв’язку та уточнимо застосовні умови." RU: "Да, обратиться можно и из другой страны. Онлайн-консультации возможны; при записи согласуем часовой пояс, формат связи и уточним применимые условия." These are **proposals only**, require factual owner/Alina confirmation; avoid the absolute phrase "regardless of country". Keep full FAQ in markup and JSON-LD semantically identical.
3. **Governance:** main protection absent; configure PR/CI ruleset only if supported and expressly approved.
4. **Unverified externals:** Google index counts/coverage, actual Formspree->recipient mailbox delivery, Alina professional cross-border scope, verified field Core Web Vitals. No Google sign-in now.
5. **Performance:** earlier tooling flagged large language-specific PNG logos; measure field and visual impact before changing brand assets.

## Reporting contract for worker -> controller

Return compact Russian answer with **ROLE / BASE / HEAD / files / checks / evidence / verified / unknown / risks / verdict / exact owner action**. Evidence must reference concrete PR/diff/run URLs. Worker's verdict is not release authorization. Controller summarizes recommendation for owner and updates [Issue #105](https://github.com/proaiexpert/alina-horb-website/issues/105) with new short checkpoint.

## Hard boundaries

NO direct `main` edits; NO auto-merge; NO unauthorized publication; NO credentials, sensitive client records or unredacted diploma; NO invented professional qualifications; NO rebuild or sweeping redesign; NO assumption "all URLs indexed". Preserve UA/RU, localized metadata/canonicals/hreflang, pricing, forms, site aesthetic and privacy boundaries.
