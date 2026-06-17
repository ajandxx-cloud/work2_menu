# M3 Claim-Ready Decision

**Phase:** 03 - Claim-Ready Evidence Decision Gate
**Created:** 2026-06-17
**Requirements addressed:** GATE-03, GATE-04
**Current status:** `blocked_pending_gate_cleanup`

## Current Decision

The current Work2 final replay path is `blocked_pending_gate_cleanup`.
Immediate final replay is not authorized.

This is a conditional go-after-gates decision. Phase 3 does not permanently
reject a future claim-ready replay by itself, because the current blocker is
missing freeze/protocol and provenance evidence rather than a completed final
evidence result. Phase 4 may pursue approved gate cleanup and readiness work,
but final replay may start only after all pre-replay gates in this document
pass from the current manifests and current filesystem state.

If those gates do not pass, Phase 4 must lock the paper as conditional
diagnostic without running final replay.

## Evidence Basis

This decision is based on read-only inspection of the current regenerated GSD
planning state, prior M1/M2 milestone deliverables, current calibration and
final candidate manifests, and current generated Phase 10 package status.

Primary evidence inputs:

- `.planning/milestones/tr_e_completion/M1_DECISION.md`
- `.planning/milestones/tr_e_completion/M2_GATE_CLEANUP_PLAN.md`
- `.planning/milestones/tr_e_completion/M2_PROVENANCE_REQUIREMENTS.md`
- `.planning/milestones/tr_e_completion/M2_USER_ACTIONS_REQUIRED.md`
- `work2_coding/Experiments/studies/calibration_robust_menu.yaml`
- `work2_coding/Experiments/studies/final_robust_menu.yaml`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`

No calibration, final replay, formal readiness, checkpoint training, artifact
builder, Phase 10 package builder, mirror replacement, case-study execution,
or manuscript claim upgrade was run for this decision.

## Freeze And Protocol Status

The current candidate manifests reference freeze/protocol artifacts that are
absent from the active regenerated planning state:

- `.planning/results/CALIBRATION_PROTOCOL.md`
- `.planning/results/FROZEN_FINAL_SETTINGS.md`

Their absence blocks immediate final replay authorization. It does not, by
itself, permanently force a diagnostic no-go, because a later approved Phase 4
cleanup may establish the missing freeze/protocol evidence from the current
manifests and current filesystem state.

Phase 3 does not create `.planning/results/FROZEN_FINAL_SETTINGS.md` and does
not create `.planning/results/CALIBRATION_PROTOCOL.md`. The blocked
freeze/protocol finding is recorded only in this
`M3_CLAIM_READY_DECISION.md` file.

Later gap closure must not restore, mine, or cite git-history versions of old
freeze/protocol files as Phase 3 replay authorization. Any later freeze or
calibration protocol record must be created from current approved inputs and
must remain non-tuning: it may not select settings from final replay outputs.

## Manifest Authorization Status

`work2_coding/Experiments/studies/calibration_robust_menu.yaml` exists and is
a `pilot` / `calibration_only` manifest. It preserves a calibration surface for
menu size, candidate count, ETA filter settings, threshold settings, and
service/opt-out guardrails, and it references
`.planning/results/CALIBRATION_PROTOCOL.md`.

`work2_coding/Experiments/studies/final_robust_menu.yaml` exists and is a
`formal` / `final_claim_candidate_after_gates` manifest. It preserves the
seven mainline policy tags and a candidate final replay surface, and it
references both `.planning/results/CALIBRATION_PROTOCOL.md` and
`.planning/results/FROZEN_FINAL_SETTINGS.md`.

The final manifest field
`selected_runtime_knobs.source: CALIBRATION_PROTOCOL.md pre-run default; not
selected from final rows` is an unverified statement while
`CALIBRATION_PROTOCOL.md` is absent. It records intended provenance, not replay
authorization.

Therefore, the manifests are candidate contracts after gates. They are not
current permission to run final replay.

## Manifest Contract Status

Command run from `work2_coding/`:

```powershell
python scripts/test_calibration_manifests.py
```

Result:

```text
PASS: 5 calibration manifest tests
```

The passing test inspects the current calibration and final manifests without
running calibration or replay. It checks that both manifests preserve the seven
mainline policy tags:

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

It also checks that calibration and final splits are disjoint; that paired
fields include seed, data seed, runtime instance, checkpoint path/requirement,
`menu_k`, `max_candidates`, HGS timing, and utility parameters; that varied
fields include policy behavior fields such as menu policy, product mode,
time-window mode, menu contract mode, pricing mode, ETA-filter mode, objective
mode, and service/opt-out guardrails; and that output schema fields preserve
checkpoint provenance and separate accounting for `count_opted_out`,
`count_accepted_home`, and `count_accepted_meeting_point`.

The relevant contract names are `paired fields` and `varied fields`; both are
part of the replay fairness boundary.

This passing manifest test supports treating the manifests as candidate
contracts after gates. It does not authorize final replay, because the
freeze/protocol, checkpoint, dependency, clean provenance, readiness, row, and
artifact gates still have to pass first.
