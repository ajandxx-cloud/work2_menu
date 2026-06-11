---
phase: 06-attention-enhanced-dspo-evidence-pivot
plan: 01
subsystem: algorithm
tags: [dspo, attention, menu-optimization, parser, testing]
requires:
  - phase: 02-core-semantics-and-robust-menu-logic
    provides: safe menu objective, robust ETA diagnostics, and solver paths
provides:
  - deterministic candidate-attention scoring for DSPO_Menu
  - explicit DSPO_original and DSPO_attention runtime knobs
  - focused attention scoring regression tests
affects: [attention-evidence, paired-replay, artifacts]
tech-stack:
  added: []
  patterns: [script-style regression tests, objective-layer deterministic attention]
key-files:
  created:
    - work2_coding/scripts/test_attention_menu_logic.py
  modified:
    - work2_coding/Src/parser.py
    - work2_coding/Src/Algorithms/DSPO_Menu.py
key-decisions:
  - "Attention enters the shared menu objective path used by exact and greedy selection."
  - "DSPO_original remains the parser default with attention disabled."
  - "Deterministic attention uses existing offer fields and metadata only."
patterns-established:
  - "Attention diagnostics are written on offers and summarized in last_policy_diagnostic."
requirements-completed: [ATTN-01, ATTN-02, BEHAV-01]
duration: 20min
completed: 2026-06-11
---

# Phase 06 Plan 01: Attention Scoring Summary

**Deterministic DSPO candidate attention integrated into the shared menu objective with parser knobs and regression coverage**

## Performance

- **Duration:** 20 min
- **Started:** 2026-06-11T18:25:00+08:00
- **Completed:** 2026-06-11T18:45:05+08:00
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Added parser/config knobs for `method_variant`, `attention_enabled`, `attention_mode`, `attention_strength`, and deterministic feature weights.
- Added deterministic attention feature extraction, score delta calculation, per-offer diagnostics, and compact `last_policy_diagnostic` summaries in `DSPO_Menu`.
- Integrated attention deltas into `evaluate_menu()`, the common objective path used by exact and greedy menu selection.
- Added script-style tests proving disabled-attention equivalence, diagnostics, and an attention-driven selection change.

## Task Commits

1. **Tasks 1-3: Parser knobs, attention objective integration, and tests** - `5196d9e` (feat)

**Plan metadata:** pending in this summary commit.

## Files Created/Modified

- `work2_coding/Src/parser.py` - Adds explicit method and attention configuration knobs with original behavior as the default.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Adds deterministic attention scoring, objective deltas, and diagnostics.
- `work2_coding/scripts/test_attention_menu_logic.py` - Covers parser defaults, disabled equivalence, diagnostics, and changed selection.

## Decisions Made

- Attention is implemented at the objective layer rather than in routing, choice semantics, ETA prediction, or cost prediction.
- The future neural mode is represented as a parser/config value, but deterministic scoring is the only implemented Phase 6 behavior.
- Attention diagnostics are emitted even when attention is disabled, while objective deltas stay zero unless enabled.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Existing Phase 6-numbered commits under stale `ooh_code/` paths were inspected and treated as legacy numbering, not as evidence that the current `work2_coding/` attention plan was complete.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` already had uncommitted runtime-support edits before this plan; they were preserved while adding attention behavior.

## Verification

- `cd work2_coding; python scripts/test_attention_menu_logic.py` - PASS
- `cd work2_coding; python scripts/test_robust_menu_logic.py` - PASS
- `cd work2_coding; python scripts/test_menu_runtime_contract.py` - PASS
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` - PASS
- `cd work2_coding; python -m py_compile Src/parser.py Src/Algorithms/DSPO_Menu.py scripts/test_attention_menu_logic.py` - PASS

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for Plan 06-02 to expose `DSPO_original` and `DSPO_attention` through manifests, adapters, normalized rows, and paired replay validation.

---
*Phase: 06-attention-enhanced-dspo-evidence-pivot*
*Completed: 2026-06-11*
