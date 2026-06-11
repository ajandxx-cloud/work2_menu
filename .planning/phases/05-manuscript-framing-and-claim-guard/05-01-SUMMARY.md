---
phase: 05-manuscript-framing-and-claim-guard
plan: 01
subsystem: manuscript-claim-guard
tags: [manuscript, claims, artifact-status, provenance, tests]
requires:
  - phase: 04-evidence-and-artifacts
    provides: blocked/non-claim-ready artifact status and provenance sidecars
provides:
  - status-driven method outline
  - status-driven experiment outline
  - status-driven result outline
  - machine-readable claim guard
  - Markdown claim checklist
  - manuscript claim guard regression tests
affects: [phase-05, manuscript, artifacts, claim-checklist]
tech-stack:
  added: []
  patterns: [status-driven manuscript support, machine-readable claim guard, artifact mirror]
key-files:
  created:
    - work2_coding/Src/manuscript_claims.py
    - work2_coding/scripts/build_manuscript_frame.py
    - work2_coding/scripts/test_manuscript_claim_guard.py
    - work2_coding/artifacts/work2_robust_menu/manuscript/CLAIM_GUARD.json
    - artifacts/work2_robust_menu/manuscript/CLAIM_GUARD.json
  modified: []
key-decisions:
  - "Current Phase 4 evidence remains blocked/non-claim-ready and the manuscript artifacts preserve that status."
  - "Allowed claims cover framework, robust pruning, solver auditability, paired replay contracts, and artifact transparency."
  - "Blocked claims include universal dominance, real passenger validation, no-filter operational recommendation, full dynamic exact optimality, empirical superiority, and pilot/formal completion."
patterns-established:
  - "Manuscript support files are generated from ARTIFACT_STATUS.json rather than hand-written from result rows."
  - "CLAIM_GUARD.json gives future manuscript tooling a structured fail-closed contract."
requirements-completed: [PAPER-01, PAPER-02, PAPER-03, PAPER-04]
duration: 25min
completed: 2026-06-11
---

# Phase 05 Plan 01: Manuscript Framing And Claim Guard Summary

**Phase 5 now produces status-driven manuscript support without upgrading blocked evidence into empirical claims**

## Performance

- **Duration:** 25 min
- **Started:** 2026-06-11T15:35:00+08:00
- **Completed:** 2026-06-11T15:55:00+08:00
- **Tasks:** 4
- **Files modified:** 13 created, 0 modified

## Accomplishments

- Added reusable `Src.manuscript_claims` helpers to load artifact status, derive claim eligibility, and render method/experiment/result/checklist Markdown.
- Added public `scripts/build_manuscript_frame.py` to regenerate manuscript support artifacts from `ARTIFACT_STATUS.json`.
- Added `scripts/test_manuscript_claim_guard.py` covering current blocked status, synthetic claim-ready status, generated Markdown/JSON, mirror output, diagnostic no-filter handling, and blocked claim IDs.
- Generated and mirrored manuscript support artifacts:
  - `method_outline.md`
  - `experiment_outline.md`
  - `result_outline.md`
  - `claim_checklist.md`
  - `CLAIM_GUARD.json`

## Files Created

- `work2_coding/Src/manuscript_claims.py` - Pure helpers for artifact-status-driven manuscript outlines and claim guard payloads.
- `work2_coding/scripts/build_manuscript_frame.py` - CLI generator for manuscript support artifacts.
- `work2_coding/scripts/test_manuscript_claim_guard.py` - Deterministic regression tests.
- `work2_coding/artifacts/work2_robust_menu/manuscript/*` - Current generated manuscript support files.
- `artifacts/work2_robust_menu/manuscript/*` - Mirrored reviewer-facing manuscript support files.

## Current Claim Guard Result

- `artifact_status = blocked`
- `claim_ready = false`
- `pilot_claim_ready = false`
- `formal_claim_ready = false`
- Blockers include missing pilot checkpoint and formal evidence skipped.
- Conditional pilot/formal effect-size and formal policy-ranking claims are blocked.
- Diagnostic/status tables and blocked-artifact explanations remain allowed.

## Verification

- `cd work2_coding; python scripts/test_manuscript_claim_guard.py` -> `PASS: 4 manuscript claim guard tests`
- `cd work2_coding; python scripts/build_manuscript_frame.py --artifact-root artifacts/work2_robust_menu --mirror-root ../artifacts/work2_robust_menu` -> generated all five manuscript support files and reported `claim_ready: false`
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`
- `cd work2_coding; python -m py_compile Src/manuscript_claims.py scripts/build_manuscript_frame.py scripts/test_manuscript_claim_guard.py` -> passed

## Deviations from Plan

None.

## Issues Encountered

- The repository already had unrelated dirty state before Phase 5: deleted `learning meeting point.docx` and an untracked Chinese-named text file. Phase 5 did not modify or revert those files.

## Next Phase Readiness

All v1 roadmap phases are now complete. The next GSD action is milestone completion/archival. Stronger empirical manuscript claims still require supplying the missing pilot checkpoint and rerunning Phase 4 to produce non-placeholder claim-ready evidence.

---
*Phase: 05-manuscript-framing-and-claim-guard*
*Completed: 2026-06-11*
