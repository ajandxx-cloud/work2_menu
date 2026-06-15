---
phase: 3
plan: 1
subsystem: formal-readiness
tags:
  - formal-readiness
  - checkpoint-provenance
  - dirty-git-gate
requires:
  - RC-01
  - RC-02
  - RC-03
provides:
  - formal-readiness-blocker-diagnosis
affects:
  - .planning/results/FORMAL_BLOCKER_DIAGNOSIS.md
tech-stack:
  added: []
  patterns:
    - manifest-driven readiness gate
key-files:
  created:
    - .planning/results/FORMAL_BLOCKER_DIAGNOSIS.md
  modified:
    - work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json
    - work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.md
key-decisions:
  - Keep Phase 3 evidence diagnostic while readiness is blocked by dirty git.
  - Reuse the existing formal shared checkpoint because readiness reports load_status=loaded with matching SHA-256.
requirements-completed:
  - RC-01
  - RC-02
  - RC-03
duration: 15 min
completed: 2026-06-15T11:51:33+08:00
---

# Phase 3 Plan 1: Formal Readiness And Blocker Diagnosis Summary

Plan 03-01 verified the formal manifest/readiness surface, confirmed checkpoint
provenance, and documented the dirty-git blocker without mutating unrelated
worktree changes.

## Results

| Task | Result |
| --- | --- |
| Inspect formal manifest and mainline contract | Formal, pilot, and smoke robust-menu manifests keep the seven-tag mainline family; the formal manifest declares `tier: formal`, `run_mode: formal`, the required checkpoint path, paired fields, varied fields, and normalized row metadata. |
| Verify or diagnose shared checkpoint readiness | Required checkpoint exists at `outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`, SHA-256 `d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4`, load status `loaded`. |
| Diagnose dirty git and readiness blockers | Created `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`; readiness status remains `blocked`, `claim_ready_allowed: false`, blocker code `dirty_git`. |
| Run focused preflight tests | Import smoke and five focused scripts passed. |

## Verification

Run from `work2_coding/`:

| Command | Result |
| --- | --- |
| `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | `IMPORT_OK` |
| `python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/phase5_readiness` | Expected blocked exit; `dirty_git`, checkpoint loaded |
| `python scripts/test_formal_readiness.py` | PASS: 4 formal readiness tests |
| `python scripts/test_formal_replay_enablement.py` | PASS: 4 formal replay enablement tests |
| `python scripts/test_checkpoint_provenance.py` | PASS: 6 checkpoint provenance tests |
| `python scripts/test_policy_fairness_contract.py` | PASS: 15 policy fairness contract tests |
| `python scripts/test_paired_replay_contract.py` | PASS: 12 paired replay contract tests |

## Commits

| Commit | Description |
| --- | --- |
| `dd1bd1b` | `docs(03-01): document formal readiness blockers` |

## Deviations from Plan

None - plan executed exactly as written. The readiness command exits nonzero
because the formal readiness gate is intentionally blocked by dirty git; that
state is documented as the expected diagnostic outcome for this plan.

**Total deviations:** 0 auto-fixed.
**Impact:** Phase 3 can continue diagnostically, but claim-ready artifacts must
remain blocked until dirty git is resolved and readiness passes.

## Self-Check: PASSED

The blocker diagnosis exists, checkpoint provenance is explicit, focused tests
passed, and no generated rows or paper artifacts were hand-edited.

## Next

Ready for Plan 03-02 formal replay row validation.
