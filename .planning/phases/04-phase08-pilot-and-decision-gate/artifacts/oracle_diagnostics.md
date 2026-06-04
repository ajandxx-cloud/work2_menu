# Phase08 Oracle Diagnostics

Cost Oracle is an insertion-cost diagnostic. Profit Oracle is a choice-aware expected-profit reference.

| Oracle | Mean service-constrained profit | Mean opt-out | Guardrail violations |
| --- | --- | --- | --- |
| cost_oracle | -5043.628 | 0.352 | 2 |
| profit_oracle | -- | 0.375 | 3 |

## Interpretation
- Cost Oracle should not be treated as the primary profit upper bound.
- Profit Oracle failing to clear Cost-L and CNN-Menu is scenario-design evidence, not proof of the expected-profit heuristic.
