# M2 User Actions Required

**Phase:** 02 - Gate Cleanup Plan Without Destructive Changes
**Created:** 2026-06-16
**Purpose:** Register actions that may be necessary later but require explicit
user approval because they can change the worktree, regenerate evidence,
replace mirrors, alter manuscript claims, or affect the formal provenance
chain.

## Phase 2 Status

All actions below are approval-required and `not executed in Phase 2`.

Phase 2 did not run git cleanup, legacy restoration, checkpoint training,
formal readiness, final/formal replay, artifact builders, package builders,
mirror replacement, case-study execution, or manuscript claim upgrades.

## Approval-Required Register

| Action | Why approval is required | Blocker addressed | Command template | Phase 2 status | Verification after approval |
| --- | --- | --- | --- | --- | --- |
| git restore/stash/revert/delete cleanup | Can remove or overwrite user changes, regenerated planning state, deleted legacy paths, or evidence-boundary context. | dirty git; clean formal provenance; readiness `git_dirty=false` | `git status --short --branch`; cleanup command must be selected by user, such as `git restore <path>`, `git stash push`, `git revert <commit>`, or approved file deletion | not executed in Phase 2 | Re-run `git status --short --branch`; readiness path may proceed only when the intended claim-supporting tree is clean or explicitly diagnostic. |
| legacy file restoration | Can reintroduce superseded planning/results files and confuse the regenerated evidence boundary. | deleted legacy planning/results; frozen settings or calibration traceability if Phase 3 needs a named legacy file | `git show <commit>:<legacy-path> > <approved-restored-path>` or another user-approved restore path | not executed in Phase 2 | Restored file is cited to a specific blocker; regenerated planning remains authoritative; no unrelated legacy tree is restored. |
| checkpoint training | Writes checkpoint and sidecar artifacts that become part of the evidence chain. | missing or incomplete formal checkpoint provenance; missing checkpoint sidecar | `cd work2_coding; python scripts/train_shared_checkpoint.py --study formal_robust_menu --checkpoint-path outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt` | not executed in Phase 2 | Checkpoint and sidecar exist; recomputed `checkpoint_sha256` and `checkpoint_sidecar_sha256` are recorded; sidecar metadata matches the approved run. |
| formal readiness | Writes `FORMAL_READINESS.json`, `FORMAL_READINESS.md`, and dependency snapshot outputs; may smoke-load checkpoints. | formal readiness status; dependency snapshot; checkpoint load status; dirty git blocker | `cd work2_coding; python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/formal_readiness --diagnostic-ok` | not executed in Phase 2 | `FORMAL_READINESS.json` exists with `status=passed` and `claim_ready_allowed=true` for claim use, or blocked status is documented as diagnostic only. |
| final/formal replay | Writes generated study rows and empirical outputs; can determine or alter evidence for claims. | GATE-03/GATE-04 go/no-go; PATH-01/PATH-02 if Phase 3 approves replay | `cd work2_coding; python scripts/run_study.py --study formal_robust_menu --execute` or `cd work2_coding; python scripts/run_study.py --study final_robust_menu --execute` | not executed in Phase 2 | Generated rows exist, all required statuses are complete, checkpoint metadata is loaded/hashed, and no tuning on final outputs occurred. |
| artifact builder | Writes aggregate artifacts, tables, figures, metadata, artifact status, and manuscript frame outputs. | artifact gate; main RC blocked status; source-row-to-artifact traceability | `cd work2_coding; python scripts/build_artifacts.py --run-dir outputs/studies/<study>/<run_id> --claim-ready` | not executed in Phase 2 | `ARTIFACT_STATUS.json` and sidecars are regenerated from approved rows; no generated rows or status files are hand-edited. |
| Phase 10 package builder | Writes the paper package index/status, strict claim guard, section map, and optional mirror. | package completeness; strict claim guard ceiling; four current missing package entries | `cd work2_coding; python scripts/build_phase10_paper_artifacts.py --default-mirror` | not executed in Phase 2 | `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, `CLAIM_GUARD.json`, and `ARTIFACT_TO_SECTION_MAP.json` are regenerated; missing entries and blocker counts are explained by source files, not hand edits. |
| mirror replacement | Can delete and replace root `artifacts/` mirror directories. | canonical-vs-root package drift; manuscript-facing artifact paths | `cd work2_coding; python scripts/build_phase10_paper_artifacts.py --default-mirror` or approved mirror copy command | not executed in Phase 2 | Canonical and mirror package JSON files match by SHA-256; source of truth remains `work2_coding/artifacts/...`. |
| case-study execution | Would move case material from scaffold-only toward runtime evidence and may require external/source-data approvals. | case scaffold status; `C8_semi_real_case_validation` blocked | approved future case manifest command, for example `cd work2_coding; python scripts/run_study.py --study <approved_case_study> --execute` | not executed in Phase 2 | Runtime case rows, source contracts, validation outputs, artifact gates, and claim guard status exist before any case validation language is used. |
| manuscript claim upgrade | Can overstate blocked or diagnostic evidence if done before strict guard authorization. | manuscript language claim ceiling; blocked positive claim IDs C1, C2, C3, C4, C6, C8 | approved manuscript edit after claim guard review, such as editing `manuscript/main.tex` or `.planning/paper/*` | not executed in Phase 2 | Every upgraded statement maps to an authorized `CLAIM_GUARD.json` claim ID and table/figure source path; prohibited language scan is clean. |

## Explicitly Not Approved By Phase 2

Phase 2 does not approve:

- `run_study.py --execute`
- `train_shared_checkpoint.py`
- `check_formal_readiness.py`
- `build_artifacts.py`
- `build_phase10_paper_artifacts.py`
- final replay
- formal replay
- case-study execution
- git restore/stash/reset/checkout/revert/delete cleanup
- mirror replacement
- generated-row, figure, table, package-status, or claim-guard hand edits
- manuscript claim upgrades

The next approval decision belongs to Phase 3, which decides whether a clean,
pre-registered final replay is scientifically legitimate or whether the paper
should remain conditional diagnostic.
