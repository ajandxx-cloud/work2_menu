# Phase 5: Manuscript Framing And Claim Guard - Context

**Gathered:** 2026-06-11T15:35:11+08:00
**Status:** Ready for planning
**Mode:** auto-selected from existing project evidence and GSD yolo/auto-advance settings

<domain>
## Phase Boundary

Phase 5 translates the verified Work2 pipeline into restrained, paper-ready manuscript support. It should produce method, experiment, and result outlines plus an explicit claim checklist that reads Phase 4 artifact status before allowing empirical claims.

This phase does not fabricate empirical results, hand-edit generated result rows, create new robust-menu algorithm behavior, supply missing checkpoints, or upgrade the current blocked artifact bundle into claim-ready evidence. If artifact status remains blocked, the manuscript framing must say the pipeline and diagnostic artifacts are ready while pilot/formal empirical claims are still gated.

</domain>

<decisions>
## Implementation Decisions

### Manuscript Scope
- **D-01:** Phase 5 should generate manuscript support documents from verified project state and artifact status, not from manual row edits or unverifiable prose.
- **D-02:** The method outline must cover service bundles, displayed menu decisions, outside option, robust time-window handling, MNL choice, pricing, and exact-small/greedy-large solver behavior.
- **D-03:** The experiment outline must cover scenarios, baselines, metrics, paired replay protocol, seeds, splits, checkpoint handling, and uptake regimes.
- **D-04:** The result outline may describe planned/diagnostic result families, but current empirical wording must be blocked when `claim_ready`, `pilot_claim_ready`, or `formal_claim_ready` is false.

### Claim Guard
- **D-05:** Claims allowed before claim-ready evidence are limited to implemented framework, reproducible contracts, diagnostic artifact pipeline, robust-pruning mechanism, solver auditability, and explicit blocker transparency.
- **D-06:** Claims blocked before claim-ready evidence include universal dominance, real passenger behavioral validation, no-filter operational recommendation, full dynamic-system exact optimality, and completed pilot/formal effect-size conclusions.
- **D-07:** `no_filter_diagnostic` may be discussed only as a diagnostic upper bound or stress test, not as an operational policy recommendation.
- **D-08:** Missing or failed checkpoint provenance must appear in the checklist and limitations text whenever artifact status records it.

### Output Contract
- **D-09:** Outputs should live under `work2_coding/artifacts/work2_robust_menu/manuscript/` and be mirrored to `artifacts/work2_robust_menu/manuscript/` for review, matching the Phase 4 artifact pattern.
- **D-10:** A machine-readable claim guard JSON should sit beside Markdown outlines so later manuscript tooling can fail closed without parsing prose.
- **D-11:** Tests should prove blocked Phase 4 status prevents empirical claims while still allowing framework and pipeline claims.

### the agent's Discretion
- The agent may choose exact filenames and helper boundaries as long as the generated artifacts and tests preserve the decisions above.
- The agent may keep the first implementation Markdown/JSON based rather than introducing LaTeX manuscript files, because no current `work2_coding/manuscript/` tree exists.
- The agent may use the current blocked artifact bundle as the primary fixture and synthetic claim-ready status only inside focused tests.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Scope
- `AGENTS.md` - Active runtime and research guardrails.
- `.planning/PROJECT.md` - Core value, validated phases, scope fences, and no-filter diagnostic framing.
- `.planning/REQUIREMENTS.md` - Phase 5 requirements `PAPER-01` through `PAPER-04`.
- `.planning/ROADMAP.md` - Phase 5 success criteria.
- `.planning/STATE.md` - Current phase state and prior phase completion status.
- `.planning/research/SUMMARY.md` - Project watch-outs for checkpoints, no-filter, and placeholder artifacts.

### Prior Evidence
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-04-SUMMARY.md` - Robust ETA modes, objective risk penalties, and solver diagnostics available for methods text.
- `.planning/phases/03-experiment-contracts-and-fair-replay/03-VERIFICATION.md` - Study contracts, baselines, paired replay, normalized row schema, and uptake regime verification.
- `.planning/phases/04-evidence-and-artifacts/04-VERIFICATION.md` - Artifact pipeline verification and current blocked/non-claim-ready status.
- `.planning/phases/04-evidence-and-artifacts/04-03-SUMMARY.md` - Claim-ready classifier, sidecar metadata, and provenance gate behavior.

### Current Runtime and Artifacts
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Robust menu construction, ETA filter modes, objective penalties, and exact/greedy diagnostics.
- `work2_coding/Src/experiment_contracts.py` - Study manifest validation, policy/baseline contracts, checkpoint requirements, and uptake-regime validation.
- `work2_coding/Src/paired_replay.py` - Normalized row fields and paired replay/fairness metadata.
- `work2_coding/Src/artifact_status.py` - Claim-ready, diagnostic, incomplete, and blocked artifact status classifier.
- `work2_coding/Src/artifact_builder.py` - Artifact builder outputs and sidecar metadata.
- `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` - Current artifact status and blockers.
- `artifacts/work2_robust_menu/ARTIFACT_STATUS.json` - Mirrored artifact status consumed by reviewer-facing outputs.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/artifact_status.py` already centralizes claim readiness concepts and should be the source of truth for Phase 5 status interpretation.
- `work2_coding/artifacts/work2_robust_menu/ARTIFACT_STATUS.json` already records blockers, claim readiness flags, policies, uptake regimes, checkpoint statuses, and generated artifact paths.
- Existing script tests under `work2_coding/scripts/test_*.py` use direct `python scripts/test_*.py` execution and temporary directories.

### Established Patterns
- Raw runs stay under `work2_coding/outputs/`; lightweight review artifacts are mirrored under root `artifacts/`.
- Artifact status can be blocked but still useful for reviewer-visible limitation and provenance text.
- Diagnostic policies are allowed in tables only with diagnostic labeling and exclusion from recommended-policy ranking.
- `.planning/codebase/` maps mention `ooh_code/`; treat those maps as historical context unless a path is revalidated under `work2_coding/`.

### Integration Points
- A new script can read `ARTIFACT_STATUS.json`, emit Markdown/JSON manuscript support under an artifact subdirectory, and mirror the same files to root artifacts.
- Tests can use temporary status JSON files and the current blocked status to verify claim boundaries.

</code_context>

<specifics>
## Specific Ideas

- Generate `method_outline.md`, `experiment_outline.md`, `result_outline.md`, `claim_checklist.md`, and `CLAIM_GUARD.json`.
- Include a `current_evidence_status` section naming `blocked`, `claim_ready=false`, `pilot_claim_ready=false`, `formal_claim_ready=false`, and missing checkpoint blockers when present.
- Treat result sections as "planned report structure" or "diagnostic/status output" until non-placeholder claim-ready evidence exists.
- Include a compact allowed/blocked claim table for quick manuscript review.

</specifics>

<deferred>
## Deferred Ideas

- Writing final LaTeX manuscript prose is deferred until artifact status is claim-ready or the user explicitly wants a draft with blocked-evidence caveats.
- Running pilot/formal studies is deferred until required checkpoint provenance is available.
- Attention-based choice/scoring and real passenger behavioral validation remain outside v1.

</deferred>

---

*Phase: 05-Manuscript Framing And Claim Guard*
*Context gathered: 2026-06-11T15:35:11+08:00*
