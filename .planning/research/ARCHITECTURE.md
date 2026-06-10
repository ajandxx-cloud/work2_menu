# Architecture Research

## Target Architecture

The project should keep a narrow vertical pipeline:

1. Runtime audit and smoke import.
2. Simulator choice/accounting correctness.
3. Robust candidate filtering and menu objective.
4. Experiment contract and paired replay runner.
5. Artifact builder and manuscript-ready evidence.

## Proposed Data Flow

```text
Passenger request
  -> candidate meeting points and home bundle
  -> service bundles with pickup windows and prices
  -> feasibility filters: routing/capacity plus ETA policy
  -> displayed menu selection: exact-small or greedy-large
  -> MNL choice with outside option
  -> simulator state transition and route/cost accounting
  -> normalized row metrics
  -> aggregate summaries, tables, figures, and claim checklist
```

## Module Boundaries

| Boundary | Preferred Location | Notes |
|----------|--------------------|-------|
| Runtime audit | `.planning` notes plus smoke commands | Phase 1 should record active root and runner status |
| ETA filtering | `work2_coding/Src/Algorithms/DSPO_Menu.py` or a helper imported by it | Existing `_choose_display_window` already contains ETA filter logic |
| Menu objective | `work2_coding/Src/Algorithms/DSPO_Menu.py` | Existing `evaluate_menu`, exact, greedy, and redesigned policy functions should be reused |
| Opt-out transition | `work2_coding/Environments/OOH/customerchoice.py` and `Parcelpoint_py.py` | Choice outcome and simulator mutation must be separated |
| Metrics | Existing runner or new experiment runner | Metrics must include policy, seed, split, trace, checkpoint, filter mode, and menu settings |
| Artifacts | New or existing artifact script | Formal artifacts must not use placeholder rows for claims |

## Build Order

1. Audit the active root, import status, runner scripts, policies, and current risk surface.
2. Repair outcome semantics and checkpoint visibility.
3. Implement robust filters and robust objective metadata.
4. Add smoke tests and manifest/contract tests.
5. Add experiment manifests and normalized output schema.
6. Run smoke/pilot/formal evidence.
7. Generate artifacts and paper-ready summaries.

## Architecture Constraints

- Do not duplicate an `ooh_code/` root if `work2_coding/` is the real root.
- Keep route realization in Hygese-backed simulator utilities.
- Keep passenger choice semantics stable except for the explicit opt-out accounting repair.
- Keep new diagnostics in metadata fields consumed by normalized rows.
- Use exact enumeration only under configured thresholds.

---
*Research note generated: 2026-06-10*
