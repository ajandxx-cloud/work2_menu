# Phase 2 Pattern Map

**Phase:** 02 - Gate Cleanup Plan Without Destructive Changes
**Created:** 2026-06-16
**Status:** Complete

## Purpose

This pattern map identifies the closest existing artifacts and source modules
for the Phase 2 plan. Phase 2 writes planning documents only; it does not edit
runtime code or generated evidence.

## Deliverable Patterns

| New deliverable | Closest analog | Pattern to reuse |
| --- | --- | --- |
| `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md` | `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md` | Use readable top-level summary plus traceable tables. Keep blocker classes and artifact/claim links explicit. |
| `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` | `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md` | Record exact paths, fields, hashes, status values, and no-modification boundaries without copying entire generated JSON files. |
| `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` | `.planning/milestones/tr_e_completion/M1_DECISION.md` | Separate current decision from forbidden or deferred next steps. Name approval-required actions plainly. |
| Phase 2 verification notes | `.planning/phases/01-repository-and-evidence-boundary-audit/01-VERIFICATION.md` | Use source assertions, import smoke output, and explicit no-generated-evidence checks. |

## Source Module Patterns

| Source file | What Phase 2 should extract | Execution boundary |
| --- | --- | --- |
| `work2_coding/Src/formal_readiness.py` | Readiness JSON fields, dependency snapshot fields, checkpoint sidecar/load/hash blockers, dirty-git blocker codes | Read only. Do not run `check_formal_readiness.py` in Phase 2. |
| `work2_coding/Src/study_execution.py` | `collect_git_provenance`, checkpoint path resolution, row-level checkpoint metadata, blocked prerequisite codes | Read only. Do not execute replay or generate rows. |
| `work2_coding/Src/artifact_status.py` | Claim-ready artifact prerequisites, readiness JSON validation, dependency snapshot/hash checks, checkpoint row status checks | Read only. Do not classify new artifacts from regenerated rows. |
| `work2_coding/Src/paper_artifacts.py` | Missing source-pattern behavior, source-family status, package index and mirror behavior | Read only. Do not run the package builder or replace mirrors. |

## Current Source Pattern Findings

- `paper_artifacts.py` creates a synthetic `missing.*` path when a configured
  glob has no matching files.
- Current case-study scaffold directory has `.yaml`, Markdown, and Python
  validator files, but no `.yml` or `.json` files.
- Current main figure directory has `*.png.status.json` files, but no real
  `*.png` or `*.metadata.json` figure files.
- `formal_readiness.py` writes readiness outputs as a side effect. Phase 2 may
  document expected commands and fields, but those commands must be marked as
  approval-required and not executed in this phase.
- `artifact_status.py` requires clean formal readiness, dependency snapshot
  integrity, loaded checkpoint status, checkpoint hashes, and source row
  checkpoint hashes before claim-ready formal artifacts.

## Planning Implications

- One plan is enough for Phase 2 because all tasks are read-only inspection and
  planning-document writing.
- The plan should include one threat model with risks around destructive git
  cleanup, checkpoint smoke-loading, artifact regeneration, mirror replacement,
  and claim-language upgrades.
- The plan must cite every Phase 2 context decision `D-01` through `D-16` in
  `must_haves.truths` so executor and verifier can trace decisions to tasks.

## PATTERN MAPPING COMPLETE
