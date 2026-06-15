# RC Formal Diagnostic Tables

## Blocker And Provenance Status

- Source run: `outputs\formal_v1\formal_robust_menu\formal_robust_menu-20260614T032323Z-c672286a`
- Run ID: `formal_robust_menu-20260614T032323Z-c672286a`
- Execution status: `completed` with `35` rows
- Readiness status: `blocked`; claim-ready allowed: `false`
- Artifact status: `blocked`; artifact claim-ready: `false`; formal claim-ready: `false`
- Claim guard ready: `false`; blocked claim IDs: `universal_dominance, real_passenger_validation, no_filter_operational_recommendation, full_dynamic_exact_optimality, ungated_dspo_plus_ranking, empirical_superiority, pilot_formal_completed`
- Checkpoint load status: `loaded`; checkpoint hash: `d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4`
- Claim interpretation status: diagnostic only. Dirty-git readiness and artifact gates block final manuscript claim use.
- Confidence intervals are intentionally omitted because this formal diagnosis has only five paired splits.
- Older smoke artifacts and smoke claim guards are not used as Phase 4 claim evidence.

### Readiness Blockers

- `dirty_git`: Repository has uncommitted changes; formal claim-ready readiness requires git_dirty=false.

### Artifact Gate Reasons

- pilot/formal rows require outside_option_util metadata
- pilot/formal rows require valid method_family metadata

## Policy Means And Population Standard Deviations

| Policy | Metric | N | Mean | Std Pop |
| --- | --- | ---: | ---: | ---: |
| `mainline_no_menu` | `net_profit` | 5 | -192582.600000 | 2586.661168 |
| `mainline_no_menu` | `operational_cost` | 5 | 192582.600000 | 2586.661168 |
| `mainline_no_menu` | `total_cost` | 5 | 192582.600000 | 2586.661168 |
| `mainline_no_menu` | `acceptance_rate` | 5 | 0.524051 | 0.000000 |
| `mainline_no_menu` | `served_rate` | 5 | 0.524051 | 0.000000 |
| `mainline_no_menu` | `optout_rate` | 5 | 0.475949 | 0.000000 |
| `mainline_no_menu` | `home_share` | 5 | 0.524051 | 0.000000 |
| `mainline_no_menu` | `meeting_point_uptake_rate` | 5 | 0.000000 | 0.000000 |
| `mainline_no_menu` | `service_time_total` | 5 | 192582.600000 | 2586.661168 |
| `mainline_fixed_menu` | `net_profit` | 5 | -182538.276401 | 6423.221052 |
| `mainline_fixed_menu` | `operational_cost` | 5 | 182422.560000 | 6518.051860 |
| `mainline_fixed_menu` | `total_cost` | 5 | 183695.215856 | 6460.248460 |
| `mainline_fixed_menu` | `acceptance_rate` | 5 | 0.530541 | 0.017491 |
| `mainline_fixed_menu` | `served_rate` | 5 | 0.530541 | 0.017491 |
| `mainline_fixed_menu` | `optout_rate` | 5 | 0.469459 | 0.017491 |
| `mainline_fixed_menu` | `home_share` | 5 | 0.466322 | 0.026712 |
| `mainline_fixed_menu` | `meeting_point_uptake_rate` | 5 | 0.064219 | 0.028173 |
| `mainline_fixed_menu` | `service_time_total` | 5 | 182422.560000 | 6518.051860 |
| `mainline_random_menu` | `net_profit` | 5 | -176651.519334 | 8123.630251 |
| `mainline_random_menu` | `operational_cost` | 5 | 176639.160000 | 8198.128385 |
| `mainline_random_menu` | `total_cost` | 5 | 177827.204072 | 8187.117872 |
| `mainline_random_menu` | `acceptance_rate` | 5 | 0.517462 | 0.025984 |
| `mainline_random_menu` | `served_rate` | 5 | 0.517462 | 0.025984 |
| `mainline_random_menu` | `optout_rate` | 5 | 0.482538 | 0.025984 |
| `mainline_random_menu` | `home_share` | 5 | 0.452100 | 0.010494 |
| `mainline_random_menu` | `meeting_point_uptake_rate` | 5 | 0.065362 | 0.031756 |
| `mainline_random_menu` | `service_time_total` | 5 | 176639.160000 | 8198.128385 |
| `mainline_optimized_m` | `net_profit` | 5 | -190803.240000 | 2870.379446 |
| `mainline_optimized_m` | `operational_cost` | 5 | 190803.240000 | 2870.379446 |
| `mainline_optimized_m` | `total_cost` | 5 | 190803.240000 | 2870.379446 |
| `mainline_optimized_m` | `acceptance_rate` | 5 | 0.525000 | 0.010247 |
| `mainline_optimized_m` | `served_rate` | 5 | 0.525000 | 0.010247 |
| `mainline_optimized_m` | `optout_rate` | 5 | 0.475000 | 0.010247 |
| `mainline_optimized_m` | `home_share` | 5 | 0.482496 | 0.010693 |
| `mainline_optimized_m` | `meeting_point_uptake_rate` | 5 | 0.042504 | 0.010875 |
| `mainline_optimized_m` | `service_time_total` | 5 | 190803.240000 | 2870.379446 |
| `mainline_optimized_mw` | `net_profit` | 5 | -184672.560000 | 8329.927572 |
| `mainline_optimized_mw` | `operational_cost` | 5 | 184672.560000 | 8329.927572 |
| `mainline_optimized_mw` | `total_cost` | 5 | 184672.560000 | 8329.927572 |
| `mainline_optimized_mw` | `acceptance_rate` | 5 | 0.512758 | 0.014443 |
| `mainline_optimized_mw` | `served_rate` | 5 | 0.512758 | 0.014443 |
| `mainline_optimized_mw` | `optout_rate` | 5 | 0.487242 | 0.014443 |
| `mainline_optimized_mw` | `home_share` | 5 | 0.494773 | 0.015021 |
| `mainline_optimized_mw` | `meeting_point_uptake_rate` | 5 | 0.017985 | 0.004153 |
| `mainline_optimized_mw` | `service_time_total` | 5 | 184672.560000 | 8329.927572 |
| `mainline_optimized_fixed_window` | `net_profit` | 5 | -180581.747301 | 7356.443474 |
| `mainline_optimized_fixed_window` | `operational_cost` | 5 | 180306.360000 | 7467.095605 |
| `mainline_optimized_fixed_window` | `total_cost` | 5 | 181746.330274 | 7387.731641 |
| `mainline_optimized_fixed_window` | `acceptance_rate` | 5 | 0.555488 | 0.032794 |
| `mainline_optimized_fixed_window` | `served_rate` | 5 | 0.555488 | 0.032794 |
| `mainline_optimized_fixed_window` | `optout_rate` | 5 | 0.444512 | 0.032794 |
| `mainline_optimized_fixed_window` | `home_share` | 5 | 0.463208 | 0.015807 |
| `mainline_optimized_fixed_window` | `meeting_point_uptake_rate` | 5 | 0.092280 | 0.038870 |
| `mainline_optimized_fixed_window` | `service_time_total` | 5 | 180306.360000 | 7467.095605 |
| `mainline_optimized_adaptive` | `net_profit` | 5 | -180581.747301 | 7356.443474 |
| `mainline_optimized_adaptive` | `operational_cost` | 5 | 180306.360000 | 7467.095605 |
| `mainline_optimized_adaptive` | `total_cost` | 5 | 181746.330274 | 7387.731641 |
| `mainline_optimized_adaptive` | `acceptance_rate` | 5 | 0.555488 | 0.032794 |
| `mainline_optimized_adaptive` | `served_rate` | 5 | 0.555488 | 0.032794 |
| `mainline_optimized_adaptive` | `optout_rate` | 5 | 0.444512 | 0.032794 |
| `mainline_optimized_adaptive` | `home_share` | 5 | 0.463208 | 0.015807 |
| `mainline_optimized_adaptive` | `meeting_point_uptake_rate` | 5 | 0.092280 | 0.038870 |
| `mainline_optimized_adaptive` | `service_time_total` | 5 | 180306.360000 | 7467.095605 |

## Paired Direction Counts

| Baseline | Metric | Adaptive Better | Baseline Better | Tie | Missing |
| --- | --- | ---: | ---: | ---: | ---: |
| `mainline_no_menu` | `net_profit` | 4 | 1 | 0 | 0 |
| `mainline_no_menu` | `operational_cost` | 4 | 1 | 0 | 0 |
| `mainline_no_menu` | `total_cost` | 4 | 1 | 0 | 0 |
| `mainline_no_menu` | `acceptance_rate` | 4 | 1 | 0 | 0 |
| `mainline_no_menu` | `served_rate` | 4 | 1 | 0 | 0 |
| `mainline_no_menu` | `optout_rate` | 4 | 1 | 0 | 0 |
| `mainline_no_menu` | `home_share` | 0 | 5 | 0 | 0 |
| `mainline_no_menu` | `meeting_point_uptake_rate` | 5 | 0 | 0 | 0 |
| `mainline_no_menu` | `service_time_total` | 4 | 1 | 0 | 0 |
| `mainline_fixed_menu` | `net_profit` | 2 | 3 | 0 | 0 |
| `mainline_fixed_menu` | `operational_cost` | 3 | 2 | 0 | 0 |
| `mainline_fixed_menu` | `total_cost` | 2 | 3 | 0 | 0 |
| `mainline_fixed_menu` | `acceptance_rate` | 4 | 1 | 0 | 0 |
| `mainline_fixed_menu` | `served_rate` | 4 | 1 | 0 | 0 |
| `mainline_fixed_menu` | `optout_rate` | 4 | 1 | 0 | 0 |
| `mainline_fixed_menu` | `home_share` | 2 | 3 | 0 | 0 |
| `mainline_fixed_menu` | `meeting_point_uptake_rate` | 5 | 0 | 0 | 0 |
| `mainline_fixed_menu` | `service_time_total` | 3 | 2 | 0 | 0 |
| `mainline_random_menu` | `net_profit` | 2 | 3 | 0 | 0 |
| `mainline_random_menu` | `operational_cost` | 2 | 3 | 0 | 0 |
| `mainline_random_menu` | `total_cost` | 2 | 3 | 0 | 0 |
| `mainline_random_menu` | `acceptance_rate` | 5 | 0 | 0 | 0 |
| `mainline_random_menu` | `served_rate` | 5 | 0 | 0 | 0 |
| `mainline_random_menu` | `optout_rate` | 5 | 0 | 0 | 0 |
| `mainline_random_menu` | `home_share` | 4 | 1 | 0 | 0 |
| `mainline_random_menu` | `meeting_point_uptake_rate` | 5 | 0 | 0 | 0 |
| `mainline_random_menu` | `service_time_total` | 2 | 3 | 0 | 0 |
| `mainline_optimized_m` | `net_profit` | 5 | 0 | 0 | 0 |
| `mainline_optimized_m` | `operational_cost` | 5 | 0 | 0 | 0 |
| `mainline_optimized_m` | `total_cost` | 4 | 1 | 0 | 0 |
| `mainline_optimized_m` | `acceptance_rate` | 3 | 2 | 0 | 0 |
| `mainline_optimized_m` | `served_rate` | 3 | 2 | 0 | 0 |
| `mainline_optimized_m` | `optout_rate` | 3 | 2 | 0 | 0 |
| `mainline_optimized_m` | `home_share` | 1 | 4 | 0 | 0 |
| `mainline_optimized_m` | `meeting_point_uptake_rate` | 5 | 0 | 0 | 0 |
| `mainline_optimized_m` | `service_time_total` | 5 | 0 | 0 | 0 |
| `mainline_optimized_mw` | `net_profit` | 2 | 3 | 0 | 0 |
| `mainline_optimized_mw` | `operational_cost` | 2 | 3 | 0 | 0 |
| `mainline_optimized_mw` | `total_cost` | 2 | 3 | 0 | 0 |
| `mainline_optimized_mw` | `acceptance_rate` | 5 | 0 | 0 | 0 |
| `mainline_optimized_mw` | `served_rate` | 5 | 0 | 0 | 0 |
| `mainline_optimized_mw` | `optout_rate` | 5 | 0 | 0 | 0 |
| `mainline_optimized_mw` | `home_share` | 0 | 5 | 0 | 0 |
| `mainline_optimized_mw` | `meeting_point_uptake_rate` | 5 | 0 | 0 | 0 |
| `mainline_optimized_mw` | `service_time_total` | 2 | 3 | 0 | 0 |
| `mainline_optimized_fixed_window` | `net_profit` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `operational_cost` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `total_cost` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `acceptance_rate` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `served_rate` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `optout_rate` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `home_share` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `meeting_point_uptake_rate` | 0 | 0 | 5 | 0 |
| `mainline_optimized_fixed_window` | `service_time_total` | 0 | 0 | 5 | 0 |

## Uptake-Regime Direction Counts

| Regime | Baseline | Metric | Adaptive Better | Baseline Better | Tie |
| --- | --- | --- | ---: | ---: | ---: |
| `low` | `mainline_no_menu` | `net_profit` | 1 | 1 | 0 |
| `low` | `mainline_no_menu` | `acceptance_rate` | 1 | 1 | 0 |
| `low` | `mainline_no_menu` | `served_rate` | 1 | 1 | 0 |
| `low` | `mainline_no_menu` | `optout_rate` | 1 | 1 | 0 |
| `low` | `mainline_no_menu` | `meeting_point_uptake_rate` | 2 | 0 | 0 |
| `low` | `mainline_fixed_menu` | `net_profit` | 1 | 1 | 0 |
| `low` | `mainline_fixed_menu` | `acceptance_rate` | 1 | 1 | 0 |
| `low` | `mainline_fixed_menu` | `served_rate` | 1 | 1 | 0 |
| `low` | `mainline_fixed_menu` | `optout_rate` | 1 | 1 | 0 |
| `low` | `mainline_fixed_menu` | `meeting_point_uptake_rate` | 2 | 0 | 0 |
| `low` | `mainline_random_menu` | `net_profit` | 0 | 2 | 0 |
| `low` | `mainline_random_menu` | `acceptance_rate` | 2 | 0 | 0 |
| `low` | `mainline_random_menu` | `served_rate` | 2 | 0 | 0 |
| `low` | `mainline_random_menu` | `optout_rate` | 2 | 0 | 0 |
| `low` | `mainline_random_menu` | `meeting_point_uptake_rate` | 2 | 0 | 0 |
| `low` | `mainline_optimized_m` | `net_profit` | 2 | 0 | 0 |
| `low` | `mainline_optimized_m` | `acceptance_rate` | 0 | 2 | 0 |
| `low` | `mainline_optimized_m` | `served_rate` | 0 | 2 | 0 |
| `low` | `mainline_optimized_m` | `optout_rate` | 0 | 2 | 0 |
| `low` | `mainline_optimized_m` | `meeting_point_uptake_rate` | 2 | 0 | 0 |
| `low` | `mainline_optimized_mw` | `net_profit` | 0 | 2 | 0 |
| `low` | `mainline_optimized_mw` | `acceptance_rate` | 2 | 0 | 0 |
| `low` | `mainline_optimized_mw` | `served_rate` | 2 | 0 | 0 |
| `low` | `mainline_optimized_mw` | `optout_rate` | 2 | 0 | 0 |
| `low` | `mainline_optimized_mw` | `meeting_point_uptake_rate` | 2 | 0 | 0 |
| `low` | `mainline_optimized_fixed_window` | `net_profit` | 0 | 0 | 2 |
| `low` | `mainline_optimized_fixed_window` | `acceptance_rate` | 0 | 0 | 2 |
| `low` | `mainline_optimized_fixed_window` | `served_rate` | 0 | 0 | 2 |
| `low` | `mainline_optimized_fixed_window` | `optout_rate` | 0 | 0 | 2 |
| `low` | `mainline_optimized_fixed_window` | `meeting_point_uptake_rate` | 0 | 0 | 2 |
| `medium` | `mainline_no_menu` | `net_profit` | 3 | 0 | 0 |
| `medium` | `mainline_no_menu` | `acceptance_rate` | 3 | 0 | 0 |
| `medium` | `mainline_no_menu` | `served_rate` | 3 | 0 | 0 |
| `medium` | `mainline_no_menu` | `optout_rate` | 3 | 0 | 0 |
| `medium` | `mainline_no_menu` | `meeting_point_uptake_rate` | 3 | 0 | 0 |
| `medium` | `mainline_fixed_menu` | `net_profit` | 1 | 2 | 0 |
| `medium` | `mainline_fixed_menu` | `acceptance_rate` | 3 | 0 | 0 |
| `medium` | `mainline_fixed_menu` | `served_rate` | 3 | 0 | 0 |
| `medium` | `mainline_fixed_menu` | `optout_rate` | 3 | 0 | 0 |
| `medium` | `mainline_fixed_menu` | `meeting_point_uptake_rate` | 3 | 0 | 0 |
| `medium` | `mainline_random_menu` | `net_profit` | 2 | 1 | 0 |
| `medium` | `mainline_random_menu` | `acceptance_rate` | 3 | 0 | 0 |
| `medium` | `mainline_random_menu` | `served_rate` | 3 | 0 | 0 |
| `medium` | `mainline_random_menu` | `optout_rate` | 3 | 0 | 0 |
| `medium` | `mainline_random_menu` | `meeting_point_uptake_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_m` | `net_profit` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_m` | `acceptance_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_m` | `served_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_m` | `optout_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_m` | `meeting_point_uptake_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_mw` | `net_profit` | 2 | 1 | 0 |
| `medium` | `mainline_optimized_mw` | `acceptance_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_mw` | `served_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_mw` | `optout_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_mw` | `meeting_point_uptake_rate` | 3 | 0 | 0 |
| `medium` | `mainline_optimized_fixed_window` | `net_profit` | 0 | 0 | 3 |
| `medium` | `mainline_optimized_fixed_window` | `acceptance_rate` | 0 | 0 | 3 |
| `medium` | `mainline_optimized_fixed_window` | `served_rate` | 0 | 0 | 3 |
| `medium` | `mainline_optimized_fixed_window` | `optout_rate` | 0 | 0 | 3 |
| `medium` | `mainline_optimized_fixed_window` | `meeting_point_uptake_rate` | 0 | 0 | 3 |

## Diagnostic Notes

- Adaptive versus random-menu net profit direction counts: adaptive better `2`, random better `3`, tie `0`.
- Adaptive versus optimized fixed-window net profit direction counts: adaptive better `0`, fixed-window better `0`, tie `5`.
- Adaptive and optimized fixed-window rows are identical across all tracked metrics: `true`.
- Product ablation evidence should be read from adaptive comparisons with `mainline_optimized_m` and `mainline_optimized_mw`.
- Menu construction evidence should be read from adaptive comparisons with no-menu, fixed-menu, and random-menu baselines.
- Acceptance, opt-out, home-share, and meeting-point uptake trade-offs are reported separately from profit/cost metrics.
- These tables do not upgrade manuscript claims while readiness, artifact, or claim-guard gates remain blocked.
