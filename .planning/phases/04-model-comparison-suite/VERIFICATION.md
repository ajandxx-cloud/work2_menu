---
status: passed
phase: 04-model-comparison-suite
updated: 2026-06-02T07:02:20Z
score: 10/10 must-haves verified
overrides_applied: 0
---

# Phase 4 Verification Report

## Phase

- **Phase:** Phase 4 - Model Comparison Suite
- **Verified:** 2026-06-02T07:02:20Z
- **Status:** PASS WITH RISKS
- **Verifier:** Codex
- **Phase Goal:** Run a pilot multi-seed model comparison and verify CNN-SetMenuNet against baselines on menu quality, operational performance, and passenger experience.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Phase 4 is a focused pilot, not an exhaustive baseline census. | VERIFIED | `04-CONTEXT.md` D-01/D-03 and `WORK2_EXPERIMENT_PROTOCOL.md` define the six core methods and mark Home only, Full-candidate CNN, and SetMenuNet as optional supplements. |
| 2 | Core methods are present: Nearest-L, Cost-L heuristic, CNN-Menu, MLP-Menu, CNN-SetMenuNet, Oracle Menu. | VERIFIED | `work2_main.yaml` contains exactly these six policy labels; `test_work2_main_manifest.py` enforces the roster. |
| 3 | Pilot uses three shared seeds with `80/20`, `K=10`, `L=3`, home always shown. | VERIFIED | `python scripts/test_work2_main_manifest.py` passed; CSV rows all have seeds `0,1,2`, `train_episodes=80`, `test_episodes=20`, `candidate_pool_size=10`, `displayed_meeting_points=3`, `home_always_shown=True`. |
| 4 | Core methods share split/trace/candidate contract. | VERIFIED | Raw `normalized_rows.json` has 21 rows = 3 splits x 7 variants including reference; each core row carries `split_id`, `train_split=0`, `test_split=1`, `candidate_pool_size=10`, `displayed_meeting_points=3`, `home_always_shown=True`. |
| 5 | Standard CSV has 18 rows = 3 seeds x 6 core methods. | VERIFIED | Independent CSV check returned `rows 18`, methods `CNN-Menu`, `CNN-SetMenuNet`, `Cost-L heuristic`, `MLP-Menu`, `Nearest-L`, `Oracle Menu`, seeds `0,1,2`. |
| 6 | CSV rows trace to actual raw pilot output, not edited-away evidence. | VERIFIED | Read-only comparison against raw `ooh_code/outputs/studies/work2_main/20260602T042600Z_41f91b9d/normalized_rows.json` found 18 raw core rows, no missing rows, and 0 mismatches across key metrics. |
| 7 | Outputs include prediction/ranking, operational, and passenger-experience metrics. | VERIFIED | CSV includes `menu_regret`, `top_L_overlap`, `spearman_cost_ranking`, `net_profit`, `total_cost`, `runtime_per_decision`, `quit_rate`, `avg_walk`; root tables exist for prediction accuracy, operational, and menu regret. |
| 8 | Summary honestly evaluates support for paper conclusions. | VERIFIED | `work2_main_summary.md` states mixed/inconclusive pilot evidence; it reports CNN-SetMenuNet does not improve mean `net_profit` versus Cost-L or learned baselines, Top-L overlap is non-discriminating, and guardrails are mixed. |
| 9 | Mixed/inconclusive evidence produces diagnostics. | VERIFIED | `diagnostics/work2_main_diagnostic.md` exists and covers cost prediction error, ranking/menu selection error, training budget, and seed instability. |
| 10 | Phase 5 readiness is conditional with risks/remediation. | VERIFIED | Summary and verification both state Phase 5 can proceed only with risks/remediation; no positive robustness or paper claim is made from Phase 4 alone. |

**Score:** 10/10 truths verified

## Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `ooh_code/experiments/studies/work2_main.yaml` | Six-method pilot manifest | VERIFIED | Enforced by manifest test; includes MLP-Menu and separates pilot `80/20` from formal `150-300/50` later-phase scope. |
| `ooh_code/scripts/test_work2_main_manifest.py` | Fast manifest contract check | VERIFIED | `python scripts/test_work2_main_manifest.py`: PASS. |
| `ooh_code/scripts/build_artifacts.py` | Work2 standard artifact builder and graded gate | VERIFIED | Contains Phase 4 core method list, evidence classifier, diagnostic writer, standard CSV writer, summary writer, and table/figure generation. |
| `ooh_code/scripts/test_work2_artifact_summary.py` | Gate and diagnostic tests | VERIFIED | `python scripts/test_work2_artifact_summary.py`: PASS, 7 tests. |
| `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv` | Standard core-method CSV | VERIFIED | 18 rows = 3 seeds x 6 core methods; key metrics match raw normalized rows. |
| `artifacts/work2_cnn_setmenunet/work2_main_summary.md` | Honest Phase 4 pilot summary | VERIFIED | Contains settings, core methods, aggregate means, seed variation, method explanations, conclusion support, caveats, and Phase 5 readiness. |
| `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md` | Diagnostic report for mixed evidence | VERIFIED | Contains the four required diagnostic sections and a remedial next-step recommendation. |
| `artifacts/work2_cnn_setmenunet/tables/*.tex` and `figures/work2_main_net_profit.png` | Paper-facing tables/figure | VERIFIED | Three root-standard table files exist; net-profit figure exists and is non-empty (`62043` bytes). |

## Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| Plan 01 manifest | Plan 02 reporting | Method tags and pilot defaults | WIRED | `build_artifacts.py` maps manifest variant tags to standard method labels and standard columns. |
| Plan 02 reporting | Plan 03 pilot artifacts | `build_work2_standard_artifacts()` | WIRED | Standard CSV/summary/diagnostic are generated from study summary rows and manifest metadata. |
| Raw pilot output | Standard CSV | `normalized_rows.json` -> `work2_main_rows.csv` | WIRED | Independent comparison found 0 mismatches for key metrics across the 18 core rows. |
| Summary | Diagnostic | Diagnostic path in mixed evidence state | WIRED | Summary links `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md`; diagnostic exists. |

## Data-Flow Trace

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| `work2_main_rows.csv` | Per-seed core method metrics | Raw `normalized_rows.json` from run `20260602T042600Z_41f91b9d` | Yes | VERIFIED |
| `work2_main_summary.md` | Aggregate means and conclusion gate | Standard CSV rows passed to `classify_work2_pilot_evidence()` | Yes | VERIFIED |
| `work2_main_diagnostic.md` | Diagnostic metrics | Standard rows plus source rows | Yes | VERIFIED |

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Manifest contract is guarded | `python scripts/test_work2_main_manifest.py` from `ooh_code/` | PASS work2_main manifest: 6 core methods, seed0..seed2, K=10, L=3, 80/20 pilot. | PASS |
| Evidence gate tests pass | `python scripts/test_work2_artifact_summary.py` from `ooh_code/` | PASS: 7 Work2 artifact summary gate tests | PASS |
| CSV shape and contract fields are correct | Read-only Python CSV check | `rows 18`; expected methods/seeds; contract fields all true | PASS |
| CSV matches raw normalized rows | Read-only Python comparison | `raw_core_rows 18`; `mismatches 0`; status PASS | PASS |

## Work 1 Impact

- **Pricing module changed?** No Phase 4 commit changed Work 1 pricing implementation files.
- **MNL choice model changed?** No Phase 4 commit changed the passenger choice implementation. However, `work2_main.yaml` did add/record run-level MNL/ETA calibration parameters for this Work 2 pilot. This is experiment configuration, not a rewrite of MNL core logic.
- **HGS/Hygese route-cost evaluation changed?** No Phase 4 commit changed HGS/Hygese implementation files or route-cost core logic.
- **Commit-scope evidence:** `git diff --name-only 2aa221c..HEAD` for Phase 4 includes only Phase 4 planning summaries, Work2 artifacts, `WORK2_EXPERIMENT_PROTOCOL.md`, `work2_main.yaml`, `build_artifacts.py`, and two Work2 test scripts. It does not include `ooh_code/Src/Algorithms/DSPO.py`, `DSPO_Menu.py`, `Src/Utils/Utils.py`, or HGS/Hygese core files.
- **Dirty worktree note:** The current workspace has unrelated dirty changes in several `ooh_code/Src` files. Those are not part of the Phase 4 committed range and were not modified by this verifier.

## Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| EXP-02 | VERIFIED WITH DOCUMENTED SCOPE | ROADMAP's wider baseline list is narrowed by Phase 4 context to six core methods plus optional non-blocking supplements; all six core methods ran. |
| EXP-03 | VERIFIED FOR PILOT | Three seeds `0,1,2` are represented. Formal five-seed default remains later-phase scope. |
| EXP-04 | VERIFIED | `instance=RC`, `K=10`, `L=3` in manifest and CSV. |
| EXP-05 | VERIFIED | Pilot train/test episodes are `80/20`. |
| EXP-06 | VERIFIED AS PRESERVED FUTURE SCOPE | Manifest and summary state formal `150-300/50` evidence remains later-phase scope; Phase 4 did not consume or rewrite it. |
| OUT-02 | VERIFIED | `work2_main_summary.md` summarizes settings, metrics, major results, conclusion support, caveats, risks, and Phase 5 readiness. |
| OUT-03 | VERIFIED | Prediction/ranking metrics are present in CSV/tables/diagnostic: Spearman, Top-L overlap, NDCG@L in raw diagnostic source, menu regret, cost MAE/RMSE in diagnostic. |
| OUT-04 | VERIFIED | Operational metrics include net profit, total cost, runtime per decision, plus table outputs. |
| OUT-05 | VERIFIED | Passenger metrics include quit rate, acceptance-related raw output, meeting-point/home pickup shares in raw output, average walk, in-vehicle time, and price/discount metrics in raw output/table path. |

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `ooh_code/scripts/build_artifacts.py` | 67 | `render_placeholder_figure` helper | INFO | Existing fallback behavior for empty artifact data; not used as a Phase 4 success substitute because actual tables/figure and real CSV exist. |
| `ooh_code/scripts/build_artifacts.py` | 153/338/360/984/2315 | Empty-list returns | INFO | Guard clauses/fallbacks, not user-visible stubs for Phase 4 artifacts. |

## Gaps Summary

No blocker gaps found. The phase goal is achieved as an interpretable pilot pipeline with mixed/inconclusive evidence. Phase 5 should proceed only as robustness plus remediation/diagnosis, not as validation of a positive CNN-SetMenuNet paper claim.

---

_Verified: 2026-06-02T07:02:20Z_
_Verifier: Codex (gsd-verifier)_
