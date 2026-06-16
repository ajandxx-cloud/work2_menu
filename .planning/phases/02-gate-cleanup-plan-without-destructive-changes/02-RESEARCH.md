# Phase 2: Gate Cleanup Plan Without Destructive Changes - Research

**Researched:** 2026-06-16
**Status:** Complete
**Mode:** Inline research, because subagent spawning was not explicitly authorized in this runtime.

## Research Question

What does the planner need to know to plan Phase 2 well?

Phase 2 must plan provenance, readiness, checkpoint, dirty-git, and package
blocker cleanup without actually performing cleanup. It is a documentation and
read-only inspection phase. It must not execute formal readiness, train or load
checkpoints, run replay, regenerate artifacts, modify generated evidence, or
normalize the dirty worktree.

## Current Scope Boundary

Phase 2 deliverables are planning documents only:

- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`

The phase may read current planning docs, generated package indexes, gate
modules, package source directories, and git status. It may write the Phase 2
milestone documents. It may run the import smoke command.

The phase must not run these commands during execution:

- `python scripts/run_study.py --execute`
- `python scripts/train_shared_checkpoint.py`
- `python scripts/check_formal_readiness.py`
- `python scripts/build_artifacts.py`
- `python scripts/build_phase10_paper_artifacts.py`
- formal or final replay
- case-study execution
- git restore, stash, reset, checkout, revert, or delete cleanup
- mirror replacement

## Phase 1 Handoff Facts

Phase 1 established that the current generated Phase 10 package is not
claim-ready and leans diagnostic-only from current files. It did not decide
whether a future final replay is scientifically legitimate.

Key facts from Phase 1:

- Active runtime root is `work2_coding/`.
- `ooh_code/` is absent and stale for current planning.
- Canonical package root is
  `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`.
- Root `artifacts/work2_robust_menu/phase10_paper_artifacts/` is a mirror.
- Four key mirror JSON files matched canonical files by SHA-256 in Phase 1:
  `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and
  `ARTIFACT_TO_SECTION_MAP.json`.
- Current package status is `claim_ready=false`.
- Current strict guard authorizes only provenance/status transparency as a
  ready claim.

## Dirty Git Research

Read-only `git status --short --branch` during planning showed the repository
is dirty before Phase 2 execution. The worktree has:

- modified regenerated planning core files, including `.planning/PROJECT.md`,
  `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`,
  `.planning/config.json`, and `.planning/research/SUMMARY.md`;
- modified paper boundary docs under `.planning/paper/`;
- deleted legacy planning and result files under old milestone, phase, result,
  and final directories;
- no untracked paths in the current status sample.

Phase 2 should classify dirty state by risk category, not by dumping every
path into the main cleanup plan. The categories should include:

1. regenerated planning core;
2. paper boundary docs;
3. deleted legacy planning, phase, final, and result files;
4. runtime/generated evidence paths, if any are dirty at execution time;
5. other user changes, if detected.

Each category should state representative paths, risk interpretation, whether
the category blocks claim-ready formal evidence, and whether user approval is
required before any action.

## Checkpoint And Readiness Contract

`work2_coding/Src/formal_readiness.py` is the main readiness preflight module.
It writes `FORMAL_READINESS.json`, `FORMAL_READINESS.md`, and
`DEPENDENCY_SNAPSHOT.json`, but Phase 2 must not execute it.

Relevant contract behavior:

- `_load_sidecar()` expects `<checkpoint>.sidecar.json` and records sidecar
  existence plus hash.
- `_write_dependency_snapshot()` records environment provenance, manifest path,
  manifest hash, resolved settings, and command.
- `_load_checkpoint_smoke()` uses `Config` and `model.load_checkpoint()` to
  smoke-load the checkpoint without formal replay. This is explicitly not for
  Phase 2 execution.
- `check_formal_readiness()` blocks dirty git unless `allow_dirty=True`.
- Missing formal checkpoint creates blocker code `missing_formal_checkpoint`.
- Non-loaded smoke status creates blocker code `formal_checkpoint_not_loaded`.
- Smoke hash mismatch creates blocker code `formal_checkpoint_hash_mismatch`.
- Smoke exceptions create blocker code `formal_checkpoint_load_failed`.

`work2_coding/Src/study_execution.py` contributes row-level provenance:

- `collect_git_provenance()` records `git_commit`, `git_dirty`, and a short
  `git_status_summary`.
- `checkpoint_path_for_manifest()` and `resolve_checkpoint_path()` define the
  manifest checkpoint path contract.
- `inspect_manifest_prerequisites()` blocks missing checkpoint path and missing
  checkpoint file for pilot/formal tiers.
- `checkpoint_metadata_for_setting()` records `checkpoint_load_status` and
  checkpoint hash when a required checkpoint exists.
- completed rows carry `checkpoint_load_status`, `checkpoint_path`,
  `checkpoint_hash`, `checkpoint_required`, and
  `checkpoint_intentional_mismatch`.

`work2_coding/Src/artifact_status.py` enforces claim-ready artifact checks:

- pilot/formal rows require loaded checkpoint provenance;
- formal claim-ready artifacts require a dependency snapshot;
- formal readiness JSON must have `status == "passed"`;
- formal readiness JSON must set `claim_ready_allowed=true`;
- formal readiness git provenance must have `git_dirty=false`;
- dependency snapshot path and hash must exist and match;
- readiness checkpoint must be loaded and hashed;
- source rows must all report loaded checkpoint status;
- readiness checkpoint hash must match source row checkpoint hashes;
- source rows must include checkpoint hashes.

The Phase 2 provenance requirements document should therefore lock these
minimum fields:

- checkpoint manifest path;
- resolved checkpoint path;
- checkpoint SHA-256 hash recomputed from the file;
- sidecar path and sidecar hash;
- sidecar metadata existence and match/exception explanation;
- checkpoint load status;
- manifest path and manifest hash;
- git SHA and git dirty state;
- dependency snapshot path and hash;
- readiness JSON path and hash;
- source row checkpoint hash and load status.

The recomputed checkpoint file SHA-256 is authoritative. Sidecar metadata
supports the evidence chain but cannot substitute for hashing the checkpoint
file.

## Phase 10 Package Blocker Research

Current `PACKAGE_STATUS.json` reports:

| Field | Value |
| --- | --- |
| `schema_version` | `phase10-paper-artifact-package-v1` |
| `claim_ready` | `false` |
| `strict_claim_guard_claim_ready` | `false` |
| `manuscript_positive_claims_allowed` | `false` |
| `artifact_count` | `74` |
| `existing_artifact_count` | `70` |
| `missing_artifact_count` | `4` |
| `blocker_count` | `108` |

Source-family status:

| Source family | Artifacts | Existing | Status |
| --- | ---: | ---: | --- |
| `blocker_status` | 6 | 6 | `blocked` |
| `case_scaffold` | 12 | 10 | `scaffold_only_no_result_evidence` |
| `main_rc` | 30 | 28 | `blocked` |
| `phase8_sensitivity` | 14 | 14 | `diagnostic_provisional_blocked` |
| `phase9_tractability` | 12 | 12 | `diagnostic_provisional_blocked` |

The four missing entries are synthesized by `paper_artifacts.py` when glob
patterns have no matching files:

| Missing source path | Source family | Package role | Why it appears |
| --- | --- | --- | --- |
| `.planning/data/case_studies/missing.yml` | `case_scaffold` | `case_scaffold_config` | `CASE_GLOBS` includes `*.yml`, but the directory currently has `.yaml` files and no `.yml` files. |
| `.planning/data/case_studies/missing.json` | `case_scaffold` | `case_scaffold_contract` | `CASE_GLOBS` includes `*.json`, but the directory currently has no `.json` files. |
| `work2_coding/artifacts/work2_robust_menu/figures/missing.png` | `main_rc` | `figure` | `MAIN_GLOBS` includes `figures/*.png`, but the directory currently has only `*.png.status.json` files. |
| `work2_coding/artifacts/work2_robust_menu/figures/missing.metadata.json` | `main_rc` | `figure_metadata` | `MAIN_GLOBS` includes `figures/*.metadata.json`, but no figure metadata files exist in that directory. |

The package code marks a missing source as blocked and adds `source file
missing`. Missing entries should be documented as expected-pattern misses, not
as proof that specific real files were recently deleted.

## Blocker Action Matrix Shape

`M2_GATE_CLEANUP_PLAN.md` should use a `Blocker -> Action -> Approval ->
Verification` shape. Each row should include:

- blocker or source;
- current evidence;
- recommended later action;
- approval requirement;
- what Phase 2 will not do;
- verification command or check.

Rows should prioritize Phase 3 go/no-go blockers:

- dirty git and clean provenance;
- formal checkpoint path/hash/sidecar/load status;
- readiness JSON and dependency snapshot integrity;
- source row checkpoint metadata;
- package missing source patterns;
- main RC blocked status and strict claim guard ceiling.

Empirical performance, adaptive-window increment, tractability credibility,
case-study validation, and central superiority are not Phase 2 repairs. They
belong to Phase 3 or later evidence-path phases.

## Pattern Research

Useful analogs:

- Phase 1 plan and deliverables show a successful read-only audit pattern:
  `.planning/phases/01-repository-and-evidence-boundary-audit/01-PLAN.md`,
  `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`,
  `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`, and
  `.planning/milestones/tr_e_completion/M1_DECISION.md`.
- Phase 1 validation uses script-style command checks and source assertions,
  which also fit Phase 2.
- Phase 2 should be stricter about user approval routing because the expected
  actions are cleanup and evidence-generation actions that are intentionally
  deferred.

## Validation Architecture

Phase 2 validation is document and boundary validation. It should not validate
by running formal readiness or artifact builders.

Recommended checks:

1. Runtime import smoke:
   `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`
2. File existence checks for:
   - `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
   - `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
   - `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`
3. Source assertions:
   - `M2_GATE_CLEANUP_PLAN.md` includes `Blocker`, `Action`, `Approval`, and
     `Verification`;
   - `M2_PROVENANCE_REQUIREMENTS.md` includes checkpoint path, checkpoint hash,
     sidecar metadata, load status, dependency snapshot, manifest hash, git
     SHA, git dirty state, readiness JSON path, and readiness JSON hash;
   - `M2_USER_ACTIONS_REQUIRED.md` lists approval-required destructive or
     evidence-generating commands and states they were not executed in Phase 2.
4. Diff check confirming no generated evidence path was modified by Phase 2
   execution:
   `git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts`

Manual review remains useful for whether recommended later actions are
scientifically sufficient, but the Phase 2 plan can be validated with source
assertions and read-only command outputs.

## Research Complete

Research found no reason to expand Phase 2 into cleanup execution. The planner
should produce one Wave 1 execution plan that writes the three M2 milestone
documents, inspects only read-only evidence, and routes every destructive or
evidence-generating cleanup action to user approval.

## RESEARCH COMPLETE
