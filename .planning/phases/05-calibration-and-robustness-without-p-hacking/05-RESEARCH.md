---
phase: 05-calibration-and-robustness-without-p-hacking
status: complete
generated: 2026-06-15T15:10:00+08:00
timezone: Asia/Shanghai
runtime_root: work2_coding/
requirements_addressed:
  - CAL-01
  - CAL-02
  - CAL-03
  - CAL-04
---

# Phase 5 Research: Calibration And Robustness Without P-Hacking

## Research Question

What must be known to plan Phase 5 well?

Phase 5 is not an experiment rerun phase by default. It is a process-integrity
phase that makes any future strong empirical claim defensible. Phase 4 found
the selected formal RC run useful diagnostically but not strong-claim-ready:
`mainline_optimized_adaptive` improves several service metrics, but it does not
dominate `mainline_random_menu` on profit and it ties
`mainline_optimized_fixed_window` across tracked metrics. Dirty-git readiness
and artifact/claim gates also block final claim use.

The implementation plan therefore needs to lock a calibration protocol,
restore or explicitly preserve gate status, define pilot/final separation, and
freeze final settings before any final rerun.

## Key Findings

### 1. Gate Cleanup Comes Before Calibration

The current formal readiness report at
`work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
has `status: blocked` and blocker code `dirty_git`, while the checkpoint load
smoke reports `checkpoint_load_status: loaded` and SHA-256
`d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4`.

This means Phase 5 must not treat a calibration pilot as a workaround for
blocked provenance. The first implementation task should re-run or update the
blocker diagnosis and require an explicit human choice before any broad git
cleanup, stash, revert, or commit policy is executed.

### 2. Calibration Must Be Pre-Registered

The allowed knobs from Phase 5 context are mechanism and realism parameters:
`menu_k`, `max_candidates`, ETA filter/threshold settings, opt-out/service
guardrail, and uptake regime. Candidate ranges should be small, explainable,
and justified by operational realism or robustness.

The prohibited behavior is just as important as the allowed behavior:

- no tuning directly on current or future final formal test results;
- no choosing a setting by single profit ranking;
- no deleting seeds, splits, policies, or unfavorable metrics;
- no hand-editing generated rows, figures, tables, or claim guard outputs;
- no treating pilot rows as final evidence.

The protocol should be written to
`.planning/results/CALIBRATION_PROTOCOL.md` before any calibration pilot is
run.

### 3. Pilot And Final Must Be Separate Artifacts

The existing manifests provide the right reference contracts:

- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` is a useful pilot
  pattern with the seven-tag family and pilot checkpoint path.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` is the current
  formal contract with five formal splits and the formal checkpoint path.

Phase 5 should create new calibration/final manifests only if needed. If it
does, the safest naming is explicit, for example:

- `work2_coding/Experiments/studies/calibration_robust_menu.yaml`
- `work2_coding/Experiments/studies/final_robust_menu.yaml`

Both must preserve the seven-tag mainline family, paired replay fields,
normalized-row provenance fields, loaded checkpoint requirement, and
opt-out/home accounting boundaries.

### 4. Frozen Final Settings Are The Main Deliverable Before Rerun

`.planning/results/FROZEN_FINAL_SETTINGS.md` should be the gate between pilot
calibration and final evidence generation. It should record:

- final manifest path and hash;
- policy tags;
- split IDs and seeds;
- checkpoint path and SHA-256;
- paired fields and varied fields;
- chosen calibration knobs and rejected alternatives;
- pilot evidence used for selection;
- readiness, replay, artifact, and claim guard commands;
- the rule that any final failure routes either to one documented second
  calibration round or to conditional paper framing.

The frozen settings document must exist before any final rerun is launched.

## Runtime And Contract Notes

- Active runtime root is `work2_coding/`; stale `ooh_code/` planning maps are
  historical only.
- Formal claim-ready artifact generation requires passed readiness JSON, clean
  git provenance, completed comparable rows, loaded checkpoint provenance,
  dependency snapshot, artifact status `claim_ready`, and `CLAIM_GUARD.json`
  approval.
- Artifact status is currently blocked by missing `method_family` and
  `outside_option_util` in the selected formal rows. Phase 5 can plan fixes or
  manifest/final-rerun requirements, but it must not edit generated rows.
- The no-filter condition remains diagnostic and must not become an operational
  recommendation.
- Attention-based choice or scoring remains out of v1 scope.

## Planning Implications

The phase should be split into two waves:

1. Gate and protocol wave: update blocker diagnosis, write
   `CALIBRATION_PROTOCOL.md`, and add tests that protect prohibited tuning and
   gate ordering.
2. Manifest and freeze wave: create or update calibration/final manifest
   contracts if needed, add manifest/frozen-settings validation helpers, and
   write `FROZEN_FINAL_SETTINGS.md` only after pilot selection rules and final
   settings are locked.

## Research Complete

Phase 5 planning can proceed. The plan should optimize for credible evidence
process, not for improving the observed Phase 4 ranking.
