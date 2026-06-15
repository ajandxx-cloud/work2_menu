---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: Work2_TR_E_Service_Menu_Optimization_Final
status: verifying
last_updated: "2026-06-15T03:56:15.301Z"
last_activity: 2026-06-15
progress:
  total_phases: 12
  completed_phases: 3
  total_plans: 5
  completed_plans: 5
  percent: 25
---

# State

## Project Reference

See: `.planning/PROJECT.md` (updated 2026-06-14)

**Core value:** Produce credible, reproducible TR Part E evidence that
optimized adaptive `m+w+p` service menus improve the profit-service-quality
trade-off under paired RC replay, without overclaiming beyond artifact and
readiness gates.

**Current focus:** Phase 03 — formal-rc-evidence-pipeline-repair-and-completion

## Current Position

Phase: 03 (formal-rc-evidence-pipeline-repair-and-completion) — EXECUTING
Plan: 3 of 3
Status: Phase complete — ready for verification
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

Phase 3 is planned. Execute the three formal RC evidence pipeline plans:

```text
$gsd-execute-phase 3
```

Use `.planning/STATE_LOCK.md` and
`.planning/paper/TR_E_RESEARCH_DESIGN.md` as the baseline. Preserve the Phase 3
plan boundary: diagnose dirty-git/readiness blockers first, validate or rerun
formal paired rows next, and build artifacts only through readiness and claim
guard gates.

---
*Updated: 2026-06-15 after Phase 3 planning*
