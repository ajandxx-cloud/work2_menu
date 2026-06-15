# Phase 6: Real Or Semi-Real Case Study Feasibility Audit - Context

**Gathered:** 2026-06-15T20:45:31+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 6 decides whether the TR-E paper should add a real or semi-real case
study, and writes the feasibility contract for that decision. The primary
deliverable is `.planning/data/CASE_STUDY_FEASIBILITY.md`, supported by any
runtime/gate audit evidence needed from `work2_coding/outputs/phase6_audit/`.

This phase is a feasibility and decision phase. It should audit data/source
options, define the minimum acceptable semi-real case, decide whether Phase 7
is approved, blocked pending gate cleanup, or deferred, and record how the
paper may describe the evidence. It must not implement new case-study
ingestion or run code, run case experiments, tune RC settings, fabricate real
data, or describe simulated demand/choice behavior as real passenger behavior.

</domain>

<decisions>
## Implementation Decisions

### Case Study Route
- **D-01:** Phase 6 should default to a semi-real case study route, not a full
  real passenger-behavior case. The case may use real or documented geography
  and a reproducible distance matrix, but sequential demand and passenger
  choices remain simulated and must be labeled as such.
- **D-02:** Yanjiao/commuting materials are useful if available, but the case
  study is not hard-bound to Yanjiao. If those materials are insufficient, the
  feasibility report may approve a general auditable semi-real case instead.
- **D-03:** The semi-real case is an external feasibility/robustness supplement
  for the paper. It must not be framed as real passenger choice validation and
  should not override the RC formal evidence ladder.
- **D-04:** Phase 7 execution must wait for upstream provenance/readiness/
  artifact gates to be cleaned, or the project must explicitly downgrade the
  downstream case run to diagnostic use before running it.

### Data Source Boundary
- **D-05:** Phase 6 should prioritize public networks and public benchmark
  sources for reproducibility and feasibility. Yanjiao/commuting materials are
  a plus, not a hard dependency.
- **D-06:** Only geography, road network, coordinates, and distance data may be
  described as real or semi-real foundations. Demand, choice behavior,
  acceptance, rejection, and opt-out behavior must be described as simulated
  unless actual audited passenger data is obtained in a future phase.
- **D-07:** Existing `Amazon_data` and `HombergerGehring_data` style sources
  may be used as public benchmarks or external scenarios, but they must not be
  packaged as a real-city DRT case study.
- **D-08:** Phase 6 planning must include an external public-data/public-network
  search and record candidate sources, reproducibility path, licensing or
  access constraints, and limitations in `CASE_STUDY_FEASIBILITY.md`.

### Semi-Real Minimum Contract
- **D-09:** The minimum acceptable semi-real case requires documented real
  geography, a plausible depot/destination definition, candidate meeting
  points, real road-network distance or a reproducible distance matrix,
  simulated sequential demand, and explicit labels stating that choice behavior
  is simulated.
- **D-10:** The default comparison family remains the seven mainline tags. If
  the case runtime or data contract cannot support the full family, Phase 7 may
  use a predefined six-tag reduced family, but the reduction must be justified
  before execution and must not selectively remove unfavorable baselines.
- **D-11:** Demand generation must be pre-registered before case experiments:
  parameters, seeds, OD/time pattern, scale/range, and any sampling rules must
  be written before results are known. Demand must not be tuned based on case
  outcomes.
- **D-12:** Distance and road-network evidence should prioritize
  reproducibility. If using an API, OSM extraction, or local routing tool,
  record source, version/date, parameters, cache or matrix hash, and rebuild
  instructions. Euclidean distance is allowed only as a diagnostic fallback,
  not as strong case-study evidence.

### Implementation And Gate Use
- **D-13:** Existing `work2_coding/Src/phase6_audit.py` should be used as
  supporting experiment-state evidence for runtime imports, manifests,
  readiness, artifact gates, and claim blockers. It is not the primary Phase 6
  case-feasibility report.
- **D-14:** Phase 6 should not implement new case-study ingestion, validation,
  manifests, or run code. Those belong to Phase 7 if Phase 6 approves the
  case-study route.
- **D-15:** If upstream readiness/artifact gates remain blocked, Phase 6 may
  approve a semi-real case only with status `blocked_pending_gate_cleanup`.
  Phase 7 execution then waits for cleanup, unless the project explicitly
  chooses a diagnostic-only downgrade.
- **D-16:** Organize outputs as one primary planning report plus optional
  supporting audit evidence: `.planning/data/CASE_STUDY_FEASIBILITY.md` is the
  main decision file, while `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md`
  and `.json` may be cited as runtime/gate evidence if generated.

### The Agent's Discretion
- The planner may choose the exact structure of `CASE_STUDY_FEASIBILITY.md`,
  provided it includes source audit, decision, preprocessing plan, required
  code changes for Phase 7, paper value, gate status, and the minimum semi-real
  contract above.
- The planner may choose the exact external-data search terms and source list,
  but must distinguish public benchmark data, public network/geography data,
  real operational/passenger data, and simulated demand.
- The planner may decide whether to run the existing Phase 6 audit script as
  part of planning, but if it is used, it remains supporting evidence and must
  not replace the case-study feasibility report.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, runtime root, active case-study
  requirement, no-fabricated-data boundary, and conditional Phase 7 rule.
- `.planning/REQUIREMENTS.md` - Case-study requirements `CASE-01`,
  `CASE-02`, `CASE-04`, plus downstream `CASE-03` and `CASE-05`.
- `.planning/ROADMAP.md` - Phase 6 goal, success criteria, additional gate
  rule for Phase 7, and minimum acceptable semi-real case language.
- `.planning/STATE.md` - Current GSD state, Phase 6 position, gate notes, and
  verification baseline.
- `.planning/research/SUMMARY.md` - TR-E framing, optional external case
  rationale, and fallback path if evidence remains diagnostic.
- `AGENTS.md` - Repository instructions, active runtime assumption, research
  guardrails, and verification baseline.

### Prior Phase Context And Paper Contract
- `.planning/phases/02-paper-level-research-design-lock/02-CONTEXT.md` -
  Optional case-study gate, no-filter/case boundary, and V1 claim framing.
- `.planning/phases/03-formal-rc-evidence-pipeline-repair-and-completion/03-CONTEXT.md`
  - Formal evidence gate boundaries, dirty-git handling, checkpoint
  provenance, and diagnostic artifact rules.
- `.planning/phases/04-rc-result-diagnosis-and-paper-claim-validation/04-CONTEXT.md`
  - Provisional/blocked claim status, result diagnosis, and warning against
  mechanical downstream expansion.
- `.planning/phases/05-calibration-and-robustness-without-p-hacking/05-CONTEXT.md`
  - Gate-first process lock, no-p-hacking calibration boundary, and
  `blocked_pending_gate_cleanup` final-rerun status.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - Paper research design,
  claim-to-evidence map, case-study optionality, and non-claim boundaries.

### Runtime And Existing Audit Scaffold
- `work2_coding/Src/phase6_audit.py` - Existing support audit for runtime
  imports, manifests, readiness, artifact gates, claim blockers, and RC
  dataset state. Use as supporting evidence only.
- `work2_coding/scripts/audit_phase6_experiment_state.py` - CLI wrapper for
  writing `PHASE6_AUDIT.md` and `PHASE6_AUDIT.json`.
- `work2_coding/scripts/test_phase6_audit.py` - Tests for current Phase 6 audit
  scaffold, including RC dataset surface, readiness blocker preservation, and
  gate handoff fields.
- `work2_coding/Environments/OOH/Amazon_data/README.md` - Public benchmark data
  context; do not frame as real DRT passenger behavior.
- `work2_coding/Environments/OOH/HombergerGehring_data/README.md` - RC/C/R
  benchmark data context and distance-data assumptions.

### Gate And Evidence Inputs
- `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
  - Current readiness/provenance gate status and checkpoint metadata.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Existing
  seven-tag formal comparison reference and paired replay surface.
- `work2_coding/Src/policy_adapters.py` - Mainline policy tag definitions and
  adapter metadata.
- `work2_coding/Src/paired_replay.py` - Paired replay contract and normalized
  row fields.
- `work2_coding/Src/study_execution.py` - Study execution status and metadata
  contract.
- `work2_coding/Src/artifact_status.py` - Artifact status and exclusion logic.
- `work2_coding/Src/manuscript_claims.py` - Claim guard logic, including
  blocked real passenger validation language.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/phase6_audit.py`: can generate a support audit for runtime
  import status, canonical file hashes, manifest summaries, RC data availability,
  readiness blockers, artifact gates, and claim status.
- `work2_coding/scripts/audit_phase6_experiment_state.py`: existing command
  wrapper for support audit generation under `work2_coding/outputs/phase6_audit/`.
- `work2_coding/scripts/test_phase6_audit.py`: validates that the support audit
  preserves current dirty-git/readiness blockers, loaded checkpoint status, RC
  split surface, and gate handoff fields.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`: reference for the
  default seven-tag comparison family and paired split structure that Phase 7
  should preserve where feasible.
- `work2_coding/Environments/OOH/Amazon_data/` and
  `work2_coding/Environments/OOH/HombergerGehring_data/`: existing public
  benchmark data roots that can inform fallback external-scenario analysis but
  must not be mislabeled as a real-city DRT case.

### Established Patterns
- Active runtime root is `work2_coding/`; stale `ooh_code/` references in old
  codebase maps remain historical.
- Experiments are manifest-driven; paper-facing evidence should flow through
  normalized rows, artifact gates, and claim guards rather than ad hoc result
  editing.
- Claim language is gated by readiness JSON, completed comparable rows,
  artifact status, and claim guard.
- Generated rows, tables, figures, and manuscript artifacts must not be
  hand-edited.
- Tests are script-style Python checks under `work2_coding/scripts/test_*.py`.

### Integration Points
- `.planning/data/CASE_STUDY_FEASIBILITY.md` should become the Phase 6 primary
  report and record data-source audit, decision, preprocessing plan, required
  code changes, paper value, gate status, and minimum semi-real contract.
- If generated, `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md` and
  `PHASE6_AUDIT.json` should be cited only as runtime/gate support evidence.
- Phase 7, if approved, should implement ingestion/validation/run contracts
  after gate cleanup or diagnostic downgrade, not during Phase 6.

</code_context>

<specifics>
## Specific Ideas

- The user chose to discuss all four gray areas in Chinese.
- The user selected option `1` for all route questions except data-source
  ordering, where the user selected public networks/public benchmarks first.
- The locked route is semi-real case study, not real passenger validation.
- The locked data posture is reproducibility first: public network/public
  benchmark audit first, Yanjiao/commuting materials as optional added value.
- The locked report structure is one primary feasibility report plus optional
  supporting audit evidence.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within Phase 6 scope.

</deferred>

---

*Phase: 6-Real Or Semi-Real Case Study Feasibility Audit*
*Context gathered: 2026-06-15T20:45:31+08:00*
