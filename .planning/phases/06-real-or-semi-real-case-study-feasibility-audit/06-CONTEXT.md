# Phase 6: Real Or Semi-Real Case Study Feasibility Audit - Context

**Gathered:** 2026-06-15T21:12:11.9183949+08:00
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
paper may describe the evidence. It must not run case experiments, tune RC
settings, fabricate real data, or describe simulated demand/choice behavior as
real passenger behavior.

Phase 7 is approved in principle only under the decision label
`approved_blocked_pending_gate_cleanup`. Before upstream gates are cleaned,
Phase 7 may prepare ingestion, validation, manifest scaffolding, and
reproducibility checks, but it must not execute formal/semi-real case
experiments, generate case result artifacts, or upgrade manuscript claims.

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
- **D-04:** Phase 6 should use the decision label
  `approved_blocked_pending_gate_cleanup`: the semi-real case route is approved
  in principle, but formal/semi-real case execution remains blocked until
  upstream gate cleanup.
- **D-05:** Do not automatically downgrade Phase 7 to diagnostic-only execution
  if gates remain blocked. Without gate cleanup, Phase 7 must not run case
  experiments or generate case result claims.
- **D-06:** Before gate cleanup, Phase 7 may implement ingestion design,
  validation scripts, manifest scaffolding, and reproducibility checks. It may
  not run formal/semi-real case experiments, generate case artifacts, or
  upgrade manuscript claims.

### Data Source Boundary
- **D-07:** Phase 6 should use a dual-track source audit: public OSM/open
  network sources and Yanjiao/Beijing commuting materials should both be
  considered.
- **D-08:** If both source routes are feasible, default the Phase 7 main route
  to public OSM/open network data because reproducibility outranks regional
  story value. Yanjiao/Beijing commuting materials remain useful as narrative
  support or an alternate candidate.
- **D-09:** Do not preset a city or region. Phase 6 should rank public-network
  candidates by reproducibility, licensing/access, distance-matrix
  rebuildability, DRT scenario plausibility, and paper value.
- **D-10:** Phase 6 must conduct external public-data/public-network web search
  and record source links, reproducibility paths, licensing or access
  constraints, and limitations in `CASE_STUDY_FEASIBILITY.md`.
- **D-11:** Only geography, road network, coordinates, and distance data may be
  described as real or semi-real foundations. Demand, choice behavior,
  acceptance, rejection, and opt-out behavior must be described as simulated
  unless actual audited passenger data is obtained in a future phase.
- **D-12:** Existing `Amazon_data` and `HombergerGehring_data` style sources
  may be used as public benchmarks or external scenarios, but they must not be
  packaged as a real-city DRT case study.

### Semi-Real Minimum Contract
- **D-13:** The minimum acceptable semi-real case requires documented real
  geography, a plausible depot/destination definition, candidate meeting
  points, real road-network distance or a reproducible distance matrix,
  simulated sequential demand, and explicit labels stating that choice behavior
  is simulated.
- **D-14:** The default comparison family remains the seven mainline tags. Phase
  6 should define a reduced-family gate rather than pre-approving arbitrary
  reduction. If Phase 7 finds a tag cannot run fairly, it must document which
  tag is infeasible, why the reason is a data/contract issue rather than an
  unfavorable result, whether the reduced family can still answer the
  case-study question, and why no unfavorable baseline is being selectively
  removed.
- **D-15:** Demand generation must be strongly pre-registered before case
  experiments:
  parameters, seeds, OD/time pattern, scale/range, and any sampling rules must
  be written before results are known. Demand must not be tuned based on case
  outcomes.
- **D-16:** Distance and road-network evidence should use a two-level standard:
  formal/semi-real case evidence requires real road-network distance or a
  reproducible distance matrix. If using an API, OSM extraction, or local
  routing tool, record source, version/date, parameters, cache or matrix hash,
  and rebuild instructions. Euclidean distance is allowed only as a diagnostic
  fallback, not as strong case-study evidence.
- **D-17:** Meeting-point candidates should use a mixed rule: prioritize public,
  explainable points such as POIs, transit stops, community entrances, parking
  areas, or pickup points. If those are insufficient, Phase 7 may add
  pre-registered grid/cluster synthetic candidates and must label them as
  synthetic candidate meeting points.

### Implementation And Gate Use
- **D-18:** Existing `work2_coding/Src/phase6_audit.py` should be used as
  supporting experiment-state evidence for runtime imports, manifests,
  readiness, artifact gates, and claim blockers. It is not the primary Phase 6
  case-feasibility report.
- **D-19:** Phase 6 should not implement new case-study ingestion, validation,
  manifests, or run code. Those belong to Phase 7 if Phase 6 approves the
  case-study route.
- **D-20:** If upstream readiness/artifact gates remain blocked, Phase 6 may
  approve a semi-real case only with status
  `approved_blocked_pending_gate_cleanup`. Phase 7 case execution then waits
  for cleanup; diagnostic-only execution is not allowed as an automatic
  fallback.
- **D-21:** Organize outputs as one primary planning report plus optional
  supporting audit evidence: `.planning/data/CASE_STUDY_FEASIBILITY.md` is the
  main decision file, while `work2_coding/outputs/phase6_audit/PHASE6_AUDIT.md`
  and `.json` may be cited as runtime/gate evidence if generated.

### Paper Narrative Boundary
- **D-22:** The semi-real case should be positioned as supplemental
  robustness/external scenario evidence. RC formal evidence remains the main
  empirical ladder.
- **D-23:** If semi-real case results conflict with RC formal evidence, report
  the conflict honestly as a boundary condition in the Discussion rather than
  hiding it or forcing a stronger claim.
- **D-24:** Semi-real case evidence may support limited external-validity
  language such as evaluation on a real road network or real geography. It may
  not support claims about real passenger behavior, real acceptance/opt-out
  rates, or real operating profit.
- **D-25:** All case-study tables, figures, artifact metadata, and manuscript
  text must clearly label `semi-real`, `simulated demand`, and `simulated
  choice` status so readers cannot mistake the case for real passenger
  validation.

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
- The planner may choose the exact web-search terms and candidate-source table,
  but the final ranking must make reproducibility and evidence limits explicit.

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
- The second discussion round selected all four new gray areas: case-study
  decision strength, data-source priority, minimum acceptable semi-real case,
  and paper narrative boundary.
- The case-study decision label is locked as
  `approved_blocked_pending_gate_cleanup`.
- Phase 7 may build ingestion/validation scaffolding before gate cleanup, but
  may not run case experiments or generate case claims.
- Data-source audit is dual-track, with public OSM/open network as the default
  Phase 7 route if both public-network and Yanjiao/Beijing routes are feasible.
- Phase 6 must use web search and record public source links for the data-source
  audit.
- The semi-real case uses strong demand pre-registration, a reduced-family gate
  if seven tags cannot run fairly, a two-level distance standard, and mixed
  meeting-point candidate rules.
- The semi-real case is supplemental robustness/external scenario evidence and
  must carry explicit `semi-real / simulated demand / simulated choice` labels.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within Phase 6 scope.

</deferred>

---

*Phase: 6-Real Or Semi-Real Case Study Feasibility Audit*
*Context gathered: 2026-06-15T21:12:11.9183949+08:00*
