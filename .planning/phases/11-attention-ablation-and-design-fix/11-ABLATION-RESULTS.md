# Phase 11 Ablation Results

**Status:** Completed; no candidate passed
**Date:** 2026-06-11

## Runs

| Manifest | Run ID | Status | Placeholder | Checkpoint | Git dirty | Complete pairs |
|---|---|---|---|---|---|---|
| `pilot_attention_ablation_strength_high` | `pilot_attention_ablation_strength_high-20260611T141326Z-313a6d81` | completed | false | loaded | false | 2/2 |
| `pilot_attention_ablation_eta_feature_focus` | `pilot_attention_ablation_eta_feature_focus-20260611T141326Z-849f4d2c` | completed | false | loaded | false | 2/2 |
| `pilot_attention_ablation_shared_eta_stronger` | `pilot_attention_ablation_shared_eta_stronger-20260611T141326Z-be81b30e` | completed | false | loaded | false | 2/2 |

## Selection Metrics

| Manifest | Net objective delta | Acceptance delta | Opt-out delta | Meeting-point uptake delta | Service-time delta | Claim guard |
|---|---:|---:|---:|---:|---:|---|
| `pilot_attention_ablation_strength_high` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | blocked: `primary_metric_not_positive` |
| `pilot_attention_ablation_eta_feature_focus` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | blocked: `primary_metric_not_positive` |
| `pilot_attention_ablation_shared_eta_stronger` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | blocked: `primary_metric_not_positive` |

## Interpretation

All ablations preserved procedural evidence integrity, but none improved the primary metric. Attention changes are not reaching realized decisions or outcomes under these pilot settings.

This is a failure for the attention-improves-DSPO superiority claim. It is not acceptable to proceed to formal evidence as if the current attention design is supported.

