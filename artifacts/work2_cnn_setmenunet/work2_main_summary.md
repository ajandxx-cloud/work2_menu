# work2_main Phase 4 Pilot Summary

**Generated:** 2026-06-02T06:55:39Z

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
- MLP-Menu
- CNN-SetMenuNet
- Oracle Menu

## Outputs

- Standard CSV: `artifacts/work2_cnn_setmenunet/results_snapshot/work2_main_rows.csv`
- Legacy study outputs remain under `ooh_code/outputs/studies/`.
- Legacy generated paper artifacts remain under `ooh_code/artifacts/`.

## Aggregate Mean Table

| Method | Seeds | Net profit mean | Net profit sd | Menu regret | Top-L overlap | Quit rate | Avg walk |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nearest-L | 3 | -4967.195 | 17.185 | 19.848 | 1.000 | 0.374 | 1361.364 |
| Cost-L heuristic | 3 | -5031.043 | 14.027 | 24.617 | 1.000 | 0.352 | 2495.529 |
| CNN-Menu | 3 | -5016.567 | 16.202 | 24.936 | 1.000 | 0.355 | 2614.898 |
| MLP-Menu | 3 | -4464.271 | 13.352 | 3200.495 | 1.000 | 0.998 | 9.128 |
| CNN-SetMenuNet | 3 | -5093.849 | 26.196 | 24.566 | 1.000 | 0.380 | 2235.166 |
| Oracle Menu | 3 | -5096.154 | 28.985 | 80.558 | 1.000 | 0.377 | 2278.000 |

## Seed Variation

- Seed-to-seed trend summary: Cost-L heuristic: 0/3 seeds with higher CNN-SetMenuNet net profit; CNN-Menu: 0/3 seeds with higher CNN-SetMenuNet net profit; MLP-Menu: 0/3 seeds with higher CNN-SetMenuNet net profit.

## Method-Level Explanations

- Nearest-L: CNN-SetMenuNet minus this method net profit is -126.654; this method's quit rate is 0.374 and average walk is 1361.364.
- Cost-L heuristic: CNN-SetMenuNet minus this method net profit is -62.806; this method's quit rate is 0.352 and average walk is 2495.529.
- CNN-Menu: CNN-SetMenuNet minus this method net profit is -77.281; this method's quit rate is 0.355 and average walk is 2614.898.
- MLP-Menu: CNN-SetMenuNet minus this method net profit is -629.578; this method's quit rate is 0.998 and average walk is 9.128.
- CNN-SetMenuNet: net profit mean -5093.849, menu regret 24.566, Top-L overlap 1.000.
- Oracle Menu: CNN-SetMenuNet minus this method net profit is 2.306; this method's quit rate is 0.377 and average walk is 2278.000.

## Paper Conclusion Support

- Conclusion gate: Mixed/inconclusive pilot evidence.
- Gate detail: CNN-SetMenuNet does not improve mean net_profit versus Cost-L or a core learned baseline in this pilot.
- Comparator used by gate: `--`
- Net profit is primary; menu regret and Top-L overlap are supporting menu-quality metrics.
- Guardrail thresholds: obvious worsening is quit_rate increase > 0.05 or avg_walk increase > 300, with a 10% relative worsening floor.
- Diagnostic report: `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md`.

## Caveats

- All configured Phase 4 core methods are represented in the standard CSV.
- Phase 4 is a three-seed pilot, not formal robustness evidence.
- Weak or negative evidence should trigger diagnostics rather than manual result editing.
- Negative or weak Phase 4 pilot evidence does not invalidate the method; it triggers diagnostics.

## Phase 5 Readiness

- Conditionally ready only if diagnostics identify a fixable issue or a clear remedial experiment.
