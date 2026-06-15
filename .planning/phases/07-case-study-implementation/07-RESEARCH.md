---
phase: 07-case-study-implementation
status: complete
researched: 2026-06-15T22:17:18+08:00
timezone: Asia/Shanghai
research_mode: inline
requirements:
  - CASE-03
  - CASE-05
---

# Phase 7 Research: Gated Semi-Real Case Study Scaffolding

## Research Question

What does Phase 7 need to implement so the Work2 semi-real case study becomes
reproducible and auditable, without downloading external data, running case
experiments, generating case-study result artifacts, or upgrading manuscript
claims while upstream provenance/readiness/artifact/claim gates remain blocked?

## Short Answer

Phase 7 should produce a planning-side case-study contract pack under
`.planning/data/case_studies/`, plus a planning-side validator and validation
summary. It should not write executable runtime manifests under
`work2_coding/Experiments/studies/`, should not build source caches or
distance matrices, and should not emit normalized case-study rows.

The executable implementation should be split into:

1. A contract artifact plan that defines dual-route source metadata, simulated
   demand placeholders, a planning-side manifest draft, a reduced-family gate,
   and prohibitive manuscript placeholders.
2. A validator/closeout plan that checks those contracts, records validation
   findings, and updates planning state only after blockers and labels remain
   explicit.

## Gate Interpretation

Phase 6 approved a semi-real case route with status
`approved_blocked_pending_gate_cleanup`. This is not approval to execute the
case study. The Phase 7 execution status for planning artifacts should remain
`scaffolding_only_blocked_execution`.

Machine-readable blockers should appear in every generated contract and
summary:

- `case_execution_allowed: false`
- `result_artifacts_allowed: false`
- `manuscript_claim_upgrade_allowed: false`

Each blocker group should include unlock conditions tied to upstream provenance,
formal readiness, artifact status, and claim guard cleanup.

## Codebase Findings

### Active Runtime Root

The active runtime root is `work2_coding/`, not the stale `ooh_code/` paths in
older codebase maps. Phase 7 plans should cite current `work2_coding/` files
only when inheriting contracts.

### Mainline Family And Paired Fields

`work2_coding/Experiments/studies/formal_robust_menu.yaml` is the source of
truth for the V1 seven-tag family:

- `mainline_no_menu`
- `mainline_fixed_menu`
- `mainline_random_menu`
- `mainline_optimized_m`
- `mainline_optimized_mw`
- `mainline_optimized_fixed_window`
- `mainline_optimized_adaptive`

The planning-side case manifest draft should inherit the formal paired fields
needed for fair replay: seed, data seed, test data seed, instance/source route,
pricing, HGS times, checkpoint path/status, `menu_k`, `max_candidates`,
`max_steps_r`, `max_steps_p`, and uptake-regime/choice parameters. It should
also record that the case manifest is not executable yet.

### Normalized Row Status Boundary

`work2_coding/Src/paired_replay.py` accepts only these execution statuses for
normalized rows: `completed`, `contract_only`, `diagnostic`, `incomplete`,
`blocked`, and `failed`. Therefore Phase 7 must not try to create normalized
rows with the custom status `scaffolding_only_blocked_execution`. That custom
status belongs in planning-side contracts and validation summaries, not in
runtime row outputs.

If a later case-execution phase emits rows before full claim readiness, it
should map to existing row statuses such as `contract_only`, `blocked`, or
`diagnostic`, with explicit labels and artifact guards.

### Artifact And Claim Gates

`work2_coding/Src/artifact_status.py` excludes placeholder-only, blocked,
failed, incomplete, contract-only, diagnostic, no-filter-only, bad checkpoint,
and invalid accounting rows from claim-ready artifact use. This supports the
Phase 7 design: keep the scaffold as contracts, not evidence.

`work2_coding/Src/manuscript_claims.py` always blocks real-passenger validation
and universal-dominance claims. Phase 7 manuscript placeholders must therefore
be prohibitive only, for example: "semi-real extension scaffolded; no case
evidence yet."

### Phase 6 Audit Pattern

`work2_coding/Src/phase6_audit.py` and
`work2_coding/scripts/audit_phase6_experiment_state.py` show useful patterns
for machine-readable blockers with `reason`, `minimal_fix`, `rerun_command`,
and `evidence_location`. Phase 7 should mirror that clarity in planning-side
validation findings without importing runtime execution paths.

## Recommended Contract Pack

Create `.planning/data/case_studies/` with these planning-side artifacts:

| Artifact | Purpose | Notes |
| --- | --- | --- |
| `README.md` | Human-readable boundary and file map | Must state no data download, no runtime manifest, no replay. |
| `source_contracts.yaml` | Dual-route OSM/open-network and Yanjiao/Beijing metadata contracts | Required fields: URL, access date, license/access notes, raw cache path placeholder, hash placeholder, bbox/polygon, tool versions, parameters, rebuild commands. |
| `route_selection_scorecard.yaml` | Predeclared route-selection criteria and weights | Criteria: reproducibility, license clarity, matrix rebuildability, DRT plausibility, paper value. Never use outcomes. |
| `simulated_demand_protocol.md` | Demand/choice protocol placeholder | Required fields for seeds, OD/time pattern, volume/range, sampling rules, demand labels, and choice labels. No generated rows. |
| `case_manifest_draft.yaml` | Planning-side study manifest draft | Include seven tags, paired-field inheritance, blocked execution status, and source-route placeholders. Do not place it under `work2_coding/Experiments/studies/`. |
| `reduced_family_gate.md` | Strict template for any later tag reduction | Must prove removal is caused by data/contract infeasibility, not unfavorable outcomes. |
| `claim_boundary_placeholders.md` | Prohibitive future manuscript language only | Must label semi-real geography/network, simulated demand, and simulated choice. |
| `validate_case_contracts.py` | Planning-side validator | Validates metadata schema, labels, blockers, required fields, placeholder naming, and absence of runtime execution artifacts. |
| `VALIDATION_SUMMARY.md` | Validator output | Reports `blocking`, `warning`, and `info` findings. |

## Validation Architecture

The validator should be planning-side and lightweight:

- Run from repository root:
  `python .planning/data/case_studies/validate_case_contracts.py --root .planning/data/case_studies --write-summary`
- Optional self-test:
  `python .planning/data/case_studies/test_case_contracts.py`
- Baseline runtime smoke from `work2_coding/`:
  `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`

Contract checks should include:

- all required planning-side files exist;
- dual routes are present;
- every route has source URL, access date placeholder, license/access notes,
  raw cache path placeholder, hash placeholder, bbox/polygon placeholder, tool
  versions, parameters, and rebuild-command placeholder;
- every contract contains `semi-real`, `simulated demand`, and `simulated
  choice` labels where relevant;
- blocker fields are present and set to false;
- unlock conditions mention provenance, readiness, artifact, and claim gates;
- the planning-side manifest draft includes all seven mainline policy tags;
- paired fields are inherited from `formal_robust_menu.yaml` vocabulary;
- no files are created under `work2_coding/Experiments/studies/`;
- no normalized rows, result tables, figures, or manuscript claim-upgrade prose
  are generated.

## Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Planning scaffold is mistaken for evidence | Use blockers in every contract and a validation summary with `case_execution_allowed: false`. |
| Custom scaffold status leaks into normalized rows | Keep `scaffolding_only_blocked_execution` outside runtime rows; later rows must use accepted row statuses. |
| Reduced policy family becomes outcome selection | Require the reduced-family gate before any tag removal and forbid result-based removal. |
| Yanjiao narrative overclaims real behavior | Label Yanjiao/Beijing as motivation unless reproducible network/matrix evidence is later pinned. |
| Validator accidentally validates external data | Restrict it to schema, metadata, placeholder, and label checks only. |

## Planning Implications

Phase 7 should close `CASE-03` by creating a reproducible ingestion,
validation, smoke/pilot/formal-or-diagnostic execution contract, not by running
the case. It should address `CASE-05` by recording that Phase 6 did not defer
the case study, so Phase 7 is not skipped, while execution and claim upgrades
remain blocked.

## Research Complete
