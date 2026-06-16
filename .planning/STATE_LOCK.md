# Repository State Lock

**Phase:** 1 - Repository Audit And State Locking  
**Audit timestamp:** 2026-06-14T23:08:14+08:00  
**Timezone policy:** Planning timestamps use Beijing local time unless a source artifact explicitly states UTC.  
**Scope:** Diagnostic state lock only. No algorithm behavior changes, formal replay, checkpoint training, artifact regeneration, generated-row edits, or manuscript claim upgrades were performed.

## Requirements Covered

- `STATE-01`: `work2_coding/` is confirmed as the active runtime root and the import smoke result is recorded.
- `STATE-02`: Current manifests, policy family, scripts, tests, runtime modules, checkpoints, readiness, artifacts, claim guard, and blockers are inventoried.
- `STATE-03`: Stale `ooh_code/` planning references are mapped to current `work2_coding/` paths where possible or marked obsolete.

## Active Runtime Root

Active runtime root: `work2_coding/`

Verification command run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

Observed output:

```text
IMPORT_OK
```

Core runtime files verified present:

| File | Status |
| --- | --- |
| `work2_coding/Src/config.py` | present |
| `work2_coding/Src/Algorithms/DSPO_Menu.py` | present |
| `work2_coding/Src/paired_replay.py` | present |
| `work2_coding/Src/policy_adapters.py` | present |
| `work2_coding/Src/study_execution.py` | present |
| `work2_coding/Src/formal_readiness.py` | present |
| `work2_coding/Src/artifact_builder.py` | present |
| `work2_coding/Src/artifact_status.py` | present |
| `work2_coding/Src/manuscript_claims.py` | present |

The old planning concern that `ooh_code/Src/Algorithms/DSPO_Menu.py` was missing is obsolete for the active runtime because `work2_coding/Src/Algorithms/DSPO_Menu.py` exists and `Src.config` imports successfully from `work2_coding/`.

## Dirty Worktree Snapshot

Command:

```powershell
git status --short
```

Pre-lock snapshot count: 111 changed paths. This is audit evidence only; Phase 1 did not stage, revert, delete, or clean unrelated files.

| Category | Count | Examples |
| --- | ---: | --- |
| planning | 50 | `.planning/ROADMAP.md`, `.planning/config.json`, deleted older `.planning/phases/*` files |
| runtime | 23 | robust-menu manifests, `DSPO_Menu.py`, `paired_replay.py`, artifact/status/claim modules, script tests |
| manuscript/paper | 33 | root `manuscript/` build/source deletions and edits, `paper/` note edits |
| other notes/templates | 5 | untracked manuscript template directory, local note files |
| outputs/artifacts | 0 | no dirty paths classified directly as generated output/artifact directories in this snapshot |

Important boundary: dirty runtime paths may contain useful prior work, but they are not formal evidence by themselves. Dirty git state is also a blocker for later claim-ready formal readiness until reviewed and resolved by the user.

## Manifest Inventory

Current robust-menu study manifests exist under `work2_coding/Experiments/studies/`:

- `smoke_robust_menu.yaml`
- `pilot_robust_menu.yaml`
- `formal_robust_menu.yaml`

Other current study manifests observed:

- `diagnostic_actual_menu.yaml`
- `formal_attention_dspo.yaml`
- `phase8_baseline_validation.yaml`
- `phase9_dspo_family_validation.yaml`
- `pilot_attention_ablation_eta_feature_focus.yaml`
- `pilot_attention_ablation_shared_eta_stronger.yaml`
- `pilot_attention_ablation_strength_high.yaml`
- `pilot_attention_dspo.yaml`
- `smoke_attention_dspo.yaml`
- `smoke_phase2_service_product_contract.yaml`

Attention manifests remain diagnostic/V2 unless a later phase explicitly upgrades their scope with independent evidence.

## Seven-Tag Mainline Family

The following tags were found in `smoke_robust_menu.yaml`, `pilot_robust_menu.yaml`, `formal_robust_menu.yaml`, and `work2_coding/Src/policy_adapters.py`:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

Current Work2 objective for this milestone is TR-E service-menu optimization around `(meeting point, pickup time window, price)`, not old Akkerman reproduction, not old TR-C DSPO_PLUS ladder planning, and not an attention-main contribution.

## Script Inventory

Key execution/build scripts verified present:

| Script | Status | Phase 1 action |
| --- | --- | --- |
| `work2_coding/scripts/train_shared_checkpoint.py` | present | inventoried only |
| `work2_coding/scripts/check_formal_readiness.py` | present | existing output read; not rerun |
| `work2_coding/scripts/run_study.py` | present | inventoried only |
| `work2_coding/scripts/build_artifacts.py` | present | inventoried only |
| `work2_coding/scripts/build_manuscript_frame.py` | present | inventoried only |

No heavy study, replay, checkpoint training, artifact build, or manuscript-frame build was launched.

## Script-Style Test Inventory

`work2_coding/scripts/` currently contains 30 `test_*.py` scripts. Focused tests relevant to Phase 1 and downstream guardrails are available:

| Audit dimension | Available scripts |
| --- | --- |
| opt-out accounting | `test_optout_accounting.py` |
| robust menu logic and runtime contracts | `test_robust_menu_logic.py`, `test_menu_runtime_contract.py`, `test_menu_mode_adapters.py`, `test_product_time_window_modes.py` |
| paired replay and policy fairness | `test_paired_replay_contract.py`, `test_policy_fairness_contract.py`, `test_smoke_study_rows.py` |
| artifact gates and claim guard | `test_artifact_gates.py`, `test_artifact_builder.py`, `test_manuscript_claim_guard.py`, `test_phase4_artifact_pipeline.py` |
| formal readiness and replay enablement | `test_formal_readiness.py`, `test_formal_replay_enablement.py`, `test_shared_checkpoint_training.py` |
| checkpoint provenance | `test_checkpoint_provenance.py` |
| study execution status | `test_study_execution_status.py` |
| attention diagnostics/V2 | `test_attention_*`, `test_attention_manifest_contracts.py`, `test_attention_paired_rows.py` |

Only the import smoke was executed in Phase 1. Script inventory is diagnostic, not proof that all contracts pass.

## Checkpoint, Readiness, Artifact, And Claim-Guard Status

Formal shared checkpoint path:

| Path | Status | Size | Timestamp |
| --- | --- | ---: | --- |
| `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt` | exists | 4,880,197 bytes | 2026-06-14T11:06:06+08:00 |

Existing readiness/artifact/claim files:

| Path | Status | Key fields |
| --- | --- | --- |
| `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json` | exists | `status: blocked`, `claim_ready_allowed: false`, `checkpoint.load_status: loaded` |
| `work2_coding/outputs/phase4_artifacts/ARTIFACT_STATUS.json` | exists | `artifact_status.status: diagnostic`, `claim_ready: false`, `formal_claim_ready: false`, `pilot_claim_ready: false`, `checkpoint_statuses: [not_requested]`, `row_statuses: [completed]` |
| `work2_coding/outputs/phase4_artifacts/manuscript/CLAIM_GUARD.json` | exists | `artifact_status: diagnostic`, `claim_ready: false`, `formal_claim_ready: false`, `pilot_claim_ready: false` |

Checkpoint load status is separate from checkpoint existence:

- Checkpoint file exists.
- Existing readiness JSON reports `checkpoint_load_status: loaded`, `checkpoint_model_type: DSPO_Menu`, and `checkpoint_compatibility_reason: state_dict loaded`.
- Existing readiness JSON still reports `status: blocked` because claim-ready readiness requires `git_dirty=false`.

Study-output status observed:

- No `work2_coding/outputs/studies/formal_robust_menu/` directory is present.
- Latest `smoke_robust_menu` summaries report `contract_only`.
- Latest `pilot_robust_menu` summaries report `blocked`.

Current evidence therefore supports pipeline/status diagnostics only. It does not support a formal empirical superiority claim for `mainline_optimized_adaptive`.

## Stale Planning Reference Mapping

Historical `.planning/codebase/` files were generated around `ooh_code/` on 2026-06-09. Treat them as architectural memory, not current truth. Current roadmap-relevant mapping:

| Historical reference | Current status |
| --- | --- |
| `ooh_code/` runtime root | Stale root. Use `work2_coding/` as active runtime root. |
| `ooh_code/Src/config.py` | Map to `work2_coding/Src/config.py` |
| `ooh_code/Src/Algorithms/DSPO_Menu.py` missing | Obsolete for active runtime. `work2_coding/Src/Algorithms/DSPO_Menu.py` exists. |
| `ooh_code/Src/Algorithms/*.py` | Map to `work2_coding/Src/Algorithms/*.py` after checking actual file existence. |
| `ooh_code/Src/research_pipeline.py` | Do not assume current. Use current study execution modules under `work2_coding/Src/`, especially `study_execution.py`, plus current script wrappers. |
| `ooh_code/experiments/studies/*.yaml` | Map to `work2_coding/Experiments/studies/*.yaml` with capital `Experiments`. |
| `ooh_code/experiments/suites/*.yaml` | No current Phase 1 dependency confirmed; verify before reuse. |
| `ooh_code/scripts/run_study.py` | Map to `work2_coding/scripts/run_study.py` |
| `ooh_code/scripts/build_artifacts.py` | Map to `work2_coding/scripts/build_artifacts.py` |
| `ooh_code/scripts/build_manuscript.py` | Obsolete name for this plan. Current inventory target is `work2_coding/scripts/build_manuscript_frame.py`. |
| `ooh_code/scripts/test_*.py` | Map to `work2_coding/scripts/test_*.py`; 30 script-style tests currently exist. |
| `ooh_code/outputs/` | Map to `work2_coding/outputs/` |
| `ooh_code/artifacts/` and root `artifacts/work2_cnn_setmenunet/` | Treat as historical artifact locations; verify current artifact builder outputs before using them as evidence. |
| `ooh_code/manuscript/` | Stale for current root-level manuscript edits observed in dirty tree; do not infer current manuscript structure without checking actual paths. |

Do not create or revive an `ooh_code/` runtime root unless a later explicit audit proves it is required.

## Blockers For Formal Claims

These are not Phase 1 failures; they are blockers for later formal empirical claims:

1. `FORMAL_READINESS.json` reports `status: blocked`.
2. Existing readiness metadata says claim-ready readiness requires clean git state, but the repository is dirty.
3. No `work2_coding/outputs/studies/formal_robust_menu/` formal run directory is present.
4. `ARTIFACT_STATUS.json` reports `claim_ready: false`, `formal_claim_ready: false`, and `pilot_claim_ready: false`.
5. `CLAIM_GUARD.json` reports `claim_ready: false`, `formal_claim_ready: false`, and `pilot_claim_ready: false`.
6. Latest pilot robust-menu study summaries are `blocked`.
7. Formal row status is not established from a formal run; existing artifact rows are diagnostic/status evidence only.

## Warnings And Audit Dimensions

Warnings:

- `.planning/codebase/` contains many stale `ooh_code/` references.
- The dirty worktree includes planning deletions, runtime edits, manuscript/paper edits, untracked manuscript template files, and new runtime/test files.
- Local output provenance must be reviewed before any paper claim uses it.
- No-filter evidence remains diagnostic unless later evidence justifies stronger claims.
- Attention artifacts and attention tests are V2/diagnostic for this milestone.

Named scientific audit dimensions to preserve:

- opt-out accounting must remain separate from accepted home pickup;
- paired replay fairness must be preserved across policy comparisons;
- checkpoint load status must be explicit in result metadata;
- artifact readiness and claim guard state must gate manuscript claims;
- paper-facing tables and figures must be generated from rows/artifact builders, not hand-edited.

## Allowed Next Steps

- Use this lock as the baseline for Phase 2 paper-level research design.
- Before formal execution, resolve or intentionally document dirty-git blockers without destructive cleanup.
- Run focused script-style tests only when a later phase needs the corresponding contract.
- Keep formal readiness, replay, artifact generation, and claim diagnosis in their assigned later phases.

## Prohibited Until Later Gates

- Do not claim optimized adaptive `m+w+p` service menus are empirically superior from current evidence.
- Do not use smoke, contract-only, diagnostic, blocked, or placeholder outputs as formal TR-E evidence.
- Do not hand-edit generated result rows, tables, figures, or claim outputs.
- Do not tune on formal test results to force a target ranking.
- Do not merge attention-based choice/scoring into the V1 contribution without a later explicit scope change.
