# Phase 08 Verification

**Status:** Passed
**Date:** 2026-06-11
**Runtime root:** `work2_coding/`

## Commands

| Check | Command | Result |
|---|---|---|
| Import smoke | `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | PASS: `IMPORT_OK` |
| Checkpoint provenance contracts | `cd work2_coding; python scripts/test_checkpoint_provenance.py` | PASS: 6 tests |
| Experiment contract tests | `cd work2_coding; python scripts/test_experiment_contracts.py` | PASS: 12 tests |
| Artifact gate tests | `cd work2_coding; python scripts/test_artifact_gates.py` | PASS: 7 tests |
| Attention artifact gate tests | `cd work2_coding; python scripts/test_attention_artifact_gate.py` | PASS: 8 tests |
| Study execution status tests | `cd work2_coding; python scripts/test_study_execution_status.py` | PASS: 7 tests |
| Attention manifest contracts | `cd work2_coding; python scripts/test_attention_manifest_contracts.py` | PASS: 7 tests |
| Study manifest tracking check | `git ls-files 'work2_coding/Experiments/studies/**'` | PASS: smoke/pilot/formal study manifests remain tracked |
| Virtualenv tracking check | `git ls-files 'work2_coding/venv/**' \| Measure-Object` | PASS: 0 tracked files after index removal |

## Git State Verification

`git status --short --ignored` before the Phase 08 execution commit showed:
- New root `.gitignore`.
- Updated `work2_coding/.gitignore`.
- New Phase 08 report/verification/validation/summary docs.
- Staged index removals for `work2_coding/venv/` only; local files remain on disk and are ignored.
- Ignored local state limited to `.planning/reports/`, Python caches, runtime raw outputs, diagnostic local manifest, and `work2_coding/venv/`.

This is the expected transitional state before the execution commit. After commit, evidence phases should be able to report `git_dirty=false` unless they intentionally create narrowly documented local outputs.

## Requirement Evidence

| Requirement | Evidence | Status |
|---|---|---|
| PROV-01 | `08-HYGIENE-REPORT.md` classifies planning docs, generated artifacts, local outputs, dependency files, deleted user documents, and other local state. | Passed |
| PROV-02 | Root `.gitignore` plus `work2_coding/.gitignore` ignore venv/cache/temp/raw output/checkpoint binaries while preserving review artifacts and study manifests. `work2_coding/venv/` removed from index. | Passed |
| PROV-03 | `08-HYGIENE-REPORT.md` records generated artifact track-vs-local policy. | Passed |
| PROV-04 | `08-HYGIENE-REPORT.md` defines the Phase 09+ evidence provenance gate for clean or narrowly documented dirty state. | Passed |

## Gate

Phase 09 may proceed after the Phase 08 execution commit. Later evidence must not support attention-improves-DSPO language unless completed paired, non-placeholder, checkpoint-loaded evidence supports that direction.

