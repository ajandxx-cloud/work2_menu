# Phase 2: Gate Cleanup Plan Without Destructive Changes - Context

**Gathered:** 2026-06-16T22:11:39+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 delivers a non-destructive cleanup plan for Work2 provenance,
readiness, checkpoint, dirty-git, and artifact-package blockers that must be
understood before Phase 3 can decide final replay legitimacy.

This phase may inspect current repository state, current generated JSON
packages, current source gates, and existing planning outputs. It may write
planning deliverables only:

- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` when
  approval-required actions exist

Phase 2 must not restore, delete, stash, revert, overwrite, regenerate evidence,
train checkpoints, smoke-load checkpoints, run formal readiness, run replay,
run artifact builders, replace mirrors, or hand-edit generated evidence.

</domain>

<decisions>
## Implementation Decisions

### Dirty Git Accounting
- **D-01:** Classify dirty working-tree state by risk category rather than
  listing every changed path. Categories should include regenerated planning,
  paper boundary docs, deleted legacy planning/results, runtime/generated
  evidence if present, and other relevant groups found by inspection.
- **D-02:** Each dirty-git category should include representative paths, risk
  interpretation, and whether user approval is required before any action.
- **D-03:** Any action that changes the worktree or evidence chain must be
  routed to `M2_USER_ACTIONS_REQUIRED.md` rather than executed in Phase 2.
  This includes git restore/stash/revert/delete, legacy file restoration, old
  path deletion, generated artifact rebuilds, mirror replacement, checkpoint
  training, formal/final replay, and readiness or artifact output generation.
- **D-04:** Deleted legacy planning and result files should be described as
  superseded by the regenerated planning. Do not treat them as a primary
  cleanup target, restore them, or mine git history unless a specific
  readiness or claim blocker explicitly depends on one of those legacy files.

### Checkpoint Provenance Contract
- **D-05:** `M2_PROVENANCE_REQUIREMENTS.md` must lock the minimum evidence
  contract for claim-supporting checkpoint provenance: checkpoint path,
  checkpoint SHA-256 hash, sidecar metadata, checkpoint load status,
  dependency snapshot, manifest hash, git SHA, git dirty state, readiness JSON
  path, and readiness JSON hash.
- **D-06:** Checkpoint provenance failures should be represented as separate
  fail-closed blocker codes. Missing checkpoint, missing sidecar, load failure,
  and hash mismatch each block claim-ready use and allow only diagnostic/status
  interpretation until resolved by an approved later phase.
- **D-07:** The recomputed checkpoint file SHA-256 is authoritative. Sidecar
  metadata is supporting evidence that must exist and match or explain the
  file hash; sidecar data cannot substitute for hashing the checkpoint file.
- **D-08:** Phase 2 must not smoke-load checkpoints and must not write new
  readiness outputs. It may document later command templates and expected
  fields only, clearly marked as approval-required and not executed in Phase 2.

### Blocker Cleanup Mapping
- **D-09:** Phase 2 should understand the Phase 10 blocker structure broadly,
  but the cleanup plan body should prioritize blockers that affect Phase 3
  go/no-go: provenance/readiness, checkpoint provenance, dirty git, formal
  readiness, and artifact packaging.
- **D-10:** The four current missing package entries should be investigated
  only to identify their source directories and expected patterns. Do not
  create placeholder files, fill scaffold files by hand, regenerate figures,
  or run package/artifact builders in Phase 2.
- **D-11:** The blocker-action matrix should use a `Blocker -> Action ->
  Approval -> Verification` shape. Each actionable row should name the blocker
  or source, recommended action, approval requirement, what Phase 2 will not
  do, and a verification command or check.
- **D-12:** Empirical performance, tractability, case validation,
  adaptive-window increment, and central superiority blockers should be marked
  as `Not Phase 2` and routed to Phase 3/Phase 4+ rather than repaired in this
  cleanup-plan phase.

### Non-Destructive Boundary
- **D-13:** Phase 2 may execute only read-only inspection commands and write
  planning documents. Allowed examples include `git status`, directory reads,
  JSON/source reads, hash comparison, and source grep.
- **D-14:** Phase 2 must explicitly list commands that require approval before
  execution: `run_study.py --execute`, `train_shared_checkpoint.py`,
  `check_formal_readiness.py`, `build_artifacts.py`,
  `build_phase10_paper_artifacts.py`, final/formal replay, case-study
  execution, git restore/stash/revert/delete, and mirror replacement.
- **D-15:** Command templates may appear in Phase 2 documents only inside
  approval-required or not-executed-in-Phase-2 sections.
- **D-16:** Phase 2 verification should check document existence and
  consistency: M2 deliverables exist, every proposed action maps to a blocker,
  approval-required actions were not executed, and the allowed import smoke
  passes. Do not run readiness/artifact generation tests as Phase 2
  verification.

### The Agent's Discretion
- The planner may choose exact table formatting and grouping names for dirty
  git categories and blocker-action rows, as long as the locked decisions above
  are preserved.
- The planner may add concise code-level observations from current gate
  modules, but must not expand Phase 2 into repair, replay, artifact
  regeneration, or manuscript claim upgrade work.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Phase Scope
- `.planning/PROJECT.md` - project scope, claim ceiling, runtime root, and
  research guardrails.
- `.planning/REQUIREMENTS.md` - Phase 2 requirements `GATE-01` and `GATE-02`.
- `.planning/ROADMAP.md` - Phase 2 goal, success criteria, and deliverables.
- `.planning/STATE.md` - current workflow state and Phase 2 focus.
- `.planning/research/SUMMARY.md` - regenerated research summary and current
  evidence facts.

### Prior Phase Handoff
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`
  - Phase 1 locked evidence-boundary decisions and handoff to Phase 2.
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md` -
  current workspace, git, package, manuscript, and evidence boundary snapshot.
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md` - six-class
  blocker taxonomy and 74-artifact/8-claim traceability.
- `.planning/milestones/tr_e_completion/M1_DECISION.md` - current diagnostic
  lean and Phase 2/3 decision handoff.

### Codebase Maps
- `.planning/codebase/ARCHITECTURE.md` - active runtime architecture and
  artifact/claim gate flow.
- `.planning/codebase/CONCERNS.md` - dirty provenance, checkpoint, artifact,
  and claim-boundary risks.
- `.planning/codebase/CONVENTIONS.md` - artifact, manifest, row, checkpoint,
  and research-integrity conventions.
- `.planning/codebase/INTEGRATIONS.md` - local artifact and readiness
  interface contracts.
- `.planning/codebase/STACK.md` - commands, dependency boundary, and active
  runtime root.
- `.planning/codebase/STRUCTURE.md` - current directory layout and generated
  artifact boundaries.
- `.planning/codebase/TESTING.md` - script-style tests and verification
  patterns.

### Runtime Gate Modules
- `work2_coding/Src/formal_readiness.py` - formal readiness preflight,
  dependency snapshot, checkpoint smoke-load, blocker codes, and readiness
  report fields.
- `work2_coding/Src/study_execution.py` - git provenance, prerequisite
  inspection, checkpoint metadata, blocked rows, and normalized row generation.
- `work2_coding/Src/artifact_status.py` - artifact classification, formal
  readiness validation, dependency snapshot/hash checks, and checkpoint row
  status gates.
- `work2_coding/Src/paper_artifacts.py` - Phase 10 package source collection,
  missing-entry behavior, package status, strict claim guard linkage, and
  mirror replacement behavior.

### Current Generated Package
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
  - canonical package status with `claim_ready=false`, blocker counts, source
  family summaries, and package readiness reason.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  - strict claim guard and current claim ceiling.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
  - package artifact index, including missing entries and source paths.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
  - artifact-to-manuscript-section mapping.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/formal_readiness.py`: exposes the fields Phase 2 should
  document for future formal readiness, including dependency snapshot path/hash,
  checkpoint path/hash/sidecar/load status, git provenance, and blockers.
- `work2_coding/Src/study_execution.py`: provides `collect_git_provenance`,
  checkpoint prerequisite inspection, and row-level checkpoint metadata fields.
- `work2_coding/Src/artifact_status.py`: validates formal readiness JSON
  against rows, dependency snapshots, checkpoint hash/status, and dirty git.
- `work2_coding/Src/paper_artifacts.py`: explains why missing package entries
  appear when expected source patterns do not match current files.
- `PACKAGE_INDEX.json`: records the current missing entry source paths:
  `.planning/data/case_studies/missing.yml`,
  `.planning/data/case_studies/missing.json`,
  `work2_coding/artifacts/work2_robust_menu/figures/missing.png`, and
  `work2_coding/artifacts/work2_robust_menu/figures/missing.metadata.json`.

### Established Patterns
- Active runtime commands should use `work2_coding/` and must not revive an
  `ooh_code/` root.
- Generated rows, package status, claim guards, figure/table outputs, and root
  mirrors are evidence outputs. Do not hand-edit them to change conclusions.
- Formal and pilot gates fail closed when checkpoint provenance, dependency
  snapshot, loaded checkpoint status, or clean git provenance is missing.
- No-filter, Phase 8, Phase 9, attention, and case-study scaffold outputs are
  diagnostic/provisional unless strict gates authorize stronger use.

### Integration Points
- Phase 2 planning should connect `M1_BLOCKER_LIST.md` to
  `formal_readiness.py`, `study_execution.py`, `artifact_status.py`, and
  `paper_artifacts.py`.
- `M2_GATE_CLEANUP_PLAN.md` should be the main action matrix.
- `M2_PROVENANCE_REQUIREMENTS.md` should lock checkpoint/readiness field
  requirements and fail-closed behavior.
- `M2_USER_ACTIONS_REQUIRED.md` should collect every action requiring user
  approval before execution.

</code_context>

<specifics>
## Specific Ideas

- User chose compact numbered options and asked for clarification about the
  four missing package entries. The explanation should be preserved: those
  entries are generated `missing.*` placeholder paths from unmatched expected
  source patterns, not proof that specific real files were recently deleted.
- The current missing-entry directories are `.planning/data/case_studies/` and
  `work2_coding/artifacts/work2_robust_menu/figures/`.
- The current `figures/` directory contains `*.png.status.json` files but no
  real `.png` images or `.metadata.json` files.
- The current case-study scaffold directory contains `.yaml`, Markdown, and
  validator files, but no `.yml` or `.json` files.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 2 scope.

</deferred>

---

*Phase: 2-Gate Cleanup Plan Without Destructive Changes*
*Context gathered: 2026-06-16T22:11:39+08:00*
