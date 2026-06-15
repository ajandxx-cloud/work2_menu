# Phase 7: Case Study Implementation - Context

**Gathered:** 2026-06-15T22:07:25+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 7 implements the approved semi-real case-study scaffolding only. Phase 6
approved a semi-real route with status `approved_blocked_pending_gate_cleanup`,
so this phase may create data contracts, offline directory scaffolding,
planning-side validation, source/license/hash fields, reproducibility scoring
frameworks, simulated-demand protocol placeholders, and planning-side manifest
drafts.

This phase must not download external OSM/GTFS/Yanjiao data, build road
graphs, build distance or duration matrices, generate simulated demand rows,
add executable case-study YAML to the runtime manifest directory, run policy
replay, generate case-study result artifacts, or upgrade manuscript claims.

All Phase 7 outputs should carry execution status
`scaffolding_only_blocked_execution`. Later data fetch, matrix construction,
case replay, result artifact generation, and manuscript claim upgrades require
a separate case-execution stage after upstream provenance, readiness, artifact,
and claim gates explicitly pass.

</domain>

<decisions>
## Implementation Decisions

### Data Source And Cache Boundary
- **D-01:** Use dual-route scaffolding for both public OSM/open-network and
  Yanjiao/Beijing routes. Phase 7 should give both routes data contracts rather
  than locking a single route prematurely.
- **D-02:** Every route contract should use a full reproducibility metadata
  package: `URL`, access date, license/access notes, raw cache path, hash,
  bbox/polygon, tool versions, parameters, and rebuild-command placeholders.
- **D-03:** If both routes can later be built, choose the default case-study
  main route by a predeclared score over reproducibility, license clarity,
  matrix rebuildability, DRT scenario plausibility, and paper value. Do not
  choose the main route based on experiment outcomes.
- **D-04:** Phase 7 must not fetch external sources, build road graphs, build
  distance matrices, or run policy replay. It should create contracts and
  offline scaffolding only.

### Ingestion And Validation Contract
- **D-05:** Validation is contract-level only. It should check metadata schema,
  required fields, directory structure, placeholder naming, hash field format,
  and rebuild-command field presence.
- **D-06:** Phase 7 validation must not validate real OSM/GTFS/OSRM content,
  matrix shape, reachable pairs, or real source availability, because Phase 7
  does not fetch or build those inputs.
- **D-07:** Put scaffolding under `.planning/data/case_studies/` so Phase 7
  remains planning-side and does not mix unfetched external-data contracts into
  runtime environment data.
- **D-08:** Write only a planning-side schema/contract validator under
  `.planning/data/case_studies/`. Do not add
  `work2_coding/scripts/validate_case_contract.py` in Phase 7.
- **D-09:** Validation findings should use `blocking`, `warning`, and `info`.
  A `blocking` issue prevents later case execution; a `warning` permits the
  contract to remain but must document limitations; `info` is explanatory.

### Simulated Demand And Manifest Scaffolding
- **D-10:** Simulated demand should be preregistered as a full protocol
  placeholder with required fields for seeds, OD/time pattern, volume/range,
  sampling rules, demand labels, and choice labels.
- **D-11:** Phase 7 must not generate demand rows or replay-ready demand files.
- **D-12:** Write a planning-side case manifest draft or contract under
  `.planning/data/case_studies/`. It should include the seven mainline tags,
  paired fields, and blocked execution status.
- **D-13:** Do not add disabled or placeholder runtime YAML under
  `work2_coding/Experiments/studies/` in Phase 7.
- **D-14:** Record a strict reduced-family gate template only. The template
  must explain which `policy_tag` is infeasible, whether the cause is a data or
  contract issue, whether the reduced family still answers the case-study
  question, and why no unfavorable baseline is being selectively removed.
  Phase 7 does not actually remove any tag.
- **D-15:** The planning-side manifest draft should inherit the core formal
  mainline paired fields from `formal_robust_menu.yaml`: seed, data seed, test
  data seed, instance/source route, `menu_k`, `max_candidates`,
  checkpoint path/status, uptake regime, choice parameters, HGS times, and
  related fairness fields.

### Evidence Gates And Paper Labels
- **D-16:** Every Phase 7 output should use status
  `scaffolding_only_blocked_execution`.
- **D-17:** Force `semi-real`, `simulated demand`, and `simulated choice`
  labels in every contract and future artifact placeholder, including source
  contracts, manifest draft, validation summary, future artifact metadata
  placeholders, and future manuscript language placeholders.
- **D-18:** Every contract, manifest, and validation summary should include
  machine-readable blocker fields:
  `case_execution_allowed: false`,
  `result_artifacts_allowed: false`, and
  `manuscript_claim_upgrade_allowed: false`.
- **D-19:** Each blocker field group must include unlock conditions tied to
  upstream provenance, readiness, artifact, and claim gate cleanup.
- **D-20:** Phase 7 may write prohibitive future manuscript language
  placeholders only, for example: "semi-real extension is scaffolded; no case
  evidence yet." It must not write usable manuscript claim-upgrade prose.

### The Agent's Discretion
- The planner may choose exact file names and schema syntax under
  `.planning/data/case_studies/`, as long as the decisions above are enforced.
- The planner may choose exact scoring weights for route selection, but the
  score must be based only on reproducibility, license clarity, matrix
  rebuildability, DRT scenario plausibility, and paper value, not results.
- The planner may choose whether the planning-side validator is implemented as
  a small script, documented schema checker, or both, provided it remains
  planning-side and does not read real external data.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, active runtime root, case-study
  requirement, no-fabricated-data boundary, and Phase 7 gate status.
- `.planning/REQUIREMENTS.md` - Case-study requirements `CASE-03` and
  `CASE-05`, plus prior `CASE-01`, `CASE-02`, and `CASE-04` decisions.
- `.planning/ROADMAP.md` - Phase 7 goal, success criteria, gate language, and
  restriction to scaffolding while upstream gates remain blocked.
- `.planning/STATE.md` - Current position, verification baseline, and notes
  that Phase 7 is limited to gated semi-real case scaffolding.
- `.planning/research/SUMMARY.md` - TR-E service-menu framing, optional
  external case rationale, and fallback path if evidence remains diagnostic.
- `AGENTS.md` - Repository instructions, active runtime assumption, research
  guardrails, and verification baseline.

### Case Study Decision Inputs
- `.planning/data/CASE_STUDY_FEASIBILITY.md` - Phase 6 feasibility decision,
  source audit, route ranking, minimum semi-real contract, preprocessing plan,
  and claim-language boundary.
- `.planning/phases/06-real-or-semi-real-case-study-feasibility-audit/06-CONTEXT.md`
  - Locked Phase 6 decisions including semi-real route, public/OSM plus
  Yanjiao dual-track audit, minimum contract, blocked execution gate, and
  mandatory labels.

### Runtime And Gate Context
- `work2_coding/Src/phase6_audit.py` - Supporting audit logic for runtime
  imports, manifest status, readiness blockers, artifact gates, and claim
  blockers. Use as gate context only.
- `work2_coding/scripts/audit_phase6_experiment_state.py` - CLI wrapper for
  Phase 6 supporting audit outputs.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Source for the
  seven mainline tags, formal paired fields, output schema, checkpoint
  requirements, and fairness contract to inherit in the planning-side case
  manifest draft.
- `work2_coding/Src/policy_adapters.py` - Mainline policy tag definitions and
  adapter metadata.
- `work2_coding/Src/paired_replay.py` - Paired replay contract and normalized
  row field semantics.
- `work2_coding/Src/study_execution.py` - Study execution status and metadata
  patterns to avoid prematurely invoking for the case study.
- `work2_coding/Src/artifact_status.py` - Artifact status and exclusion logic
  that motivates machine-readable blockers.
- `work2_coding/Src/manuscript_claims.py` - Claim guard logic and blocked
  claim-language patterns.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`: reference for
  the seven-tag family, paired fields, checkpoint status, and normalized-row
  schema. Phase 7 should borrow its contract vocabulary for the planning-side
  manifest draft, not create executable runtime YAML.
- `work2_coding/Src/phase6_audit.py` and
  `work2_coding/scripts/audit_phase6_experiment_state.py`: useful examples of
  machine-readable gate/blocker reporting and status fields. Phase 7 should
  mirror the clarity, but stay planning-side.
- `work2_coding/Src/artifact_status.py` and
  `work2_coding/Src/manuscript_claims.py`: existing gate/claim guard patterns
  that justify explicit `case_execution_allowed: false`,
  `result_artifacts_allowed: false`, and
  `manuscript_claim_upgrade_allowed: false` fields.

### Established Patterns
- Active runtime root is `work2_coding/`; old `.planning/codebase/` references
  to `ooh_code/` are stale historical memory.
- Experiments are manifest-driven and row-based, but Phase 7 must not add an
  executable runtime manifest or produce normalized rows.
- Paper-facing artifacts and manuscript language are gate-controlled and must
  not be hand-edited into stronger claims.
- Script-style tests exist under `work2_coding/scripts/test_*.py`, but Phase 7
  should keep the case validator in `.planning/data/case_studies/` rather than
  adding a runtime test wrapper.

### Integration Points
- `.planning/data/case_studies/` should become the Phase 7 contract root.
- A planning-side source contract should define both public OSM/open-network
  and Yanjiao/Beijing route metadata packages.
- A planning-side validation summary should report `blocking`, `warning`, and
  `info` findings without touching runtime outputs.
- A planning-side manifest draft should preserve seven mainline tags, formal
  paired-field inheritance, blocked execution status, simulated labels, and the
  reduced-family gate template.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four gray areas for discussion.
- The user chose dual-route scaffolding for public OSM/open-network and
  Yanjiao/Beijing.
- The user chose full reproducibility metadata for route contracts.
- The user chose route scoring based on reproducibility, license clarity,
  matrix rebuildability, DRT plausibility, and paper value, never results.
- The user explicitly selected "contract plus offline directories only": no
  external data download, no road graph, no distance matrix, no policy replay.
- The user chose `.planning/data/case_studies/` as the scaffolding root.
- The user chose planning-side validation only, with no runtime script under
  `work2_coding/scripts/`.
- The user chose `blocking / warning / info` validation severity.
- The user chose full simulated-demand protocol placeholders without demand
  rows.
- The user chose a planning-side manifest draft with seven tags, paired fields,
  and blocked execution status.
- The user chose a strict reduced-family gate template and no actual tag
  removal in Phase 7.
- The user chose inherited formal mainline paired fields.
- The user chose status `scaffolding_only_blocked_execution`.
- The user chose mandatory `semi-real / simulated demand / simulated choice`
  labels across contracts and future artifact placeholders.
- The user chose machine-readable blocker fields and prohibitive manuscript
  placeholders only.

</specifics>

<deferred>
## Deferred Ideas

- Enable external data download, road-graph or distance-matrix construction,
  and policy replay only in a later case-execution stage after upstream gates
  explicitly allow it.

</deferred>

---

*Phase: 7-Case Study Implementation*
*Context gathered: 2026-06-15T22:07:25+08:00*
