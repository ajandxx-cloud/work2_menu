# Phase 3: Claim-Ready Evidence Decision Gate - Context

**Gathered:** 2026-06-17T10:08:09.1788059+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 is a decision-gate phase for Work2 TR-E claim readiness. It decides
whether the project may pursue a final claim-ready replay path after strict
pre-replay gates, or whether the manuscript path must be locked as conditional
diagnostic.

This phase may inspect current manifests, current planning evidence, prior
phase deliverables, current artifact/claim-guard status, and current gate
contracts. It may write the formal go/no-go decision:

- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`

Phase 3 must not run calibration, checkpoint training, formal readiness,
final/formal replay, artifact builders, package builders, case-study execution,
mirror replacement, manuscript claim upgrades, or any hand edits to generated
rows, result tables, figures, package status, or claim guards.

</domain>

<decisions>
## Implementation Decisions

### Frozen Settings Gap
- **D-01:** Phase 3 must classify the current final replay path as
  `blocked_pending_gate_cleanup`, not as immediately authorized. Current
  `final_robust_menu.yaml` and `calibration_robust_menu.yaml` exist, but
  `.planning/results/FROZEN_FINAL_SETTINGS.md` and
  `.planning/results/CALIBRATION_PROTOCOL.md` are absent.
- **D-02:** Missing freeze/protocol evidence does not become a permanent
  no-go by itself, but it blocks replay authorization until the required
  freeze/protocol, clean provenance, checkpoint, dependency, and readiness
  gates are satisfied.
- **D-03:** Later gap closure may use only current manifests and current
  filesystem state. Do not restore, mine, or cite git-history versions of old
  freeze/calibration protocol files for Phase 3 authorization.
- **D-04:** The `selected_runtime_knobs.source` statement in
  `final_robust_menu.yaml` that references `CALIBRATION_PROTOCOL.md` is an
  unverified statement of intent while that file is missing. It cannot
  authorize a final replay.
- **D-05:** Phase 3 should write the blocked freeze/protocol finding only in
  `M3_CLAIM_READY_DECISION.md`. Do not create
  `.planning/results/FROZEN_FINAL_SETTINGS.md` or
  `.planning/results/CALIBRATION_PROTOCOL.md` during Phase 3.

### Final Replay Legitimacy Threshold
- **D-06:** Phase 3 should use a conditional go-after-gates decision: Phase 3
  does not authorize immediate replay, but Phase 4 may perform approved gate
  cleanup/readiness work and may run final replay only after all required
  pre-replay gates pass.
- **D-07:** Required pre-replay gates include provenance gates and
  manifest/paired replay gates: clean/freeze/checkpoint/dependency evidence,
  final manifest stability, seven mainline policy tags, fixed splits and
  seeds, and valid paired/varied fields.
- **D-08:** Phase 4 cleanup before final replay may repair only paths,
  metadata, sidecars, hashes, dependency snapshots, readiness metadata, and
  evidence-chain records. It must not alter the policy family, split IDs,
  seeds, metrics, or frozen runtime settings such as `menu_k`,
  `max_candidates`, ETA filter mode, guardrails, or other result-affecting
  knobs.
- **D-09:** After any authorized replay, claim readiness must be decided
  strictly by generated artifact gates and strict `CLAIM_GUARD.json`. Replay
  produces candidate evidence only. Human judgment cannot override the guard.

### Claim Classification Rule
- **D-10:** Use claim-by-claim classification. Each claim ID must be governed
  by its own strict claim guard status. One passing claim cannot upgrade
  unrelated blocked claims or the paper as a whole.
- **D-11:** If `C1_central_adaptive_menu_superiority` remains blocked but
  local mechanism or boundary claims pass, classify the paper as a conditional
  regime-specific manuscript. Do not state central adaptive-menu superiority.
- **D-12:** Current Phase 8, Phase 9, no-filter, and case-scaffold materials
  may be used only as diagnostic boundary or appendix material. They must not
  support positive main claims.
- **D-13:** If overall `claim_ready=false` but a specific claim has
  `manuscript_allowed=true`, Phase 5 may use that local content only with
  explicit claim ID, claim status, source artifact, and allowed-use labeling.
  The overall manuscript remains diagnostic or conditional.

### Failure And Second-Attempt Rule
- **D-14:** If pre-replay gates fail, Phase 4 must directly lock the
  diagnostic path. It must not run final replay on blocked gates or use
  blocked evidence to probe results.
- **D-15:** If all pre-replay gates pass and final replay starts but fails,
  times out, or emits incomplete rows for technical reasons, allow at most one
  technical rerun.
- **D-16:** The single technical rerun must use the same manifest, git SHA,
  checkpoint path/hash, seeds, splits, policy tags, and frozen settings. It may
  repair only runtime failure or environment interruption. It must not change
  result-affecting settings.
- **D-17:** If the second final replay attempt still fails, times out, or is
  incomplete, lock the diagnostic path immediately. Do not reduce scale, delete
  failed rows, or continue rerunning.
- **D-18:** If final replay technically completes but regenerated
  `CLAIM_GUARD.json` remains `claim_ready=false`, do not tune the manifest or
  settings for another attempt. Guard failure is an evidence result, not a
  technical failure. Continue with diagnostic or conditional manuscript path.

### The Agent's Discretion
None. The user selected explicit decisions for all discussed gray areas.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Roadmap
- `.planning/PROJECT.md` - project scope, claim ceiling, runtime root, and
  research guardrails.
- `.planning/REQUIREMENTS.md` - Phase 3 requirements `GATE-03` and
  `GATE-04`, plus downstream path requirements.
- `.planning/ROADMAP.md` - Phase 3 goal, success criteria, deliverable, and
  Phase 4 branching.
- `.planning/STATE.md` - current workflow state and Phase 3 focus.
- `.planning/research/SUMMARY.md` - regenerated research summary and current
  evidence facts.

### Prior Phase Handoff
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`
  - Phase 1 evidence-boundary decisions and handoff to Phase 3.
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-CONTEXT.md`
  - Phase 2 cleanup, provenance, and non-destructive boundary decisions.
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md` -
  current workspace, git, package, manuscript, and evidence boundary snapshot.
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md` - six-class
  blocker taxonomy and strict claim traceability.
- `.planning/milestones/tr_e_completion/M1_DECISION.md` - current diagnostic
  lean and Phase 3 decision handoff.
- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md` - blocker to
  cleanup action matrix and approval boundary.
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` -
  required checkpoint, dependency, manifest, git, readiness, and source-row
  provenance fields.
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` -
  approval-required actions that Phase 3/4 must not execute silently.

### Codebase Maps
- `.planning/codebase/TESTING.md` - script-style test patterns, formal
  readiness checks, artifact gate checks, and current coverage gaps.
- `.planning/codebase/CONVENTIONS.md` - generated evidence, manifest,
  checkpoint, claim guard, paired replay, opt-out, no-filter, and attention
  boundaries.
- `.planning/codebase/STRUCTURE.md` - active `work2_coding/` runtime layout,
  generated artifact locations, and where manifests/gates live.
- `.planning/codebase/CONCERNS.md` - dirty provenance, checkpoint, final-run,
  claim-boundary, and test-coverage risks.

### Runtime Manifests And Tests
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml` -
  calibration-only pilot manifest; references missing
  `.planning/results/CALIBRATION_PROTOCOL.md`.
- `work2_coding/Experiments/studies/final_robust_menu.yaml` - frozen final
  candidate manifest; references missing `FROZEN_FINAL_SETTINGS.md` and
  `CALIBRATION_PROTOCOL.md`.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - formal
  comparison contract and current formal checkpoint boundary.
- `work2_coding/scripts/test_frozen_final_settings.py` - expected blocked,
  frozen, or conditional freeze record contract.
- `work2_coding/scripts/test_calibration_protocol.py` - expected calibration
  protocol headings and prohibited tuning boundary.
- `work2_coding/scripts/test_calibration_manifests.py` - calibration/final
  manifest separation, policy family, checkpoint, and paired-field contract.

### Generated Artifact Package
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  - canonical strict claim guard; current `claim_ready=false`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
  - canonical package status; current package is not claim-ready.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
  - paper artifact index and missing-entry source paths.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
  - artifact-to-manuscript-section map.

### Runtime Gate Modules
- `work2_coding/Src/formal_readiness.py` - formal readiness preflight,
  dependency snapshot, checkpoint smoke-load, blocker codes, and readiness
  report fields.
- `work2_coding/Src/study_execution.py` - generated row execution status,
  checkpoint metadata, prerequisite inspection, and git provenance.
- `work2_coding/Src/artifact_status.py` - artifact readiness classification
  and fail-closed formal evidence rules.
- `work2_coding/Src/paper_artifacts.py` - Phase 10 package status, missing
  pattern behavior, and strict claim guard linkage.
- `work2_coding/Src/manuscript_claims.py` - strict manuscript claim guard and
  claim-specific allowed-use boundary.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Experiments/studies/final_robust_menu.yaml`: contains the
  final candidate policy family, split/seed set, frozen runtime knob intent,
  and required final checkpoint path. It is a candidate input only, not replay
  authorization.
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml`: records the
  calibration-only grid and selection-rule intent. It cannot authorize final
  replay while its protocol reference is missing.
- `work2_coding/scripts/test_calibration_manifests.py`: can validate
  calibration/final split separation, policy tag preservation, paired fields,
  varied fields, and provenance/accounting schema fields.
- `work2_coding/scripts/test_frozen_final_settings.py` and
  `work2_coding/scripts/test_calibration_protocol.py`: define the missing
  freeze/protocol document contracts if a later phase is approved to create
  them.

### Established Patterns
- Active runtime root is `work2_coding/`; do not recreate or depend on a
  parallel `ooh_code/` root.
- Generated rows, artifacts, package status, package indexes, figures, tables,
  and claim guards are evidence outputs and must not be hand-edited.
- Formal/pilot gates fail closed on dirty git, missing checkpoint provenance,
  missing dependency snapshots, unloaded checkpoints, placeholder formal rows,
  mismatched hashes, and missing source-row checkpoint metadata.
- Paired replay fairness, opt-out accounting, no-filter diagnostic status, and
  attention-out-of-v1-scope remain hard research boundaries.

### Integration Points
- Phase 3 planning should produce
  `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`.
- Phase 4 Path A may start only with approved gate cleanup/readiness, then
  final replay if all pre-replay gates pass.
- Phase 4 Path B should start immediately if pre-replay gates fail or if final
  replay/claim guard outcomes force diagnostic lock.
- Phase 5 manuscript writing must consume claim IDs and allowed-use metadata
  from regenerated strict claim guard output, not from narrative preference.

</code_context>

<specifics>
## Specific Ideas

- User selected compact numbered options during discussion.
- Phase 3 should make `blocked_pending_gate_cleanup` explicit without creating
  the missing freeze/protocol files.
- The final replay path is conditional and gate-bound, not currently
  authorized.
- A technically completed replay with `claim_ready=false` is an evidence
  outcome; it must not trigger tuning or additional attempts in v1.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 3 scope.

</deferred>

---

*Phase: 3-Claim-Ready Evidence Decision Gate*
*Context gathered: 2026-06-17T10:08:09.1788059+08:00*
