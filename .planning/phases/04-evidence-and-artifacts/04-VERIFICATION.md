---
phase: 04-evidence-and-artifacts
status: passed
verified: 2026-06-11
requirements:
  - ART-01
  - ART-02
  - ART-03
  - ART-04
---

# Phase 04 Verification: Evidence And Artifacts

## Result

Status: passed

Phase 4 achieved its bounded goal: the repository now has a reproducible evidence/artifact pipeline that writes normalized rows, aggregate summaries, table families, figure/status artifacts, provenance sidecars, and mirrored review artifacts. The current generated artifact bundle is explicitly **blocked / not claim-ready** because the required pilot checkpoint is unavailable and formal evidence was skipped; no placeholder or checkpoint-blocked evidence is presented as formal support.

## Requirement Traceability

| Requirement | Status | Evidence |
|-------------|--------|----------|
| ART-01 | passed | `scripts/run_study.py`, `Src/paired_replay.py`, and `Src/study_execution.py` write normalized rows with run ID, manifest/settings/trace hashes, checkpoint fields, status, placeholder flag, and git provenance. `ARTIFACT_STATUS.json` and aggregate JSON/CSV are generated from those rows. |
| ART-02 | passed | `Src/artifact_builder.py` and generated `tables/*.tex` cover policy summary, robust filtering, exact/greedy diagnostics, uptake regime behavior, and provenance/status. |
| ART-03 | passed | `Src/artifact_builder.py` generates PNG figures when metrics are available and explicit `.status.json` files when metric families are unavailable. The current bundle records incomplete figure statuses instead of fabricating charts. |
| ART-04 | passed | `Src/artifact_status.py`, artifact sidecars, and `ARTIFACT_STATUS.json` record manifest hash, run ID, git state, checkpoint provenance, placeholder/incomplete/blocked status, and claim readiness gates. |

## Automated Checks

- `cd work2_coding; python scripts/test_experiment_contracts.py` -> `PASS: 12 experiment contract tests`
- `cd work2_coding; python scripts/test_paired_replay_contract.py` -> `PASS: 10 paired replay contract tests`
- `cd work2_coding; python scripts/test_policy_fairness_contract.py` -> `PASS: 10 policy fairness contract tests`
- `cd work2_coding; python scripts/test_smoke_study_rows.py` -> `PASS: 9 smoke study row tests`
- `cd work2_coding; python scripts/test_study_execution_status.py` -> `PASS: 6 study execution status tests`
- `cd work2_coding; python scripts/test_artifact_builder.py` -> `PASS: 5 artifact builder tests`
- `cd work2_coding; python scripts/test_artifact_gates.py` -> `PASS: 6 artifact gate tests`
- `cd work2_coding; python scripts/test_phase4_artifact_pipeline.py` -> `PASS: 2 Phase 4 artifact pipeline tests`
- `cd work2_coding; python scripts/run_phase4_artifacts.py --study pilot_robust_menu --allow-incomplete --skip-formal` -> wrote `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` and mirrored `artifacts/work2_robust_menu/ARTIFACT_STATUS.json`
- `cd work2_coding; python scripts/run_study.py --study smoke_robust_menu --contract-only --output-root <temp>` -> wrote normalized rows and summary
- `cd work2_coding; python scripts/build_artifacts.py --run-dir <temp-run-dir> --output-root <temp> --allow-incomplete` -> wrote JSON/CSV, tables, figure status files, and sidecars
- `cd work2_coding; python scripts/build_artifacts.py --study smoke_robust_menu --study-output-root <temp> --output-root <temp> --allow-incomplete` -> passed latest-run study lookup
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`

## Must-Have Review

- Normalized rows and summaries distinguish `completed`, `contract_only`, `diagnostic`, `incomplete`, and `blocked`; completed placeholder rows are rejected.
- Pilot/formal missing checkpoints produce blocker metadata and cannot become claim-ready artifacts.
- Contract-only smoke rows can feed incomplete/diagnostic artifacts but remain visibly non-claim-ready.
- `no_filter_diagnostic` remains labeled diagnostic and is excluded from recommended-policy ranking.
- Every generated aggregate/table/ranking/figure-status artifact has adjacent metadata or top-level status provenance.
- Lightweight artifacts are mirrored under `artifacts/work2_robust_menu/`; raw run outputs remain under ignored `work2_coding/outputs/`.

## Current Artifact Status

- `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` -> `artifact_status.status = blocked`
- `artifacts/work2_robust_menu/ARTIFACT_STATUS.json` -> mirrored blocked status
- Pilot blocker: missing `outputs/shared_training/work2_robust_menu/pilot/supervised_ml.pt`
- Formal blocker: formal evidence skipped for this Phase 4 run
- `pilot_claim_ready = false`
- `formal_claim_ready = false`

## Boundaries

Phase 4 does not provide claim-ready formal evidence yet. It provides the artifact pipeline and an honest blocked bundle. Phase 5 may use the status report for restrained manuscript framing, but any stronger empirical claim requires supplying the required checkpoint and rerunning Phase 4 to produce non-placeholder, claim-ready pilot/formal rows.

## Residual Risks

- The current artifact bundle records a dirty git state because generated artifacts were created before the final documentation and artifact commits. This is visible in provenance and does not make the bundle claim-ready.
- Actual simulator replay remains blocked by missing checkpoint prerequisites. The implementation intentionally refuses random-weight evidence for pilot/formal comparisons.

