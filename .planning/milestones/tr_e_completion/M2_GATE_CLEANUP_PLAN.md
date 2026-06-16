# M2 Gate Cleanup Plan

**Phase:** 02 - Gate Cleanup Plan Without Destructive Changes
**Created:** 2026-06-16
**Scope:** Non-destructive cleanup planning for Work2 provenance, readiness,
checkpoint, dirty-git, and package blockers before the Phase 3 go/no-go
decision.

## Phase 2 Boundary

Phase 2 is a planning and inspection phase. It may run read-only commands,
read current source and generated package metadata, and write planning
documents under `.planning/milestones/tr_e_completion/`.

Phase 2 did not run restore, stash, reset, checkout, revert, delete cleanup,
formal readiness, checkpoint smoke-load, replay, artifact generation, package
generation, case-study execution, mirror replacement, or manuscript claim
upgrade commands.

Any action that would change the worktree, regenerate evidence, replace a
mirror, train or load a checkpoint, or alter the evidence chain requires user
approval and is routed to `M2_USER_ACTIONS_REQUIRED.md`.

## Dirty-Git State Classification

Read-only command used:

```powershell
git status --short --branch
```

Snapshot summary before Phase 2 deliverable writes:

| Measure | Value |
| --- | ---: |
| Branch state | `main...origin/main [ahead 17]` |
| Changed paths | 146 |
| Modified planning core paths | 7 |
| Modified paper boundary docs | 4 |
| Deleted legacy planning/results paths | 132 |
| New current Phase 2 planning artifacts | 4 |
| Dirty active generated evidence paths | 0 |
| Other detected user changes | 0 |

### Risk Categories

| Category | Representative paths | Risk interpretation | Claim-ready blocker? | User approval required before action? |
| --- | --- | --- | --- | --- |
| regenerated planning core | `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/config.json`, `.planning/research/SUMMARY.md` | Current regenerated GSD state defines the active milestone, requirements, and evidence boundary. It is expected planning drift from the reset and Phase 1/2 setup, not runtime evidence. | Not by itself, but it documents the current claim ceiling and must not be overwritten by stale planning. | Yes for any revert, overwrite, or normalization. Phase 2 only reads or updates current planning artifacts through the workflow. |
| current Phase 2 planning artifacts | `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-PLAN.md`, `02-RESEARCH.md`, `02-VALIDATION.md`, `02-PATTERNS.md` | These are current regenerated Phase 2 planning inputs. They support the M2 cleanup plan and are not generated empirical evidence. | No. They are workflow context for the cleanup-plan phase. | Yes for deletion or replacement. They should be preserved unless the user explicitly replans Phase 2. |
| paper boundary docs | `.planning/paper/CLAIM_SAFE_LANGUAGE.md`, `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`, `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`, `.planning/paper/TR_E_RESEARCH_DESIGN.md` | These documents bound manuscript wording and table/figure use while `CLAIM_GUARD.json` remains not claim-ready. Reverting them could loosen claim-safety constraints. | Not a runtime blocker, but a manuscript claim-safety blocker if stale language is restored. | Yes for any revert, restore, or rewrite beyond normal later manuscript phases. |
| deleted legacy planning/results | `.planning/STATE_LOCK.md`, `.planning/milestones/claim_ready_resolution/*`, older `.planning/phases/*`, `.planning/results/RC_FORMAL_DIAGNOSIS.md`, `.planning/results/SENSITIVITY_SUMMARY.md`, `.planning/results/FROZEN_FINAL_SETTINGS.md` | These deletions belong to the superseded legacy GSD planning/results boundary. Phase 1 treats them as provenance risk, not as files to restore automatically. They are described as superseded by regenerated planning unless a specific readiness or claim blocker depends on one legacy file. | Potentially yes for traceability if Phase 3 needs a specific frozen-setting or calibration document. Not a Phase 2 repair target. | Yes. Restore, history mining, or selective resurrection is approval-required and must be tied to a named blocker. |
| runtime/generated evidence | `work2_coding/outputs/`, `work2_coding/artifacts/`, root `artifacts/` | Current read-only diff check found no dirty paths in active generated evidence roots. Generated rows, artifact status, package status, figures, tables, and mirrors remain evidence outputs and must not be hand-edited. | Yes if dirty or manually edited, because formal evidence and claim guards depend on reproducible outputs. | Yes for any edit, deletion, mirror replacement, artifact rebuild, package rebuild, or evidence regeneration. |
| other user changes | none detected in the current status snapshot | No current paths outside the categories above were detected. Future paths should be classified before any action. | Unknown until inspected. | Yes until classified and tied to a blocker. |

## Non-Destructive Statement

Phase 2 inspected dirty state without reverting, deleting, stashing, checking
out, resetting, or overwriting unrelated files. The dirty-git state remains a
provenance and formal-readiness issue to be resolved only through an approved
later cleanup or clean rerun path.

## Gate Source Inspection

Phase 2 inspected the following source gates and generated package indexes
read-only:

- `work2_coding/Src/formal_readiness.py`: formal preflight writes dependency
  snapshots, records manifest hash and git provenance, resolves the formal
  checkpoint, recomputes the checkpoint hash, reads sidecar metadata when
  present, smoke-loads the checkpoint, and blocks dirty git, missing formal
  checkpoint, unloaded checkpoint, checkpoint hash mismatch, and load failure.
- `work2_coding/Src/study_execution.py`: study execution blocks missing
  checkpoint path/file for pilot and formal tiers, records row-level
  `checkpoint_load_status`, `checkpoint_path`, `checkpoint_hash`, and git
  provenance.
- `work2_coding/Src/artifact_status.py`: artifact classification requires
  formal readiness JSON status `passed`, `claim_ready_allowed=true`,
  `git_dirty=false`, matching dependency snapshot hash, loaded and hashed
  checkpoint, matching manifest hash, and source rows with loaded checkpoint
  statuses and hashes.
- `work2_coding/Src/paper_artifacts.py`: Phase 10 packaging indexes source
  patterns and creates synthetic `missing.*` entries when expected glob
  patterns have no matching files.

Current package status from
`work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`:

| Field | Value |
| --- | --- |
| `schema_version` | `phase10-paper-artifact-package-v1` |
| `generated_at_utc` | `2026-06-16T05:48:47+00:00` |
| `claim_ready` | `false` |
| `strict_claim_guard_claim_ready` | `false` |
| `manuscript_positive_claims_allowed` | `false` |
| `artifact_count` | 74 |
| `existing_artifact_count` | 70 |
| `missing_artifact_count` | 4 |
| `blocker_count` | 108 |

## Current Missing Package Entries

The four missing package entries are expected-pattern misses produced by
`paper_artifacts.py`; they are not proof that four specific real files were
recently deleted.

| Missing source path | Source family | Package role | Current source-directory finding | Phase 2 interpretation |
| --- | --- | --- | --- | --- |
| `.planning/data/case_studies/missing.yml` | `case_scaffold` | `case_scaffold_config` | `.planning/data/case_studies/` contains `.yaml`, Markdown, and validator files, but no `.yml` files. | Synthetic miss from `CASE_GLOBS` including `*.yml`; scaffold-only, not runtime evidence. |
| `.planning/data/case_studies/missing.json` | `case_scaffold` | `case_scaffold_contract` | `.planning/data/case_studies/` contains no `.json` files. | Synthetic miss from `CASE_GLOBS` including `*.json`; scaffold-only, not runtime evidence. |
| `work2_coding/artifacts/work2_robust_menu/figures/missing.png` | `main_rc` | `figure` | `work2_coding/artifacts/work2_robust_menu/figures/` contains `*.png.status.json` files, but no real `.png` images. | Synthetic miss from `MAIN_GLOBS` including `figures/*.png`; package completeness blocker. |
| `work2_coding/artifacts/work2_robust_menu/figures/missing.metadata.json` | `main_rc` | `figure_metadata` | `work2_coding/artifacts/work2_robust_menu/figures/` contains no `*.metadata.json` files. | Synthetic miss from `MAIN_GLOBS` including `figures/*.metadata.json`; package provenance blocker. |

Phase 2 does not create placeholder files, fill scaffold files by hand,
regenerate figures, run artifact builders, or run package builders.

## Blocker -> Action -> Approval -> Verification Matrix

| Blocker | Action | Approval | Verification |
| --- | --- | --- | --- |
| Dirty git blocks clean formal provenance. Current status has regenerated planning, paper boundary docs, deleted legacy planning/results, and no dirty active generated-evidence roots. | Preserve the current dirty-state classification and defer cleanup to an approved cleanup branch or clean rerun protocol. | Required for any restore, stash, revert, delete cleanup, commit normalization, or legacy file restoration. | Before formal readiness, run `git status --short --branch`; claim-supporting readiness must record `git_dirty=false`. |
| Formal readiness JSON is currently blocked or absent for any future claim-supporting rerun. | Run formal readiness only after Phase 3 approves a legitimate final or formal path and the checkpoint/dependency/git contract is satisfied. | Required because `check_formal_readiness.py` writes readiness and dependency outputs and may smoke-load checkpoints. | `FORMAL_READINESS.json` exists, `status=passed`, `claim_ready_allowed=true`, and `readiness_json_sha256` is recorded. |
| Checkpoint provenance is incomplete: formal checkpoint file exists, but expected sidecar metadata is currently missing. | Regenerate or approve checkpoint provenance through the checkpoint training/readiness protocol; do not hand-create sidecar metadata. | Required because checkpoint training, sidecar writing, and smoke-loading change the evidence chain. | `checkpoint_resolved_path`, `checkpoint_sha256`, `checkpoint_sidecar_path`, `checkpoint_sidecar_sha256`, and `checkpoint_load_status=loaded` are recorded and match source rows. |
| Dependency snapshot is required for formal claim-ready artifacts. | Generate a dependency snapshot as part of approved formal readiness, not as a standalone manual artifact. | Required because it records environment state for a claim-supporting evidence chain. | `dependency_snapshot_path` exists and `dependency_snapshot_sha256` matches the file consumed by readiness/artifact classification. |
| Source row checkpoint metadata must align with readiness metadata. | If Phase 3 approves replay, produce new source rows through `run_study.py --execute`; do not patch existing rows. | Required because replay writes generated rows and can alter empirical evidence. | `source_row_checkpoint_hashes` include the readiness checkpoint hash and `source_row_checkpoint_load_statuses` contain only `loaded` for required formal rows. |
| Current missing package source patterns block package completeness. | Leave the four synthetic missing entries documented until an approved artifact/package regeneration path creates real source files or explicitly narrows package expectations. | Required for artifact builder, package builder, placeholder creation, or source-pattern changes. | `PACKAGE_INDEX.json` has no synthetic `missing.*` entries only after approved regeneration; mirror SHA checks match canonical package JSON. |
| Main RC source family is `blocked` with 30 artifacts, 28 existing. | Treat main RC artifacts as blocker/status and diagnostic inputs until clean formal readiness, completed formal rows, and artifact gates pass. | Required for any final/formal replay or main artifact rebuild. | `ARTIFACT_STATUS.json` and Phase 10 package status report claim-ready only when generated gates authorize it. |
| Strict claim guard ceiling is `claim_ready=false`; only `C7_provenance_status_transparency` is currently claim-ready. | Keep manuscript and planning language within the strict claim guard. Do not upgrade positive claims from the cleanup plan. | Required for any manuscript claim upgrade or regenerated strict claim guard. | `CLAIM_GUARD.json` explicitly authorizes the exact claim ID and manuscript use. |
| Case scaffold status is `scaffold_only_no_result_evidence` with two missing expected-pattern entries. | Keep case materials as scaffold/future-work context. Runtime case execution is not a Phase 2 repair. | Required for case-study execution, real-data validation, or package-source upgrades. | Approved case-study phase produces runtime rows, source contracts, validation outputs, and claim guard approval. |
| Phase 8 sensitivity status is `diagnostic_provisional_blocked`. | Keep Phase 8 as diagnostic boundary evidence. No-filter and sensitivity outputs are Not Phase 2 repairs. | Required for any operational robustness or no-filter recommendation. | Artifact status and strict claim guard authorize a specific stronger use; otherwise diagnostic-only language remains. |
| Phase 9 tractability status is `diagnostic_provisional_blocked`. | Keep exact-vs-greedy material diagnostic until a run actually exercises fallback and records credible gap/overlap diagnostics. | Required for tractability rerun or exact/greedy credibility claim. | Phase 9 artifacts and claim guard authorize computational credibility; otherwise no near-optimal or exact-greedy claim. |
| Manuscript language can overstate blocked evidence. | Preserve claim-safe language and route wording upgrades to later manuscript phases after the claim path is selected. | Required for any manuscript claim upgrade using current or regenerated evidence. | `.planning/paper/CLAIM_SAFE_LANGUAGE.md`, table/figure maps, and `CLAIM_GUARD.json` agree on allowed wording. |

## Not Phase 2

The following blockers are not Phase 2 repairs and must not be fixed by
cleanup-plan execution:

| Blocker class | Current boundary | Owner |
| --- | --- | --- |
| empirical performance | Central adaptive-menu superiority, product ablation value, menu-construction value, and adaptive-window increment remain unsupported or blocked by current strict claim guard output. | Phase 3 go/no-go and Phase 4 evidence path. |
| tractability credibility | Phase 9 is diagnostic/provisional and does not establish exact-vs-greedy computational credibility. | Phase 4 or later tractability evidence phase. |
| case validation | Case-study materials are scaffold-only and do not validate real passenger behavior or runtime case outcomes. | Future case-study execution phase, not v1 Phase 2. |
| adaptive-window increment | Current evidence does not authorize an adaptive-window improvement claim. | Phase 3/4 if a legitimate final replay path exists. |
| central superiority | Current strict claim guard blocks central adaptive-menu superiority. | Phase 3/4 if evidence and guard output change. |

## Approval-Required Commands

Command templates appear here only as approval-required examples. They were
not executed in Phase 2.

```powershell
cd work2_coding
python scripts/run_study.py --study formal_robust_menu --execute
python scripts/train_shared_checkpoint.py --study formal_robust_menu --checkpoint-path outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt
python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/formal_readiness --diagnostic-ok
python scripts/build_artifacts.py --run-dir outputs/studies/<study>/<run_id> --claim-ready
python scripts/build_phase10_paper_artifacts.py --default-mirror
```

Git restore/stash/revert/delete cleanup, final/formal replay, case-study
execution, mirror replacement, and manuscript claim upgrades are also
approval-required and not executed in Phase 2.
