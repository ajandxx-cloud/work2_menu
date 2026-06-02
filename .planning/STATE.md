---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
current_phase: 5
status: ready_to_plan
last_updated: 2026-06-02T07:04:15.344Z
progress:
  total_phases: 6
  completed_phases: 4
  total_plans: 8
  completed_plans: 8
  percent: 67
stopped_at: Phase 04 complete (3/3) — ready to discuss Phase 5
---

# Project State: Work2_CNN_SetMenuNet_DRT_Menu_Experiments

**Last Updated:** 2026-06-02  
**Status:** Ready to plan
**Current Phase:** 5
**Next Command:** `$gsd-plan-phase 5`

## Project Reference

See: `.planning/PROJECT.md`

**Core value:** 证明或诚实诊断 CNN-SetMenuNet 是否比传统 CNN-Menu、MLP-Menu、Nearest-L、Cost-L heuristic 等方法更适合 DRT 动态服务菜单设计。

## Current Focus

Phase 5 should use the completed Phase 4 pilot as a robustness and remediation input:

- Keep `K=10` as meeting-point candidates and `L=3` as displayed meeting points
- Treat Phase 4 evidence as mixed/inconclusive rather than supportive of a positive net-profit claim
- Use `artifacts/work2_cnn_setmenunet/diagnostics/work2_main_diagnostic.md` to choose remediation and robustness checks
- Preserve shared request traces, candidate pools, masks, labels, and train/test split semantics where applicable
- Do not manually edit results to create supportive evidence

Phase 4 closeout evidence is captured in `.planning/phases/04-model-comparison-suite/VERIFICATION.md`.

## Active Defaults

- `instance = RC`
- `K = 10`
- `L = 3`
- `home option = always shown`
- `pilot training episodes = 80`
- `pilot test episodes = 20`
- `formal training episodes = 150-300`
- `formal test episodes = 50`
- `seeds = 0,1,2,3,4`

## Guardrails

- Do not modify Work 1 pricing logic without explicit approval.
- Do not modify MNL passenger choice core logic without explicit approval.
- Do not modify HGS/Hygese route-cost evaluation core logic without explicit approval.
- Do not use SPO/SPO+ as the Work 2 main contribution.
- Do not manually alter results to match expected conclusions.

## Verification Status

| Phase | Status | Verification Report |
|-------|--------|---------------------|
| Phase 1 | Passed | `.planning/phases/01-project-baseline-and-boundaries/VERIFICATION.md` |
| Phase 2 | Passed | `.planning/phases/02-smoke-experiment-pipeline/VERIFICATION.md` |
| Phase 3 | Passed | `.planning/phases/03-candidate-feature-and-label-contract/VERIFICATION.md` |
| Phase 4 | Passed with risks | `.planning/phases/04-model-comparison-suite/VERIFICATION.md` |
| Phase 5 | Pending | `.planning/phases/05-robustness-experiments/VERIFICATION.md` |
| Phase 6 | Pending | `.planning/phases/06-formal-results-and-diagnostics/VERIFICATION.md` |

## Notes

- Existing `ooh_code` may contain useful implementations of `CNNSetMenuNet`, `SetMenuNet`, `MLPMenuNet`, menu policies, and study runners.
- Existing `ooh_code` also contains older Work2 candidate-filtering/full-display framing; that framing is not the source of truth for this project.
- Phase 1 completed on 2026-06-01 with `.planning/phases/01-project-baseline-and-boundaries/01-01-SUMMARY.md`.
- Phase 2 completed on 2026-06-01 with `.planning/phases/02-smoke-experiment-pipeline/02-01-SUMMARY.md`.
- Phase 4 completed on 2026-06-02 with mixed/inconclusive pilot evidence and conditional Phase 5 readiness.
