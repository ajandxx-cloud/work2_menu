---
phase: 3
phase_name: Mainline Comparison Contract
status: complete
completed: 2026-06-14
evidence:
  - .planning/phases/03-mainline-comparison-contract/03-VERIFICATION.md
---

# Phase 3 Summary: Mainline Comparison Contract

Phase 3 completed the V1 mainline comparison contract for `work2_robust_menu`.

## Result

- The smoke, pilot, and formal manifests were migrated to the seven-tag mainline
  family.
- Smoke and pilot cover `menu_k={1,2,3,5}`.
- Formal fixes `menu_k=3`, includes at least five paired splits, and requires
  checkpoint provenance.
- Row, paired fairness, failed-row, and artifact eligibility tests passed.
- Actual smoke replay completed 28 rows covering all seven mainline policy tags.

## Verification

See `.planning/phases/03-mainline-comparison-contract/03-VERIFICATION.md` for
the full command list, output path, row counts, policy coverage, and scope
guardrails.
