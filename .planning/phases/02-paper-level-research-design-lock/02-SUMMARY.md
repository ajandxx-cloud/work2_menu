---
phase: 02-paper-level-research-design-lock
plan: 02
subsystem: paper-design
tags:
  - tr-e
  - service-menu-optimization
  - claim-gates
  - paired-replay
  - mathematical-model
requires:
  - phase: 01-repository-audit-and-state-locking
    provides: active runtime root, state lock, formal evidence blockers, stale path mapping
provides:
  - TR-E paper research design contract
  - service-bundle and outside-option semantics
  - mathematical model skeleton
  - claim-to-evidence matrix
  - table and figure plan
affects:
  - phase-03-formal-rc-evidence-pipeline-repair-and-completion
  - phase-04-rc-result-diagnosis-and-paper-claim-validation
  - manuscript-claim-gating
tech-stack:
  added: []
  patterns:
    - documentation-only design lock before formal evidence
    - strong-claim reserved framing with formal gates
key-files:
  created:
    - .planning/paper/TR_E_RESEARCH_DESIGN.md
  modified:
    - .planning/STATE.md
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
key-decisions:
  - "The V1 paper contribution is dynamic service menu optimization for many-to-one DRT, not attention or pricing-only framing."
  - "Positive manuscript claims remain gated on formal readiness, paired formal rows, artifact status, and claim guard approval."
  - "Outside option is refusal/lost demand and stays separate from accepted home pickup."
  - "No-filter and attention evidence remain diagnostic unless a later gated phase changes scope."
patterns-established:
  - "Claim ladder: strong, conditional, weak-diagnostic, unsupported."
  - "Every planned paper claim maps to comparison policies, metrics, required artifacts, and allowed manuscript use."
requirements-completed:
  - PAPER-01
  - PAPER-02
  - PAPER-03
  - PAPER-04
  - PAPER-05
duration: 0 min
completed: 2026-06-15
---

# Phase 02 Plan 02: Paper-Level Research Design Lock Summary

**TR-E service-menu optimization design contract with model skeleton, claim ladder, evidence gates, and paper table/figure plan**

## Performance

- **Duration:** 0 min recorded by GSD metric command; actual inline execution completed in this session.
- **Started:** 2026-06-15T10:32:33+08:00
- **Completed:** 2026-06-15T10:32:33+08:00
- **Tasks:** 6
- **Files modified:** 1 primary artifact plus GSD tracking files

## Accomplishments

- Created `.planning/paper/TR_E_RESEARCH_DESIGN.md` as the Phase 2 paper-level design contract.
- Defined service bundles as `(meeting point, pickup time window, price)`, with accepted home pickup separated from the outside option.
- Added a mathematical model skeleton covering sets, service bundles, menu variables, MNL probability, expected profit, guardrails, ETA/window feasibility, and exact/greedy solvers.
- Mapped planned paper claims to the seven-tag mainline family, required metrics, required artifacts, and allowed manuscript use.
- Locked table and figure families before formal experiments.
- Preserved non-claim boundaries for attention, no-filter diagnostics, smoke/pilot/status-only evidence, and optional case-study evidence.

## Task Commits

1. **Tasks 1-5: research design contract** - `9359cbc` (`docs(02-02): lock TR-E paper research design`)
2. **Task 6: verification and closeout** - covered by summary and tracker commit

**Plan metadata:** pending in the summary/tracking commit.

## Files Created/Modified

- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - TR-E research design lock covering `PAPER-01` through `PAPER-05` and decisions `D-01` through `D-19`.
- `.planning/phases/02-paper-level-research-design-lock/02-SUMMARY.md` - this execution summary.
- `.planning/STATE.md` - moved Phase 2 toward verification.
- `.planning/REQUIREMENTS.md` - marked `PAPER-01` through `PAPER-05` complete.
- `.planning/ROADMAP.md` - updated by GSD roadmap progress commands.

## Decisions Made

- Kept the central claim as strong-claim reserved rather than currently asserted.
- Treated current smoke, pilot, diagnostic, blocked, placeholder, and status-only outputs as non-claim evidence.
- Defined `mainline_optimized_adaptive` as the primary V1 method but required paired formal rows and claim-ready artifacts before positive manuscript use.
- Kept attention V2/diagnostic only and no-filter diagnostic/upper-bound/stress-test only.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

The repository has a large pre-existing dirty worktree from earlier work. Phase 2 edits were kept scoped to the paper design artifact and GSD tracking files; unrelated modified/deleted/untracked files were not reverted or cleaned.

## Verification

- `DESIGN_CHECK_OK`: confirmed `PAPER-01` through `PAPER-05`, `D-01` through `D-19`, all seven mainline tags, mathematical model skeleton, claim-to-evidence map, table/figure plan, attention boundary, no-filter boundary, outside option, and accepted home semantics.
- `IMPORT_OK`: ran from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

No formal replay, checkpoint training, artifact regeneration, generated-row edit, or manuscript claim upgrade occurred.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 3 can use `.planning/paper/TR_E_RESEARCH_DESIGN.md` as the paper claim and evidence contract while inspecting `formal_robust_menu.yaml`, checkpoint readiness, formal replay rows, artifact status, and claim guard outputs.

---
*Phase: 02-paper-level-research-design-lock*
*Completed: 2026-06-15*
