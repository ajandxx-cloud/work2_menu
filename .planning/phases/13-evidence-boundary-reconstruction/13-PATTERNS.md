---
phase: 13
phase_name: evidence-boundary-reconstruction
status: complete
created: 2026-06-16T15:58:08+08:00
timezone: Asia/Shanghai
---

# Phase 13 Pattern Map

## Pattern Mapping Complete

Phase 13 is a planning-document phase. The closest existing analogs are prior
phase plans and result summaries, not runtime modules.

## Files To Create

| Target | Role | Closest analogs |
| --- | --- | --- |
| `.planning/milestones/claim_ready_resolution/01_EVIDENCE_BOUNDARY.md` | Timeline narrative and source-boundary audit | `.planning/results/PHASE3_FORMAL_EVIDENCE_HANDOFF.md`, `.planning/results/RC_FORMAL_DIAGNOSIS.md`, `.planning/phases/10-paper-artifact-generation/10-VERIFICATION.md` |
| `.planning/milestones/claim_ready_resolution/01_CLAIM_READY_FALSE_CAUSES.md` | Audit table of canonical `claim_ready=false` causes | `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`, `.planning/paper/CLAIM_SAFE_LANGUAGE.md` |
| `.planning/milestones/claim_ready_resolution/01_BLOCKER_TAXONOMY.md` | Taxonomy table using the roadmap's nine blocker classes | `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md`, `.planning/results/SENSITIVITY_SUMMARY.md`, `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` |

## Established Documentation Patterns

- Use YAML frontmatter for phase, status, generated timestamp, timezone, and
  source paths when the file is a phase deliverable.
- Use tables for audit rows and concise narrative for interpretation.
- Put blockers before positive interpretation.
- Preserve generated artifact paths exactly and treat them as source references.
- Use explicit status strings such as `claim_ready: false`,
  `diagnostic_provisional_blocked`, `blocked`, and
  `scaffold_only_no_result_evidence`.
- Keep "allowed", "blocked", and "diagnostic" manuscript language separated.

## Required Cross-Index Pattern

Use stable ids:

- `EB-001`, `EB-002`, ... for evidence-boundary facts and conflicts.
- `CF-001`, `CF-002`, ... for canonical `claim_ready=false` causes.
- `BT-001`, `BT-002`, ... for blocker taxonomy rows.

Each deliverable should reference the other id families:

- `01_EVIDENCE_BOUNDARY.md` should point timeline facts to `CF-*` and `BT-*`
  rows where the fact causes a blocker.
- `01_CLAIM_READY_FALSE_CAUSES.md` should point each canonical cause to source
  `EB-*` facts and one or more `BT-*` taxonomy rows.
- `01_BLOCKER_TAXONOMY.md` should list covered `CF-*` causes and evidence
  facts for each taxonomy row.

## Source Parsing Pattern

Executors may use PowerShell `ConvertFrom-Json` or a small read-only helper to
summarize JSON. Any helper must:

- read generated artifacts only;
- write only planning deliverables under
  `.planning/milestones/claim_ready_resolution/`;
- never update `work2_coding/outputs/`, `work2_coding/artifacts/`, root
  `artifacts/`, `paper/`, or `manuscript/`.

## Verification Pattern

Use script-style checks and `Select-String`/JSON parsing rather than subjective
review only. The minimum verification surface is:

- required files exist;
- required ids and claim ids are present;
- all nine taxonomy classes are present;
- generated artifact roots are not modified;
- import smoke still passes.

