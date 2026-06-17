# Roadmap: Work2 TR-E Claim-Ready Manuscript Completion

## Execution Policy

This regenerated roadmap follows the user's option to create new planning from
the current workspace rather than restore deleted legacy GSD planning files.
It treats current generated artifacts as evidence, not as editable source.

Execute runtime commands from `work2_coding/` unless a phase explicitly works
on planning, manuscript, or root-level artifact files. Do not run calibration,
final replay, case-study execution, or manuscript claim upgrades until the
phase gates authorize them.

## Phase 1: Repository And Evidence Boundary Audit

**Status:** Complete (2026-06-16)

**Goal:** Reconstruct the exact current state before any new work.

**Success Criteria:**
1. Current planning, codebase maps, artifacts, manuscript files, git status,
   and runtime root are inspected.
2. Current `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`,
   and `ARTIFACT_TO_SECTION_MAP.json` status are recorded.
3. Causes of current `claim_ready=false` are separated into
   provenance/readiness, empirical-performance, artifact-packaging,
   manuscript-language, case-study, and computational-tractability blockers.
4. No experiments are run and no generated evidence is modified.
5. The phase states whether a claim-ready path is feasible or whether only
   diagnostic manuscript writing is feasible.

**Deliverables:**
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`
- `.planning/milestones/tr_e_completion/M1_DECISION.md`

**Requirements:** EVID-01, EVID-02, EVID-03, EVID-04

**Verification:**

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

## Phase 2: Gate Cleanup Plan Without Destructive Changes

**Status:** Complete (2026-06-16)

**Goal:** Resolve or document provenance, readiness, and artifact blockers
needed before any final rerun or claim upgrade.

**Success Criteria:**
1. Dirty git state is inspected without reverting or deleting unrelated user
   changes.
2. Checkpoint path, hash, sidecar metadata, and load status requirements are
   documented.
3. Formal readiness scripts and artifact builders are inspected.
4. Every cleanup recommendation maps to a readiness or claim-guard blocker.
5. Destructive or ambiguous cleanup is stopped and routed to user approval.

**Deliverables:**
- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` if needed

**Requirements:** GATE-01, GATE-02

## Phase 3: Claim-Ready Evidence Decision Gate

**Status:** Complete (2026-06-17)

**Goal:** Decide whether to pursue a final claim-ready rerun or lock the paper
as conditional diagnostic.

**Success Criteria:**
1. Calibration and frozen final settings are read if present in the current
   workspace.
2. The phase determines whether a final replay is scientifically legitimate or
   would amount to tuning on test results.
3. The project classifies support for central adaptive-menu superiority,
   conditional regime-specific claims, or diagnostic-only contribution.
4. A formal go/no-go decision is written.

**Deliverable:**
- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`

**Requirements:** GATE-03, GATE-04

## Phase 4: Execute Selected Claim Path

**Status:** Complete (2026-06-17)

**Goal:** Execute only the evidence-authorized path.

**Path A - Final RC Replay And Artifact Regeneration:**
Run only if Phase 3 finds that gates can be cleaned and frozen settings are
valid without result-chasing.

Expected deliverables:
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md`
- `.planning/milestones/tr_e_completion/M4A_CLAIM_CLASSIFICATION.md`
- A regenerated final artifact package under an explicitly named final
  artifact directory

Outcome: pre-replay gates remained blocked, so final replay and final artifact
generation were not authorized. `M4A_FINAL_REPLAY_REPORT.md` records
`not_run`; no `M4A_CLAIM_CLASSIFICATION.md` was created because no regenerated
final package exists.

**Path B - Diagnostic Manuscript Lock:**
Run if Phase 3 rejects final replay or regenerated evidence still yields
`claim_ready=false`.

Expected deliverables:
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md`
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md`

**Success Criteria:**
1. No final rerun occurs unless it is pre-registered and legitimate.
2. No generated result row, table, figure, or claim guard is manually edited.
3. Strict claim guard determines the final claim ceiling.
4. If `claim_ready=false`, the diagnostic manuscript path is selected.

**Requirements:** PATH-01, PATH-02, PATH-03, PATH-04

## Phase 5: TR-E Manuscript Draft Construction

**Status:** Planned (2026-06-17)

**Goal:** Build a full manuscript draft aligned with the selected claim path.

**Success Criteria:**
1. The manuscript includes Introduction, Literature Review, Problem
   Description, Mathematical Model, Solution Method, Experimental Design,
   Results, Discussion, Conclusion, and Appendix.
2. The body uses academic English paragraph prose.
3. Notation is consistent with the regenerated paper design.
4. Every table and figure has source artifact path, claim ID, claim status,
   and allowed use.
5. Prohibited positive language is absent unless strict claim guard authorizes
   the exact claim.

**Deliverables:**
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` or
  `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.tex`
- `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md`
- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md`
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`
- `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`

**Requirements:** MS-01, MS-02, MS-03, MS-04, MS-05

## Phase 6: Final TR-E Submission Readiness Audit

**Status:** Not started

**Goal:** Determine whether the manuscript is ready for TR-E submission or
requires another milestone.

**Success Criteria:**
1. Novelty, model rigor, empirical credibility, claim safety, source
   traceability, reproducibility, academic writing quality, and reviewer risks
   are audited.
2. A final recommendation is produced:
   submit-ready, revise-before-submission, diagnostic-only but draftable, or
   not ready.
3. The final answer states whether Work2 is claim-ready empirical or
   conditional diagnostic.

**Deliverables:**
- `.planning/milestones/tr_e_completion/M6_FINAL_TR_E_READINESS_AUDIT.md`
- `manuscript/TR_E_WORK2_FINAL_REVISION_TASKS.md`

**Verification:**

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_artifact_gates.py
python scripts/test_paired_replay_contract.py
python scripts/test_policy_fairness_contract.py
python scripts/test_manuscript_claim_guard.py
```

**Requirements:** SUB-01, SUB-02, SUB-03

---
*Roadmap regenerated: 2026-06-16*
