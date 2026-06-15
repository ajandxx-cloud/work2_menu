# Phase 8: Sensitivity And Robustness Experiments - Context

**Gathered:** 2026-06-15T23:13:09+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 8 adds diagnostic sensitivity and robustness experiments for the TR-E
service-menu paper. The phase should produce controlled, one-factor-at-a-time
sensitivity evidence around the current frozen/default robust-menu settings,
plus a planning-side summary that identifies where optimized service menus work
and where they fail.

This phase is not a gate-cleanup phase, not a final rerun phase, not a
semi-real case execution phase, and not a manuscript-claim upgrade phase. While
upstream provenance, readiness, artifact, and claim gates remain unresolved,
Phase 8 actual replay is allowed only as diagnostic/provisional pilot evidence
with `claim_ready=false`.

</domain>

<decisions>
## Implementation Decisions

### Sensitivity Matrix Scope
- **D-01:** Run actual replay only for the four must-have Phase 8 dimensions:
  `menu_k`, ETA/filter mode, uptake regime, and opt-out/service guardrail.
- **D-02:** Treat nice-to-have dimensions as deferred/contract notes only:
  candidate pool size (`max_candidates`), fleet/capacity stress, and pricing
  bounds or price sensitivity. Do not generate executable runtime manifests for
  those nice-to-have dimensions in Phase 8.
- **D-03:** Use one-factor-at-a-time sensitivity around the current
  frozen/default settings instead of a crossed matrix. Each sensitivity axis
  should vary one mechanism while preserving paired replay fairness.
- **D-04:** The `menu_k` axis should run values `2`, `3`, and `4`. Value `3`
  remains the center/default setting.

### Run And Gate Strategy
- **D-05:** Keep `phase8_baseline_validation` as a prerequisite gate, not as
  part of the sensitivity suite. Baseline validation and sensitivity evidence
  should remain separate.
- **D-06:** If `phase8_baseline_validation` fails, Phase 8 sensitivity should
  write a blocked report and must not start actual sensitivity replay.
- **D-07:** Phase 8 sensitivity actual replay may run while current gates are
  unresolved, but all outputs must be classified as diagnostic/provisional and
  must keep `claim_ready=false`.
- **D-08:** Use diagnostic/pilot tier for Phase 8 sensitivity. Do not use
  formal tier for this phase while upstream gates remain unresolved.

### Robustness Knob Semantics
- **D-09:** The ETA/filter sensitivity axis should run `hard`,
  `interval_overlap`, and `chance_constraint`. The no-filter mode (`none`)
  is diagnostic boundary evidence only and must not be included in the main
  deployable comparison or described as an operational recommendation.
- **D-10:** For `chance_constraint`, run threshold `0.25` only.
- **D-11:** The uptake-regime axis should use only the existing `low` and
  `medium` regimes. Do not add a new high-uptake regime in Phase 8.
- **D-12:** The opt-out/service guardrail axis should run guardrail values
  `0.35` and `0.40`. The manifest/report must state explicitly whether this
  varies `service_quit_rate_guardrail`, `menu_optout_guardrail`, or both.

### Outputs And Manuscript Boundary
- **D-13:** Write `.planning/results/SENSITIVITY_SUMMARY.md` as a conditional
  boundary map: where optimized service menus help, where they fail, and which
  regimes expose profit-service-quality trade-offs.
- **D-14:** Paper-facing tables and figures must be generated from normalized
  rows and artifact builders. Planning summaries may interpret results and cite
  artifact paths, but must not hand-write paper-facing result tables or figures.
- **D-15:** Phase 8 outputs should use status
  `diagnostic_provisional_blocked` unless later gates explicitly authorize a
  stronger status.
- **D-16:** Even if sensitivity results look strong, Phase 8 must not upgrade
  abstract/conclusion-level manuscript claims. It may write manuscript-safe
  diagnostic language such as conditional robustness under named regimes.

### The Agent's Discretion
- The planner may choose exact sensitivity manifest names, suite names, output
  roots, split IDs, and report section headings, provided the decisions above
  are enforced.
- The planner may decide whether each sensitivity axis is implemented as a
  separate study manifest or as a suite of small manifests, as long as
  `phase8_baseline_validation` remains a separate prerequisite gate.
- The planner may choose exact diagnostic artifact filenames and aggregation
  format, provided generated rows remain the source of truth and paper-facing
  tables/figures are artifact-built.
- The planner may choose the minimal script-style tests needed to protect the
  new contracts, but should preserve existing test style under
  `work2_coding/scripts/test_*.py`.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, active runtime root, current gate
  status, fallback conditional framing, and Phase 8 sensitivity requirement.
- `.planning/REQUIREMENTS.md` - Sensitivity requirements `SENS-01` through
  `SENS-03`, including must-have and nice-to-have split.
- `.planning/ROADMAP.md` - Phase 8 goal, success criteria, and additional gate
  rule that separates must-have from nice-to-have sensitivity dimensions.
- `.planning/STATE.md` - Current position, Phase 8 handoff, runtime root, and
  upstream blockers that prevent claim upgrades.
- `.planning/research/SUMMARY.md` - TR-E service-menu framing, evidence ladder,
  sensitivity rationale, and conditional fallback contribution.
- `AGENTS.md` - Repository instructions, active runtime assumption, research
  guardrails, and verification baseline.

### Prior Phase Context And Paper Contract
- `.planning/phases/05-calibration-and-robustness-without-p-hacking/05-CONTEXT.md`
  - Gate-first process lock, allowed/prohibited calibration knobs, pilot/final
  separation, and final rerun boundaries.
- `.planning/phases/06-real-or-semi-real-case-study-feasibility-audit/06-CONTEXT.md`
  - Case-study gate status and labels; important because Phase 8 must not run
  semi-real case experiments.
- `.planning/phases/07-case-study-implementation/07-CONTEXT.md` - Scaffold-only
  case-study completion and blocked-execution status; confirms Phase 8 remains
  RC sensitivity, not case execution.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - Claim ladder, service-bundle
  semantics, no-filter diagnostic boundary, exact/greedy diagnostics, and
  required table/figure families.

### Results And Gate Inputs
- `.planning/results/RC_FORMAL_DIAGNOSIS.md` - Phase 4 diagnosis showing the
  selected formal RC run is diagnostic/provisional and does not support strong
  universal dominance.
- `.planning/results/CALIBRATION_PROTOCOL.md` - Pre-registered ranges for
  `menu_k`, `max_candidates`, ETA filter/threshold, guardrail values, and
  uptake-regime handling.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` - Current frozen/default values
  for `menu_k`, `max_candidates`, `menu_eta_filter_mode`,
  `service_quit_rate_guardrail`, and `menu_optout_guardrail`; final replay
  remains blocked pending gate cleanup.
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` - Dirty-git/provenance
  blocker context to preserve diagnostic/provisional status.

### Manifests And Runtime Contracts
- `work2_coding/Experiments/studies/phase8_baseline_validation.yaml` - Existing
  Phase 8 prerequisite gate comparing `mainline_optimized_mw` and
  `phase8_static_flat_markdown`.
- `work2_coding/Experiments/studies/final_robust_menu.yaml` - Frozen/default
  final robust-menu settings to use as the center of sensitivity design, but
  not to execute as final claim evidence in Phase 8.
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml` -
  Calibration-grid reference for small allowed ranges and non-claim pilot
  boundaries.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Seven-tag
  mainline family, paired fields, varied fields, and normalized-row schema
  reference.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` - Existing pilot
  manifest pattern for non-final paired replay.

### Code And Script Integration Points
- `work2_coding/Src/baseline_validation.py` - Phase 8 baseline validation gate,
  blocking failure rules, claim-ready separation, and report writer.
- `work2_coding/scripts/build_phase8_baseline_validation_report.py` - CLI
  wrapper for writing the baseline validation report.
- `work2_coding/scripts/test_phase8_baseline_validation.py` - Existing tests
  for Phase 8 baseline validation, including paired rows, checkpoint
  provenance, and accounting blockers.
- `work2_coding/Src/paired_replay.py` - Normalized-row fields, paired setting
  resolution, trace/settings hashes, and opt-out/home/meeting-point accounting.
- `work2_coding/Src/study_execution.py` - Actual replay and blocked-row
  contracts for manifest execution.
- `work2_coding/Src/artifact_status.py` - Claim-ready, diagnostic, incomplete,
  and blocked artifact classification.
- `work2_coding/Src/artifact_builder.py` - Artifact aggregation, tables,
  figures, metadata, filter-mode reporting, and uptake-regime coverage.
- `work2_coding/Src/policy_adapters.py` - Mainline tags, optional Phase 8
  static-pricing baseline, ETA/filter overrides, and guardrail variants.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Menu construction, ETA filtering,
  exact/greedy selection diagnostics, candidate diagnostics, and menu build
  timing.
- `work2_coding/Src/parser.py` - Runtime flags for `menu_k`, `max_candidates`,
  ETA/filter modes, chance threshold, guardrails, pricing modes, and tiered
  menu behavior.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Experiments/studies/phase8_baseline_validation.yaml`: already
  defines the Phase 8 prerequisite baseline gate with five paired splits and
  two policies. Phase 8 sensitivity should depend on it rather than merge into
  it.
- `work2_coding/Src/baseline_validation.py`: already writes
  `PHASE8_BASELINE_VALIDATION.json` and `.md`, opens the Phase 9 release gate
  only when the baseline gate passes, and explicitly keeps `claim_ready=false`.
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml` and
  `.planning/results/CALIBRATION_PROTOCOL.md`: provide the pre-registered
  small ranges for `menu_k`, ETA/filter, guardrail, and uptake-regime
  sensitivity.
- `work2_coding/Src/paired_replay.py`: provides normalized-row schema fields
  needed for Phase 8 outputs, including `trace_hash`, `settings_hash`,
  `checkpoint_load_status`, `menu_k`, `max_candidates`, `filter_mode`,
  `uptake_regime`, `menu_build_time`, opt-out accounting, and status fields.
- `work2_coding/Src/Algorithms/DSPO_Menu.py`: already records exact/greedy
  solver diagnostics, candidate counts, ETA pruning diagnostics, and
  `menu_build_time` that can support sensitivity interpretation.

### Established Patterns
- Active runtime root is `work2_coding/`; older `.planning/codebase/` maps that
  reference `ooh_code/` are historical and must not override current paths.
- Experiments are manifest-driven. Add or adapt YAML manifests rather than
  creating ad hoc paper-facing result scripts.
- Paper-facing evidence flows from normalized rows through artifact builders.
  Generated rows, tables, figures, and claim guards must not be hand-edited.
- Pilot/formal rows require valid `method_family`, `outside_option_util`,
  checkpoint provenance, status fields, and opt-out/home/meeting-point
  accounting to pass artifact gates.
- No-filter rows are diagnostic only. They can explain boundaries or stress
  tests, but cannot support deployable or formal superiority claims.
- Tests are executable script-style Python files under
  `work2_coding/scripts/test_*.py`.

### Integration Points
- Create Phase 8 sensitivity manifests or suites under
  `work2_coding/Experiments/studies/` and/or `work2_coding/Experiments/suites/`
  only after preserving `phase8_baseline_validation` as a separate gate.
- Use `work2_coding/scripts/run_study.py` for actual replay after the baseline
  gate passes.
- Extend or add artifact builder/reporting code only so generated normalized
  rows produce sensitivity tables, figures, and metadata; do not write
  paper-facing tables manually.
- Write `.planning/results/SENSITIVITY_SUMMARY.md` as a planning-side
  interpretation and source-path index after generated artifacts exist.
- Add script-style tests for the new sensitivity manifest contract, baseline
  prerequisite behavior, diagnostic/provisional status, and artifact source
  path requirements.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four gray areas for discussion.
- For all questions in the discussion, the user selected option `1`.
- The user chose must-have-only actual replay and deferred/contract-only
  nice-to-have dimensions.
- The user chose one-factor-at-a-time sensitivity around default/frozen
  settings.
- The user chose `menu_k` values `2`, `3`, and `4`.
- The user chose `phase8_baseline_validation` as a prerequisite gate and
  required sensitivity replay to stop if that gate fails.
- The user allowed actual replay during unresolved gates only as
  diagnostic/provisional pilot evidence with `claim_ready=false`.
- The user chose diagnostic/pilot tier, not formal tier, for Phase 8
  sensitivity.
- The user chose ETA/filter modes `hard`, `interval_overlap`, and
  `chance_constraint` with chance threshold `0.25`; no-filter remains
  diagnostic only.
- The user chose only existing `low` and `medium` uptake regimes.
- The user chose guardrail values `0.35` and `0.40`.
- The user chose a conditional boundary-map narrative for
  `SENSITIVITY_SUMMARY.md`.
- The user chose generated normalized-row/artifact-builder outputs as the only
  source for paper-facing tables and figures.
- The user chose Phase 8 output status `diagnostic_provisional_blocked`.
- The user rejected direct manuscript claim upgrades from Phase 8.

</specifics>

<deferred>
## Deferred Ideas

- Candidate pool size sensitivity (`max_candidates`) is a nice-to-have
  dimension for later work or a future contract, not executable Phase 8 replay.
- Fleet/capacity stress is a nice-to-have dimension for later work or a future
  contract, not executable Phase 8 replay.
- Pricing bounds or price sensitivity is a nice-to-have dimension for later
  work or a future contract, not executable Phase 8 replay.
- High-uptake regime, `menu_k` values `1` and `5`, `soft_penalty` ETA mode, and
  no-filter main-comparison claims are not in Phase 8 actual replay scope.

</deferred>

---

*Phase: 8-Sensitivity And Robustness Experiments*
*Context gathered: 2026-06-15T23:13:09+08:00*
