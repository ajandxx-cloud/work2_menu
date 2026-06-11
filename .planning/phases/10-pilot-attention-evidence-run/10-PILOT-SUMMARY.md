# Phase 10 Pilot Summary

**Status:** Completed pilot evidence; attention claim failed/not supported
**Date:** 2026-06-11
**Study:** `pilot_attention_dspo`
**Source run:** `pilot_attention_dspo-20260611T140616Z-07415c4f`

## Execution Status

| Field | Value |
|---|---|
| execution_status | `completed` |
| placeholder_only | `false` |
| row_count | 4 |
| checkpoint_statuses | `["loaded"]` |
| pair_count | 2 |
| complete_pair_count | 2 |
| tiers | `["pilot"]` |
| git_dirty | `false` |

## Primary Result

The primary metric is `net_objective_proxy`, where higher is better.

| Policy | Mean `net_objective_proxy` |
|---|---:|
| `DSPO_original` | -8378.3 |
| `DSPO_attention` | -8378.3 |
| Delta | 0.0 |

Result: **FAILED / not_supported** for the attention-improves-DSPO claim.

## Secondary Metrics

| Metric | Original mean | Attention mean | Delta |
|---|---:|---:|---:|
| acceptance_rate | 0.6428571428571429 | 0.6428571428571429 | 0.0 |
| optout_rate | 0.35714285714285715 | 0.35714285714285715 | 0.0 |
| meeting_point_uptake_rate | 0.0 | 0.0 | 0.0 |
| service_time_total | 8440.8 | 8440.8 | 0.0 |
| net_price_revenue | 62.5 | 62.5 | 0.0 |

## Regime-Level Rows

| Split | Regime | Policy | Net objective | Acceptance | Opt-out | Meeting-point uptake | Attention score delta total |
|---|---|---|---:|---:|---:|---:|---:|
| `pilot_attention_rc_low_seed0` | low | `DSPO_original` | -8083.0 | 0.6428571428571429 | 0.35714285714285715 | 0.0 | 0.0 |
| `pilot_attention_rc_low_seed0` | low | `DSPO_attention` | -8083.0 | 0.6428571428571429 | 0.35714285714285715 | 0.0 | -2.1530706407964466 |
| `pilot_attention_rc_medium_seed1` | medium | `DSPO_original` | -8673.6 | 0.6428571428571429 | 0.35714285714285715 | 0.0 | 0.0 |
| `pilot_attention_rc_medium_seed1` | medium | `DSPO_attention` | -8673.6 | 0.6428571428571429 | 0.35714285714285715 | 0.0 | -2.211349971599813 |

Low and medium regimes are present, and acceptance/opt-out behavior is non-degenerate. However, meeting-point uptake is zero in both regimes and all policy deltas are zero. This limits the usefulness of the pilot for a positive claim.

## Claim Guard

`ATTENTION_CLAIM_GUARD.json` reports:

```text
claim_ready = false
attention_improves_dspo_allowed = false
primary_metric.delta_mean = 0.0
blocker = primary_metric_not_positive
```

The claim guard is therefore a **NO-GO** for attention superiority.

