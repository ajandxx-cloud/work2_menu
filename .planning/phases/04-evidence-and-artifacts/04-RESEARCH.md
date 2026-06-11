# Phase 04 Research: Evidence And Artifacts

## RESEARCH COMPLETE

## Scope

Phase 4 must turn the Phase 3 study contracts into evidence artifacts without weakening the project guardrails. The active runtime remains `work2_coding/`; the historical `.planning/codebase/` references to `ooh_code/` are stale architectural memory and must not drive file paths.

## Current Runtime Findings

- `work2_coding/scripts/run_study.py` currently emits contract-only rows for smoke and pilot-style studies. It writes `manifest_snapshot.yaml`, `study_summary.json`, `normalized_rows.json`, and `normalized_rows.csv`.
- `run_study.py` rejects formal contract-only rows, which is correct: formal placeholder evidence cannot support claims.
- `work2_coding/Src/paired_replay.py` already defines the normalized-row schema, trace/settings hashes, checkpoint metadata fields, placeholder guards, and row validation.
- `work2_coding/Src/experiment_contracts.py` validates smoke, pilot, and formal study manifests, including checkpoint contracts and uptake regimes.
- `work2_coding/Src/policy_adapters.py` keeps no-filter labeled as diagnostic and prevents policy adapters from mutating paired replay fields.
- Phase 3 tests use script-style direct execution from `work2_coding/scripts/`, which should remain the Phase 4 testing pattern.

## Recommended Architecture

Build Phase 4 as a narrow evidence pipeline around the existing Phase 3 public runner:

1. Extend the study runner to produce non-placeholder smoke/pilot rows when actual execution is available, and explicit `incomplete` or `blocked` status when checkpoint/runtime prerequisites are missing.
2. Add artifact helpers that load normalized rows and produce aggregate JSON/CSV, LaTeX tables, PNG figures, and artifact status/provenance sidecars.
3. Keep raw runs under `work2_coding/outputs/`, lightweight artifacts under `work2_coding/artifacts/`, and mirror review-ready artifacts to `artifacts/work2_robust_menu/`.
4. Add gates that prevent `placeholder_only=True`, invalid checkpoint status, missing formal dependency snapshots, or unlabeled `no_filter_diagnostic` rows from becoming claim-ready artifacts.
5. Generate a blocker/status report when formal evidence is unavailable rather than silently producing formal-looking figures.

## Key Implementation Risks

- Pilot/formal manifests require checkpoint provenance. If the expected checkpoint is absent, the runner or artifact builder must mark evidence `incomplete` or `blocked`; it must not fall back to random weights for claim-ready rows.
- `contract_only` rows are useful diagnostics but must only feed placeholder/incomplete reports.
- `no_filter_diagnostic` may appear in result tables/figures as a diagnostic upper bound, but not in recommended-policy ranking.
- The artifact builder must not hand-edit generated rows or paper artifacts. It should consume row files and write derived artifacts deterministically.
- Figure generation should use `matplotlib`, already in the inherited dependency set, and must degrade cleanly if optional plotting dependencies are unavailable.
- A dirty git worktree is allowed, but provenance must record commit and dirty-state markers explicitly.

## Plan Shape

- Plan 01: make runner output and row status honest for real-or-blocked pilot evidence.
- Plan 02: build aggregate tables and reviewer-facing figures from normalized rows.
- Plan 03: add provenance sidecars and artifact gates for placeholders, checkpoints, diagnostics, environment, and git status.
- Plan 04: run the pilot/artifact pipeline, mirror lightweight artifacts, and write verification-ready blocker/status reports.

## Suggested Verification

- `cd work2_coding; python scripts/test_experiment_contracts.py`
- `cd work2_coding; python scripts/test_paired_replay_contract.py`
- `cd work2_coding; python scripts/test_policy_fairness_contract.py`
- `cd work2_coding; python scripts/test_smoke_study_rows.py`
- `cd work2_coding; python scripts/test_artifact_builder.py`
- `cd work2_coding; python scripts/test_artifact_gates.py`
- `cd work2_coding; python scripts/run_study.py --study smoke_robust_menu --contract-only`
- `cd work2_coding; python scripts/build_artifacts.py --study smoke_robust_menu --allow-incomplete`
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`

