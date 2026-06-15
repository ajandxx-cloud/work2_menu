---
phase: 05-calibration-and-robustness-without-p-hacking
status: ready
generated: 2026-06-15T15:10:00+08:00
timezone: Asia/Shanghai
validation_type: process-integrity
---

# Phase 5 Validation Strategy

## Critical Assumptions To Validate

1. Calibration protocol exists before any calibration pilot or final rerun.
2. Provenance/readiness blockers are surfaced before calibration proceeds.
3. Pilot and final manifests, if created, use distinct split IDs, output roots,
   run modes, and checkpoint paths.
4. The seven-tag family remains intact across pilot/final contracts.
5. Final settings are frozen before final evidence generation.
6. Generated rows, artifact tables, figures, and claim guard JSON are never
   hand-edited to improve rankings.

## Required Checks

Run from `work2_coding/` after implementation:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_formal_readiness.py
python scripts/test_artifact_gates.py
python scripts/test_policy_fairness_contract.py
python scripts/test_paired_replay_contract.py
python scripts/test_checkpoint_provenance.py
python scripts/test_calibration_protocol.py
python scripts/test_calibration_manifests.py
```

If the implementation does not add the last two test scripts, it must document
the equivalent existing script-style checks and why they cover the same
contracts.

## Manual Audit

- `CALIBRATION_PROTOCOL.md` contains allowed knobs, prohibited tuning behavior,
  pilot selection rules, second-round limits, and pilot/final separation.
- `FROZEN_FINAL_SETTINGS.md` contains final manifest hash, policy tags, split
  IDs/seeds, checkpoint path/hash, paired/varied fields, runtime knobs, and gate
  commands.
- The plan does not instruct an executor to clean, revert, stash, or commit
  unrelated dirty worktree paths without explicit user approval.
- Pilot rows are labeled calibration evidence only, not final claim evidence.
- If final evidence fails again, the protocol downgrades to conditional
  service-menu framing after at most one justified second calibration round.
