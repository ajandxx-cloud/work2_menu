# Phase 3: Formal RC Evidence Pipeline Repair And Completion - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-15T11:03:25+08:00
**Phase:** 3-Formal RC Evidence Pipeline Repair And Completion
**Areas discussed:** existing formal run positioning, dirty-git gate, failed run retention, artifact and claim-ready boundary, failure outputs, verification strength, checkpoint policy, success definition

---

## Existing Formal Run Positioning

| Option | Description | Selected |
|--------|-------------|----------|
| A | Use the latest completed formal run as candidate formal evidence input, but only claim-ready after readiness/artifact/claim guard gates approve. | Yes |
| B | Treat it only as diagnostic material and rerun formal after clean git. | |
| C | Use it for pipeline status but require a newly gated run as final output. | |
| D | Let the agent decide. | |

**User's choice:** 1A  
**Notes:** Latest completed run observed: `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a`.

---

## Dirty Git Gate

| Option | Description | Selected |
|--------|-------------|----------|
| A | First write `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` with dirty paths, blockers, and cleanup/commit/stash recommendations; wait for confirmation before cleanup. | Yes |
| B | Include organizing and committing relevant runtime/planning changes in Phase 3 to unlock readiness. | |
| C | Ignore dirty git for now and defer claim-ready status. | |
| D | Let the agent decide. | |

**User's choice:** 2A  
**Notes:** No automatic destructive cleanup or broad git state mutation.

---

## Failed Run Retention

| Option | Description | Selected |
|--------|-------------|----------|
| A | Keep the older failed run as failure diagnostic evidence, including `UnboundLocalError` and 7 failed rows. | Yes |
| B | Ignore the old run and only use the latest completed run. | |
| C | Keep it but exclude it from artifacts, mentioning it only in Phase 3 summary/diagnosis. | |
| D | Let the agent decide. | |

**User's choice:** 3A  
**Notes:** Failed run observed: `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T031927Z-fca35a73`.

---

## Artifact And Claim-Ready Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| A | If readiness or claim guard does not approve, generate diagnostic artifacts only and prohibit paper-facing positive result artifacts. | Yes |
| B | Generate tables/figures but label them non-claim or diagnostic. | |
| C | Generate only machine-readable JSON/CSV/status, no manuscript frame. | |
| D | Let the agent decide. | |

**User's choice:** 4A  
**Notes:** Current `ARTIFACT_STATUS.json` and `CLAIM_GUARD.json` observed as diagnostic/not claim-ready.

---

## Failure Outputs

| Option | Description | Selected |
|--------|-------------|----------|
| A | Failed formal replay must write normalized rows with `status`, `error_type`, and `error_message`. | |
| B | Failed formal replay writes blocker diagnosis only, not failed rows. | |
| C | Preserve both failed rows and blocker diagnosis. | Yes |
| D | Let the agent decide. | |

**User's choice:** 5C  
**Notes:** This keeps failure mode and row comparability visible for Phase 4 or debugging.

---

## Verification Strength

| Option | Description | Selected |
|--------|-------------|----------|
| A | Minimal: import, formal readiness, and formal replay enablement. | |
| B | Standard: include import/readiness/replay enablement plus opt-out, paired replay, policy fairness, checkpoint provenance, and artifact gates. | Yes |
| C | Full: run every related `scripts/test_*.py`; slower. | |
| D | Let the agent decide. | |

**User's choice:** 6B  
**Notes:** Standard verification balances evidence integrity with scope.

---

## Checkpoint Policy

| Option | Description | Selected |
|--------|-------------|----------|
| A | Reuse an existing checkpoint when load status is `loaded`, while re-recording hash and provenance. | Yes |
| B | Always retrain the shared checkpoint for reproducibility. | |
| C | Run readiness first; retrain only if checkpoint/hash/provenance is inconsistent. | |
| D | Let the agent decide. | |

**User's choice:** 7A  
**Notes:** Existing formal checkpoint path: `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`.

---

## Success Definition

| Option | Description | Selected |
|--------|-------------|----------|
| A | Phase 3 succeeds when formal replay is completed and rows are comparable; claim-ready can remain a later gate. | Yes |
| B | Phase 3 succeeds only if readiness, formal replay, artifact status, and claim guard all pass. | |
| C | Use tiered success: pipeline-complete, artifact-ready, claim-ready. | |
| D | Let the agent decide. | |

**User's choice:** 8A  
**Notes:** Claim-ready remains controlled by explicit gate artifacts.

---

## Context Write Confirmation

| Option | Description | Selected |
|--------|-------------|----------|
| A | Write Phase 3 CONTEXT.md and DISCUSSION-LOG.md. | Yes |
| B | Continue with more questions. | |
| C | Pause without writing files. | |

**User's choice:** 9A  
**Notes:** User approved writing workflow artifacts.

## The Agent's Discretion

- The planner may decide whether to validate the latest completed formal run first or rerun after readiness diagnostics, provided the locked gate boundaries are respected.
- The planner may choose exact diagnostic artifact output roots while preserving the active runtime root and formal evidence boundaries.

## Deferred Ideas

None - discussion stayed within Phase 3 scope.
