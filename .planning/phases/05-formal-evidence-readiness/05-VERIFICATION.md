---
status: passed
phase: 5
phase_name: Formal Evidence Readiness
verified: 2026-06-14
requirements:
  - MLC-05
  - ART-02
  - ART-03
---

# Phase 5 Verification

## Result

Phase 5 passed as a readiness-and-gating phase. The implementation now fails closed before formal claims unless a passed matching readiness JSON, loaded checkpoint provenance, dependency snapshot, clean git state, completed formal rows, and artifact gates all agree.

The real `formal_robust_menu` readiness preflight is currently blocked, which is the correct outcome: the formal checkpoint is missing and the repository has uncommitted changes.

## Commands Run

From `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_formal_readiness.py
python scripts/test_artifact_gates.py
python scripts/test_manuscript_claim_guard.py
python scripts/test_experiment_contracts.py
python scripts/test_checkpoint_provenance.py
python scripts/test_shared_checkpoint_training.py
python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/phase5_readiness
```

## Test Results

- Import smoke: passed (`IMPORT_OK`).
- Formal readiness tests: passed, 4 tests.
- Artifact gate tests: passed, 19 tests.
- Manuscript claim guard tests: passed, 4 tests.
- Experiment contract tests: passed, 15 tests.
- Checkpoint provenance tests: passed, 6 tests.
- Shared checkpoint training tests: passed, 1 test.

## Real Readiness Report

- JSON: `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
- Markdown: `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.md`
- Dependency snapshot: `work2_coding/outputs/phase5_readiness/formal_robust_menu/DEPENDENCY_SNAPSHOT.json`
- Dependency snapshot SHA256: `3e914424b1dcea836b90f6dce45c903f71144603800868d64bd071cfb0e7a9f9`
- Manifest hash: `fca35a73f720f5318178585d216f90b610e4ad75d28f9de5b87911ef4c23d50a`
- Readiness status: `blocked`
- Claim-ready allowed: `false`

## Current Blockers

- `dirty_git`: formal claim-ready readiness requires `git_dirty=false`.
- `missing_formal_checkpoint`: missing `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`.

Checkpoint generation command:

```powershell
python scripts/train_shared_checkpoint.py --study formal_robust_menu --checkpoint-path outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt
```

## Gate Conclusions

- Missing, failed, or mismatched formal readiness JSON blocks `build_artifacts.py --claim-ready`.
- Dirty readiness JSON blocks formal claim-ready artifact generation.
- Manifest-hash and checkpoint-hash mismatches block formal claim-ready artifact generation.
- Passed readiness does not override artifact gates; failed, blocked, incomplete, placeholder, bad-checkpoint, diagnostic, and no-filter-only rows still block claim-ready status.
- Formal readiness reports include dependency snapshot path/hash and checkpoint status/hash when available.

## Boundaries Honored

- Formal replay was not executed.
- Checkpoint binaries were not committed.
- Generated result rows, paper artifacts, and manuscript source were not hand-edited.
