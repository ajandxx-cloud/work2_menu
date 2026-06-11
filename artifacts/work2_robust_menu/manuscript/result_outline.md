# Result Outline

## Current Evidence Status

Current artifact status is not claim-ready. Result sections must remain a report structure and limitation/status discussion, not empirical superiority claims.

- `missing_checkpoint_file`: Required checkpoint file is unavailable; refusing random-weight evidence. Path: `outputs/shared_training/work2_robust_menu/pilot/supervised_ml.pt`.
- `formal_skipped`: Formal evidence was skipped for this Phase 4 run; formal claim readiness is false.

## Result Families

- Exact-vs-greedy quality: report candidate counts, build time, gap/overlap diagnostics, and fallback reason.
- Robust filtering comparison: report pruning diagnostics, ETA-risk behavior, and feasibility-preserving no-filter diagnostics.
- Uptake-regime behavior: report low/medium regime coverage when available and avoid extrapolating beyond covered regimes.
- Profit decomposition: report profit, acceptance, opt-out, route/service cost, and uncertainty/gap outputs only when source rows are claim-ready.
- External or semi-real checks: mark as unavailable unless new external validation data is added.

## Limitations

- Current evidence is simulation-pipeline evidence, not real passenger behavioral validation.
- no_filter_diagnostic is a diagnostic upper bound or stress test, not an operational recommendation.
- Exact optimality applies only to bounded menu candidate subsets, not the full dynamic DRT system.
- Pilot/formal empirical claims require loaded checkpoint provenance and non-placeholder rows.
