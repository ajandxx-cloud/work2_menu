# Phase 3: Formal RC Evidence Pipeline Repair And Completion - Context

**Gathered:** 2026-06-15T11:03:25+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 3 repairs and completes the formal RC evidence pipeline for the V1
seven-tag mainline family. It should inspect the formal manifest, verify or
reuse the required shared checkpoint, run formal readiness without bypassing
blockers, execute or validate formal paired replay rows, and build only the
artifacts allowed by readiness and claim-guard gates.

This phase may produce formal rows, diagnostic artifacts, blocker diagnoses,
and evidence-gate metadata. It must not hand-edit generated rows, tune on
formal results to force a ranking, upgrade manuscript claims from diagnostic
evidence, revive `ooh_code/`, or treat no-filter diagnostics as operational
recommendations.

</domain>

<decisions>
## Implementation Decisions

### Existing Formal Run Positioning
- **D-01:** The latest completed formal run may be used as a candidate formal
  evidence input, but it becomes claim-ready only if readiness, artifact
  status, and claim guard gates allow it.
- **D-02:** The latest completed run observed during discussion is
  `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a`.
  It has 35 rows, all seven mainline policy tags, five formal split IDs, loaded
  checkpoint status, and `execution_status: completed`, but its metadata still
  records `git_dirty: true`.
- **D-03:** The prior failed run remains useful diagnostic evidence. Keep
  `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T031927Z-fca35a73`
  as a failure case with 7 failed rows, `UnboundLocalError`, and blocker code
  `actual_replay_failed_rows`.

### Dirty Git And Readiness Gate
- **D-04:** If formal readiness is blocked by dirty git, Phase 3 should first
  produce `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` listing relevant
  modified/deleted/untracked paths, blockers, and recommended cleanup, commit,
  or stash actions. It must request user confirmation before any destructive
  cleanup or broad git state change.
- **D-05:** Phase 3 should not automatically clean, revert, or stage unrelated
  dirty worktree changes. The dirty worktree is evidence and a gate condition,
  not permission to mutate user work.

### Artifact And Claim-Ready Boundary
- **D-06:** If readiness or claim guard does not allow claim-ready use, Phase 3
  may generate diagnostic artifacts only. It must not generate or promote
  paper-facing positive result artifacts that imply empirical superiority.
- **D-07:** Formal replay failures should preserve both failed normalized rows
  and a blocker diagnosis. Failed rows must include `status`, `execution_status`,
  `error_type`, and `error_message` metadata so downstream diagnosis can
  distinguish runtime failure from empirical performance.

### Verification And Checkpoint Policy
- **D-08:** Use the standard verification set for this phase: import smoke,
  formal readiness, formal replay enablement, opt-out accounting, paired replay,
  policy fairness, checkpoint provenance, and artifact gates.
- **D-09:** If the required checkpoint already exists and readiness reports
  `checkpoint_load_status: loaded`, reuse it, but re-record checkpoint hash,
  load status, resolved path, and provenance in readiness/run metadata.

### Success Definition
- **D-10:** Phase 3 succeeds when formal replay is completed and the rows are
  comparable across the seven-tag family. Claim-ready status is a later gate
  condition and may remain blocked or diagnostic if readiness, artifact status,
  or claim guard does not approve positive claim use.

### The Agent's Discretion
- The planner may decide whether to validate the latest completed formal run
  first or rerun formal replay after readiness diagnostics, provided the final
  plan respects D-01 through D-10.
- The planner may choose exact output roots for diagnostic artifacts, but should
  keep formal run outputs under `work2_coding/outputs/formal_v1/` unless a
  clearer project-local convention is already present.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, runtime root, active requirements,
  research guardrails, and key decisions through Phase 2.
- `.planning/REQUIREMENTS.md` - Phase 3 requirements `RC-01` through `RC-05`
  and downstream claim/calibration requirements.
- `.planning/ROADMAP.md` - Phase 3 scope, baseline commands, and global gate
  rules, especially dirty-git blocker handling.
- `.planning/STATE.md` - Current GSD state, verification baseline, and Phase 3
  next-step notes.
- `.planning/STATE_LOCK.md` - Phase 1 baseline, active runtime confirmation,
  checkpoint/readiness/artifact status, stale path mapping, and formal claim
  blockers.
- `.planning/research/SUMMARY.md` - TR-E framing, evidence ladder, scientific
  boundary, and fallback contribution path.
- `AGENTS.md` - Repository instructions, runtime assumption, research
  guardrails, and verification baseline.

### Prior Phase Context And Paper Contract
- `.planning/phases/01-repository-audit-and-state-locking/01-CONTEXT.md` -
  Decisions about runtime root, stale `ooh_code/` handling, blocker
  classification, verification boundaries, opt-out accounting, paired replay
  fairness, and checkpoint provenance.
- `.planning/phases/02-paper-level-research-design-lock/02-CONTEXT.md` -
  Decisions about claim ladder, service-bundle semantics, outside option,
  seven-tag family, paired replay requirements, table/figure plan, no-filter
  boundary, and attention boundary.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - Locked paper-level research
  design, mathematical skeleton, claim-to-evidence map, evidence tiers,
  artifact gates, tables, figures, and downstream handoff to Phase 3.

### Runtime Manifests, Scripts, And Gate Logic
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Formal RC
  manifest, seven-tag policy family, split IDs, paired fields, checkpoint
  requirement, and normalized row schema.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` - Pilot robust
  menu manifest and checkpoint provenance expectations.
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml` - Smoke robust
  menu manifest for quick contract checks.
- `work2_coding/scripts/train_shared_checkpoint.py` - Shared checkpoint
  training entry point; use only if checkpoint provenance requires retraining.
- `work2_coding/scripts/check_formal_readiness.py` - Formal readiness wrapper.
- `work2_coding/scripts/run_study.py` - Formal replay execution wrapper.
- `work2_coding/scripts/build_artifacts.py` - Artifact builder wrapper.
- `work2_coding/scripts/build_manuscript_frame.py` - Manuscript-frame builder;
  use only within claim-gate boundaries.
- `work2_coding/Src/formal_readiness.py` - Formal readiness checks and
  claim-ready blockers.
- `work2_coding/Src/study_execution.py` - Study execution status and metadata.
- `work2_coding/Src/paired_replay.py` - Paired replay contract and row fields.
- `work2_coding/Src/policy_adapters.py` - Seven-tag policy adapter contract.
- `work2_coding/Src/artifact_builder.py` - Artifact generation contract.
- `work2_coding/Src/artifact_status.py` - Artifact status classification.
- `work2_coding/Src/manuscript_claims.py` - Claim guard and manuscript-frame
  logic.

### Current Evidence Files Observed During Discussion
- `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`
  - Required formal shared checkpoint; readiness previously reported loaded.
- `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
  - Existing readiness JSON; status observed as blocked due to dirty git while
  checkpoint load status was loaded.
- `work2_coding/outputs/phase4_artifacts/ARTIFACT_STATUS.json` - Existing
  artifact status; diagnostic, not claim-ready.
- `work2_coding/outputs/phase4_artifacts/manuscript/CLAIM_GUARD.json` -
  Existing claim guard; blocks empirical superiority claims.
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/study_summary.json`
  - Latest completed formal run summary observed during discussion.
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json`
  - Latest completed formal rows observed during discussion.
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T031927Z-fca35a73/study_summary.json`
  - Prior failed formal run summary observed during discussion.
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T031927Z-fca35a73/blockers.json`
  - Prior failed formal run blocker record.
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T031927Z-fca35a73/normalized_rows.json`
  - Prior failed formal rows with 7 failures.

### Focused Verification Scripts
- `work2_coding/scripts/test_optout_accounting.py` - Opt-out accounting
  contract.
- `work2_coding/scripts/test_paired_replay_contract.py` - Paired replay
  contract.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Policy fairness
  across variants.
- `work2_coding/scripts/test_checkpoint_provenance.py` - Checkpoint provenance
  and load status contract.
- `work2_coding/scripts/test_artifact_gates.py` - Artifact gate behavior.
- `work2_coding/scripts/test_formal_readiness.py` - Formal readiness contract.
- `work2_coding/scripts/test_formal_replay_enablement.py` - Formal replay
  enablement contract.
- `work2_coding/scripts/test_study_execution_status.py` - Study status and
  blocker row behavior.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/scripts/check_formal_readiness.py`: readiness command wrapper
  for formal gate checks and dirty-git blocker reporting.
- `work2_coding/scripts/run_study.py`: formal replay entry point for
  `formal_robust_menu`.
- `work2_coding/scripts/build_artifacts.py`: artifact builder, but Phase 3
  must keep generated outputs diagnostic unless claim gates allow stronger use.
- `work2_coding/scripts/build_manuscript_frame.py`: manuscript-frame builder;
  do not use it to upgrade claims while artifact status remains diagnostic.
- `work2_coding/scripts/test_*.py`: script-style tests with direct assertions;
  use targeted scripts rather than inventing a new test runner.

### Established Patterns
- Active runtime root is `work2_coding/`; `.planning/codebase/` references to
  `ooh_code/` are historical and must be rechecked against `work2_coding/`.
- Formal studies are manifest-driven YAML contracts under
  `work2_coding/Experiments/studies/`.
- Normalized rows must carry status/provenance metadata and must not be edited
  by hand.
- Claim language is gated by readiness JSON, completed comparable rows,
  artifact status, and claim guard.

### Integration Points
- Phase 3 planning should connect `formal_robust_menu.yaml`,
  `FORMAL_READINESS.json`, latest formal run rows, artifact status, claim guard,
  and focused test scripts into one evidence pipeline.
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` should be created when dirty
  git or replay failures block claim-ready progression.
- The latest completed formal run can be validated and consumed as candidate
  evidence, but downstream manuscript-facing use must remain blocked unless
  the gate artifacts approve it.

</code_context>

<specifics>
## Specific Ideas

- The user chose to discuss all gray areas using compact numbered options.
- The user selected `1A,2A,3A,4A,5C,6B,7A,8A`.
- Phase 3 should treat formal replay completion and row comparability as the
  phase success bar, while leaving claim-ready status to explicit gates.
- Dirty git should be diagnosed first, not automatically cleaned.
- The failed formal run should remain part of the evidence trail rather than
  being hidden.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within Phase 3 scope.

</deferred>

---

*Phase: 3-Formal RC Evidence Pipeline Repair And Completion*
*Context gathered: 2026-06-15T11:03:25+08:00*
