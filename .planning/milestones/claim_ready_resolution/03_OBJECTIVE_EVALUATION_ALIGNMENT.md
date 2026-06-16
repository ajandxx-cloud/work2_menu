# Phase 15 Objective Evaluation Alignment

Date: 2026-06-16

Status: diagnosis only. Phase 15 inspected existing rows, replay metric construction, choice-model code paths, menu objective code paths, and artifact summaries. It did not tune parameters, modify algorithms, regenerate rows, repair gates, regenerate artifacts, or upgrade claims.

## Question

Does the optimized menu objective align with the final replay evaluation metric?

## Evidence Inspected

- `work2_coding/Src/Algorithms/DSPO_Menu.py`
- `work2_coding/Src/study_execution.py`
- `work2_coding/Src/paired_replay.py`
- `work2_coding/Environments/OOH/customerchoice.py`
- `work2_coding/Environments/OOH/Parcelpoint_py.py`
- `work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json`
- `.planning/results/RC_FORMAL_POLICY_SUMMARY.csv`
- `.planning/results/RC_FORMAL_PAIRED_DIFFS.csv`

## Finding

The optimized menu objective may be improving a proxy objective that does not translate into realized replay net profit under the selected formal evidence. This is a diagnosis, not a proof of the complete causal chain, because key predicted-objective diagnostics are not persisted in the formal rows.

The clearest source-bound evidence is that `mainline_optimized_adaptive` serves more customers and reduces opt-outs relative to `mainline_random_menu`, but realizes lower mean net profit because the additional service is associated with higher operating/service cost and higher discount cost. That is compatible with a proxy objective that values acceptance/service probability differently from the final realized profit metric, or estimates route/service cost differently from replay realization.

## Final Replay Metric

The selected formal rows evaluate realized replay profit as:

- `net_price_revenue = charge_revenue - discount_cost`
- `operational_cost = service_time_total`
- `total_cost = service_time_total + discount_cost`
- `net_profit = net_price_revenue - operational_cost`

This metric is constructed after replay choices and route updates in `work2_coding/Src/study_execution.py:307-326` and normalized in `work2_coding/Src/paired_replay.py:516-525`.

The environment tracks opt-out separately from accepted home and meeting-point service in `work2_coding/Environments/OOH/Parcelpoint_py.py:257-279`. Opt-out choices do not mutate routes (`work2_coding/Environments/OOH/Parcelpoint_py.py:284-293`).

## Optimized Menu Objective Path

The optimized policies use the redesigned menu selection path:

- Policy adapter maps optimized policies to `menu_policy=service_guarded_expected_profit`.
- Candidate menus are evaluated in `evaluate_menu(...)` and objective helpers (`work2_coding/Src/Algorithms/DSPO_Menu.py:715-837`).
- The `service_guarded_expected_profit` selector chooses among menus using predicted expected system profit subject to an outside-option guardrail; if no menu satisfies the guardrail, it falls back to minimizing predicted outside probability (`work2_coding/Src/Algorithms/DSPO_Menu.py:1327-1432`).
- Exact menu selection is used for the optimized fixed/adaptive policies in the selected rows.

This objective is not identical to the final realized aggregate replay metric. It is a predicted expectation over candidate menus and choice probabilities before realized stochastic choices and route mutation.

## Choice Model and Realization

The choice code in `work2_coding/Environments/OOH/customerchoice.py:135-186` samples a realized choice from offer utilities plus an outside option. The realized replay row therefore depends on stochastic choice outcomes and subsequent route/service accounting, not only on the expected menu score.

This creates several possible alignment risks:

- The optimizer may select menus with better predicted expected profit but worse realized service-time cost after stochastic replay.
- The optimizer may lower predicted outside probability by offering options that increase realized discount or routing cost.
- The optimizer may estimate service quality or feasibility through candidate-level labels that do not match final replay route mutation costs.
- The outside-option guardrail may improve acceptance while failing to improve net profit if marginal accepted demand is costly.

The selected evidence is consistent with these risks: optimized adaptive has 39.20 more accepted/served customers and 24.60 fewer opt-outs than random on average, but random still has 3930.23 higher mean net profit.

## Price, Discount, and Routing-Cost Alignment

Available aggregate evidence:

| Component | random - adaptive mean difference | Alignment implication |
|---|---:|---|
| charge_revenue | +11.10 | Random has slightly higher realized charge revenue. |
| discount_cost | -251.93 | Optimized adaptive pays more realized discount. |
| net_price_revenue | +263.03 | Price/discount realization favors random. |
| operational_cost | -3667.20 | Optimized adaptive has much higher realized service cost. |
| accepted_count | -39.20 | Optimized adaptive serves more demand. |
| count_opted_out | +24.60 | Optimized adaptive reduces opt-outs. |

The final replay metric rewards net price revenue and penalizes realized service time. The optimized adaptive policy appears to improve service uptake, but not in a way that survives the realized cost accounting.

## ETA, Window Feasibility, and Service-Quality Guardrails

The optimized fixed/adaptive policies use `interval_overlap` filtering and exact menu selection. The random baseline uses `hard` filtering and heuristic random menu selection. This means the random-vs-optimized comparison differs in both menu objective and ETA filtering mode, not only optimization.

For adaptive versus fixed, however, both optimized policies use the same filter and objective. Their equality points to the time-window implementation issue diagnosed in `03_ADAPTIVE_WINDOW_DIAGNOSIS.md`.

The persisted rows do not expose whether the service-quality guardrail was binding on selected menus. They also do not persist selected per-offer ETA/window diagnostics. Phase 15 therefore cannot determine whether guardrails were too loose, too strict, or simply misaligned with realized replay costs.

## Persisted Diagnostic Gaps

The selected rows include realized aggregate outcomes and some menu metadata, but they do not persist enough predicted-objective detail to fully audit objective alignment:

- No selected-menu predicted expected system profit.
- No selected-menu predicted outside probability.
- No persisted guardrail threshold per row.
- No per-offer predicted route cost versus realized route-cost contribution.
- No per-offer selected price/discount distribution.
- No per-offer ETA/window feasibility trace.
- No customer-level outside-option utility in historical rows.

The current code appears to have added some schema fields after the selected run, but Phase 14 already classified the selected historical artifact package as schema-incomplete. Phase 15 does not repair that schema or regenerate rows.

## Diagnosis

The optimization may be improving a proxy objective that does not translate into realized replay net profit. The strongest available evidence is directional:

- Optimized adaptive improves acceptance and reduces opt-out relative to random.
- Optimized adaptive also increases realized discount cost and operating/service cost.
- The cost increase dominates, yielding lower realized net profit.
- The persisted rows do not contain enough predicted-objective diagnostics to prove whether the mismatch is caused by expected-profit scoring, cost estimation, pricing/discount behavior, outside-option accounting, ETA/window filtering, or guardrail behavior.

This blocks claim-ready status. It also identifies a Phase 16 decision input: objective/evaluation alignment may require either an implementation/configuration fix plus legitimate rerun, or a diagnostic manuscript lock if the proxy objective is scientifically intentional but empirically weak.
