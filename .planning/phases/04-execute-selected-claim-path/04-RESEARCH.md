# Phase 4 Research: Execute Selected Claim Path

**Phase:** 04 - Execute Selected Claim Path
**Created:** 2026-06-17
**Status:** Complete
**Mode:** Inline research, because subagent spawning was not explicitly authorized in this runtime.

## Research Question

What does Phase 4 need to execute the evidence-authorized claim path without
turning gate cleanup into result tuning?

Phase 4 must attempt Path A only through a strict pre-replay gate pass. It may
create current freeze/protocol records and generated readiness metadata from
current manifests and current filesystem state. Final replay is allowed only if
all pre-replay gates pass. If gates remain blocked, if a second same-settings
technical replay fails, or if regenerated strict `CLAIM_GUARD.json` remains
`claim_ready=false`, Phase 4 must lock Path B: the conditional diagnostic
manuscript path.

## Current Evidence And Routing State

- Active runtime root is `work2_coding/`.
- Phase 3 classified final replay as `blocked_pending_gate_cleanup`.
- Immediate final replay is not authorized.
- `.planning/results/CALIBRATION_PROTOCOL.md` and
  `.planning/results/FROZEN_FINAL_SETTINGS.md` are absent/deleted in the
  current worktree.
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml` is a
  `pilot` / `calibration_only` manifest.
- `work2_coding/Experiments/studies/final_robust_menu.yaml` is a `formal` /
  `final_claim_candidate_after_gates` manifest.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` is an older
  formal comparison contract and remains useful as a code contract reference,
  but Phase 4's selected Path A should use `final_robust_menu` after gates.
- The current Phase 10 package has `claim_ready=false` and
  `strict_claim_guard_claim_ready=false`.
- The only currently ready strict claim is
  `C7_provenance_status_transparency`.

## Runtime Contract Findings

The approved script surfaces are:

- `python scripts/test_calibration_manifests.py`
- `python scripts/test_calibration_protocol.py`
- `python scripts/test_frozen_final_settings.py`
- `python scripts/check_formal_readiness.py --study final_robust_menu --output-root outputs/formal_readiness --diagnostic-ok`
- `python scripts/run_study.py --study final_robust_menu --execute --output-root outputs/studies/final_rc`
- `python scripts/build_artifacts.py --study final_robust_menu --study-output-root outputs/studies/final_rc --output-root <final-artifact-root> --claim-ready --readiness-json outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json`
- `python scripts/build_phase10_paper_artifacts.py --output-root <final-package-root> --main-artifact-root <final-artifact-root> --no-mirror`

`check_formal_readiness.py` writes `FORMAL_READINESS.json`,
`FORMAL_READINESS.md`, and a dependency snapshot. With `--diagnostic-ok`, the
command can return zero while still recording `status=blocked`; Phase 4 must
inspect the JSON status, not just the process exit code.

`run_study.py` writes manifest snapshots, normalized rows, summaries, and
blockers under the requested output root. Formal studies cannot emit
contract-only rows, and blocked prerequisites produce blocked rows rather than
claim-ready evidence.

`build_artifacts.py --claim-ready` requires a readiness JSON for formal rows.
It blocks dirty readiness, bad checkpoint metadata, manifest mismatch, failed
rows, placeholder rows, and missing dependency/checkpoint evidence.

`build_phase10_paper_artifacts.py` writes the strict package index and claim
guard. Path A should first write an explicit final package directory with
`--no-mirror`. The root paper-facing mirror may be updated only after package
status and SHA/drift checks are recorded.

## Current Filesystem Probe

Current pre-planning probes found:

- `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`
  exists.
- `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt.sidecar.json`
  is absent.
- `work2_coding/outputs/shared_training/work2_robust_menu/final/supervised_ml.pt`
  is absent.
- `work2_coding/outputs/shared_training/work2_robust_menu/final/supervised_ml.pt.sidecar.json`
  is absent.

These observations strongly suggest Path A may fail the pre-replay gate unless
the executor can prove an approved, non-result-affecting provenance repair from
current filesystem state. The plan should not pre-decide the outcome; it should
force the executor to record the gate status and lock Path B if blockers
remain after the one authorized readiness pass.

## Claim Guard Findings

The current strict claim table is the Phase 4 claim ceiling until regenerated
evidence changes it:

| Claim ID | Current status | Manuscript use |
| --- | --- | --- |
| `C1_central_adaptive_menu_superiority` | unsupported/blocked | Not allowed |
| `C2_product_ablation_value` | conditional diagnostic/blocked | No positive claim |
| `C3_adaptive_window_increment` | unsupported | Not allowed |
| `C4_menu_construction_value` | conditional diagnostic/blocked | No positive claim |
| `C5_eta_robustness_boundary` | diagnostic only | Diagnostic boundary only |
| `C6_exact_greedy_computational_credibility` | blocked diagnostic | No credibility claim |
| `C7_provenance_status_transparency` | status supported | Status/provenance transparency only |
| `C8_semi_real_case_validation` | scaffold only/blocked | Not allowed |

If regenerated `CLAIM_GUARD.json` remains `claim_ready=false`, that result is
evidence. Phase 4 must not tune manifests, reduce scale, remove baselines,
delete rows, or rerun again to force a positive claim.

## Planning Implications

Phase 4 should use one plan with explicit branch gates:

1. Create current, non-tuning `CALIBRATION_PROTOCOL.md` and
   `FROZEN_FINAL_SETTINGS.md` records from current manifests and Phase 3 rules.
2. Run manifest/protocol/freeze tests and one formal readiness pass for
   `final_robust_menu`.
3. If readiness is blocked, write the diagnostic lock package immediately.
4. If readiness passes, run one final replay and at most one same-settings
   technical rerun.
5. If replay completes, build artifacts and a strict final package under
   explicit final evidence directories.
6. Let regenerated strict `CLAIM_GUARD.json` decide whether Phase 5 receives
   claim-ready, conditional, or diagnostic-only manuscript instructions.

## RESEARCH COMPLETE
