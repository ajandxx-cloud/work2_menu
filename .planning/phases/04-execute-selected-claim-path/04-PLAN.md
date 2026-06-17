---
phase: 04
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/results/CALIBRATION_PROTOCOL.md
  - .planning/results/FROZEN_FINAL_SETTINGS.md
  - .planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md
  - .planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md
  - .planning/milestones/tr_e_completion/M4A_CLAIM_CLASSIFICATION.md
  - .planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md
  - .planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md
  - .planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md
  - work2_coding/outputs/formal_readiness/final_robust_menu/
  - work2_coding/outputs/studies/final_rc/
  - work2_coding/artifacts/work2_robust_menu/final_rc_*/
  - work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts_final_*/
autonomous: true
requirements:
  - PATH-01
  - PATH-02
  - PATH-03
  - PATH-04
requirements_addressed:
  - PATH-01
  - PATH-02
  - PATH-03
  - PATH-04
must_haves:
  truths:
    - "D-01: Try Path A first through strict pre-replay gate cleanup/readiness, and switch to Path B if gates fail."
    - "D-02: Path A receives exactly one strict gate-cleanup/readiness pass; no remediation loop is allowed."
    - "D-03: If final replay starts and fails, times out, or emits incomplete rows for technical reasons, allow at most one same-settings technical rerun."
    - "D-04: The technical rerun must preserve manifest, git SHA, checkpoint hash, seeds, splits, policy tags, and frozen settings."
    - "D-05: If completed replay still yields claim_ready=false, lock Path B without tuning, scale reduction, manifest narrowing, row deletion, or extra replay."
    - "D-06: Phase 4 may create CALIBRATION_PROTOCOL.md and FROZEN_FINAL_SETTINGS.md only from current manifests and current filesystem state."
    - "D-07: Freeze/protocol records are pre-run, non-tuning evidence documents and must not select settings from final outputs."
    - "D-08: Use an existing checkpoint only; do not retrain. If the checkpoint exists, provenance sidecars, hashes, load status, and readiness metadata may be generated."
    - "D-09: Execute the formal readiness command once as the core Path A gate check; blocked readiness switches to Path B."
    - "D-10: If and only if all pre-replay gates pass, run final replay, artifact builder, and Phase 10 package builder without another user pause."
    - "D-11: Successful final replay/artifacts must use an explicit final evidence directory, not overwrite old diagnostic or pilot outputs."
    - "D-12: Canonical generated evidence remains under work2_coding/artifacts; root artifacts is a mirror only after package pass and SHA/drift checks."
    - "D-13: If package building produces missing entries or blockers, do not create placeholders or hand-edit outputs; record blockers and switch to Path B if needed."
    - "D-14: Hand off complete claim traceability to Phase 5 for every usable and unusable claim."
    - "D-15: If gates fail or claim guard remains false, produce the full M4B diagnostic lock package."
    - "D-16: Diagnostic narrative is claim-gated diagnostic service-menu optimization with paired replay and claim-gate transparency."
    - "D-17: Reviewer-risk response prioritizes honest evidence boundary attacks, no-filter/case/tractability diagnostic limits, and claim-guard credibility."
    - "D-18: Phase 5 handoff must prohibit dominance/superiority/improvement/validation/near-optimal wording unless exact claim guard authorization exists."
  artifacts:
    - path: ".planning/results/CALIBRATION_PROTOCOL.md"
      provides: "Current non-tuning calibration protocol and allowed/prohibited knob boundary"
    - path: ".planning/results/FROZEN_FINAL_SETTINGS.md"
      provides: "Current final settings status, final manifest hash, gate commands, and replay authorization state"
    - path: ".planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md"
      provides: "One-pass pre-replay gate and formal-readiness report"
    - path: ".planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md"
      provides: "Durable replay status, row status, blocker, timeout, and rerun accounting"
    - path: ".planning/milestones/tr_e_completion/M4A_CLAIM_CLASSIFICATION.md"
      provides: "Strict post-package claim classification when replay/package generation occurs"
    - path: ".planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md"
      provides: "Diagnostic-path lock when gates, replay, package, or strict guard do not authorize claim-ready writing"
    - path: ".planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md"
      provides: "Claim ID, status, source path, allowed use, and prohibited wording handoff"
    - path: ".planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md"
      provides: "Reviewer-risk response plan for evidence boundary and claim-safety attacks"
  key_links:
    - source: ".planning/phases/04-execute-selected-claim-path/04-CONTEXT.md"
      target: ".planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md"
      must: "Translate D-01 through D-18 into concrete gate results and routing"
    - source: "work2_coding/Experiments/studies/final_robust_menu.yaml"
      target: ".planning/results/FROZEN_FINAL_SETTINGS.md"
      must: "Record final manifest path/hash, seven policy tags, splits/seeds, paired fields, varied fields, and selected runtime knobs"
    - source: "work2_coding/outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json"
      target: ".planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md"
      must: "Readiness status controls whether final replay is authorized"
    - source: "work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts_final_*/CLAIM_GUARD.json"
      target: ".planning/milestones/tr_e_completion/M4A_CLAIM_CLASSIFICATION.md"
      must: "Strict regenerated guard determines the final claim ceiling"
---

# Plan 01 - Execute Selected Claim Path

<objective>
Execute Phase 4's selected claim path without result-chasing. The phase first
attempts Path A through a single strict pre-replay gate pass. It runs final
replay only if all gates pass from current manifests and current filesystem
state. If any gate remains blocked, if two same-settings technical replay
attempts fail, or if regenerated strict `CLAIM_GUARD.json` remains
`claim_ready=false`, the phase locks Path B and hands Phase 5 a diagnostic,
claim-safe manuscript package.
</objective>

<scope>
In scope:
- Create current, non-tuning freeze/protocol records from the current
  calibration and final manifests.
- Run manifest/protocol/freeze contract tests.
- Run one formal readiness pass for `final_robust_menu` and inspect
  `FORMAL_READINESS.json`.
- If and only if all pre-replay gates pass, run the final replay and at most
  one same-settings technical rerun.
- Regenerate artifacts and a strict Phase 10 package only from generated source
  rows and readiness metadata.
- Write Path A and/or Path B milestone handoff documents under
  `.planning/milestones/tr_e_completion/`.
- Keep all claims bounded by strict `CLAIM_GUARD.json`.

Out of scope:
- Retraining checkpoints.
- Restoring or mining deleted legacy planning/results files.
- Changing policy tags, split IDs, seeds, metrics, acceptance/accounting
  definitions, checkpoint policy/path except approved pre-replay provenance
  repair, `menu_k`, `max_candidates`, ETA filter mode, guardrails, product
  mode, time-window mode, menu-contract mode, pricing mode, or row inclusion
  after seeing evidence.
- Hand-editing generated rows, package status, package indexes, figures,
  tables, mirrors, or claim guards.
- Running more than one readiness pass or more than one same-settings
  technical rerun.
- Upgrading manuscript wording beyond exact strict-guard authorization.
</scope>

<must_haves>
<truths>
- D-01: Phase 4 tries Path A first through strict gates, and switches to Path B if gates fail.
- D-02: Path A has one strict gate-cleanup/readiness pass only.
- D-03: A final replay technical failure permits at most one same-settings technical rerun.
- D-04: The same-settings technical rerun preserves manifest, git SHA, checkpoint hash, seeds, splits, policy tags, and frozen settings.
- D-05: Completed replay with regenerated `claim_ready=false` is evidence and triggers Path B without tuning.
- D-06: `CALIBRATION_PROTOCOL.md` and `FROZEN_FINAL_SETTINGS.md` are created only from current manifests and filesystem state.
- D-07: Freeze/protocol records are pre-run/non-tuning documents.
- D-08: Phase 4 uses an existing checkpoint only and never retrains it.
- D-09: One formal readiness command is the core Path A gate check.
- D-10: Artifact and package builders run only after all pre-replay gates pass.
- D-11: Final replay/artifacts use explicit final evidence directories.
- D-12: `work2_coding/artifacts/...` remains canonical; root `artifacts/...` is mirror-only after package pass and drift checks.
- D-13: Missing package entries or blockers are recorded, not patched by placeholders or hand edits.
- D-14: Phase 5 receives complete claim traceability for usable and unusable claims.
- D-15: Gate failure or guard-false output produces the full M4B diagnostic lock package.
- D-16: Diagnostic manuscript framing is claim-gated service-menu optimization with paired replay and transparent claim gates.
- D-17: Reviewer-risk response covers evidence boundary, no-filter/case/tractability limits, and claim-guard credibility.
- D-18: Phase 5 handoff prohibits dominance, superiority, improvement, real-passenger validation, and near-optimality language unless exact strict-guard authorization exists.
</truths>
</must_haves>

<threat_model>
| Threat | Severity | Mitigation |
| --- | --- | --- |
| Gate cleanup turns into result-affecting tuning | high | Restrict cleanup to current-manifest freeze/protocol records, metadata, hashes, sidecars, dependency/readiness records, and evidence-chain documentation |
| Missing checkpoint or dirty git is bypassed to force replay | high | Inspect `FORMAL_READINESS.json`; replay is authorized only when readiness status is `passed`, `claim_ready_allowed=true`, and all pre-replay gates pass |
| Final replay failure leads to repeated attempts or scale reduction | high | Allow one same-settings technical rerun only; second failure locks Path B |
| Generated rows or claim guard are edited by hand | high | Use only `run_study.py`, `build_artifacts.py`, and `build_phase10_paper_artifacts.py`; verification checks generated-evidence diffs and source reports |
| Root artifact mirror is treated as independent evidence | medium | Build explicit final package under `work2_coding/artifacts/...`; update mirror only after package pass and SHA/drift checks |
| Diagnostic material is promoted to positive manuscript claims | high | Build M4B safe claim table and use strict claim IDs/status/allowed-use labels for Phase 5 |
</threat_model>

<tasks>
<task id="04-01-01" type="execute">
<title>Create current non-tuning freeze and calibration protocol records</title>
<read_first>
- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/04-execute-selected-claim-path/04-CONTEXT.md`
- `.planning/phases/04-execute-selected-claim-path/04-RESEARCH.md`
- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml`
- `work2_coding/Experiments/studies/final_robust_menu.yaml`
- `work2_coding/scripts/test_calibration_protocol.py`
- `work2_coding/scripts/test_frozen_final_settings.py`
</read_first>
<action>
Create `.planning/results/` if needed. Write
`.planning/results/CALIBRATION_PROTOCOL.md` from the current calibration and
final manifests only. Include headings required by
`test_calibration_protocol.py`: `Allowed Calibration Knobs`,
`Prohibited Tuning Actions`, `Pilot Selection Rule`,
`Pilot And Final Separation`, `Final Freeze And Rerun Rule`,
`Second-Round Limit`, and `Downgrade Rule`. State that Phase 4 diagnostics are
a non-tuning input and not a better ranking.

Write `.planning/results/FROZEN_FINAL_SETTINGS.md` from current manifest
fields and current filesystem state. Include `final_status:` with one of
`frozen`, `blocked_pending_gate_cleanup`, or `conditional_reframe_selected`.
Include final manifest path/hash, calibration manifest path/hash, seven policy
tags, split IDs and seeds, checkpoint path, checkpoint hash if the current
file exists, paired fields, varied fields, and gate commands. If any gate is
currently blocked, state exactly that final rerun is not authorized and name
the blockers, including `dirty_git` and artifact status where applicable.
Do not restore legacy results or edit runtime manifests.
</action>
<verify>
- `Test-Path .planning/results/CALIBRATION_PROTOCOL.md` prints `True`.
- `Test-Path .planning/results/FROZEN_FINAL_SETTINGS.md` prints `True`.
- `CALIBRATION_PROTOCOL.md` contains `final-result tuning`, `seed deletion`, `baseline deletion`, `generated-row edits`, `single profit ranking`, `phase 4`, `diagnostic`, `non-tuning input`, and `not a better ranking`.
- `FROZEN_FINAL_SETTINGS.md` contains `final_status:`, `final manifest path`, `final manifest hash`, `calibration manifest path`, `calibration manifest hash`, `seven policy tags`, `split ids and seeds`, `checkpoint path`, `paired fields`, `varied fields`, and `gate commands`.
</verify>
<acceptance_criteria>
- The freeze/protocol records are current-state evidence documents, not final-output tuning records.
- The files are derived from current manifests and current filesystem state.
- No runtime manifest, generated row, artifact status, package status, figure, table, mirror, or claim guard is hand-edited.
- PATH-01 is protected by making replay authorization explicit before any replay command.
</acceptance_criteria>
</task>

<task id="04-01-02" type="execute">
<title>Run the one-pass pre-replay gate and formal readiness check</title>
<read_first>
- `.planning/results/CALIBRATION_PROTOCOL.md`
- `.planning/results/FROZEN_FINAL_SETTINGS.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`
- `work2_coding/Src/formal_readiness.py`
- `work2_coding/Src/artifact_status.py`
- `work2_coding/scripts/test_calibration_manifests.py`
- `work2_coding/scripts/test_calibration_protocol.py`
- `work2_coding/scripts/test_frozen_final_settings.py`
</read_first>
<action>
Run these commands from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_calibration_manifests.py
python scripts/test_calibration_protocol.py
python scripts/test_frozen_final_settings.py
python scripts/check_formal_readiness.py --study final_robust_menu --output-root outputs/formal_readiness --diagnostic-ok
```

Inspect `outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json`.
Write `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md`
with the command outputs, readiness JSON path/hash, dependency snapshot
path/hash, manifest hash, git SHA/dirty state, checkpoint path/hash/sidecar
path/sidecar hash/load status, blocker codes, and a routing decision.

If readiness status is anything other than `passed`, or
`claim_ready_allowed` is not `true`, or any required Phase 3 pre-replay gate is
blocked, set `FROZEN_FINAL_SETTINGS.md` `final_status:
blocked_pending_gate_cleanup`, state that final replay is not authorized, and
route directly to task `04-01-03`. Do not run readiness again in this phase.
</action>
<verify>
- The import smoke prints `IMPORT_OK`.
- `test_calibration_manifests.py`, `test_calibration_protocol.py`, and `test_frozen_final_settings.py` exit 0.
- `outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json` exists.
- `M4A_PRE_REPLAY_GATE_REPORT.md` contains `FORMAL_READINESS.json`, `readiness status`, `claim_ready_allowed`, `git_dirty`, `checkpoint`, `dependency_snapshot`, `manifest hash`, and `routing decision`.
</verify>
<acceptance_criteria>
- Exactly one formal readiness pass is executed for Path A.
- Replay is authorized only when all readiness and pre-replay gates pass.
- Blocked readiness is treated as a Path B trigger, not permission for remediation loops.
- PATH-01 remains satisfied because no final replay occurs on blocked gates.
</acceptance_criteria>
</task>

<task id="04-01-03" type="execute">
<title>Lock diagnostic Path B when pre-replay gates remain blocked</title>
<read_first>
- `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md`
- `.planning/results/FROZEN_FINAL_SETTINGS.md`
- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
</read_first>
<action>
Skip this task only if task `04-01-02` recorded that all pre-replay gates
passed. Otherwise write the full Path B diagnostic package:

- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md`
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md`

The diagnostic lock must state that final replay was not run, identify the
blocking gate(s), preserve the current evidence boundary, and classify the
Phase 5 manuscript as conditional diagnostic service-menu optimization.

The safe claim table must include all strict claim IDs C1 through C8, current
or regenerated support status, claim-ready flag, manuscript-allowed flag,
source artifact path, allowed manuscript use, blocker reason, and prohibited
language. It must explicitly preserve opt-out/home separation, no-filter
diagnostic status, scaffold-only case limits, and blocked exact/greedy
credibility.

The reviewer-risk plan must address why the paper does not claim superiority,
why no-filter/case/tractability evidence is diagnostic, why final replay did
not run or did not authorize stronger claims, and why the claim guard is the
authority.
</action>
<verify>
- `M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md` exists and contains `conditional diagnostic`, `final replay was not run` or `claim_ready=false`, and `claim-gated`.
- `M4B_SAFE_CLAIM_TABLE.md` exists and contains all claim IDs C1 through C8.
- `M4B_SAFE_CLAIM_TABLE.md` contains `dominates`, `superior`, `improves`, `validates real passengers`, and `near-optimal` as prohibited language unless authorized.
- `M4B_REVIEWER_RISK_RESPONSE_PLAN.md` exists and contains `no-filter`, `case`, `tractability`, `claim guard`, and `evidence boundary`.
</verify>
<acceptance_criteria>
- PATH-03 is satisfied when claim-ready evidence is unavailable.
- PATH-04 is satisfied by using strict claim guard output as the claim ceiling.
- Phase 5 receives enough claim-safe material to draft without rediscovering raw JSON.
- No generated evidence file is hand-edited.
</acceptance_criteria>
</task>

<task id="04-01-04" type="execute">
<title>Run final replay only after all pre-replay gates pass</title>
<read_first>
- `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md`
- `.planning/results/FROZEN_FINAL_SETTINGS.md`
- `work2_coding/Experiments/studies/final_robust_menu.yaml`
- `work2_coding/Src/study_execution.py`
- `work2_coding/Src/paired_replay.py`
- `work2_coding/scripts/run_study.py`
</read_first>
<action>
Run this task only if task `04-01-02` records all pre-replay gates as passed
and `FROZEN_FINAL_SETTINGS.md` records `final_status: frozen`. Run from
`work2_coding/`:

```powershell
python scripts/run_study.py --study final_robust_menu --execute --output-root outputs/studies/final_rc
```

Read the generated `study_summary.json`, `blockers.json` if present, and
`normalized_rows.json`. Write or update
`.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md` with run
directory, manifest hash, git SHA, checkpoint path/hash/load status, row
counts by `execution_status`, completed/failed/blocked/incomplete/missing row
counts, timeout/infeasible/failure evidence if present, policy tags, split IDs,
and whether artifact generation may proceed.

If the first replay fails, times out, or emits incomplete rows for technical
reasons after all gates had passed, run the exact same command at most one
more time. The rerun must use the same manifest, git SHA, checkpoint path/hash,
seeds, splits, policy tags, and frozen settings. Record both run directories
and compare those invariants in `M4A_FINAL_REPLAY_REPORT.md`.

If the second attempt fails, times out, or remains incomplete, stop replay and
run task `04-01-03` to lock Path B. Do not reduce scale, remove rows, remove
baselines, edit manifests, or run a third attempt.
</action>
<verify>
- If replay is skipped, `M4A_FINAL_REPLAY_REPORT.md` states `not_run` and names the blocking gate.
- If replay runs, `outputs/studies/final_rc/final_robust_menu/*/study_summary.json` exists.
- `M4A_FINAL_REPLAY_REPORT.md` contains `completed`, `failed`, `blocked`, `incomplete`, `missing`, `manifest hash`, `checkpoint`, `policy tags`, `split IDs`, and `technical rerun`.
- If a rerun occurs, the report contains `same manifest`, `same git SHA`, `same checkpoint`, `same seeds`, `same splits`, and `same policy tags`.
</verify>
<acceptance_criteria>
- PATH-01 is satisfied because final replay runs only after pre-registered gates pass.
- PATH-02 is satisfied because completed, failed, timeout, infeasible, blocked, and missing row states are represented durably.
- A second technical failure locks Path B immediately.
- No result-affecting setting is changed after evidence is observed.
</acceptance_criteria>
</task>

<task id="04-01-05" type="execute">
<title>Build final artifacts and explicit Phase 10 package only from completed source rows</title>
<read_first>
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md`
- `work2_coding/outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json`
- `work2_coding/Src/artifact_builder.py`
- `work2_coding/Src/artifact_status.py`
- `work2_coding/Src/paper_artifacts.py`
- `work2_coding/Src/manuscript_claims.py`
- `work2_coding/scripts/build_artifacts.py`
- `work2_coding/scripts/build_phase10_paper_artifacts.py`
</read_first>
<action>
Run this task only if task `04-01-04` produced completed final rows with no
blocking or incomplete row states. Derive `FINAL_EVIDENCE_ID` from the selected
final run ID or manifest hash. Run from `work2_coding/`:

```powershell
python scripts/build_artifacts.py --study final_robust_menu --study-output-root outputs/studies/final_rc --output-root artifacts/work2_robust_menu/final_rc_<FINAL_EVIDENCE_ID> --claim-ready --readiness-json outputs/formal_readiness/final_robust_menu/FORMAL_READINESS.json
python scripts/build_phase10_paper_artifacts.py --output-root artifacts/work2_robust_menu/phase10_paper_artifacts_final_<FINAL_EVIDENCE_ID> --main-artifact-root artifacts/work2_robust_menu/final_rc_<FINAL_EVIDENCE_ID> --no-mirror
```

Read `ARTIFACT_STATUS.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`,
`ARTIFACT_TO_SECTION_MAP.json`, and `CLAIM_GUARD.json` from the explicit final
artifact/package directories. If package status has missing entries, blockers,
or `claim_ready=false`, do not create placeholders and do not hand-edit
generated outputs. Record the blocker and route to task `04-01-06`.

If package status passes and the strict guard is claim-ready, optionally update
the root mirror only through:

```powershell
python scripts/build_phase10_paper_artifacts.py --output-root artifacts/work2_robust_menu/phase10_paper_artifacts_final_<FINAL_EVIDENCE_ID> --main-artifact-root artifacts/work2_robust_menu/final_rc_<FINAL_EVIDENCE_ID> --default-mirror
```

Then record SHA-256 checks for the four key package JSON files between the
canonical final package and the root mirror.
</action>
<verify>
- If artifact/package generation is skipped, `M4A_FINAL_REPLAY_REPORT.md` names the reason.
- If artifact generation runs, `artifacts/work2_robust_menu/final_rc_<FINAL_EVIDENCE_ID>/ARTIFACT_STATUS.json` exists.
- If package generation runs, `artifacts/work2_robust_menu/phase10_paper_artifacts_final_<FINAL_EVIDENCE_ID>/CLAIM_GUARD.json` and `PACKAGE_STATUS.json` exist.
- No generated row, package status, package index, figure, table, or claim guard is modified by hand.
- If a mirror is updated, SHA checks for `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and `ARTIFACT_TO_SECTION_MAP.json` are recorded.
</verify>
<acceptance_criteria>
- Final evidence is written under explicit final directories.
- Artifact and package builders consume generated rows and readiness metadata only.
- Missing package entries or blockers are recorded rather than patched.
- Root mirror use remains paper-facing and traceable.
</acceptance_criteria>
</task>

<task id="04-01-06" type="execute">
<title>Classify regenerated claims and choose claim-ready or diagnostic handoff</title>
<read_first>
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts_final_*/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts_final_*/PACKAGE_STATUS.json`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `.planning/milestones/tr_e_completion/M3_CLAIM_READY_DECISION.md`
</read_first>
<action>
Write `.planning/milestones/tr_e_completion/M4A_CLAIM_CLASSIFICATION.md` if
final artifact/package generation ran. Include one row per strict claim ID
with support status, claim-ready flag, manuscript-allowed flag, source artifact
paths, allowed use, and blocker reason.

If regenerated `CLAIM_GUARD.json` has `claim_ready=true`, classify the Phase 5
handoff as claim-ready only for the exact claim IDs authorized by the guard.
Still prohibit universal dominance, real passenger validation, no-filter
operational recommendation, and near-optimal greedy language unless the exact
claim authorizes it.

If regenerated `CLAIM_GUARD.json` has `claim_ready=false`, treat that result as
evidence. Do not tune, rerun, narrow manifests, remove baselines, delete rows,
or hand-edit outputs. Run task `04-01-03` to produce the full diagnostic lock
package using the regenerated package as the source when available.
</action>
<verify>
- If final package exists, `M4A_CLAIM_CLASSIFICATION.md` exists and contains all claim IDs C1 through C8.
- `M4A_CLAIM_CLASSIFICATION.md` contains `claim_ready`, `manuscript_allowed`, `source artifact`, `allowed use`, and `blocker reason`.
- If strict guard remains false, the M4B diagnostic lock files exist and cite the regenerated guard.
- If strict guard is true, the classification names the exact authorized claim IDs and keeps unrelated claims blocked.
</verify>
<acceptance_criteria>
- PATH-04 is satisfied because strict `CLAIM_GUARD.json` determines the final claim ceiling.
- PATH-03 is satisfied whenever claim-ready evidence is unavailable.
- Phase 5 receives explicit allowed/prohibited language and claim traceability.
- No extra replay or tuning follows a guard-false result.
</acceptance_criteria>
</task>

<task id="04-01-07" type="verify">
<title>Run Phase 4 verification and evidence-boundary checks</title>
<read_first>
- `.planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md`
- `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md`
- `.planning/milestones/tr_e_completion/M4A_CLAIM_CLASSIFICATION.md`
- `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`
- `.planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md`
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md`
</read_first>
<action>
Run the verification suite appropriate to the chosen path:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_calibration_manifests.py
python scripts/test_calibration_protocol.py
python scripts/test_frozen_final_settings.py
python scripts/test_formal_readiness.py
python scripts/test_checkpoint_provenance.py
python scripts/test_artifact_gates.py
python scripts/test_phase10_paper_artifacts.py
python scripts/test_manuscript_claim_guard.py
cd ..
```

Then check that either the Path A classification exists with a regenerated
strict guard source, or the full M4B diagnostic lock package exists. Record the
verification commands and results in the executor summary. Include a
`git diff --name-only` review focused on generated-evidence roots and state
which changes were produced by approved script commands versus planning docs.
</action>
<verify>
- Import smoke prints `IMPORT_OK`.
- Manifest/protocol/freeze tests pass.
- Formal readiness, checkpoint provenance, artifact gate, Phase 10 package, and manuscript claim guard tests pass or any failure is recorded as a blocker in the M4B lock.
- Either `M4A_CLAIM_CLASSIFICATION.md` or all three M4B files exist.
- Generated evidence changes are traceable to approved scripts; no hand edits are reported.
</verify>
<acceptance_criteria>
- PATH-01 through PATH-04 are covered by milestone documents and generated gate outputs.
- Verification records the selected path and why the alternative path was not used.
- Phase 5 can proceed with a clear claim ceiling and source artifact map.
- The executor summary records that no generated rows, package status, figures, tables, mirrors, or claim guards were hand-edited.
</acceptance_criteria>
</task>
</tasks>

<verification>
Run these checks after executing the plan:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_calibration_manifests.py
python scripts/test_calibration_protocol.py
python scripts/test_frozen_final_settings.py
python scripts/test_formal_readiness.py
python scripts/test_checkpoint_provenance.py
python scripts/test_artifact_gates.py
python scripts/test_phase10_paper_artifacts.py
python scripts/test_manuscript_claim_guard.py
cd ..
Test-Path .planning/milestones/tr_e_completion/M4A_PRE_REPLAY_GATE_REPORT.md
Test-Path .planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md
Test-Path .planning/milestones/tr_e_completion/M4B_SAFE_CLAIM_TABLE.md
Test-Path .planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md
```

Expected results depend on the selected path:

- Path A may proceed to replay only if `FORMAL_READINESS.json` reports
  `status=passed` and all Phase 3 pre-replay gates pass.
- Path B is expected if readiness remains blocked, replay fails twice, package
  blockers remain, or strict `CLAIM_GUARD.json` remains `claim_ready=false`.
- In all cases, Phase 4 must produce either a strict claim classification from
  regenerated package outputs or the full diagnostic lock package.
</verification>

<success_criteria>
- PATH-01: Final replay occurs only when pre-registered gates pass from current
  manifests and current filesystem state.
- PATH-02: Completed, failed, timeout, infeasible, blocked, and missing row
  states are represented durably when replay is run or skipped.
- PATH-03: If claim-ready evidence is unavailable, the paper is locked as a
  conditional diagnostic TR-E manuscript.
- PATH-04: Strict `CLAIM_GUARD.json` output determines the final claim ceiling.
- `CALIBRATION_PROTOCOL.md` and `FROZEN_FINAL_SETTINGS.md` are non-tuning,
  current-state records.
- No generated row, table, figure, package status, package index, mirror, or
  claim guard is hand-edited.
- Phase 5 receives complete claim traceability and allowed/prohibited language.
</success_criteria>

## PLANNING COMPLETE
