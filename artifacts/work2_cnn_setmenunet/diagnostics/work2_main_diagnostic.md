# work2_main Diagnostic Report

**Generated:** 2026-06-02T06:55:39Z

- Evidence gate: Mixed/inconclusive pilot evidence
- Gate detail: CNN-SetMenuNet does not improve mean net_profit versus Cost-L or a core learned baseline in this pilot.
- Comparator: `--`

## Cost Prediction Error

- CNN-SetMenuNet: cost MAE 210.143, cost RMSE 776.886, Spearman ranking 0.500.
- If cost MAE/RMSE are unavailable for a method, the current normalized rows cannot isolate prediction error from menu-selection error.

## Ranking/Menu Selection Error

- CNN-SetMenuNet: menu regret 24.566, Top-L overlap 1.000, NDCG@L 1.000.
- Needs follow-up if CNN-SetMenuNet improves ranking metrics but still loses net_profit, because pricing or realized route-cost interactions may dominate menu quality.

## Training Budget

- Pilot training episodes: `80`.
- Pilot test episodes per seed: `20`.
- Observed seeds: `seed0, seed1, seed2`.
- Formal evidence remains later-phase scope; Phase 4 should not expand seeds automatically unless diagnostics identify a fixable training-budget issue.

## Seed Instability

- Seed-to-seed trend summary: Cost-L heuristic: 0/3 seeds with higher CNN-SetMenuNet net profit; CNN-Menu: 0/3 seeds with higher CNN-SetMenuNet net profit; MLP-Menu: 0/3 seeds with higher CNN-SetMenuNet net profit.
- CNN-SetMenuNet net_profit sd: 26.196.

## Recommended Next Step

- Do not alter result rows manually. If diagnostics point to prediction or ranking error, tune that component and rerun the same manifest; if instability dominates, report Phase 4 as mixed and reserve stronger claims for later robustness/formal phases.
