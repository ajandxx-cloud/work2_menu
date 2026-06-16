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
