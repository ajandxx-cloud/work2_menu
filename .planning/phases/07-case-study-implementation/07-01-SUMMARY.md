---
phase: 07-case-study-implementation
plan: 01
subsystem: planning-data-contracts
tags:
  - case-study
  - semi-real
  - simulated-demand
  - claim-gates
requires:
  - phase: 06-real-or-semi-real-case-study-feasibility-audit
    provides: approved semi-real route with blocked execution gate
provides:
  - planning-side semi-real case-study source contracts
  - non-executable case manifest draft with seven mainline tags
  - simulated-demand and claim-boundary placeholders
affects:
  - phase-07-validator
  - phase-08-sensitivity
  - manuscript-claim-gates
tech-stack:
  added: []
  patterns:
    - planning-side contract pack with blocker fields
    - prohibitive scaffold language for gated case evidence
key-files:
  created:
    - .planning/data/case_studies/README.md
    - .planning/data/case_studies/source_contracts.yaml
    - .planning/data/case_studies/route_selection_scorecard.yaml
    - .planning/data/case_studies/simulated_demand_protocol.md
    - .planning/data/case_studies/case_manifest_draft.yaml
    - .planning/data/case_studies/reduced_family_gate.md
    - .planning/data/case_studies/claim_boundary_placeholders.md
  modified: []
key-decisions:
  - "Keep Phase 7 outputs planning-side and non-executable until provenance/readiness/artifact/claim gates pass."
  - "Preserve all seven mainline tags in the case manifest draft; no reduced family is applied in Phase 7."
patterns-established:
  - "Every case scaffold artifact carries scaffolding_only_blocked_execution and blocker fields."
  - "Future route selection is governed by predeclared source-quality criteria, not experiment outcomes."
requirements-completed:
  - CASE-03
  - CASE-05
duration: 12 min
completed: 2026-06-15
---

# Phase 7 Plan 1: Planning-Side Case Study Contract Pack Summary

**Planning-side semi-real case contracts with blocked execution fields, seven-tag manifest scaffolding, and prohibitive claim boundaries**

## Performance

- **Duration:** 12 min
- **Started:** 2026-06-15T22:19:30+08:00
- **Completed:** 2026-06-15T22:31:30+08:00
- **Tasks:** 6
- **Files modified:** 7

## Accomplishments

- Created `.planning/data/case_studies/` as the contract root for the semi-real case scaffold.
- Added dual-route source contracts for public OSM/open-network and Yanjiao/Beijing motivated routes, with reproducibility placeholders and blocker fields.
- Added a non-executable planning-side case manifest draft that preserves all seven formal mainline tags and paired-field vocabulary.
- Added simulated-demand protocol, reduced-family gate, and prohibitive claim-boundary placeholders without creating runtime YAML or result artifacts.

## Task Commits

Each task was committed atomically:

1. **Task 1: Create case-study contract root** - `c326b49` (docs)
2. **Task 2: Define dual-route source contracts** - `b29b6a3` (docs)
3. **Task 3: Predeclare route selection scoring** - `e33f33a` (docs)
4. **Task 4: Write simulated demand and choice protocol placeholder** - `1e7b269` (docs)
5. **Task 5: Draft planning-side case manifest** - `f071e66` (docs)
6. **Task 6: Define reduced-family gate and claim boundaries** - `bf35133` (docs)

## Files Created/Modified

- `.planning/data/case_studies/README.md` - File map and scaffold-only boundary.
- `.planning/data/case_studies/source_contracts.yaml` - Dual-route source metadata and blocker contracts.
- `.planning/data/case_studies/route_selection_scorecard.yaml` - Predeclared route-selection criteria and outcome-selection prohibition.
- `.planning/data/case_studies/simulated_demand_protocol.md` - Placeholder-only simulated demand and simulated choice protocol.
- `.planning/data/case_studies/case_manifest_draft.yaml` - Planning-side manifest draft with seven mainline tags and paired fields.
- `.planning/data/case_studies/reduced_family_gate.md` - Future gate template for any pre-outcome policy-family reduction.
- `.planning/data/case_studies/claim_boundary_placeholders.md` - Prohibitive future manuscript and artifact labels only.

## Decisions Made

- Used placeholder source/cache/hash fields rather than fetching or building external data, preserving the Phase 7 no-execution boundary.
- Kept route IDs unique in `source_contracts.yaml` so validator checks can distinguish route entries from cache-path text.
- Deferred requirement-status closeout to Plan 2, where the validator and planning documents close Phase 7 as scaffold-only.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Initial source cache placeholders repeated route IDs, which would have weakened the "route IDs appear exactly once" acceptance check. The placeholders were renamed before commit and verification passed.

## Verification

- `Test-Path .planning/data/case_studies/README.md` returned `True`.
- Required Wave 1 files all returned `True`; `Test-Path work2_coding/Experiments/studies/case_manifest_draft.yaml` returned `False`.
- `Select-String` checks found required blocker fields, status labels, seven mainline tags, paired fields, reduced-family fields, and prohibitive claim-boundary language.
- Route IDs in `source_contracts.yaml` each appeared exactly once after cleanup.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Wave 2 can build the planning-side validator against the contract pack. Case execution, runtime manifest creation, normalized rows, result artifacts, and manuscript claim upgrades remain blocked.

## Self-Check: PASSED

---
*Phase: 07-case-study-implementation*
*Completed: 2026-06-15*
