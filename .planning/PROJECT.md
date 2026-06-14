# Work2 Robust Time-Window Service Menu Optimization

## What This Is

This project builds the V1 mainline evidence pipeline for robust time-window
service menu optimization in many-to-one DRT using the active `work2_coding/`
runtime.

## Core Value

Produce defensible, paired-replay evidence for whether optimized service menus
over `m`, `m+w`, and `m+w+p` products improve RC outcomes over no-menu,
fixed-menu, random-menu, and fixed-window baselines.

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

### Active

- [ ] Preserve formal checkpoint provenance and dependency snapshots before any
  formal rows are treated as claim-ready.

### Out of Scope

- Attention-based choice or scoring for V1.
- Treating no-filter diagnostics as formal ranking evidence.
- Hand-editing generated result rows, tables, figures, or manuscript claims.
- Creating a parallel `ooh_code/` runtime root.

## Context

The active runtime lives in `work2_coding/`. Existing `.planning/codebase/`
documents still contain many `ooh_code/` references; use
`.planning/repository_audit.md` to map stale paths to current `work2_coding/`
equivalents.

The current V1 mainline policy family is:

- `mainline_no_menu`
- `mainline_fixed_menu`
- `mainline_random_menu`
- `mainline_optimized_m`
- `mainline_optimized_mw`
- `mainline_optimized_fixed_window`
- `mainline_optimized_adaptive`

## Constraints

- Use `work2_coding/` as the runtime root.
- Preserve paired replay fairness across policy comparisons.
- Keep opt-out accounting separate from accepted home pickup.
- Keep checkpoint load status explicit in result metadata.
- Exclude diagnostic, failed, blocked, placeholder-only, no-filter-only, and
  bad-checkpoint rows from formal claims.
- Do not hand-edit generated paper artifacts.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Use `work2_coding/` as runtime root | Current imports and smoke runs pass there; `ooh_code/` maps are stale. | Validated |
| Use normalized-row-v2 | V1 needs product/time-window/menu/pricing/status/provenance fields. | Validated |
| Keep seven mainline tags | Separates menu baselines, product ablations, and fixed/adaptive windows. | Validated |
| Require checkpoint provenance for formal evidence | Prevents random or incompatible weights from becoming claim evidence. | Active |
| Require passed readiness JSON for formal claim-ready artifacts | Keeps dependency snapshot, clean git, checkpoint hash, and manifest hash checks explicit before formal claims. | Validated |
| Keep attention out of V1 | Attention artifacts are diagnostic/V2 only. | Active |

## Evolution

Update this document only when the Work2 V1 scope changes or a phase is
verified.

---
*Last updated: 2026-06-14 after Phase 5 readiness gate verification*
