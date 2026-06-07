# work2_remediation_smoke Smoke Summary

**Generated:** 2026-06-05T02:25:21Z

## Settings

- Study: `work2_remediation_smoke`
- Instance: `RC`
- K: `10`
- L: `3`
- Home option: always shown
- Internal candidate slots: `11`
- Training episodes: `2`
- Test episodes: `1`
- Seeds: `seed0`

## Compared Methods

- CNN-Menu
- CNN-SetMenuNet
- CNN-SetMenuNet current
- Cost-L heuristic
- Nearest-L
- Oracle Menu

## Outputs

- Standard CSV: `artifacts/work2_cnn_setmenunet/results_snapshot/work2_remediation_smoke_rows.csv`
- Legacy study outputs remain under `ooh_code/outputs/studies/`.
- Legacy generated paper artifacts remain under `ooh_code/artifacts/`.

## Comparability Contract

- K reports meeting-point candidate count and excludes home.
- L reports displayed meeting-point count and excludes home.
- Home is always shown outside L for learned, heuristic, and oracle rows.
- The existing Oracle Menu row is a diagnostic reference; Phase 2 separates Cost Oracle from Profit Oracle before any upper-bound wording.
- Nearest-L and Cost-L use their own ranking rules but share the same candidate pool and menu semantics.

## Smoke Metrics

| Method | Net profit | Adjusted profit | Service profit | Quit rate | Guardrail | Avg walk | Menu regret | Top-L overlap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Oracle Menu | -5148.333 | -19048.333 | -5148.333 | 0.372 | pass | 1827.594 | 126.108 | 1.000 |
| CNN-Menu | -5070.033 | -18070.033 | -5070.033 | 0.348 | pass | 2285.134 | 38.830 | 1.000 |
| Cost-L heuristic | -5112.326 | -18312.326 | -5112.326 | 0.353 | pass | 2066.952 | 35.201 | 1.000 |
| Nearest-L | -5053.038 | -18553.038 | -5053.038 | 0.361 | pass | 1159.893 | 28.754 | 1.000 |
| CNN-SetMenuNet current | -5158.309 | -19158.309 | -5158.309 | 0.374 | pass | 1676.471 | 35.892 | 1.000 |
| CNN-SetMenuNet | -5160.933 | -18860.933 | -5160.933 | 0.366 | pass | 1777.219 | 35.377 | 1.000 |

## Paper Conclusion Support

- CNN-SetMenuNet net profit claim: Inconclusive - smoke confirms comparability, not statistical dominance
- Lower menu regret claim: Inconclusive - smoke confirms comparability, not statistical dominance
- Higher Top-L overlap claim: Inconclusive - smoke confirms comparability, not statistical dominance
- Quit rate and walking distance guardrail: Inconclusive in a one-seed smoke run.

## Caveats

- This is a one-seed, tiny-episode smoke run intended to validate the pipeline and schema.
- Negative or weak smoke evidence should trigger diagnostics in later formal phases, not manual result editing.

## Next Recommended Action

- Can Phase 3 proceed? No
- Missing required methods: Expected-Profit Enumeration, Service-Constrained Expected-Profit, Profit Oracle
