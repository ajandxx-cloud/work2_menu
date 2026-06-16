# Phase 1: Repository And Evidence Boundary Audit - Context

**Gathered:** 2026-06-16
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase reconstructs the current repository, manuscript, planning, codebase-map, and generated-evidence boundary before any repair, final replay, artifact regeneration, or manuscript claim upgrade.

Phase 1 is a read-only audit phase. It may inspect file existence, git status, JSON summaries, package indexes, manuscript wording, and runtime import health. It must not run studies, rebuild artifacts, regenerate package status, modify generated rows, restore old planning files, or edit manuscript/evidence outputs.

The phase deliverables are:

- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`
- `.planning/milestones/tr_e_completion/M1_DECISION.md`

</domain>

<decisions>
## Implementation Decisions

### Canonical Evidence Source
- **D-01:** Treat `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` as the canonical generated paper artifact package.
- **D-02:** Treat root `artifacts/work2_robust_menu/phase10_paper_artifacts/` as a paper-facing mirror, not as an independent source of truth.
- **D-03:** Check mirror drift only for the four key JSON files: `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and `ARTIFACT_TO_SECTION_MAP.json`.
- **D-04:** For those four JSON files, record top-level fields, `source_family_status`, blocked claim IDs, and each claim's `support_status`. Do not copy entire large JSON files into the audit.

### Blocker Taxonomy And Traceability
- **D-05:** `M1_BLOCKER_LIST.md` should use a mixed format: a readable six-class summary in the body plus a traceable matrix.
- **D-06:** The six blocker classes are provenance/readiness, empirical performance, artifact packaging, manuscript language, case-study, and computational tractability.
- **D-07:** The traceable matrix should cover the Phase 10 package's 74 artifacts and the strict claim guard's 8 claims.
- **D-08:** Classify blockers automatically from package fields where possible, then add short human explanation for why each cluster belongs to its blocker class.

### Feasibility And Decision Wording
- **D-09:** Phase 1 should state a conditional evidence-path conclusion: the current generated package is not claim-ready and leans diagnostic-only, but Phase 2/3 still need to check whether clean provenance and valid frozen final settings make a legitimate final replay path possible.
- **D-10:** `M1_DECISION.md` should recommend that Phase 3 decide between a legitimate final replay and diagnostic lock, with the current package leaning diagnostic.
- **D-11:** Phase 1 should not itself run cleanup, rerun experiments, tune settings, or upgrade claims.

### Dirty Git And Deleted Legacy Files
- **D-12:** The current dirty git state, including regenerated planning files and deleted legacy planning/results files, should be recorded as part of the evidence boundary.
- **D-13:** Deleted legacy planning/results files are a provenance risk, not an automatic Phase 1 blocker. Current evidence is based on present generated packages and current workspace files.
- **D-14:** Do not restore or deeply mine deleted legacy files in Phase 1. Only inspect git history if a deleted file directly affects the current evidence boundary.
- **D-15:** `manuscript/main.tex` has been restored and should not be treated as missing. Phase 1 may read it only to identify possible claim-boundary wording issues and must not edit it.

### Allowed Audit Commands
- **D-16:** Phase 1 may run read-only parsing commands, file existence checks, JSON summarizers, `git status`, and the import smoke check.
- **D-17:** Phase 1 must not run `run_study.py --execute`, artifact builders, package builders, checkpoint training, final replay, calibration, or any command that regenerates evidence.
- **D-18:** Runtime smoke verification should remain limited to:
  `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"` from repository root, or the equivalent import check from `work2_coding/`.

### Handoff To Later Phases
- **D-19:** Phase 2 should focus on provenance/readiness cleanup planning without destructive changes.
- **D-20:** Phase 3 should decide whether frozen final settings and calibration/final-test separation justify a legitimate final replay, or whether the manuscript must be locked as conditional diagnostic.

### Agent Discretion
- The agent may choose exact table formatting, JSON extraction helpers, and wording order for the three Phase 1 milestone documents, as long as the decisions above are preserved.
- The agent may add concise evidence facts discovered by read-only inspection, but may not expand Phase 1 into repair, rerun, or manuscript writing work.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Roadmap
- `.planning/PROJECT.md` - project scope, claim ceiling, runtime root, and research guardrails.
- `.planning/REQUIREMENTS.md` - Phase 1 requirements `EVID-01` through `EVID-04` and out-of-scope boundaries.
- `.planning/ROADMAP.md` - Phase 1 goal, success criteria, deliverables, and verification baseline.
- `.planning/STATE.md` - current workflow state and current focus.
- `.planning/research/SUMMARY.md` - regenerated research summary and current evidence facts.

### Codebase Maps
- `.planning/codebase/ARCHITECTURE.md` - active runtime architecture and artifact/claim gate flow.
- `.planning/codebase/CONCERNS.md` - current blockers, reproducibility risks, stale path risks, and claim-boundary risks.
- `.planning/codebase/CONVENTIONS.md` - artifact, manifest, row, checkpoint, and research-integrity conventions.
- `.planning/codebase/INTEGRATIONS.md` - local integration and artifact interface contracts.
- `.planning/codebase/STACK.md` - runtime stack, commands, and dependency boundary.
- `.planning/codebase/STRUCTURE.md` - active directory layout and generated artifact boundaries.
- `.planning/codebase/TESTING.md` - script-style test patterns and verification commands.

### Generated Artifact Package
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` - canonical strict claim guard; current `claim_ready=false`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` - canonical package status; current 74 artifacts, 70 existing, 4 missing, 108 blockers.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json` - canonical package artifact index.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json` - canonical artifact-to-manuscript-section map.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json` - mirror file for drift check only.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json` - mirror file for drift check only.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json` - mirror file for drift check only if present.
- `artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json` - mirror file for drift check only if present.

### Manuscript And Paper Boundary
- `manuscript/main.tex` - restored manuscript source; Phase 1 may inspect wording only, not edit.
- `manuscript/references.bib` - manuscript bibliography source.
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md` - claim-safe manuscript language guidance.
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md` - table/figure evidence mapping.
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md` - target manuscript structure.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - TR-E research design framing.

### Runtime Contracts
- `work2_coding/Src/artifact_status.py` - artifact readiness classification boundary.
- `work2_coding/Src/manuscript_claims.py` - strict claim guard and manuscript claim boundary.
- `work2_coding/Src/paper_artifacts.py` - Phase 10 paper package indexing.
- `work2_coding/Src/formal_readiness.py` - formal readiness and checkpoint provenance gates.
- `work2_coding/Src/study_execution.py` - row generation and checkpoint metadata behavior.
- `work2_coding/Src/paired_replay.py` - normalized row schema and paired replay fairness.
- `work2_coding/Src/policy_adapters.py` - policy-tag catalog and mainline comparison family.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`: source-family counts, package-tier counts, blocked claim IDs, and `claim_ready_reason` can drive the Phase 1 summary.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`: per-claim `support_status`, `claim_ready`, `manuscript_allowed`, safe language, forbidden language, source artifacts, and blocker reasons can drive the claim matrix.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`: artifact entries can drive the 74-artifact traceability matrix.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`: section mappings can identify which manuscript sections are affected by blocked or diagnostic artifacts.

### Established Patterns
- Active runtime root is `work2_coding/`; `ooh_code/` is absent and stale references must be verified before use.
- Generated rows, artifact packages, package status, and claim guards are evidence outputs and must not be hand-edited.
- Formal and pilot claim readiness fail closed when checkpoint provenance, dependency snapshot, loaded checkpoint status, or clean git provenance is missing.
- No-filter outputs remain diagnostic unless formal evidence and artifact gates justify stronger use.
- Attention-based choice/scoring remains outside v1 scope.
- Opt-out accounting must remain separate from accepted home pickup.

### Integration Points
- Phase 1 report generation should read from current planning docs, current git status, `manuscript/main.tex`, the Phase 10 canonical package, and root mirror JSON files.
- Phase 1 verification should include the runtime import smoke only, not study execution or artifact regeneration.
- Phase 2 should use Phase 1 outputs as the boundary for provenance/readiness cleanup planning.
- Phase 3 should use Phase 1 and Phase 2 outputs to decide final replay legitimacy versus diagnostic manuscript lock.

</code_context>

<specifics>
## Specific Ideas

- User prefers Chinese interaction and compact option answers such as `1A,2B`.
- Phase 1 should use a conservative scientific tone: current evidence leans diagnostic, but the final replay path remains a gated Phase 2/3 question.
- The audit should be useful for downstream planning rather than exhaustive reproduction of large JSON files.
- `manuscript/main.tex` is available again and should be considered present for Phase 1.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 1 scope.

</deferred>

---

*Phase: 1-Repository And Evidence Boundary Audit*
*Context gathered: 2026-06-16*
