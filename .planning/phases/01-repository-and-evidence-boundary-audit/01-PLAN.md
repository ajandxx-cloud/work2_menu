---
phase: 01
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md
  - .planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md
  - .planning/milestones/tr_e_completion/M1_DECISION.md
autonomous: true
requirements:
  - EVID-01
  - EVID-02
  - EVID-03
  - EVID-04
requirements_addressed:
  - EVID-01
  - EVID-02
  - EVID-03
  - EVID-04
must_haves:
  truths:
    - "D-01: Canonical generated paper artifact package is work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/."
    - "D-02: Root artifacts/work2_robust_menu/phase10_paper_artifacts/ is a paper-facing mirror, not independent evidence."
    - "D-03: Mirror drift check is limited to CLAIM_GUARD.json, PACKAGE_STATUS.json, PACKAGE_INDEX.json, and ARTIFACT_TO_SECTION_MAP.json."
    - "D-04: The audit records top-level fields, source_family_status, blocked claim IDs, and support_status without copying whole JSON files."
    - "D-05: M1_BLOCKER_LIST.md uses a readable six-class summary plus a traceable matrix."
    - "D-06: The six blocker classes are provenance/readiness, empirical performance, artifact packaging, manuscript language, case-study, and computational tractability."
    - "D-07: The traceable matrix covers 74 Phase 10 package artifacts and 8 strict claim guard claims."
    - "D-08: Blockers are classified from package fields where possible, with short human explanations for clusters."
    - "D-09: Phase 1 states current package is not claim-ready and leans diagnostic-only, while Phase 2/3 decide legitimate final replay feasibility."
    - "D-10: M1_DECISION.md recommends Phase 3 decide between legitimate final replay and diagnostic lock."
    - "D-11: Phase 1 does not run cleanup, rerun experiments, tune settings, or upgrade claims."
    - "D-12: Current dirty git state, regenerated planning files, and deleted legacy planning/results files are recorded as evidence boundary."
    - "D-13: Deleted legacy planning/results files are a provenance risk, not an automatic Phase 1 blocker."
    - "D-14: Phase 1 does not restore or deeply mine deleted legacy files unless directly required for current boundary evidence."
    - "D-15: manuscript/main.tex is present and may only be inspected for claim-boundary wording risks."
    - "D-16: Phase 1 may run read-only parsing, file existence checks, JSON summarizers, git status, and import smoke."
    - "D-17: Phase 1 must not run run_study.py --execute, artifact builders, package builders, checkpoint training, final replay, calibration, or evidence regeneration."
    - "D-18: Runtime smoke verification is limited to importing Src.config from the active work2_coding root."
    - "D-19: Phase 2 focuses on provenance/readiness cleanup planning without destructive changes."
    - "D-20: Phase 3 decides whether frozen final settings and calibration/final-test separation justify legitimate final replay or diagnostic lock."
  artifacts:
    - path: ".planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md"
      provides: "Current repository, runtime, artifact, manuscript, and git evidence boundary"
    - path: ".planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md"
      provides: "Six-class blocker summary and traceability matrix for artifacts and claims"
    - path: ".planning/milestones/tr_e_completion/M1_DECISION.md"
      provides: "Conditional evidence-path decision and Phase 2/3 handoff"
  key_links:
    - source: "work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json"
      target: ".planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md"
      must: "Audit records strict claim statuses and claim ceiling"
    - source: "work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json"
      target: ".planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md"
      must: "Blocker list traces package blocker state without editing generated JSON"
---

# Plan 01 - Repository And Evidence Boundary Audit

<objective>
Create the Phase 1 read-only evidence-boundary audit for the current Work2 TR-E
manuscript project. The audit must record the current repository, planning,
manuscript, runtime, generated package, and strict claim-guard state before any
repair, final replay, artifact regeneration, or manuscript claim upgrade.
</objective>

<scope>
In scope:
- Read current planning docs, codebase maps, manuscript source, git status, and
  generated package metadata.
- Summarize the four key canonical JSON files:
  `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and
  `ARTIFACT_TO_SECTION_MAP.json`.
- Check root mirror drift for those four JSON files only.
- Classify current claim-readiness blockers into the required six classes.
- Write the three Phase 1 milestone documents.
- Run only the runtime import smoke verification.

Out of scope:
- Running `run_study.py --execute`, final replay, calibration, checkpoint
  training, case-study execution, artifact builders, package builders, or any
  command that regenerates evidence.
- Editing `work2_coding/outputs/`, `work2_coding/artifacts/`, root
  `artifacts/`, generated result rows, claim guards, package status, paper
  artifact files, or manuscript source.
- Restoring, deleting, stashing, or reverting unrelated dirty git changes.
</scope>

<must_haves>
<truths>
- D-01: Treat `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/` as the canonical generated paper artifact package.
- D-02: Treat root `artifacts/work2_robust_menu/phase10_paper_artifacts/` as a paper-facing mirror only.
- D-03: Check mirror drift only for `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and `ARTIFACT_TO_SECTION_MAP.json`.
- D-04: Record top-level fields, `source_family_status`, blocked claim IDs, and each claim's `support_status` without copying entire large JSON files.
- D-05: `M1_BLOCKER_LIST.md` uses a readable six-class summary plus a traceable matrix.
- D-06: The six blocker classes are provenance/readiness, empirical performance, artifact packaging, manuscript language, case-study, and computational tractability.
- D-07: The traceable matrix covers the Phase 10 package's 74 artifacts and the strict claim guard's 8 claims.
- D-08: Classify blockers automatically from package fields where possible, then add short human explanation for each cluster.
- D-09: Phase 1 states that the current generated package is not claim-ready and leans diagnostic-only, while Phase 2/3 still decide whether a legitimate final replay path exists.
- D-10: `M1_DECISION.md` recommends Phase 3 decide between legitimate final replay and diagnostic lock, with the current package leaning diagnostic.
- D-11: Phase 1 does not run cleanup, rerun experiments, tune settings, or upgrade claims.
- D-12: Record the current dirty git state, including regenerated planning files and deleted legacy planning/results files, as part of the evidence boundary.
- D-13: Treat deleted legacy planning/results files as provenance risk, not an automatic Phase 1 blocker.
- D-14: Do not restore or deeply mine deleted legacy files unless a deleted file directly affects the current evidence boundary.
- D-15: Treat `manuscript/main.tex` as present; inspect it only for claim-boundary wording risks and do not edit it.
- D-16: Allowed commands are read-only parsing, file existence checks, JSON summarizers, `git status`, and the import smoke check.
- D-17: Forbidden commands include `run_study.py --execute`, artifact builders, package builders, checkpoint training, final replay, calibration, and evidence regeneration.
- D-18: Runtime smoke verification is limited to importing `Src.config` from the active `work2_coding/` root.
- D-19: Phase 2 focuses on provenance/readiness cleanup planning without destructive changes.
- D-20: Phase 3 decides whether frozen final settings and calibration/final-test separation justify legitimate final replay or diagnostic lock.
</truths>
</must_haves>

<threat_model>
| Threat | Severity | Mitigation |
| --- | --- | --- |
| Generated evidence is accidentally modified during audit | high | Use read-only commands; verification checks diff paths under `work2_coding/outputs`, `work2_coding/artifacts`, and root `artifacts` |
| Current dirty git state is accidentally normalized away | high | Record dirty status only; do not restore, revert, stash, delete, or checkout user changes |
| Diagnostic artifacts are promoted into positive manuscript claims | high | Anchor decision wording to `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, and `.planning/paper/CLAIM_SAFE_LANGUAGE.md` |
| Mirror package is treated as independent evidence | medium | Compare hashes for four key JSON files and name runtime package as canonical |
| Manuscript wording risk becomes manuscript editing work | medium | Inspect `manuscript/main.tex` for line references only; defer edits to manuscript phases |
</threat_model>

<tasks>
<task id="01-01-01" type="execute">
<title>Inventory current repository, planning, runtime, and generated evidence boundary</title>
<read_first>
- `AGENTS.md`
- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-RESEARCH.md`
- `.planning/codebase/ARCHITECTURE.md`
- `.planning/codebase/STRUCTURE.md`
- `.planning/codebase/CONCERNS.md`
- `.planning/codebase/CONVENTIONS.md`
- `.planning/codebase/INTEGRATIONS.md`
- `.planning/codebase/STACK.md`
- `.planning/codebase/TESTING.md`
</read_first>
<action>
Create `.planning/milestones/tr_e_completion/` if it does not exist. Write
`.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md` with
sections named `Scope`, `Current Workspace Boundary`, `Planning Boundary`,
`Runtime Boundary`, `Generated Evidence Boundary`, `Manuscript Boundary`,
`Dirty Git Boundary`, and `No-Modification Statement`. Record that
`work2_coding/` is the active runtime root and that `ooh_code/` references are
stale until verified. Include the current `git status --short --branch` summary
without changing git state.
</action>
<verify>
- `M1_EVIDENCE_BOUNDARY_AUDIT.md` exists.
- The file contains `work2_coding/`.
- The file contains `No experiments were run`.
- The file contains `No generated evidence was modified`.
- The file contains `git status`.
</verify>
<acceptance_criteria>
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md` exists.
- The audit contains the exact string `work2_coding/`.
- The audit contains the exact string `No experiments were run`.
- The audit contains the exact string `No generated evidence was modified`.
- The audit records dirty git state without changing unrelated files.
</acceptance_criteria>
</task>

<task id="01-01-02" type="execute">
<title>Record canonical Phase 10 JSON status and mirror drift</title>
<read_first>
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
- `artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
- `artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
</read_first>
<action>
Update `M1_EVIDENCE_BOUNDARY_AUDIT.md` with a `Phase 10 Package Snapshot`
section. Record canonical and mirror paths, SHA-256 match status for the four
key JSON files, `PACKAGE_STATUS.json` schema/version fields, `claim_ready`,
`strict_claim_guard_claim_ready`, artifact counts, blocker count,
`source_family_status`, package tier counts, missing artifact IDs, and the
strict claim guard table with all 8 claim IDs and `support_status` values.
Do not paste full JSON documents.
</action>
<verify>
- `M1_EVIDENCE_BOUNDARY_AUDIT.md` contains `phase10-paper-artifact-package-v1`.
- `M1_EVIDENCE_BOUNDARY_AUDIT.md` contains `phase10-strict-claim-guard-v1`.
- `M1_EVIDENCE_BOUNDARY_AUDIT.md` contains `artifact_count`.
- `M1_EVIDENCE_BOUNDARY_AUDIT.md` contains `C7_provenance_status_transparency`.
- `M1_EVIDENCE_BOUNDARY_AUDIT.md` contains all four JSON filenames.
</verify>
<acceptance_criteria>
- The audit records `claim_ready=false`.
- The audit records `artifact_count=74`, `existing_artifact_count=70`, `missing_artifact_count=4`, and `blocker_count=108`.
- The audit lists all 8 claim IDs from `CLAIM_GUARD.json`.
- The audit states that all four key mirror JSON files match the canonical files or records any mismatch explicitly.
</acceptance_criteria>
</task>

<task id="01-01-03" type="execute">
<title>Build the six-class blocker list and traceability matrix</title>
<read_first>
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-RESEARCH.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `.planning/codebase/CONCERNS.md`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
</read_first>
<action>
Write `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`. Include six
top-level sections named exactly `Provenance/readiness`,
`Empirical performance`, `Artifact packaging`, `Manuscript language`,
`Case-study`, and `Computational tractability`. Add a traceability matrix with
one row per `PACKAGE_INDEX.json` entry and one row per strict claim guard claim.
Each artifact row must include artifact ID, source family, package tier, status,
exists flag, blocker class, and short explanation. Each claim row must include
claim ID, support status, claim-ready flag, manuscript-allowed flag, blocker
class, and allowed use.
</action>
<verify>
- `M1_BLOCKER_LIST.md` exists.
- The file contains all six blocker class headings.
- The file contains `C1_central_adaptive_menu_superiority`.
- The file contains `C8_semi_real_case_validation`.
- The file contains `main_rc`.
- The file contains `phase9_tractability`.
</verify>
<acceptance_criteria>
- `M1_BLOCKER_LIST.md` has a readable six-class summary.
- `M1_BLOCKER_LIST.md` includes traceability for 74 artifact entries from `PACKAGE_INDEX.json`.
- `M1_BLOCKER_LIST.md` includes traceability for 8 strict claim guard claims.
- The blocker list does not claim any positive empirical result is authorized.
</acceptance_criteria>
</task>

<task id="01-01-04" type="execute">
<title>Inspect manuscript and paper boundary without editing source</title>
<read_first>
- `manuscript/main.tex`
- `manuscript/references.bib`
- `.planning/paper/CLAIM_SAFE_LANGUAGE.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`
- `.planning/paper/TR_E_RESEARCH_DESIGN.md`
</read_first>
<action>
Add a `Manuscript Claim-Language Boundary` section to
`M1_EVIDENCE_BOUNDARY_AUDIT.md`. Inspect `manuscript/main.tex` for claim-risk
phrases including `dominates`, `superior`, `outperform`, `improve`,
`near-optimal`, `adaptive window`, `adaptive menu`, `case-study validation`,
and `real passenger behavior`. Record line numbers and short context only. Do
not edit `manuscript/main.tex` or bibliography files.
</action>
<verify>
- `M1_EVIDENCE_BOUNDARY_AUDIT.md` contains `Manuscript Claim-Language Boundary`.
- `git diff --name-only -- manuscript/main.tex manuscript/references.bib` prints no paths caused by this task.
- The audit references `.planning/paper/CLAIM_SAFE_LANGUAGE.md`.
</verify>
<acceptance_criteria>
- Manuscript source remains unmodified.
- The audit records claim-language risks as review items, not as completed edits.
- The audit explicitly says manuscript rewriting is deferred to later phases.
</acceptance_criteria>
</task>

<task id="01-01-05" type="execute">
<title>Write the Phase 1 evidence-path decision</title>
<read_first>
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/research/SUMMARY.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-CONTEXT.md`
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-RESEARCH.md`
</read_first>
<action>
Write `.planning/milestones/tr_e_completion/M1_DECISION.md` with sections
named `Current Decision`, `Evidence Basis`, `Claim Ceiling`, `Feasibility
Assessment`, `Phase 2 Handoff`, `Phase 3 Handoff`, and `Forbidden Next Steps`.
State that the current generated package is not claim-ready and leans
diagnostic-only. Also state that Phase 1 does not decide final replay
legitimacy; Phase 2/3 must decide whether clean provenance and frozen final
settings can support a legitimate final replay without tuning on final outputs.
</action>
<verify>
- `M1_DECISION.md` exists.
- The file contains `not claim-ready`.
- The file contains `diagnostic`.
- The file contains `Phase 2`.
- The file contains `Phase 3`.
- The file contains `without tuning on final outputs`.
</verify>
<acceptance_criteria>
- `M1_DECISION.md` satisfies EVID-04.
- The decision does not authorize final replay, calibration, cleanup, artifact regeneration, or manuscript claim upgrades.
- The decision clearly routes provenance/readiness cleanup planning to Phase 2.
- The decision clearly routes final replay legitimacy versus diagnostic lock to Phase 3.
</acceptance_criteria>
</task>

<task id="01-01-06" type="verify">
<title>Run Phase 1 verification and evidence-boundary diff checks</title>
<read_first>
- `.planning/phases/01-repository-and-evidence-boundary-audit/01-VALIDATION.md`
- `.planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md`
- `.planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md`
- `.planning/milestones/tr_e_completion/M1_DECISION.md`
</read_first>
<action>
Run only the Phase 1 allowed checks:
`python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`
from repository root, file existence checks for the three milestone documents,
source assertions from `01-VALIDATION.md`, and a diff-name check for generated
evidence paths. Record verification results in the executor summary when this
plan is executed.
</action>
<verify>
- The import smoke prints `IMPORT_OK`.
- `M1_EVIDENCE_BOUNDARY_AUDIT.md`, `M1_BLOCKER_LIST.md`, and `M1_DECISION.md` exist.
- No generated evidence path under `work2_coding/outputs`, `work2_coding/artifacts`, or root `artifacts` was modified by this phase execution.
</verify>
<acceptance_criteria>
- The verification command exits 0.
- The three milestone deliverables exist.
- The executor summary records that no experiments, artifact builders, package builders, checkpoint training, final replay, calibration, or case-study execution were run.
</acceptance_criteria>
</task>
</tasks>

<verification>
Run these checks after executing the plan:

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
Test-Path .planning/milestones/tr_e_completion/M1_EVIDENCE_BOUNDARY_AUDIT.md
Test-Path .planning/milestones/tr_e_completion/M1_BLOCKER_LIST.md
Test-Path .planning/milestones/tr_e_completion/M1_DECISION.md
git diff --name-only -- work2_coding/outputs work2_coding/artifacts artifacts
```

Expected results:

- The Python smoke command prints `IMPORT_OK`.
- All three `Test-Path` commands print `True`.
- The generated-evidence diff check prints no paths caused by Phase 1 execution.
</verification>

<success_criteria>
- EVID-01: Current planning, codebase maps, artifacts, manuscript files, git
  status, and runtime root are inspected and recorded.
- EVID-02: Current `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`,
  `PACKAGE_INDEX.json`, and `ARTIFACT_TO_SECTION_MAP.json` status are recorded
  using generated files only.
- EVID-03: Current `claim_ready=false` causes are separated into
  provenance/readiness, empirical-performance, artifact-packaging,
  manuscript-language, case-study, and computational-tractability blockers.
- EVID-04: The phase states whether a claim-ready path is feasible or whether
  only diagnostic manuscript writing is feasible from current evidence.
- No experiments are run.
- No generated evidence is modified.
- No positive manuscript claim is upgraded.
</success_criteria>
