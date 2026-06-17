---
phase: 03
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md
autonomous: true
requirements:
  - GATE-03
  - GATE-04
requirements_addressed:
  - GATE-03
  - GATE-04
must_haves:
  truths:
    - "D-01: Phase 3 classifies the current final replay path as blocked_pending_gate_cleanup, not immediately authorized."
    - "D-02: Missing freeze/protocol evidence blocks replay authorization but is not by itself a permanent diagnostic no-go."
    - "D-03: Later gap closure may use only current manifests and current filesystem state, not restored or mined legacy git-history files."
    - "D-04: final_robust_menu.yaml selected_runtime_knobs.source is an unverified statement while CALIBRATION_PROTOCOL.md is missing."
    - "D-05: Phase 3 writes the blocked freeze/protocol finding only in M3_CLAIM_READY_DECISION.md and does not create FROZEN_FINAL_SETTINGS.md or CALIBRATION_PROTOCOL.md."
    - "D-06: Phase 3 uses a conditional go-after-gates decision; immediate final replay is not authorized."
    - "D-07: Required pre-replay gates include provenance plus manifest and paired replay gates."
    - "D-08: Phase 4 cleanup before replay may repair only paths, metadata, sidecars, hashes, dependency snapshots, readiness metadata, and evidence-chain records."
    - "D-09: After authorized replay, generated artifact gates and strict CLAIM_GUARD.json decide claim readiness."
    - "D-10: Use claim-by-claim classification; one passing claim cannot upgrade unrelated claims or the paper as a whole."
    - "D-11: If C1 remains blocked but local claims pass, classify as conditional regime-specific, not central adaptive-menu superiority."
    - "D-12: Current Phase 8, Phase 9, no-filter, and case-scaffold materials may be used only as diagnostic boundary or appendix material."
    - "D-13: If claim_ready=false overall but a specific claim has manuscript_allowed=true, Phase 5 may use it only with claim ID, claim status, source artifact, and allowed-use labeling."
    - "D-14: If pre-replay gates fail, Phase 4 must lock the diagnostic path without running final replay."
    - "D-15: If final replay starts and fails, times out, or emits incomplete rows for technical reasons, allow at most one technical rerun."
    - "D-16: The technical rerun must use the same manifest, git SHA, checkpoint path/hash, seeds, splits, policy tags, and frozen settings."
    - "D-17: If the second final replay attempt still fails, times out, or is incomplete, lock the diagnostic path immediately."
    - "D-18: If final replay completes but regenerated CLAIM_GUARD.json remains claim_ready=false, do not tune the manifest or settings for another attempt."
  artifacts:
    - path: ".planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md"
      provides: "Formal Phase 3 go/no-go decision for final replay versus diagnostic or conditional manuscript path"
  key_links:
    - source: "work2_coding/Experiments/studies/final_robust_menu.yaml"
      target: ".planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md"
      must: "Record final manifest as candidate after gates, not current replay authorization"
    - source: "work2_coding/Experiments/studies/calibration_robust_menu.yaml"
      target: ".planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md"
      must: "Record calibration-only status and missing calibration protocol reference"
    - source: "work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json"
      target: ".planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md"
      must: "Use strict claim guard as claim ceiling and claim-by-claim authority"
    - source: ".planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md"
      target: ".planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md"
      must: "List provenance, checkpoint, dependency, manifest, git, readiness, and source-row gates before replay"
---

# Plan 01 - Claim-Ready Evidence Decision Gate

<objective>
Create the Phase 3 formal decision document that determines whether Work2 may
pursue a final claim-ready replay after strict pre-replay gates, or whether the
paper must proceed as conditional diagnostic. The phase must preserve the
current generated evidence boundary, avoid final-result tuning, and route all
evidence-generating work to later approved phases.
</objective>

<scope>
In scope:
- Inspect current Phase 3 context, prior M1/M2 milestone files, calibration
  and final manifests, strict claim guard, package status, and relevant gate
  source/tests.
- Decide whether the current final replay path is authorized, blocked pending
  cleanup, or diagnostic/no-go.
- Write `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`.
- Define the pre-replay gates Phase 4 must satisfy before any final replay.
- Define claim-by-claim classification and post-replay claim guard authority.
- Define pre-replay gate failure, one technical rerun, second-failure, and
  post-guard-failure rules.
- Run only non-generating verification checks and source assertions.

Out of scope:
- Creating `.planning/results/FROZEN_FINAL_SETTINGS.md`.
- Creating `.planning/results/CALIBRATION_PROTOCOL.md`.
- Restoring or mining deleted legacy planning/results files.
- Running calibration, final replay, formal replay, checkpoint training,
  formal readiness, artifact builders, Phase 10 package builders, mirror
  replacement, case-study execution, or manuscript claim upgrades.
- Editing generated rows, package status, package indexes, figures, tables,
  root mirrors, or claim guards.
- Changing policy family, split IDs, seeds, metrics, manifest runtime knobs,
  checkpoint paths, ETA filter mode, menu size, candidate count, guardrails,
  or any other result-affecting setting.
</scope>

<must_haves>
<truths>
- D-01: Phase 3 must classify the current final replay path as `blocked_pending_gate_cleanup`, not as immediately authorized.
- D-02: Missing freeze/protocol evidence does not become a permanent no-go by itself, but it blocks replay authorization until required gates pass.
- D-03: Later gap closure may use only current manifests and current filesystem state. Do not restore, mine, or cite git-history versions of old freeze/calibration protocol files for Phase 3 authorization.
- D-04: The `selected_runtime_knobs.source` statement in `final_robust_menu.yaml` is an unverified statement of intent while `CALIBRATION_PROTOCOL.md` is missing.
- D-05: Phase 3 writes the blocked freeze/protocol finding only in `M3_CLAIM_READY_DECISION.md`. Do not create `.planning/results/FROZEN_FINAL_SETTINGS.md` or `.planning/results/CALIBRATION_PROTOCOL.md` during Phase 3.
- D-06: Phase 3 uses a conditional go-after-gates decision. It does not authorize immediate final replay.
- D-07: Required pre-replay gates include clean/freeze/checkpoint/dependency evidence, final manifest stability, seven mainline policy tags, fixed splits and seeds, and valid paired/varied fields.
- D-08: Phase 4 cleanup before final replay may repair only paths, metadata, sidecars, hashes, dependency snapshots, readiness metadata, and evidence-chain records. It must not alter policy family, split IDs, seeds, metrics, or frozen runtime settings.
- D-09: After any authorized replay, claim readiness is decided strictly by generated artifact gates and strict `CLAIM_GUARD.json`.
- D-10: Use claim-by-claim classification. One passing claim cannot upgrade unrelated blocked claims or the paper as a whole.
- D-11: If `C1_central_adaptive_menu_superiority` remains blocked but local mechanism or boundary claims pass, classify the paper as conditional regime-specific and do not state central adaptive-menu superiority.
- D-12: Current Phase 8, Phase 9, no-filter, and case-scaffold materials may be used only as diagnostic boundary or appendix material.
- D-13: If overall `claim_ready=false` but a specific claim has `manuscript_allowed=true`, Phase 5 may use that local content only with explicit claim ID, claim status, source artifact, and allowed-use labeling.
- D-14: If pre-replay gates fail, Phase 4 must directly lock the diagnostic path. It must not run final replay on blocked gates.
- D-15: If all pre-replay gates pass and final replay starts but fails, times out, or emits incomplete rows for technical reasons, allow at most one technical rerun.
- D-16: The single technical rerun must use the same manifest, git SHA, checkpoint path/hash, seeds, splits, policy tags, and frozen settings. It may repair only runtime failure or environment interruption.
- D-17: If the second final replay attempt still fails, times out, or is incomplete, lock the diagnostic path immediately. Do not reduce scale, delete failed rows, or continue rerunning.
- D-18: If final replay technically completes but regenerated `CLAIM_GUARD.json` remains `claim_ready=false`, do not tune the manifest or settings for another attempt.
</truths>
</must_haves>

<threat_model>
| Threat | Severity | Mitigation |
| --- | --- | --- |
| Missing freeze/protocol files are accidentally reconstructed during Phase 3 | high | Write only `M3_CLAIM_READY_DECISION.md`; assert missing `.planning/results/FROZEN_FINAL_SETTINGS.md` and `.planning/results/CALIBRATION_PROTOCOL.md` remain absent unless pre-existing user changes already differ |
| Candidate final manifest is treated as immediate replay authorization | high | State `blocked_pending_gate_cleanup`; list all pre-replay gates before any Phase 4 replay |
| Phase 4 cleanup becomes result-affecting tuning | high | Restrict cleanup to paths, metadata, sidecars, hashes, dependency snapshots, readiness metadata, and evidence-chain records |
| Generated evidence or claim guard is hand-edited to improve readiness | high | Verification checks generated-evidence diff paths; plan forbids edits to rows, package status, indexes, figures, tables, mirrors, and claim guards |
| Diagnostic or scaffold material is promoted to positive manuscript claims | high | Use claim-by-claim classification and strict `CLAIM_GUARD.json` as authority |
| Technical replay failure leads to repeated attempts or scale reduction | medium | Allow only one same-settings technical rerun, then diagnostic lock |
</threat_model>

<tasks>
<task id="03-01-01" type="execute">
<title>Establish current freeze/protocol and manifest authorization status</title>
<read_first>
- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-CONTEXT.md`
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-RESEARCH.md`
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-PATTERNS.md`
- `.planning/milestones/tr_e_completion/M1_DECISION.md`
- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml`
- `work2_coding/Experiments/studies/final_robust_menu.yaml`
</read_first>
<action>
Create `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md` with
sections named `Current Decision`, `Evidence Basis`, `Freeze And Protocol
Status`, and `Manifest Authorization Status`. State exactly that the current
status is `blocked_pending_gate_cleanup`. Record that
`calibration_robust_menu.yaml` and `final_robust_menu.yaml` exist, preserve the
intended calibration/final split surface, and reference missing
`.planning/results/CALIBRATION_PROTOCOL.md` and
`.planning/results/FROZEN_FINAL_SETTINGS.md`. State that these missing files
block immediate final replay but do not permanently force diagnostic lock by
themselves. State that `selected_runtime_knobs.source` in the final manifest
is unverified while the referenced protocol is absent.
</action>
<verify>
- `Test-Path .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md` prints `True`.
- `M3_CLAIM_READY_DECISION.md` contains `blocked_pending_gate_cleanup`.
- `M3_CLAIM_READY_DECISION.md` contains `FROZEN_FINAL_SETTINGS.md`.
- `M3_CLAIM_READY_DECISION.md` contains `CALIBRATION_PROTOCOL.md`.
- `M3_CLAIM_READY_DECISION.md` contains `unverified statement`.
</verify>
<acceptance_criteria>
- GATE-03 current authorization status is explicitly decided.
- The decision does not create freeze or protocol files.
- The decision does not restore or cite git-history versions of old freeze/protocol files.
- The decision does not authorize immediate final replay.
</acceptance_criteria>
</task>

<task id="03-01-02" type="execute">
<title>Validate candidate manifest separation without replay</title>
<read_first>
- `work2_coding/scripts/test_calibration_manifests.py`
- `work2_coding/Src/experiment_contracts.py`
- `work2_coding/Src/paired_replay.py`
- `work2_coding/Src/policy_adapters.py`
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml`
- `work2_coding/Experiments/studies/final_robust_menu.yaml`
</read_first>
<action>
Run `cd work2_coding; python scripts/test_calibration_manifests.py`. Add a
`Manifest Contract Status` section to `M3_CLAIM_READY_DECISION.md`. Record the
command, whether it passed, and the specific contracts it checks: seven
mainline policy tags, calibration/final split separation, paired fields,
varied fields, checkpoint required/loaded intent, output schema provenance
fields, and separate opt-out/home/meeting-point accounting. If the command
fails, record failure output and keep the decision blocked; do not repair
manifests in Phase 3.
</action>
<verify>
- `cd work2_coding; python scripts/test_calibration_manifests.py` exits 0 and prints `PASS: 5 calibration manifest tests`, or failure is recorded as a blocker in `M3_CLAIM_READY_DECISION.md`.
- `M3_CLAIM_READY_DECISION.md` contains `seven mainline policy tags`.
- `M3_CLAIM_READY_DECISION.md` contains `paired fields`.
- `M3_CLAIM_READY_DECISION.md` contains `varied fields`.
- `M3_CLAIM_READY_DECISION.md` contains `count_opted_out`.
</verify>
<acceptance_criteria>
- Calibration/final manifest separation is inspected without running calibration or replay.
- The seven-policy family is preserved or the blocker is documented.
- Paired replay and accounting fields are named in the decision.
- No manifest settings are changed.
</acceptance_criteria>
</task>

<task id="03-01-03" type="execute">
<title>Define required pre-replay gates and approved cleanup boundary</title>
<read_first>
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`
- `work2_coding/Src/formal_readiness.py`
- `work2_coding/Src/study_execution.py`
- `work2_coding/Src/artifact_status.py`
- `work2_coding/scripts/test_frozen_final_settings.py`
- `work2_coding/scripts/test_calibration_protocol.py`
</read_first>
<action>
Add sections named `Required Pre-Replay Gates`, `Approved Phase 4 Cleanup
Boundary`, and `Forbidden Phase 4 Cleanup`. Required gates must include:
freeze/protocol evidence; clean or explicitly claim-eligible git provenance;
checkpoint path, resolved path, SHA-256 hash, sidecar path/hash, and loaded
status; dependency snapshot path/hash; final manifest stability and manifest
hash; seven mainline policy tags; fixed split IDs and seeds; valid paired and
varied fields; source-row checkpoint hashes and load statuses; readiness JSON
path/hash; and generated artifact/claim guard gate authority. Approved cleanup
may repair only paths, metadata, sidecars, hashes, dependency snapshots,
readiness metadata, and evidence-chain records. Forbidden cleanup must include
changes to policy family, split IDs, seeds, metrics, `menu_k`,
`max_candidates`, ETA filter mode, service/opt-out guardrails, checkpoint
policy, or other result-affecting runtime settings.
</action>
<verify>
- `M3_CLAIM_READY_DECISION.md` contains `Required Pre-Replay Gates`.
- `M3_CLAIM_READY_DECISION.md` contains `checkpoint_sha256`.
- `M3_CLAIM_READY_DECISION.md` contains `dependency_snapshot`.
- `M3_CLAIM_READY_DECISION.md` contains `manifest hash`.
- `M3_CLAIM_READY_DECISION.md` contains `menu_k`.
- `M3_CLAIM_READY_DECISION.md` contains `max_candidates`.
- `M3_CLAIM_READY_DECISION.md` contains `ETA filter mode`.
</verify>
<acceptance_criteria>
- GATE-03 defines the exact gates required before final replay.
- The approved cleanup boundary excludes result-affecting changes.
- The decision does not run formal readiness or checkpoint smoke-load commands.
- The future freeze/protocol test files are treated as contracts only, not as Phase 3 deliverables.
</acceptance_criteria>
</task>

<task id="03-01-04" type="execute">
<title>Define claim-by-claim manuscript classification rule</title>
<read_first>
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`
- `work2_coding/Src/manuscript_claims.py`
- `work2_coding/Src/paper_artifacts.py`
</read_first>
<action>
Add sections named `Claim-By-Claim Classification`, `Current Claim Ceiling`,
and `Manuscript Handoff Rule`. Include a table for claim IDs C1 through C8
with current `claim_ready`, current `manuscript_allowed`, and allowed Phase 5
use. State that only `C7_provenance_status_transparency` is currently
claim-ready; `C5_eta_robustness_boundary` is manuscript-allowed only as
diagnostic boundary content; all blocked positive claims remain forbidden.
State that if overall `claim_ready=false` after any authorized replay, Phase 5
may use only claim-specific `manuscript_allowed=true` material with explicit
claim ID, claim status, source artifact, and allowed-use labeling.
</action>
<verify>
- `M3_CLAIM_READY_DECISION.md` contains `Claim-By-Claim Classification`.
- `M3_CLAIM_READY_DECISION.md` contains `C1_central_adaptive_menu_superiority`.
- `M3_CLAIM_READY_DECISION.md` contains `C7_provenance_status_transparency`.
- `M3_CLAIM_READY_DECISION.md` contains `C8_semi_real_case_validation`.
- `M3_CLAIM_READY_DECISION.md` contains `manuscript_allowed`.
- `M3_CLAIM_READY_DECISION.md` contains `diagnostic boundary`.
</verify>
<acceptance_criteria>
- GATE-04 is classified by strict claim guard status, not desired paper narrative.
- One passing claim cannot upgrade the whole paper.
- Diagnostic/provisional materials remain diagnostic or appendix-only.
- The manuscript handoff prevents positive central adaptive-menu superiority unless the guard later authorizes it.
</acceptance_criteria>
</task>

<task id="03-01-05" type="execute">
<title>Define failure, rerun, and diagnostic-lock routing</title>
<read_first>
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-CONTEXT.md`
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
</read_first>
<action>
Add sections named `Phase 4 Routing`, `Pre-Replay Gate Failure`,
`First Final Replay Technical Failure`, `Second Final Replay Failure`, and
`Completed Replay With claim_ready=false`. State that Phase 4 may perform
approved gate cleanup/readiness work and may run final replay only after all
pre-replay gates pass. If pre-replay gates fail, Phase 4 must lock the
diagnostic path without running final replay. If final replay starts and fails
for technical reasons, allow at most one technical rerun with the same
manifest, git SHA, checkpoint path/hash, seeds, splits, policy tags, and
frozen settings. If the second attempt fails, lock diagnostic immediately.
If replay completes but regenerated strict claim guard remains false, proceed
with diagnostic or conditional manuscript path and do not tune the manifest.
</action>
<verify>
- `M3_CLAIM_READY_DECISION.md` contains `Pre-Replay Gate Failure`.
- `M3_CLAIM_READY_DECISION.md` contains `First Final Replay Technical Failure`.
- `M3_CLAIM_READY_DECISION.md` contains `Second Final Replay Failure`.
- `M3_CLAIM_READY_DECISION.md` contains `same manifest, git SHA, checkpoint path/hash, seeds, splits, policy tags, and frozen settings`.
- `M3_CLAIM_READY_DECISION.md` contains `do not tune`.
</verify>
<acceptance_criteria>
- Failure routing cannot be used to probe final results with blocked gates.
- Exactly one same-settings technical rerun is allowed after a technical failure.
- Guard failure after completed replay is treated as evidence, not as permission to tune.
- Phase 4 has a clear handoff to Path A or Path B.
</acceptance_criteria>
</task>

<task id="03-01-06" type="verify">
<title>Run Phase 3 verification and no-evidence-generation checks</title>
<read_first>
- `.planning/phases/03-claim-ready-evidence-decision-gate/03-VALIDATION.md`
- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`
</read_first>
<action>
Run the Phase 3 validation checklist: import smoke from `work2_coding/`,
`python scripts/test_calibration_manifests.py`, source assertions for the M3
decision sections, checks that Phase 3 did not create
`.planning/results/FROZEN_FINAL_SETTINGS.md` or
`.planning/results/CALIBRATION_PROTOCOL.md`, and a generated-evidence diff
name check. Record results in the executor summary when this plan is
executed. Do not run final replay, formal readiness, checkpoint training,
artifact builders, package builders, or claim upgrades.
</action>
<verify>
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` prints `IMPORT_OK`.
- `cd work2_coding; python scripts/test_calibration_manifests.py` prints `PASS: 5 calibration manifest tests`.
- `Test-Path .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md` prints `True`.
- `Test-Path .planning/results/FROZEN_FINAL_SETTINGS.md` prints `False` unless the file existed before Phase 3 execution.
- `Test-Path .planning/results/CALIBRATION_PROTOCOL.md` prints `False` unless the file existed before Phase 3 execution.
- `git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts` prints no paths caused by Phase 3 execution.
</verify>
<acceptance_criteria>
- M3 decision document exists and covers GATE-03 and GATE-04.
- Import smoke exits 0.
- Calibration/final manifest contract test exits 0 or failure is recorded as a blocker.
- Phase 3 creates no freeze/protocol documents.
- Generated evidence files are not modified by Phase 3 execution.
</acceptance_criteria>
</task>
</tasks>

<verification>
Run these checks after executing the plan:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_calibration_manifests.py
cd ..
Test-Path .planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md
Test-Path .planning/results/FROZEN_FINAL_SETTINGS.md
Test-Path .planning/results/CALIBRATION_PROTOCOL.md
git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts
```

Expected results:

- The Python smoke command prints `IMPORT_OK`.
- The manifest test prints `PASS: 5 calibration manifest tests`.
- `M3_CLAIM_READY_DECISION.md` exists.
- Phase 3 did not create `FROZEN_FINAL_SETTINGS.md` or
  `CALIBRATION_PROTOCOL.md`.
- The generated-evidence diff check prints no paths caused by Phase 3
  execution.
</verification>

<success_criteria>
- GATE-03: The project decides whether frozen final settings are valid and
  pre-registered enough to support a legitimate final replay.
- GATE-04: The project classifies the manuscript path as claim-ready
  empirical, conditional diagnostic, or not ready based on evidence rather
  than desired conclusions.
- Current final replay status is `blocked_pending_gate_cleanup`.
- Phase 4 has a gated Path A only after all pre-replay gates pass.
- Phase 4 has a diagnostic-lock Path B for pre-replay gate failure, second
  technical replay failure, or completed replay with `claim_ready=false`.
- No calibration, final replay, formal readiness, checkpoint training,
  artifact/package builder, mirror replacement, case-study execution, or
  manuscript claim upgrade is run by Phase 3.
</success_criteria>

## PLANNING COMPLETE
