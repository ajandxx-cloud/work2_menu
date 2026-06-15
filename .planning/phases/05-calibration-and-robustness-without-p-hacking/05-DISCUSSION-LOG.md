# Phase 5: Calibration And Robustness Without P-Hacking - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-15T14:41:40+08:00
**Phase:** 5-Calibration And Robustness Without P-Hacking
**Areas discussed:** Phase 5 route choice, allowed and prohibited calibration boundary, pilot/final split design, frozen settings and rerun gates

---

## Phase 5 Route Choice

| Option | Description | Selected |
|--------|-------------|----------|
| Continue pursuing strong claim | Clean provenance plus pre-registered pilot/final calibration; no direct tuning on existing formal results. | yes |
| Directly switch to conditional framing | Stop strong-claim pursuit and write a short calibration gate note. | |
| Minimal dual-track calibration | Write strict protocol and allow only a small pilot before stopping if no mechanism signal appears. | |

**User's choice:** Continue pursuing strong claim.
**Notes:** User selected the strong-claim route, then selected gate-first ordering, stop-and-diagnose if gates remain blocked, and process-lock success criteria.

| Option | Description | Selected |
|--------|-------------|----------|
| Clean gates first, then calibrate | Resolve dirty-git/provenance and readiness before calibration execution. | yes |
| Write protocol first, then clean gates | Lock protocol before provenance cleanup. | |
| Plan in parallel | Plan protocol and cleanup together, but do not run experiments until gates clear. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Stop and diagnose | If gates remain blocked, do not start calibration pilot. | yes |
| Allow diagnostic pilot | Allow pilot despite incomplete claim-ready gates, but not final rerun. | |
| Write protocol but pause experiments | Complete templates while pausing pilot/final execution. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Strong-claim process prerequisites | Success means provenance/readiness restored, protocol locked, pilot selection pre-registered, and final settings frozen. | yes |
| Result-improvement oriented | Success requires pilot improvement trend. | |
| Minimal compliance oriented | Success only requires protocol and frozen settings documents. | |

---

## Allowed And Prohibited Calibration Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Realism and mechanism parameters | Allow `menu_k`, `max_candidates`, ETA filter/threshold, opt-out guardrail, and uptake regime when justified by realism/robustness. | yes |
| Only experiment-scale parameters | Only tune seeds/splits/episodes/HGS time. | |
| Wider mechanism search | Allow broader menu target, guardrail, filter, and price-sensitivity search with pre-registration. | |

**User's choice:** Realism and mechanism parameters.
**Notes:** User selected a strict no-p-hacking boundary: no direct formal/final ranking optimization, no seed/split/baseline/metric deletion, no hand-edited rows/artifacts, multi-metric pilot selection, and small candidate ranges.

| Option | Description | Selected |
|--------|-------------|----------|
| Prohibit direct formal ranking optimization | Do not use final/formal test results for parameter choice; do not remove unfavorable evidence; do not hand-edit outputs. | yes |
| Only prohibit hand-edited results | Allow formal-result-driven parameter changes if documented. | |
| Prohibit changing core behavior model | Forbid utility/choice/pricing changes but allow other formal-driven tweaks. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Pre-registered multi-metric thresholds | Select by profit non-degradation plus service and mechanism guardrails. | yes |
| Primary metric first | Select primarily by profit or service-constrained profit, with service vetoes. | |
| Robustness first | Prefer cross-regime/split stability even if mean profit is lower. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Small and explainable | Use roughly 2-3 candidate values per knob. | yes |
| Medium grid | Use a larger grid with a bounded number of pilot runs. | |
| Stage-expanded search | Expand search after weak pilot signal with protocol amendments. | |

---

## Pilot/Final Split Design

| Option | Description | Selected |
|--------|-------------|----------|
| Strict separation | Pilot uses independent splits/seeds and only selects settings; final uses frozen independent splits/seeds. | yes |
| Reuse current pilot and formal manifests | Keep current manifests and document the boundary. | |
| Rebuild two fully separate manifests | Create fully new calibration and final manifests. | |

**User's choice:** Strict separation.
**Notes:** User selected full seven-tag family in both pilot and final, retrained and locked calibration/final checkpoints, and complete manifest-granularity freezing.

| Option | Description | Selected |
|--------|-------------|----------|
| Keep seven tags | Keep all seven mainline policy tags in calibration pilot and final. | yes |
| Reduced pilot and seven-tag final | Pilot uses critical baselines only; final uses seven tags. | |
| Only claim-critical tags | Use a reduced claim-critical family. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Retrain and lock calibration/final checkpoint | Record path, hash, sidecar, and load status; do not change checkpoint by ranking. | yes |
| Reuse existing formal checkpoint | Continue using the current formal checkpoint. | |
| Pilot retrains, final reuses formal checkpoint | Explore with pilot checkpoint and return to existing formal checkpoint for final. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Complete manifest granularity | Freeze manifest hash, policy tags, split IDs/seeds, checkpoint, paired/varied fields, runtime knobs, and gate commands. | yes |
| Key parameter granularity | Freeze only the main knobs and checkpoint. | |
| Document-only description | Describe settings without manifest hash or complete field lock. | |

---

## Frozen Settings And Rerun Gates

| Option | Description | Selected |
|--------|-------------|----------|
| Provenance and readiness all pass | Require clean provenance/readiness, checkpoint protocol, and locked calibration protocol before pilot. | yes |
| Only protocol locked | Allow diagnostic pilot once protocol is written. | |
| Only no hand-edited results | Start pilot if outputs are not hand-edited. | |

**User's choice:** Provenance and readiness all pass.
**Notes:** User selected frozen-file and gate-command lock before final rerun, allowed one second calibration round after first final failure, and required one-time exception guardrails.

| Option | Description | Selected |
|--------|-------------|----------|
| Frozen files and gate commands all locked | Require `FROZEN_FINAL_SETTINGS.md`, manifest hash, checkpoint hash, split IDs, policy tags, and gate commands before final rerun. | yes |
| Pilot result passes thresholds | Enter final when pilot reaches thresholds and document afterward. | |
| User confirmation only | User approval is enough; details can be filled in during execution. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Automatically downgrade to conditional framing | Stop calibration after first final failure. | |
| Allow second calibration round | Permit a second round with a new protocol explaining round-one failure and scientific basis. | yes |
| Leave decision to Phase 8 sensitivity | Defer strong-claim decision to sensitivity phase. | |

| Option | Description | Selected |
|--------|-------------|----------|
| One-time exception plus external/mechanism reason | Permit at most one additional round, justified by mechanism failure or operational realism; second final failure forces conditional framing. | yes |
| Multiple pre-registered rounds | Allow multiple pre-registered pilot/final rounds. | |
| User approves each round without fixed cap | No predefined cap; user decides after each failure. | |

---

## The Agent's Discretion

- Planner may choose exact manifest names, output roots, headings, and document structure.
- Planner may propose exact candidate values for allowed calibration knobs within small, explainable ranges.
- Planner may decide whether to create new YAML manifests during Phase 5 or specify them first in protocol documents.

## Deferred Ideas

None - discussion stayed within Phase 5 scope.
