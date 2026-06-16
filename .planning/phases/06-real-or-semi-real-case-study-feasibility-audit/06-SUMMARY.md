---
phase: 06-real-or-semi-real-case-study-feasibility-audit
plan: 06
subsystem: research-planning
tags: [case-study, semi-real, osm, osrm, gtfs, claim-gates]
requires:
  - phase: 05-calibration-and-robustness-without-p-hacking
    provides: calibration/final gate status and blocked final-rerun boundary
provides:
  - Semi-real case-study feasibility decision
  - Source audit and minimum semi-real contract
  - Phase 7 scaffolding-only gate before upstream cleanup
affects: [phase-7-case-study-implementation, manuscript-claims, artifact-gates]
tech-stack:
  added: []
  patterns:
    - Gate-aware semi-real case-study approval
    - Mandatory simulated-demand and simulated-choice labeling
key-files:
  created:
    - .planning/data/CASE_STUDY_FEASIBILITY.md
    - work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md
    - work2_coding/outputs/phase6_audit/PHASE6_AUDIT.json
    - .planning/phases/06-real-or-semi-real-case-study-feasibility-audit/06-VERIFICATION.md
  modified:
    - .planning/PROJECT.md
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - .planning/STATE.md
key-decisions:
  - "Decision: add semi-real case, approved_blocked_pending_gate_cleanup."
  - "Default Phase 7 route: public OSM/open-network data unless Yanjiao/Beijing sources can be documented with equal reproducibility."
  - "Before gate cleanup, Phase 7 may prepare scaffolding but may not run case experiments or upgrade claims."
patterns-established:
  - "Semi-real case artifacts must label semi-real geography/network, simulated demand, and simulated choice."
  - "Real passenger behavior, acceptance, opt-out, and operating profit cannot be claimed from simulated case data."
requirements-completed:
  - CASE-01
  - CASE-02
  - CASE-04
duration: 20 min
completed: 2026-06-15T21:50:00+08:00
---

# Phase 6: Real Or Semi-Real Case Study Feasibility Audit Summary

**Semi-real case-study route approved behind gates with reproducible public-network sourcing and simulated-demand labels**

## Performance

- **Duration:** 20 min
- **Started:** 2026-06-15T21:30:00+08:00
- **Completed:** 2026-06-15T21:50:00+08:00
- **Tasks:** 6/6
- **Files modified:** 8

## Accomplishments

- Wrote `.planning/data/CASE_STUDY_FEASIBILITY.md` with source audit, candidate ranking, decision, preprocessing plan, Phase 7 code-change outline, paper value, gate status, and minimum semi-real contract.
- Generated supporting audit outputs at `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md` and `.json`; audit confirms `IMPORT_OK`, readiness `blocked`, checkpoint `loaded`, claim-ready `false`, and no formal replay.
- Updated planning state so `CASE-01`, `CASE-02`, and `CASE-04` are complete while Phase 7 remains limited to scaffolding until upstream gates pass.

## Task Commits

No task commits were created in this run because the repository entered Phase 6
with extensive pre-existing dirty and deleted files, including modified
planning documents. To avoid accidentally sweeping unrelated user/prior-work
changes into a commit, Phase 6 outputs are left in the working tree for review.

## Files Created/Modified

- `.planning/data/CASE_STUDY_FEASIBILITY.md` - Primary Phase 6 decision artifact.
- `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md` - Generated runtime/gate audit.
- `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.json` - Generated machine-readable audit.
- `.planning/PROJECT.md` - Records Phase 6 validated decision and active Phase 7 boundary.
- `.planning/REQUIREMENTS.md` - Marks `CASE-01`, `CASE-02`, and `CASE-04` complete.
- `.planning/ROADMAP.md` - Marks Phase 6 complete and adds Phase 7 gate result.
- `.planning/STATE.md` - Advances current focus to Phase 7 gated scaffolding.
- `.planning/phases/06-real-or-semi-real-case-study-feasibility-audit/06-VERIFICATION.md` - Phase verification report.

## Decisions Made

- Add a semi-real case in principle, with status `approved_blocked_pending_gate_cleanup`.
- Use public OSM/open-network data as the default Phase 7 route unless Yanjiao/Beijing sources can be reproduced equally well.
- Treat Yanjiao/Beijing commuting material as motivation/context unless it is paired with reproducible network and matrix evidence.
- Keep RC formal evidence as the main empirical ladder; the case study is supplemental external-scenario robustness.
- Forbid real passenger-behavior, real acceptance, real opt-out, or real profit claims from simulated demand and simulated choice.

## Deviations from Plan

None - plan executed within scope. Phase 6 did not implement ingestion code, run case experiments, generate case result rows, edit generated paper artifacts, or upgrade manuscript claims.

## Issues Encountered

- The repository was already heavily dirty before Phase 6 execution. This blocked clean per-task committing without risking unrelated changes. The work was completed and verified in-place.
- External source links were checked during execution; the report records URLs and access date, but Phase 7 must still pin exact source snapshots/hashes before any case execution.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 7 is ready to be planned as a scaffolding-only phase: source ingestion,
metadata validation, candidate-point rules, distance-matrix rebuild contracts,
and manifest preparation. Case-study experiment execution and case-study claims
remain blocked until provenance/readiness/artifact/claim gates pass.

---
*Phase: 06-real-or-semi-real-case-study-feasibility-audit*
*Completed: 2026-06-15*
