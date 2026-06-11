# Phase 5: Manuscript Framing And Claim Guard - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md. This log preserves the alternatives considered.

**Date:** 2026-06-11T15:35:11+08:00
**Phase:** 5-Manuscript Framing And Claim Guard
**Areas discussed:** Evidence posture, manuscript output target, claim strictness
**Mode:** Human discussion amendment after initial auto draft.
**User response:** `1A, 2A, 3A`

---

## Evidence Posture

| Option | Description | Selected |
|--------|-------------|----------|
| Strictly conservative | Only write method, experiment design, diagnostic artifacts, and limitations; empirical advantage claims wait for claim-ready evidence. | yes |
| Conditional draft | Write result templates with every empirical conclusion marked as awaiting claim-ready evidence. | |
| Evidence first | Pause Phase 5 and return to Phase 4 to supply checkpoint-backed pilot/formal evidence. | |

**User's choice:** 1A - strictly conservative.
**Notes:** Phase 4 explicitly says current artifacts are blocked/non-claim-ready. Phase 5 must frame safely rather than strengthen claims.

---

## Output Target

| Option | Description | Selected |
|--------|-------------|----------|
| Support documents | Keep Markdown outlines and `CLAIM_GUARD.json` as safe inputs for later LaTeX writing. | yes |
| LaTeX draft | Add or update LaTeX section drafts while still using claim guard limits. | |
| Bilingual support | Generate Chinese writing aid plus English manuscript outline. | |

**User's choice:** 2A - support documents.
**Notes:** This keeps Phase 5 as reproducible manuscript support, not final paper prose.

---

## Claim Strictness

| Option | Description | Selected |
|--------|-------------|----------|
| Fail closed | If any claim-ready flag is false, empirical superiority, ranking, and policy recommendation claims are blocked. | yes |
| Allow weak wording | Allow preliminary or diagnostic-trend language but prohibit formal conclusions. | |
| Checklist only | List allowed/blocked claims without script/JSON enforcement. | |

**User's choice:** 3A - fail closed.
**Notes:** Claim checks should read `ARTIFACT_STATUS.json`, including checkpoint blockers and `claim_ready` flags.

---

## the agent's Discretion

- Exact helper/module names.
- Exact Markdown section wording as long as blocked evidence remains blocked.
- Whether to create a small reusable module or keep logic inside one script.

## Deferred Ideas

- Final LaTeX prose after claim-ready pilot/formal evidence exists.
- Pilot/formal execution after the required checkpoint is supplied.
