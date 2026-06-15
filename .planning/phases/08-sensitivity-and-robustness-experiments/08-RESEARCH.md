---
phase: 08-sensitivity-and-robustness-experiments
status: complete
researched: 2026-06-15T23:24:48+08:00
timezone: Asia/Shanghai
research_mode: inline
requirements:
  - SENS-01
  - SENS-02
  - SENS-03
---

# Phase 8 Research: Diagnostic Sensitivity And Robustness Experiments

## Research Question

How should Phase 8 add TR-E sensitivity evidence for robust service-menu
optimization while upstream provenance, readiness, artifact, and claim gates
remain unresolved?

## Short Answer

Phase 8 should create a diagnostic/pilot sensitivity suite for the four
must-have dimensions only: `menu_k`, ETA/filter mode, uptake regime, and
opt-out/service guardrail. The suite should be one-factor-at-a-time around the
frozen/default robust-menu settings and should run only after the existing
`phase8_baseline_validation` gate passes.

The phase should produce generated sensitivity rows, diagnostic artifact
tables/figures, and `.planning/results/SENSITIVITY_SUMMARY.md`. Every output
must remain `diagnostic_provisional_blocked` and `claim_ready=false` until
upstream gates explicitly authorize stronger use.

## Boundary Interpretation

Phase 8 is not a gate-cleanup phase and not a final rerun phase. It may run
diagnostic replay, but it must not:

- hand-edit generated rows, tables, or figures;
- use no-filter as a deployable recommendation;
- run nice-to-have dimensions as executable Phase 8 replay;
- tune on final results;
- upgrade abstract, conclusion, or central manuscript claims.

If the prerequisite baseline validation fails, Phase 8 should write a blocked
sensitivity summary and stop before actual sensitivity replay.

## Codebase Findings

### Active Runtime Root

The active runtime root is `work2_coding/`. The older `.planning/codebase/`
documents still reference `ooh_code/`, but current planning and implementation
should cite `work2_coding/` files.

### Existing Gate

`work2_coding/Experiments/studies/phase8_baseline_validation.yaml` already
defines the prerequisite gate comparing:

- `mainline_optimized_mw`
- `phase8_static_flat_markdown`

`work2_coding/Src/baseline_validation.py` validates paired rows, checkpoint
load status, `method_family`, `outside_option_util`, provenance hashes, and
opt-out/home/meeting-point accounting. It opens `phase9_release_gate` only when
the baseline comparison passes, while keeping claim-ready status blocked.

### Manifest System

`work2_coding/Src/experiment_contracts.py` supports extra top-level manifest
metadata and ignores non-argument split metadata. That makes a lightweight
Phase 8 sensitivity contract possible without expanding the parser for every
axis label.

Recommended manifest pattern:

- use `tier: pilot`;
- use `run_mode: diagnostic`;
- use `required_policy_tags: [mainline_optimized_adaptive]`;
- keep one policy tag per sensitivity study;
- encode `sensitivity_axis`, `sensitivity_value`, and `baseline_value` in
  manifest/split metadata;
- use existing parser args for actual mechanism changes.

This keeps replay rows valid and lets a dedicated Phase 8 artifact builder map
rows back to sensitivity axis/value from the manifest snapshot.

### Runtime Knobs

`work2_coding/Src/parser.py` already exposes the required knobs:

- `menu_k`
- `max_candidates`
- `menu_eta_filter_mode`
- `menu_eta_chance_threshold`
- `service_quit_rate_guardrail`
- `menu_optout_guardrail`
- `menu_selection_solver`
- `menu_use_exact_eval`

`work2_coding/Src/Algorithms/DSPO_Menu.py` implements `hard`,
`interval_overlap`, `chance_constraint`, `soft_penalty`, and `none` ETA/filter
modes. Phase 8 should use `hard`, `interval_overlap`, and
`chance_constraint` with threshold `0.25`; `none` remains diagnostic boundary
evidence outside the main deployable comparison.

### Row And Artifact Contracts

`work2_coding/Src/paired_replay.py` already records:

- `menu_k`
- `max_candidates`
- `filter_mode`
- `uptake_regime`
- `checkpoint_load_status`
- `method_family`
- `outside_option_util`
- `accepted_count`
- `count_opted_out`
- `count_accepted_home`
- `count_accepted_meeting_point`
- `menu_build_time`
- `exact_enumerated_menu_count`
- `relative_optimality_gap`
- `menu_overlap_rate`

Guardrail values are not currently first-class row fields, so the Phase 8
summary/artifact builder should read them from `manifest_snapshot.yaml` and
attach them to generated diagnostic tables. This is still generated evidence
because the source is the manifest snapshot plus normalized rows.

`work2_coding/Src/artifact_status.py` already prevents diagnostic runs,
placeholder rows, bad checkpoint rows, and invalid accounting from becoming
claim-ready artifacts.

## Recommended Phase Split

### Plan 1: Sensitivity Manifest Contracts

Create four diagnostic/pilot studies plus one suite:

- `phase8_sensitivity_menu_k.yaml`
- `phase8_sensitivity_eta_filter.yaml`
- `phase8_sensitivity_uptake_regime.yaml`
- `phase8_sensitivity_guardrail.yaml`
- `phase8_sensitivity_must_have.yaml`

Actual replay dimensions:

| Axis | Values | Notes |
| --- | --- | --- |
| `menu_k` | `2`, `3`, `4` | `3` is the center/default. |
| ETA/filter mode | `hard`, `interval_overlap`, `chance_constraint` | Chance threshold fixed at `0.25`. |
| uptake regime | `low`, `medium` | Use existing utility settings only. |
| opt-out/service guardrail | `0.35`, `0.40` | Vary both `service_quit_rate_guardrail` and `menu_optout_guardrail` together. |

Nice-to-have dimensions remain documented but non-executable in Phase 8:
`max_candidates`, fleet/capacity stress, pricing bounds, and price
sensitivity.

### Plan 2: Sensitivity Artifacts And Summary Builder

Add a small Phase 8 sensitivity module and scripts that:

- check the baseline-validation report first;
- load latest suite/member run directories;
- map rows to axis/value using manifest snapshots;
- validate one-factor-at-a-time discipline;
- build generated JSON/CSV/LaTeX/figure artifacts;
- write `.planning/results/SENSITIVITY_SUMMARY.md` as a conditional boundary
  map with source artifact paths and `claim_ready=false`.

### Plan 3: Gated Diagnostic Replay And Closeout

Run the baseline gate. If it passes, run the sensitivity suite actual replay,
build diagnostic artifacts, write the sensitivity summary, and update planning
state. If it fails, write a blocked summary and do not run sensitivity replay.

## Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Phase 8 becomes hidden calibration or p-hacking | Use predeclared values only and one-factor-at-a-time manifests. |
| Nice-to-have axes expand runtime and scope | Keep them contract-only/deferred and test that no executable nice-to-have manifest exists. |
| Baseline gate fails but sensitivity replay still starts | Make the summary builder and run plan block on `PHASE8_BASELINE_VALIDATION.json`. |
| Guardrail axis is ambiguous | Vary both `service_quit_rate_guardrail` and `menu_optout_guardrail`, and record both in artifacts. |
| Diagnostic rows are mistaken for claim-ready evidence | Use `tier: pilot`, `run_mode: diagnostic`, artifact status checks, and summary status `diagnostic_provisional_blocked`. |
| No-filter gets promoted as recommended | Exclude `none` from executable Phase 8 main sensitivity; document it as boundary-only if referenced. |

## Research Complete
