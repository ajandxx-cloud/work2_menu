# M1 Decision

**Phase:** 01 - Repository And Evidence Boundary Audit
**Created:** 2026-06-16
**Requirements addressed:** EVID-01, EVID-02, EVID-03, EVID-04

## Current Decision

The current generated Work2 Phase 10 package is not claim-ready. From current
files alone, the defensible manuscript direction leans diagnostic: formulation,
paired replay design, artifact-gated reporting, and transparent claim-boundary
control.

Phase 1 does not decide final replay legitimacy. Phase 1 records the current
evidence boundary and routes the scientific go/no-go decision to Phase 2 and
Phase 3.

## Evidence Basis

The decision is based on read-only inspection of current planning files,
codebase maps, manuscript source, git status, and the canonical generated
Phase 10 package under:

```text
work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/
```

Key package facts:

- `PACKAGE_STATUS.json` schema: `phase10-paper-artifact-package-v1`.
- `CLAIM_GUARD.json` schema: `phase10-strict-claim-guard-v1`.
- `claim_ready=false`.
- `strict_claim_guard_claim_ready=false`.
- `artifact_count=74`.
- `existing_artifact_count=70`.
- `missing_artifact_count=4`.
- `blocker_count=108`.
- Four key root mirror JSON files match the canonical package by SHA-256.
- The only strict claim marked ready is
  `C7_provenance_status_transparency`.

## Claim Ceiling

The current claim ceiling is provenance/status transparency only. The current
package does not authorize positive empirical claims about:

- central adaptive-menu superiority;
- product ablation value;
- adaptive-window increment;
- menu construction value;
- exact/greedy computational credibility;
- semi-real case validation.

`C5_eta_robustness_boundary` is manuscript-allowed only as diagnostic boundary
language. It does not authorize no-filter operational recommendations.

## Feasibility Assessment

Current evidence is not sufficient for a claim-ready empirical optimization
paper. The current package can support a diagnostic manuscript path if later
phases choose to lock the paper that way.

A future claim-ready path is not ruled out by Phase 1, but it is gated. It
requires Phase 2 and Phase 3 to show that provenance/readiness cleanup and
frozen final settings can support a legitimate final replay without tuning on
final outputs.

The deleted legacy planning/results files are a provenance risk, not an
automatic Phase 1 blocker. The current evidence boundary is the present
workspace and current generated packages.

## Phase 2 Handoff

Phase 2 should plan provenance/readiness cleanup without destructive changes.
It should inspect dirty git state, checkpoint provenance requirements, artifact
readiness scripts, and package blocker causes. It should not restore, delete,
stash, revert, or overwrite unrelated user changes without explicit approval.

Phase 2 should produce a cleanup plan that maps every proposed action to a
readiness or claim-guard blocker.

## Phase 3 Handoff

Phase 3 should decide whether frozen final settings and calibration/final-test
separation justify a legitimate final replay or whether the manuscript must be
locked as conditional diagnostic.

The required Phase 3 question is:

```text
Can Work2 run a pre-registered final replay without tuning on final outputs,
and can regenerated strict guards then authorize stronger claims?
```

If the answer is no, the paper should proceed as a diagnostic service-menu
optimization manuscript. If the answer is yes, the replay path must still be
run through generated rows, readiness gates, artifact status, and strict claim
guard output before any manuscript claim upgrade.

## Forbidden Next Steps

Phase 1 does not authorize:

- final replay;
- calibration;
- tuning settings to force a desired ranking;
- checkpoint training;
- case-study execution;
- `run_study.py --execute`;
- artifact builders;
- package builders;
- manual edits to generated rows, figures, tables, package status, or claim
  guards;
- manuscript claim upgrades;
- claims that adaptive menu dominates, adaptive windows improve, greedy is
  near-optimal, or case-study validation exists.

The next work should be Phase 2 provenance/readiness cleanup planning, followed
by Phase 3 final replay legitimacy versus diagnostic lock.
