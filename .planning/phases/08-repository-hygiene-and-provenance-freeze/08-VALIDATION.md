# Phase 08 Validation

**Status:** Passed
**Date:** 2026-06-11

## Validation Question

Does Phase 08 reduce provenance risk enough for Phase 09 checkpoint training and later evidence runs to proceed without hiding unsupported claims?

## Result

Passed.

The repository now has explicit ignore policy, classified local state, a documented generated-artifact policy, and an evidence gate that requires clean or narrowly documented dirty provenance. The user instruction is preserved as a hard claim-honesty gate: if attention evidence does not support the desired conclusion, later phases must mark the claim failed, blocked, or not allowed.

## Checks

| Risk | Validation |
|---|---|
| Untracked generated planning report could pollute evidence provenance | `.planning/reports/` is classified as local generated planning output and ignored. Canonical planning docs remain tracked. |
| Virtual environment was tracked as source | `work2_coding/venv/` was removed from Git index and ignored while preserving local files. |
| Ignore rules could hide future study manifests | Ignore patterns were narrowed so `work2_coding/Experiments/studies/{smoke,pilot,formal}_*.yaml` remain trackable. |
| Raw outputs could be mistaken for evidence artifacts | Raw output roots are ignored; review-facing artifact bundles remain trackable. |
| Checkpoint binaries could support claims without provenance | New checkpoint binaries are ignored by default; Phase 09+ must add sidecars and hashes before checkpoints can support evidence. |
| Unsupported attention results could be softened into positive language | Claim gate requires failed/blocked/not_allowed status when paired evidence is missing, placeholder-only, or directionally unsupported. |

## Residual Risks

- Legacy tracked checkpoint `.pt` files remain in historical experiment directories. They are documented as not evidence-ready for Phase 09+ claims unless later phases add sidecars and hashes or replace them with real shared checkpoints.
- `.planning/reports/MILESTONE_SUMMARY-v2.0.md` contains text-encoding damage and remains local/ignored rather than canonical.

## Decision

Phase 09 may proceed. The current evidence still does not support an attention-improves-DSPO paper claim; that is not a Phase 08 failure because Phase 08 only freezes provenance before producing new empirical evidence.

