# work2_formal_main Formal Summary

**Generated:** 2026-06-03T22:26:17Z

## Settings

- Study: `work2_formal_main`
- Instance: `RC`
- K: `10`
- L: `3`
- Home option: always shown outside public L
- Training episodes: `150`
- Test episodes: `50`
- Seeds: `seed0, seed1, seed2, seed3, seed4`
- Formal budget rule: `300/50` is diagnostic escalation only, not automatic.

## Required Formal Methods

- Nearest-L
- Cost-L heuristic
- CNN-Menu
- MLP-Menu
- SetMenuNet
- CNN-SetMenuNet
- Oracle Menu

## Outputs

- Standard CSV: `artifacts/work2_cnn_setmenunet/results_snapshot/work2_formal_main_rows.csv`
- Raw study outputs remain under `ooh_code/outputs/studies/`.
- Lightweight Work2 summaries remain under `artifacts/work2_cnn_setmenunet/`.
- Diagnostic report: `artifacts/work2_cnn_setmenunet/diagnostics/work2_formal_main_diagnostic.md`.

## Main Formal Table

| Method | Seeds | Net profit | Total cost | Quit rate | MP share | Avg walk | Menu regret | Top-L overlap | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Nearest-L | 5 | -4959.466 | 4959.466 | 0.373 | -- | 1352.336 | 19.485 | 1.000 | 0.035 |
| Cost-L heuristic | 5 | -5003.708 | 5003.708 | 0.351 | -- | 2496.678 | 23.249 | 1.000 | 0.035 |
| CNN-Menu | 5 | -5001.454 | 5001.454 | 0.354 | -- | 2607.244 | 23.448 | 1.000 | 0.035 |
| MLP-Menu | 5 | -4453.467 | 4453.467 | 0.997 | -- | 14.664 | 1742.937 | 1.000 | 0.038 |
| SetMenuNet | 5 | -4452.977 | 4452.977 | 0.997 | -- | 14.664 | 1742.937 | 1.000 | 0.038 |
| CNN-SetMenuNet | 5 | -5083.690 | 5083.690 | 0.380 | -- | 2199.565 | 23.310 | 1.000 | 0.040 |
| Oracle Menu | 5 | -5084.768 | 5084.768 | 0.376 | -- | 2248.880 | 78.289 | 1.000 | 0.039 |

## Seed Variation

- Seed-to-seed trend summary: Cost-L heuristic: 0/5 seeds with higher CNN-SetMenuNet net profit; CNN-Menu: 0/5 seeds with higher CNN-SetMenuNet net profit; MLP-Menu: 0/5 seeds with higher CNN-SetMenuNet net profit.

## Method-Level Explanations

- Nearest-L: CNN-SetMenuNet minus this method net profit is -124.223; this method's quit rate is 0.373 and average walk is 1352.336.
- Cost-L heuristic: CNN-SetMenuNet minus this method net profit is -79.982; this method's quit rate is 0.351 and average walk is 2496.678.
- CNN-Menu: CNN-SetMenuNet minus this method net profit is -82.235; this method's quit rate is 0.354 and average walk is 2607.244.
- MLP-Menu: CNN-SetMenuNet minus this method net profit is -630.223; this method's quit rate is 0.997 and average walk is 14.664.
- SetMenuNet: CNN-SetMenuNet minus this method net profit is -630.713; this method's quit rate is 0.997 and average walk is 14.664.
- CNN-SetMenuNet: net profit mean -5083.690, menu regret 23.310, Top-L overlap 1.000.
- Oracle Menu: CNN-SetMenuNet minus this method net profit is 1.078; this method's quit rate is 0.376 and average walk is 2248.880.

## Formal RC Conclusion Support

- Conclusion gate: Mixed/inconclusive formal evidence.
- Gate detail: CNN-SetMenuNet does not improve mean net_profit versus Cost-L or a core learned baseline in the formal RC evidence.
- Comparator used by gate: `--`
- Net profit is primary; menu regret and Top-L overlap are supporting menu-quality metrics.
- Quit rate and average walking distance remain passenger-experience guardrails.

## Robustness Claim Separation

- RC formal evidence and robustness evidence are separate claims.
- A positive RC formal result must not be converted into a global robustness claim.
- Cite robustness only after rebuilding `work2_robustness` artifacts and checking diagnostic posture.

## Caveats

- All required formal methods are represented in the standard CSV.
- Generated result rows, tables, figures, and summaries must not be manually edited toward a desired conclusion.
- Negative or weak Phase 6 formal evidence does not invalidate the method; it triggers diagnostics.

## Recommended Next Action

- Use the diagnostic report to choose a follow-up remediation phase or an explicitly approved 300/50 escalation if training budget or seed instability is implicated.
