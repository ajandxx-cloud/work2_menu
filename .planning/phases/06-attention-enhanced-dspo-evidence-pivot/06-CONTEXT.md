# Phase 6: Attention-Enhanced DSPO Evidence Pivot - Context

**Gathered:** 2026-06-11T18:20:31+08:00
**Status:** Ready for planning
**Language:** Chinese discussion; downstream code, file paths, field names, and policy tags remain English.

<domain>
## Phase Boundary

Phase 6 makes the main Work2 method comparison `DSPO_original` vs `DSPO_attention`. It should implement an attention-enhanced DSPO variant, preserve the current safe no-attention DSPO/Menu behavior as the original baseline, and generate paired replay evidence on identical request traces, seeds, split IDs, pricing mode, routing/HGS settings, and checkpoint policy.

This phase does not rewrite the simulator, replace routing, hand-edit generated rows, make no-filter an operational recommendation, or rank robust/no-filter/cost-bound policies as the main method comparison. Robust menu diagnostics remain supporting evidence only.

</domain>

<decisions>
## Implementation Decisions

### Attention Integration
- **D-01:** Attention should enter the menu scoring layer first, not the lower-level cost or ETA predictor. The treatment effect should be in menu/candidate scoring so paired replay against `DSPO_original` remains clean.
- **D-02:** The first attention mechanism should model per-candidate importance weights using existing candidate and `MenuOffer.metadata` style signals such as ETA risk, walk/time, price, predicted/system cost, route delay, and capacity risk.
- **D-03:** Use a dual-track implementation contract: run a deterministic, explainable attention mode by default, while leaving explicit `attention_mode` and diagnostics hooks for a future trainable neural attention mode.
- **D-04:** Attention must directly adjust candidate or menu objective scores and be able to change selected bundles. It must not be only a tie-breaker or diagnostics-only annotation.

### Original Baseline
- **D-05:** `DSPO_original` means the current no-attention DSPO/Menu logic with Phase 2-5 safety repairs preserved. It must keep opt-out accounting, checkpoint metadata, paired replay fairness, artifact gates, and fail-closed behavior.
- **D-06:** The main comparison variants must be exposed as policy tags `DSPO_original` and `DSPO_attention` in manifests and normalized rows.
- **D-07:** In the main comparison, the only substantive difference between `DSPO_original` and `DSPO_attention` is attention score adjustment enabled vs disabled. They must share menu policy, filter mode, objective mode, pricing, routing/HGS settings, checkpoint policy, request traces, and seeds.
- **D-08:** Normalized rows must explicitly record method identity and attention metadata, not infer it only from `policy_tag`. At minimum, downstream planners should add fields or equivalent schema support for `method_variant`, `attention_enabled`, `attention_mode`, and an attention weight/diagnostic summary.

### Evidence And Claim Gates
- **D-09:** Smoke evidence only proves both variants run on identical traces and produce valid row/schema outputs. Pilot completed non-placeholder paired evidence is the minimum level for directional attention improvement language.
- **D-10:** The main claim "attention improves DSPO" is unlocked only when completed, non-placeholder, checkpoint-valid paired evidence shows original/attention rows aligned on the same traces.
- **D-11:** The primary improvement metric is net objective or profit proxy. Acceptance, opt-out, non-home uptake, and service cost are service constraints that must not materially degrade.
- **D-12:** If early results do not support attention, the implementation may search for better attention configurations, but tuning and held-out evaluation must be separated. Search may happen on smoke or pilot tuning splits; formal or held-out splits must be evaluated once and must not guide tuning.

### Manifests And Artifacts
- **D-13:** Create attention-specific study manifests, for example `smoke_attention_dspo.yaml`, `pilot_attention_dspo.yaml`, and `formal_attention_dspo.yaml`. The main attention manifests should focus on `DSPO_original` and `DSPO_attention`; robust-menu baselines may live in diagnostics or a separate suite.
- **D-14:** Create a separate artifact family `work2_attention_dspo`, writing under `work2_coding/artifacts/work2_attention_dspo/` and mirroring to root `artifacts/work2_attention_dspo/`.
- **D-15:** Attention artifacts must include an original-vs-attention paired delta table covering net objective/profit proxy, acceptance, opt-out, non-home uptake, service cost, checkpoint status, and pair completeness. They must also include an attention claim guard JSON.
- **D-16:** Robust policies, `no_filter`, `home_only`, and meeting-point-only/cost-bound outputs are supporting diagnostics only. They must not participate in the main attention claim ranking.

### The Agent's Discretion
- The planner may choose exact helper names, class boundaries, parser flag names, metadata filenames, and deterministic attention formula details as long as the decisions above are preserved.
- The planner may implement the deterministic attention mode before neural attention, provided the schema and diagnostics make future neural attention possible without changing the evidence contract.
- The planner may choose whether policy tags are implemented through adapters, manifest metadata, parser flags, or a small method-variant layer, provided paired replay only varies attention behavior in the main comparison.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Scope
- `AGENTS.md` - Active runtime root, research guardrails, and verification baseline.
- `.planning/PROJECT.md` - Core value, attention-method pivot, runtime root, and no-filter/cost-bound guardrails.
- `.planning/REQUIREMENTS.md` - Phase 6 requirements `ATTN-01` through `ATTN-04` and `BEHAV-01`.
- `.planning/ROADMAP.md` - Phase 6 goal and success criteria.
- `.planning/STATE.md` - Current project state and Phase 6 readiness.
- `.planning/research/SUMMARY.md` - Project-level watch-outs for checkpoints, opt-out, no-filter, and placeholder artifacts.

### Prior Phase Decisions
- `.planning/phases/03-experiment-contracts-and-fair-replay/03-CONTEXT.md` - Manifest, paired replay, normalized row, and baseline fairness contracts.
- `.planning/phases/04-evidence-and-artifacts/04-CONTEXT.md` - Artifact generation, provenance, incomplete/blocked evidence behavior, and diagnostic labeling.
- `.planning/phases/05-manuscript-framing-and-claim-guard/05-CONTEXT.md` - Claim guard posture, blocked evidence handling, and support-document output pattern.

### Runtime Integration Points
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Current menu scoring, ETA filters, expected-profit policies, objective evaluation, solver diagnostics, and selected-offer metadata.
- `work2_coding/Src/policy_adapters.py` - Current policy tag adapter pattern and policy-only drift guard.
- `work2_coding/Src/paired_replay.py` - Normalized row schema, paired setting validation, checkpoint row metadata, and row validation rules.
- `work2_coding/Src/experiment_contracts.py` - Manifest validation, required policy tag checks, paired fields, varied fields, checkpoint requirements, and uptake-regime validation.
- `work2_coding/Src/artifact_builder.py` - Artifact aggregation, ranking eligibility, sidecars, mirroring, and status output pattern.
- `work2_coding/Src/artifact_status.py` - Claim-ready, diagnostic, incomplete, and blocked status classification.
- `work2_coding/experiments/studies/smoke_robust_menu.yaml` - Existing study manifest structure to mirror when creating attention-specific manifests.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/Src/Algorithms/DSPO_Menu.py` already records rich candidate and menu metadata, objective diagnostics, ETA risk penalties, effective policy, solver diagnostics, and menu build time. This is the natural place to add deterministic candidate attention scoring and diagnostics.
- `work2_coding/Src/policy_adapters.py` already validates policy-only overrides and marks diagnostic/cost-bound policies. Phase 6 can add attention-specific tags or a parallel method-variant adapter without letting routing, checkpoint, seed, or HGS settings drift.
- `work2_coding/Src/paired_replay.py` already validates paired settings and normalized rows. Phase 6 should extend this schema for attention identity and pair completeness rather than relying on ad hoc CSV columns.
- `work2_coding/Src/artifact_builder.py` and `work2_coding/Src/artifact_status.py` already provide the artifact/gate pattern for claim readiness, blockers, sidecars, and mirroring.

### Established Patterns
- Use `work2_coding/` as the active runtime root. `.planning/codebase/` maps still contain stale `ooh_code/` references and should be treated as historical patterns unless revalidated against current files.
- Study definitions are YAML manifests under `work2_coding/experiments/studies/`, with suites under `work2_coding/experiments/suites/`.
- Tests are executable Python scripts under `work2_coding/scripts/test_*.py`, using direct `assert` and `main()` functions.
- Generated raw run state stays under `work2_coding/outputs/`; lightweight committed artifacts are mirrored under root `artifacts/`.
- Diagnostic and cost-bound policies should be visible in metadata and excluded from recommended/main claim ranking.

### Integration Points
- Parser/config may need attention flags such as `attention_enabled`, `attention_mode`, deterministic attention weights, and possibly a future neural attention mode selector.
- Policy/manifests should expose `DSPO_original` and `DSPO_attention` without allowing non-attention fields to drift in the main comparison.
- Normalized rows need method and attention fields plus pair-completeness information for artifact and claim gates.
- Artifact generation needs a separate `work2_attention_dspo` output root, paired delta table generation, and an attention-specific claim guard JSON.
- Script tests should cover attention adapter fairness, row schema fields, paired delta construction, attention claim gate blocking, and smoke manifest validity.

</code_context>

<specifics>
## Specific Ideas

- Candidate attention should be explainable in v1 and should expose enough metadata for tables or diagnostics.
- The main attention comparison should be easier to audit than a broad policy ranking: two method tags, same trace, same settings, attention enabled vs disabled.
- Formal or held-out attention evidence must not be used for tuning. Any search for better attention weights must happen on separate tuning splits.
- Suggested artifact names include a paired delta table and an attention claim guard JSON under `work2_attention_dspo`.

</specifics>

<deferred>
## Deferred Ideas

- Trainable neural attention is deferred beyond the first deterministic implementation unless the planner can add it without weakening the evidence contract.
- Menu-level set interaction attention and passenger-state-to-candidate attention remain future ablations/extensions after candidate importance attention is working.
- Robust/no-filter/cost-bound comparisons remain supporting diagnostics, not the Phase 6 main method ranking.

</deferred>

---

*Phase: 06-Attention-Enhanced DSPO Evidence Pivot*
*Context gathered: 2026-06-11T18:20:31+08:00*
