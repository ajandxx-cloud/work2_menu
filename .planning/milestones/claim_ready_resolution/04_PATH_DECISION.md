---
phase: 16
status: path_decision_complete
selected_path: Path C
claim_ready: false
generated_at: 2026-06-16T19:24:25+08:00
timezone: Asia/Shanghai
decision_only: true
source_claim_guard: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json
---

# Phase 16 Claim-Ready Path Decision

## 1. selected_path

`Path C: conditional diagnostic lock`

## 2. reason

Path C is selected because the current blockers are not gate-only and a
claim-ready rerun is not valid under the current frozen settings. Phase 13
established `claim_ready=false`; Phase 14 showed that some metadata and
artifact repairs are possible but are insufficient for the central empirical
claim; Phase 15 showed substantive blockers: `mainline_random_menu` currently
outperforms `mainline_optimized_adaptive` on mean realized net profit,
adaptive and fixed-window optimized policies are behaviorally degenerate in
the inspected implementation path, and objective/evaluation alignment remains
suspect.

This makes Path A invalid because empirical evidence is not already
sufficient. It makes Path B invalid for Phase 17 because the frozen final
settings are `blocked_pending_gate_cleanup`, the adaptive-window
implementation/configuration issue would invalidate a claim-ready rerun, and a
rerun aimed at rescuing the central result after observing random-menu
outperformance would be result-chasing unless a later milestone creates a new,
pre-registered implementation-fix protocol.

## 3. evidence basis from Phase 13-15

Phase 13 binding evidence:

- `01_EVIDENCE_BOUNDARY.md` records the selected 35-row formal run as
  diagnostic source evidence only, not claim-ready evidence.
- EB-004 records that `mainline_random_menu` has better mean net profit than
  `mainline_optimized_adaptive`, and adaptive loses to random on net profit in
  3 of 5 paired splits.
- EB-005 records that `mainline_optimized_adaptive` and
  `mainline_optimized_fixed_window` are identical across tracked metrics and
  all five paired splits.
- EB-016, EB-017, and EB-020 record that the Phase 10 package has
  `claim_ready=false`, `manuscript_positive_claims_allowed=false`, six blocked
  positive claim ids, C5 diagnostic-only status, and C7 status/provenance-only
  support.
- `01_CLAIM_READY_FALSE_CAUSES.md` classifies random-menu profit advantage as
  CF-005, adaptive-window equality as CF-006, Phase 8 sensitivity as
  diagnostic/provisional, Phase 9 tractability as diagnostic/provisional, and
  case evidence as scaffold-only.
- `01_BLOCKER_TAXONOMY.md` states that random-baseline and adaptive-window
  blockers are not repairable by metadata or wording and that
  `mainline_random_menu` must remain visible as a serious comparator.

Phase 14 binding evidence:

- `02_GATE_REPAIR_PLAN.md` identifies safe candidate metadata, provenance, and
  artifact-builder repairs, but GR-018 and GR-019 classify random-menu
  outperformance and adaptive/fixed equality as not legitimate gate-only
  repairs.
- `02_ARTIFACT_SCHEMA_REPAIR_PLAN.md` records missing `method_family`,
  `outside_option_util`, and `solver_candidate_count` in the selected rows as
  true source-row or evidence-quality issues, not hand-editable package noise.
- `02_CHECKPOINT_PROVENANCE_PLAN.md` records that Path A would not be enough if
  strict readiness requires clean source-row provenance, reconstructed sidecar
  provenance is insufficient, missing schema fields must exist in original
  rows, or empirical performance blockers remain central.
- `02_DIRTY_GIT_ACTIONS_REQUIRED.md` records that the live tree was clean, but
  historical dirty provenance remains in generated evidence and cannot be
  erased by current cleanup.

Phase 15 binding evidence:

- `03_RANDOM_BASELINE_DIAGNOSIS.md` decomposes the mean net-profit gap:
  random beats adaptive by 3930.23, mostly through lower operating/service
  cost and lower discount cost, while adaptive improves acceptance and reduces
  opt-out at a realized cost that exceeds additional realized revenue.
- `03_ADAPTIVE_WINDOW_DIAGNOSIS.md` finds that fixed-window and adaptive-window
  modes appear behaviorally collapsed in `DSPO_Menu`; only `no_time_window`
  has distinct behavior in the inspected path.
- `03_OBJECTIVE_EVALUATION_ALIGNMENT.md` finds that the optimized menu
  objective may be improving a predicted proxy objective that does not
  translate into realized replay net profit, and the selected rows do not
  persist enough diagnostics to close the causal chain.
- `03_RECOVERABILITY_DECISION.md` states that the central positive claim is
  conditionally recoverable but unsupported by current evidence, and that
  metadata repair alone is insufficient.
- `15-RESULT_MANIFEST.md` confirms that Phase 15 was diagnosis-only and did
  not hide, remove, or reclassify `mainline_random_menu`.

Calibration and frozen-setting evidence:

- `CALIBRATION_PROTOCOL.md` prohibits final-result tuning, baseline deletion,
  metric deletion, generated-row edits, and claim-guard hand edits.
- `FROZEN_FINAL_SETTINGS.md` records `final_status:
  blocked_pending_gate_cleanup`, preserves all seven policy tags including
  `mainline_random_menu`, and states that final replay is not authorized until
  provenance, checkpoint, readiness, row metadata, and artifact gates pass.

Phase 10 package evidence:

- `CLAIM_GUARD.json` uses schema `phase10-strict-claim-guard-v1`, contains 8
  claims, keeps overall `claim_ready=false`, and keeps
  `manuscript_positive_claims_allowed=false`.
- `PACKAGE_INDEX.json` contains 74 indexed artifacts across blocker/status,
  main RC, Phase 8 sensitivity, Phase 9 tractability, and case scaffold source
  families.
- `10-VERIFICATION.md` and `10-REVIEW.md` report a verified Phase 10 package
  with no open review findings, but the package remains claim-boundary
  infrastructure and does not authorize claim upgrades.

## 4. allowed actions

For Phase 17, the allowed actions are limited to Path C execution:

- Write a formal diagnostic lock under
  `.planning/milestones/claim_ready_resolution/05C_DIAGNOSTIC_LOCK.md`.
- Write a safe claim table under
  `.planning/milestones/claim_ready_resolution/05C_SAFE_CLAIM_TABLE.md`.
- Write prohibited manuscript language under
  `.planning/milestones/claim_ready_resolution/05C_PROHIBITED_LANGUAGE.md`.
- Write manuscript positioning under
  `.planning/milestones/claim_ready_resolution/05C_MANUSCRIPT_POSITIONING.md`.
- Preserve `mainline_random_menu` as a serious comparator and report its
  current profit advantage rather than hiding, removing, or downgrading it.
- Preserve the Phase 10 strict claim guard as binding claim authority.
- Use existing Phase 13-16 evidence to frame conditional diagnostic claims,
  limitations, future-work requirements, and status/provenance transparency.
- Keep opt-out accounting separate from accepted home pickup in any written
  interpretation.
- Run lightweight verification commands only; do not run empirical replay or
  artifact regeneration.

## 5. prohibited actions

Phase 17 must not:

- Execute Path A or Path B.
- Run new empirical experiments, final replay, calibration replay, sensitivity
  replay, tractability replay, or case-study replay.
- Tune parameters, alter frozen settings, change seeds, remove splits, remove
  metrics, or remove baselines.
- Modify algorithms, policy adapters, manifests, row builders, artifact
  builders, or claim-guard code.
- Repair readiness gates, repair artifact gates, or regenerate paper artifacts.
- Regenerate `CLAIM_GUARD.json`, `PACKAGE_INDEX.json`, generated rows,
  generated tables, generated figures, or manuscript-frame artifacts.
- Hand-edit generated rows or generated paper artifacts.
- Upgrade manuscript claims by wording.
- Claim adaptive-menu superiority, adaptive-window increment, menu-construction
  value, product-ablation value, near-optimal greedy behavior, online
  tractability, case-study validation, real passenger behavior, or no-filter
  operational recommendation.
- Hide, remove, relabel, or downgrade `mainline_random_menu` because it
  outperforms `mainline_optimized_adaptive`.

## 6. claim ceiling

The claim ceiling is conditional diagnostic only:

- Overall manuscript status remains `claim_ready=false`.
- C1 central adaptive-menu superiority remains unsupported/blocked.
- C2 product-ablation value remains conditional diagnostic or blocked.
- C3 adaptive-window increment remains blocked.
- C4 menu-construction value remains conditional diagnostic or blocked.
- C5 ETA robustness boundary remains diagnostic-only.
- C6 exact/greedy computational credibility remains blocked diagnostic.
- C7 provenance/status transparency remains the only claim-ready item, and it
  is not evidence of empirical effectiveness.
- C8 semi-real case validation remains scaffold-only blocked.

The paper may claim that the current evidence identifies when optimized
service menus improve service-quality metrics but fail to recover realized net
profit under the selected paired replay. It may not claim that optimized
adaptive menus are superior.

## 7. whether a positive central claim is allowed

No. A positive central claim is not allowed.

## 8. whether a conditional claim is allowed

Yes. Conditional diagnostic claims are allowed if they preserve the random
baseline result, adaptive/fixed-window blocker, Phase 8/9 diagnostic labels,
and Phase 10 claim guard boundaries.

## 9. whether the manuscript must remain diagnostic

Yes. The manuscript must remain diagnostic unless a later milestone creates new
authorized evidence and a regenerated strict claim guard passes. Phase 17 under
this decision does not authorize that.

## 10. whether implementation/configuration degeneracy blocks claim-ready rerun

Yes. The adaptive-window handling degeneracy blocks a claim-ready rerun under
the current implementation/configuration. A rerun with the current behavior
would not create valid adaptive-window value evidence, and a behavior-changing
fix would require a separate pre-registered implementation verification and
rerun protocol outside the selected Phase 17 Path C work.

## 11. whether the frozen final settings are still valid

The frozen final settings remain valid as a historical anti-p-hacking contract
and evidence-boundary record. They are not valid authorization for a Phase 17
claim-ready rerun.

Reasons:

- `FROZEN_FINAL_SETTINGS.md` itself records `final_status:
  blocked_pending_gate_cleanup`.
- The settings predate the Phase 15 adaptive-window implementation diagnosis.
- Current implementation/configuration degeneracy would invalidate adaptive
  window evidence under those settings.
- Objective/evaluation alignment remains unresolved.
- The current evidence includes an unfavorable random-menu comparator result
  that cannot be tuned around.

## 12. whether any rerun would be legitimate or would constitute result-chasing

Under Phase 17 as selected here, any empirical rerun is prohibited and would be
outside scope.

A rerun under the current frozen settings would not be legitimate for
claim-ready recovery because final status is blocked and adaptive-window
behavior is degenerate. A rerun aimed at reversing the observed
`mainline_random_menu` profit advantage, without a new pre-registered
implementation-fix protocol and strict no-tuning guardrails, would constitute
result-chasing.

A future rerun could become legitimate only in a later milestone if it is
pre-registered before execution, follows documented implementation
verification, preserves paired replay fairness and the seven policy tags, keeps
`mainline_random_menu` visible, records checkpoint provenance, and accepts all
outcomes including continued `claim_ready=false`.

## 13. required Phase 17 execution instructions for the selected path

Phase 17 must execute only Path C.

Required inputs:

- `.planning/milestones/claim_ready_resolution/01_EVIDENCE_BOUNDARY.md`
- `.planning/milestones/claim_ready_resolution/01_CLAIM_READY_FALSE_CAUSES.md`
- `.planning/milestones/claim_ready_resolution/01_BLOCKER_TAXONOMY.md`
- `.planning/milestones/claim_ready_resolution/02_GATE_REPAIR_PLAN.md`
- `.planning/milestones/claim_ready_resolution/02_DIRTY_GIT_ACTIONS_REQUIRED.md`
- `.planning/milestones/claim_ready_resolution/02_ARTIFACT_SCHEMA_REPAIR_PLAN.md`
- `.planning/milestones/claim_ready_resolution/02_CHECKPOINT_PROVENANCE_PLAN.md`
- `.planning/milestones/claim_ready_resolution/03_RANDOM_BASELINE_DIAGNOSIS.md`
- `.planning/milestones/claim_ready_resolution/03_ADAPTIVE_WINDOW_DIAGNOSIS.md`
- `.planning/milestones/claim_ready_resolution/03_OBJECTIVE_EVALUATION_ALIGNMENT.md`
- `.planning/milestones/claim_ready_resolution/03_RECOVERABILITY_DECISION.md`
- `.planning/milestones/claim_ready_resolution/04_PATH_DECISION.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
- `.planning/results/CALIBRATION_PROTOCOL.md`
- `.planning/results/FROZEN_FINAL_SETTINGS.md`

Required deliverables:

- `.planning/milestones/claim_ready_resolution/05C_DIAGNOSTIC_LOCK.md`
- `.planning/milestones/claim_ready_resolution/05C_SAFE_CLAIM_TABLE.md`
- `.planning/milestones/claim_ready_resolution/05C_PROHIBITED_LANGUAGE.md`
- `.planning/milestones/claim_ready_resolution/05C_MANUSCRIPT_POSITIONING.md`
- `.planning/phases/17-execute-selected-claim-path/17-RESULT_MANIFEST.md`

Required Phase 17 content:

- State that `claim_ready=false` remains binding.
- State that Path A and Path B were not executed.
- Preserve `mainline_random_menu` outperformance as a reported comparator
  result.
- State that adaptive-window value is blocked by implementation/configuration
  degeneracy and current rows.
- State that objective/evaluation alignment remains a diagnostic limitation.
- Convert each Phase 10 claim id into one of: status/provenance allowed,
  conditional diagnostic allowed, unsupported/prohibited, or future work.
- Include explicit prohibited language for abstract, introduction, results,
  conclusion, and limitations sections.
- Keep sensitivity, tractability, and case-study material diagnostic,
  diagnostic/provisional, or scaffold-only.

Required Phase 17 verification:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config"
python scripts/test_phase10_paper_artifacts.py
python scripts/test_manuscript_claim_guard.py
```

Diff check for edited markdown:

```powershell
git diff --check -- .planning/milestones/claim_ready_resolution/05C_DIAGNOSTIC_LOCK.md .planning/milestones/claim_ready_resolution/05C_SAFE_CLAIM_TABLE.md .planning/milestones/claim_ready_resolution/05C_PROHIBITED_LANGUAGE.md .planning/milestones/claim_ready_resolution/05C_MANUSCRIPT_POSITIONING.md .planning/phases/17-execute-selected-claim-path/17-RESULT_MANIFEST.md
```

Phase 17 must stop after Path C documentation. It must not repair gates,
regenerate artifacts, or run replay.
