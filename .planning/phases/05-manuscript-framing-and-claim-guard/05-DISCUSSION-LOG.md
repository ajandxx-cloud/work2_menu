# Phase 5: Manuscript Framing And Claim Guard - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md. This log preserves the alternatives considered.

**Date:** 2026-06-11T15:35:11+08:00
**Phase:** 5-Manuscript Framing And Claim Guard
**Areas discussed:** Manuscript scope, claim guard, output contract
**Mode:** auto-selected all gray areas from existing GSD yolo/auto-advance settings.

---

## Manuscript Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Status-driven support docs | Generate method/experiment/result outlines from verified project state and artifact status. | yes |
| Freeform manuscript prose | Draft final paper prose even though current artifacts are blocked. | |
| New empirical execution | Attempt to create missing pilot/formal evidence during Phase 5. | |

**User's choice:** Auto-selected status-driven support docs.
**Notes:** Phase 4 explicitly says current artifacts are blocked/non-claim-ready. Phase 5 should frame safely rather than strengthen claims.

---

## Claim Guard

| Option | Description | Selected |
|--------|-------------|----------|
| Machine-readable guard plus Markdown checklist | Keep claims enforceable and reviewer-readable. | yes |
| Markdown only | Simpler, but later tooling would need to parse prose. | |
| No guard artifact | Unsafe because PAPER-04 requires explicit blocked claims. | |

**User's choice:** Auto-selected machine-readable guard plus Markdown checklist.
**Notes:** Claim checks should read `ARTIFACT_STATUS.json`, including checkpoint blockers and `claim_ready` flags.

---

## Output Contract

| Option | Description | Selected |
|--------|-------------|----------|
| Artifact manuscript support directory | Write generated outputs under `work2_coding/artifacts/work2_robust_menu/manuscript/` and mirror to root artifacts. | yes |
| Planning docs only | Easier but less useful to manuscript tooling. | |
| LaTeX manuscript tree | Premature because no current manuscript tree exists under `work2_coding/`. | |

**User's choice:** Auto-selected artifact manuscript support directory.
**Notes:** Mirrors Phase 4 lightweight artifact convention and avoids creating a new manuscript system too early.

---

## the agent's Discretion

- Exact helper/module names.
- Exact Markdown section wording as long as blocked evidence remains blocked.
- Whether to create a small reusable module or keep logic inside one script.

## Deferred Ideas

- Final LaTeX prose after claim-ready pilot/formal evidence exists.
- Pilot/formal execution after the required checkpoint is supplied.
