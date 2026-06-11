---
phase: 06-attention-enhanced-dspo-evidence-pivot
status: passed
verified: 2026-06-11
requirements:
  - ATTN-01
  - ATTN-02
  - ATTN-03
  - ATTN-04
  - BEHAV-01
---

# Phase 06 Verification: Attention-Enhanced DSPO Evidence Pivot

## Result

Status: passed

Phase 6 achieved its goal: `DSPO_original` and `DSPO_attention` are explicit method variants, deterministic candidate attention is integrated into the shared menu objective path, paired replay contracts and normalized rows carry attention identity, and the separate `work2_attention_dspo` artifact family reports paired deltas with a fail-closed claim guard.

The current evidence does **not** support the manuscript claim that attention improves DSPO. The committed smoke run is execution/schema evidence only. `ATTENTION_CLAIM_GUARD.json` correctly reports `attention_improves_dspo_allowed=false` because the evidence is smoke-tier and the primary metric delta is not positive.

## Requirement Traceability

| Requirement | Status | Evidence |
|-------------|--------|----------|
| ATTN-01 | passed | `policy_adapters.py` exposes `DSPO_original` and `DSPO_attention`; attention manifests require exactly those tags for the main comparison. |
| ATTN-02 | passed | `DSPO_Menu.py` adds deterministic attention scoring using existing offer fields/metadata without routing mutation or choice-semantics changes. |
| ATTN-03 | passed | `smoke_attention_dspo.yaml`, `pilot_attention_dspo.yaml`, and `formal_attention_dspo.yaml` use paired fields; row tests verify identical trace IDs and pair IDs. |
| ATTN-04 | passed | `attention_artifacts.py` and `ATTENTION_CLAIM_GUARD.json` report deltas and block unsupported improvement claims. |
| BEHAV-01 | passed | Deterministic attention can alter selected bundles in `test_attention_menu_logic.py`, establishing the attention-based scoring ablation surface. |

## Automated Checks

- `cd work2_coding; python scripts/test_attention_menu_logic.py` -> `PASS: 4 attention menu logic tests`
- `cd work2_coding; python scripts/test_attention_manifest_contracts.py` -> `PASS: 7 attention manifest contract tests`
- `cd work2_coding; python scripts/test_attention_paired_rows.py` -> `PASS: 5 attention paired row tests`
- `cd work2_coding; python scripts/test_attention_artifact_gate.py` -> `PASS: 8 attention artifact gate tests`
- `cd work2_coding; python scripts/test_attention_smoke_execution.py` -> `PASS: 4 attention smoke execution tests`
- `cd work2_coding; python scripts/test_policy_fairness_contract.py` -> `PASS: 11 policy fairness contract tests`
- `cd work2_coding; python scripts/test_paired_replay_contract.py` -> `PASS: 10 paired replay contract tests`
- `cd work2_coding; python scripts/test_experiment_contracts.py` -> `PASS: 12 experiment contract tests`
- `cd work2_coding; python scripts/test_artifact_gates.py` -> `PASS: 7 artifact gate tests`
- `cd work2_coding; python scripts/test_manuscript_claim_guard.py` -> `PASS: 4 manuscript claim guard tests`
- `cd work2_coding; python scripts/run_study.py --study smoke_attention_dspo --contract-only` -> wrote normalized rows
- `cd work2_coding; python scripts/run_study.py --study smoke_attention_dspo --execute --max-policies 2` -> completed actual smoke rows
- `cd work2_coding; python scripts/run_study.py --study pilot_attention_dspo --execute --max-policies 2` -> blocked with missing checkpoint metadata
- `cd work2_coding; python scripts/build_attention_artifacts.py --run-dir outputs/studies/smoke_attention_dspo/smoke_attention_dspo-20260611T105742Z-80ab59ee --allow-incomplete --mirror-root ../artifacts/work2_attention_dspo` -> refreshed mirrored artifacts
- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"` -> `IMPORT_OK`

## Evidence Status

- **Smoke actual run:** `work2_coding/outputs/studies/smoke_attention_dspo/smoke_attention_dspo-20260611T105742Z-80ab59ee`
- **Pilot blocker run:** `work2_coding/outputs/studies/pilot_attention_dspo/pilot_attention_dspo-20260611T105742Z-07415c4f`
- **Attention artifacts:** `work2_coding/artifacts/work2_attention_dspo/` and mirrored `artifacts/work2_attention_dspo/`
- **Claim guard:** `claim_ready=false`, `attention_improves_dspo_allowed=false`
- **Pair completeness:** 1/1 smoke pairs complete
- **Primary metric delta:** `net_objective_proxy_delta_mean = 0.0`

## Blockers And Follow-Up

Pilot/formal empirical evidence is blocked until shared checkpoint provenance is available:

- `outputs/shared_training/work2_attention_dspo/pilot/supervised_ml.pt`
- `outputs/shared_training/work2_attention_dspo/formal/supervised_ml.pt`

Once checkpoint files exist, rerun:

- `cd work2_coding; python scripts/run_study.py --study pilot_attention_dspo --execute`
- `cd work2_coding; python scripts/run_study.py --study formal_attention_dspo --execute`
- `cd work2_coding; python scripts/build_attention_artifacts.py --run-dir <completed-run-dir> --allow-incomplete --mirror-root ../artifacts/work2_attention_dspo`

## Boundaries

Phase 6 implements and verifies the attention-method evidence path, but it does not prove attention superiority. Any paper language must remain at implementation/schema/smoke-evidence level until completed non-placeholder pilot/formal paired evidence with valid checkpoint provenance supports the positive primary metric direction.

## Residual Risks

- Actual smoke uses one tiny trace and produced zero primary delta, so it is not a tuning or effect-size result.
- The broader worktree still contains unrelated pre-existing dirty robust-menu artifacts and local files; Phase 6 ignored unrelated changes.
