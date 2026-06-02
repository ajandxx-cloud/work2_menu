# work2_main Phase 4 Pilot Summary

**Generated:** 2026-06-02T04:14:39Z

## Settings

- Study: `work2_main`
- Instance: `RC`
- K: `10`
- L: `3`
- Home option: always shown
- Training episodes: `80`
- Test episodes: `20`
- Seeds: `seed0, seed1, seed2`

## Core Methods

- Nearest-L
- Cost-L heuristic
- CNN-Menu
- MLP-Menu (missing)
- CNN-SetMenuNet
- Oracle Menu

## Outputs

- Standard CSV: `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv`
- Legacy study outputs remain under `ooh_code/outputs/studies/`.
- Legacy generated paper artifacts remain under `ooh_code/artifacts/`.

## Aggregate Mean Table

| Method | Seeds | Net profit mean | Net profit sd | Menu regret | Top-L overlap | Quit rate | Avg walk |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nearest-L | 3 | -5015.786 | 33.769 | 19.419 | 1.000 | 0.362 | 1554.610 |
| Cost-L heuristic | 3 | -5047.636 | 18.152 | 24.794 | 1.000 | 0.353 | 2499.727 |
| CNN-Menu | 3 | -5045.706 | 11.105 | 25.088 | 1.000 | 0.355 | 2635.128 |
| CNN-SetMenuNet | 3 | -5105.858 | 20.329 | 24.610 | 1.000 | 0.375 | 2311.556 |
| Oracle Menu | 3 | -5109.995 | 26.938 | 80.576 | 1.000 | 0.374 | 2318.840 |

## Seed Variation

- Seed-to-seed trend summary: Cost-L heuristic: 0/3 seeds with higher CNN-SetMenuNet net profit; CNN-Menu: 0/3 seeds with higher CNN-SetMenuNet net profit.

## Method-Level Explanations

- Nearest-L: CNN-SetMenuNet minus this method net profit is -90.072; this method's quit rate is 0.362 and average walk is 1554.610.
- Cost-L heuristic: CNN-SetMenuNet minus this method net profit is -58.222; this method's quit rate is 0.353 and average walk is 2499.727.
- CNN-Menu: CNN-SetMenuNet minus this method net profit is -60.152; this method's quit rate is 0.355 and average walk is 2635.128.
- MLP-Menu: not present in the current pilot rows; treat the comparison as incomplete.
- CNN-SetMenuNet: net profit mean -5105.858, menu regret 24.610, Top-L overlap 1.000.
- Oracle Menu: CNN-SetMenuNet minus this method net profit is 4.137; this method's quit rate is 0.374 and average walk is 2318.840.

## Paper Conclusion Support

- Conclusion gate: pending graded Phase 4 evidence classification.
- Net profit is primary; menu regret and Top-L overlap are supporting menu-quality metrics.
- Quit rate and average walk are guardrails; obvious worsening must be treated as a trade-off.

## Caveats

- Missing core methods: MLP-Menu.
- Phase 4 is a three-seed pilot, not formal robustness evidence.
- Weak or negative evidence should trigger diagnostics rather than manual result editing.

## Phase 5 Readiness

- Pending graded conclusion gate.
