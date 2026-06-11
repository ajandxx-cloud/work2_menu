# Phase 6: Attention-Enhanced DSPO Evidence Pivot - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-11T18:20:31+08:00
**Phase:** 06-Attention-Enhanced DSPO Evidence Pivot
**Areas discussed:** Attention integration, original baseline definition, evidence and claim gates, manifests and artifacts

---

## Attention Integration

| Option | Description | Selected |
|--------|-------------|----------|
| Menu scoring layer | Add attention in candidate/menu scoring; keeps paired replay against original DSPO cleaner. | Yes |
| Cost prediction layer | Add attention to cost or ETA prediction; stronger model change but harder checkpoint attribution. | |
| Lightweight ablation | Use a simple attention reweighting first; fast but weaker as a paper contribution. | |

**User's choice:** Menu scoring layer.
**Notes:** The user asked for clarification on what candidate attention means. After explanation, the user selected per-candidate importance weights.

| Option | Description | Selected |
|--------|-------------|----------|
| Candidate importance weights | Weight each candidate bundle using its own features and metadata. | Yes |
| Menu interaction attention | Model substitution/complementarity among options in the displayed menu. | |
| Passenger-state matching | Attend from passenger/request state to candidate features. | |

**User's choice:** Candidate importance weights.
**Notes:** First implementation should use existing candidate metadata and remain easy to test.

| Option | Description | Selected |
|--------|-------------|----------|
| Deterministic explainable weights | Explicit formula or small deterministic module over ETA, walk/time, price, cost, and capacity. | |
| Trainable neural attention | Add a learned attention head with training/checkpoint implications. | |
| Dual track | Default to deterministic explainable attention while preserving a neural-attention interface. | Yes |

**User's choice:** Dual track.
**Notes:** Deterministic v1 should be runnable; neural extension hooks should remain visible.

| Option | Description | Selected |
|--------|-------------|----------|
| Adjust objective score | Attention changes candidate/menu objective scores and can change selected bundles. | Yes |
| Tie-breaker only | Attention only resolves close original-score ties. | |
| Diagnostics only | Record attention weights without affecting selection. | |

**User's choice:** Adjust objective score.
**Notes:** Attention must have a real treatment effect for the main comparison.

---

## Original Baseline Definition

| Option | Description | Selected |
|--------|-------------|----------|
| Safe original | Current no-attention DSPO/Menu logic with Phase 2-5 safety repairs preserved. | Yes |
| Historical original | Try to restore an older DSPO behavior even if it has weaker guardrails. | |
| Dual baseline | Main safe original plus historical diagnostic baseline. | |

**User's choice:** Safe original.
**Notes:** Baseline must keep opt-out accounting, checkpoint metadata, paired replay, and artifact gates.

| Option | Description | Selected |
|--------|-------------|----------|
| Policy tag exposure | Use `DSPO_original` and `DSPO_attention` as manifest/row policy tags. | Yes |
| Algorithm/class exposure | Distinguish mainly through algorithm class or `algo_name`. | |
| Dual exposure | Expose both policy tags and code-level class/switch names. | |

**User's choice:** Policy tag exposure.
**Notes:** The main evidence surface should be easy to read from manifests and rows.

| Option | Description | Selected |
|--------|-------------|----------|
| Attention only differs | Original and attention share all settings except attention score adjustment. | Yes |
| New objective allowed | Attention may also introduce new objective shaping. | |
| Strict main, looser appendix | Main comparison is strict; extra ablations can be looser. | |

**User's choice:** Attention only differs.
**Notes:** Main attribution should be strict.

| Option | Description | Selected |
|--------|-------------|----------|
| Explicit row fields | Add method/attention fields to each normalized row. | Yes |
| Policy tag only | Infer identity only from `policy_tag`. | |
| Sidecar metadata | Keep row schema compact and store attention details in sidecars. | |

**User's choice:** Explicit row fields.
**Notes:** Rows should support transparent paired delta analysis.

---

## Evidence And Claim Gates

| Option | Description | Selected |
|--------|-------------|----------|
| Smoke runs, pilot judges direction | Smoke only proves runnable/schema validity; pilot non-placeholder evidence can support directional language. | Yes |
| Smoke allows direction | Smoke output can support initial improvement language. | |
| Formal only | No improvement language before formal evidence. | |

**User's choice:** Smoke runs, pilot judges direction.
**Notes:** Smoke evidence is not enough for method claims.

| Option | Description | Selected |
|--------|-------------|----------|
| Completed non-placeholder paired evidence | Require completed rows, non-placeholder evidence, valid checkpoint status, and aligned original/attention pairs. | Yes |
| Artifact claim_ready only | Reuse generic artifact readiness without attention-pair checks. | |
| Human override | Allow claim after manual review even when gates are incomplete. | |

**User's choice:** Completed non-placeholder paired evidence.
**Notes:** Claim gate must fail closed.

| Option | Description | Selected |
|--------|-------------|----------|
| Net objective/profit primary | Primary metric is net objective/profit proxy; service metrics are constraints. | Yes |
| Multiple metrics equal | Present all metrics without a single primary metric. | |
| User experience primary | Prioritize opt-out and non-home uptake over profit/cost. | |

**User's choice:** Net objective/profit primary.
**Notes:** Acceptance, opt-out, non-home uptake, and service cost must not materially degrade.

| Option | Description | Selected |
|--------|-------------|----------|
| Fail closed and diagnose | Block superiority claim and report deltas/failure causes. | |
| Mixed-results claim | Allow partial scenario or metric claims. | |
| Search better attention config | Try better attention settings if early results do not support attention. | Yes |
| Tuning/held-out separation | Search only on tuning splits; formal/held-out split is evaluated once. | Yes |

**User's choice:** Search better attention config with tuning/held-out separation.
**Notes:** The guardrail was added to avoid p-hacking and keep formal evidence credible.

---

## Manifests And Artifacts

| Option | Description | Selected |
|--------|-------------|----------|
| Attention-specific manifests | New smoke/pilot/formal manifests focused on `DSPO_original` and `DSPO_attention`. | Yes |
| Extend robust-menu manifests | Add attention variants into existing robust-menu studies. | |
| Suite combining both | Keep attention and robust studies separate, then combine in a suite. | |

**User's choice:** Attention-specific manifests.
**Notes:** Robust-menu baselines may remain diagnostics or suite members, not the main comparison.

| Option | Description | Selected |
|--------|-------------|----------|
| New `work2_attention_dspo` family | Write and mirror a separate attention artifact tree. | Yes |
| Reuse `work2_robust_menu` | Continue using the existing robust artifact family. | |
| Write both | Main new family plus compatible robust summary. | |

**User's choice:** New `work2_attention_dspo` family.
**Notes:** Keeps the attention evidence from being mixed with currently blocked robust-menu artifacts.

| Option | Description | Selected |
|--------|-------------|----------|
| Paired delta plus claim guard JSON | Generate paired deltas and an attention-specific guard. | Yes |
| Policy summary only | Add original/attention rows to policy summary. | |
| Diagnostics-focused | Emphasize attention weights and feature importance. | |

**User's choice:** Paired delta plus claim guard JSON.
**Notes:** Delta artifacts must include pair completeness and checkpoint status.

| Option | Description | Selected |
|--------|-------------|----------|
| Supporting diagnostics only | Robust/no-filter/cost-bound outputs are not in the main ranking. | Yes |
| Rank everything together | Put all methods in one ranking. | |
| No robust diagnostics | Keep Phase 6 artifacts purely attention-only. | |

**User's choice:** Supporting diagnostics only.
**Notes:** Main attention ranking should only compare `DSPO_original` and `DSPO_attention`.

## The Agent's Discretion

- Exact helper boundaries, parser flag names, deterministic attention formula, and artifact filenames are left to planner/executor judgment.
- Neural attention is allowed as a future extension surface but not required for first evidence.

## Deferred Ideas

- Trainable neural attention.
- Menu-level interaction attention.
- Passenger-state-to-candidate matching attention.
- Robust/no-filter/cost-bound policy ranking as a main method comparison.
