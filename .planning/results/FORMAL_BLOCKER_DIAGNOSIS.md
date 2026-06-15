---
phase: 03-formal-rc-evidence-pipeline-repair-and-completion
plan: 03-01
status: blocked_diagnostic
created: 2026-06-15T12:00:00+08:00
timezone: Asia/Shanghai
---

# Formal Blocker Diagnosis

## Summary

Formal readiness was rerun from `work2_coding/`:

```powershell
python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/phase5_readiness
```

The command completed its checks but exited blocked because readiness requires
`git_dirty: false` for claim-ready formal evidence.

| Field | Value |
| --- | --- |
| Readiness JSON | `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json` |
| Readiness status | `blocked` |
| Claim-ready allowed | `false` |
| Blocking code | `dirty_git` |
| Current git commit in readiness | `ccc0da39ff35165c49bbc2bd23d00176b54dd215` |
| Formal manifest hash | `4d4648bcbccc604b6fe50fa863286e66cbae021a18c108b7efa06ea40a94a675` |

## Manifest And Policy Contract

`work2_coding/Experiments/studies/formal_robust_menu.yaml` exists and declares
`tier: formal` and `run_mode: formal`.

The formal manifest requires the shared checkpoint:

```text
outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt
```

The seven formal policy tags match `Src.policy_adapters.mainline_policy_tags()`:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

The manifest includes paired fields for seed, trace/runtime settings, checkpoint
path, checkpoint requirement, menu size, candidate count, and utility settings.
It also requires normalized-row metadata including `checkpoint_load_status`,
`checkpoint_path`, `checkpoint_required`, `status`, `execution_status`,
`error_type`, and `error_message`.

Pilot and smoke manifests keep the same seven-tag family and row metadata
contract. The formal manifest differs by formal tier/mode, five formal split
IDs, and the formal shared checkpoint path.

## Checkpoint State

The required checkpoint exists and readiness reports it as loaded.

| Field | Value |
| --- | --- |
| Resolved path | `C:\Users\39583\Desktop\4_Publication\2.paper_2_menu optimization-7分_trE\work2_coding\outputs\shared_training\work2_robust_menu\formal\supervised_ml.pt` |
| SHA-256 | `d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4` |
| Load status | `loaded` |
| Expected status | `loaded` |
| Required | `true` |
| Model type | `DSPO_Menu` / `CNN_2d` module load smoke |
| Sidecar path | `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt.sidecar.json` |
| Dependency snapshot | `work2_coding/outputs/phase5_readiness/formal_robust_menu/DEPENDENCY_SNAPSHOT.json` |

No checkpoint retraining is needed for Phase 3 unless a later validation step
finds that the selected formal run does not match the manifest/checkpoint
provenance.

## Dirty Worktree Categories

Readiness is blocked by dirty git. The current dirty paths include:

| Category | Count | Examples |
| --- | ---: | --- |
| Planning | 57 | `.planning/STATE.md`, `.planning/config.json`, old phase deletions, new Phase 3 plan files |
| Runtime | 23 | robust-menu manifests, `Src/Algorithms/DSPO_Menu.py`, artifact/status/claim modules, focused test scripts |
| Generated artifacts | 0 | None observed in `git status --short` |
| Manuscript/paper | 33 | root `manuscript/` deletions/modifications, `manuscript/els-cas-dc.cls` |
| Unrelated notes or legacy | 5 | Chinese note files and template directory changes |

These changes are not automatically cleaned, reverted, staged, or stashed.

## Focused Preflight Results

All focused checks passed except the readiness claim-ready gate, which is
blocked by dirty git as expected.

| Command | Result |
| --- | --- |
| `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` | `IMPORT_OK` |
| `python scripts/test_formal_readiness.py` | PASS: 4 tests |
| `python scripts/test_formal_replay_enablement.py` | PASS: 4 tests |
| `python scripts/test_checkpoint_provenance.py` | PASS: 6 tests |
| `python scripts/test_policy_fairness_contract.py` | PASS: 15 tests |
| `python scripts/test_paired_replay_contract.py` | PASS: 12 tests |

## Recommended Actions

1. Keep Phase 3 evidence diagnostic until the worktree is intentionally cleaned
   up and readiness is rerun without `dirty_git`.
2. If claim-ready artifacts are needed, ask the user which dirty categories to
   commit, stash, or preserve before making any broad git-state change.
3. Do not use `git reset --hard`, automatic revert, or generated-row edits to
   force readiness.
4. Continue Phase 3 row validation diagnostically, because checkpoint load,
   manifest contract, policy fairness, paired replay, and provenance tests are
   locally coherent.

## Claim Boundary

Formal rows may be validated as candidate evidence, but no claim-ready formal
artifact or manuscript superiority language may be promoted while readiness
reports `status: blocked` and `claim_ready_allowed: false`.
