---
phase: 03-formal-rc-evidence-pipeline-repair-and-completion
status: complete
generated: 2026-06-15T11:45:00+08:00
timezone: Asia/Shanghai
runtime_root: work2_coding/
requirements_researched:
  - RC-01
  - RC-02
  - RC-03
  - RC-04
  - RC-05
---

# Phase 3 Research: Formal RC Evidence Pipeline

## RESEARCH COMPLETE

Phase 3 should be planned as a gate-preserving formal evidence pipeline, not as
a result-claiming phase. The repository already contains the main execution
surface for the formal RC benchmark: the `formal_robust_menu` manifest, shared
checkpoint path, readiness checker, study runner, artifact builder, manuscript
frame builder, and focused script-style tests. The current blockers are mostly
provenance and gate status, not absence of the formal run machinery.

## Current Evidence Position

The active runtime root is `work2_coding/`. Phase 1 locked this as the current
runtime, and the import baseline is:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

`work2_coding/Experiments/studies/formal_robust_menu.yaml` defines the formal
seven-tag mainline family:

- `mainline_no_menu`
- `mainline_fixed_menu`
- `mainline_random_menu`
- `mainline_optimized_m`
- `mainline_optimized_mw`
- `mainline_optimized_fixed_window`
- `mainline_optimized_adaptive`

It uses five formal splits across low and medium uptake regimes and requires
the shared checkpoint at
`outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt` with
expected status `loaded`.

Existing readiness evidence at
`work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
reports:

- `status: blocked`
- `claim_ready_allowed: false`
- `checkpoint.load_status: loaded`
- `checkpoint.hash: d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4`
- blocker code `dirty_git`

The latest completed formal run observed is:

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a
```

Its `study_summary.json` reports 35 rows, all seven policy tags, five split
IDs, `execution_status: completed`, `checkpoint_statuses: [loaded]`, and
`git_dirty: true`. It is a candidate formal evidence input, but not
claim-ready while readiness and artifact gates remain blocked.

The prior failed run remains useful diagnostic evidence:

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T031927Z-fca35a73
```

It has 35 rows with seven failed rows and blocker code
`actual_replay_failed_rows` caused by `UnboundLocalError`. Phase 3 should keep
this failure trail visible instead of hiding it.

Existing artifact and claim outputs under `outputs/phase4_artifacts/` are
diagnostic. `ARTIFACT_STATUS.json` is based on a smoke source run, reports
`claim_ready: false`, and `CLAIM_GUARD.json` blocks empirical superiority
claims. These are useful gate examples, not formal final artifacts.

## Implementation Surface

Primary files and responsibilities:

- `work2_coding/Experiments/studies/formal_robust_menu.yaml` defines formal
  split, policy, paired-field, checkpoint, and normalized-row contracts.
- `work2_coding/Src/formal_readiness.py` checks dirty git, checkpoint presence,
  checkpoint load smoke, checkpoint hash, dependency snapshot, and readiness
  status.
- `work2_coding/scripts/check_formal_readiness.py` exposes the readiness CLI.
- `work2_coding/Src/study_execution.py` builds completed, failed, blocked, or
  placeholder rows with checkpoint and git provenance.
- `work2_coding/scripts/run_study.py` writes `study_summary.json`,
  `normalized_rows.json`, `normalized_rows.csv`, and `blockers.json` where
  relevant.
- `work2_coding/Src/paired_replay.py` resolves paired settings, trace identity,
  settings hashes, checkpoint metadata, and normalized row fields.
- `work2_coding/Src/policy_adapters.py` defines the mainline policy family and
  limits policy-only drift.
- `work2_coding/Src/artifact_status.py` classifies artifacts and validates
  formal claim-ready runs against passed readiness JSON.
- `work2_coding/Src/artifact_builder.py` builds aggregate tables, figures,
  artifact status, provenance metadata, and formal readiness links.
- `work2_coding/Src/manuscript_claims.py` generates `CLAIM_GUARD.json` and
  keeps unsupported empirical claims out of positive manuscript language.

Focused tests already exist for the Phase 3 gates:

- `scripts/test_optout_accounting.py`
- `scripts/test_paired_replay_contract.py`
- `scripts/test_policy_fairness_contract.py`
- `scripts/test_checkpoint_provenance.py`
- `scripts/test_artifact_gates.py`
- `scripts/test_formal_readiness.py`
- `scripts/test_formal_replay_enablement.py`
- `scripts/test_study_execution_status.py`

## Planning Implications

1. Start with a non-destructive dirty-git and formal-readiness diagnosis. If
   dirty git blocks claim readiness, produce
   `.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md` before asking the user to
   clean, commit, or stash anything.
2. Reuse the existing checkpoint only if its path, hash, and load status remain
   explicit in readiness and row metadata. Retrain only if the checkpoint is
   missing, incompatible, or provenance is unusable.
3. Validate the latest completed formal run first. Rerun formal replay only if
   the candidate run fails manifest, row, status, checkpoint, paired replay, or
   artifact-source checks.
4. If replay fails, preserve failed rows with `status`, `execution_status`,
   `error_type`, and `error_message`, then write
   `.planning/results/FORMAL_FAILURE_DIAGNOSIS.md`.
5. Generate claim-ready artifacts only when readiness passes and the formal
   source run matches readiness manifest/checkpoint/dependency provenance. When
   gates do not pass, build diagnostic artifacts with explicit status and keep
   empirical superiority claims blocked.
6. Phase 3 succeeds when formal replay rows are complete and comparable across
   the seven-tag family. Claim diagnosis and claim strength classification are
   Phase 4 work.
