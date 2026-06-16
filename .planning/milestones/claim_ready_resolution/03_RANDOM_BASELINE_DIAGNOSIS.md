# Phase 15 Random Baseline Diagnosis

Date: 2026-06-16

Status: diagnosis only. Phase 15 inspected existing source rows, result summaries, manifests, and code paths. It did not run new empirical experiments, tune parameters, regenerate rows, modify algorithms, repair gates, regenerate artifacts, or upgrade manuscript claims.

## Binding Inputs

This diagnosis treats the Phase 13 and Phase 14 outputs as binding:

- `01_EVIDENCE_BOUNDARY.md`
- `01_CLAIM_READY_FALSE_CAUSES.md`
- `01_BLOCKER_TAXONOMY.md`
- `02_GATE_REPAIR_PLAN.md`
- `02_DIRTY_GIT_ACTIONS_REQUIRED.md`
- `02_ARTIFACT_SCHEMA_REPAIR_PLAN.md`
- `02_CHECKPOINT_PROVENANCE_PLAN.md`

The Phase 10 claim guard remains binding: 8 claims, `claim_ready=false`. The random-menu profit advantage is treated as a serious result unless source evidence proves otherwise.

## Evidence Inspected

- `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv`
- `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv`
- `.planning/results/RC_FORMAL_DIAGNOSIS.md`
- `.planning/results/RC_FORMAL_DIAGNOSTIC_TABLES.md`
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json`
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/study_summary.json`
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/manifest_snapshot.yaml`
- `work2_coding/outputs/phase3_formal_artifacts/aggregates/policy_summary.json`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- Replay metric code paths in `work2_coding/Src/study_execution.py`, `work2_coding/Src/paired_replay.py`, and `work2_coding/Environments/OOH/Parcelpoint_py.py`

## Finding

In the selected formal run, `mainline_random_menu` has higher mean realized net profit than `mainline_optimized_adaptive` because it serves fewer customers and therefore incurs lower operating/service cost and lower discount cost. The optimized adaptive policy improves acceptance and reduces opt-out counts, but the extra served demand is not profitable under the realized replay net-profit definition.

This finding does not delete, hide, or reclassify `mainline_random_menu`. It means the random-menu advantage must remain a central empirical blocker until a later phase proves otherwise through allowed evidence.

## Mean Decomposition

Existing row formula:

- `net_price_revenue = charge_revenue - discount_cost`
- `total_cost = operational_cost + discount_cost`
- `net_profit = net_price_revenue - operational_cost`

That formula is implemented in the replay row builder (`work2_coding/Src/study_execution.py:311-326`) and normalized replay contract (`work2_coding/Src/paired_replay.py:516-525`).

Mean values across the 5 paired formal splits:

| Field | mainline_random_menu | mainline_optimized_adaptive | random - adaptive | Diagnosis |
|---|---:|---:|---:|---|
| net_profit | -176651.52 | -180581.75 | +3930.23 | Random is better by 3930.23 mean net profit. |
| charge_revenue | 1175.68 | 1164.58 | +11.10 | Random has slightly higher aggregate charged revenue. |
| discount_cost | 1188.04 | 1439.97 | -251.93 | Random pays materially less discount. |
| net_price_revenue | -12.36 | -275.39 | +263.03 | Price/discount arithmetic favors random. |
| operational_cost | 176639.16 | 180306.36 | -3667.20 | Random has much lower operating/service-time cost. |
| service_time_total | 176639.16 | 180306.36 | -3667.20 | Persisted rows equate operating cost with service-time total. |
| total_cost | 177827.20 | 181746.33 | -3919.13 | Random has lower total cost. |
| accepted_count | 434.60 | 473.80 | -39.20 | Random accepts fewer customers. |
| served_count | 434.60 | 473.80 | -39.20 | Served count matches accepted count in these rows. |
| count_opted_out | 404.80 | 380.20 | +24.60 | Random loses more demand to opt-out. |
| count_accepted_home | 379.60 | 395.40 | -15.80 | Random has fewer home-service acceptances. |
| count_accepted_meeting_point | 55.00 | 78.40 | -23.40 | Random has fewer meeting-point acceptances. |
| acceptance_rate | 0.5175 | 0.5555 | -0.0380 | Random has lower acceptance. |
| optout_rate | 0.4825 | 0.4445 | +0.0380 | Random has higher opt-out. |
| home_share | 0.4521 | 0.4632 | -0.0111 | Random has lower accepted-home share. |
| meeting_point_uptake_rate | 0.0654 | 0.0923 | -0.0269 | Random has lower meeting-point uptake. |

Arithmetic contribution to the 3930.23 mean profit gap:

- Lower operating/service cost contributes +3667.20 to random relative net profit.
- Better net price revenue contributes +263.03, from +11.10 charge revenue and -251.93 discount cost.
- These two available components account for the full persisted-row net-profit gap: 3667.20 + 263.03 = 3930.23.

## Paired Split Evidence

The random advantage is not uniform, but it is present in 3 of 5 splits:

| Split | random - adaptive net_profit | Interpretation |
|---|---:|---|
| low_seed0 | +5581.18 | Random better. |
| low_seed1 | +7510.95 | Random better. |
| medium_seed0 | -3651.21 | Adaptive better. |
| medium_seed1 | +11527.94 | Random better. |
| medium_seed2 | -1317.73 | Adaptive better. |

This supports Phase 13's blocker framing: the selected evidence does not support a robust positive dominance claim over random.

## Opt-Out and Lost-Demand Accounting

The existing rows preserve opt-out accounting separately from accepted home pickup:

- `count_opted_out` records customers who opted out.
- `count_accepted_home` records accepted home-service choices.
- `count_accepted_meeting_point` records accepted meeting-point choices.

The environment code maintains these separately in `work2_coding/Environments/OOH/Parcelpoint_py.py:257-279`, and only non-opt-out choices mutate routes (`work2_coding/Environments/OOH/Parcelpoint_py.py:284-293`).

However, the persisted formal rows do not include an explicit monetary lost-demand value. The available lost-demand evidence is count/rate based only: random has 24.60 more opt-outs on average, but no row field converts those opt-outs into lost revenue, consumer surplus, or penalty. Phase 15 therefore cannot invent a lost-demand dollar decomposition.

## Service-Cost Effect

The available service-cost field is aggregate:

- `operational_cost`
- `service_time_total`

Both are equal in the selected rows. They do not decompose operating cost by accepted home service versus accepted meeting-point service. The persisted data show that random has 39.20 fewer accepted/served customers and 3667.20 lower service-time cost on average, but they do not prove which service type or route segment caused the cost reduction.

## Price and Discount Effect

The rows contain:

- `charge_revenue`
- `discount_cost`
- `net_price_revenue`

They do not contain customer-level prices, selected-offer price distributions, or discount distributions. The aggregate evidence is still sufficient to show that random's mean price/discount arithmetic is better by 263.03, mostly because it pays 251.93 less discount.

## Fields Unavailable for This Diagnosis

The following fields are unavailable in the selected persisted evidence and are not inferred:

- Explicit lost-demand monetary value.
- Per-customer outside-option utility in historical rows.
- Customer-level chosen price and discount distributions.
- Route-level or service-type-specific operating cost.
- Service-cost decomposition by accepted home versus accepted meeting-point.
- Selected-offer predicted profit, predicted outside probability, and guardrail binding state.
- Generated per-offer time-window values for each selected menu.

## Phase 16 Implication

The weak central claim is not explained away by a metadata-only issue. Based on existing rows, `mainline_optimized_adaptive` appears to buy higher acceptance and meeting-point uptake at a realized cost that exceeds the additional realized revenue. Phase 16 should treat this as a substantive empirical failure mode unless a permitted implementation/configuration diagnosis proves that the selected comparison was not behaviorally valid.
