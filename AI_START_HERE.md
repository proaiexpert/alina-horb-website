# AI Start Here — Alina Horb Website

## Purpose
Deterministic entrypoint for a fresh session working on `proaiexpert/alina-horb-website`.

## Required First Actions
1. Fetch current `main` and record SHA.
2. Read `AGENTS.md`.
3. Read `AI_CURRENT_HANDOFF.md`.
4. Read `README.md` when present.
5. Read only task-specific pages and canonical documents named by the handoff or owner.
6. Inspect relevant branch/PR metadata when active work is referenced.

## Role Selection
- Strategy, content architecture, or SEO planning → `Control`.
- Implementation, branch, commit, or push → `Builder`.
- Audit, diff review, or readiness check → `Reviewer`.
- Merge/publication → `Publisher`, only when explicitly authorized.
- Ambiguous request → `Control`, read-only.

## Project Invariants
- Ukrainian is the primary language; Russian is a full localized counterpart.
- Preserve calm, personal, editorial, privacy-conscious psychologist positioning.
- Do not invent clinical claims, credentials, rankings, leads, outcomes, or professional facts.
- Preserve separate localized URLs, title/description, H1, internal links, canonical, hreflang, x-default, and sitemap relationships unless explicitly changing them.
- Never modify `main`, merge, publish, roll back, force-push, delete, or perform destructive operations without explicit owner authorization.

## Risk Routing
- Tier 1: one ChatGPT chat for small scoped work.
- Tier 2: separate Builder and Reviewer chats for production-facing, shared UI/JS, UA/RU parity, SEO, or medium-risk work.
- Tier 3: Codex only when local runtime, browser automation, screenshots, complex testing, broad debugging, or a large refactor is materially required.

## First Response Contract
Report repository, role, risk tier, main SHA, files read, current state, task interpretation, branch, permissions, blockers, and next action before editing.

## Handoff Rule
After meaningful merged work, update `AI_CURRENT_HANDOFF.md` in the same approved documentation pass.
