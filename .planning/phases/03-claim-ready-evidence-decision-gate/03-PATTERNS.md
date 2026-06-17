# Phase 3 Pattern Map

**Phase:** 03 - Claim-Ready Evidence Decision Gate
**Created:** 2026-06-17
**Status:** Complete

## Purpose

This pattern map identifies the closest existing artifacts and source modules
for Phase 3 planning. Phase 3 writes a decision document only; it does not
repair gates, generate evidence, or edit generated artifacts.

## Deliverable Patterns

| New deliverable | Closest analog | Pattern to reuse |
| --- | --- | --- |
| `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md` | `.planning/milestones/tr_e_completion/M1_DECISION.md` | Separate current decision, evidence basis, claim ceiling, handoff, and forbidden next steps. |
| Gate list in M3 decision | `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` | Use exact field and blocker names for checkpoint, readiness, dependency, manifest, git, and source-row provenance. |
| Approval/action boundary | `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` | Mark gate cleanup, readiness, replay, builders, mirror replacement, and claim upgrades as later approval/execution actions. |
| Verification notes | `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-VALIDATION.md` | Use source assertions, import smoke output, manifest contract test, and explicit no-generated-evidence checks. |

## Source Module Patterns

| Source file | What Phase 3 should extract | Execution boundary |
| --- | --- | --- |
| `work2_coding/Experiments/studies/calibration_robust_menu.yaml` | Calibration-only status, pilot split set, grid, checkpoint path, policy tags, paired/varied fields, protocol reference | Read only. Do not run calibration or create protocol docs. |
| `work2_coding/Experiments/studies/final_robust_menu.yaml` | Final candidate status, frozen-settings requirement, selected runtime knob intent, final split set, checkpoint path, policy tags | Read only. Do not run final replay or treat manifest intent as authorization. |
| `work2_coding/scripts/test_calibration_manifests.py` | Non-generating validation of policy family, split separation, paired/varied fields, provenance/accounting schema | May run as Phase 3 verification. |
| `work2_coding/scripts/test_frozen_final_settings.py` | Future contract for a freeze record if a later phase is approved to create it | Read only. Do not use as a passing Phase 3 gate while the file is intentionally missing. |
| `work2_coding/scripts/test_calibration_protocol.py` | Future contract for a calibration protocol if a later phase is approved to create it | Read only. Do not use as a passing Phase 3 gate while the file is intentionally missing. |
| `work2_coding/Src/formal_readiness.py` | Dirty-git, checkpoint, dependency snapshot, and checkpoint load blockers | Read only. Do not run `check_formal_readiness.py` in Phase 3. |
| `work2_coding/Src/artifact_status.py` | Artifact claim-ready prerequisites and diagnostic/blocked classification rules | Read only. Do not classify regenerated artifacts in Phase 3. |
| `work2_coding/Src/study_execution.py` | Checkpoint path resolution, row-level checkpoint metadata, git provenance, blocked prerequisite behavior | Read only. Do not execute replay. |
| `work2_coding/Src/manuscript_claims.py` | Strict claim guard boundary and claim-specific allowed-use behavior | Read only. Do not edit generated `CLAIM_GUARD.json`. |

## Current Source Pattern Findings

- Phase 3 has one natural deliverable: `M3_CLAIM_READY_DECISION.md`.
- The current final replay path is a candidate after gates, not an authorized
  run. The manifest says `final_claim_candidate_after_gates` and references
  missing freeze/protocol documents.
- Phase 3 should use the exact status label
  `blocked_pending_gate_cleanup` for current replay authorization.
- The decision should preserve the Phase 4 branch: approved gate cleanup and
  readiness first, then final replay only if all pre-replay gates pass.
- If gates fail, Phase 4 should lock the diagnostic path without probing
  final results.
- If final replay technically completes but the strict claim guard remains
  false, the result is evidence, not permission to tune.

## Planning Implications

- One plan is enough because Phase 3 is a decision-document phase.
- The plan should cite all Phase 3 context decisions `D-01` through `D-18` in
  `must_haves.truths`.
- The plan should include a threat model for accidental replay authorization,
  protocol reconstruction, final-result tuning, generated artifact edits,
  and claim overstatement.
- The executor should run only non-generating checks and source assertions.

## PATTERN MAPPING COMPLETE
