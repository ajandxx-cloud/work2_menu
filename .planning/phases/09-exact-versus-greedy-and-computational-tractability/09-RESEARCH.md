---
phase: 09
phase_name: Exact Versus Greedy And Computational Tractability
status: research-complete
generated: 2026-06-16T10:09:40+08:00
timezone: Asia/Shanghai
requirements:
  - COMP-01
  - COMP-02
source_context: .planning/phases/09-exact-versus-greedy-and-computational-tractability/09-CONTEXT.md
---

# Phase 9 Research: Exact Versus Greedy And Computational Tractability

## Research Question

What must be planned so Phase 9 can credibly show whether the online service
menu solver is computationally usable, while preserving paired replay fairness
and the current diagnostic/claim-blocked evidence boundary?

## Short Answer

Phase 9 should not invent a new solver. The live `work2_coding/` runtime
already exposes the important exact/greedy mechanics:

- `DSPO_Menu.py` can select exact menus when candidate count is at or below
  `menu_exact_threshold`.
- The same code falls back to greedy selection with
  `solver_fallback_reason=above_exact_threshold` when exact is requested above
  the threshold.
- Solver diagnostics already include effective solver, enumerated menu count,
  relative optimality gap, menu overlap, and build time surfaces.
- `study_execution.py` aggregates these diagnostics into normalized rows.
- `paired_replay.py` already has normalized-row-v2 fields for
  `menu_selection_solver_effective`, `solver_fallback_reason`,
  `exact_enumerated_menu_count`, `relative_optimality_gap`,
  `menu_overlap_rate`, and `menu_build_time`.
- `artifact_builder.py` has a thin existing exact/greedy table and runtime
  figure, but it is too policy-oriented and too sparse for Phase 9's required
  candidate-count, enumerated-count, overlap, fallback, and source-metadata
  table.

The implementation plan should therefore focus on manifesting the exact-greedy
diagnostic comparison, tightening row/report fields where needed, and adding a
Phase 9 artifact/summary builder.

## Live Code Findings

### Solver Selection

`work2_coding/Src/Algorithms/DSPO_Menu.py` is the active solver surface. The
menu constructor reads:

- `max_candidates`
- `menu_k`
- `menu_exact_threshold`
- `menu_exact_gap_threshold`
- `menu_selection_solver`
- `menu_use_exact_eval`

Exact selection uses `_select_menu_exact(...)`, enumerates feasible subsets up
to `menu_k`, and records `exact_enumerated_menu_count`. Greedy selection uses
`_select_menu_greedy(...)`, filling menu slots by marginal objective gain.

For the generic optimized menu path, requesting `menu_selection_solver=exact`
above `menu_exact_threshold` falls back to greedy and records
`solver_fallback_reason=above_exact_threshold`. This matches the Phase 9
context decision to show large-candidate exact infeasibility through the
existing threshold-triggered fallback rather than forcing a timeout.

### Diagnostics And Row Schema

`work2_coding/Src/study_execution.py` collects:

- `menu_build_time`
- `relative_optimality_gap`
- `menu_overlap_rate`
- `exact_enumerated_menu_count`
- `menu_selection_solver_effective`
- `solver_fallback_reason`

`work2_coding/Src/paired_replay.py` writes these into normalized rows. One gap
remains: `DSPO_Menu.py` has `solver_candidate_count` and
`exact_gap_candidate_count` in diagnostics, but the current normalized row
schema does not persist an actual observed solver candidate count. Phase 9 can
either treat `max_candidates` as the controlled candidate-count field or add a
row field such as `solver_candidate_count`. Because the Phase 9 table must
report candidate count, the safer plan is to add and test the explicit
`solver_candidate_count` field while retaining `max_candidates` as the
experimental setting.

### Existing Status Gate

The existing `phase9_dspo_family_validation` report has already passed as a
status gate:

- report: `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.md`
- JSON: `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.json`
- status: `passed`
- `claim_ready=false`

Phase 9 should cite or lightly check this status, but should not rerun the full
DSPO family validation. It is not the exact-versus-greedy tractability result.

### Manifest Strategy

Arbitrary solver-scale names cannot be introduced as `policy_tag` without
adding policy adapters. The least invasive tractability manifest should use the
existing `mainline_optimized_adaptive` policy tag and encode the three
solver-scale variants as split metadata plus `args_overrides`.

The required 15-row design is:

- 5 paired split surfaces, reusing the Phase 8/Phase 9 low and medium uptake
  split IDs/seeds.
- 3 solver-scale variants per paired split:
  - small exact: `max_candidates=8`, `menu_exact_threshold=8`,
    `menu_selection_solver=exact`
  - large fallback/greedy: `max_candidates=12`, `menu_exact_threshold=8`,
    `menu_selection_solver=exact`
  - large fallback/greedy: `max_candidates=16`, `menu_exact_threshold=8`,
    `menu_selection_solver=exact`
- fixed `menu_k=3`
- formal-like paired replay with loaded checkpoint requirement
- diagnostic output status and `claim_ready=false`

For large variants, requesting exact above threshold is intentional. The
effective solver should be greedy and the row/report should show
`solver_fallback_reason=above_exact_threshold`.

## Implementation Risks

| Risk | Impact | Planning Mitigation |
| --- | --- | --- |
| Large variants silently run exact instead of fallback | Runtime can become too expensive or lose the intended infeasibility signal | Contract tests assert `max_candidates > menu_exact_threshold` for large variants and expected fallback fields in synthetic rows/report tests. |
| Candidate count is only implied by `max_candidates` | Required table may be too weak for paper review | Add or preserve `solver_candidate_count` in row/report outputs; still report `max_candidates` as setting. |
| Existing exact-greedy artifact table is too thin | Phase 9 cannot satisfy COMP-01 | Add Phase 9-specific artifact/summary tooling with candidate count, enumerated count, runtime, gap, overlap, fallback/status, source metadata. |
| Diagnostic output is mistaken for claim-ready evidence | Manuscript overclaims while blockers remain | Every manifest, artifact status, and planning summary preserves `claim_ready=false` and blocked/provisional reasons. |
| Paired fairness drifts across solver-scale variants | Gap/runtime comparisons become confounded | Tests enforce shared seed, data seeds, checkpoint, utility settings, pricing, HGS, and `menu_k` across the three variants in a paired group. |

## Validation Architecture

Phase 9 validation should be script-style and contract-first:

1. Manifest tests validate the 15-row design, known policy tag use, paired
   fairness, fixed `menu_k=3`, small exact settings, large fallback settings,
   loaded checkpoint requirement, and diagnostic claim boundary.
2. Runtime contract tests validate that exact-above-threshold falls back to
   greedy with `above_exact_threshold` and that candidate-count diagnostics are
   persisted.
3. Artifact/summary tests use synthetic normalized rows to prove the Phase 9
   builder emits candidate count, enumerated count, build time, gap, overlap,
   fallback/status, source paths, and `claim_ready=false`.
4. Closeout checks run import smoke plus focused Phase 9 tests and relevant
   existing replay/artifact/fairness tests.

Recommended commands from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_phase9_exact_greedy_contracts.py
python scripts/test_phase9_tractability_summary.py
python scripts/test_robust_menu_logic.py
python scripts/test_paired_replay_contract.py
python scripts/test_policy_fairness_contract.py
python scripts/test_artifact_builder.py
```

## Planning Implication

Use three plans:

1. Add the exact-greedy tractability manifest and contract tests.
2. Add Phase 9 tractability artifact and summary tooling.
3. Run the gated diagnostic replay, build generated artifacts and
   `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`, then update
   planning state without upgrading manuscript claims.

## RESEARCH COMPLETE
