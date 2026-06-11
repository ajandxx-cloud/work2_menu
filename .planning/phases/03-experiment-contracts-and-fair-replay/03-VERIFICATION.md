---
phase: 03-experiment-contracts-and-fair-replay
status: passed
verified: 2026-06-11
requirements:
  - EXP-01
  - EXP-02
  - EXP-03
  - EXP-04
---

# Phase 03 Verification: Experiment Contracts And Fair Replay

## Result

Status: passed

Phase 3 achieved its goal: the project now has runnable smoke/pilot/formal study contracts, required baseline policy declarations, paired replay validation, normalized row schema helpers, uptake-regime contracts, and a public smoke command that emits normalized rows without generating paper artifacts.

## Requirement Traceability

| Requirement | Status | Evidence |
|-------------|--------|----------|
| EXP-01 | passed | `work2_coding/Experiments/studies/{smoke,pilot,formal}_robust_menu.yaml`, `work2_coding/Experiments/suites/work2_robust_menu.yaml`, and `scripts/run_study.py` define and validate study/suite contracts. |
| EXP-02 | passed | `Src/policy_adapters.py` and manifest policies cover full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, no-filter diagnostic, robust risk-adjusted, robust service-guarded, and optional random top-k. |
| EXP-03 | passed | `Src/paired_replay.py` enforces paired fields, trace IDs, manifest/settings hashes, checkpoint metadata, and row provenance. |
| EXP-04 | passed | Pilot/formal manifests declare low and medium uptake regimes; smoke declares a medium behaviorally live contract regime and rows carry `uptake_regime`. |

## Automated Checks

- `cd work2_coding; python scripts/test_experiment_contracts.py` -> `PASS: 12 experiment contract tests`
- `cd work2_coding; python scripts/test_paired_replay_contract.py` -> `PASS: 10 paired replay contract tests`
- `cd work2_coding; python scripts/test_policy_fairness_contract.py` -> `PASS: 10 policy fairness contract tests`
- `cd work2_coding; python scripts/test_smoke_study_rows.py` -> `PASS: 9 smoke study row tests`
- `cd work2_coding; python -c "import sys; sys.path.insert(0,'.'); from Src.experiment_contracts import load_manifest, validate_manifest; m=load_manifest('smoke_robust_menu'); validate_manifest(m); print('SMOKE_MANIFEST_OK')"` -> `SMOKE_MANIFEST_OK`
- `cd work2_coding; python scripts/run_study.py --study smoke_robust_menu --contract-only` -> wrote `manifest_snapshot.yaml`, `study_summary.json`, `normalized_rows.json`, and `normalized_rows.csv` under `work2_coding/outputs/studies/smoke_robust_menu/...`
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `cd work2_coding; python -m py_compile Src/experiment_contracts.py Src/paired_replay.py Src/policy_adapters.py scripts/run_study.py scripts/test_experiment_contracts.py scripts/test_paired_replay_contract.py scripts/test_policy_fairness_contract.py scripts/test_smoke_study_rows.py` -> passed
- `Test-Path ooh_code` -> `False`

## Must-Have Review

- Smoke, pilot, and formal study contracts exist and validate policy names, seeds, split IDs, menu sizes, filter modes, checkpoint requirements, HGS parameters, and row schema fields.
- Baselines are represented through explicit policy adapters and manifest tags.
- Paired replay fairness compares resolved parser settings and rejects drift in checkpoint, HGS, seed, pricing, candidate, and behavior fields.
- Normalized rows include study/run IDs, policy tag, seed, split ID, trace ID/hash, checkpoint fields, manifest/settings hashes, run mode, menu settings, filter/effective policy, solver diagnostics fields, opt-out/acceptance fields, and placeholder status.
- No-filter is labeled diagnostic in adapter metadata, manifest metadata, and smoke rows.
- Formal placeholder rows are rejected by schema/runner tests.

## Boundaries

Phase 3 does not produce formal paper evidence. The public smoke runner currently emits `contract_only` rows with `placeholder_only: true` for smoke-scale contract verification. Phase 4 should execute pilot/formal evidence and replace placeholder runtime metrics with actual simulator results before artifact tables/figures support manuscript claims.

## Residual Risks

- Study manifests are committed under `work2_coding/Experiments/...` because the existing Windows ignore rule treats `Experiments/` and `experiments/` case-insensitively. `experiment_contracts.py` resolves both lowercase and uppercase directories.
- Actual simulator replay remains Phase 4 work. The Phase 3 row schema and public runner are ready for it, but pilot/formal checkpoint files must exist before formal execution can pass.

