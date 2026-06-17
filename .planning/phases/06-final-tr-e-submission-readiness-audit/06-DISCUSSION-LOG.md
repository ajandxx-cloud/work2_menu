# Phase 6: Final TR-E Submission Readiness Audit - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-17T21:33:08.4394119+08:00
**Phase:** 6-Final TR-E Submission Readiness Audit
**Areas discussed:** Final recommendation stance, TR-E reviewer risk ordering, Revision task list granularity, Verification threshold

---

## Final Recommendation Stance

| Option | Description | Selected |
|--------|-------------|----------|
| Revise first | Default to `revise-before-submission`, matching the current `claim_ready=false` boundary. | Yes |
| Diagnostic draftable | Treat the manuscript as diagnostic-only but draftable. | |
| Agent decides | Let Phase 6 execution decide the final label based on audit results. | |

**User's choice:** Revise first.
**Notes:** The user also selected preserving `diagnostic-only but draftable` as a secondary conclusion, downgrading to `not ready` only for hard failures, and using a two-layer report style: hard audit conclusions plus author-friendly revision tasks.

---

## TR-E Reviewer Risk Ordering

| Option | Description | Selected |
|--------|-------------|----------|
| Claim/evidence safety first | Prioritize claim safety, source traceability, and reproducibility before TR-E contribution review. | |
| TR-E contribution first | Prioritize novelty, transportation relevance, and model rigor before evidence compliance review. | |
| Two-axis matrix | Audit TR-E contribution risk and evidence compliance risk side by side. | Yes |

**User's choice:** Two-axis matrix.
**Notes:** The user selected no automatic single-axis veto, `Blocker`/`Major`/`Minor` risk levels, and a status for every audit dimension.

---

## Revision Task List Granularity

| Option | Description | Selected |
|--------|-------------|----------|
| Submission blocker list | Prioritize blockers first, then major/minor revisions. | |
| Section-by-section plan | Organize all tasks by manuscript section. | |
| Hybrid | Combine priority order with section mapping. | |
| User-provided hybrid template | Use the exact template supplied by the user. | Yes |

**User's choice:** User-provided hybrid template.
**Notes:** `Submission Blockers` should contain only true hard blockers. Every Blocker and Major task must bind to evidence/source references. Every task should include checkable completion criteria. The final checklist should include required command checks.

---

## Verification Threshold

| Option | Description | Selected |
|--------|-------------|----------|
| Add manuscript checks | Add manuscript file, source-map, prohibited-language, and traceability checks beyond roadmap commands. | Yes |
| Only run roadmap commands | Keep verification to the roadmap command set. | |
| Manual audit without new script | Review manuscript package manually without adding a new script. | |

**User's choice:** Add manuscript checks.
**Notes:** The user selected adding a lightweight script such as `work2_coding/scripts/test_manuscript_readiness_package.py`. The script should fail only on hard contract breaks, not qualitative writing or novelty judgments. The final audit should record PASS/FAIL and a short output summary for each command. If the manuscript readiness script fails, final recommendation cannot exceed `revise-before-submission`; source traceability or claim-safety hard failures may downgrade to `not ready`.

---

## the agent's Discretion

- Choose the exact layout of the two-axis audit matrix.
- Choose the internal implementation structure of the new manuscript readiness script.
- Choose exact task wording while preserving the user-provided task template and all locked claim boundaries.

## Deferred Ideas

None. Discussion stayed within Phase 6 scope.
