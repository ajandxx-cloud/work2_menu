---
status: passed
phase: 04-model-comparison-suite
updated: 2026-06-02
---

# Phase 4 Verification Report

## Phase

- **Phase:** Phase 4 - Model Comparison Suite
- **Date:** 2026-06-02
- **Status:** PASS WITH RISKS
- **Verifier:** Codex

## Changed Files

```text
ooh_code/experiments/studies/work2_main.yaml
ooh_code/scripts/test_work2_main_manifest.py
ooh_code/docs/WORK2_EXPERIMENT_PROTOCOL.md
ooh_code/scripts/build_artifacts.py
ooh_code/scripts/test_work2_artifact_summary.py
artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv
artifacts/work2_cnn_setmenunet/work2_main_summary.md
artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md
artifacts/work2_cnn_setmenunet/tables/work2_main_prediction_accuracy.tex
artifacts/work2_cnn_setmenunet/tables/work2_main_operational.tex
artifacts/work2_cnn_setmenunet/tables/work2_main_menu_regret.tex
artifacts/work2_cnn_setmenunet/figures/work2_main_net_profit.png
.planning/phases/04-model-comparison-suite/04-01-SUMMARY.md
.planning/phases/04-model-comparison-suite/04-02-SUMMARY.md
.planning/phases/04-model-comparison-suite/04-03-SUMMARY.md
.planning/phases/04-model-comparison-suite/VERIFICATION.md
```

Generated raw outputs are intentionally left under ignored study-output directories:

```text
ooh_code/outputs/studies/work2_main/20260602T042600Z_41f91b9d/
ooh_code/outputs/shared_training/work2_mainseed0_41f91b9d/
ooh_code/outputs/shared_training/work2_mainseed1_41f91b9d/
ooh_code/outputs/shared_training/work2_mainseed2_41f91b9d/
```

## Work 1 Impact

- **Pricing module changed?** No
- **MNL choice model changed?** No
- **HGS/Hygese route-cost evaluation changed?** No
- **Notes:** Phase 4 uses existing pricing, passenger-choice, and route-cost evaluation paths. It changes the Work 2 manifest, reporting logic, tests, and generated artifacts only.

## Smoke Test

- **Smoke test command:** `python scripts/run_study.py --study smoke_work2_main --resume_latest`
- **Smoke test result:** PASS
- **Manifest contract command:** `python scripts/test_work2_main_manifest.py`
- **Manifest contract result:** PASS
- **Artifact summary command:** `python scripts/test_work2_artifact_summary.py`
- **Artifact summary result:** PASS, 7 Work2 gate/diagnostic tests passed

## Full Pilot Run

- **Pilot command:** `python -u scripts/run_study.py --study work2_main --resume_run_id 20260602T042600Z_41f91b9d`
- **Pilot result:** PASS
- **Study status:** `completed`
- **Completed splits:** `3/3`
- **Splits:** `seed0`, `seed1`, `seed2`
- **Variants:** 7 total; the standard CSV keeps the six configured core methods.
- **Pilot budget:** `80` training episodes and `20` test episodes per seed. This does not consume or rewrite the later formal `150-300/50` default.

## Expected CSV

- **Expected CSV generated?** Yes
- **CSV path:** `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv`
- **Schema checked?** Yes
- **Missing required columns:** None
- **Rows checked:** 18 rows = 3 seeds x 6 core methods
- **Core methods checked:** `Nearest-L`, `Cost-L heuristic`, `CNN-Menu`, `MLP-Menu`, `CNN-SetMenuNet`, `Oracle Menu`
- **Contract columns checked:** `K=10`, `L=3`, `candidate_pool_size=10`, `displayed_meeting_points=3`, `home_always_shown=True`

## Paper Conclusion Support

Answer based only on generated evidence.

- **Does current result support CNN-SetMenuNet net profit claim?** No
- **Does current result support lower menu regret?** Mixed
- **Does current result support higher Top-L overlap?** Inconclusive
- **Does current result avoid worsening quit rate and avg walking distance?** Mixed

Evidence summary from `artifacts/work2_cnn_setmenunet/work2_main_summary.md`:

- Conclusion gate: Mixed/inconclusive pilot evidence.
- CNN-SetMenuNet net profit mean: `-5093.849`.
- CNN-SetMenuNet did not beat Cost-L heuristic, CNN-Menu, MLP-Menu, or Nearest-L on mean net profit in this pilot.
- CNN-SetMenuNet menu regret (`24.566`) is close to Cost-L (`24.617`) and CNN-Menu (`24.936`) but not lower than Nearest-L (`19.848`).
- Top-L overlap is `1.000` for all six core methods, so it does not distinguish the methods in this pilot.
- CNN-SetMenuNet quit rate (`0.380`) is slightly worse than Cost-L (`0.352`) and CNN-Menu (`0.355`) but similar to Oracle Menu (`0.377`); average walk (`2235.166`) is better than Cost-L/CNN-Menu but worse than Nearest-L.

## Risks And Diagnostics

- Phase 4 produced interpretable pilot evidence, but the result is mixed/inconclusive rather than supportive of the expected CNN-SetMenuNet net-profit claim.
- MLP-Menu is behaviorally degenerate in this pilot (`quit_rate` near 1.0 and very large menu regret in aggregate), so its strong net-profit value should be treated as a diagnostic signal rather than paper-ready dominance evidence.
- The diagnostic report points to cost-prediction and realized route-cost / pricing interactions as follow-up areas.
- Existing workspace planning/state files had pre-existing unrelated dirty diffs before Phase 4 execution; Phase 4 commits intentionally avoided staging unrelated planning migrations.

Diagnostic report:

```text
artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md
```

## Next Phase Readiness

- **Can next phase proceed?** Yes with risks
- **Required before next phase:** Treat Phase 5 as robustness plus remediation. Do not make a positive paper claim from Phase 4 alone; use the diagnostic report to decide whether to tune prediction/ranking components, inspect MLP-Menu degeneracy, or carry mixed evidence forward with clear caveats.

## Evidence

```text
python scripts/test_work2_main_manifest.py
PASS work2_main manifest: 6 core methods, seed0..seed2, train/test split 0/1, K=10, L=3, 80/20 pilot.

python scripts/test_work2_artifact_summary.py
PASS: 7 Work2 artifact summary gate tests

python -u scripts/run_study.py --study work2_main --resume_run_id 20260602T042600Z_41f91b9d
Completed study: work2_main
Study run id: 20260602T042600Z_41f91b9d
Variants: 7

python scripts/build_artifacts.py --study work2_main
Built artifacts for: work2_main
```

Key outputs:

```text
artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv
artifacts/work2_cnn_setmenunet/work2_main_summary.md
artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md
artifacts/work2_cnn_setmenunet/tables/work2_main_prediction_accuracy.tex
artifacts/work2_cnn_setmenunet/tables/work2_main_operational.tex
artifacts/work2_cnn_setmenunet/tables/work2_main_menu_regret.tex
artifacts/work2_cnn_setmenunet/figures/work2_main_net_profit.png
```
