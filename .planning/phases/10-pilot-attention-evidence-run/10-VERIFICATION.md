# Phase 10 Verification

**Status:** Passed execution/artifact requirements; claim failed/not supported
**Date:** 2026-06-11

## Commands

| Check | Command | Result |
|---|---|---|
| Pre-run cleanliness | `git status --short` | PASS: clean before pilot run |
| Pilot actual replay | `cd work2_coding; python scripts/run_study.py --study pilot_attention_dspo --execute` | PASS: completed run `pilot_attention_dspo-20260611T140616Z-07415c4f` |
| Rebuild artifacts | `cd work2_coding; python scripts/build_attention_artifacts.py --study pilot_attention_dspo --allow-incomplete --default-mirror` | PASS: artifacts and mirror rebuilt |
| Attention artifact gate tests | `cd work2_coding; python scripts/test_attention_artifact_gate.py` | PASS: 8 tests |
| Study execution status tests | `cd work2_coding; python scripts/test_study_execution_status.py` | PASS: 7 tests |
| Shared checkpoint training tests | `cd work2_coding; python scripts/test_shared_checkpoint_training.py` | PASS: 1 test |
| Attention smoke execution tests | `cd work2_coding; python scripts/test_attention_smoke_execution.py` | PASS: 4 tests |

## Artifact Outputs

Rebuilt:
- `work2_coding/artifacts/work2_attention_dspo/`
- `artifacts/work2_attention_dspo/`

Key files:
- `ATTENTION_CLAIM_GUARD.json`
- `ARTIFACT_STATUS.json`
- `PAIR_COMPLETENESS.json`
- `paired_deltas/attention_delta_summary.json`
- `paired_deltas/attention_pair_deltas.csv`
- `paired_deltas/attention_pair_deltas.json`
- `tables/attention_pair_deltas.tex`

## Requirement Evidence

| Requirement | Evidence | Status |
|---|---|---|
| PILOT-01 | Pilot run completed with `placeholder_only=false` and `checkpoint_statuses=["loaded"]`. | Passed |
| PILOT-02 | Claim guard reports `pair_count=2`, `complete_pair_count=2`, `all_pairs_complete=true`. | Passed |
| PILOT-03 | Low and medium regimes are present; acceptance and opt-out are non-degenerate. Limitation: meeting-point uptake is zero and deltas are zero. | Limited pass |
| PILOT-04 | Attention artifacts and claim guard rebuilt from completed run. | Passed |
| PILOT-05 | `10-PILOT-SUMMARY.md` reports primary/secondary deltas, attention weights, checkpoint provenance, and regime rows. | Passed |
| PILOT-06 | `10-GO-NOGO.md` records a NO-GO decision. | Passed |

## Claim Verification

The claim failed:

```text
attention_improves_dspo_allowed = false
blocker = primary_metric_not_positive
net_objective_proxy_delta_mean = 0.0
```

This is not a soft positive result. It is a no-go for the current attention design.

