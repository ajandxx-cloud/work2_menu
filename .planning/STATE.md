---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: Work2_TR_E_Service_Menu_Optimization_Final
status: executing
last_updated: "2026-06-16T03:18:08.649Z"
last_activity: 2026-06-16
progress:
  total_phases: 12
  completed_phases: 8
  total_plans: 18
  completed_plans: 17
  percent: 67
---

# State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-06-15)

**Core value:** Produce credible, reproducible TR Part E evidence that
optimized adaptive `m+w+p` service menus improve, match, or fail to improve
the profit-service-quality trade-off under paired RC replay, without
overclaiming beyond artifact and readiness gates.

**Current focus:** Phase 09 — exact-versus-greedy-and-computational-tractability

## Current Position

Phase: 09 (exact-versus-greedy-and-computational-tractability) — EXECUTING
Plan: 3 of 3
Status: Ready to execute
Last activity: 2026-06-16

## Initialization Evidence

Runtime root checked from repository root on 2026-06-14:

```powershell
python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"
```

Result: `IMPORT_OK`

Existing runtime files observed:

- `work2_coding/Src/Algorithms/DSPO_Menu.py`
- `work2_coding/scripts/run_study.py`
- `work2_coding/scripts/train_shared_checkpoint.py`
- `work2_coding/scripts/check_formal_readiness.py`
- `work2_coding/scripts/build_artifacts.py`
- `work2_coding/scripts/build_manuscript_frame.py`
- `work2_coding/Experiments/studies/formal_robust_menu.yaml`
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml`
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml`

## Current Notes

- `.planning/codebase/` exists but was generated before the current
  `work2_coding/` runtime was locked. Treat `ooh_code/` references as stale.

- Git status already contains many modified/deleted files outside this
  initialization. Do not revert unrelated user or prior workflow changes.

- The 6.14 discussion says current smoke/pipeline results are not enough for
  TR-E empirical claims. Formal checkpoint, formal replay, and claim guard must
  pass first.

- Attention artifacts and manifests remain V2/diagnostic unless a later phase
  explicitly upgrades them with independent evidence.

- Phase 5 and Phase 7 are conditional. Record `skipped-by-gate` rather than
  executing them mechanically when Phase 4 or Phase 6 makes that appropriate.

- If formal results do not support strong dominance, preserve the fallback path:
  write a conditional service-menu design contribution instead of forcing a
  universal superiority claim.

- Phase 5 completed a process lock, not new empirical evidence. Calibration
  and final manifests exist, but `FROZEN_FINAL_SETTINGS.md` marks final rerun
  `blocked_pending_gate_cleanup` until provenance/readiness/artifact/claim
  gates are resolved.

- Phase 6 approved a semi-real case route with decision
  `approved_blocked_pending_gate_cleanup`. Default to a public OSM/open-network
  reproducibility route; use Yanjiao/Beijing commuting material as narrative
  support unless it can be documented with equal reproducibility.

- Before gate cleanup, Phase 7 may build ingestion/validation scaffolding and
  reproducibility checks only. Do not run semi-real case experiments, generate
  case-study result artifacts, or upgrade manuscript claims.

- Future case-study tables, figures, artifact metadata, and manuscript language
  must label semi-real geography/network, simulated demand, and simulated
  choice. Do not claim real passenger behavior, acceptance, opt-out, or profit.

- Phase 7 produced planning-side contracts and validation only under
  `.planning/data/case_studies/` with status
  `scaffolding_only_blocked_execution`. No runtime case-study YAML, normalized
  rows, case artifacts, external data download, matrix build, replay run, or
  manuscript claim upgrade was created.

- Phase 8 completed the diagnostic must-have sensitivity suite after
  `PHASE8_BASELINE_VALIDATION_STATUS=passed`. It generated 50 completed rows
  across `menu_k`, `eta_filter_mode`, `uptake_regime`, and `guardrail`, plus
  artifacts under
  `work2_coding/artifacts/work2_robust_menu/phase8_sensitivity/` and
  `.planning/results/SENSITIVITY_SUMMARY.md`. Status remains
  `diagnostic_provisional_blocked` with `claim_ready: false`; no abstract or
  conclusion claim upgrade is authorized.

- Phase 8 nice-to-have sensitivity dimensions remain deferred: candidate pool
  size, fleet/capacity stress, pricing bounds, and price sensitivity.

- Timestamps should use ISO-8601 with timezone. Planning timestamps default to
  Beijing time; generated run artifacts may use UTC if their own metadata says
  so.

## Verification Baseline

Minimum checks after implementation phases:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

Expected additional checks as phases implement them:

- `python scripts/test_optout_accounting.py`
- `python scripts/test_robust_menu_logic.py`
- `python scripts/test_menu_runtime_contract.py`
- `python scripts/test_menu_mode_adapters.py`
- `python scripts/test_policy_fairness_contract.py`
- `python scripts/test_paired_replay_contract.py`
- `python scripts/test_artifact_gates.py`
- `python scripts/test_formal_readiness.py`
- `python scripts/test_formal_replay_enablement.py`
- `python scripts/test_study_execution_status.py`

## Next Step

Phase 8 is verified and complete. Phase 9 Plans 09-01 and 09-02 are complete;
execute Phase 9 Plan 09-03 next:

```text
$gsd-execute-phase 9
```

Continue avoiding case-study experiments until upstream gates pass. Phase 9
should focus on exact versus greedy and computational tractability; do not
reinterpret Phase 8 diagnostic sensitivity artifacts as claim-ready evidence.

Do not run calibration pilot or final replay until Phase 5 gate cleanup
conditions are explicitly resolved. Do not run semi-real case experiments or
generate case-study result claims until upstream gates pass.

---
*Updated: 2026-06-15 after Phase 8 diagnostic sensitivity closeout*
