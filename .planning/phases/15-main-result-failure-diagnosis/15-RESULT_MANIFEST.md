# Phase 15 Result Manifest

Date: 2026-06-16

Phase: 15 - Main Result Failure Diagnosis

## Deliverables

Phase 15 created the following diagnosis outputs:

- `.planning/milestones/claim_ready_resolution/03_RANDOM_BASELINE_DIAGNOSIS.md`
- `.planning/milestones/claim_ready_resolution/03_ADAPTIVE_WINDOW_DIAGNOSIS.md`
- `.planning/milestones/claim_ready_resolution/03_OBJECTIVE_EVALUATION_ALIGNMENT.md`
- `.planning/milestones/claim_ready_resolution/03_RECOVERABILITY_DECISION.md`
- `.planning/phases/15-main-result-failure-diagnosis/15-RESULT_MANIFEST.md`

## Diagnosis-Only Declaration

Phase 15 performed diagnosis only.

It inspected existing source rows, generated summaries, artifact package metadata, manifests, and code paths. It did not:

- Run new empirical experiments.
- Tune parameters.
- Regenerate empirical rows.
- Modify algorithms.
- Repair gates.
- Regenerate artifacts.
- Choose Path A, Path B, or Path C.
- Upgrade manuscript claims.
- Delete, hide, or reclassify `mainline_random_menu`.
- Claim adaptive-window value while optimized adaptive and optimized fixed-window remain identical across tracked metrics.

## Binding Inputs Used

Phase 15 used the Phase 13 and Phase 14 outputs as binding inputs:

- `.planning/milestones/claim_ready_resolution/01_EVIDENCE_BOUNDARY.md`
- `.planning/milestones/claim_ready_resolution/01_CLAIM_READY_FALSE_CAUSES.md`
- `.planning/milestones/claim_ready_resolution/01_BLOCKER_TAXONOMY.md`
- `.planning/milestones/claim_ready_resolution/02_GATE_REPAIR_PLAN.md`
- `.planning/milestones/claim_ready_resolution/02_DIRTY_GIT_ACTIONS_REQUIRED.md`
- `.planning/milestones/claim_ready_resolution/02_ARTIFACT_SCHEMA_REPAIR_PLAN.md`
- `.planning/milestones/claim_ready_resolution/02_CHECKPOINT_PROVENANCE_PLAN.md`

## Result Summary

- Random baseline diagnosis: `mainline_random_menu` has higher mean net profit because it has lower realized operating/service cost and lower discount cost, despite lower acceptance and higher opt-out.
- Adaptive-window diagnosis: `mainline_optimized_adaptive` and `mainline_optimized_fixed_window` appear behaviorally degenerate in the inspected implementation; this is not support for a scientific adaptive-window equivalence claim.
- Objective/evaluation alignment: optimized menu selection may improve a predicted proxy objective that does not translate into realized replay net profit; persisted rows lack enough predicted-objective diagnostics to close the causal chain.
- Recoverability evidence: the central positive claim is conditionally recoverable but unsupported by current selected formal evidence. Metadata repair alone is insufficient; implementation/configuration repair and any rerun would require explicit Phase 16 authorization.

## Verification

Required verification commands for Phase 15:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config"
python scripts/test_phase10_paper_artifacts.py
python scripts/test_manuscript_claim_guard.py
python scripts/test_paired_replay_contract.py
python scripts/test_policy_fairness_contract.py
```

Markdown diff check:

```powershell
git diff --check -- .planning/milestones/claim_ready_resolution/03_RANDOM_BASELINE_DIAGNOSIS.md .planning/milestones/claim_ready_resolution/03_ADAPTIVE_WINDOW_DIAGNOSIS.md .planning/milestones/claim_ready_resolution/03_OBJECTIVE_EVALUATION_ALIGNMENT.md .planning/milestones/claim_ready_resolution/03_RECOVERABILITY_DECISION.md .planning/phases/15-main-result-failure-diagnosis/15-RESULT_MANIFEST.md
```

The executed verification result is reported in the Phase 15 completion response.
