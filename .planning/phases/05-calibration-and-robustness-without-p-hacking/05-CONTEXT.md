# Phase 5: Calibration And Robustness Without P-Hacking - Context

**Gathered:** 2026-06-15T14:41:40+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 5 defines a credible calibration and robustness protocol for pursuing a
strong central empirical claim after Phase 4 found the selected formal RC run
diagnostic but not claim-ready. This phase should first restore provenance and
readiness gates, then write `.planning/results/CALIBRATION_PROTOCOL.md`, create
or define calibration/final manifests if needed, and write
`.planning/results/FROZEN_FINAL_SETTINGS.md` before any final rerun.

This phase must not tune directly on current or future final formal test
results, hand-edit generated rows or paper artifacts, delete unfavorable
seeds/splits/baselines/metrics, or treat calibration pilot rows as final claim
evidence.

</domain>

<decisions>
## Implementation Decisions

### Phase 5 Route Choice
- **D-01:** Continue pursuing a strong central empirical claim, but only through
  clean provenance plus pre-registered pilot/final calibration. Existing formal
  test results must not be used for direct parameter tuning.
- **D-02:** The order is gate first, then calibration. Resolve dirty-git and
  provenance/readiness blockers before calibration protocol and pilot/final
  manifests drive any experiment execution.
- **D-03:** If gate cleanup still leaves readiness/artifact/claim-ready
  foundations blocked, stop and diagnose. Do not start calibration pilot as a
  workaround for blocked gates.
- **D-04:** Phase 5 success is a credible process lock, not a better result:
  provenance/readiness restored, calibration protocol locked, pilot used only
  for pre-registered setting selection, and final settings frozen before final
  rerun.

### Allowed And Prohibited Calibration Boundary
- **D-05:** Allowed calibration should focus on realism and mechanism
  parameters such as `menu_k`, `max_candidates`, ETA filter/threshold,
  opt-out guardrail, and uptake regime. Changes must be justified by
  operational realism or robustness, not ranking improvement alone.
- **D-06:** Explicitly prohibit optimizing formal/final ranking, selecting
  parameters from current or future final formal test results, deleting seeds,
  splits, baselines, or unfavorable metrics, and hand-editing rows or artifacts.
- **D-07:** Pilot selection should use pre-registered multi-metric thresholds:
  profit non-degradation, acceptance/opt-out/meeting-point uptake mechanism
  signals, and service-quality guardrails. Do not choose final settings by
  single profit ranking.
- **D-08:** Candidate ranges should be small and explainable, with roughly 2-3
  candidate values per knob where possible, to avoid open-ended search.

### Pilot/Final Split Design
- **D-09:** Use strict pilot/final separation. Calibration pilot uses
  independent pilot splits/seeds and selects pre-registered settings only;
  final formal uses frozen independent formal splits/seeds. Pilot rows must not
  become final claim evidence.
- **D-10:** Keep the full seven-tag mainline policy family in both calibration
  pilot and final so the strong central claim remains comparable across
  no-menu, fixed-menu, random-menu, product-ablation, window-ablation, and
  adaptive baselines.
- **D-11:** Retrain and lock calibration/final checkpoints with explicit paths,
  hashes, sidecars, and load status. Checkpoint choice must be pre-registered
  and must not change based on pilot or final ranking.
- **D-12:** Freeze final settings at complete manifest granularity: final
  manifest hash, policy tags, split IDs/seeds, checkpoint path/hash, paired
  fields, varied fields, key runtime knobs, and artifact/claim gate commands.

### Frozen Settings And Rerun Gates
- **D-13:** Pilot may start only after provenance and readiness gates pass:
  dirty-git cleanup is resolved, formal readiness is no longer
  provenance-blocked, checkpoint protocol is written, and calibration protocol
  is locked.
- **D-14:** Final rerun may start only after `FROZEN_FINAL_SETTINGS.md` is
  written and all final settings/gate commands are locked, including final
  manifest hash, checkpoint hash, split IDs, policy tags, and gate commands.
- **D-15:** If the first final rerun still fails to support the strong claim,
  allow a second calibration round only with a new protocol documenting why
  round one failed and what scientific basis justifies another round.
- **D-16:** The second calibration round is a one-time exception requiring
  mechanism-failure diagnosis or operational realism justification. If the
  second final rerun still fails, force downgrade to conditional service-menu
  design framing.

### The Agent's Discretion
- The planner may choose exact manifest names, output roots, and section
  headings, provided pilot/final separation, calibration prohibitions, and
  frozen-setting gates are explicit.
- The planner may propose exact candidate values for allowed knobs, but must
  keep ranges small, justify them by realism/robustness, and record prohibited
  search behavior clearly.
- The planner may decide whether Phase 5 creates new YAML manifests or records
  manifest requirements before implementation, as long as final settings are
  frozen before any final rerun.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, runtime root, research guardrails,
  Phase 5 conditional status, and key decisions through Phase 4.
- `.planning/REQUIREMENTS.md` - Calibration integrity requirements `CAL-01`
  through `CAL-04`.
- `.planning/ROADMAP.md` - Phase 5 goal, gate result, success criteria, and
  global no-overclaim/no-p-hacking rules.
- `.planning/STATE.md` - Current GSD state and Phase 5 readiness position.
- `.planning/research/SUMMARY.md` - TR-E framing, evidence ladder, scientific
  boundary, and fallback contribution path.
- `AGENTS.md` - Repository instructions, active runtime assumption, research
  guardrails, and verification baseline.

### Prior Phase Context And Paper Contract
- `.planning/phases/02-paper-level-research-design-lock/02-CONTEXT.md` -
  Strong-claim reserved framing, claim ladder, paired replay requirements,
  outside-option boundary, no-filter boundary, and fallback route.
- `.planning/phases/03-formal-rc-evidence-pipeline-repair-and-completion/03-CONTEXT.md`
  - Formal run positioning, dirty-git readiness boundary, checkpoint
  provenance, diagnostic artifact policy, and latest completed formal run.
- `.planning/phases/04-rc-result-diagnosis-and-paper-claim-validation/04-CONTEXT.md`
  - Phase 4 claim diagnosis decisions, paired split reporting rules, formal
  run/gate boundaries, and Phase 5 routing.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - Paper research design,
  mathematical skeleton, claim-to-evidence map, table/figure plan, and evidence
  tiers.

### Formal Evidence And Gate Inputs
- `.planning/results/RC_FORMAL_DIAGNOSIS.md` - Phase 4 diagnosis showing the
  selected formal run is diagnostic, not strong-claim-ready.
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` - Dirty-git/provenance
  blocker diagnosis and recommended cleanup boundaries.
- `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
  - Current formal readiness gate, checkpoint status, dirty-git blocker, and
  formal settings metadata.
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/study_summary.json`
  - Selected completed formal run summary used diagnostically by Phase 4.
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json`
  - Selected formal normalized rows; diagnostic input only, not a tuning target.

### Manifests And Runtime Contracts
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Current formal
  seven-tag manifest, paired fields, varied fields, and output schema.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` - Current pilot
  seven-tag manifest and useful reference for calibration split design.
- `work2_coding/Src/formal_readiness.py` - Formal readiness and claim-ready
  blocker logic.
- `work2_coding/Src/study_execution.py` - Study execution status and run
  metadata contract.
- `work2_coding/Src/paired_replay.py` - Paired replay contract and row fields.
- `work2_coding/Src/policy_adapters.py` - Seven-tag policy adapter contract.
- `work2_coding/Src/artifact_builder.py` - Artifact generation contract.
- `work2_coding/Src/artifact_status.py` - Artifact status classification.
- `work2_coding/Src/manuscript_claims.py` - Claim guard and manuscript-frame
  logic.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`: reference formal
  manifest for seven-tag family, paired fields, varied fields, checkpoint
  requirement, and normalized-row schema.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml`: reference pilot
  manifest for calibration design, but Phase 5 should preserve strict pilot
  versus final separation.
- `work2_coding/scripts/check_formal_readiness.py`: readiness command wrapper
  to rerun after provenance cleanup.
- `work2_coding/scripts/train_shared_checkpoint.py`: shared checkpoint
  training entry point if Phase 5 creates locked calibration/final checkpoints.
- `work2_coding/scripts/run_study.py`: manifest study runner for pilot/final
  execution after protocols and gates are locked.
- `work2_coding/scripts/build_artifacts.py` and
  `work2_coding/scripts/build_manuscript_frame.py`: artifact and manuscript
  frame builders, gated by artifact status and claim guard.

### Established Patterns
- Active runtime root is `work2_coding/`; old `.planning/codebase/` references
  to `ooh_code/` are historical and must not override current paths.
- Formal evidence is manifest-driven and row-based; generated rows, tables,
  figures, and claim guard outputs must not be hand-edited.
- Claim language is gated by readiness JSON, completed comparable rows,
  artifact status, and claim guard.
- Tests are executable Python scripts with direct assertions rather than a
  repository-wide pytest configuration.

### Integration Points
- `.planning/results/CALIBRATION_PROTOCOL.md` should state allowed knobs,
  prohibited tuning behavior, pilot selection rules, second-round limits, and
  pilot/final separation.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` should record final manifest
  hash, policy tags, split IDs/seeds, checkpoint path/hash, paired/varied
  fields, runtime knobs, and gate commands before final rerun.
- Calibration/final manifests, if added, should stay under
  `work2_coding/Experiments/studies/` and preserve normalized-row provenance
  fields.
- Gate reruns should use existing readiness, artifact-status, and claim-guard
  contracts rather than bypassing them.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four gray areas for discussion.
- The user selected options `1,1,1,1` for Phase 5 route choice.
- The user selected options `1,1,1,1` for allowed/prohibited calibration
  boundary.
- The user selected options `1,1,1,1` for pilot/final split design.
- The user selected options `1,1,2,1` for frozen settings and rerun gates:
  gates must pass before pilot, final settings must be locked before final
  rerun, one additional calibration round is allowed after first final failure,
  and that second round is a one-time exception with mechanism or operational
  justification.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within Phase 5 scope.

</deferred>

---

*Phase: 5-Calibration And Robustness Without P-Hacking*
*Context gathered: 2026-06-15T14:41:40+08:00*
