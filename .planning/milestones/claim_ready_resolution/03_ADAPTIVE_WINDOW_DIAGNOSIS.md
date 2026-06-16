# Phase 15 Adaptive Window Diagnosis

Date: 2026-06-16

Status: diagnosis only. Phase 15 inspected existing rows, manifest configuration, policy adapter mapping, time-window code paths, and persisted replay metadata. It did not modify algorithms, regenerate rows, tune parameters, repair gates, regenerate artifacts, or upgrade claims.

## Binding Inputs

This diagnosis treats Phase 13 and Phase 14 outputs as binding. In particular:

- Adaptive-window increment claims are blocked while `mainline_optimized_adaptive` and `mainline_optimized_fixed_window` remain identical across tracked metrics.
- Missing evidence must be reported as unavailable, not inferred.
- Phase 15 prepares evidence for Phase 16 and does not choose Path A, Path B, or Path C.

## Evidence Inspected

- `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv`
- `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv`
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json`
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/manifest_snapshot.yaml`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- `work2_coding/Src/policy_adapters.py`
- `work2_coding/Src/Algorithms/DSPO_Menu.py`

## Finding

The equality between `mainline_optimized_adaptive` and `mainline_optimized_fixed_window` appears to be a code/path implementation issue, with a configuration degeneracy at the policy level. It does not appear to be evidence of true scientific equivalence between adaptive and fixed time windows.

The persisted rows show separate policy labels and separate `time_window_mode` metadata, but the menu-generation and feasibility-filtering code does not implement distinct behavior for `adaptive_window` versus `fixed_window`. In the inspected code path, both modes collapse to "uses a time window" for `m+w+p` products. Only `no_time_window` has distinct behavior.

## Persisted Row Equality

Across the selected formal rows, the optimized adaptive and optimized fixed-window policies are identical across tracked realized performance fields:

| Field group | Observed relation |
|---|---|
| Net profit and cost | Identical `net_profit`, `charge_revenue`, `discount_cost`, `net_price_revenue`, `operational_cost`, `service_time_total`, and `total_cost`. |
| Demand outcomes | Identical `accepted_count`, `served_count`, `count_opted_out`, `count_accepted_home`, `count_accepted_meeting_point`, acceptance rate, opt-out rate, home share, and meeting-point uptake. |
| Menu metadata | Identical `menu_mode`, `product_mode`, `pricing_mode`, `filter_mode`, `menu_selection_solver_effective`, `exact_enumerated_menu_count`, `menu_utilization`, and `choice_entropy`. |
| Fallback metadata | Both use exact menu selection and have no recorded solver fallback reason. |
| Runtime metadata | `menu_build_time` differs only by tiny timing noise and is not a tracked scientific performance metric. |
| Mode metadata | `time_window_mode` differs: fixed rows record `fixed_window`; adaptive rows record `adaptive_window`. |

The tiny timing difference argues against simple row reuse or result copying. The substantive equality is better explained by both policies traversing the same behavioral code path.

## Manifest and Policy Adapter Mapping

The formal policy configuration maps:

- `mainline_optimized_fixed_window` to `menu_mode=optimized_menu`, `product_mode=m+w+p`, `time_window_mode=fixed_window`, `pricing_mode=lambertw`, `filter_mode=interval_overlap`, and `menu_policy=service_guarded_expected_profit`.
- `mainline_optimized_adaptive` to the same settings, except `time_window_mode=adaptive_window`.

The adapter mapping in `work2_coding/Src/policy_adapters.py:280-308` therefore creates a clean metadata contrast but not necessarily a behavioral contrast. The only intended difference reaching the algorithm is `time_window_mode`.

## Time-Window Mode Handling

The inspected `DSPO_Menu` path records `time_window_mode` at initialization and in method metadata (`work2_coding/Src/Algorithms/DSPO_Menu.py:43-58`, `work2_coding/Src/Algorithms/DSPO_Menu.py:178-196`).

The behavioral gate is `_product_uses_window()` (`work2_coding/Src/Algorithms/DSPO_Menu.py:160-163`):

- It returns true when the product uses windows and `time_window_mode != no_time_window`.
- It does not distinguish `fixed_window` from `adaptive_window`.

The downstream window code follows the same pattern:

- `_display_windows(customer)` builds displayed candidate windows from preferred pickup time and window-width settings, without branching on fixed versus adaptive mode (`work2_coding/Src/Algorithms/DSPO_Menu.py:376-383`).
- `_window_for_eta(...)` derives candidate ETA windows from the same display-window list (`work2_coding/Src/Algorithms/DSPO_Menu.py:385-401`).
- `_eta_filter_result(...)` applies the configured ETA filter mode to those windows, without branching on fixed versus adaptive mode (`work2_coding/Src/Algorithms/DSPO_Menu.py:403-470`).
- Utility and scoring include time-window penalties when `_product_uses_window()` is true, again without a fixed/adaptive branch (`work2_coding/Src/Algorithms/DSPO_Menu.py:521-532`, `work2_coding/Src/Algorithms/DSPO_Menu.py:640-652`).

Result: for `m+w+p` policies using a time window, `fixed_window` and `adaptive_window` are behaviorally equivalent in the inspected implementation.

## Generated Window Values

Generated per-offer window values are not available in the persisted formal rows or artifact summaries. The normalized rows do not include selected `window_start`, `window_end`, or `window_center` values. Phase 15 therefore cannot prove equality by comparing persisted generated windows.

The code path nevertheless indicates that both modes call the same display-window generator and filter logic. That is sufficient to diagnose a likely implementation degeneracy, but a later implementation phase would need persisted diagnostics or targeted tests to verify corrected adaptive behavior.

## Feasibility Filtering

Both optimized policies record:

- `filter_mode=interval_overlap`
- `menu_selection_solver_effective=exact`
- empty `solver_fallback_reason`

The feasibility path therefore does not explain the equality as an emergency fallback. It reinforces the implementation finding: the same feasible candidate set and exact optimizer are likely reached because the fixed/adaptive distinction is not behaviorally active.

## Cache or Fallback Behavior

No persisted evidence indicates a cache collision or fallback that overwrote one policy with the other:

- Both policies have distinct `method` strings and distinct `time_window_mode` metadata.
- Both policies record exact solver use.
- Both policies have no recorded fallback reason.
- `menu_build_time` differs slightly, suggesting both rows were evaluated rather than copied wholesale.

Phase 15 cannot rule out all internal memoization effects because candidate-level cache keys are not persisted, but the available evidence points first to the shared implementation path.

## Classification

The equality is best classified as:

- Code/path implementation issue: fixed and adaptive modes are not behaviorally separated in the inspected menu code.
- Configuration degeneracy: the manifest creates a one-field contrast, but the active algorithm treats both values as the same "window enabled" state.
- Missing metric issue, secondary: selected generated window values are not persisted, so artifacts cannot independently demonstrate whether any hidden window variation occurred.

It is not currently supportable as a true scientific equivalence result. Adaptive-window increment claims must remain blocked.

## Phase 16 Implication

Phase 16 should treat adaptive/fixed equality as a likely implementation/configuration blocker, not as evidence that adaptive windows have no scientific value. However, the current formal rows cannot support an adaptive-window value claim. Recoverability would require a later, explicitly authorized implementation/configuration fix and a legitimate final rerun; it cannot be repaired by manuscript wording or metadata schema changes alone.
