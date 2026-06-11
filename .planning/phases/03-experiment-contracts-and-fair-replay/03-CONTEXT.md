# Phase 3: Experiment Contracts And Fair Replay - Context

**Gathered:** 2026-06-11
**Status:** Ready for planning
**Source:** User marked Phase 3 `ready_to_plan`; context synthesized from PROJECT, REQUIREMENTS, ROADMAP, STATE, Phase 2 summaries, and current `work2_coding/` inspection.

<domain>
## Phase Boundary

Phase 3 converts the repaired robust menu runtime into a reproducible study pipeline for fair policy comparisons. It should define smoke, pilot, and formal study contracts; validate policy names, seeds, split IDs, `menu_k`, ETA filter modes, HGS/routing parameters, checkpoint requirements, and output schema; implement paired replay controls; and produce a smoke run or contract-level equivalent that emits normalized rows.

Phase 3 does not generate paper-facing tables/figures, choose a final winning policy, strengthen no-filter claims, hand-edit generated rows, or write manuscript text. Phase 4 owns evidence artifacts. Phase 5 owns paper framing and claim guardrails.

</domain>

<decisions>
## Implementation Decisions

### Runtime Root And Scope
- **D-01:** Use `work2_coding/` as the only active runtime root. Do not recreate `ooh_code/`; `.planning/codebase/` paths that mention it are stale risk memory.
- **D-02:** Keep Phase 3 contract-first. Build small manifest, validation, paired replay, and normalized-row surfaces before formal runs or artifact generation.
- **D-03:** Treat no-filter as diagnostic. It may appear in study contracts as an upper-bound/diagnostic baseline, but row metadata and manifests must not present it as the recommended operational policy.

### Study Contracts
- **D-04:** Define manifest tiers for smoke, pilot, and formal studies. Smoke must be cheap and runnable; pilot/formal may be contracts until Phase 4 executes evidence.
- **D-05:** Manifest validation must cover policy tags, parser-compatible policy settings, seeds, split IDs, `menu_k`, `max_candidates`, ETA filter mode, pricing mode, run mode, checkpoint requirement, HGS parameters, and output schema version.
- **D-06:** Baseline set must include full display, home only, nearest heuristic, top-k cheapest, min-lateness, hard filter, no-filter diagnostic, robust time-window menu, and optional random top-k.
- **D-07:** Formal and pilot manifests must require explicit shared checkpoint provenance. Diagnostic or smoke manifests may continue without a checkpoint only when rows expose the status.

### Paired Replay Fairness
- **D-08:** Every compared policy in a study must share request traces, split ID, seed, data seed, test seed, pricing mode, HGS/reopt parameters, candidate pool settings, checkpoint path/hash/status, and base behavior parameters unless the manifest marks a field as intentionally varied.
- **D-09:** Request traces should be materialized or reconstructible with a trace ID/hash. Normalized rows must carry `trace_id` or equivalent trace provenance.
- **D-10:** Policy adapters must set only intended policy/filter/objective knobs. They must not accidentally change data split, checkpoint, pricing, routing, or HGS parameters.
- **D-11:** Uptake regime checks should include at least low and medium behaviorally live settings when runtime permits. If a regime is not executable in Phase 3, record it as a validated contract for Phase 4.

### Normalized Rows
- **D-12:** Normalized rows must include at least study/run identifiers, policy tag, seed, split ID, trace ID, checkpoint status/path/hash, manifest hash, run mode, `menu_k`, filter mode, effective policy, solver diagnostics, acceptance/opt-out metrics, and placeholder/incomplete status.
- **D-13:** Output schemas should be validated by script-style tests before being consumed by artifact builders.
- **D-14:** Smoke rows may be diagnostic or incomplete, but this must be explicit. Formal rows must not be placeholder-only.

### The Agent's Discretion
- The planner may choose exact module names, manifest field names, and normalized row helper boundaries as long as the decisions above remain visible in code and tests.
- The implementation may use deterministic synthetic replay fixtures for fast contract tests, but the smoke study command should exercise the same public runner and row writer planned for real studies.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Scope
- `.planning/PROJECT.md` - Project value, runtime root, no-filter diagnostic framing, and artifact guardrails.
- `.planning/REQUIREMENTS.md` - Phase 3 requirements `EXP-01` through `EXP-04`.
- `.planning/ROADMAP.md` - Phase 3 goal, success criteria, and boundary before Phase 4 evidence.
- `.planning/STATE.md` - Current `ready_to_plan` state and Phase 2 completion.
- `.planning/research/SUMMARY.md` - Project-level watch-outs for checkpoint, opt-out, no-filter, and generated artifacts.
- `AGENTS.md` - Active runtime and verification instructions.

### Prior Phase Facts
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-01-SUMMARY.md` - Parser/menu runtime contract and script-test pattern.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-02-SUMMARY.md` - Structured `ChoiceResult`, opt-out accounting, stats metadata.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-03-SUMMARY.md` - Checkpoint provenance, fail-closed run modes, metadata fields.
- `.planning/phases/02-core-semantics-and-robust-menu-logic/02-04-SUMMARY.md` - Robust ETA modes, candidate diagnostics, solver telemetry.

### Current Runtime Files
- `work2_coding/Src/parser.py` - Parser flags for menu policies, ETA modes, checkpoint/run mode, and HGS settings.
- `work2_coding/Src/config.py` - Runtime construction, seed setting, checkpoint metadata defaults, output paths.
- `work2_coding/run.py` - Legacy solver train/eval loop; useful but not yet a manifest study runner.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Policy names, robust ETA/objective logic, selected-offer metadata, solver diagnostics.
- `work2_coding/Environments/OOH/Parcelpoint_py.py` - Opt-out/acceptance stats and route-state behavior.
- `work2_coding/Environments/OOH/customerchoice.py` - Menu choice and outside-option behavior.
- `work2_coding/scripts/test_menu_runtime_contract.py` - Script-style regression pattern.
- `work2_coding/scripts/test_optout_accounting.py` - Opt-out accounting coverage.
- `work2_coding/scripts/test_checkpoint_provenance.py` - Checkpoint provenance coverage.
- `work2_coding/scripts/test_robust_menu_logic.py` - Robust menu metadata coverage.

</canonical_refs>

<code_context>
## Existing Code Insights

- `work2_coding/` currently lacks a manifest-based study runner and normalized row pipeline. Phase 3 should add these rather than patching ad hoc behavior into `run.py`.
- Parser choices already expose required menu policies and ETA modes. Study manifests can validate against parser choices instead of duplicating policy lists by hand.
- `Config` redirects stdout through `Utils.Logger`; a study runner should restore/contain stdout where needed so machine-readable row writing remains reliable.
- `Parcelpoint_py.step()` returns `stats[8]` metadata containing opt-out and acceptance rates. Row extraction should prefer this structured metadata over legacy positional inference.
- `DSPO_Menu.get_action_menu()` writes selected-offer metadata for effective policy, ETA diagnostics, menu build time, and solver diagnostics. Row extraction should consume these fields when available.
- Pilot/formal checkpoint failures should fail closed through Phase 2 `Agent.load_checkpoint()` and predictor load metadata. Phase 3 rows should expose the status rather than guessing.

</code_context>

<specifics>
## Specific Ideas

- Add `work2_coding/experiments/studies/*.yaml` for smoke, pilot, and formal contracts and `work2_coding/experiments/suites/*.yaml` for grouped runs.
- Add a small reusable module, for example `work2_coding/Src/experiment_contracts.py`, for manifest loading, validation, manifest hashing, policy expansion, paired-setting checks, and normalized row schema.
- Add `work2_coding/scripts/run_study.py` as the public study runner and `work2_coding/scripts/test_experiment_contracts.py`, `test_paired_replay_contract.py`, and `test_smoke_study_rows.py` as script-style tests.
- Keep smoke tiny: short episodes, one split, deterministic seed, low HGS times, and explicit `run_mode: smoke`.

</specifics>

<deferred>
## Deferred Ideas

- Phase 4 should execute pilot/formal evidence, build tables/figures, and enforce artifact gates.
- Phase 5 should write manuscript outlines and claim checklist.
- Attention-based choice/scoring, distance-band ETA calibration, and real passenger validation remain outside v1 Phase 3 scope.

</deferred>

---

*Phase: 03-experiment-contracts-and-fair-replay*
*Context gathered: 2026-06-11*
