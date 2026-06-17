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

## Required Pre-Replay Gates

Final replay is authorized only if all gates below pass before replay starts.
The gates must be checked against the current manifests and current filesystem
state, not restored legacy planning files.

| Gate | Required evidence before replay |
| --- | --- |
| Freeze/protocol evidence | A current, approved calibration protocol and frozen-final settings record that were not selected from final replay outputs. |
| Clean or claim-eligible git provenance | `git_sha` is recorded and the claim-supporting tree has `git_dirty=false`, unless a later approved protocol explicitly marks the run diagnostic-only. |
| Checkpoint provenance | `checkpoint_manifest_path`, `checkpoint_resolved_path`, `checkpoint_sha256`, `checkpoint_sidecar_path`, `checkpoint_sidecar_sha256`, and `checkpoint_load_status=loaded` are recorded. |
| Dependency provenance | `dependency_snapshot_path` and `dependency_snapshot_sha256` are recorded from the same readiness/evidence chain. |
| Final manifest stability | Final manifest path and manifest hash are recorded before replay; the manifest is not changed after seeing final outputs. |
| Policy family | The seven mainline policy tags remain present: no-menu, fixed-menu, random-menu, optimized-m, optimized-mw, optimized-fixed-window, and optimized-adaptive. |
| Split and seed freeze | Final split IDs, seeds, data seeds, and data-test seeds are fixed before replay. |
| Paired/varied fields | Paired fields and varied fields validate through the manifest contract without result-affecting drift. |
| Source-row checkpoint metadata | Source rows include checkpoint hashes and source-row checkpoint load statuses, with required formal rows all reporting `loaded`. |
| Readiness JSON | `readiness_json_path` and `readiness_json_sha256` are recorded, and readiness status supports claim use. |
| Generated artifact authority | Generated artifact gates and regenerated strict `CLAIM_GUARD.json` decide final claim readiness. |

Formal readiness and artifact classification must fail closed on dirty git,
missing or unloaded checkpoints, missing sidecar/hash evidence, dependency
snapshot gaps, manifest-hash mismatch, placeholder rows, blocked/failed rows,
incomplete rows, invalid opt-out/home/meeting-point accounting, no-filter-only
diagnostics, and all-diagnostic policy sets.

## Approved Phase 4 Cleanup Boundary

If Phase 4 pursues Path A, approved cleanup before final replay may repair only
the evidence chain around the candidate manifests:

- path normalization for current manifest, checkpoint, readiness, dependency,
  and artifact inputs;
- metadata sidecars and sidecar hashes;
- recomputed checkpoint, sidecar, dependency snapshot, readiness JSON, and
  manifest hashes;
- checkpoint load-status reporting;
- dependency snapshot records;
- readiness metadata;
- source-row evidence-chain records created by approved replay, not by manual
  row edits;
- documentation that links generated gate outputs to the strict claim guard.

These repairs may make provenance auditable. They must not change what the
final replay is trying to measure.

## Forbidden Phase 4 Cleanup

Phase 4 cleanup must not alter result-affecting runtime settings or empirical
comparison definitions after seeing current or final evidence. Forbidden
cleanup includes changes to:

- policy family or required policy tags;
- split IDs, seeds, data seeds, or test seeds;
- metrics, objective reporting, or acceptance/accounting definitions;
- `menu_k`;
- `max_candidates`;
- ETA filter mode;
- menu exact/greedy thresholds when those thresholds affect final evidence;
- service guardrails, opt-out guardrails, or outside-option handling;
- checkpoint policy, checkpoint path, or mismatch policy except as approved
  provenance repair before replay;
- price model, product mode, time-window mode, menu-contract mode, or pricing
  mode;
- row deletion, failed-row deletion, blocked-row deletion, or generated-row
  edits;
- artifact status, package status, figure/table data, package indexes, root
  mirrors, or claim guards by hand.

If fixing a blocker requires any forbidden cleanup, the claim-ready final
replay path is not available for this milestone and Phase 4 must lock the
diagnostic path.

## Claim-By-Claim Classification

Strict `CLAIM_GUARD.json` is the authority for manuscript claims. Claim
classification is local to each claim ID. One passing claim cannot upgrade
unrelated blocked claims or convert the whole paper into a claim-ready
empirical manuscript.

| Claim ID | Current claim_ready | Current manuscript_allowed | Allowed Phase 5 use |
| --- | --- | --- | --- |
| `C1_central_adaptive_menu_superiority` | false | false | Not allowed. Do not state central adaptive-menu superiority or universal dominance. |
| `C2_product_ablation_value` | false | false | Not allowed as a positive claim; use only as diagnostic structure if the manuscript labels the blocker. |
| `C3_adaptive_window_increment` | false | false | Not allowed. Do not claim adaptive windows improve outcomes. |
| `C4_menu_construction_value` | false | false | Not allowed as a positive claim; discuss only as an auditable mechanism with blocked/diagnostic status. |
| `C5_eta_robustness_boundary` | false | true | Diagnostic boundary content only, with no-filter kept diagnostic and not operationally recommended. |
| `C6_exact_greedy_computational_credibility` | false | false | Not allowed as computational credibility; exact/greedy material remains diagnostic computational boundary evidence. |
| `C7_provenance_status_transparency` | true | true | Allowed as provenance/status transparency only; it does not prove empirical effectiveness. |
| `C8_semi_real_case_validation` | false | false | Not allowed; case-study materials remain scaffold-only/future-work context. |

## Current Claim Ceiling

The current strict package has `claim_ready=false`,
`strict_claim_guard_claim_ready=false`, and
`manuscript_positive_claims_allowed=false`. The package indexes 74 artifacts,
70 existing artifacts, 4 missing expected-pattern artifacts, and 108 blockers.

Only `C7_provenance_status_transparency` is currently claim-ready.
`C5_eta_robustness_boundary` is `manuscript_allowed=true` only as diagnostic
boundary material. All blocked positive claims remain forbidden unless a later
authorized replay and regenerated strict claim guard change the exact claim ID
status.

Current Phase 8, Phase 9, no-filter, and case-scaffold materials may be used
only as diagnostic boundary, computational diagnostic, appendix, status, or
future-work material. They do not support positive main claims.

If `C1_central_adaptive_menu_superiority` remains blocked but some local
mechanism or boundary claim later passes, the paper must be classified as
conditional regime-specific, not central adaptive-menu superiority.

## Manuscript Handoff Rule

If overall `claim_ready=false` after any authorized replay, Phase 5 may use
only claim-specific material with `manuscript_allowed=true`, and every such
use must include:

1. claim ID;
2. claim status;
3. source artifact path;
4. allowed manuscript use;
5. a label distinguishing generated evidence, diagnostic evidence, blocked
   status, scaffold-only material, or conceptual illustration.

Phase 5 must not use positive language such as "dominates", "outperforms",
"superior", "near-optimal", "adaptive windows improve", "case-study
validation", or "real passenger behavior" unless regenerated strict
`CLAIM_GUARD.json` authorizes that exact claim.

## Phase 4 Routing

Phase 4 must choose between a gated Path A and diagnostic-lock Path B based on
pre-replay gates and generated evidence outcomes.

Path A is allowed only as approved gate cleanup/readiness work first, followed
by final replay only after all pre-replay gates pass. The authorized replay
input is the current final candidate manifest after gate cleanup, not a
retuned or narrowed manifest.

Path B is required when pre-replay gates fail, when a second same-settings
technical replay attempt fails, or when completed regenerated evidence keeps
overall `claim_ready=false` and does not authorize the needed manuscript
claims.

## Pre-Replay Gate Failure

If any required pre-replay gate fails, Phase 4 must lock the diagnostic path
without running final replay. Gate failure is not permission to probe final
results, reduce scale, remove baselines, edit generated rows, or alter
result-affecting runtime settings.

Diagnostic lock should preserve the current evidence boundary and route Phase
5 toward conditional diagnostic TR-E writing.

## First Final Replay Technical Failure

If all pre-replay gates pass and final replay starts, but the run fails, times
out, or emits incomplete rows for technical reasons, Phase 4 may allow at most
one technical rerun.

That rerun must use the same manifest, git SHA, checkpoint path/hash, seeds, splits, policy tags, and frozen settings.
It may repair only runtime failure, environment interruption, or
non-result-affecting execution plumbing.

The rerun must not change policy family, split IDs, seeds, metrics,
checkpoint policy, frozen runtime knobs, or row inclusion rules.

## Second Final Replay Failure

If the second final replay attempt still fails, times out, or emits incomplete
rows, Phase 4 must lock the diagnostic path immediately.

It must not reduce scale, delete failed rows, delete blocked rows, rerun
again, replace baselines, or continue tuning. A second technical failure means
the claim-ready replay path is not available for this milestone.

## Completed Replay With claim_ready=false

If final replay technically completes but regenerated strict `CLAIM_GUARD.json`
or generated artifact gates still report `claim_ready=false`, that result is
evidence. Phase 4 and Phase 5 must proceed with a diagnostic or conditional
manuscript path and do not tune the manifest.

The project may still use claim-specific `manuscript_allowed=true` content
under the manuscript handoff rule, but it must not upgrade central adaptive
menu superiority or any other blocked positive claim.
