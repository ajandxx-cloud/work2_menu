# Phase 1: Repository Audit And Runtime Baseline - Context

**Gathered:** 2026-06-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 1 delivers a Stage 0 repository audit and a minimal runnable baseline assessment for the current Work2 codebase. It must identify the active runtime root, verify low-side-effect import and entrypoint facts, document stale planning references, list existing menu assets and runner gaps, and propose the minimal patch plan needed for later robust time-window service-menu experiments.

Phase 1 does not modify algorithm behavior, run full episodes, repair opt-out semantics, implement robust ETA filtering, or change manuscript/artifact outputs.

</domain>

<decisions>
## Implementation Decisions

### Runtime Root And Stale References
- **D-01:** Treat `work2_coding/` as the only current active runtime root for Phase 1 planning.
- **D-02:** Treat all `.planning/codebase/*` references to `ooh_code/` as stale map references unless the audit finds concrete current filesystem evidence. Phase 1 should report this mismatch but must not bulk-edit or regenerate `.planning/codebase/` maps.
- **D-03:** Do not create a parallel `ooh_code/` root.

### Baseline Verification Depth
- **D-04:** Use low-side-effect checks only. Do not intentionally create experiment directories, redirect stdout through `Config(args)`, or execute training/evaluation episodes as part of Phase 1 verification.
- **D-05:** The audit should go beyond the already-known `import Src.config` smoke by statically checking `Config` constructability risks, `run.py` / `run_ppo.py` entrypoint wiring, and the relationship between `parser.py` and `DSPO_Menu`.
- **D-06:** `run.py` and `run_ppo.py` should be inspected for entrypoint/import relationships only. Do not run `--max_episodes 1` or any episode-level smoke in Phase 1.

### Menu Asset And Entrypoint Contract
- **D-07:** Explicitly capture the current finding that `work2_coding/Src/Algorithms/DSPO_Menu.py` exists and contains menu-oriented assets, while the current CLI/parser/runner contract appears inconsistent or incomplete.
- **D-08:** Treat the menu entrypoint gap as the highest-priority blocker in the minimal patch plan: existing menu code cannot be relied on for robust comparisons until `parser.py`, runner wiring, and required menu configuration fields expose it consistently.
- **D-09:** Do not turn Phase 1 into a full `DSPO_Menu.py` implementation review. Summarize the asset and blocker; leave behavioral correctness work for Phase 2.

### Stage 0 Audit Output
- **D-10:** The planned Phase 1 deliverable should include `.planning/phases/01-repository-audit-and-runtime-baseline/01-STAGE0-AUDIT.md`.
- **D-11:** Keep the Stage 0 audit report short: concise audit checklist, current facts, blocking gaps, and minimal patch plan.
- **D-12:** The report must separate commands actually executed from recommended follow-up commands. Any command not run must be clearly marked `not run`.

### Phase 1 Completion Boundary
- **D-13:** The planner should plan "audit + minimal patch plan" only. It should not plan runtime fixes as required Phase 1 completion work.
- **D-14:** The minimal patch plan may list future fixes such as parser/runner menu exposure, checkpoint metadata, and opt-out accounting, but Phase 1 itself must not implement those algorithm/runtime behavior changes.

### The Agent's Discretion
- The agent may choose exact wording and structure for the short audit report as long as it preserves the decisions above.
- The agent may choose additional low-side-effect static inspections if they clarify the Stage 0 audit without creating runtime outputs.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Scope And Guardrails
- `.planning/PROJECT.md` - Project scope, active runtime assumption, scientific guardrails, and key decisions.
- `.planning/REQUIREMENTS.md` - Phase 1 audit requirements `AUDIT-01` through `AUDIT-04` and downstream requirement traceability.
- `.planning/ROADMAP.md` - Phase 1 goal and success criteria.
- `.planning/STATE.md` - Current project state and known facts from initialization.
- `.planning/research/SUMMARY.md` - Research summary and recommended first-phase audit targets.
- `AGENTS.md` - Repository-level instructions, runtime root assumption, and verification baseline.

### Existing Codebase Maps To Treat As Stale Until Verified
- `.planning/codebase/STACK.md` - Useful historical stack map, but paths referencing `ooh_code/` are stale for current Phase 1 decisions.
- `.planning/codebase/STRUCTURE.md` - Useful historical structure map, but must be cross-checked against `work2_coding/`.
- `.planning/codebase/CONCERNS.md` - Useful risk list, but contains stale `ooh_code/` assumptions and must be revalidated.

### Current Runtime Root Files
- `work2_coding/README.md` - Current inherited Work1/Work2 package usage notes and runner description.
- `work2_coding/Src/config.py` - Runtime path setup, data loading, environment construction, and dynamic algorithm loading.
- `work2_coding/Src/parser.py` - Current CLI argument schema; important because it does not currently expose `DSPO_Menu` or menu-specific parser fields.
- `work2_coding/run.py` - Main DSPO-style training/evaluation loop to inspect, not execute, in Phase 1.
- `work2_coding/run_ppo.py` - PPO runner to inspect, not execute, in Phase 1.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Existing menu-oriented algorithm asset; audit should summarize its presence and entrypoint mismatch.
- `work2_coding/Src/Algorithms/Agent.py` - Checkpoint save/load surface currently visible through algorithm base behavior.
- `work2_coding/Environments/OOH/customerchoice.py` - Current MNL choice model and home/parcelpoint choice semantics.
- `work2_coding/Environments/OOH/Parcelpoint_py.py` - Simulator transition, route mutation, and service accounting surface.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/Algorithms/DSPO_Menu.py`: Contains existing menu-mode concepts including menu policies, ETA-related fields, objective variants, exact/greedy selection paths, and metadata hooks. Treat as a real current asset, not missing code.
- `work2_coding/Environments/OOH/`: Contains current simulator, MNL choice model, route helpers, containers, and bundled data.
- `work2_coding/run.py` and `work2_coding/run_ppo.py`: Existing runner loops for inherited algorithms.

### Established Patterns
- `work2_coding/Src/config.py` dynamically loads algorithms from `Src/Algorithms` based on `args.algo_name` and creates experiment/log/checkpoint/results directories during `Config(args)` construction.
- `work2_coding/Src/parser.py` is the main CLI contract for runtime knobs, but currently lists `algo_name` choices as inherited algorithms and lacks obvious menu-mode parser fields.
- Existing `.planning/codebase` documents are useful as historical risk memory but are not authoritative for paths because current filesystem inspection shows `work2_coding/`, not `ooh_code/`.

### Integration Points
- Menu runtime exposure likely needs future work around `work2_coding/Src/parser.py`, `work2_coding/Src/config.py`, and runner selection, but Phase 1 should only document this as a blocker and patch-plan item.
- Opt-out and route-state risks likely involve `work2_coding/Environments/OOH/customerchoice.py`, `work2_coding/Environments/OOH/Parcelpoint_py.py`, and metric extraction surfaces, but behavior changes belong to Phase 2.
- Checkpoint metadata and failure visibility likely involve algorithm/model save-load surfaces and future experiment row metadata, but Phase 1 should only identify the risk.

</code_context>

<specifics>
## Specific Ideas

- Use a short Stage 0 report, not a broad refactor plan.
- Favor low-side-effect static verification because `Config(args)` can create runtime directories and redirect stdout.
- Report exact executed smoke commands separately from recommended commands marked `not run`.
- Put parser/runner menu exposure at the top of the minimal patch plan because `DSPO_Menu.py` exists but is not currently exposed by the inherited CLI contract.

</specifics>

<deferred>
## Deferred Ideas

- Implementing parser/runner fixes for menu mode belongs after Phase 1 unless a later phase explicitly includes it.
- Repairing opt-out accounting belongs to Phase 2.
- Adding explicit checkpoint load status and provenance metadata belongs to Phase 2 and later experiment/artifact phases.
- Robust ETA filter implementation, menu objective changes, exact/greedy behavior changes, and formal replay contracts belong to later phases.

</deferred>

---

*Phase: 1-Repository Audit And Runtime Baseline*
*Context gathered: 2026-06-11*
