# Phase08 Pilot Summary

## Run Metadata
- Study: `work2_phase08_pilot`
- Run id: `20260604T124624Z_bf03b88d`
- Manifest hash: `bf03b88d675a048322bc654c3c665fb57d243f42`
- Row source: `C:\Users\39583\Desktop\4_Publication\2.paper_2_menu optimization-7分_trE\ooh_code\outputs\studies\work2_phase08_pilot\20260604T124624Z_bf03b88d\normalized_rows.json`
- Status: `completed`

## Gate Outcome
- Decision state: `recalibrate_objective`
- Pilot complete: `true`
- Human confirmation required: `false`

## Policy Means
| Policy | Mean service-constrained profit | Mean adjusted profit | Mean raw profit | Mean opt-out | Guardrail violations | Max fallback |
| --- | --- | --- | --- | --- | --- | --- |
| nearest_L | -- | -18957.889 | -4967.889 | 0.374 | 3 | 0.000 |
| cost_L | -5042.812 | -18200.781 | -5030.781 | 0.352 | 2 | 0.000 |
| cnn_menu | -- | -18304.957 | -5019.957 | 0.355 | 3 | 0.000 |
| cnn_setmenu_net_current | -- | -19303.289 | -5091.622 | 0.380 | 3 | 0.000 |
| expected_profit_enumeration | -- | -19219.913 | -5088.246 | 0.378 | 3 | 0.000 |
| service_constrained_expected_profit | -- | -18387.102 | -5042.102 | 0.357 | 3 | 0.513 |
| cost_oracle | -5043.628 | -18200.832 | -5030.832 | 0.352 | 2 | 0.000 |
| profit_oracle | -- | -19122.786 | -5102.786 | 0.375 | 3 | 0.000 |

## Reasons
- Service-Constrained Expected-Profit used fallback on at least one seed.
- expected_profit_enumeration violated the quit-rate guardrail.
- expected_profit_enumeration has ineligible service-constrained profit rows.
- service_constrained_expected_profit violated the quit-rate guardrail.
- service_constrained_expected_profit has ineligible service-constrained profit rows.
- Cost-L or CNN-Menu has unavailable service-constrained profit, so the hard comparison gate cannot proceed.
- Profit Oracle did not provide a clear service-constrained reference above Cost-L and CNN-Menu.

## Next Action
Stop and review objective parameters, fallback behavior, and service penalties before formal runtime.
