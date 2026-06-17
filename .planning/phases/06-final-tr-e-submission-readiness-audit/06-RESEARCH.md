# Phase 6 Research - Final TR-E Submission Readiness Audit

**Phase:** 06 - Final TR-E Submission Readiness Audit
**Created:** 2026-06-17
**Mode:** inline phase research

## RESEARCH COMPLETE

## Source Basis

This research synthesis is grounded in the current planning state, the Phase 5
manuscript package, Phase 4 diagnostic lock outputs, codebase maps, paper
control documents, and current generated Phase 10 paper-package status.

No internet research, final replay, artifact regeneration, generated-row
editing, claim-guard editing, or manuscript claim upgrade was performed.

## Current Evidence Boundary

Phase 6 starts from a locked diagnostic evidence ceiling:

- Phase 4 did not authorize final replay.
- The current strict claim guard reports `claim_ready=false`.
- Positive empirical claims remain blocked for C1, C2, C3, C4, C6, and C8.
- C5 is usable only as diagnostic ETA/no-filter boundary material.
- C7 is usable as provenance/status transparency only.
- Case-study material remains scaffold-only.
- Phase 8 sensitivity and Phase 9 exact/greedy material remain diagnostic or
  provisional, not claim-ready support.

This means the readiness audit must judge submission readiness for a
conditional diagnostic service-menu manuscript, not for a claim-ready empirical
optimization paper.

## Phase 5 Package Inputs

Phase 5 produced the core manuscript package under `manuscript/`:

- `TR_E_WORK2_MANUSCRIPT_DRAFT.md`
- `TR_E_WORK2_CLAIM_AUDIT.md`
- `TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`
- `TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`
- `TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md`

The draft contains the required TR-E manuscript sections and opens Results
with claim-gate status. The companion files establish claim IDs, source paths,
allowed manuscript use, and prohibited language. Phase 6 should verify these
contracts rather than rewrite them.

## Readiness Dimensions

The audit should use the two-axis structure selected in Phase 6 context.

TR-E contribution risk:

- Novelty: whether the paper offers a credible service-menu optimization
  contribution despite the diagnostic evidence ceiling.
- Transportation relevance: whether many-to-one DRT, meeting points, pickup
  windows, pricing, and passenger choice are central rather than incidental.
- Model rigor: whether the formulation, choice model, feasibility constraints,
  and objective are clear enough for TR-E review.
- Manuscript structure: whether required sections exist and read as a paper,
  not a status memo.
- Academic writing quality: whether prose is polished enough for submission
  after bounded revision.

Evidence compliance risk:

- Claim safety: whether wording stays within strict `CLAIM_GUARD.json`.
- Source traceability: whether tables, figures, and claims map to concrete
  source artifacts.
- Reproducibility: whether package status, checkpoint/load status, generated
  row status, and verification commands are visible.
- Generated-artifact validity: whether the manuscript avoids hand-edited rows,
  package statuses, figures, tables, mirrors, or claim guards.
- Strict claim-guard alignment: whether final conclusions answer claim-ready
  empirical versus conditional diagnostic status.

Every dimension should receive `Blocker`, `Major`, or `Minor`.

## Recommendation Logic

The default recommendation should be `revise-before-submission`. This is
appropriate when the diagnostic manuscript is promising but still needs author
revision before journal submission.

Use `diagnostic-only but draftable` when the audit finds the manuscript is
valid as a conditional diagnostic artifact but too limited or underdeveloped
for immediate TR-E submission.

Use `not ready` only for hard failures:

- Missing key manuscript sections.
- Broken source traceability.
- Claim-safety failure or prohibited positive empirical language.
- Failed hard manuscript package contracts.
- Missing generated package authority files.
- Verification failures that undermine the Phase 6 deliverables.

Use `submit-ready` only if no Blocker or Major issues remain and the current
diagnostic framing is strong enough for TR-E submission as-is. Given current
evidence, this is unlikely and should require explicit justification.

## Contract Test Design

Phase 6 should add `work2_coding/scripts/test_manuscript_readiness_package.py`.
It should fail only on hard contract breaks, not qualitative judgments.

Recommended checks:

- Required manuscript files exist.
- The manuscript draft includes required sections: Abstract, Introduction,
  Literature Review, Problem Description, Mathematical Model, Solution Method,
  Experimental Design, Results, Discussion, Conclusion, and Appendix.
- `CLAIM_GUARD.json` exists and reports schema
  `phase10-strict-claim-guard-v1`.
- The current guard still has `claim_ready=false` and
  `manuscript_positive_claims_allowed=false`, so the test should verify that
  the manuscript does not state positive empirical claims.
- `TR_E_WORK2_CLAIM_AUDIT.md` covers C1 through C8.
- `TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` has source path, claim ID, claim
  status, allowed manuscript use, and evidence class columns.
- Source paths cited in the source map exist when they are concrete local
  paths. Treat semicolon-separated paths and planning scaffold directories
  carefully.
- The draft body does not contain unauthorized positive language such as
  unqualified dominance, superiority, outperformance, near-optimal greedy,
  case-study validation, no-filter recommendation, DSPO_PLUS foregrounding,
  Behavior-Aware framing, TR-C framing, or ranking-validation promises.

The script should print one concise `PASS: ...` line when all checks pass.

## Audit Report Design

`M6_FINAL_TR_E_READINESS_AUDIT.md` should be reviewer-style and firm. It
should include:

- Evidence basis and files inspected.
- Verification command table with PASS/FAIL and short output summaries.
- Two-axis risk matrix.
- Per-dimension `Blocker`/`Major`/`Minor` status.
- Final recommendation.
- Explicit answer to whether the paper is claim-ready empirical or conditional
  diagnostic.
- Reviewer attack points and responses.
- Residual risks and required revision path.

Do not paste long command output. Use short summaries and cite artifacts.

## Revision Task Design

`manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md` should use the requested
hybrid structure:

1. Overall recommendation.
2. Submission blockers.
3. Major revisions.
4. Minor revisions.
5. Section-by-section implementation map.
6. Final pre-submission checklist.

`Submission Blockers` should list only true hard blockers. Strong but
non-blocking improvements belong under `Major Revisions`. Every Blocker and
Major task must bind to evidence or artifact source references and include
checkable completion criteria.

## Planning Implication

Phase 6 should be one execution plan in one wave:

1. Audit the existing manuscript and evidence package.
2. Add the hard-contract manuscript readiness test.
3. Run roadmap verification plus manuscript checks.
4. Write the final readiness audit.
5. Write the final revision task list.
6. Re-run verification and record final status.

The executor must not run final replay, calibration, checkpoint training,
case-study execution, or artifact builders for claim upgrades.
