# Phase 11 Ablation Preregistration

**Registered before execution:** 2026-06-11

## Candidate Set

| Manifest | Design | Policy-specific varied fields |
|---|---|---|
| `pilot_attention_ablation_strength_high` | Increase attention strength to test whether the score perturbation is too weak. | `method_variant`, `attention_enabled`, `attention_mode`, `attention_strength` |
| `pilot_attention_ablation_eta_feature_focus` | Focus attention weights on ETA risk and remove other feature weights. | `method_variant`, `attention_enabled`, `attention_mode`, `attention_strength`, attention weight fields |
| `pilot_attention_ablation_shared_eta_stronger` | Use a shared stronger ETA variant for both policies, then compare original vs attention under that shared condition. | `method_variant`, `attention_enabled`, `attention_mode`, `attention_strength` |

## Selection Criteria

A candidate can be selected for formal only if all are true:

1. The run completes with non-placeholder rows.
2. All rows have `checkpoint_load_status=loaded`.
3. Every pair contains both `DSPO_original` and `DSPO_attention`.
4. Low and medium regimes are present.
5. `net_objective_proxy_delta_mean > 0.0`.
6. Service constraints pass:
   - acceptance rate is not materially lower.
   - opt-out rate is not materially higher.
   - meeting-point uptake is not materially lower.
   - service time is not materially higher.

Decision rule:
- If exactly one candidate passes, select it as the formal candidate.
- If zero candidates pass, stop the superiority claim.
- If multiple candidates pass, do not cherry-pick; stop and require a separate pre-registered tie-break phase.

## Claim Rule

No formal attention-improves-DSPO claim may proceed unless the selected candidate satisfies the criteria above.

