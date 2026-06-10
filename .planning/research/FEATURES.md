# Feature Research

## Table Stakes

### Repository Audit And Runtime Repair

- Identify the active runtime root.
- Verify import paths for `Src.config`, `DSPO_Menu`, simulator, and choice model.
- List runnable entry points, missing runners, and current command contract.
- Produce a concise audit report before algorithm behavior changes.

### Choice And Accounting Semantics

- Represent outcomes explicitly as `accepted_home`, `accepted_meeting_point`, and `opted_out`.
- Prevent opt-out from mutating route plans as accepted service.
- Record opt-out counts, service cost, acceptance rate, and route-state effects separately.
- Preserve model-update compatibility only where needed.

### Robust ETA/Time-Window Filtering

- Implement modes: `hard`, `calibrated`, `interval_overlap`, `chance_constraint`, `soft_penalty`, and `none`.
- Attach metadata for predicted ETA, filter ETA, heuristic ETA, sigma, pass/fail, violation probability, interval bounds, window bounds, and prune reason.
- Ensure no-filter disables only ETA pruning, not routing or capacity feasibility.
- Ensure soft-penalty keeps candidates but changes objective value.

### Menu Objective And Solver

- Support expected profit, opt-out penalty, ETA risk penalty, and service-guarded expected profit.
- Apply pricing and cost definitions consistently across baselines.
- Use exact enumeration for small candidate sets and greedy forward selection for larger sets.
- Log exact-vs-greedy value, gap, overlap, build time, candidate count, and enumerated menu count.

### Experiment Pipeline

- Define smoke, pilot, and formal study contracts.
- Compare full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, no-filter diagnostic, robust time-window menu, and optional random top-k.
- Use paired replay traces, shared predictor checkpoints, fixed seeds, split IDs, and HGS parameters.
- Emit normalized rows and aggregate summaries with provenance.

### Artifact And Paper Output

- Build robust filtering, exact-greedy, uptake-regime, ETA diagnostics, profit decomposition, and uncertainty/gap summaries.
- Build figures for net-profit gap, opt-out/acceptance, false-negative pruning, home-only menu share, ETA error quantiles, and exact/greedy runtime.
- Emit artifact status with manifest hash, run ID, git marker, checkpoint path/hash, completed/incomplete status, and placeholder flag.
- Produce paper-ready method, experiment, result, limitation, and claim-checklist text.

## Differentiators

- Uncertainty-aware candidate management that prevents hard ETA filters from deleting plausible service bundles.
- Auditable exact-small/greedy-large menu construction rather than opaque heuristic-only comparison.
- Explicit service-quality guardrails around opt-out, walking distance, pickup deviation, capacity risk, and route delay.
- A reproducibility chain from manifest to raw rows to tables/figures to manuscript claims.

## Deferred Enhancements

- Attention-based menu-aware choice/scoring.
- Decision-focused menu regret training.
- Rich distance-band or candidate-type ETA sigma models beyond the global-sigma first version.
- Real passenger preference estimation.
- Many-to-many DRT.

---
*Research note generated: 2026-06-10*
