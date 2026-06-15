---
status: diagnostic_provisional_blocked
phase: 04-rc-result-diagnosis-and-paper-claim-validation
source_run: work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a
run_id: formal_robust_menu-20260614T032323Z-c672286a
row_count: 35
split_count: 5
policy_count: 7
claim_ready: false
created: 2026-06-15T14:20:00+08:00
timezone: Asia/Shanghai
---

# RC Formal Diagnosis And Paper-Claim Validation

## 1. Executive Status

The selected formal RC run is complete and comparable for diagnosis:

- `35` completed rows.
- `5` paired formal splits.
- `7` mainline policy tags per split.
- uptake regimes: `low`, `medium`.
- checkpoint load status: `loaded`.
- placeholder rows: `false`.

This evidence is not claim-ready for manuscript superiority language. Formal
readiness is blocked by dirty git, artifact status is blocked, and
`CLAIM_GUARD.json` keeps empirical superiority and formal ranking claims
unavailable. All empirical classifications below are provisional diagnostic
classifications until provenance and artifact gates are rerun and pass.

Older smoke artifacts and smoke claim guards are not used as Phase 4 claim
evidence.

## 2. Blockers And Provenance

| Gate | Status | Claim Effect |
| --- | --- | --- |
| Formal rows | `completed`, `35` rows | Usable for diagnosis |
| Formal readiness | `blocked` | Blocks claim-ready use |
| Readiness blocker | `dirty_git` | Blocks final formal claim classification |
| Artifact status | `blocked` | Blocks claim-ready tables/figures |
| Artifact reasons | missing `outside_option_util`; missing valid `method_family` | Blocks pilot/formal claim-ready artifacts |
| Claim guard | `claim_ready: false`, `formal_claim_ready: false` | Allows diagnostic/status tables only |
| Checkpoint | `loaded`, SHA-256 `d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4` | Satisfies diagnostic checkpoint provenance |

Source artifacts:

- Formal rows:
  `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json`
- Formal readiness:
  `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
- Artifact status:
  `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json`
- Claim guard:
  `work2_coding/outputs/phase3_formal_artifacts/manuscript/CLAIM_GUARD.json`
- Phase 4 generated diagnostics:
  `.planning/results/RC_FORMAL_DIAGNOSTIC_TABLES.md`
  `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv`
  `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv`

## 3. Formal Result Diagnostics

Confidence intervals and strong statistical language are intentionally omitted:
there are only five paired formal splits. The primary view is paired
split-level direction and magnitude.

### 3.1 Policy-Level Means

| Policy | Net Profit | Acceptance | Served | Opt-out | Home Share | Meeting-Point Uptake |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `mainline_no_menu` | -192582.600000 | 0.524051 | 0.524051 | 0.475949 | 0.524051 | 0.000000 |
| `mainline_fixed_menu` | -182538.276401 | 0.530541 | 0.530541 | 0.469459 | 0.466322 | 0.064219 |
| `mainline_random_menu` | -176651.519334 | 0.517462 | 0.517462 | 0.482538 | 0.452100 | 0.065362 |
| `mainline_optimized_m` | -190803.240000 | 0.525000 | 0.525000 | 0.475000 | 0.482496 | 0.042504 |
| `mainline_optimized_mw` | -184672.560000 | 0.512758 | 0.512758 | 0.487242 | 0.494773 | 0.017985 |
| `mainline_optimized_fixed_window` | -180581.747301 | 0.555488 | 0.555488 | 0.444512 | 0.463208 | 0.092280 |
| `mainline_optimized_adaptive` | -180581.747301 | 0.555488 | 0.555488 | 0.444512 | 0.463208 | 0.092280 |

Interpretation:

- `mainline_optimized_adaptive` improves service-quality metrics relative to
  most baselines: higher acceptance/served rate, lower opt-out, and higher
  meeting-point uptake.
- It does not dominate profit-side metrics. `mainline_random_menu` has better
  mean net profit than adaptive, and adaptive loses to random on net profit in
  3 of 5 paired splits.
- Adaptive and optimized fixed-window rows are identical across tracked
  metrics. This blocks any incremental adaptive-window claim from the selected
  formal run.

### 3.2 Paired Split Direction Summary

| Comparison: adaptive vs baseline | Net Profit | Acceptance | Opt-out | Meeting-Point Uptake | Claim Signal |
| --- | --- | --- | --- | --- | --- |
| `mainline_no_menu` | 4 better / 1 worse | 4 better / 1 worse | 4 better / 1 worse | 5 better | Conditional positive versus no-menu |
| `mainline_fixed_menu` | 2 better / 3 worse | 4 better / 1 worse | 4 better / 1 worse | 5 better | Service positive, profit unstable |
| `mainline_random_menu` | 2 better / 3 worse | 5 better | 5 better | 5 better | Service positive, profit not dominant |
| `mainline_optimized_m` | 5 better | 3 better / 2 worse | 3 better / 2 worse | 5 better | Product-price bundle helps profit, service mixed |
| `mainline_optimized_mw` | 2 better / 3 worse | 5 better | 5 better | 5 better | Service positive, profit unstable |
| `mainline_optimized_fixed_window` | 5 ties | 5 ties | 5 ties | 5 ties | No adaptive-window increment shown |

Lower values are treated as better for cost, opt-out, and service-time metrics;
higher values are treated as better for profit, acceptance, served rate, and
meeting-point uptake.

### 3.3 Uptake-Regime Summary

Low uptake regime:

- Adaptive loses to random menu on net profit in both low-uptake splits.
- Adaptive improves acceptance, opt-out, and meeting-point uptake versus random
  in both low-uptake splits.
- Adaptive beats `mainline_optimized_m` on net profit in both low-uptake splits,
  but loses on acceptance and opt-out in both.

Medium uptake regime:

- Adaptive beats no-menu on net profit and service metrics in all three
  medium-uptake splits.
- Adaptive beats random menu on net profit in 2 of 3 medium-uptake splits and
  improves service metrics in all three.
- Adaptive still ties optimized fixed-window in all three medium-uptake splits.

Regime dependence downgrades any positive claim to conditional or diagnostic.

### 3.4 Product And Window Ablations

Product ablation:

- Versus `mainline_optimized_m`, adaptive improves net profit in 5 of 5 splits
  and meeting-point uptake in 5 of 5 splits, but service metrics are mixed
  across uptake regimes.
- Versus `mainline_optimized_mw`, adaptive improves service metrics in 5 of 5
  splits but loses net profit in 3 of 5 splits.
- The product-composition story is conditional: adding price/adaptive menu
  structure can improve service behavior and some profit comparisons, but it
  does not produce uniform profit dominance.

Window ablation:

- `mainline_optimized_adaptive` equals
  `mainline_optimized_fixed_window` on every tracked metric and every split in
  the selected formal run.
- The selected formal rows do not support a positive adaptive-window increment
  claim.

## 4. Claim Matrix

| Claim ID | Comparison | Required Metrics | Observed Evidence | Paired Direction | Uptake Caveat | Classification | Blocker Status | Allowed Manuscript Use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 central superiority | adaptive vs all six baselines | profit plus acceptance/served/opt-out/home/meeting-point uptake | service metrics often improve, but random menu has better mean net profit and adaptive loses to random on 3/5 profit splits; fixed-window ties exactly | mixed; not all-baseline positive | low uptake loses to random profit in 2/2 | unsupported as strong; at best conditional diagnostic | provenance-blocked and artifact-blocked | no positive superiority claim |
| C2 product ablation value | adaptive vs optimized `m` and `m+w` | profit, acceptance, opt-out, uptake | adaptive beats `m` on profit 5/5 and uptake 5/5; adaptive beats `m+w` on service 5/5 but loses profit 3/5 | mixed by ablation target | low and medium differ for `m` service metrics | conditional / weak-diagnostic | provenance-blocked | mechanism discussion only after gates pass; diagnostic wording now |
| C3 window ablation value | adaptive vs optimized fixed-window | profit and service metrics | all tracked metrics tie in all five splits | 5/5 ties | no regime difference because all ties | unsupported | provenance-blocked | no adaptive-window improvement claim |
| C4 menu construction value | adaptive vs no-menu, fixed-menu, random-menu | profit, acceptance, opt-out, non-home uptake | adaptive beats no-menu on most metrics; improves service versus fixed/random; does not beat fixed/random profit consistently | conditional; random profit 3/5 better | low uptake particularly weak versus random | conditional diagnostic, not strong | provenance-blocked and artifact-blocked | diagnostic/status tables only |
| C5 provenance/status | formal rows and gates | row status, checkpoint load, readiness, artifact status, claim guard | rows complete and checkpoint loaded; readiness dirty; artifacts blocked; claim guard false | not a performance claim | all regimes equally gated | strong status claim | not blocked for status wording | allowed as reproducibility/gate transparency |

## 5. Unsupported Or Mixed-Result Routing

The selected formal run does not support a strong central claim that optimized
adaptive `m+w+p` dominates all baselines. The main reasons are:

1. Profit-side evidence is mixed. Random menu outperforms adaptive on mean net
   profit and in 3 of 5 paired profit splits.
2. Adaptive-window increment is absent. Adaptive and optimized fixed-window are
   identical in the selected formal rows.
3. Service-quality evidence is better than profit evidence, but profit alone
   and service alone are not enough for the strong central claim.
4. Positive empirical classifications are blocked by dirty-git readiness and
   artifact/claim-guard gates.

The safest paper framing is therefore a conditional service-menu design study:
optimized service menus can improve acceptance, opt-out, and meeting-point
uptake, and can improve profit in some comparisons/regimes, but the selected
formal RC evidence does not justify universal superiority.

## 6. Phase 5 Recommendation

Do not skip Phase 5 by gate at this point.

Recommended route:

1. Clean or otherwise intentionally resolve the provenance gate, then rerun
   formal readiness and claim-ready artifact gates. Do not use destructive git
   cleanup without user approval.
2. If the goal remains a strong central empirical claim, execute Phase 5
   calibration with a documented pilot/final split. The current formal run is
   weak/unstable for the central claim and cannot be tuned directly.
3. If Phase 5 is not worth the runtime or scientific risk, reframe the paper as
   a conditional service-menu design contribution and document failure regimes.
4. Do not hand-edit generated rows, generated tables, generated figures, or
   manuscript claim guard outputs to force a stronger result.

## 7. Verification

Commands run from `work2_coding/`:

| Command | Result |
| --- | --- |
| `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | PASS |
| `python scripts/test_rc_formal_claim_diagnosis.py` | PASS: 3 tests |
| `python scripts/test_paired_replay_contract.py` | PASS: 12 tests |
| `python scripts/test_policy_fairness_contract.py` | PASS: 15 tests |
| `python scripts/test_artifact_gates.py` | PASS: 22 tests |
| `python scripts/test_phase4_artifact_pipeline.py` | PASS: 2 tests |

Manual audit:

- Blockers and provenance appear before positive result interpretation.
- CLAIM-01 through CLAIM-05 are covered.
- No confidence intervals or strong statistical-significance language are used.
- Claim classifications are marked diagnostic/provisional while gates remain
  blocked.

