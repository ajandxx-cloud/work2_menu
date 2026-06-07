# work2_remediation_smoke Diagnostic Report

**Generated:** 2026-06-05T02:25:21Z

- Evidence gate: Remediation smoke trace
- Gate detail: Smoke run validates remediation artifact paths and offer-level objective trace only; it is not paper evidence.
- Comparator: `--`
- Evidence scope: Smoke RC evidence; robustness evidence is reported separately.
- Service guardrail: quit_rate <= `0.4`.
- Quit penalty for adjusted profit: `100.0` per opt-out request.

## Service-Constrained Objective Diagnostics

- CNN-SetMenuNet: raw net profit -5160.933, adjusted profit -18860.933, service-constrained profit -5160.933, quit rate 0.366, guardrail violation rate 0.000.
- A row with empty service-constrained profit violated the quit-rate guardrail and should not be treated as supportive profit evidence.
- High-quit policies that improve raw net_profit must be discussed as diagnostic failures unless adjusted/service-constrained profit remains competitive.

## Oracle Taxonomy

- Cost Oracle: selects low true insertion-cost menus; useful for cost-ranking diagnostics only.
- Profit Oracle: should select high expected-profit menus under choice, pricing, route-cost, and opt-out objective; this remains Phase 3 scope unless explicitly implemented in the current manifest.
- Realized Oracle: ex-post upper bound using realized choices/routes; not implemented in v1 unless a later phase adds it.
- Do not describe the existing `Oracle Menu` row as a profit upper bound unless the manifest explicitly maps it to Profit Oracle semantics.

## Cost Prediction Error

- CNN-SetMenuNet: cost MAE 213.620, cost RMSE 580.084, Spearman ranking 0.393.
- If cost MAE/RMSE are unavailable for a method, the current normalized rows cannot isolate prediction error from menu-selection error.

## Ranking/Menu Selection Error

- CNN-SetMenuNet: menu regret 35.377, Top-L overlap 1.000, NDCG@L 1.000.
- Needs follow-up if CNN-SetMenuNet improves ranking metrics but still loses net_profit, because pricing or realized route-cost interactions may dominate menu quality.

## Offer-Level Objective Trace

- CNN-SetMenuNet: offer trace rows 1496.000, system-minus-menu cost 0.266, choice probability 0.143, selected expected profit -1.854.
- If system-minus-menu cost is material while selected expected profit is weak, the menu objective may be misaligned with realized net_profit.
- Remediation runs should compare `menu_objective_mode=current` with `menu_objective_mode=system_profit` using unchanged seeds and comparators.

## Candidate Feature Insufficiency

- Candidate feature sufficiency cannot be proven from aggregate rows alone.
- Needs follow-up if Top-L overlap and menu regret remain weak despite stable training budget and paired candidate pools.
- Phase 3 feature contracts must remain intact: K counts meeting-point candidates, L counts displayed meeting points, and home is always shown outside L.

## Training Budget

- Smoke training episodes: `2`.
- Smoke test episodes per seed: `1`.
- Observed seeds: `seed0`.
- Smoke evidence validates the remediation path only; pilot remains the next preregistered gate.

## MNL/Outside-Option Sensitivity

- Outside-option utility: `0.0`.
- Base utility: `1.0`.
- Incentive sensitivity: `-0.08`.
- If quit_rate worsens while ranking metrics improve, passenger-choice sensitivity may dominate menu quality.

## Route-Cost Realization Gap

- Route-cost realization cannot be isolated from aggregate rows alone.
- Needs follow-up if predicted ranking is reasonable but realized net_profit or total_cost degrades.
- Do not modify HGS/Hygese route-cost core logic inside this diagnostic phase.

## Seed Instability

- Seed-to-seed trend summary: Cost-L heuristic: 0/1 seeds with higher CNN-SetMenuNet net profit; CNN-Menu: 0/1 seeds with higher CNN-SetMenuNet net profit.
- CNN-SetMenuNet net_profit sd: 0.000.

## Instance/Robustness Instability

- RC formal evidence and robustness evidence are separate claims.
- Before making any robustness claim, rebuild and inspect `work2_robustness` artifacts.
- If robustness remains degraded or mixed, use diagnostic-only robustness wording even when RC formal evidence is positive.

## Recommended Next Step

- Do not alter result rows manually. If diagnostics point to prediction or ranking error, tune that component and rerun the same manifest; if instability dominates, report the current evidence as mixed and reserve stronger claims for later preregistered phases.
