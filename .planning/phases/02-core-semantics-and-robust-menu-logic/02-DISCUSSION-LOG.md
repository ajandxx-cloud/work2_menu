# Phase 2: Core Semantics And Robust Menu Logic - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-11
**Phase:** 2-Core Semantics And Robust Menu Logic
**Areas discussed:** Menu runtime minimum activation boundary, Opt-out semantics, Checkpoint load status strictness, Robust ETA filter and no-filter boundary, Menu objective and solver priority semantics

---

## Menu Runtime Minimum Activation Boundary

| Question | Options Considered | User's Choice |
|----------|--------------------|---------------|
| How far should Phase 2 activate `DSPO_Menu`? | 1A Minimal activation; 1B Can generate a menu; 1C Can run a short episode | 1A |
| How should missing `DSPO_Menu` dependencies be handled? | 2A Fix only real gaps; 2B Also normalize contract/metadata; 2C Compatibility wrapper | 2A |
| How should parser/config expose menu parameters? | 3A Explicit complete CLI; 3B Experiment config object first; 3C Minimal CLI | 3A |
| What menu runtime acceptance test should Phase 2 target? | 4A Import plus parser contract; 4B Constructor smoke; 4C Menu action smoke; 4D Short episode smoke | 4A |

**Notes:** User chose minimal activation, minimum dependency repair, explicit parser flags, and import/parser contract as the Phase 2 acceptance line.

---

## Opt-Out Semantics

| Question | Options Considered | User's Choice |
|----------|--------------------|---------------|
| How should opted-out be represented in the simulator? | 1A Independent outcome string; 1B Structured choice result; 1C Minimal compatible metadata | 1B |
| How should opted-out requests affect route and service state? | 2A Completely outside route/service; 2B Demand log only; 2C Keep penalty cost | 2B |
| How much compatibility should old algorithms retain? | 3A Strict interface change; 3B Compatible legacy tuple; 3C Dual adapter | 3C |
| What opt-out acceptance tests should Phase 2 include? | 4A Forced opt-out state test; 4B Three-outcome state tests; 4C Metric tests; 4D All of A+B+C | 4D |

**Notes:** User chose structured choice results, separate opt-out logging, no route/service mutation for opted-out demand, and dual compatibility during migration.

---

## Checkpoint Load Status Strictness

| Question | Options Considered | User's Choice |
|----------|--------------------|---------------|
| What should happen when a shared predictor checkpoint load fails? | 1A Fail closed; 1B Warn plus random fallback; 1C Distinguish by run mode | 1C |
| What checkpoint metadata is required in rows/results? | 2A Basic status; 2B Traceable status; 2C Formal provenance | 2C |
| When are intentional mismatch or random init allowed? | 3A Never allowed; 3B Diagnostic only; 3C Allowed as ablation | 3B |
| What checkpoint tests should Phase 2 include? | 4A Load success/failure tests; 4B Hash/provenance tests; 4C Intentional mismatch tests; 4D All of A+B+C | 4D |

**Notes:** User chose formal/pilot fail-closed behavior, diagnostic-only fallback, and full provenance metadata.

---

## Robust ETA Filter And No-Filter Boundary

| Question | Options Considered | User's Choice |
|----------|--------------------|---------------|
| Which ETA filter modes must Phase 2 fully implement? | 1A Full required mode list; 1B Core robust subset; 1C Minimal verifiable subset | 1B |
| What is the boundary of none/no-filter? | 2A Disable ETA pruning only; 2B Display all candidates; 2C Dual mode | 2C |
| What candidate-level ETA diagnostics are required? | 3A Basic diagnostics; 3B Robust diagnostics; 3C Audit diagnostics | 3C |
| What should `soft_penalty` mean? | 4A Never prune; 4B Weak prune plus penalty; 4C Policy-dependent | 4A |
| How should initial ETA sigma/calibration work? | 5A Global sigma; 5B Distance-segmented sigma; 5C Oracle/empirical first | 5A |

**Notes:** User chose a core robust mode subset, separated `none` from wider diagnostics, required audit-grade candidate metadata, and kept soft-penalty non-pruning.

---

## Menu Objective And Solver Priority Semantics

| Question | Options Considered | User's Choice |
|----------|--------------------|---------------|
| How should objective priorities be organized? | 1A Expected profit dominant; 1B Service guardrail first; 1C Policy-family specific | 1C |
| What happens when the highest-profit menu has excessive predicted opt-out? | 2A Hard block; 2B Penalty only; 2C Fallback | 2C |
| How should exact-small and greedy-large selection switch? | 3A Fixed threshold; 3B Policy-aware threshold; 3C Time-budget fallback | 3C |
| How should exact-vs-greedy diagnostics be recorded? | 4A Exact only; 4B Sampled gap diagnostics; 4C Formal full diagnostics | 4C |
| Should Phase 2 decide the final recommended policy? | 5A Do not decide; 5B Pick service_guarded as main; 5C Dual mainline candidates | 5C |
| What objective/solver tests should Phase 2 include? | 6A Small menu ordering tests; 6B Solver switch tests; 6C Diagnostic field tests; 6D All of A+B+C | 6D |

**Notes:** User chose dual policy-family semantics, guardrail fallback with reason metadata, threshold plus time-budget fallback, and full solver diagnostics.

---

## The Agent's Discretion

- Choose exact helper names and metadata grouping while preserving the locked semantics.
- Sequence Phase 2 implementation and tests in the safest order.

## Deferred Ideas

- Distance-band ETA sigma calibration.
- Formal experiment contracts and final policy selection.
- Artifact generation, manuscript claim language, and attention-based choice/scoring.
