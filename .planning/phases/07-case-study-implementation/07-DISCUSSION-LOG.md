# Phase 7: Case Study Implementation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-15T22:07:25+08:00
**Phase:** 7-Case Study Implementation
**Areas discussed:** Data source and cache boundary, Ingestion and validation contract, Simulated demand and manifest scaffolding, Evidence gates and paper labels

---

## Data Source And Cache Boundary

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| How should Phase 7 lock the primary data-source route? | Public OSM first; Dual routes in parallel; Yanjiao first | Dual routes in parallel |
| What metadata/cache granularity should be required? | Full reproducibility package; Lightweight metadata; Tiered by source | Full reproducibility package |
| If both routes can be built, how should the default main route be selected? | Select main route by reproducibility score; Public OSM always main; Yanjiao main if available | Select main route by reproducibility score |
| Should Phase 7 fetch external sources or only create offline contracts? | Contract plus offline directories only; Allow raw-source caching; Allow matrix cache construction | Contract plus offline directories only |

**Notes:** The user clarified that Phase 7 only creates data contracts and
scaffolding for both routes. It must not download external data, generate a
road graph or distance matrix, or run policy replay. Route selection is based
on reproducibility, license clarity, matrix rebuildability, DRT scenario
plausibility, and paper value, never result quality.

---

## Ingestion And Validation Contract

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| What layer should Phase 7 validation verify? | Contract-level validation; Contract plus offline fixture validation; Near-execution validation | Contract-level validation |
| Where should the scaffolding directory live? | `work2_coding/Experiments/case_studies/`; `work2_coding/Environments/OOH/case_studies/`; `.planning/data/case_studies/` | `.planning/data/case_studies/` |
| Should Phase 7 add a runtime validation script or only a planning-side validator? | Planning-side validator only; Add `work2_coding/scripts/validate_case_contract.py`; Both planning-side validator and runtime wrapper | Planning-side validator only |
| How should validation failures be classified? | blocking / warning / info; pass / fail; gate-specific codes | blocking / warning / info |

**Notes:** The user chose planning-side validation only. The validator should
validate contract files, not real external data, matrices, or runtime studies.

---

## Simulated Demand And Manifest Scaffolding

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| How far should Phase 7 preregister simulated demand? | Full protocol placeholder; Protocol plus small fake fixture; Generate replay-ready demand template | Full protocol placeholder |
| What form should the case manifest take in Phase 7? | Planning-side manifest draft; Runtime YAML placeholder; Prose only | Planning-side manifest draft |
| How should the reduced-family gate be designed? | Strict gate document; Predefine removable tag list; Never allow reduced family | Strict gate document |
| Which paired replay fairness fields should be locked in the planning-side manifest draft? | Inherit formal mainline paired fields; Lock only case-specific fields; Let the planner decide all fields | Inherit formal mainline paired fields |

**Notes:** The user chose full protocol placeholders without generating demand
rows, a planning-side manifest draft under `.planning/data/case_studies/`, a
strict reduced-family gate template, and inheritance from
`formal_robust_menu.yaml` paired fields.

---

## Evidence Gates And Paper Labels

| Question | Options Considered | User's Choice |
| --- | --- | --- |
| What execution status should all Phase 7 outputs carry? | `scaffolding_only_blocked_execution`; `diagnostic_contract_only`; `ready_for_case_execution` | `scaffolding_only_blocked_execution` |
| Where should `semi-real / simulated demand / simulated choice` labels appear? | All contracts and future artifact fields; Only manifest draft and validation summary; Only prose documentation | All contracts and future artifact fields |
| How should Phase 7 prevent its artifacts from being misused as case results? | Machine-readable blocker fields; Top-of-document warning; Directory isolation only | Machine-readable blocker fields |
| Should Phase 7 update manuscript-related placeholder text? | Prohibitive placeholders only; Do not touch manuscript placeholders; Write usable manuscript draft | Prohibitive placeholders only |

**Notes:** The user chose explicit machine-readable blockers:
`case_execution_allowed: false`, `result_artifacts_allowed: false`, and
`manuscript_claim_upgrade_allowed: false`, with unlock conditions tied to
upstream gate cleanup.

---

## The Agent's Discretion

- Choose exact planning-side file names and schema syntax under
  `.planning/data/case_studies/`.
- Choose route scoring weights, provided they use only the approved
  reproducibility and paper-value criteria.
- Choose the planning-side validator format, provided it remains outside the
  runtime and avoids real source or matrix validation.

## Deferred Ideas

- Enable external data download, road-graph or distance-matrix construction,
  and policy replay only in a later case-execution stage after upstream gates
  explicitly allow it.
