# Phase 9: Exact Versus Greedy And Computational Tractability - Context

**Gathered:** 2026-06-16T10:02:14.2694067+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 9 delivers computational-tractability evidence for the online service
menu solver. The phase should compare small exact menu enumeration against
large-candidate greedy/fallback behavior under paired RC replay, then report
candidate count, enumerated menu count, menu build time, relative optimality
gap, menu overlap, fallback/status, and claim-ready blockers.

This phase is not a provenance cleanup phase, not a final formal rerun phase,
not a case-study execution phase, and not a manuscript claim-upgrade phase.
Existing Phase 9 DSPO family validation is treated as a passed prerequisite
status gate only. The main Phase 9 work remains exact-versus-greedy
tractability. Outputs may open diagnostic tractability/status language, but
must keep `claim_ready=false` while current dependency snapshot and clean-git
provenance blockers remain unresolved.

</domain>

<decisions>
## Implementation Decisions

### Phase 9 Boundary
- **D-01:** Keep `phase9_dspo_family_validation` as a prerequisite status gate.
  It has already passed and may be cited as status context, but it is not the
  main exact-versus-greedy tractability result.
- **D-02:** Do not turn Phase 9 into provenance or artifact-gate cleanup.
  Existing `claim_ready=false` blockers remain in force and must be reported.
- **D-03:** Do not rerun the full DSPO family validation study. Cite the
  existing passed report and allow only lightweight status/existence checks if
  the planner needs them.
- **D-04:** Express Phase 9 final status as
  `tractability diagnostic passed/open, claim-ready still blocked` when the
  exact-greedy diagnostic succeeds.

### Candidate-Set Scale Design
- **D-05:** Use `max_candidates=8` and `menu_exact_threshold=8` as the small
  exact benchmark scale.
- **D-06:** Use `max_candidates=12` and `max_candidates=16` as large greedy
  scales.
- **D-07:** Keep `menu_k=3` fixed throughout Phase 9. Do not mix Phase 8 menu
  size sensitivity back into this tractability phase.
- **D-08:** Represent exact infeasibility for large candidate sets through the
  existing threshold-triggered fallback mechanism. Record
  `solver_fallback_reason=above_exact_threshold` and related metadata rather
  than forcing exact enumeration with a timeout.

### Run Tier And Paired Fairness
- **D-09:** Run Phase 9 exact-greedy evidence as formal-equivalent diagnostic
  replay: formal-like paired replay and loaded checkpoint requirements, but
  diagnostic/status-gated outputs with `claim_ready=false`.
- **D-10:** Reuse the five Phase 8 / existing Phase 9 DSPO validation paired
  splits, including low and medium uptake regimes.
- **D-11:** Compare solver-scale variants within the same split. Each split
  should contain comparable rows for small exact `max_candidates=8`, large
  greedy `max_candidates=12`, and large greedy `max_candidates=16`, while
  sharing seed, request trace, checkpoint, choice parameters, pricing settings,
  and HGS settings except for solver/candidate-scale fields.
- **D-12:** Require the shared checkpoint to load successfully and record
  checkpoint path, hash, required flag, and load status. Missing or failed
  checkpoint loading should produce blocked rows/report status, not random-model
  replacement.

### Outputs And Claim Narrowing
- **D-13:** Write `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` as
  the planning-side interpretation, and generate runtime reports/artifacts as
  the source for paper-facing tables and figures.
- **D-14:** Phase 9 table/figure outputs must include candidate count,
  enumerated menu count, menu build time, relative optimality gap, menu overlap,
  fallback/status, and source artifact metadata.
- **D-15:** If greedy gaps are large, narrow the computational claim to:
  "computationally fast but approximate; quality is regime-dependent." Do not
  claim greedy is near-optimal when gap/overlap evidence does not support it.
- **D-16:** Phase 9 completion requires 15 solver-scale rows
  (5 paired splits x 3 solver-scale variants) to be completed or explicitly
  blocked, plus report/artifact outputs. Completion does not require
  claim-ready status; `claim_ready=false` must remain visible.

### The Agent's Discretion
- The planner may choose exact study manifest names, policy tags, report
  filenames, and artifact directory names, provided the three solver-scale
  variants and five-split paired contract above are enforced.
- The planner may decide whether to extend the existing general artifact
  builder or add a Phase 9-specific builder, as long as paper-facing tables and
  figures are generated from normalized rows and metadata rather than hand
  edited.
- The planner may choose exact blocked-report wording and test names, provided
  failures are explicit and include minimal repair/rerun guidance.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, active runtime root, current
  diagnostic/provisional status, fallback claim framing, and Phase 9
  requirement.
- `.planning/REQUIREMENTS.md` - Requirements `COMP-01` and `COMP-02` for
  exact-small versus greedy-large evidence and computational credibility.
- `.planning/ROADMAP.md` - Phase 9 goal, success criteria, and claim-narrowing
  rule when greedy gaps are large.
- `.planning/STATE.md` - Current position, Phase 9 handoff, runtime root, and
  upstream blockers that prevent claim-ready evidence.
- `.planning/research/SUMMARY.md` - TR-E service-menu framing, evidence ladder,
  and exact-versus-greedy tractability rationale.
- `AGENTS.md` - Repository instructions, active runtime assumption, research
  guardrails, and verification baseline.

### Prior Context And Paper Contract
- `.planning/phases/08-sensitivity-and-robustness-experiments/08-CONTEXT.md`
  - Phase 8 paired split/gate context, diagnostic status, and frozen/default
  center settings.
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` - Mathematical model skeleton,
  exact and greedy solver definitions, claim-to-evidence matrix, required
  exact-greedy table/figure families, and no-overclaim boundary.
- `.planning/results/SENSITIVITY_SUMMARY.md` - Phase 8 completed diagnostic
  sensitivity outputs and source run IDs; Phase 9 should not reinterpret these
  as claim-ready evidence.
- `.planning/results/FROZEN_FINAL_SETTINGS.md` - Frozen/default settings,
  including `menu_k`, `max_candidates`, ETA/filter, and guardrail context.
- `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` - Current provenance/artifact
  blockers that must remain visible rather than cleaned inside Phase 9.

### Existing Phase 9 Status Gate
- `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.md`
  - Passed prerequisite status report; status-only, not a ranking conclusion.
- `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.json`
  - Machine-readable Phase 9 DSPO family validation status, source run ID, and
  `claim_ready=false` reasons.
- `work2_coding/Experiments/studies/phase9_dspo_family_validation.yaml` -
  Existing five-split DSPO family gate and paired-field reference.
- `work2_coding/Src/dspo_validation.py` - Existing Phase 9 DSPO validation
  report/gate helper; use as status context, not as the tractability result.
- `work2_coding/scripts/test_phase9_dspo_family_validation.py` - Existing tests
  for the DSPO status gate and claim-ready separation.

### Runtime Manifests And Replay Contracts
- `work2_coding/Experiments/studies/phase8_baseline_validation.yaml` -
  Baseline five-split gate context referenced by existing Phase 9 validation.
- `work2_coding/Experiments/studies/final_robust_menu.yaml` - Frozen/default
  formal robust-menu settings; reference only, not a final rerun in Phase 9.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Main formal
  paired replay family and normalized-row schema reference.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` - Existing pilot
  manifest pattern with `max_candidates`, exact thresholds, and required
  output fields.
- `work2_coding/scripts/run_study.py` - Manifest-driven study execution entry
  point.

### Code And Artifact Integration Points
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Exact enumeration, greedy
  selection, fallback diagnostics, gap/overlap diagnostics, candidate count,
  enumerated count, and menu build timing.
- `work2_coding/Src/parser.py` - Runtime knobs for `menu_k`, `max_candidates`,
  `menu_exact_threshold`, `menu_exact_gap_threshold`, `menu_selection_solver`,
  and related menu behavior.
- `work2_coding/Src/study_execution.py` - Actual replay execution and
  aggregation of `menu_build_time`, `relative_optimality_gap`,
  `menu_overlap_rate`, and `exact_enumerated_menu_count`.
- `work2_coding/Src/paired_replay.py` - Normalized-row fields for solver
  diagnostics, checkpoint provenance, split/trace/settings hashes, and
  opt-out/home/meeting-point accounting.
- `work2_coding/Src/artifact_builder.py` - Existing exact-greedy table and
  timing figure hooks; likely needs extension for candidate count, enumerated
  count, overlap, and fallback/status.
- `work2_coding/Src/artifact_status.py` - Claim-ready, diagnostic, incomplete,
  and blocked artifact classification.
- `work2_coding/scripts/build_artifacts.py` - General artifact builder wrapper
  and source of generated paper-facing artifacts.
- `work2_coding/scripts/test_artifact_builder.py` - Existing artifact-builder
  test surface including `exact_greedy.tex`.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/Algorithms/DSPO_Menu.py`: already implements exact
  enumeration, greedy selection, threshold fallback, `menu_overlap_rate`,
  `relative_optimality_gap`, `exact_enumerated_menu_count`, and
  `menu_build_time` metadata. Phase 9 should reuse this surface rather than
  inventing a parallel solver.
- `work2_coding/Src/study_execution.py`: already collects and averages solver
  diagnostics into row metadata during actual replay.
- `work2_coding/Src/paired_replay.py`: already exposes solver diagnostic fields
  in normalized-row-v2.
- `work2_coding/Src/artifact_builder.py`: already writes `exact_greedy.tex`
  and `exact_greedy_time.png`, but current aggregation is thin and may need
  Phase 9 extensions for candidate counts, enumerated counts, overlap, and
  fallback/status.
- `work2_coding/outputs/phase9_dspo_family_validation/PHASE9_DSPO_FAMILY_VALIDATION.md`:
  existing passed status gate, useful as a prerequisite reference.

### Established Patterns
- Active runtime root is `work2_coding/`; old `.planning/codebase/` references
  to `ooh_code/` are stale historical memory.
- Experiments are manifest-driven. Phase 9 should add or adapt YAML manifests
  instead of using ad hoc paper-facing result edits.
- Paired replay fairness depends on shared split settings, request traces,
  checkpoint provenance, pricing settings, and HGS settings.
- Paper-facing tables and figures must be generated from normalized rows and
  artifact builders. Do not hand-edit generated rows, tables, figures, or
  manuscript claim outputs.
- Upstream provenance/artifact blockers remain active. Phase 9 may complete as
  diagnostic/status-gated evidence but must not claim formal readiness.

### Integration Points
- Add a Phase 9 exact-greedy tractability study or suite under
  `work2_coding/Experiments/studies/` and/or `work2_coding/Experiments/suites/`.
- Use `work2_coding/scripts/run_study.py` to execute the 15 solver-scale rows
  when planning decides the manifest is ready.
- Extend or add artifact/report code so solver diagnostics produce a generated
  tractability table/figure and a planning-side
  `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md`.
- Add script-style tests under `work2_coding/scripts/test_*.py` for the manifest
  contract, row count/status contract, fallback/infeasibility contract,
  checkpoint-required behavior, and artifact/report fields.

</code_context>

<specifics>
## Specific Ideas

- The user selected all four gray areas for discussion and selected option `1`
  for every decision.
- The existing `phase9_dspo_family_validation` status report is passed but
  remains status-only and `claim_ready=false`.
- The exact-greedy evidence should be 5 paired splits x 3 solver-scale variants:
  small exact `max_candidates=8`, large greedy `max_candidates=12`, and large
  greedy `max_candidates=16`.
- `menu_k=3` is fixed because Phase 8 already handled menu-size sensitivity.
- Large candidate exact infeasibility is shown through fallback metadata, not by
  forcing exact enumeration until timeout.
- If greedy gaps are large, the manuscript-safe interpretation is computational
  speed with approximation risk, not near-optimality.

</specifics>

<deferred>
## Deferred Ideas

- Provenance cleanup, dependency snapshot cleanup, and clean-git claim-ready
  artifact enabling remain outside Phase 9.
- Full rerun of `phase9_dspo_family_validation` is deferred unless a later gate
  explicitly requires it.
- `max_candidates=20`, varying `menu_k`, forced exact timeout experiments, and
  greedy algorithm redesign are outside this Phase 9 context.

</deferred>

---

*Phase: 9-Exact Versus Greedy And Computational Tractability*
*Context gathered: 2026-06-16T10:02:14.2694067+08:00*
