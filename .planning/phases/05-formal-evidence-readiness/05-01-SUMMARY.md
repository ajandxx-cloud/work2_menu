---
phase: 5
plan: 05-01-formal-readiness-preflight
subsystem: formal-readiness
tags:
  - readiness
  - checkpoint-provenance
  - dependency-snapshot
key-files:
  created:
    - work2_coding/Src/formal_readiness.py
    - work2_coding/scripts/check_formal_readiness.py
    - work2_coding/scripts/test_formal_readiness.py
  modified: []
requirements-completed:
  - MLC-05
  - ART-02
  - ART-03
completed: 2026-06-14
---

# Phase 5 Plan 01: Formal Readiness Preflight Summary

Implemented a dedicated formal readiness preflight that does not run formal replay.

## Completed

- Added `Src/formal_readiness.py` with manifest validation, checkpoint resolution, SHA256 capture, load-smoke support, row metadata probe, git provenance, dependency snapshot writing, and JSON/Markdown report generation.
- Added `scripts/check_formal_readiness.py` with `--study`, `--output-root`, `--allow-dirty`, and `--diagnostic-ok`.
- Added `scripts/test_formal_readiness.py` covering missing checkpoint reports, loaded checkpoint probes, dirty-git blocking, manifest hash recording, and dependency snapshot hashing.

## Verification

- `python scripts/test_formal_readiness.py` passed with 4 tests.
- Real preflight wrote `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json` and `.md`.

## Deviations

None - plan executed as readiness gating, not formal replay.

## Self-Check: PASSED
