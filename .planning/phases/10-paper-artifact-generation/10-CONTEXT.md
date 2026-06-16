# Phase 10: Paper Artifact Generation - Context

**Gathered:** 2026-06-16T11:43:00+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 10 generates the paper-facing artifact bundle for the TR-E service-menu
paper: tables, figures, source indexes, manuscript-frame outlines, and a strict
`CLAIM_GUARD.json`. It should organize existing evidence into a minimal main
paper artifact package plus a diagnostic appendix package, with every artifact
generated from rows, artifact builders, status gates, or planning-side scaffold
contracts.

This phase is not a new experiment phase, not a final formal replay, not a
gate-cleanup phase, not a semi-real case execution phase, and not Phase 11
manuscript writing. It must not upgrade abstract/conclusion claims. Current
outputs remain `claim_ready=false` unless every relevant readiness, artifact,
and claim gate explicitly passes. Phase 8 and Phase 9 outputs are diagnostic
boundary evidence; Phase 7 case materials are scaffold-only and contain no
case-study result evidence.

</domain>

<decisions>
## Implementation Decisions

### Evidence Source Boundary
- **D-01:** Include all available evidence sources in the Phase 10 artifact
  index, but stratify them by evidentiary tier.
- **D-02:** Treat the main RC formal/diagnostic artifacts as the core empirical
  evidence source, while preserving existing readiness and artifact blockers.
- **D-03:** Include Phase 8 sensitivity artifacts as
  `diagnostic_provisional_blocked` boundary evidence only.
- **D-04:** Include Phase 9 tractability artifacts as
  `diagnostic_provisional_blocked` evidence, with the exact-vs-greedy quality
  claim explicitly blocked because the configured large scales did not trigger
  greedy fallback.
- **D-05:** Include Phase 7 case-study materials only as
  `scaffold_only_no_result_evidence`. They may appear in a source/index or
  appendix placeholder, but not as a result table, result figure, or case
  validation claim.

### Artifact Package Structure
- **D-06:** Build a minimal main-paper artifact package plus a diagnostic
  appendix package.
- **D-07:** The minimal main-paper package should cover experimental design,
  main RC results, product/time-window ablations where generated rows support
  them, and core claim-guard references.
- **D-08:** The diagnostic appendix package should cover Phase 8 sensitivity,
  Phase 9 tractability, blocked/gate notes, and case-scaffold placeholders.
- **D-09:** Every artifact must carry source paths, status, claim linkage, and
  enough metadata to distinguish main-paper, appendix, diagnostic, blocked, and
  scaffold-only outputs.

### Claim Guard Strictness
- **D-10:** Generate a strict per-claim `CLAIM_GUARD.json`, not only an overall
  gate status.
- **D-11:** Each claim entry should include at minimum `claim_id`,
  `claim_text`, `support_status`, `source_artifacts`, `blocker_reasons`,
  `safe_language`, `forbidden_language`, `manuscript_allowed`, and
  `claim_ready`.
- **D-12:** Supported language must be conservative and artifact-bound.
  Forbidden language must explicitly block universal dominance,
  claim-ready superiority, real passenger behavior, case-study validation, and
  near-optimal greedy statements unless the corresponding evidence exists.
- **D-13:** Overall `claim_ready` should remain `false` unless all formal
  readiness, artifact status, and claim-guard conditions pass. Current Phase 10
  planning should assume `claim_ready=false`.

### Manuscript Frame Depth
- **D-14:** Generate artifact-facing manuscript frame outputs only:
  result/method/experiment outlines, artifact-to-section map, source index, and
  claim checklist.
- **D-15:** Do not write manuscript body paragraphs, abstract/conclusion
  upgrades, or final narrative claims in Phase 10.
- **D-16:** Phase 10 may create safe-language boundaries that Phase 11 can use,
  but should not create polished manuscript prose snippets.

### The Agent's Discretion
- The planner may choose exact filenames and directory layout for the main
  paper package and diagnostic appendix package, provided the package tier and
  claim boundary are machine-readable.
- The planner may extend existing general artifact builders or add
  Phase 10-specific orchestration helpers, provided paper-facing outputs flow
  from rows/status artifacts/builders and no generated result rows are edited by
  hand.
- The planner may choose exact claim IDs and section labels, provided each
  claim maps to source artifacts and a safe/forbidden language boundary.
- The planner may choose exact tests, but should include script-style checks
  for artifact source metadata, claim-guard strictness, case-scaffold
  no-result labeling, and `claim_ready=false` preservation.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Current project purpose, active runtime root,
  validated Phase 8/9 diagnostic status, and no-overclaim boundary.
- `.planning/REQUIREMENTS.md` - Requirements `ART-01` and `ART-02`, plus
  completed `COMP-01`/`COMP-02` diagnostic limitations.
- `.planning/ROADMAP.md` - Phase 10 goal and success criteria for tables,
  figures, row-generated outputs, and `CLAIM_GUARD.json`.
- `.planning/STATE.md` - Current position, Phase 10 handoff, runtime root, and
  explicit Phase 8/9 diagnostic blockers.
- `AGENTS.md` - Repository instructions, active runtime assumption,
  verification baseline, and research guardrails.

### Paper And Claim Context
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - Paper claim ladder, service menu
  framing, table/figure families, exact/greedy definitions, and non-claim
  boundaries.
- `.planning/results/RC_FORMAL_DIAGNOSIS.md` - Main RC diagnosis and
  conditional/unsupported claim classification.
- `.planning/results/SENSITIVITY_SUMMARY.md` - Phase 8 diagnostic sensitivity
  source index, boundary conclusions, and `claim_ready=false` status.
- `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` - Phase 9
  tractability source index, 15-row coverage, and exact-vs-greedy blocker.
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` - Dirty-git/provenance and
  artifact blockers that Phase 10 must keep visible.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` - Frozen settings and
  final-rerun blocked status; reference only, not a final replay trigger.

### Prior Phase Context
- `.planning/phases/07-case-study-implementation/07-CONTEXT.md` - Case-study
  scaffold-only status, mandatory semi-real/simulated labels, and no-result
  evidence boundary.
- `.planning/phases/08-sensitivity-and-robustness-experiments/08-CONTEXT.md`
  - Phase 8 diagnostic/provisional sensitivity decisions and artifact boundary.
- `.planning/phases/09-exact-versus-greedy-and-computational-tractability/09-CONTEXT.md`
  - Intended Phase 9 exact-greedy contract and claim-narrowing rules.
- `.planning/phases/09-exact-versus-greedy-and-computational-tractability/09-VERIFICATION.md`
  - Verified Phase 9 diagnostic closeout and blocked exact-vs-greedy claim.

### Runtime And Artifact Integration Points
- `work2_coding/Src/artifact_builder.py` - Existing main artifact aggregation,
  table, figure, metadata, and status integration point.
- `work2_coding/Src/artifact_status.py` - Artifact classification and
  claim-ready/diagnostic/blocked status helpers.
- `work2_coding/Src/manuscript_claims.py` - Existing manuscript frame and claim
  guard logic to extend or wrap for strict per-claim mapping.
- `work2_coding/Src/sensitivity_analysis.py` - Phase 8 artifact and summary
  helper; source for diagnostic appendix integration.
- `work2_coding/Src/computational_tractability.py` - Phase 9 tractability
  artifact and summary helper; source for diagnostic appendix integration.
- `work2_coding/scripts/build_artifacts.py` - General artifact builder CLI.
- `work2_coding/scripts/build_phase8_sensitivity_artifacts.py` - Phase 8
  artifact builder CLI.
- `work2_coding/scripts/build_phase9_tractability_artifacts.py` - Phase 9
  artifact builder CLI.
- `work2_coding/scripts/build_manuscript_frame.py` - Existing manuscript frame
  and `CLAIM_GUARD.json` CLI.
- `work2_coding/scripts/test_artifact_builder.py` - Existing artifact builder
  tests and table/figure expectations.
- `work2_coding/scripts/test_artifact_gates.py` - Existing artifact status and
  claim-ready gate tests.
- `work2_coding/scripts/test_manuscript_claim_guard.py` - Existing manuscript
  claim guard test surface.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/artifact_builder.py`: already generates core artifact
  tables/figures/status files from normalized rows; likely the main-paper
  artifact package should build on this rather than bypassing it.
- `work2_coding/Src/manuscript_claims.py`: already writes manuscript-frame
  artifacts and `CLAIM_GUARD.json`; Phase 10 should extend this toward strict
  per-claim mapping instead of inventing an unrelated claim system.
- `work2_coding/Src/sensitivity_analysis.py`: already emits Phase 8 aggregate
  tables, figures, metadata sidecars, and diagnostic status.
- `work2_coding/Src/computational_tractability.py`: already emits Phase 9
  aggregate tables, build-time figure/status artifacts, metadata sidecars, and
  blocked claim boundary.
- `.planning/data/case_studies/`: contains planning-side case scaffold
  contracts and validation outputs that can be indexed as scaffold-only
  references, not result evidence.

### Established Patterns
- Active runtime root is `work2_coding/`; older `.planning/codebase/`
  references to `ooh_code/` are stale historical memory.
- Experiments and paper artifacts are generated from manifests, normalized
  rows, builder outputs, and metadata. Generated rows/tables/figures must not
  be hand-edited to change conclusions.
- Artifact outputs should include metadata sidecars, source paths, status
  reasons, and claim readiness fields.
- Phase 8 and Phase 9 artifacts deliberately remain
  `diagnostic_provisional_blocked`; Phase 10 should aggregate that status, not
  overwrite it.
- Tests are direct script-style Python tests under `work2_coding/scripts/`.

### Integration Points
- Add or extend a Phase 10 orchestration CLI under `work2_coding/scripts/` if
  the existing builders need a single command to assemble main-paper and
  diagnostic appendix packages.
- Extend `work2_coding/Src/manuscript_claims.py` or a focused helper so
  `CLAIM_GUARD.json` can record per-claim source artifacts, blockers,
  safe language, and forbidden language.
- Generate Phase 10 source indexes and artifact-to-section maps under
  `work2_coding/artifacts/work2_robust_menu/` or a clearly named Phase 10
  subdirectory, then mirror only lightweight committed artifacts if needed.
- Add tests for strict claim guard schema, all-source stratification,
  no-result case scaffold labeling, and no claim-ready upgrade.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four gray areas for discussion and chose option `1`
  for each.
- Evidence source decision: include all evidence sources, but stratify them by
  `claim-ready`, `diagnostic/provisional`, and `scaffold-only` status.
- Artifact package decision: generate a minimal main-paper package plus a
  diagnostic appendix package.
- Claim guard decision: use strict per-claim mapping with source artifacts,
  blocker reasons, safe language, forbidden language, and manuscript
  permission fields.
- Manuscript frame decision: generate artifact-facing frame only; do not write
  body text or polished claim prose in Phase 10.

</specifics>

<deferred>
## Deferred Ideas

- Formal provenance/artifact gate cleanup remains outside Phase 10 unless a
  later phase explicitly targets it.
- Final formal replay remains blocked by Phase 5 gate cleanup requirements.
- Semi-real case-study data fetching, matrix construction, replay, result
  artifacts, and manuscript validation claims remain deferred.
- Phase 11 manuscript structure and writing plan may consume Phase 10 frame
  outputs, but Phase 10 should not write manuscript body sections.

</deferred>

---

*Phase: 10-Paper Artifact Generation*
*Context gathered: 2026-06-16T11:43:00+08:00*
