# Phase 13: Evidence Boundary Reconstruction - Context

**Gathered:** 2026-06-16T15:47:00+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 13 reconstructs the exact current evidence boundary for the v1.1
claim-ready resolution milestone before any gate repair, experiment rerun, or
manuscript writing. It must read and summarize planning, paper, result,
readiness, frozen-setting, and Phase 10 artifact-package evidence; identify
the concrete causes of current `claim_ready=false`; classify blockers into the
roadmap taxonomy; and write the three milestone deliverables under
`.planning/milestones/claim_ready_resolution/`.

This phase is an evidence audit and recommendation phase. It may classify
claims and causes as repair, rerun, or diagnostic-lock candidates, but it must
not execute repairs, regenerate claim-bearing artifacts, start final replay,
edit generated rows or paper artifacts, write manuscript claims, or formally
choose Path A/B/C. Final path selection remains Phase 16 authority.

</domain>

<decisions>
## Implementation Decisions

### Evidence Source Authority And Conflicts
- **D-01:** Use a dual-track audit when sources disagree. Phase 13 must not
  force one final authority between generated artifacts, root mirrors,
  planning summaries, and paper docs. It should record disagreements as part of
  the evidence boundary for later Phase 16 path decision.
- **D-02:** Present source disagreements in a conflict matrix. Each conflict
  should include source A, source B, conflicting field or wording, affected
  claim or blocker, temporary Phase 13 treatment, and downstream owner.
- **D-03:** Use layered reading. Read core authority/status files fully
  (`CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, package/source indexes, key
  `.planning/results/*.md`, and paper claim maps), then inspect source
  artifacts only when referenced by claims, blockers, or conflicts.
- **D-04:** Treat `work2_coding/artifacts/...` as the runtime source and root
  `artifacts/...` as a paper-facing mirror. If hashes or key fields match,
  merge the evidence record; if they differ, add the discrepancy to the
  conflict matrix.

### claim_ready=false Classification Granularity
- **D-05:** Use three-level traceability in
  `01_CLAIM_READY_FALSE_CAUSES.md`: top-level blocker category, affected claim
  id, then artifact id / original blocker reason.
- **D-06:** Merge repeated blockers into canonical causes while preserving
  affected artifact count and representative artifact ids. Do not expand every
  duplicate occurrence unless needed to explain a conflict.
- **D-07:** Give explicit repair-path recommendations at the claim/cause level.
  Each canonical cause or claim may be labeled as needing repair, rerun, or
  diagnostic lock, but Phase 13 must not execute those actions or formally
  choose Path A/B/C.
- **D-08:** Classify each claim using four states:
  `repair_candidate`, `rerun_candidate`, `diagnostic_lock_candidate`, and
  `already_safe_or_status_only`. Include evidence and downstream phase
  ownership for each classification.

### Deliverable Organization
- **D-09:** Use a mixed structure for the three deliverables.
  `01_EVIDENCE_BOUNDARY.md` should be narrative-first; `01_CLAIM_READY_FALSE_CAUSES.md`
  and `01_BLOCKER_TAXONOMY.md` should be audit-table-first.
- **D-10:** Organize `01_EVIDENCE_BOUNDARY.md` by timeline:
  Phase 3/4 -> Phase 5 -> Phase 8 -> Phase 9 -> Phase 10. The document should
  reconstruct how evidence accumulated and where blockers constrained it.
- **D-11:** In `01_BLOCKER_TAXONOMY.md`, use the roadmap's nine top-level
  blocker classes exactly: provenance/readiness, artifact-generation,
  empirical-performance, adaptive-window, random-baseline, sensitivity,
  tractability, semi-real-case, and manuscript-language. Subcategories are
  allowed under those top-level classes.
- **D-12:** Use strong cross-indexing across the three deliverables with stable
  ids such as `EB-001`, `CF-001`, and `BT-001`. Boundary items, canonical
  false-cause rows, and blocker-taxonomy rows should cross-reference each
  other.

### Phase 13 Recommendation Boundary
- **D-13:** Write recommendations but not authorization. Use a field such as
  `recommended_next_action = repair | rerun | diagnostic_lock`, and mark each
  recommendation as requiring Phase 14, Phase 15, or Phase 16 confirmation.
- **D-14:** Explicitly identify cases that should not be repaired by wording.
  Use labels such as `do_not_repair_by_wording` or
  `diagnostic_lock_candidate` when evidence scope itself is insufficient.
- **D-15:** For rerun recommendations, only mark `rerun_candidate` and explain
  why existing evidence may require Path B / rerun. Do not design experiments,
  split counts, seeds, manifests, or parameters in Phase 13.
- **D-16:** Do not write an overall Path A/B/C tendency in Phase 13. Classify
  claims and causes as repair/rerun/lock candidates, but leave the
  milestone-wide Path A/B/C decision to Phase 16.

### The Agent's Discretion
- The planner/researcher may choose exact table column names, as long as they
  preserve the decisions above and the three deliverables remain cross-indexed.
- The planner/researcher may choose the exact representative artifact ids for
  each canonical cause, provided affected artifact counts and raw reasons
  remain traceable.
- The planner/researcher may add small helper scripts for parsing JSON/status
  artifacts if useful, but Phase 13 outputs should remain planning documents,
  not generated empirical-result edits.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Milestone State
- `AGENTS.md` - Repository guardrails, active runtime assumption, and
  verification baseline.
- `.planning/PROJECT.md` - Current v1.1 milestone purpose, active runtime root,
  current claim boundary, and project-level no-overclaim decisions.
- `.planning/REQUIREMENTS.md` - v1.1 requirements, especially `EVID-01` through
  `EVID-04`.
- `.planning/ROADMAP.md` - Phase 13 goal, success criteria, deliverables, and
  blocker taxonomy categories.
- `.planning/STATE.md` - Current state, Phase 13 handoff, and current known
  evidence blockers.
- `.planning/research/SUMMARY.md` - TR-E service-menu framing and fallback
  conditional diagnostic contribution.

### Prior Phase Context
- `.planning/phases/08-sensitivity-and-robustness-experiments/08-CONTEXT.md` -
  Phase 8 sensitivity diagnostic/provisional boundaries.
- `.planning/phases/09-exact-versus-greedy-and-computational-tractability/09-CONTEXT.md` -
  Phase 9 tractability diagnostic/provisional boundaries.
- `.planning/phases/10-paper-artifact-generation/10-CONTEXT.md` - Phase 10
  package, claim guard, source-tier, and no-claim-upgrade decisions.

### Result And Gate Evidence
- `.planning/results/PHASE3_FORMAL_EVIDENCE_HANDOFF.md` - Phase 3 formal
  evidence handoff and selected run context.
- `.planning/results/RC_FORMAL_DIAGNOSIS.md` - Main RC diagnosis, random-menu
  profit advantage, adaptive/fixed equality, and claim classification.
- `.planning/results/RC_FORMAL_DIAGNOSTIC_TABLES.md` - Human-readable
  diagnostic tables for main RC evidence.
- `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv` - Policy-level summary rows
  for main RC diagnosis.
- `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv` - Paired split differences
  for main RC diagnosis.
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` - Dirty-git/provenance and
  artifact gate blockers.
- `.planning/results/FORMAL_FAILURE_DIAGNOSIS.md` - Formal failure/blocker
  context that must remain visible.
- `.planning/results/CALIBRATION_PROTOCOL.md` - Calibration/final-test
  separation and prohibited result-chasing boundaries.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` - Frozen final settings and
  final-rerun blocked status.
- `.planning/results/SENSITIVITY_SUMMARY.md` - Phase 8 diagnostic sensitivity
  source index and `claim_ready=false` boundary.
- `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` - Phase 9
  tractability evidence and exact-vs-greedy blocker.

### Paper And Claim Maps
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - Paper claim ladder, service menu
  formulation, table/figure plan, and non-claim boundaries.
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md` - Table/figure/claim source map.
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md` - Safe and prohibited claim language
  boundaries.
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md` - Manuscript structure to
  keep aligned with claim guard outcomes, without writing manuscript in Phase 13.

### Phase 10 Runtime Source And Mirror
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` -
  Runtime-source strict claim guard; core `claim_ready=false` input.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` -
  Runtime-source package status, blocker count, source-family status, and
  package claim-readiness.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json` -
  Runtime-source package index and source artifact inventory.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/SOURCE_INDEX.json` -
  Runtime-source source index.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json` -
  Runtime-source artifact-to-section mapping.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/claim_checklist.md` -
  Human-readable claim checklist.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/safe_language_boundaries.md` -
  Generated safe-language boundary.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` -
  Root mirror of the strict claim guard; compare with runtime source.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` -
  Root mirror of package status; compare with runtime source.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json` -
  Root mirror of package index; compare with runtime source.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/SOURCE_INDEX.json` -
  Root mirror of source index; compare with runtime source.

### Runtime Integration Points
- `work2_coding/Src/paper_artifacts.py` - Phase 10 package index and status
  builder.
- `work2_coding/Src/manuscript_claims.py` - Strict claim guard construction
  and safe/forbidden language materialization.
- `work2_coding/Src/artifact_status.py` - Artifact classification logic.
- `work2_coding/Src/artifact_builder.py` - Main robust-menu artifact builder
  and generated table/figure/status integration.
- `work2_coding/scripts/build_phase10_paper_artifacts.py` - Phase 10 package
  builder CLI.
- `work2_coding/scripts/test_phase10_paper_artifacts.py` - Phase 10 package
  test surface.
- `work2_coding/scripts/test_manuscript_claim_guard.py` - Claim guard test
  surface.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/paper_artifacts.py`: Existing Phase 10 package builder and
  likely best source for interpreting package roles, source families, package
  tiers, missing artifacts, and mirror/source expectations.
- `work2_coding/Src/manuscript_claims.py`: Existing strict claim guard logic;
  use it to understand how claim ids, blocker reasons, safe language, and
  forbidden language are produced.
- `work2_coding/Src/artifact_status.py`: Artifact gate classifier; use it to
  separate claim-ready, diagnostic, incomplete, and blocked status causes.
- `work2_coding/Src/artifact_builder.py`: Main robust-menu artifact source for
  core RC artifacts that Phase 10 indexes.
- `work2_coding/scripts/test_phase10_paper_artifacts.py` and
  `work2_coding/scripts/test_manuscript_claim_guard.py`: Existing tests that
  define current package and claim guard contracts.

### Established Patterns
- Active runtime root is `work2_coding/`; do not create or rely on `ooh_code/`.
- Generated evidence under `work2_coding/outputs/`, `work2_coding/artifacts/`,
  and root `artifacts/` must not be hand-edited to change conclusions.
- Paper-facing claims must align with generated `CLAIM_GUARD.json` and paper
  claim maps. Phase 13 may audit and recommend but may not upgrade claims.
- Phase 8 and Phase 9 evidence remain `diagnostic_provisional_blocked`.
- Phase 7 case-study material remains scaffold-only and cannot validate
  results.
- `mainline_random_menu` currently outperforms `mainline_optimized_adaptive`
  on mean net profit, and `mainline_optimized_adaptive` equals
  `mainline_optimized_fixed_window` across tracked metrics; Phase 13 should
  preserve these as evidence-boundary facts, not repair them by wording.

### Integration Points
- The Phase 13 deliverables should be written under
  `.planning/milestones/claim_ready_resolution/`.
- The deliverables should reference runtime source files and root mirror files
  separately where needed, then merge only when key fields match.
- If helper parsing is used, it should read JSON/status artifacts and produce
  planning-side tables; it must not edit generated package files.
- Minimum verification after planning should include the import smoke from
  `work2_coding/` if Phase 13 or downstream phases touch runtime-adjacent
  parsing code.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four gray areas for discussion.
- Evidence authority: dual-track audit, conflict matrix, layered reading, and
  runtime-source/mirror consistency handling are locked.
- `claim_ready=false` causes: three-level traceability, canonical-cause
  de-duplication, explicit recommended next action, and four-state claim
  classification are locked.
- Deliverable shape: `01_EVIDENCE_BOUNDARY.md` should be timeline narrative;
  `01_CLAIM_READY_FALSE_CAUSES.md` and `01_BLOCKER_TAXONOMY.md` should be
  audit-table-first; all three should be strongly cross-indexed.
- Recommendation boundary: Phase 13 may recommend repair/rerun/diagnostic lock
  and identify `do_not_repair_by_wording` cases, but must not authorize action,
  design rerun parameters, or choose the overall Path A/B/C.

</specifics>

<deferred>
## Deferred Ideas

- Phase 14 owns detailed gate repair planning and may confirm or reject
  Phase 13 `repair_candidate` recommendations.
- Phase 15 owns source-row and code-path diagnosis for random-menu profit
  advantage and adaptive/fixed-window equality.
- Phase 16 owns the final Path A/B/C decision.
- Phase 17 owns execution of the selected path and any artifact regeneration or
  final replay authorized by Phase 16.

</deferred>

---

*Phase: 13-Evidence Boundary Reconstruction*
*Context gathered: 2026-06-16T15:47:00+08:00*
