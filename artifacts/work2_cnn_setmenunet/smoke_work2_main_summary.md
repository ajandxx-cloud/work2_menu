# smoke_work2_main Smoke Summary

**Generated:** 2026-06-02T04:20:58Z

## Settings

- Study: `smoke_work2_main`
- Instance: `RC`
- K: `10`
- L: `3`
- Home option: always shown
- Internal candidate slots: `11`
- Training episodes: `1`
- Test episodes: `1`
- Seeds: `seed0`

## Compared Methods

- CNN-Menu
- CNN-SetMenuNet
- Cost-L heuristic
- Nearest-L
- Oracle Menu
- SetMenuNet

## Outputs

- Standard CSV: `artifacts/work2_cnn_setmenunet/results_snapshot/smoke_work2_main_rows.csv`
- Legacy study outputs remain under `ooh_code/outputs/studies/`.
- Legacy generated paper artifacts remain under `ooh_code/artifacts/`.

## Comparability Contract

- K reports meeting-point candidate count and excludes home.
- L reports displayed meeting-point count and excludes home.
- Home is always shown outside L for learned, heuristic, and oracle rows.
- Oracle Menu is an upper/reference benchmark using true candidate costs, not deployable evidence.
- Nearest-L and Cost-L use their own ranking rules but share the same candidate pool and menu semantics.

## Smoke Metrics

| Method | Net profit | Total cost | Quit rate | Avg walk | Menu regret | Top-L overlap |
|---|---:|---:|---:|---:|---:|---:|
| Oracle Menu | -4.850 | 4.850 | 1.000 | 0.000 | 0.000 | 0.000 |
| CNN-SetMenuNet | -4.850 | 4.850 | 1.000 | 0.000 | 0.000 | 0.000 |
| SetMenuNet | -4.850 | 4.850 | 1.000 | 0.000 | 0.000 | 0.000 |
| CNN-Menu | -4.850 | 4.850 | 1.000 | 0.000 | 0.000 | 0.000 |
| Cost-L heuristic | -4.850 | 4.850 | 1.000 | 0.000 | 0.000 | 0.000 |
| Nearest-L | -4.850 | 4.850 | 1.000 | 0.000 | 0.000 | 0.000 |

## Paper Conclusion Support

- CNN-SetMenuNet net profit claim: Inconclusive - smoke confirms comparability, not statistical dominance
- Lower menu regret claim: Inconclusive - smoke confirms comparability, not statistical dominance
- Higher Top-L overlap claim: Inconclusive - smoke confirms comparability, not statistical dominance
- Quit rate and walking distance guardrail: Inconclusive in a one-seed smoke run.

## Caveats

- This is a one-seed, tiny-episode smoke run intended to validate the pipeline and schema.
- Negative or weak smoke evidence should trigger diagnostics in later formal phases, not manual result editing.

## Next Recommended Action

- Can Phase 3 proceed? Yes
- Required smoke methods and standard CSV columns are present.
