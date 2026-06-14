# Phase 4 Research: Mainline Artifact Pipeline And Claim Guard

**Date:** 2026-06-14
**Runtime root:** `work2_coding/`
**Status:** Complete

## Research Summary

Phase 4 can be implemented by extending the existing artifact pipeline instead
of creating a parallel builder. The current code already has the right shape:

- `work2_coding/Src/artifact_builder.py` loads normalized rows and study
  summaries, aggregates by policy, emits JSON/CSV summaries, LaTeX tables,
  figure outputs or incomplete-status sidecars, sidecar metadata,
  `ARTIFACT_STATUS.json`, README, ranking JSON, and optional mirrors.
- `work2_coding/Src/artifact_status.py` centralizes artifact eligibility and
  environment provenance collection.
- `work2_coding/Src/manuscript_claims.py` generates manuscript-frame Markdown
  and `CLAIM_GUARD.json` from artifact status.
- `work2_coding/scripts/build_artifacts.py` and
  `work2_coding/scripts/build_manuscript_frame.py` are thin CLI wrappers.
- `work2_coding/scripts/test_artifact_gates.py` already provides synthetic run
  helpers and focused gate tests.

## Key Findings

### Artifact Status

`classify_artifact()` already blocks many unsafe cases, including placeholder,
failed, blocked, contract-only, diagnostic, no-filter-only, missing checkpoint,
and missing formal dependency snapshot cases. Phase 4 needs to tighten tier
semantics so smoke cannot become claim-ready and formal loaded checkpoint
provenance is required when formal claim-ready artifacts are requested.

### Ranking

`aggregate_by_policy()` currently marks rows as rank-eligible if they are not
diagnostic and not cost-bound. That is too broad for the V1 mainline contract:
`mainline_no_menu` is a baseline/boundary policy and should be excluded from
`recommended_policy_ranking.json`, while six operational mainline strategies
remain ranking-eligible.

### Manuscript Frame

`write_manuscript_frame()` is currently separate from `build_artifacts()`. Phase
4 should either integrate it into the artifact build result or add an explicit
tested wrapper path that builds both the artifact bundle and manuscript frame
from the same `ARTIFACT_STATUS.json`.

### Provenance

Sidecars already include source run, manifest hash, checkpoint summary, and git
provenance. Phase 4 should ensure generated status and manuscript-frame outputs
retain tier-specific claim readiness, dependency snapshot state, and source run
metadata.

## Recommended Approach

1. Tighten `classify_artifact()` tier and checkpoint gates first.
2. Make ranking eligibility mainline-aware in `artifact_builder.py`.
3. Integrate or orchestrate manuscript-frame generation as part of the full
   Phase 4 artifact bundle.
4. Extend tests around synthetic smoke, pilot, formal, no-menu, mainline ranking,
   dependency snapshot, checkpoint status, and manuscript claim guard.
5. Verify with smoke actual output in a temporary or phase verification output
   directory before writing Phase 4 summary.

## Risks

- Existing artifact labels still mention older robust-policy comparisons in some
  prose. Update generated frame text carefully without making unsupported claims.
- Formal rows in synthetic tests must not accidentally pass without loaded
  checkpoint status and dependency snapshot.
- Mirrored artifacts should not copy raw normalized rows or manifest snapshots.
- Do not use generated smoke outputs as empirical superiority claims.

## RESEARCH COMPLETE
