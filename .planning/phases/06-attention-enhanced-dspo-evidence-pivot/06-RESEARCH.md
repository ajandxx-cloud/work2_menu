# Phase 6 Research: Attention-Enhanced DSPO Evidence Pivot

**Researched:** 2026-06-11
**Status:** Complete
**Runtime root:** `work2_coding/`

## Research Question

How should Work2 add an attention-enhanced DSPO treatment while preserving a clean paired replay comparison against the current no-attention DSPO baseline?

## Findings

### Existing Runtime Surface

- `work2_coding/Src/Algorithms/DSPO_Menu.py` is the correct algorithm integration point. It already builds `MenuOffer` candidates, prices menus, evaluates expected-profit objectives, applies ETA risk penalties, selects exact or greedy menus, and writes per-offer and solver metadata.
- `work2_coding/Src/policy_adapters.py` is the current policy tag surface. It can expose `DSPO_original` and `DSPO_attention` through manifest-friendly adapters while guarding against unfair drift in seeds, checkpoint paths, routing, pricing, and HGS settings.
- `work2_coding/Src/paired_replay.py` owns normalized rows and paired setting checks. Attention identity must be explicit row data, not inferred only from `policy_tag`.
- `work2_coding/Src/experiment_contracts.py` currently assumes robust-menu baseline coverage. Attention-focused manifests need either a manifest-level required-tag override or a comparison-family branch so `DSPO_original` and `DSPO_attention` can be the main required tags without pulling robust diagnostics into the main method ranking.
- `work2_coding/Src/artifact_builder.py`, `work2_coding/Src/artifact_status.py`, and `work2_coding/Src/manuscript_claims.py` already provide the fail-closed pattern for artifact status and manuscript claim eligibility. Phase 6 should reuse that posture in a separate `work2_attention_dspo` artifact family.

### Recommended Attention Design

Add a deterministic v1 attention mode inside `DSPO_Menu` after candidate/menu pricing and before final objective comparison. The attention treatment should:

- Read existing candidate metadata and offer fields: ETA risk, walk distance, pickup time deviation, price, predicted/system/menu cost, route delay, and remaining capacity.
- Compute an explainable scalar attention weight or score delta per candidate.
- Adjust candidate/menu objective scores enough to change selected bundles when attention favors a different option.
- Record diagnostics on every selected offer and in `last_policy_diagnostic`: `method_variant`, `attention_enabled`, `attention_mode`, weight summary, and score contribution.
- Leave a future neural-attention hook visible through parser/config names without making trainable attention a Phase 6 prerequisite.

This keeps the treatment effect in menu scoring, not in route feasibility, checkpoint loading, passenger choice semantics, or lower-level cost/ETA prediction.

### Pairing And Claim Guard Implications

The main attention comparison should contain exactly two method variants:

- `DSPO_original`: safe current DSPO/Menu behavior with attention disabled.
- `DSPO_attention`: same policy/objective/filter/runtime settings with attention enabled.

For the main study pair, the only intentionally varied fields should be attention/method fields such as `method_variant`, `attention_enabled`, `attention_mode`, and deterministic attention weights. Seeds, split IDs, traces, pricing, routing/HGS settings, checkpoint policy, candidate limits, ETA filter mode, and menu objective must remain paired.

Smoke evidence should prove executability, row validity, and pair alignment only. Directional improvement language requires pilot-or-better completed non-placeholder paired evidence with valid checkpoint provenance. Formal or held-out attention evidence must not be used for tuning; any tuning search must be separated from held-out evaluation.

## Recommended Plan Shape

1. Add deterministic attention scoring and diagnostics inside `DSPO_Menu`, parser/config flags, and focused unit tests.
2. Add `DSPO_original` / `DSPO_attention` adapters, attention-focused manifest validation, normalized row fields, and attention study manifests.
3. Add `work2_attention_dspo` artifact generation with paired delta tables and an attention-specific fail-closed claim guard.
4. Run contract tests, import smoke, attention smoke study, and artifact-gate checks; if pilot/formal checkpoints are absent, record blockers rather than producing claims.

## Risks

- If attention only annotates selected offers, it will not satisfy the treatment contract. Tests must prove selected bundles can change.
- If attention manifests reuse broad robust-menu policy rankings, the main comparison becomes scientifically noisy. Keep robust/no-filter/cost-bound outputs diagnostic.
- If normalized rows lack explicit attention fields, artifact builders and claim guards will have to infer method identity from policy tags. Add row fields instead.
- If pilot/formal evidence runs without required checkpoint provenance, the claim guard must remain blocked.

## RESEARCH COMPLETE
