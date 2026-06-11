# Phase 2: Core Semantics And Robust Menu Logic - Context

**Gathered:** 2026-06-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 2 makes the current `work2_coding/` simulator and menu algorithm scientifically safe enough for later robust time-window menu comparisons. It should repair the minimum runtime contract around `DSPO_Menu`, separate opt-out from accepted service, expose checkpoint load/provenance status, implement robust ETA filtering semantics, and lock objective/solver diagnostics.

Phase 2 does not define formal experiment manifests, run paper-facing studies, generate artifact tables/figures, select a final winning policy, add attention-based choice/scoring, or edit manuscript outputs.

</domain>

<decisions>
## Implementation Decisions

### Menu Runtime Minimum Activation
- **D-01:** Phase 2 should use minimal menu runtime activation. `parser.py` and `config.py` should recognize `DSPO_Menu`, and low-side-effect import/parser checks should pass.
- **D-02:** Fix only real missing contracts needed by current code. Add the minimum `MenuOffer`, `ServiceBundle`, and `Src.Utils.option_features` surfaces expected by `DSPO_Menu.py`; do not turn this into a broad container redesign.
- **D-03:** Expose Phase 2 menu controls explicitly in `work2_coding/Src/parser.py` with conservative defaults, including the `menu_*` fields currently expected by `DSPO_Menu`.
- **D-04:** The menu runtime acceptance target is import plus parser contract: `Src.config` imports, and the parser accepts `DSPO_Menu` and the new menu flags. Constructor, menu-action, and episode smoke tests can be planned only if they fall naturally out of this minimum scope.

### Opt-Out Semantics
- **D-05:** Represent passenger choice with a structured result carrying at least `outcome`, `location`, `offer`, `price`, and `route_mutates`. Outcomes must distinguish `accepted_home`, `accepted_meeting_point`, and `opted_out`.
- **D-06:** Opted-out requests should be recorded in a separate opt-out or demand log, but must not append to HGS/routing data, mutate fleet routes, increment accepted home delivery, or add accepted-service time.
- **D-07:** Use a dual adapter in `Parcelpoint_py.step()` so the simulator can accept both legacy tuple-style choice returns and new structured choice results while Phase 2 migrates behavior.
- **D-08:** Add deterministic script-style tests covering forced opt-out non-mutation, all three passenger outcomes, opt-out count, acceptance rate, service cost, and route-state effects.

### Checkpoint Load Status And Provenance
- **D-09:** Checkpoint load behavior should depend on run mode. Formal and pilot comparisons fail closed when a required shared predictor checkpoint fails to load. Diagnostic and smoke runs may continue only when the fallback is explicit in metadata.
- **D-10:** Result metadata should reach formal provenance level: `checkpoint_load_status`, checkpoint path, load error, checkpoint hash, model type, compatibility reason, run id, manifest/settings summary, and intentional-mismatch marker.
- **D-11:** Intentional mismatch or random initialization is diagnostic only. It may be used for smoke/debug or compatibility investigation, but it must not enter formal policy comparisons.
- **D-12:** Add tests for checkpoint load success/failure status, path/hash/model provenance, and allowed/blocked intentional mismatch behavior.

### Robust ETA Filtering
- **D-13:** Phase 2 should implement the core robust ETA filter subset: `hard`, `interval_overlap`, `chance_constraint`, `soft_penalty`, and `none`. A `calibrated` mode may initially map to parameterized chance/interval behavior rather than a separate full calibration system.
- **D-14:** Keep `none` and wider diagnostics separate. `none` disables ETA pruning only; it must still respect routing feasibility, capacity feasibility, and basic candidate generation constraints. A separate `all_feasible_diagnostic` style mode may represent a wider candidate-availability upper bound.
- **D-15:** Candidate-level ETA diagnostics should be audit-grade: predicted ETA, window bounds, pass/fail, prune reason, sigma, interval bounds, violation probability, filter mode, ETA source/variant, true/oracle ETA when available, soft penalty value, risk score, and whether the objective retained the candidate.
- **D-16:** `soft_penalty` must not prune candidates for ETA risk. It preserves candidates and applies ETA risk only through objective penalty.
- **D-17:** Use an initial global sigma constant or config value, record its source in metadata, and defer distance-band or candidate-type calibration.

### Menu Objective And Solver Semantics
- **D-18:** Preserve both objective families. `risk_adjusted_expected_profit` uses penalty semantics, while `service_guarded_expected_profit` uses guardrail semantics; both remain comparable candidate main methods.
- **D-19:** For service-guarded behavior, choose the highest-profit menu within the opt-out/service guardrail when possible. If no menu satisfies the guardrail, choose the lowest-opt-out fallback and record a fallback reason.
- **D-20:** Exact-small versus greedy-large selection should start from a candidate-count threshold, with a build-time fallback to greedy when needed. Any fallback must be recorded.
- **D-21:** Every menu selection should record solver, candidate count, and enumerated count. Small candidate sets should additionally record exact-vs-greedy value gap, overlap, and build time.
- **D-22:** Phase 2 should not pick the final recommended policy. Keep `risk_adjusted_expected_profit` and `service_guarded_expected_profit` as dual mainline candidates for Phase 3/4 experiments to judge.
- **D-23:** Add objective/solver tests for hand-built menu ordering, solver switching across thresholds/time budget, diagnostic fields, gap metrics, and fallback reasons.

### The Agent's Discretion
- The planner may choose exact helper names and metadata field grouping, as long as the decisions above are preserved.
- The planner may sequence tests around the safest patch order, but parser/import contract, opt-out accounting, checkpoint status, ETA diagnostics, and solver metadata must all be represented in Phase 2 planning.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Scope And Guardrails
- `.planning/PROJECT.md` - Project scope, active runtime root, scientific guardrails, no-filter framing, and deferred attention decision.
- `.planning/REQUIREMENTS.md` - Phase 2 requirements `ACCT-01` through `ACCT-04`, `ETA-01` through `ETA-04`, and `MENU-01` through `MENU-04`.
- `.planning/ROADMAP.md` - Phase 2 goal, success criteria, and boundary against experiment/artifact phases.
- `.planning/STATE.md` - Current phase state and Phase 1 completion facts.
- `.planning/research/SUMMARY.md` - Research summary and watch-outs for opt-out, checkpoint, robust filters, and no-filter diagnostics.
- `AGENTS.md` - Repository-level runtime and verification instructions.

### Prior Phase Facts
- `.planning/phases/01-repository-audit-and-runtime-baseline/01-CONTEXT.md` - Locked Phase 1 decisions, especially `work2_coding/` as active root and stale `ooh_code/` maps.
- `.planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md` - Stage 0 audit, current menu assets, parser/runner exposure gap, opt-out risk, and checkpoint provenance risk.

### Current Runtime Files
- `work2_coding/Src/parser.py` - CLI contract; currently rejects `DSPO_Menu` and lacks expected `menu_*` fields.
- `work2_coding/Src/config.py` - Dynamic algorithm loading and runtime construction path.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Existing menu algorithm asset with ETA modes, objective variants, exact/greedy paths, metadata hooks, and currently missing dependency expectations.
- `work2_coding/Environments/OOH/containers.py` - Domain dataclasses; currently lacks `MenuOffer` and `ServiceBundle` used by `DSPO_Menu.py`.
- `work2_coding/Environments/OOH/customerchoice.py` - Choice model surface where structured choice result and outside/opt-out semantics should be introduced.
- `work2_coding/Environments/OOH/Parcelpoint_py.py` - Simulator transition and route/service mutation surface that must keep opt-out out of accepted service.
- `work2_coding/Src/Algorithms/Agent.py` - Algorithm save/load surface relevant to checkpoint metadata.
- `work2_coding/Src/Utils/Predictors.py` - Predictor checkpoint load/save implementations relevant to load status and hash/provenance.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/Algorithms/DSPO_Menu.py`: Existing menu-oriented algorithm with policy names, ETA filtering logic, pricing/objective variants, and exact/greedy diagnostics. Treat as the asset to minimally expose and repair, not as a missing algorithm.
- `work2_coding/Environments/OOH/Parcelpoint_py.py`: Current simulator transition where route, data, home delivery count, service time, and stats are mutated.
- `work2_coding/Environments/OOH/customerchoice.py`: Existing MNL-style choice paths that can be adapted to emit structured choice results.
- `work2_coding/Src/Utils/Predictors.py` and `work2_coding/Src/Algorithms/Agent.py`: Current checkpoint save/load surfaces where load status and provenance should be made explicit.

### Established Patterns
- Runtime configuration is CLI/parser driven through `work2_coding/Src/parser.py`, then loaded dynamically in `work2_coding/Src/config.py`.
- Existing simulator state is mutable and route-centric. New opt-out handling must avoid accidental append/insert side effects.
- Existing tests are expected to be script-style rather than a heavyweight new test framework.
- `.planning/codebase/*` files contain stale `ooh_code/` paths. Use them as risk memory only after checking current `work2_coding/` files.

### Integration Points
- Parser/config menu exposure connects `work2_coding/Src/parser.py`, `work2_coding/Src/config.py`, and `work2_coding/Src/Algorithms/DSPO_Menu.py`.
- Opt-out semantics connect `work2_coding/Environments/OOH/customerchoice.py`, `work2_coding/Environments/OOH/Parcelpoint_py.py`, and downstream metric extraction.
- Robust ETA and menu objective diagnostics should be attached to candidate/menu metadata in `DSPO_Menu.py` and later row/artifact surfaces.
- Checkpoint load status should be available close to predictor/agent load code and propagated into result metadata without silent random fallback in formal/pilot modes.

</code_context>

<specifics>
## Specific Ideas

- Use `all_feasible_diagnostic` or an equivalent clearly named mode for candidate upper-bound diagnostics so it is not confused with `none`.
- Keep `risk_adjusted_expected_profit` and `service_guarded_expected_profit` as dual mainline candidate policies until experiments decide.
- Do not strengthen no-filter claims or choose a final recommended policy in Phase 2.

</specifics>

<deferred>
## Deferred Ideas

- Distance-band or candidate-type ETA calibration is deferred until after global-sigma robust modes work.
- Formal experiment manifests, paired replay contracts, and policy winner selection belong to Phase 3/4.
- Artifact tables, figures, manuscript claim language, and formal evidence gates belong to Phase 4/5.
- Attention-based choice/scoring remains outside v1.

</deferred>

---

*Phase: 2-Core Semantics And Robust Menu Logic*
*Context gathered: 2026-06-11*
