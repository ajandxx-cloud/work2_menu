# Phase08 Profit Versus Quit Tradeoff

Raw profit is diagnostic only; the gate uses service-constrained profit and quit-rate eligibility.

| Policy | Raw profit | Adjusted profit | Service-constrained profit | Opt-out | Eligible |
| --- | --- | --- | --- | --- | --- |
| nearest_L | -4967.889 | -18957.889 | -- | 0.374 | no |
| cost_L | -5030.781 | -18200.781 | -5042.812 | 0.352 | no |
| cnn_menu | -5019.957 | -18304.957 | -- | 0.355 | no |
| cnn_setmenu_net_current | -5091.622 | -19303.289 | -- | 0.380 | no |
| expected_profit_enumeration | -5088.246 | -19219.913 | -- | 0.378 | no |
| service_constrained_expected_profit | -5042.102 | -18387.102 | -- | 0.357 | no |
| cost_oracle | -5030.832 | -18200.832 | -5043.628 | 0.352 | no |
| profit_oracle | -5102.786 | -19122.786 | -- | 0.375 | no |

## Guardrail
- Quit-rate guardrail: `0.400`
- Policies exceeding the guardrail are ineligible for proceed-to-formal decisions.
