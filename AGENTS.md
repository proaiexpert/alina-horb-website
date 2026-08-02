# AGENTS.md

## Default Execution Model
- ChatGPT direct GitHub work is the default route for planning, code, content, SEO, documentation, branches, commits, pushes, and PR preparation.
- Use one ChatGPT chat for small, scoped, reversible work.
- Use separate ChatGPT Builder and Reviewer chats for production-facing, shared UI/JS, UA/RU parity, or medium-risk work.
- Use Codex only when a local dev server, browser automation, screenshots, complex build/test pipelines, broad debugging, large refactoring, or prolonged terminal execution is materially required.
- Gemini and other third-party or weak substitute models are not default workflow tools.

## Project Rules
- Preserve the Ukrainian primary version and full Russian counterpart unless explicitly changing language architecture.
- Preserve truthful psychologist positioning, calm editorial tone, privacy boundaries, localized URLs, canonical/hreflang relationships, and internal links.
- Do not introduce clinical claims, invented credentials, rankings, leads, or performance claims.
- Prefer minimal targeted changes; do not perform broad redesign or cleanup without explicit scope.
- Read the current file before editing and do not invent paths, selectors, APIs, dependencies, or professional facts.

## Independent Review
For medium-risk or production-facing changes:

- Builder works in a dedicated branch and reports base SHA, head SHA, exact files, checks, unverified items, and risks.
- Reviewer starts in a fresh ChatGPT chat, initially read-only, and checks the actual GitHub diff.
- Reviewer returns `ACCEPT`, `TARGETED CORRECTION`, or `REJECT`.

## Git and Production Safety
- Work in a dedicated branch.
- Never modify `main`, merge, publish, roll back production, force-push, delete, or perform destructive operations without explicit owner authorization.
- Commit and push only when explicitly authorized or clearly included in the task.
- Before merge, verify base SHA, expected head SHA, changed files, mergeability, and scope.
- Prefer squash merge when intermediate commits should not enter production history.

## External Model Policy
- Do not route ordinary work to Gemini, OpenCode, Telegram agents, or other third-party models.
- An external model requires a concrete unique capability reason and explicit owner approval.

## Required Report
- route used;
- base SHA and head SHA;
- files changed;
- checks run;
- verified and unverified behavior;
- risks;
- intentionally untouched areas;
- next action.
