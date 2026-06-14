# Work2 TR-C Paper Rewriting and Experiment Rebuild

## What This Is

This project is a GSD-managed research workflow for a Transportation Research
Part C manuscript on behavior-aware service-menu optimization in many-to-one
demand-responsive transit. The active runtime remains `work2_coding/`, and the
new milestone turns the completed V1 robust-menu evidence pipeline into a
reviewer-ready paper and experiment rebuild plan centered on RC data.

## Core Value

Produce a defensible TR-C manuscript whose DSPO, DSPO_PLUS, static-pricing, and
no-pricing comparisons are reproducible, behaviorally coherent, and gated before
any empirical superiority claim is made.

## Current Milestone: v1.1 Work2_TR_PartC_Paper_Rewriting_and_Experiment_Rebuild_RC

**Goal:** Rebuild the paper and experiment plan around TR-C expectations while
preserving strict evidence gates for DSPO/DSPO_PLUS, menu, time-window, pricing,
and passenger-choice claims.

**Target features:**
- Restructure the LaTeX manuscript into an Elsevier double-column TR-C format.
- Audit the DSPO/DSPO_PLUS/menu/time-window code and RC dataset pipeline before
  algorithm or experiment behavior changes.
- Repair model and experiment inconsistencies around MNL choice, utility terms,
  pricing modes, and opt-out accounting.
- Validate no-pricing, static-pricing, DSPO, and DSPO_PLUS baselines under paired
  replay before formal manuscript claims.
- Add gated ablation and reviewer-risk sections for time windows, menu expansion,
  and the DSPO-to-DSPO_PLUS gap.

## Requirements

### Validated

- [x] Confirm `work2_coding/` as the active importable runtime root.
- [x] Audit stale `ooh_code/` codebase maps and document safe path mappings.
- [x] Define explicit service product, product-mode, time-window-mode,
  menu-mode, pricing-mode, row-v2, and artifact eligibility contracts.
- [x] Migrate `work2_robust_menu` smoke, pilot, and formal manifests to the
  seven-tag V1 mainline family.
- [x] Verify smoke actual replay for all seven mainline policies across
  `menu_k={1,2,3,5}`.
- [x] Make artifact building mainline-aware for normalized-row-v2 outputs.
- [x] Add claim guards for the seven-tag mainline family.
- [x] Build mirrored artifact bundles and manuscript-facing tables/figures from
  regenerated outputs.
- [x] Implement formal readiness preflight, dependency snapshot reporting, and
  formal claim-ready artifact gates.
- [x] Audit current Work2 DSPO/menu/time-window/pricing/RC/readiness/artifact
  surfaces before model or experiment behavior changes.
- [x] Repair MNL outside-option, DSPO/DSPO_PLUS method-family, and
  opt-out/home/meeting-point accounting contracts across rows, artifact gates,
  and manuscript definitions.
- [x] Validate no-pricing and static-pricing baselines under paired replay before
  DSPO or DSPO_PLUS ladder claims are advanced.

### Active

- [ ] Rebuild the main manuscript in Elsevier `cas-dc` double-column format.
- [ ] Keep current non-claim-ready artifact status explicit until checkpoint and
  formal evidence gates pass.
- [ ] Preserve paired replay fairness across all policy comparisons.
- [ ] Validate the RC-centered DSPO/DSPO_PLUS ladder before writing ranking
  claims.
- [ ] Add reviewer-facing risk analysis covering novelty, modeling weakness,
  experiment weakness, and acceptance probability.

### Out of Scope

- Attention-based choice or scoring for this milestone's v1 paper claims.
- Treating no-filter diagnostics as formal ranking evidence.
- Hand-editing generated result rows, generated tables, generated figures, or
  formal claim outputs.
- Creating a parallel `ooh_code/` runtime root.
- Inventing experiment results or asserting the target ranking before the
  required gate passes.
- Introducing a new RL algorithm or otherwise changing the algorithm family
  beyond the current DSPO/DSPO_PLUS/menu-time-window scope.

## Context

The active runtime lives in `work2_coding/`. Existing `.planning/codebase/`
documents contain stale `ooh_code/` references and must be interpreted through
`.planning/repository_audit.md` and the current `work2_coding/` filesystem.

The previous milestone completed the V1 robust-menu pipeline and formal
readiness gates, but real formal readiness still blocked on missing formal
checkpoint provenance and local dirty-git provenance. The current artifact
bundle `work2_coding/artifacts/work2_robust_menu/` reports blocked/non-claim-ready
status, so the manuscript may describe implemented methods, diagnostics, and
required gates but must not claim empirical DSPO_PLUS dominance until the
formal evidence ladder passes.

Phase 6 completed the code and experiment audit. The current factual policy
classification remains the seven-tag mainline robust-menu family, attention
tags remain V2/diagnostic, static pricing and DSPO_PLUS are downstream gaps, and
formal claim readiness remains blocked by `dirty_git` despite loaded checkpoint
and dependency snapshot provenance.

Phase 8 completed paired baseline validation for no-pricing and static-pricing
baselines. Baseline execution passed and Phase 9 may proceed, but claim-ready
ranking artifacts remain gated by formal provenance and downstream DSPO /
DSPO_PLUS validation.

Phase 9 completed paired DSPO validation for `dspo_clip` and `dspo_wide` across
the five Phase 8-equivalent splits. The DSPO validation gate is open, but
`claim_ready=false` remains explicit and no ranking or DSPO_PLUS claim is
unlocked.

The TR-C manuscript target structure is:
Introduction, Literature Review, Problem Formulation, Methodology, Experimental
Design, Results, Ablation Study, Conclusion, plus reviewer-risk and GSD
execution-report appendices when useful.

## Constraints

- **Runtime root:** Use `work2_coding/` for Python checks and artifact inputs.
- **Manuscript format:** Use Elsevier CAS double-column (`cas-dc`) format for
  the main LaTeX manuscript.
- **Evidence integrity:** Preserve paired replay fairness across policy
  comparisons.
- **Behavior accounting:** Keep opt-out separate from accepted home pickup.
- **Checkpoint provenance:** Keep checkpoint load status explicit in result
  metadata and manuscript status language.
- **Claim gates:** Exclude diagnostic, failed, blocked, placeholder-only,
  no-filter-only, contract-only, and bad-checkpoint rows from formal claims.
- **Result integrity:** Do not hand-edit generated result rows, tables, figures,
  or claim-ready artifacts.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Use `work2_coding/` as runtime root | Current imports and smoke runs passed there; `ooh_code/` maps are stale. | Validated |
| Use normalized-row-v2 | V1 needs product/time-window/menu/pricing/status/provenance fields. | Validated |
| Keep seven mainline tags | Separates menu baselines, product ablations, and fixed/adaptive windows. | Validated |
| Require checkpoint provenance for formal evidence | Prevents random or incompatible weights from becoming claim evidence. | Active |
| Require passed readiness JSON for formal claim-ready artifacts | Keeps dependency snapshot, checkpoint hash, manifest hash, and artifact gates explicit. | Validated |
| Keep attention out of v1 paper claims | Attention artifacts are diagnostic/V2 only. | Active |
| Use Elsevier `cas-dc` for the manuscript | The user requested Elsevier double-column format for the TR-C paper rewrite. | Active |
| Treat DSPO_PLUS ranking as a gate, not an assumption | The target ranking must be verified, not written into the paper as fact before evidence passes. | Active |
| Treat Phase 8 baseline validation separately from claim-ready artifacts | Baseline execution can pass while formal ranking artifacts remain blocked by provenance gates. | Validated |

## Evolution

Update this document only when the Work2 paper-rewrite scope changes or a phase
is verified.

---
*Last updated: 2026-06-14 after Phase 9 DSPO family validation*
