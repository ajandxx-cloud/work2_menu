# Phase 4: Mainline Artifact Pipeline And Claim Guard - Context

**Gathered:** 2026-06-14
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase makes the artifact and claim pipeline consume normalized-row-v2
outputs from the seven-tag Work2 V1 mainline family. It should generate
artifact bundles, provenance/status sidecars, manuscript-frame claim guards, and
mainline-aware ranking/baseline outputs from regenerated study rows.

This phase does not run formal replay, train formal checkpoints, edit manuscript
source, or hand-edit generated result rows. Formal claim-ready evidence remains
gated by checkpoint provenance and dependency snapshots.

</domain>

<decisions>
## Implementation Decisions

### Artifact Output Scope

- **D-01:** Phase 4 should generate the full artifact bundle, not only status
  stubs. The bundle includes aggregates, LaTeX tables, figures or figure-status
  sidecars, `ARTIFACT_STATUS.json`, README, and metadata sidecars.
- **D-02:** Phase 4 should also generate the manuscript frame and machine-readable
  claim guard from `ARTIFACT_STATUS.json`.
- **D-03:** Manuscript-frame outputs are allowed only as generated frame artifacts
  under artifact directories. Phase 4 must not edit manuscript source text or
  paper result rows by hand.

### Claim-Ready Gates

- **D-04:** Smoke outputs are diagnostic/status evidence only and must not be
  claim-ready even when all rows complete.
- **D-05:** Pilot outputs may be claim-ready when rows are completed,
  non-placeholder, non-diagnostic, non-filter-only, and checkpoint requirements
  pass.
- **D-06:** Formal outputs require both a dependency snapshot and loaded
  checkpoint provenance before they can be claim-ready.
- **D-07:** Claim guards must continue to block diagnostic, failed, blocked,
  placeholder-only, no-filter-only, contract-only, incomplete, and bad-checkpoint
  rows.
- **D-08:** Checkpoint load status and dependency provenance must be visible in
  status JSON and sidecar metadata, not only implicit in command logs.

### Ranking And Baseline Tables

- **D-09:** Recommended-policy ranking should include operational comparison
  strategies from the seven-tag mainline family except `mainline_no_menu`.
- **D-10:** `mainline_no_menu` should be reported in a baseline or boundary table,
  not in the recommended-policy ranking.
- **D-11:** The ranking-eligible mainline tags are:
  `mainline_fixed_menu`, `mainline_random_menu`, `mainline_optimized_m`,
  `mainline_optimized_mw`, `mainline_optimized_fixed_window`, and
  `mainline_optimized_adaptive`.
- **D-12:** Optimized product ablations (`mainline_optimized_m` and
  `mainline_optimized_mw`) remain ranking-eligible because they answer the V1
  product-composition question, even though their `pricing_mode` is
  `no_pricing`.
- **D-13:** Existing no-filter diagnostic policies, cost-bound-only policies, and
  legacy diagnostic rows remain excluded from recommended ranking.

### the agent's Discretion

The agent may choose the exact artifact file names and helper boundaries as long
as the generated bundle remains manifest/provenance-driven, test-covered, and
compatible with the existing `build_artifacts.py` and `build_manuscript_frame.py`
entry points.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning And Prior Phases

- `.planning/PROJECT.md` - Work2 V1 scope, guardrails, and seven-tag mainline family.
- `.planning/REQUIREMENTS.md` - Artifact, claim, row, and provenance requirements.
- `.planning/ROADMAP.md` - Phase 4 boundary and success criteria.
- `.planning/STATE.md` - Current phase position and recent verification.
- `.planning/repository_audit.md` - Active runtime root, stale path mapping, reusable robust-menu inventory, and artifact trust notes.
- `.planning/phases/02-service-product-contract/02-VERIFICATION.md` - Verified service-product and row-v2 foundation.
- `.planning/phases/03-mainline-comparison-contract/03-VERIFICATION.md` - Verified seven-tag mainline smoke replay and Phase 4 handoff.

### Artifact And Claim Code

- `work2_coding/Src/artifact_builder.py` - Current artifact bundle generation, ranking, tables, figures, status JSON, sidecars, and mirror behavior.
- `work2_coding/Src/artifact_status.py` - Artifact eligibility classification, checkpoint gates, and dependency provenance helper.
- `work2_coding/Src/manuscript_claims.py` - Manuscript frame and claim guard generation from artifact status.
- `work2_coding/scripts/build_artifacts.py` - CLI entry point for artifact generation.
- `work2_coding/scripts/build_manuscript_frame.py` - CLI entry point for manuscript-frame and claim-guard generation.

### Runtime Rows And Tests

- `work2_coding/Src/paired_replay.py` - normalized-row-v2 schema and method composition.
- `work2_coding/Src/study_execution.py` - completed/failed/blocked row generation and provenance metadata.
- `work2_coding/scripts/test_artifact_gates.py` - Existing artifact eligibility, ranking exclusion, checkpoint, dependency snapshot, and sidecar tests.
- `work2_coding/scripts/test_smoke_study_rows.py` - Smoke row-v2 expectations for mainline outputs.
- `work2_coding/scripts/test_experiment_contracts.py` - Mainline manifest contract validation.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Paired fairness checks.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `build_artifacts()` already writes policy aggregates, CSV/JSON summaries,
  LaTeX tables, figures or incomplete figure-status files, ranking JSON,
  `ARTIFACT_STATUS.json`, README, and metadata sidecars.
- `classify_artifact()` already blocks empty rows, placeholder rows, failed or
  blocked rows, incomplete/contract-only rows, bad pilot/formal checkpoints,
  diagnostic run modes, diagnostic-only labels, no-filter-only rows, and formal
  claim-ready generation without dependency snapshot.
- `collect_environment_provenance()` already records Python, platform, package
  versions, and optional `pip freeze`.
- `write_manuscript_frame()` already emits method, experiment, result,
  checklist, and `CLAIM_GUARD.json` files from artifact status.
- `test_artifact_gates.py` already has synthetic study/run helpers that can be
  extended for mainline Phase 4 contracts without running expensive formal replay.

### Established Patterns

- Artifact generation is file-based and uses `normalized_rows.json`,
  `study_summary.json`, and `manifest_snapshot.yaml` from run directories.
- The current build CLI requires either `--study` or `--run-dir`.
- Diagnostic/incomplete artifacts are allowed only when callers pass
  `--allow-incomplete`; claim-ready mode raises if gates fail.
- Mirror output intentionally excludes raw normalized rows and manifest snapshots
  while copying lightweight status, aggregate, table, figure, and manuscript
  frame artifacts.

### Integration Points

- Update `aggregate_by_policy()` and ranking generation in
  `work2_coding/Src/artifact_builder.py` so `mainline_no_menu` is baseline-only
  and the six selected mainline tags are ranking-eligible when other gates pass.
- Update `classify_artifact()` in `work2_coding/Src/artifact_status.py` if smoke
  currently can become claim-ready or if formal dependency/checkpoint checks are
  not strict enough.
- Update `build_artifacts.py` only if CLI flags need clearer Phase 4 behavior.
- Update `manuscript_claims.py` if claim labels still describe old robust-policy
  families instead of the seven-tag mainline comparison.
- Extend script-style tests before relying on generated artifact outputs.

</code_context>

<specifics>
## Specific Ideas

- Full artifact bundle includes aggregates, tables, figures/status sidecars,
  `ARTIFACT_STATUS.json`, README, sidecar metadata, manuscript frame, and
  `CLAIM_GUARD.json`.
- Claim-ready gates:
  - smoke: diagnostic/status only
  - pilot: may be claim-ready if row and checkpoint gates pass
  - formal: dependency snapshot plus loaded checkpoint provenance required
- Recommended ranking excludes `mainline_no_menu`.
- Recommended ranking includes:
  - `mainline_fixed_menu`
  - `mainline_random_menu`
  - `mainline_optimized_m`
  - `mainline_optimized_mw`
  - `mainline_optimized_fixed_window`
  - `mainline_optimized_adaptive`
- `mainline_no_menu` belongs in baseline/boundary reporting.

</specifics>

<deferred>
## Deferred Ideas

- Formal actual replay and formal checkpoint training remain deferred to Phase 5
  or later evidence-readiness work.
- Manuscript source editing remains deferred until generated artifact and claim
  guards are in place.
- Attention-based choice/scoring remains V2/diagnostic only.

</deferred>

---

*Phase: 4-Mainline Artifact Pipeline And Claim Guard*
*Context gathered: 2026-06-14*
