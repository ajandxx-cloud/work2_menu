# Work2 Robustness Summary

**Generated:** 2026-06-04T07:18:25Z

## Evidence Contract

- EXP-07 dimensions: menu size, candidate pool size, demand intensity, outside option utility, and cross-instance generalization.
- Public K is meeting-point candidates; public L is displayed meeting points; home is always shown outside L.
- Phase 4 evidence was mixed/inconclusive, so this summary uses conservative conclusion language.

## Outputs

- Standard robustness CSV: `artifacts/work2_cnn_setmenunet/results_snapshot/work2_robustness_rows.csv`
- Diagnostic report: `artifacts/work2_cnn_setmenunet/diagnostics/work2_robustness_diagnostic.md`.

## Dimension Evidence

| Dimension | Status | Rows | Settings | CNN net profit | Cost-L net profit | CNN-Menu net profit | Menu regret | Top-L overlap | Quit rate | Avg walk |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| menu_size | Degraded | 7 | 2, 3, 5 | -5197.413 | -5063.042 | -5093.929 | 36.036 | 1.000 | 0.380 | 1662.674 |
| candidate_pool | Degraded | 6 | 10, 15, 6 | -5197.413 | -5163.568 | -5092.909 | 36.036 | 1.000 | 0.380 | 1662.674 |
| demand | Degraded | 6 | 490, 700, 910 | -5197.413 | -5123.067 | -5093.929 | 36.036 | 1.000 | 0.380 | 1662.674 |
| outside_option | Degraded | 6 | -0.5, 0.0, 0.5 | -5197.413 | -5084.846 | -5092.909 | 36.036 | 1.000 | 0.380 | 1662.674 |
| cross_instance | Conditional/mixed | 4 | Austin | -1635.683 | -1673.845 | -1645.343 | 34.100 | 1.000 | 0.118 | 366.013 |

## Conservative Conclusion

- Phase 6 claim posture: **diagnostic-only claim**.
- Overall wording is no stronger than the weakest material robustness dimension.
- Missing or negative dimensions remain diagnostic evidence; they are not edited into supportive findings.

## Dimension Notes

- **menu_size**: menu_size robustness degrades against core comparators or guardrails.
- **candidate_pool**: candidate_pool robustness degrades against core comparators or guardrails.
- **demand**: demand robustness degrades against core comparators or guardrails.
- **outside_option**: outside_option robustness degrades against core comparators or guardrails.
- **cross_instance**: cross_instance robustness has mixed primary or menu-quality evidence.
  - Mixed or weak dimensions cannot be converted into supportive wording.
