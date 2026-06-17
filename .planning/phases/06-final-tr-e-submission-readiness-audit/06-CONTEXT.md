# Phase 6: Final TR-E Submission Readiness Audit - Context

**Gathered:** 2026-06-17T21:33:08.4394119+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 6 audits the Phase 5 TR-E manuscript package and determines submission
readiness. It must produce:

- `.planning/milestones/tr_e_completion/M6_FINAL_TR_E_READINESS_AUDIT.md`
- `manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md`

This phase is an audit and readiness phase. It must not reopen final replay,
calibration, checkpoint training, case-study execution, artifact regeneration
for claim upgrades, or any hand edits to generated rows, package status,
figures, tables, mirrors, or claim guards. The Phase 4 diagnostic lock and
current strict `CLAIM_GUARD.json` remain the claim ceiling. Current evidence
supports a conditional diagnostic manuscript path, not a claim-ready empirical
optimization paper.

</domain>

<decisions>
## Implementation Decisions

### Final Recommendation Stance
- **D-01:** Phase 6 should default to a final recommendation of
  `revise-before-submission` unless the audit finds the manuscript package is
  unusually strong against all readiness dimensions.
- **D-02:** The audit should preserve `diagnostic-only but draftable` as a
  secondary conclusion. The paper may be valuable as a conditional diagnostic
  TR-E manuscript even while it is not ready for direct submission.
- **D-03:** Downgrade to `not ready` only for hard failures, such as claim
  safety failure, broken source traceability, missing key manuscript sections,
  failed readiness contracts, or recurrence of prohibited positive empirical
  language.
- **D-04:** Use a two-layer reporting style: reviewer-style hard conclusions
  in `M6_FINAL_TR_E_READINESS_AUDIT.md`, and author-friendly actionable
  language in `TR_E_WORK2_FINAL_REVISION_TASKS.md`.

### TR-E Reviewer Risk Ordering
- **D-05:** Structure the readiness audit as a two-axis matrix:
  TR-E contribution risk and evidence compliance risk.
- **D-06:** TR-E contribution risk should cover novelty, transportation
  relevance, model rigor, manuscript structure, and academic writing quality.
- **D-07:** Evidence compliance risk should cover claim safety, source
  traceability, reproducibility, generated-artifact validity, and strict
  claim-guard alignment.
- **D-08:** Neither axis has automatic veto power. Each axis contributes risk
  levels to the overall audit judgment. The hard-failure downgrade rule in
  D-03 still applies.
- **D-09:** Use `Blocker`, `Major`, and `Minor` as the risk taxonomy.
- **D-10:** Assign a `Blocker`/`Major`/`Minor` status to every audit
  dimension, not only to the final report as a whole.

### Revision Task List Granularity
- **D-11:** `manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md` must use the
  user-provided hybrid template:
  overall recommendation, submission blockers, major revisions, minor
  revisions, section-by-section implementation map, and final
  pre-submission checklist.
- **D-12:** `Submission Blockers` should contain only true hard blockers that
  prevent submission. Strong recommendations that do not block submission
  belong under `Major Revisions`.
- **D-13:** Every `Blocker` and `Major` task must bind to evidence or artifact
  source references. `Minor` tasks may be lighter but should still include
  enough context to be actionable.
- **D-14:** Every task must include checkable completion criteria. Avoid vague
  goals that cannot be verified.
- **D-15:** The final pre-submission checklist must include required command
  checks, not only human review items.

### Verification Threshold
- **D-16:** Phase 6 should run the roadmap verification commands and add
  manuscript-focused checks for manuscript file presence, source-map path
  existence, claim/prohibited phrase scanning, and table/figure source
  traceability.
- **D-17:** Add a lightweight script such as
  `work2_coding/scripts/test_manuscript_readiness_package.py`.
- **D-18:** The new manuscript readiness script should fail only on hard
  contract breaks: missing files, missing key sections, missing source paths,
  unauthorized positive language, or claim-guard mismatch. It must not fail on
  qualitative judgments such as prose style, novelty strength, or model-rigor
  depth.
- **D-19:** `M6_FINAL_TR_E_READINESS_AUDIT.md` must record each verification
  command with PASS/FAIL and a short output summary. Do not paste full long
  command output into the report.
- **D-20:** If the manuscript readiness script fails while the existing
  runtime tests pass, the final recommendation cannot be higher than
  `revise-before-submission`. If the failure is a claim-safety or source
  traceability hard failure, Phase 6 may downgrade to `not ready`.

### the agent's Discretion
The planner and executor may choose the exact internal structure of the new
manuscript readiness test script, the precise audit table layout, and the
wording of individual revision tasks, as long as all decisions above are
honored.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project And Roadmap
- `.planning/PROJECT.md` - project scope, runtime root, Phase 5 handoff, and
  claim ceiling.
- `.planning/REQUIREMENTS.md` - Phase 6 `SUB-01` through `SUB-03`, manuscript
  requirements, and out-of-scope boundaries.
- `.planning/ROADMAP.md` - Phase 6 goal, deliverables, verification commands,
  and success criteria.
- `.planning/STATE.md` - current workflow state and Phase 6 handoff.
- `.planning/research/SUMMARY.md` - current evidence facts, strict claim
  status, and safe framing.

### Prior Phase Handoff
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-CONTEXT.md` -
  final replay legitimacy threshold, claim-by-claim classification, and
  failure rules.
- `.planning/phases/04-execute-selected-claim-path/04-CONTEXT.md` - Path B
  diagnostic lock, prohibited/allowed language boundary, and Phase 5 handoff.
- `.planning/phases/05-tr-e-manuscript-draft-construction/05-CONTEXT.md` -
  manuscript carrier, claim-safe writing decisions, evidence placement, and
  required Phase 5 deliverables.
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md` - final
  replay status; final replay was not run.
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md` -
  formal diagnostic manuscript lock.
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md` - claim ID,
  source artifact, status, allowed-use, blocker, and prohibited-language table.
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md` -
  reviewer-risk framing and section-level guidance.

### Phase 5 Manuscript Package
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` - primary draft to audit.
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md` - Phase 5 claim audit.
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` - table/figure source
  map and allowed-use record.
- `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md` - prohibited language
  scan and findings.
- `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md` - Phase 5 migration,
  risk, and verification notes.

### Paper Design And Claim Controls
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md` - allowed and forbidden language by
  strict claim ID.
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md` - table/figure source path,
  claim ID, claim status, and allowed-use requirements.
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md` - required TR-E section
  structure and claim-safe section responsibilities.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - research question, service
  product definition, primary policy family, and evidence-tier definitions.

### Generated Artifact Package And Claim Authority
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  - canonical strict claim guard; current `claim_ready=false`.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
  - canonical package status and blocker summary.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
  - package artifact index and missing-entry source paths.
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
  - artifact-to-manuscript-section map.

### Codebase Maps And Runtime Surfaces
- `.planning/codebase/TESTING.md` - script-style checks and known coverage
  gaps.
- `.planning/codebase/CONVENTIONS.md` - manuscript, generated evidence,
  claim-guard, opt-out, no-filter, and attention-scope conventions.
- `.planning/codebase/STRUCTURE.md` - active `work2_coding/` layout,
  manuscript directory, `.planning/paper/` docs, and generated artifact
  boundaries.
- `.planning/codebase/CONCERNS.md` - claim boundary risks, manuscript
  language risks, reproducibility risks, and artifact mirror drift.
- `work2_coding/scripts/test_artifact_gates.py` - artifact gate contract test.
- `work2_coding/scripts/test_paired_replay_contract.py` - paired replay row
  and fairness contract test.
- `work2_coding/scripts/test_policy_fairness_contract.py` - policy fairness
  contract test.
- `work2_coding/scripts/test_manuscript_claim_guard.py` - manuscript claim
  guard validation test.
- `work2_coding/scripts/test_manuscript_readiness_package.py` - planned new
  Phase 6 manuscript package readiness test.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`: main manuscript body to audit
  for TR-E contribution, structure, claim safety, and writing quality.
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md`: starting point for claim-by-claim
  readiness review.
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`: starting point for
  source-path and table/figure traceability checks.
- `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`: starting point for
  prohibited-language verification.
- `work2_coding/scripts/test_manuscript_claim_guard.py`: existing script-style
  claim-guard check to include in Phase 6 verification.
- `work2_coding/scripts/test_artifact_gates.py`,
  `work2_coding/scripts/test_paired_replay_contract.py`, and
  `work2_coding/scripts/test_policy_fairness_contract.py`: existing roadmap
  checks for artifact, replay, and policy comparison contracts.

### Established Patterns
- Active runtime root is `work2_coding/`; do not revive stale `ooh_code/`
  paths.
- Script-style tests live in `work2_coding/scripts/` and are invoked directly
  with `python scripts/test_*.py`.
- Tests should print concise PASS output and fail via assertions or nonzero
  exit status.
- Generated evidence, package status, package indexes, figures, tables, root
  mirrors, and claim guards must not be hand-edited.
- The strict claim guard is the claim authority. Current positive empirical
  claims remain blocked.
- No-filter material stays diagnostic. Case-study material stays
  scaffold-only. Attention-based choice/scoring stays out of v1 scope.

### Integration Points
- Add the new manuscript readiness test under
  `work2_coding/scripts/test_manuscript_readiness_package.py`.
- Write the final audit under
  `.planning/milestones/tr_e_completion/M6_FINAL_TR_E_READINESS_AUDIT.md`.
- Write the final revision tasks under
  `manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md`.
- The audit should consume Phase 5 manuscript files and generated claim/package
  JSON files but must not modify generated evidence.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four Phase 6 gray areas for discussion.
- The user supplied the exact desired structure for
  `TR_E_WORK2_FINAL_REVISION_TASKS.md`.
- The final readiness recommendation should be conservative but not fatalistic:
  default `revise-before-submission`, preserve `diagnostic-only but
  draftable`, and reserve `not ready` for hard failures.
- The audit should be clear enough for a future author to see what blocks
  submission, what is a major revision, and what is a minor cleanup item.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 6 scope.

</deferred>

---

*Phase: 6-Final TR-E Submission Readiness Audit*
*Context gathered: 2026-06-17T21:33:08.4394119+08:00*
