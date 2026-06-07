# Work2 Robustness Diagnostic

**Generated:** 2026-06-04T07:18:25Z

## Incomplete/Degraded/Mixed Dimensions

- **menu_size**: Degraded - menu_size robustness degrades against core comparators or guardrails. Likely cause: menu selection error.
- **candidate_pool**: Degraded - candidate_pool robustness degrades against core comparators or guardrails. Likely cause: candidate-pool scaling.
- **demand**: Degraded - demand robustness degrades against core comparators or guardrails. Likely cause: demand sensitivity.
- **outside_option**: Degraded - outside_option robustness degrades against core comparators or guardrails. Likely cause: outside-option/MNL sensitivity.
- **cross_instance**: Conditional/mixed - cross_instance robustness has mixed primary or menu-quality evidence. Likely cause: instance instability.
  - Mixed or weak dimensions cannot be converted into supportive wording.

## Prediction Error

- unavailable or not implicated by current robustness evidence.

## Ranking/Menu Selection Error

- menu_size: Degraded.

## Demand Sensitivity

- demand: Degraded.

## Outside-Option/MNL Sensitivity

- outside_option: Degraded.

## Instance Instability

- cross_instance: Conditional/mixed.

## Training Budget

- unavailable or not implicated by current robustness evidence.

## Candidate-Pool Scaling

- candidate_pool: Degraded.

## Recommended Next Actions

- Do not manually edit result rows or summary language.
- If missing, run or resume the corresponding robustness member study.
- If degraded or mixed, inspect prediction accuracy, ranking/menu selection, MNL sensitivity, demand setting, instance transfer, and training budget before Phase 6 claims are written.
