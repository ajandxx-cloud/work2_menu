# Phase 4: Execute Selected Claim Path - Context

**Gathered:** 2026-06-17T17:25:47.8071034+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 4 executes the evidence-authorized claim path selected by Phase 3. It
starts with a gate-bound Path A attempt: current freeze/protocol evidence,
checkpoint provenance metadata, formal readiness, and pre-replay gates are
checked before any final replay. Final replay is permitted only if every
pre-replay gate passes from current manifests and current filesystem state.

If any pre-replay gate remains blocked after the single authorized gate pass,
if a second same-settings technical replay attempt fails, or if regenerated
strict `CLAIM_GUARD.json` remains `claim_ready=false`, Phase 4 must lock Path B:
the conditional diagnostic manuscript path.

Phase 4 may write planning/gate deliverables and approved generated evidence
only through runtime scripts and builders. It must not hand-edit generated rows,
artifact status, package status, figures, tables, root mirrors, or claim guards.
It must not alter result-affecting final settings, policy definitions, splits,
seeds, metrics, acceptance/accounting definitions, checkpoint policy, or any
runtime knob after seeing evidence.

</domain>

<decisions>
## Implementation Decisions

### Path Routing
- **D-01:** Phase 4 should try Path A first. It performs strict pre-replay gate
  cleanup/readiness and may run final replay only after all gates pass.
  Otherwise it immediately switches to Path B.
- **D-02:** Path A receives exactly one strict gate-cleanup/readiness pass. If
  blockers remain after that pass, Phase 4 must not enter a remediation loop;
  it must lock Path B.
- **D-03:** If final replay starts after all gates pass but fails, times out, or
  emits incomplete rows for technical reasons, Phase 4 may run at most one
  same-settings technical rerun.
- **D-04:** The single technical rerun must preserve the same manifest, git
  SHA, checkpoint hash, seeds, splits, policy tags, and frozen settings. A
  second technical failure immediately triggers Path B.
- **D-05:** If final replay technically completes but regenerated strict
  `CLAIM_GUARD.json` remains `claim_ready=false`, Phase 4 treats that as an
  evidence result and locks Path B. No tuning, scale reduction, manifest
  narrowing, row deletion, or additional replay is allowed.

### Gate Cleanup Authorization
- **D-06:** Phase 4 may create current
  `.planning/results/CALIBRATION_PROTOCOL.md` and
  `.planning/results/FROZEN_FINAL_SETTINGS.md` records, but only from current
  manifests and current filesystem state.
- **D-07:** The freeze/protocol records must be pre-run/non-tuning evidence
  documents. They must not select settings from final outputs or modify any
  result-affecting knobs.
- **D-08:** Phase 4 must use the existing checkpoint only. It must not retrain
  the checkpoint. If the checkpoint file exists, Phase 4 may generate or fill
  sidecar metadata, hashes, dependency snapshot, checkpoint load-status, and
  readiness metadata.
- **D-09:** Phase 4 may execute the formal readiness command once as the core
  Path A gate check. If readiness remains blocked, Phase 4 must switch to Path
  B.
- **D-10:** Chained authorization is approved: if and only if all pre-replay
  gates pass, Phase 4 may run final replay; after successful replay, it may run
  artifact builder and Phase 10 package builder to regenerate claim
  guard/package without another user pause.

### Final Artifact And Mirror Strategy
- **D-11:** Successful final replay/artifacts must be written under an
  explicit final evidence directory, such as a `final_rc` directory marked by
  timestamp and/or manifest hash. Do not overwrite old diagnostic or pilot
  outputs.
- **D-12:** The canonical source of generated paper evidence remains under
  `work2_coding/artifacts/...`. The root-level `artifacts/` mirror may be
  updated only after package pass, only as a paper-facing copy, and with
  SHA/drift checks recorded.
- **D-13:** If the package builder produces new `missing.*` entries or
  blockers, Phase 4 must not create placeholders and must not hand-edit
  package/status/claim-guard outputs. Record the blocker and switch to Path B
  if needed.
- **D-14:** Phase 4 must hand off complete claim traceability to Phase 5. For
  every usable and unusable claim, list claim ID, status, source artifact path,
  allowed manuscript use, and blocker reason.

### Diagnostic Lock Strength
- **D-15:** If gates fail or claim guard remains false, Path B must produce the
  full diagnostic lock package:
  `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`,
  `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md`, and
  `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md`.
- **D-16:** The diagnostic manuscript narrative should be
  claim-gated diagnostic service-menu optimization: present the service-menu
  optimization framework and paired replay/claim-gate pipeline, while clearly
  reporting which claims are supported, blocked, and bounded.
- **D-17:** The reviewer-risk response should prioritize evidence boundary and
  honest-claim attacks: why the paper does not claim superiority, why
  no-filter/case/tractability evidence is diagnostic, and why the claim guard
  is credible.
- **D-18:** Phase 4 must give Phase 5 a prohibited/allowed language handoff.
  Prohibit wording such as `dominates`, `superior`, `improves`, `validates real
  passengers`, and `near-optimal` unless the exact claim is explicitly
  authorized. Prefer wording such as `diagnose`, `audit`, `boundary
  conditions`, and `claim-gated evidence`.

### The Agent's Discretion
None. The user selected explicit decisions for every discussed gray area.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Roadmap
- `.planning/PROJECT.md` - project scope, claim ceiling, runtime root, and
  research guardrails.
- `.planning/REQUIREMENTS.md` - Phase 4 requirements `PATH-01` through
  `PATH-04`, plus manuscript and submission boundaries.
- `.planning/ROADMAP.md` - Phase 4 goal, Path A/Path B deliverables, success
  criteria, and downstream Phase 5/6 context.
- `.planning/STATE.md` - current workflow state and Phase 4 handoff.
- `.planning/research/SUMMARY.md` - regenerated research summary and current
  evidence facts.

### Prior Phase Handoff
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`
  - evidence-boundary decisions and generated artifact authority.
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-CONTEXT.md`
  - non-destructive cleanup and provenance contract decisions.
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-CONTEXT.md` -
  Phase 3 routing, replay legitimacy, claim classification, and failure rules.
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md` -
  current workspace, package, manuscript, and evidence boundary snapshot.
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md` - blocker taxonomy
  and strict claim traceability.
- `.planning/milestones/tr_e_completion/M1_DECISION.md` - diagnostic lean and
  Phase 2/3/4 handoff.
- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md` - blocker to
  action matrix and approval-required boundary.
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` -
  checkpoint, dependency, manifest, git, readiness, and source-row provenance
  fields.
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` -
  approval-required actions and command templates.
- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md` -
  `blocked_pending_gate_cleanup`, required pre-replay gates, approved cleanup,
  forbidden cleanup, and replay failure rules.

### Codebase Maps
- `.planning/codebase/ARCHITECTURE.md` - manifest-driven execution and
  artifact/claim gate flow.
- `.planning/codebase/CONCERNS.md` - dirty provenance, checkpoint, final-run,
  claim-boundary, and mirror-drift risks.
- `.planning/codebase/CONVENTIONS.md` - manifest, normalized-row, checkpoint,
  generated artifact, paired replay, opt-out, no-filter, and attention
  conventions.
- `.planning/codebase/INTEGRATIONS.md` - local file interfaces, checkpoint,
  readiness, artifact, and package interfaces.
- `.planning/codebase/STACK.md` - active runtime root, dependencies, common
  commands, and script entry points.
- `.planning/codebase/STRUCTURE.md` - active `work2_coding/` layout and
  generated artifact boundaries.
- `.planning/codebase/TESTING.md` - script-style tests, formal readiness
  checks, artifact gate checks, and coverage gaps.

### Runtime Manifests And Tests
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml` -
  calibration-only pilot manifest and current calibration surface.
- `work2_coding/Experiments/studies/final_robust_menu.yaml` - final candidate
  manifest; candidate only until gates pass.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - formal
  comparison/checkpoint contract.
- `work2_coding/scripts/test_calibration_manifests.py` - policy family,
  calibration/final split separation, paired/varied fields, checkpoint, and
  accounting schema checks.
- `work2_coding/scripts/test_frozen_final_settings.py` - expected freeze
  record contract.
- `work2_coding/scripts/test_calibration_protocol.py` - expected calibration
  protocol and no-tuning boundary.

### Runtime Gate Modules
- `work2_coding/Src/formal_readiness.py` - formal readiness preflight,
  dependency snapshot, checkpoint smoke-load, blocker codes, and readiness
  report fields.
- `work2_coding/Src/study_execution.py` - generated row execution status,
  checkpoint metadata, prerequisite inspection, and git provenance.
- `work2_coding/Src/artifact_status.py` - artifact readiness classification
  and fail-closed formal evidence rules.
- `work2_coding/Src/paper_artifacts.py` - Phase 10 package indexing, package
  status, missing-entry behavior, and mirror output behavior.
- `work2_coding/Src/manuscript_claims.py` - strict manuscript claim guard and
  claim-specific allowed-use boundary.

### Generated Artifact Package
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  - canonical strict claim guard; current `claim_ready=false`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
  - canonical package status and blocker summary.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
  - paper artifact index and missing-entry source paths.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
  - artifact-to-manuscript-section map.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Experiments/studies/final_robust_menu.yaml`: candidate final
  replay contract after gates, preserving the seven mainline policy tags and
  final settings intent.
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml`: current
  calibration-only manifest that can inform the pre-run calibration protocol
  record without mining old git history.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`: formal
  checkpoint and comparison contract used by readiness and gate checks.
- `work2_coding/scripts/test_calibration_manifests.py`,
  `work2_coding/scripts/test_frozen_final_settings.py`, and
  `work2_coding/scripts/test_calibration_protocol.py`: existing script-style
  tests for the manifest/freeze/protocol boundary.
- `work2_coding/scripts/check_formal_readiness.py`,
  `work2_coding/scripts/run_study.py`,
  `work2_coding/scripts/build_artifacts.py`, and
  `work2_coding/scripts/build_phase10_paper_artifacts.py`: approved script
  surfaces for readiness, replay, artifact generation, and package generation.

### Established Patterns
- Active runtime root is `work2_coding/`; do not create or target a parallel
  `ooh_code/` root.
- Study manifests are executable contracts. Policy families, paired fields,
  varied fields, splits, seeds, and checkpoint requirements must be validated
  before execution.
- Generated rows, tables, figures, status files, package indexes, root
  mirrors, and claim guards are generated evidence. Do not hand-edit them.
- Formal and pilot gates fail closed on dirty git, missing/unloaded
  checkpoints, sidecar/hash gaps, dependency snapshot gaps, invalid accounting,
  placeholder rows, blocked/failed rows, and no-filter-only diagnostics.
- Paired replay fairness, opt-out/home/meeting-point accounting separation,
  no-filter diagnostic status, and attention-out-of-v1-scope remain hard
  research boundaries.

### Integration Points
- Path A gate cleanup may create the missing current freeze/protocol records in
  `.planning/results/`, then run one formal readiness pass.
- If gates pass, final replay should use current validated final/formal
  manifests and write to an explicit final evidence directory.
- Artifact/package regeneration must consume generated source rows and
  readiness metadata, then let strict `CLAIM_GUARD.json` determine the final
  claim ceiling.
- Path B must produce M4B diagnostic lock deliverables under
  `.planning/milestones/tr_e_completion/` and hand claim-safe wording guidance
  to Phase 5.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four Phase 4 gray areas for discussion.
- The user chose compact numbered answers and accepted the recommended option
  for every Phase 4 decision.
- Phase 4 should be decisive: one strict gate pass, no open-ended repair loop,
  one same-settings technical rerun only if replay starts and fails for
  technical reasons, and strict Path B if `claim_ready=false` remains.
- Phase 4 should write downstream-friendly handoff material rather than making
  Phase 5 rediscover claim boundaries from raw package JSON.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 4 scope.

</deferred>

---

*Phase: 4-Execute Selected Claim Path*
*Context gathered: 2026-06-17T17:25:47.8071034+08:00*
