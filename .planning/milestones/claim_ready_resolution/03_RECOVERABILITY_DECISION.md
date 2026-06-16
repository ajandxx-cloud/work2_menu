# Phase 15 Recoverability Decision Evidence

Date: 2026-06-16

Status: diagnosis only. This document does not select Path A, Path B, or Path C. It provides evidence for the Phase 16 path decision.

## Binding Boundaries

- Phase 10 `CLAIM_GUARD.json` remains binding with 8 claims and `claim_ready=false`.
- The random-menu profit advantage remains a serious result.
- Adaptive/fixed-window equality blocks adaptive-window increment claims.
- Missing decomposition fields are reported as unavailable, not inferred.
- Phase 15 does not tune parameters, regenerate empirical rows, modify algorithms, repair gates, regenerate artifacts, upgrade claims, or choose a path.

## Overall Recoverability Status

The central positive claim is conditionally recoverable, but unsupported by the current selected formal evidence.

Current evidence does not support claim-ready manuscript language because:

- `mainline_random_menu` has higher mean realized net profit than `mainline_optimized_adaptive`.
- `mainline_optimized_adaptive` and `mainline_optimized_fixed_window` are identical across tracked realized metrics.
- Historical selected artifacts have schema/provenance blockers already documented by Phase 13 and Phase 14.
- The optimized menu objective may not align with realized replay net profit, and selected rows lack enough predicted-objective diagnostics to close that question.

The claim is not declared permanently unrecoverable because Phase 15 found plausible implementation/configuration and evidence-packaging failure modes. Those failure modes would require explicit Phase 16 authorization before any fix or rerun.

## Recoverability by Mechanism

| Mechanism | Recoverability contribution | Phase 15 evidence | Limitation |
|---|---|---|---|
| Metadata/schema gate repair | Recoverable for artifact trust and claim gating mechanics only. | Phase 14 identified missing schema/provenance fields and repair plans. | Cannot overturn random advantage or adaptive/fixed equality. |
| Implementation/configuration bug fix | Potentially recoverable for adaptive-window distinction. | `fixed_window` and `adaptive_window` appear behaviorally collapsed in the inspected code path; only `no_time_window` is distinct. | A fix would change behavior and require legitimate rerun; current rows cannot support adaptive-window value. |
| Legitimate pre-registered final rerun | Conditionally recoverable for the empirical claim. | A corrected implementation and schema-complete manifest could produce valid final evidence if Phase 16 authorizes it. | Must not be parameter tuning or result-chasing; current evidence remains negative until superseded by a valid rerun. |
| Diagnostic manuscript lock | Scientifically supported fallback if empirical blockers remain. | Existing rows robustly document random advantage and adaptive/fixed equality as blockers. | Would require downgrading central positive claims, not upgrading them. |

## Evidence for Metadata/Schema Gate Repair

Phase 13 and Phase 14 already establish that selected artifacts are not claim-ready due to provenance and schema issues, including historical dirty-git rows and missing contract fields in selected outputs.

Phase 15 confirms that metadata/schema repair alone would not resolve the central empirical blockers:

- The random-vs-adaptive gap is directly decomposable from existing numeric fields.
- The adaptive/fixed equality is visible in realized metrics and code-path behavior.
- A cleaner artifact schema would improve auditability, but not change the selected historical results.

Therefore, metadata/schema gate repair is necessary for future trust, but insufficient for the current central positive claim.

## Evidence for Implementation/Configuration Bug Fix

Adaptive/fixed equality appears recoverable only through implementation/configuration work, not through interpretation:

- The manifest and adapter create a one-field policy contrast: `time_window_mode=fixed_window` versus `time_window_mode=adaptive_window`.
- The inspected `DSPO_Menu` path treats both values as the same "window enabled" state.
- Window generation, ETA filtering, menu utility, and scoring do not branch on fixed versus adaptive mode.
- Persisted generated window values are unavailable, so current artifacts cannot demonstrate hidden adaptive behavior.

This points to a likely implementation/configuration bug or incomplete implementation. If Phase 16 chooses an implementation path, it should require targeted tests showing that fixed and adaptive windows generate distinct behavior before any rerun.

## Evidence for Legitimate Pre-Registered Final Rerun

A rerun could be scientifically legitimate only if it follows from a documented fix or documented manifest/schema correction, not from tuning around the random baseline.

Phase 15 evidence that a rerun may be needed if recovery is attempted:

- Existing rows do not contain enough predicted-objective diagnostics to fully audit objective/evaluation alignment.
- Adaptive/fixed behavior appears degenerate in the selected implementation.
- Historical selected artifacts have schema/provenance limitations.

Phase 15 evidence that a rerun must be constrained:

- Random-menu outperformance is a real selected-result blocker.
- The optimized adaptive policy's higher service uptake currently comes with higher realized operating and discount cost.
- Any new run must preserve paired replay fairness and checkpoint provenance, and must not hide or reclassify `mainline_random_menu`.

## Evidence for Diagnostic Manuscript Lock

If Phase 16 does not authorize a behavior-changing fix and legitimate final rerun, the current evidence supports a diagnostic manuscript lock rather than a central positive claim.

A diagnostic lock would preserve:

- The random baseline as a serious comparator that outperforms optimized adaptive on mean net profit in the selected evidence.
- The adaptive/fixed equality as a blocker to adaptive-window increment claims.
- The Phase 10 `claim_ready=false` state.
- The distinction between status/provenance support and effectiveness claims.

This would be scientifically defensible if the project chooses not to pursue implementation repair or if later valid evidence still fails to recover the central claim.

## Phase 16 Decision Inputs

Phase 16 should decide among paths using these evidence constraints:

1. If only metadata/schema issues are addressed, the central positive claim remains unsupported.
2. If adaptive-window behavior is repaired, the project needs targeted implementation verification and a legitimate final rerun before making any adaptive-window value claim.
3. If objective/evaluation mismatch is confirmed and scientifically intentional, the manuscript should lock to diagnostic claims unless valid evidence shows realized net-profit recovery.
4. If random-menu superiority persists under valid, schema-complete, paired replay evidence, the main positive claim is unsupported.

Phase 15 does not choose among these options.
