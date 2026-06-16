---
status: locked_pending_gate_cleanup
phase: 05-calibration-and-robustness-without-p-hacking
created: 2026-06-15T16:35:00+08:00
timezone: Asia/Shanghai
source_evidence:
  - .planning/results/RC_FORMAL_DIAGNOSIS.md
  - .planning/results/FORMAL_BLOCKER_DIAGNOSIS.md
  - work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json
requirements:
  - CAL-01
  - CAL-04
---

# Calibration Protocol

## Status And Source Evidence

Phase 4 found the selected formal RC run diagnostic but not claim-ready. The
run has 35 comparable rows across five paired splits and seven mainline policy
tags, with checkpoint load status `loaded`, but it does not support a strong
universal dominance claim for `mainline_optimized_adaptive`.

Current gates remain blocked:

- Formal readiness: `blocked` by `dirty_git`.
- Artifact status: `blocked` because pilot/formal rows require generated
  `method_family` and `outside_option_util` metadata.
- Claim guard: `claim_ready: false` and `formal_claim_ready: false`.

The selected formal result is non-tuning input. It identifies failure modes and
gate blockers, but it must not be used to select parameter values, remove
unfavorable cases, or upgrade manuscript claims.

Phase 5 success is process integrity: clean gate visibility, a locked protocol,
strict pilot/final separation, and frozen settings before any final rerun. It
is not a better ranking.

## Allowed Calibration Knobs

Allowed calibration changes must have a realism or robustness rationale and
must be pre-registered before pilot execution.

| Knob | Candidate Range | Rationale |
| --- | --- | --- |
| `menu_k` | `2`, `3`, `4` | Tests display-size sensitivity while keeping menus operationally plausible. |
| `max_candidates` | `8`, `10`, `12` | Tests candidate-pool breadth without open-ended search. |
| ETA filter mode/threshold | `hard`; `interval_overlap`; chance threshold `0.20`, `0.25` | Tests ETA robustness and feasibility discipline. |
| Service or opt-out guardrail | service quit/opt-out guardrail `0.35`, `0.40` | Tests service-quality protection under stronger uptake pressure. |
| Uptake regime assumptions | low and medium regimes already defined; any added regime requires written justification | Keeps passenger-choice assumptions explicit and regime-specific. |

Any added knob must state the operational mechanism it represents, the small
candidate range, and why it is not a search over final outcomes.

## Small Candidate Ranges

Candidate ranges are intentionally small: roughly two or three values per knob
where possible. Open-ended sweeps, adaptive search over final results, and
post-hoc expansion of the grid are prohibited unless a new written protocol
records the scientific basis before the next pilot.

## Prohibited Tuning Actions

The following actions are prohibited:

- No final-result tuning and no current-formal-result tuning.
- No selecting settings from future final formal test results.
- No seed deletion or split deletion.
- No baseline deletion, including no removal of random, fixed-window,
  no-menu, or product-ablation policies.
- No metric deletion, including unfavorable profit, acceptance, opt-out,
  meeting-point uptake, or service-quality metrics.
- No generated-row edits, generated table edits, generated figure edits, or
  claim-guard hand edits.
- No single profit ranking selection as the sole pilot-selection rule.
- No treating calibration pilot rows as final claim evidence.

## Pilot Selection Rule

Pilot selection uses pre-registered multi-metric thresholds, not a single
profit ranking. A candidate setting can be selected for final freezing only if
it satisfies all of the following pilot criteria:

- Profit non-degradation: no large paired net-profit deterioration against the
  no-menu and fixed/random menu baselines without a documented service-quality
  trade-off.
- Service-quality guardrails: acceptance and served rate must not deteriorate
  materially, and opt-out must not increase materially in the target regime.
- Mechanism signal: meeting-point uptake and menu utilization should indicate
  that the service-menu mechanism is active rather than a home-only fallback.
- Regime reporting: low and medium uptake regimes must be reported separately.
- Artifact readiness: pilot rows must include checkpoint load status,
  checkpoint hash where available, `method_family`, `outside_option_util`,
  opt-out/home/meeting-point accounting, status fields, and error fields.

If no candidate satisfies the thresholds, the protocol routes to diagnosis or
conditional service-menu framing rather than relaxing the rule after seeing
results.

## Pilot And Final Separation

Calibration pilot and final formal evidence are separate artifacts.

- Pilot splits/seeds are used only to choose pre-registered settings.
- Final splits/seeds must be independent from pilot splits/seeds.
- Pilot rows must not be reused as final evidence.
- The full seven-tag mainline family must be preserved in both pilot and final
  contracts.
- Checkpoint paths, hashes, sidecars, and load-status requirements must be
  recorded before execution.

## Final Freeze And Rerun Rule

`FROZEN_FINAL_SETTINGS.md` must be written before any final rerun. It must
record the final manifest path and hash, policy tags, split IDs/seeds,
checkpoint path/hash/sidecar, paired fields, varied fields, runtime knobs, and
gate commands.

The final run must be independent from pilot selection. Final settings cannot
be changed after inspecting final rows. Final readiness, replay, artifact, and
claim-guard commands must pass before any stronger manuscript claim is allowed.

## Second-Round Limit

If the first final rerun fails to support the strong claim, one second
calibration round is allowed only after a new written protocol explains why the
first final run failed and what scientific mechanism or operational realism
justifies another round.

This second calibration round is a one-time exception. It must use a new
pilot/final separation and must not tune on the failed final rows beyond
diagnosing mechanisms.

## Downgrade Rule

If the second final rerun also fails, the project must downgrade to conditional
service-menu design framing. The manuscript may discuss where optimized
service menus help or fail, but it must not claim universal superiority.

## Gate Before Execution

Calibration pilot may start only after provenance/readiness gates pass or after
remaining blockers are documented as explicit stopping conditions. If dirty git,
artifact metadata, or claim guard blockers remain, stop and diagnose those
foundations first.
