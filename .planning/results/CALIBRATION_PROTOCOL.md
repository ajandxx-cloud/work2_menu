# Calibration Protocol

**Purpose:** current, non-tuning protocol record for Phase 4 gate evaluation.

This document is derived from the current calibration and final manifests only:

- Calibration manifest: `work2_coding/Experiments/studies/calibration_robust_menu.yaml`
- Calibration manifest SHA-256: `6659DC8AE770C9A857F4B14E2914BD071E8EE7F728BEB41521A802F5D426135E`
- Final manifest: `work2_coding/Experiments/studies/final_robust_menu.yaml`
- Final manifest SHA-256: `77278B816F6CCDFB9E260B5A29F4ED4118F7357690A5D82328D77402AAD29696`

Phase 4 uses this protocol as a diagnostic, non-tuning input. It is not a better ranking, not a final-result selection device, and not permission to alter final settings after observing evidence.

## Allowed Calibration Knobs

The current calibration manifest declares only these pilot calibration knobs:

- `menu_k`: `[2, 3, 4]`
- `max_candidates`: `[8, 10, 12]`
- ETA filter settings: `hard`, `interval_overlap`, and chance-threshold diagnostics `0.20` and `0.25`
- Service or opt-out guardrail threshold values: `0.35` and `0.40`
- Uptake regime coverage through low and medium calibration splits

The final manifest currently records the pre-run selected runtime defaults as:

- `menu_k: 3`
- `max_candidates: 10`
- `menu_eta_filter_mode: interval_overlap`
- `service_quit_rate_guardrail: 0.35`
- `menu_optout_guardrail: 0.35`

These values are recorded from the current manifest surface. They are not selected from final replay outputs.

## Prohibited Tuning Actions

Phase 4 prohibits final-result tuning. The following actions are not allowed:

- seed deletion
- split deletion
- baseline deletion
- metric deletion
- generated-row edits
- single profit ranking as the sole pilot selection rule
- policy-family narrowing after evidence is observed
- changing `menu_k`, `max_candidates`, ETA filter mode, threshold values, service guardrails, opt-out guardrails, price mode, product mode, time-window mode, or menu-construction mode after seeing final evidence
- editing generated rows, tables, figures, package status, package indexes, mirrors, or claim guards by hand

If any blocker can be cleared only through one of these actions, the claim-ready replay path is unavailable for this milestone.

## Pilot Selection Rule

The calibration manifest declares `selection_rule.type: pre_registered_multi_metric`. Its metrics are:

- `net_profit`
- `acceptance_rate`
- `optout_rate`
- `meeting_point_uptake_rate`
- `served_rate`

The rule explicitly forbids single profit ranking and forbids final-result tuning. The calibration surface is pilot-only and cannot be treated as final claim evidence.

## Pilot And Final Separation

The calibration manifest is a `pilot` / `calibration_only` contract using calibration split IDs and seeds. The final manifest is a `formal` / `final_claim_candidate_after_gates` contract using disjoint final split IDs and seeds.

Both manifests preserve the seven policy tags:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

The pilot and final roles stay separate. Phase 4 may use the calibration manifest to document the pre-run calibration surface, but not to tune against final outputs.

## Final Freeze And Rerun Rule

Final replay is authorized only after the current freeze/protocol records, checkpoint provenance, dependency provenance, manifest hash, git provenance, paired replay contract, and formal readiness checks all pass.

If final replay starts after all gates pass and fails, times out, or produces incomplete rows for technical reasons, Phase 4 permits at most one same-settings technical rerun. The rerun must preserve the same final manifest, git SHA, checkpoint path and hash, seeds, split IDs, policy tags, and frozen settings.

## Second-Round Limit

There is no remediation loop in Phase 4. The formal readiness command is run once for the Path A pre-replay gate. If final replay starts after passing gates, only one same-settings technical rerun is allowed. A second final technical failure, timeout, or incomplete-row outcome routes directly to diagnostic lock.

## Downgrade Rule

If readiness is blocked, if final replay is not authorized, if a second same-settings technical replay fails, or if regenerated strict `CLAIM_GUARD.json` remains `claim_ready=false`, Phase 4 locks the conditional service-menu design framing.

That downgrade is an evidence-boundary decision, not a better ranking. The manuscript handoff must describe conditional diagnostic service-menu optimization, paired replay transparency, claim-gated evidence, opt-out/home separation, no-filter diagnostic status, scaffold-only case limits, and blocked exact/greedy credibility.
