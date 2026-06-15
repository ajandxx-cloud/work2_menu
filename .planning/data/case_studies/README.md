# Phase 7 Case-Study Scaffold

status: scaffolding_only_blocked_execution
case_execution_allowed: false
result_artifacts_allowed: false
manuscript_claim_upgrade_allowed: false

This directory is the planning-side contract root for the Phase 7 semi-real
case-study extension. It records reproducibility contracts, validation rules,
and future unlock conditions only.

Phase 7 creates contracts only: no data download, no road graph build, no
distance or duration matrix build, no simulated demand rows, no runtime
manifest, no policy replay, no normalized case rows, no case-study result
artifacts, and no manuscript claim upgrade.

## File Map

| File | Purpose | Execution status |
| --- | --- | --- |
| `source_contracts.yaml` | Dual-route source and cache metadata contracts for public OSM/open-network and Yanjiao/Beijing motivated routes. | scaffolding_only_blocked_execution |
| `route_selection_scorecard.yaml` | Predeclared route-selection criteria independent of case experiment outcomes. | scaffolding_only_blocked_execution |
| `simulated_demand_protocol.md` | Placeholder protocol for simulated demand and simulated choice design. | scaffolding_only_blocked_execution |
| `case_manifest_draft.yaml` | Planning-side, non-executable manifest draft that preserves formal paired-field vocabulary. | scaffolding_only_blocked_execution |
| `reduced_family_gate.md` | Future gate template for any policy-family reduction. No tag is removed in Phase 7. | scaffolding_only_blocked_execution |
| `claim_boundary_placeholders.md` | Prohibitive placeholder language only; it is not claim-upgrade prose. | scaffolding_only_blocked_execution |

## Boundary

The scaffold labels all future case material as semi-real geography/network
with simulated demand and simulated choice. It does not claim real passenger
behavior, real acceptance, real opt-out, or real operating profit.

Future case execution can begin only after upstream provenance, formal
readiness, artifact-status, and claim-guard gates explicitly pass and a later
phase creates executable runtime files.
