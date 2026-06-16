---
phase: 14
status: dirty_git_audit_complete
claim_ready: false
generated_at: 2026-06-16T18:44:53+08:00
timezone: Asia/Shanghai
phase_scope: planning_and_audit_only
---

# Dirty Git Actions Required

## Boundary

Phase 14 inspected git status only. It did not delete, revert, stash,
overwrite, or clean unrelated files. It did not repair readiness gates or
regenerate artifacts.

## Current Git Status

Command:

```powershell
git status --short
```

Observed before Phase 14 edits: no output.

Interpretation: the current working tree was clean before writing Phase 14
documentation outputs.

## Required Current-Tree Actions

| item | status | required action now | claim-ready relevance |
| --- | --- | --- | --- |
| Current uncommitted non-Phase-14 files | none observed | none | No current dirty working-tree action is needed before planning docs are written. |
| Current dirty-git blocker for future readiness | absent in live tree | preserve clean tree; do not introduce unrelated edits before any future readiness preflight | Relevant to potential future Path A, if selected. |
| Unrelated dirty files | none observed | none; do not delete, revert, stash, or overwrite | No unrelated cleanup is required. |

## Historical Dirty Provenance Still Recorded

The live tree is clean, but several generated evidence files still record
historical dirty provenance. That historical metadata remains relevant to
claim-ready readiness and cannot be erased by cleaning the current tree.

| source | recorded dirty status | examples | relevance |
| --- | --- | --- | --- |
| `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json` | `git_dirty=true`, blocker `dirty_git` | Modified `.planning/STATE.md`, `.planning/config.json`, and deleted old phase planning files are recorded in the readiness blocker. | CF-001 remains in the existing readiness JSON until a future authorized readiness preflight is run from a clean tree. |
| `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json` | all 35 rows record `git_dirty=true` | Modified planning docs, manifests, runtime code, artifact builders, row schema, and tests are recorded in `git_status_summary`. | This is source-row provenance, not a current-tree cleanup issue. It cannot be changed by hand. |
| `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` | `git_dirty=true` in package provenance | Deleted `learning meeting point.docx` and an untracked text file were recorded by that generated artifact package. | This package is already blocked and indexes older pilot/placeholder evidence. It remains a generated historical status artifact. |

## Action Classification

| action_id | possible action | classification | Phase 17 treatment if later selected |
| --- | --- | --- | --- |
| DG-001 | Keep the live tree clean before a future readiness preflight. | non-semantic metadata/schema repair | Path A allowed if selected. |
| DG-002 | Rerun readiness from a clean tree to produce a new readiness JSON. | non-semantic metadata/schema repair | Path A allowed if selected; it does not rerun empirical replay. |
| DG-003 | Commit Phase 14 documentation outputs only. | non-semantic documentation/provenance action | Required by the user for this phase. |
| DG-004 | Edit historical generated rows to change `git_dirty` or `git_status_summary`. | prohibited generated-row manipulation | Not allowed in Path A, Path B, or Path C. |
| DG-005 | Delete, revert, or stash unrelated historical files to make old generated provenance look clean. | prohibited cleanup/manipulation | Not allowed. Current tree is already clean, and historical provenance must remain truthful. |
| DG-006 | Produce a new clean empirical replay because historical source rows are dirty. | new experiment path | Requires Path B if later selected; otherwise current rows stay diagnostic/blocked. |

## Conclusion

Current dirty-git actions required: none beyond committing Phase 14
documentation outputs.

Dirty-git or provenance blockers still remain in existing generated evidence:

- existing Phase 5 readiness is blocked by historical `dirty_git`;
- selected formal rows carry historical `git_dirty=true`;
- main RC artifact status carries historical dirty provenance from an older
  blocked package.

These historical blockers are relevant to claim-ready readiness, but Phase 14
does not repair them.
