# Phase 4: Evidence And Artifacts - Context

**Gathered:** 2026-06-11T14:50:02+08:00
**Status:** Ready for planning
**Language:** Chinese discussion; downstream code and file paths remain English.

<domain>
## Phase Boundary

Phase 4 turns the Phase 3 robust-menu study contracts and normalized-row schema into a provenance-backed evidence pipeline. It should run at least pilot-level non-placeholder evidence, generate normalized rows and aggregate summaries, build tables and figures, mirror lightweight artifacts for review, and enforce status/provenance gates that prevent incomplete or placeholder evidence from supporting formal claims.

Phase 4 does not write manuscript claims, choose a universally winning policy, hand-edit generated results, add attention-based choice/scoring, or treat `no_filter_diagnostic` as an operational recommendation. Phase 5 owns manuscript framing and claim checklist.

</domain>

<decisions>
## Implementation Decisions

### Run Ladder
- **D-01:** Phase 4's minimum completion bar is a real pilot run with non-placeholder results. Formal evidence may be deferred, but Phase 4 must produce a gate/blocker report when formal evidence is unavailable.
- **D-02:** `contract_only` rows may feed placeholder or incomplete artifacts only when those artifacts are visibly marked and cannot support claims.
- **D-03:** If pilot or formal runs lack a required checkpoint, Phase 4 should generate `incomplete` status plus a blocker report, not formal claim-ready artifacts.
- **D-04:** Smoke and pilot runs may train or reuse a shared checkpoint. Formal artifacts require explicit checkpoint provenance.

### Artifact Set
- **D-05:** The artifact builder should generate machine-readable JSON/CSV, core LaTeX tables, and PNG figures.
- **D-06:** Core tables should cover five artifact families: policy summary, robust filtering, exact/greedy solver diagnostics, uptake regime behavior, and provenance/status.
- **D-07:** Core figures should include 4-6 reviewer-facing plots: profit gap, acceptance/opt-out, ETA pruning, home-only share, and exact/greedy build-time or gap behavior.
- **D-08:** Raw outputs remain under `work2_coding/outputs/`. Lightweight snapshots, tables, figures, and status artifacts should be written under `work2_coding/artifacts/` and mirrored to `artifacts/work2_robust_menu/`.

### Artifact Gate
- **D-09:** Rows or artifacts with `placeholder_only=True` may only generate incomplete or diagnostic reports. They must not generate claim-ready tables or figures.
- **D-10:** Invalid checkpoint status in pilot/formal runs blocks claim-ready artifacts and should produce a blocker report plus status/provenance artifact.
- **D-11:** If only one uptake regime is available, Phase 4 may still emit results for the available regime. Artifacts must clearly state the covered regimes so downstream writing does not overgeneralize.
- **D-12:** `no_filter_diagnostic` may appear in main result tables/figures only when grouped or labeled as a diagnostic upper bound. It must not participate in recommended-policy ranking.

### Provenance Pack
- **D-13:** Normalized rows should carry complete provenance: `run_id`, `manifest_hash`, `settings_hash`, `trace_id`, `trace_hash`, checkpoint status/path/hash, git marker, and schema version.
- **D-14:** Each generated artifact should have adjacent metadata/status JSON recording source rows, source run, manifest hash, generation time, and placeholder/incomplete status.
- **D-15:** Environment provenance should record Python version and key package versions or a `pip freeze` snapshot. Formal artifacts require this dependency snapshot to exist.
- **D-16:** Git commit and dirty-state markers should enter provenance. A dirty worktree may still generate artifacts, but status/provenance must explicitly mark it.

### The Agent's Discretion
- The planner may choose exact module names, helper boundaries, metadata filenames, and table/figure filenames as long as the decisions above are preserved.
- The planner may decide whether to implement the artifact builder as one script first or a small package plus CLI, provided tests cover row loading, gates, generated files, and provenance metadata.
- The planner may use compact synthetic or temporary-row fixtures for gate tests, but the Phase 4 evidence path should consume public runner outputs from `work2_coding/scripts/run_study.py`.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning Scope
- `.planning/PROJECT.md` - Project value, active runtime root, no-filter diagnostic framing, and artifact guardrails.
- `.planning/REQUIREMENTS.md` - Phase 4 requirements `ART-01` through `ART-04`.
- `.planning/ROADMAP.md` - Phase 4 goal, success criteria, and boundary before Phase 5 manuscript framing.
- `.planning/STATE.md` - Current phase state and completed Phase 1-3 facts.
- `.planning/research/SUMMARY.md` - Project-level watch-outs for checkpoints, opt-out, no-filter, and placeholder artifacts.
- `AGENTS.md` - Active runtime and verification instructions.

### Prior Phase Context
- `.planning/phases/03-experiment-contracts-and-fair-replay/03-CONTEXT.md` - Phase 3 decisions about manifests, paired replay, normalized rows, baseline policies, and placeholder constraints.
- `.planning/phases/03-experiment-contracts-and-fair-replay/03-VERIFICATION.md` - Phase 3 verification status before Phase 4 consumes contracts.

### Current Runtime Files
- `work2_coding/scripts/run_study.py` - Public study runner currently emitting contract-level rows and summaries.
- `work2_coding/Src/paired_replay.py` - Normalized-row fields, row validation, trace/settings hashes, and placeholder/formal guard.
- `work2_coding/Src/experiment_contracts.py` - Study manifest loading, validation, checkpoint contract rules, and uptake-regime checks.
- `work2_coding/Src/policy_adapters.py` - Policy tag adapters and diagnostic metadata for baselines.
- `work2_coding/experiments/studies/smoke_robust_menu.yaml` - Smoke contract and schema fields.
- `work2_coding/experiments/studies/pilot_robust_menu.yaml` - Pilot contract, checkpoint requirement, and low/medium uptake regime settings.
- `work2_coding/experiments/studies/formal_robust_menu.yaml` - Formal contract, stricter checkpoint provenance, and formal split definitions.
- `work2_coding/experiments/suites/work2_robust_menu.yaml` - Suite grouping for smoke, pilot, and formal studies.
- `work2_coding/scripts/test_smoke_study_rows.py` - Existing runner/row tests and placeholder/formal rejection pattern.
- `work2_coding/scripts/test_paired_replay_contract.py` - Row schema, checkpoint propagation, and formal placeholder guard tests.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Baseline coverage and paired fairness contract tests.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/scripts/run_study.py` already writes `manifest_snapshot.yaml`, `study_summary.json`, `normalized_rows.json`, and `normalized_rows.csv` for contract-only runs.
- `work2_coding/Src/paired_replay.py` already defines `NORMALIZED_ROW_FIELDS`, row validation, `placeholder_only`, checkpoint metadata, trace hashes, and formal placeholder rejection.
- `work2_coding/Src/experiment_contracts.py` already validates smoke/pilot/formal manifests, checkpoint requirements, policy coverage, and uptake regimes.
- Existing script tests under `work2_coding/scripts/test_*.py` provide the preferred direct-execution testing style for Phase 4 artifact gates.

### Established Patterns
- Use `work2_coding/` as the active runtime root. Ignore stale `.planning/codebase/` references to `ooh_code/` unless revalidated against current files.
- Keep generated raw run state separate from lightweight committed artifacts.
- Treat `contract_only` and placeholder rows as diagnostic/incomplete material, not as evidence for formal claims.
- Keep `no_filter_diagnostic` visibly diagnostic and separate from recommended operational policy ranking.

### Integration Points
- Artifact building should consume public run outputs from `work2_coding/outputs/studies/<study>/<run_id>/`.
- Artifact status/provenance should connect row-level fields in `paired_replay.py`, manifest hashes from `experiment_contracts.py`, and source files generated by `run_study.py`.
- Tests should cover artifact file creation, gate behavior for placeholder/checkpoint/status problems, provenance sidecars, and output mirroring to `artifacts/work2_robust_menu/`.

</code_context>

<specifics>
## Specific Ideas

- Add a public artifact builder such as `work2_coding/scripts/build_artifacts.py`.
- Add reusable artifact helpers under `work2_coding/Src/` only if the builder would otherwise become too large.
- Add script-style tests for artifact gates, provenance sidecars, mirror output, and diagnostic labeling.
- Use status names like `claim_ready`, `diagnostic`, `incomplete`, and `blocked` if they help keep artifact eligibility explicit.
- Keep the uptake-regime decision narrow: available-regime results may be emitted, but artifact metadata must identify the coverage.

</specifics>

<deferred>
## Deferred Ideas

- Phase 5 should translate completed artifacts into method/results outline and claim checklist.
- Formal evidence may remain blocked if required checkpoint provenance, dependency snapshot, or non-placeholder rows are unavailable.
- Attention-based choice/scoring, distance-band ETA calibration, and real passenger behavioral validation remain outside v1 Phase 4.

</deferred>

---

*Phase: 04-Evidence And Artifacts*
*Context gathered: 2026-06-11T14:50:02+08:00*
