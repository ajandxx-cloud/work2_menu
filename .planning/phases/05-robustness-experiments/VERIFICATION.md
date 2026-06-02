---
status: gaps_found
phase: 05-robustness-experiments
updated: 2026-06-02T20:59:12Z
score: 6/10 must-haves verified
overrides_applied: 0
---

# Phase 5 Verification Report

## Phase

- **Phase:** Phase 5 - Robustness Experiments
- **Verified:** 2026-06-02T20:59:12Z
- **Status:** BLOCKED / GAPS FOUND
- **Verifier:** Codex
- **Phase Goal:** Run or resume the Work2 robustness suite, build Work2-standard artifacts, and decide whether Phase 6 can make positive, conditional, or diagnostic-only claims.

## Goal Achievement

Phase 5 completed the robustness manifest and artifact contract, but did not complete actual robustness study rows. A full-suite run was attempted and stopped after runtime exceeded the practical execution window without producing a member `study_summary.json`.

**Result:** The phase is not passed. It is ready for a remediation/runtime pass, not for Phase 6 positive claims.

## Changed Files

```text
ooh_code/experiments/suites/work2_robustness.yaml
ooh_code/experiments/studies/work2_menu_size_robustness.yaml
ooh_code/experiments/studies/work2_candidate_pool_robustness.yaml
ooh_code/experiments/studies/work2_demand_robustness.yaml
ooh_code/experiments/studies/work2_outside_option_robustness.yaml
ooh_code/experiments/studies/work2_cross_instance_robustness.yaml
ooh_code/scripts/test_work2_robustness_manifests.py
ooh_code/scripts/build_artifacts.py
ooh_code/scripts/test_work2_robustness_artifacts.py
artifacts/work2_cnn_setmenunet/results_snapshot/work2_robustness_rows.csv
artifacts/work2_cnn_setmenunet/work2_robustness_summary.md
artifacts/work2_cnn_setmenunet/tables/work2_robustness_by_dimension.tex
artifacts/work2_cnn_setmenunet/figures/work2_robustness_net_profit.png
artifacts/work2_cnn_setmenunet/diagnostics/work2_robustness_diagnostic.md
.planning/phases/05-robustness-experiments/05-01-SUMMARY.md
.planning/phases/05-robustness-experiments/05-02-SUMMARY.md
.planning/phases/05-robustness-experiments/05-03-SUMMARY.md
.planning/phases/05-robustness-experiments/VERIFICATION.md
```

## Work 1 Impact

- **Pricing module changed?** No.
- **MNL choice model changed?** No core choice implementation was changed.
- **HGS/Hygese route-cost evaluation changed?** No.
- **Note:** Experiment manifests include Work2 MNL/ETA run-level parameters, but no Work 1 pricing, MNL choice, or HGS/Hygese route-cost core files were edited by this phase.

## Smoke Test

- **Smoke test command:** `python scripts/test_work2_robustness_manifests.py`
- **Smoke test result:** PASS
- **Additional artifact gate:** `python scripts/test_work2_robustness_artifacts.py` PASS

## Expected CSV

- **Expected CSV generated?** Yes, but header-only because no member study completed.
- **CSV path:** `artifacts/work2_cnn_setmenunet/results_snapshot/work2_robustness_rows.csv`
- **Schema checked?** Yes.
- **Missing required columns:** None.
- **Rows:** 0.

## EXP-07 Dimension Coverage

| Dimension | Manifest Coverage | Artifact Status | Actual Rows | Verification |
|---|---|---|---:|---|
| Menu size | `work2_menu_size_robustness`, includes `L=3` plus non-default values | Not run | 0 | GAP |
| Candidate pool size | `work2_candidate_pool_robustness`, includes `K=10` plus non-default values | Not run | 0 | GAP |
| Demand intensity | `work2_demand_robustness`, includes low/default/high `max_steps_r` | Not run | 0 | GAP |
| Outside option utility | `work2_outside_option_robustness`, includes `outside_option_util=0.0` plus non-default values | Not run | 0 | GAP |
| Cross-instance generalization | `work2_cross_instance_robustness`, uses Austin non-RC instance | Not run | 0 | GAP |

## Run Attempt

```text
python scripts/run_study.py --study work2_robustness --resume_latest
```

Observed partial trace:

```text
ooh_code/outputs/studies/work2_robustness/20260602T205054Z_cdf96a15/manifest_snapshot.yaml
ooh_code/outputs/studies/work2_menu_size_robustness/20260602T205054Z_842858e1/manifest_snapshot.yaml
ooh_code/outputs/shared_training/work2_menu_size_robustnessseed0_842858e1/0/checkpoints/supervised_ml.pt
ooh_code/outputs/shared_training/work2_menu_size_robustnessseed0_842858e1/0/checkpoints/cnn_aux.pt
```

No `study_summary.json`, split summary, or normalized rows were produced before the run was stopped for runtime control.

## Paper Conclusion Support

- **Does current result support CNN-SetMenuNet net profit claim?** No / not evaluated.
- **Does current result support lower menu regret?** No / not evaluated.
- **Does current result support higher Top-L overlap?** No / not evaluated.
- **Does current result avoid worsening quit rate and avg walking distance?** Inconclusive / not evaluated.
- **Phase 6 posture:** Diagnostic-only or remediation loop. Do not make positive or conditional robustness claims until member studies produce rows.

## Risks And Diagnostics

- Full-suite runtime is too high for the current inline execution pass.
- Current robustness artifacts correctly label all five dimensions as `Not run`.
- Diagnostic report: `artifacts/work2_cnn_setmenunet/diagnostics/work2_robustness_diagnostic.md`
- Required next retry step: run member studies individually in priority order, starting with `work2_menu_size_robustness`, and let each member reach `study_summary.json` before rebuilding artifacts.

## Next Phase Readiness

- **Can next phase proceed?** No, not as formal Phase 6 evidence.
- **Required before next phase:** Complete at least the required Phase 5 member runs or explicitly re-plan Phase 5 with smaller budgets/member roster. Then rerun:

```text
python scripts/build_artifacts.py --study work2_robustness
```

## Evidence

```text
python scripts/test_work2_robustness_manifests.py
PASS work2 robustness manifests: suite + five EXP-07 studies, K=10, L=3, outside-option 0.0, Austin cross-instance, 80/20 pilot.

python scripts/test_work2_robustness_artifacts.py
PASS: 7 Work2 robustness artifact tests

python scripts/build_artifacts.py --study work2_robustness
Built artifacts for: work2_robustness

CSV schema check
rows 0
missing []
columns 25
```

---

_Verified: 2026-06-02T20:59:12Z_
_Verifier: Codex_
