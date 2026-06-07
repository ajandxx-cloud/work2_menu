# work2_formal_main Diagnostic Report

**Generated:** 2026-06-03T22:26:17Z

- Evidence gate: Mixed/inconclusive formal evidence
- Gate detail: CNN-SetMenuNet does not improve mean net_profit versus Cost-L or a core learned baseline in the formal RC evidence.
- Comparator: `--`
- Evidence scope: Formal RC evidence; robustness evidence is reported separately.

## Cost Prediction Error

- CNN-SetMenuNet: cost MAE 197.606, cost RMSE 761.379, Spearman ranking 0.489.
- If cost MAE/RMSE are unavailable for a method, the current normalized rows cannot isolate prediction error from menu-selection error.

## Ranking/Menu Selection Error

- CNN-SetMenuNet: menu regret 23.310, Top-L overlap 1.000, NDCG@L 1.000.
- Needs follow-up if CNN-SetMenuNet improves ranking metrics but still loses net_profit, because pricing or realized route-cost interactions may dominate menu quality.

## Candidate Feature Insufficiency

- Candidate feature sufficiency cannot be proven from aggregate rows alone.
- Needs follow-up if Top-L overlap and menu regret remain weak despite stable training budget and paired candidate pools.
- Phase 3 feature contracts must remain intact: K counts meeting-point candidates, L counts displayed meeting points, and home is always shown outside L.

## Training Budget

- Formal training episodes: `150`.
- Formal test episodes per seed: `50`.
- Observed seeds: `seed0, seed1, seed2, seed3, seed4`.
- A later 300/50 rerun is justified only if this diagnostic implicates training budget or seed instability; negative results alone do not trigger automatic escalation.

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

- Seed-to-seed trend summary: Cost-L heuristic: 0/5 seeds with higher CNN-SetMenuNet net profit; CNN-Menu: 0/5 seeds with higher CNN-SetMenuNet net profit; MLP-Menu: 0/5 seeds with higher CNN-SetMenuNet net profit.
- CNN-SetMenuNet net_profit sd: 11.962.

## Instance/Robustness Instability

- RC formal evidence and robustness evidence are separate claims.
- Before making any robustness claim, rebuild and inspect `work2_robustness` artifacts.
- If robustness remains degraded or mixed, use diagnostic-only robustness wording even when RC formal evidence is positive.

## Recommended Next Step

- Do not alter result rows manually. If diagnostics point to prediction, ranking, feature, MNL, route-cost, or seed instability, open a follow-up remediation phase or approved 300/50 escalation; do not run remediation automatically inside Phase 6.
