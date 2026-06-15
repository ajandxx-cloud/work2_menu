---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: Work2_TR_E_Service_Menu_Optimization_Final
status: ready_to_plan
last_updated: 2026-06-15T14:41:56.967Z
last_activity: 2026-06-15
progress:
  total_phases: 12
  completed_phases: 7
  total_plans: 12
  completed_plans: 12
  percent: 58
stopped_at: Phase 07 complete (2/2) — ready to discuss Phase 8
---

# State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-06-15)

**Core value:** Produce credible, reproducible TR Part E evidence that
optimized adaptive `m+w+p` service menus improve the profit-service-quality
trade-off under paired RC replay, without overclaiming beyond artifact and
readiness gates.

**Current focus:** Phase 8 — sensitivity and robustness experiments

## Current Position

Phase: 8
Plan: Not started
Status: Ready to plan
Last activity: 2026-06-15

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

Phase 7 scaffold implementation is ready for verification:

```text
$gsd-verify-work 7
```

After Phase 7 verification passes, proceed to Phase 8 sensitivity and
robustness planning without running case-study experiments until upstream gates
pass.

Do not run calibration pilot or final replay until Phase 5 gate cleanup
conditions are explicitly resolved. Do not run semi-real case experiments or
generate case-study result claims until upstream gates pass.

---
*Updated: 2026-06-15 after Phase 7 scaffold-only contract validation*
