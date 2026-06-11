# Phase 11 Formal Candidate Decision

**Decision:** STOP superiority claim
**Date:** 2026-06-11

## Decision Rule

The preregistered rule required exactly one ablation candidate with:

- completed non-placeholder rows.
- loaded checkpoint provenance.
- complete original/attention pairs.
- low and medium regimes present.
- positive `net_objective_proxy_delta_mean`.
- service constraints passing.

## Result

Zero candidates passed. All three ablations had:

```text
net_objective_proxy_delta_mean = 0.0
attention_improves_dspo_allowed = false
blocker = primary_metric_not_positive
```

## Consequence

No formal candidate is selected.

The current attention-enhanced DSPO design should not proceed to formal superiority evidence. The superiority claim is stopped for this design until a new, separately justified attention mechanism or objective pathway is created and preregistered.

## Allowed Language

- "Ablations completed with loaded checkpoint provenance."
- "No tested attention ablation improved the primary pilot metric."
- "The current attention design does not support an attention-improves-DSPO claim."

## Blocked Language

- "Attention improves DSPO."
- "Ablation supports formal superiority testing."
- "The current design should proceed to formal evidence."

