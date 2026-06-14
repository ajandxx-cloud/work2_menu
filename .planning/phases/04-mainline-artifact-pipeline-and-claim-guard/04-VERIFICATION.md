---
phase: 4
phase_name: Mainline Artifact Pipeline And Claim Guard
status: passed
verified: 2026-06-14
runtime_root: work2_coding
smoke_output: work2_coding/outputs/phase4_verification/smoke_robust_menu/smoke_robust_menu-20260614T021107Z-759dc2ce
artifact_output: work2_coding/outputs/phase4_artifacts
---

# Phase 4 Verification

## Result

Phase 4 passed. The artifact and claim pipeline now consumes normalized-row-v2
mainline outputs from the seven-tag Work2 V1 family, emits mainline-aware
artifact bundles, and generates manuscript-frame claim guards without editing
manuscript source or generated result rows by hand.

## Commands Run

All commands were run from `work2_coding/`.

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_artifact_gates.py
python scripts/test_smoke_study_rows.py
python scripts/test_experiment_contracts.py
python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase4_verification
python scripts/build_artifacts.py --run-dir outputs/phase4_verification/smoke_robust_menu/smoke_robust_menu-20260614T021107Z-759dc2ce --output-root outputs/phase4_artifacts --allow-incomplete
python scripts/build_manuscript_frame.py --artifact-root outputs/phase4_artifacts
```

## Automated Results

- Import smoke: passed (`IMPORT_OK`)
- Artifact gate tests: passed, 13 tests
- Smoke study row tests: passed, 9 tests
- Experiment contract tests: passed, 15 tests
- Actual smoke replay: completed
- Artifact build: completed
- Manuscript frame build: completed

## Smoke Replay Output

Output directory:

```text
work2_coding/outputs/phase4_verification/smoke_robust_menu/smoke_robust_menu-20260614T021107Z-759dc2ce
```

Observed:

- `row_count`: 28
- `status` values: `completed`
- `execution_status` row values: `completed`
- `checkpoint_load_status` values: `not_requested`
- `policy_tag` coverage: all seven mainline tags
- `menu_k` coverage: `{1, 2, 3, 5}`

## Artifact Output

Artifact output directory:

```text
work2_coding/outputs/phase4_artifacts
```

Observed:

- `ARTIFACT_STATUS.json` exists.
- `artifact_status.status`: `diagnostic`
- `claim_ready`: `false`
- reason: `smoke artifacts are diagnostic/status evidence only`
- `recommended_policy_ranking.json` excludes `mainline_no_menu`.
- `baseline_boundary_policies.json` includes `mainline_no_menu`.
- Manuscript-frame files exist under `manuscript/`:
  - `method_outline.md`
  - `experiment_outline.md`
  - `result_outline.md`
  - `claim_checklist.md`
  - `CLAIM_GUARD.json`
- `CLAIM_GUARD.json` has `artifact_status="diagnostic"` and
  `claim_ready=false`.

## Scope Guardrails

- No manuscript source was edited.
- No generated result row was hand-edited.
- Formal replay was not executed.
- Formal checkpoint training was not executed.
- Smoke artifacts remain diagnostic/status evidence and do not unlock empirical
  superiority or formal ranking claims.

## Phase 5 Handoff

- Prepare formal evidence readiness: checkpoint provenance, dependency snapshot,
  formal replay prerequisites, and stricter claim-ready formal gates.
- Keep generated artifact and claim-guard paths as the source for any manuscript
  framing work.
- Continue excluding diagnostic, failed, blocked, placeholder-only,
  no-filter-only, contract-only, incomplete, and bad-checkpoint rows from
  formal claims.
