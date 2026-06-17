# Phase 3 Research: Claim-Ready Evidence Decision Gate

**Phase:** 03 - Claim-Ready Evidence Decision Gate
**Created:** 2026-06-17
**Status:** Complete

## Research Question

What does Phase 3 need to know to plan a legitimate Work2 TR-E claim-ready
evidence decision gate?

Phase 3 is not an execution or repair phase. It must decide whether the
project can proceed toward a final claim-ready replay after strict gates, or
whether the manuscript path must be locked as conditional diagnostic from the
current evidence. It may inspect current files and write
`.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`, but it must
not create missing freeze/protocol files, run final replay, run formal
readiness, train checkpoints, regenerate artifacts, replace mirrors, execute a
case study, or upgrade manuscript claims.

## Current Evidence State

- `work2_coding/` is the active runtime root.
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml` exists and
  is a `pilot` / `calibration_only` manifest.
- `work2_coding/Experiments/studies/final_robust_menu.yaml` exists and is a
  `formal` / `final_claim_candidate_after_gates` manifest.
- The calibration manifest references
  `../../.planning/results/CALIBRATION_PROTOCOL.md`.
- The final manifest references both
  `../../.planning/results/CALIBRATION_PROTOCOL.md` and
  `../../.planning/results/FROZEN_FINAL_SETTINGS.md`.
- In the current worktree, `.planning/results/CALIBRATION_PROTOCOL.md` and
  `.planning/results/FROZEN_FINAL_SETTINGS.md` are deleted or absent.
- The final manifest contains `selected_runtime_knobs.source:
  CALIBRATION_PROTOCOL.md pre-run default; not selected from final rows`, but
  Phase 3 context classifies that statement as unverified while the referenced
  protocol file is missing.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
  currently reports `claim_ready=false`,
  `strict_claim_guard_claim_ready=false`, `artifact_count=74`,
  `existing_artifact_count=70`, `missing_artifact_count=4`, and
  `blocker_count=108`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  uses schema `phase10-strict-claim-guard-v1`, reports
  `claim_ready=false`, and marks only
  `C7_provenance_status_transparency` as `claim_ready=true`.

## Manifest Contract Findings

`work2_coding/scripts/test_calibration_manifests.py` defines the relevant
contract for calibration/final separation:

- The calibration and final manifests must preserve the seven mainline policy
  tags.
- The required policy family is:
  `mainline_no_menu`, `mainline_fixed_menu`, `mainline_random_menu`,
  `mainline_optimized_m`, `mainline_optimized_mw`,
  `mainline_optimized_fixed_window`, and
  `mainline_optimized_adaptive`.
- Calibration and final splits must be disjoint.
- Required paired fields include seed/data seed fields, runtime instance,
  checkpoint path/requirement, menu size, candidate count, HGS timing, and
  utility parameters.
- Required varied fields include policy behavior fields such as menu policy,
  product mode, time-window mode, menu contract mode, pricing mode,
  ETA-filter mode, objective mode, and service/opt-out guardrails.
- Output schema must preserve checkpoint provenance and separate
  `count_opted_out`, `count_accepted_home`, and
  `count_accepted_meeting_point`.

This means Phase 3 can treat the current manifests as candidate contracts, but
not as final replay authorization. The missing freeze/protocol evidence and
formal provenance gates still block claim-ready use.

## Gate And Provenance Findings

`work2_coding/Src/formal_readiness.py` and
`work2_coding/Src/artifact_status.py` fail closed on the relevant evidence
boundaries:

- Dirty git blocks claim-ready readiness unless explicitly allowed for a
  diagnostic path.
- Formal readiness writes dependency snapshots and readiness reports as side
  effects, so Phase 3 should not run it.
- Missing formal checkpoint, missing sidecar metadata, failed checkpoint
  smoke-load, and checkpoint hash mismatch are blockers.
- Formal claim-ready artifacts require a dependency snapshot.
- Pilot/formal rows require loaded checkpoint metadata.
- Placeholder, blocked, failed, incomplete, or contract-only rows cannot
  support claim-ready artifacts.
- Pilot/formal rows with invalid accepted-home, accepted-meeting-point, or
  opt-out accounting are blocked.
- No-filter-only and diagnostic run modes remain diagnostic.

Phase 2 already documented the provenance requirements in
`.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` and
approval-required commands in
`.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`.

## Claim Classification Findings

The strict claim guard supports claim-by-claim classification:

| Claim ID | Current claim_ready | Current manuscript_allowed | Phase 3 interpretation |
| --- | --- | --- | --- |
| C1_central_adaptive_menu_superiority | false | false | Not allowed; central superiority remains blocked. |
| C2_product_ablation_value | false | false | Not allowed as positive claim; diagnostic structure only if later allowed by maps. |
| C3_adaptive_window_increment | false | false | Not allowed. |
| C4_menu_construction_value | false | false | Not allowed as positive claim. |
| C5_eta_robustness_boundary | false | true | Allowed only as diagnostic boundary content. |
| C6_exact_greedy_computational_credibility | false | false | Not allowed as computational credibility claim. |
| C7_provenance_status_transparency | true | true | Allowed as status/provenance transparency only. |
| C8_semi_real_case_validation | false | false | Not allowed; case materials remain scaffold-only. |

One passing claim does not upgrade unrelated claims or the whole paper. If
overall `claim_ready=false`, Phase 5 may only use any local
`manuscript_allowed=true` content with explicit claim ID, status, source
artifact, and allowed-use labeling.

## Planning Implications

Phase 3 should be planned as one documentation decision plan. The executor
should:

1. Inspect current manifests, package status, claim guard, prior M1/M2
   milestone files, and the relevant script/gate source files.
2. Write only `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`.
3. Classify current replay status as `blocked_pending_gate_cleanup`, not as
   `authorized`.
4. State that missing freeze/protocol files block immediate final replay but
   do not permanently force diagnostic lock by themselves.
5. State that Phase 4 may perform approved gate cleanup/readiness work, and
   may run final replay only after all pre-replay gates pass.
6. State that Phase 4 cleanup may repair only path, metadata, sidecar, hash,
   dependency, readiness, and evidence-chain records. It must not alter policy
   family, split IDs, seeds, metrics, or frozen runtime settings such as
   `menu_k`, `max_candidates`, ETA filter mode, guardrails, or other
   result-affecting knobs.
7. State that if pre-replay gates fail, Phase 4 must lock the diagnostic path
   without running final replay.
8. State that if final replay starts and fails for technical reasons, at most
   one technical rerun is allowed with the same manifest, git SHA, checkpoint
   path/hash, seeds, splits, policies, and frozen settings.
9. State that if replay completes but regenerated `CLAIM_GUARD.json` remains
   `claim_ready=false`, the project must proceed with diagnostic or
   conditional manuscript framing, not tuning.

## Validation Architecture

Phase 3 validation should use source assertions and non-generating script tests:

- Import smoke from `work2_coding/`:
  `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`
- Manifest contract test:
  `python scripts/test_calibration_manifests.py`
- File existence/source assertions for
  `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`.
- Negative source assertions that the Phase 3 execution did not create
  `.planning/results/FROZEN_FINAL_SETTINGS.md` or
  `.planning/results/CALIBRATION_PROTOCOL.md`.
- Generated-evidence diff-name check:
  `git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts`

Do not run `test_frozen_final_settings.py` or
`test_calibration_protocol.py` as passing gates in Phase 3 because their
target documents are intentionally missing and must not be created during this
phase. These tests define future Phase 4 cleanup contracts.

## RESEARCH COMPLETE
