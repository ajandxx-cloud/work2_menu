# Pitfalls Research

## Path Drift

**Risk:** Existing planning docs mention `ooh_code/`, but current filesystem shows `work2_coding/`.

**Warning signs:** New files appear under a new root; import commands use stale paths; roadmap tasks refer to scripts that do not exist.

**Prevention:** Phase 1 must identify active runtime root and produce a patch plan before algorithm edits.

## Opt-Out Pollution

**Risk:** Outside-option choices may be represented as home fallback offers and accidentally enter route/service accounting.

**Warning signs:** Opt-out increases home service counts, route data changes after forced outside choice, or service cost changes on opt-out.

**Prevention:** Add explicit outcome states and deterministic opt-out tests before using results for claims.

## Silent Random Checkpoints

**Risk:** Predictor load failure can leave randomly initialized models in formal comparisons.

**Warning signs:** Row metadata has checkpoint paths but no load status; incompatible model architectures compare as if frozen.

**Prevention:** Add `checkpoint_load_status`, fail closed for shared predictor loading, and hash checkpoint files in formal metadata.

## Unfair Policy Comparisons

**Risk:** Policies differ by trace, seed, checkpoint, routing parameters, pricing mode, or uptake regime.

**Warning signs:** Results cannot be paired by seed/split/trace; manifests omit checkpoint and HGS parameters.

**Prevention:** Build paired replay protocol and normalized row schema before formal studies.

## Degenerate Choice Regime

**Risk:** Opt-out is so high or non-home uptake so low that menu design has little behavioral content.

**Warning signs:** Acceptance approaches zero, non-home acceptance approaches zero, or home-only menu share dominates.

**Prevention:** Include low/medium/high uptake regimes and interpret robust menu value conditional on behaviorally meaningful regimes.

## Exact Enumeration Explosion

**Risk:** Exact menu enumeration becomes combinatorial and blocks experiments.

**Warning signs:** Build time grows sharply with candidate count; smoke studies stall.

**Prevention:** Keep exact thresholds low; use greedy forward for large sets; log exact-vs-greedy gaps where feasible.

## Placeholder Artifacts

**Risk:** Incomplete or placeholder rows enter paper-ready outputs.

**Warning signs:** Tables lack source run IDs, placeholder flags are missing, or formal outputs appear without raw run provenance.

**Prevention:** Add artifact status files and block formal claims when placeholder status is true.

---
*Research note generated: 2026-06-10*
