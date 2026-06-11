# Phase 08 Hygiene And Provenance Report

**Status:** Implemented pending verification
**Date:** 2026-06-11
**Runtime root:** `work2_coding/`

## Summary

Phase 08 classifies current repository state, adds repository-level ignore policy, removes an already-tracked virtual environment from the Git index while preserving local files, and records the provenance gate for Phase 09+ evidence work.

No generated result rows or manuscript artifacts were hand-edited.

## Current State Classification

Source command:

```powershell
git status --short --ignored
```

| Category | Paths / Examples | Action | Evidence status |
|---|---|---|---|
| Planning docs | `.planning/phases/08-repository-hygiene-and-provenance-freeze/*` | Track Phase 08 plan, report, verification, validation, summary. | Canonical planning evidence. |
| Generated planning reports | `.planning/reports/MILESTONE_SUMMARY-v2.0.md` | Keep local and ignored by root `.gitignore`. | Not canonical evidence; content is a generated v2.0 summary and is text-encoding damaged. Its usable conclusion is carried forward in Phase 08 docs: current attention evidence is not claim-ready. |
| Generated artifacts to track | `artifacts/`, `work2_coding/artifacts/` | Keep trackable. | Review-facing snapshots/status/tables/figures may be committed when built by artifact scripts. |
| Raw local outputs | `work2_coding/outputs/`, `work2_coding/outputs/studies_actual/`, `work2_coding/Experiments/Parcelpoint_py/pricing/DSPO_Menu/` | Ignore. | Local runtime state, not paper evidence unless promoted by a formal archive process. |
| Python caches | `__pycache__/`, `*.pyc` under `work2_coding/` | Ignore. | Local cache state. |
| Dependency files | `work2_coding/venv/` | Removed from Git index with `git rm -r --cached -- work2_coding/venv`; files remain on disk and are ignored. | Dependency environment is no longer a tracked artifact after commit. |
| Study manifests | `work2_coding/Experiments/studies/smoke_*.yaml`, `pilot_*.yaml`, `formal_*.yaml` | Keep trackable. | Study contracts remain versioned. |
| Local diagnostic manifest | `work2_coding/Experiments/studies/diagnostic_actual_menu.yaml` | Ignore. | Local diagnostic contract, not a formal evidence contract. |
| Legacy tracked checkpoints | `work2_coding/Experiments/Parcelpoint_py/pricing/*/rundefault/1234/Checkpoints/*.pt` | Keep as existing tracked legacy assets for now; do not use as Phase 09+ evidence unless provenance sidecars and hashes are created by later phases. | Historical risk documented; not evidence-ready for attention claims. |
| Deleted user documents | None observed. | No restore/remove decision needed. | No user-facing document deletion found. |
| Other local state | None observed beyond ignored caches/outputs. | No action. | Classified. |

## Ignore Policy

Root `.gitignore` now covers:
- Python caches and local test/tool caches.
- Virtual environments.
- Editor and OS temporary files.
- LaTeX build byproducts.
- Raw local experiment outputs.
- Local model/checkpoint binaries by default.
- Generated planning reports under `.planning/reports/`.

`work2_coding/.gitignore` remains the runtime-local layer. It now explicitly keeps study manifests trackable while ignoring local runtime outputs and the diagnostic actual-menu manifest.

Important non-ignored paths:
- `.planning/phases/`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `artifacts/`
- `work2_coding/artifacts/`
- `work2_coding/Experiments/studies/{smoke,pilot,formal}_*.yaml`

## Generated Artifact Policy

Track:
- Lightweight review-facing artifact snapshots.
- Status JSON files.
- Metadata sidecars.
- Tables and figures intended for manuscript review.
- Study manifests and contract files.

Keep local/ignored by default:
- Raw run directories.
- Python caches.
- Virtual environments.
- Temporary files.
- Generated planning summaries under `.planning/reports/`.
- Checkpoint binaries unless a later formal archive policy explicitly tracks them with sidecars and hashes.

Checkpoint rule:
- Phase 09+ pilot/formal checkpoints must be real trained weights with sidecars and hashes.
- Missing, mismatched, random-weight, or sidecar-free checkpoints must not support pilot/formal claims.

## Evidence Provenance Gate

Phase 09+ evidence runs should report:
- `git_dirty=false` when possible.
- `git_dirty=true` only when narrowly documented and limited to known local-output exceptions.
- commit hash or git marker.
- checkpoint path and hash when checkpoints are required.
- explicit checkpoint load status.
- placeholder status.

Evidence is not claim-ready when:
- rows are placeholder-only.
- checkpoint provenance is missing or failed.
- paired replay is incomplete.
- git dirty state is unexplained.
- primary paired attention delta does not support the intended claim.

## Claim Honesty Gate

The paper target is attention-enhanced DSPO improving original DSPO. If pilot/formal evidence does not support that conclusion, Phase 10+ and Phase 13 artifacts must mark the claim as `failed`, `blocked`, or `not_allowed`. They must not convert unsupported results into positive claim language.

The current v2.0 generated summary already indicates the existing attention evidence is not claim-ready: smoke-only evidence and primary attention delta not positive. Phase 08 preserves that as a hard provenance/claim boundary for later phases.

