---
phase: 02
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md
  - .planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md
  - .planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md
autonomous: true
requirements:
  - GATE-01
  - GATE-02
requirements_addressed:
  - GATE-01
  - GATE-02
must_haves:
  truths:
    - "D-01: Classify dirty working-tree state by risk category rather than listing every changed path."
    - "D-02: Each dirty-git category includes representative paths, risk interpretation, and whether user approval is required."
    - "D-03: Any action that changes the worktree or evidence chain is routed to M2_USER_ACTIONS_REQUIRED.md rather than executed in Phase 2."
    - "D-04: Deleted legacy planning and result files are described as superseded by regenerated planning, not restored or mined unless a specific readiness or claim blocker depends on them."
    - "D-05: M2_PROVENANCE_REQUIREMENTS.md locks checkpoint path, checkpoint SHA-256 hash, sidecar metadata, load status, dependency snapshot, manifest hash, git SHA, git dirty state, readiness JSON path, and readiness JSON hash."
    - "D-06: Missing checkpoint, missing sidecar, load failure, and hash mismatch are separate fail-closed blocker codes."
    - "D-07: Recomputed checkpoint file SHA-256 is authoritative; sidecar metadata cannot substitute for hashing the checkpoint file."
    - "D-08: Phase 2 does not smoke-load checkpoints or write new readiness outputs."
    - "D-09: Phase 2 prioritizes provenance/readiness, checkpoint provenance, dirty git, formal readiness, and artifact packaging blockers that affect Phase 3 go/no-go."
    - "D-10: The four current missing package entries are investigated only to identify source directories and expected patterns."
    - "D-11: The blocker-action matrix uses a Blocker -> Action -> Approval -> Verification shape."
    - "D-12: Empirical performance, tractability, case validation, adaptive-window increment, and central superiority blockers are Not Phase 2 repairs."
    - "D-13: Phase 2 may execute only read-only inspection commands and write planning documents."
    - "D-14: Phase 2 explicitly lists commands that require approval before execution."
    - "D-15: Command templates appear only inside approval-required or not-executed-in-Phase-2 sections."
    - "D-16: Phase 2 verification checks document existence and consistency plus the allowed import smoke; it does not run readiness or artifact generation tests."
  artifacts:
    - path: ".planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md"
      provides: "Non-destructive blocker-to-action matrix for provenance, readiness, checkpoint, dirty-git, and packaging blockers"
    - path: ".planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md"
      provides: "Claim-supporting checkpoint and formal-readiness provenance contract"
    - path: ".planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md"
      provides: "Approval-required cleanup, replay, artifact, mirror, and git actions that Phase 2 did not execute"
  key_links:
    - source: "work2_coding/Src/formal_readiness.py"
      target: ".planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md"
      must: "Document readiness, dependency snapshot, checkpoint sidecar/hash/load, and dirty-git blocker requirements"
    - source: "work2_coding/Src/artifact_status.py"
      target: ".planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md"
      must: "Document artifact claim-ready prerequisites and readiness JSON validation fields"
    - source: "work2_coding/Src/paper_artifacts.py"
      target: ".planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md"
      must: "Explain current missing package entries as expected source-pattern misses"
    - source: "git status --short --branch"
      target: ".planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md"
      must: "Classify dirty state without restore, stash, revert, checkout, reset, delete, or cleanup"
---

# Plan 01 - Gate Cleanup Plan Without Destructive Changes

<objective>
Create the Phase 2 non-destructive cleanup plan for Work2 provenance,
readiness, checkpoint, dirty-git, and artifact-package blockers. The phase
must document what needs approval or later repair before Phase 3 can decide
final replay legitimacy, while preserving the current worktree and generated
evidence untouched.
</objective>

<scope>
In scope:
- Inspect current git status, Phase 1 handoff files, current generated package
  indexes, and gate source modules.
- Classify dirty git state by risk category.
- Document the checkpoint and formal-readiness provenance contract.
- Explain current missing package entries by source pattern and directory.
- Map every recommended cleanup action to a readiness or claim-guard blocker.
- Write all destructive, ambiguous, or evidence-generating actions to
  `M2_USER_ACTIONS_REQUIRED.md` rather than executing them.
- Run only source assertions and the runtime import smoke verification.

Out of scope:
- Running formal readiness, final replay, calibration, checkpoint training,
  artifact builders, package builders, case-study execution, or any command
  that writes generated evidence.
- Editing generated rows, package status, claim guards, figures, tables,
  artifact mirrors, or manuscript claim language.
- Running git restore, stash, reset, checkout, revert, delete cleanup, or
  mirror replacement.
- Deciding whether final replay is legitimate. Phase 3 owns that go/no-go.
</scope>

<must_haves>
<truths>
- D-01: Classify dirty working-tree state by risk category rather than listing every changed path.
- D-02: Each dirty-git category includes representative paths, risk interpretation, and whether user approval is required before any action.
- D-03: Any action that changes the worktree or evidence chain is routed to `M2_USER_ACTIONS_REQUIRED.md` rather than executed in Phase 2.
- D-04: Deleted legacy planning and result files are described as superseded by regenerated planning. Do not restore them or mine git history unless a specific readiness or claim blocker explicitly depends on one legacy file.
- D-05: `M2_PROVENANCE_REQUIREMENTS.md` locks the minimum checkpoint evidence contract: checkpoint path, checkpoint SHA-256 hash, sidecar metadata, checkpoint load status, dependency snapshot, manifest hash, git SHA, git dirty state, readiness JSON path, and readiness JSON hash.
- D-06: Missing checkpoint, missing sidecar, load failure, and hash mismatch are separate fail-closed blocker codes.
- D-07: The recomputed checkpoint file SHA-256 is authoritative. Sidecar metadata is supporting evidence and cannot substitute for hashing the checkpoint file.
- D-08: Phase 2 must not smoke-load checkpoints and must not write new readiness outputs.
- D-09: Phase 2 prioritizes blockers that affect Phase 3 go/no-go: provenance/readiness, checkpoint provenance, dirty git, formal readiness, and artifact packaging.
- D-10: The four current missing package entries are investigated only to identify source directories and expected patterns. Do not create placeholder files, fill scaffold files by hand, regenerate figures, or run builders.
- D-11: The blocker-action matrix uses a `Blocker -> Action -> Approval -> Verification` shape.
- D-12: Empirical performance, tractability, case validation, adaptive-window increment, and central superiority blockers are `Not Phase 2` and routed to Phase 3 or later evidence phases.
- D-13: Phase 2 may execute only read-only inspection commands and write planning documents.
- D-14: Phase 2 explicitly lists commands that require approval before execution: `run_study.py --execute`, `train_shared_checkpoint.py`, `check_formal_readiness.py`, `build_artifacts.py`, `build_phase10_paper_artifacts.py`, final/formal replay, case-study execution, git restore/stash/revert/delete, and mirror replacement.
- D-15: Command templates may appear only inside approval-required or not-executed-in-Phase-2 sections.
- D-16: Phase 2 verification checks document existence and consistency, confirms approval-required actions were not executed, and runs the allowed import smoke. It does not run readiness or artifact generation tests.
</truths>
</must_haves>

<threat_model>
| Threat | Severity | Mitigation |
| --- | --- | --- |
| Destructive git cleanup removes user or regenerated planning changes | high | Use read-only `git status` and document approvals in `M2_USER_ACTIONS_REQUIRED.md`; do not run restore, stash, reset, checkout, revert, or delete cleanup |
| Formal readiness or checkpoint smoke-load writes new outputs during a planning phase | high | Document command templates as approval-required only; do not execute `check_formal_readiness.py` or checkpoint loading commands |
| Generated evidence is altered to satisfy package blockers | high | Explain source-pattern misses and later builder commands; do not edit generated rows, package status, claim guards, figures, tables, or mirrors |
| Diagnostic blockers are misclassified as Phase 2 repairs | high | Mark empirical performance, tractability, case validation, adaptive-window increment, and central superiority as `Not Phase 2` |
| Sidecar metadata is treated as a replacement for checkpoint file hashing | medium | Require recomputed checkpoint SHA-256 as authoritative and sidecar metadata as supporting evidence only |
| Missing package entries are misread as proof of deleted real files | medium | Explain `paper_artifacts.py` synthetic `missing.*` behavior and current source directory contents |
</threat_model>

<tasks>
<task id="02-01-01" type="execute">
<title>Classify dirty git and current blocker state without changing the worktree</title>
<read_first>
- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-CONTEXT.md`
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-RESEARCH.md`
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`
- `.planning/milestones/tr_e_completion/M1_DECISION.md`
</read_first>
<action>
Run read-only status and file inspection commands such as `git status --short
--branch`, directory listings, and source reads. Write the dirty-git section of
`.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`. Use categories
named `regenerated planning core`, `paper boundary docs`, `deleted legacy
planning/results`, `runtime/generated evidence`, and `other user changes`.
For each category, include representative paths, risk interpretation, whether
it blocks claim-ready formal readiness, and whether user approval is required
before any action. State explicitly that Phase 2 did not run restore, stash,
reset, checkout, revert, delete cleanup, or commit normalization.
</action>
<verify>
- `M2_GATE_CLEANUP_PLAN.md` contains `regenerated planning core`.
- `M2_GATE_CLEANUP_PLAN.md` contains `deleted legacy planning/results`.
- `M2_GATE_CLEANUP_PLAN.md` contains `user approval`.
- `M2_GATE_CLEANUP_PLAN.md` contains `did not run restore`.
</verify>
<acceptance_criteria>
- Dirty git state is inspected without reverting, deleting, stashing, or overwriting unrelated files.
- At least five dirty-state categories are documented.
- Each category has representative paths and an approval requirement.
- No generated evidence path is modified by this task.
</acceptance_criteria>
</task>

<task id="02-01-02" type="execute">
<title>Lock checkpoint and formal-readiness provenance requirements</title>
<read_first>
- `work2_coding/Src/formal_readiness.py`
- `work2_coding/Src/study_execution.py`
- `work2_coding/Src/artifact_status.py`
- `work2_coding/Src/paired_replay.py`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-RESEARCH.md`
- `.planning/codebase/INTEGRATIONS.md`
- `.planning/codebase/CONCERNS.md`
</read_first>
<action>
Write `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`.
Include required fields named exactly: `checkpoint_manifest_path`,
`checkpoint_resolved_path`, `checkpoint_sha256`, `checkpoint_sidecar_path`,
`checkpoint_sidecar_sha256`, `checkpoint_load_status`, `dependency_snapshot_path`,
`dependency_snapshot_sha256`, `manifest_path`, `manifest_hash`, `git_sha`,
`git_dirty`, `readiness_json_path`, `readiness_json_sha256`,
`source_row_checkpoint_hashes`, and `source_row_checkpoint_load_statuses`.
Document fail-closed blockers named `missing_checkpoint_path`,
`missing_checkpoint_file`, `missing_formal_checkpoint`,
`missing_checkpoint_sidecar`, `formal_checkpoint_not_loaded`,
`formal_checkpoint_hash_mismatch`, `formal_checkpoint_load_failed`,
`dirty_git`, `missing_dependency_snapshot`, `dependency_snapshot_hash_mismatch`,
and `readiness_manifest_hash_mismatch`. State that recomputed checkpoint
SHA-256 is authoritative and that Phase 2 does not smoke-load checkpoints or
write readiness outputs.
</action>
<verify>
- `M2_PROVENANCE_REQUIREMENTS.md` exists.
- The file contains `checkpoint_sha256`.
- The file contains `checkpoint_load_status`.
- The file contains `readiness_json_sha256`.
- The file contains `recomputed checkpoint SHA-256 is authoritative`.
- The file contains `Phase 2 does not smoke-load checkpoints`.
</verify>
<acceptance_criteria>
- Checkpoint path, hash, sidecar metadata, and load status requirements are documented.
- Dependency snapshot, manifest hash, git SHA, git dirty state, readiness JSON path, and readiness JSON hash are documented.
- Missing checkpoint, missing sidecar, load failure, and hash mismatch are separate fail-closed blockers.
- No checkpoint smoke-load or readiness command is executed.
</acceptance_criteria>
</task>

<task id="02-01-03" type="execute">
<title>Map package and claim blockers to non-destructive cleanup actions</title>
<read_first>
- `work2_coding/Src/paper_artifacts.py`
- `work2_coding/Src/artifact_status.py`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-RESEARCH.md`
</read_first>
<action>
Complete `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md` with a
`Blocker -> Action -> Approval -> Verification` matrix. Include rows for
dirty git, formal readiness, checkpoint provenance, dependency snapshot,
source row checkpoint metadata, current missing package source patterns,
main RC blocked status, strict claim guard ceiling, case scaffold status,
Phase 8 diagnostic status, Phase 9 diagnostic status, and manuscript language
claim ceiling. For the four missing package entries, name the exact current
source paths `.planning/data/case_studies/missing.yml`,
`.planning/data/case_studies/missing.json`,
`work2_coding/artifacts/work2_robust_menu/figures/missing.png`, and
`work2_coding/artifacts/work2_robust_menu/figures/missing.metadata.json`.
Explain that these are synthetic expected-pattern misses from `paper_artifacts.py`.
Mark empirical performance, tractability credibility, case validation,
adaptive-window increment, and central superiority as `Not Phase 2`.
</action>
<verify>
- `M2_GATE_CLEANUP_PLAN.md` contains `Blocker`.
- `M2_GATE_CLEANUP_PLAN.md` contains `Action`.
- `M2_GATE_CLEANUP_PLAN.md` contains `Approval`.
- `M2_GATE_CLEANUP_PLAN.md` contains `Verification`.
- `M2_GATE_CLEANUP_PLAN.md` contains `.planning/data/case_studies/missing.yml`.
- `M2_GATE_CLEANUP_PLAN.md` contains `Not Phase 2`.
</verify>
<acceptance_criteria>
- Formal readiness scripts and artifact builders are inspected.
- Every cleanup recommendation maps to a readiness or claim-guard blocker.
- Four current missing package entries are explained without creating placeholder files.
- Destructive, ambiguous, or evidence-generating cleanup is routed to user approval.
</acceptance_criteria>
</task>

<task id="02-01-04" type="execute">
<title>Write approval-required user action register</title>
<read_first>
- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-CONTEXT.md`
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-RESEARCH.md`
</read_first>
<action>
Write `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`.
Include a table with columns `Action`, `Why approval is required`,
`Blocker addressed`, `Command template`, `Phase 2 status`, and `Verification
after approval`. Include rows for git restore/stash/revert/delete cleanup,
legacy file restoration, checkpoint training, formal readiness, final/formal
replay, artifact builder, Phase 10 package builder, mirror replacement,
case-study execution, and manuscript claim upgrade. Set every row's Phase 2
status to `not executed in Phase 2`.
</action>
<verify>
- `M2_USER_ACTIONS_REQUIRED.md` exists.
- The file contains `run_study.py --execute`.
- The file contains `train_shared_checkpoint.py`.
- The file contains `check_formal_readiness.py`.
- The file contains `build_artifacts.py`.
- The file contains `build_phase10_paper_artifacts.py`.
- The file contains `not executed in Phase 2`.
</verify>
<acceptance_criteria>
- Every destructive or evidence-generating command template is listed as approval-required.
- The file clearly says Phase 2 did not execute those actions.
- The register includes verification-after-approval guidance for each action.
</acceptance_criteria>
</task>

<task id="02-01-05" type="verify">
<title>Run Phase 2 source assertions and import smoke</title>
<read_first>
- `.planning/phases/02-gate-cleanup-plan-without-destructive-changes/02-VALIDATION.md`
- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`
</read_first>
<action>
Run only allowed Phase 2 verification checks: file existence checks for the
three M2 deliverables, source assertions from `02-VALIDATION.md`, the import
smoke command from `work2_coding/`, and a diff-name check for generated
evidence paths. Record verification results in the executor summary when this
plan is executed. Do not run readiness, artifact, package, replay, checkpoint,
or case-study generation commands.
</action>
<verify>
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` prints `IMPORT_OK`.
- `Test-Path .planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md` prints `True`.
- `Test-Path .planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md` prints `True`.
- `Test-Path .planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md` prints `True`.
- `git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts` prints no paths caused by Phase 2 execution.
</verify>
<acceptance_criteria>
- Phase 2 deliverables exist.
- Import smoke exits 0.
- Generated evidence files are not modified by phase execution.
- The executor summary records that readiness/artifact/package/replay/checkpoint/case-study generation commands were not run.
</acceptance_criteria>
</task>
</tasks>

<verification>
Run these checks after executing the plan:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
cd ..
Test-Path .planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md
Test-Path .planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md
Test-Path .planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md
git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts
```

Expected results:

- The Python smoke command prints `IMPORT_OK`.
- All three `Test-Path` commands print `True`.
- The generated-evidence diff check prints no paths caused by Phase 2 execution.
</verification>

<success_criteria>
- GATE-01: Dirty git state is inspected without reverting, deleting, stashing,
  or overwriting unrelated files.
- GATE-02: Checkpoint path, hash, sidecar metadata, and load status
  requirements are documented.
- Formal readiness scripts and artifact builders are inspected.
- Every cleanup recommendation maps to a readiness or claim-guard blocker.
- Destructive or ambiguous cleanup is stopped and routed to user approval.
- No formal readiness, replay, checkpoint training, artifact builder, package
  builder, case-study execution, or manuscript claim upgrade command is run.
</success_criteria>

## PLANNING COMPLETE
