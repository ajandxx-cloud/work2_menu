# Phase 8: Sensitivity And Robustness Experiments - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-15T23:13:09+08:00
**Phase:** 8-Sensitivity And Robustness Experiments
**Areas discussed:** Sensitivity matrix scope, Run and gate strategy, Robustness knob semantics, Outputs and manuscript conclusion format

---

## Sensitivity Matrix Scope

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Matrix breadth | Must-have actual replay, nice-to-have contract only | Run `menu_k`, ETA/filter, uptake regime, and opt-out guardrail; keep `max_candidates`, fleet/capacity, and pricing sensitivity as deferred/contract notes. | Yes |
| Matrix breadth | Must-have actual replay plus a small number of nice-to-have runs | Add one or two light nice-to-have dimensions, increasing runtime and interpretation complexity. |  |
| Matrix breadth | Full actual replay for every sensitivity dimension | Most complete but likely too expensive and risky under unresolved gates. |  |
| Must-have organization | One-factor-at-a-time sensitivity around frozen/default settings | Change one axis at a time around current defaults for clear interpretation. | Yes |
| Must-have organization | Small crossed matrix | Run small interactions such as `menu_k x ETA/filter` and `uptake x guardrail`. |  |
| Must-have organization | Planner chooses minimal publishable matrix | Let the planner choose the smallest matrix that covers all must-have axes. |  |
| `menu_k` values | `2, 3, 4` | Uses the pre-registered small range with `3` as the center/default. | Yes |
| `menu_k` values | `1, 2, 3, 4, 5` | Covers extreme small and larger menus but increases runtime and diagnostic burden. |  |
| `menu_k` values | `2, 3, 4` actual replay; `1/5` as placeholder/future contract | Keeps actual replay small while documenting wider edges. |  |
| Nice-to-have handling | Deferred/contract notes only, no runtime manifest | Record candidate pool, fleet/capacity, and pricing sensitivity without executable runtime manifests. | Yes |
| Nice-to-have handling | Disabled planning manifest drafts | More future-ready but creates more files and possible confusion. |  |
| Nice-to-have handling | Only mention deferred in CONTEXT.md | Simplest, but gives future planners less detail. |  |

**User's choice:** Option 1 for all questions.
**Notes:** Phase 8 actual replay is restricted to must-have dimensions. Nice-to-have dimensions are preserved for later but not executable in this phase.

---

## Run And Gate Strategy

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Use of existing baseline validation | Prerequisite gate, sensitivity suite separate | Keep `phase8_baseline_validation` as a front gate and create a separate sensitivity suite. | Yes |
| Use of existing baseline validation | Merge into sensitivity suite | Centralizes files but mixes baseline validation with sensitivity evidence. |  |
| Use of existing baseline validation | Skip baseline validation | Fastest but discards an existing Phase 8 gate. |  |
| Output classification under unresolved gates | Actual replay allowed, all diagnostic/provisional | Produce rows and summaries while keeping `claim_ready=false` and no manuscript claim upgrade. | Yes |
| Output classification under unresolved gates | Contracts only, no replay | Most conservative but produces no empirical sensitivity rows. |  |
| Output classification under unresolved gates | Smoke/pilot only, no formal sensitivity | Middle path, defers formal evidence. |  |
| Tier/run mode | Diagnostic/pilot tier, no formal tier | Matches current blocked-gate status and supports mechanism diagnostics. | Yes |
| Tier/run mode | Formal tier with artifact gate forced blocked/provisional | Closer to future claim pipeline but easy to misread. |  |
| Tier/run mode | Pilot actual replay plus formal future contract | Clear but more file-heavy. |  |
| Baseline gate enforcement | Baseline validation failure blocks sensitivity replay | Failed front gate writes a blocked report and stops sensitivity actual replay. | Yes |
| Baseline gate enforcement | Failed baseline still allows blocked/provisional replay | More diagnostic data, but mixes results on failed foundations. |  |
| Baseline gate enforcement | Warning only | Flexible but weakens gate semantics. |  |

**User's choice:** Option 1 for all questions.
**Notes:** `phase8_baseline_validation` remains a separate prerequisite. Sensitivity is diagnostic/pilot actual replay only, and baseline validation failure blocks replay.

---

## Robustness Knob Semantics

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| ETA/filter modes | `hard`, `interval_overlap`, `chance_constraint`; no-filter diagnostic only | Covers strict, robust-overlap, and probability constraint modes while keeping no-filter out of deployable comparison. | Yes |
| ETA/filter modes | `hard` and `interval_overlap` only | Most conservative but weaker ETA uncertainty coverage. |  |
| ETA/filter modes | Add `soft_penalty` and `none` to main replay | Broadest, but harder to explain and riskier for gates. |  |
| Chance threshold | `0.25` only | Existing default and adapter value; avoids matrix expansion. | Yes |
| Chance threshold | `0.20` and `0.25` | Matches calibration candidates but adds rows. |  |
| Chance threshold | Planner decides whether to add `0.20` | Flexible but less locked. |  |
| Uptake regime | Existing `low` and `medium` only | Aligns with formal/final/calibration manifests. | Yes |
| Uptake regime | Add high uptake diagnostic stress-test | Adds mechanism information but requires new pre-registered parameters. |  |
| Uptake regime | High uptake contract only | Leaves future entry without replay. |  |
| Guardrail values | `0.35` and `0.40` | Uses Phase 5 pre-registered guardrail range. | Yes |
| Guardrail values | `0.35`, `0.40`, and `0.45` | Adds wider stress-test boundary. |  |
| Guardrail values | `0.35` only | Too narrow for the must-have guardrail axis. |  |

**User's choice:** Option 1 for all questions.
**Notes:** ETA sensitivity is limited to three deployable/robust modes plus no-filter as a diagnostic boundary. Uptake stays low/medium. Guardrail values are 0.35 and 0.40.

---

## Outputs And Manuscript Conclusion Format

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Summary narrative | Conditional boundary map | Explain where optimized service menus help and where they fail. | Yes |
| Summary narrative | Strong central claim support | More aggressive but inconsistent with current gates and Phase 4 diagnosis. |  |
| Summary narrative | Pure run-status report | Safe but less useful for the paper discussion. |  |
| Tables/figures source | Generated from normalized rows/artifact builder; planning summary cites paths | Preserves no-hand-edited-artifacts rule. | Yes |
| Tables/figures source | Markdown tables first, formal artifacts later | Fast but risks hand-written paper-facing tables. |  |
| Tables/figures source | JSON/CSV only, no figures | Machine-friendly but weak for paper readability. |  |
| Claim status | `diagnostic_provisional_blocked` | Captures actual replay plus unresolved gates. | Yes |
| Claim status | `sensitivity_complete_not_claim_ready` | More positive but "complete" may be misleading. |  |
| Claim status | `blocked_pending_gate_cleanup` | Too blocking if actual replay is allowed. |  |
| Manuscript language upgrade | No; diagnostic-safe language only | Avoids abstract/conclusion claim upgrades in Phase 8. | Yes |
| Manuscript language upgrade | Conditional claim draft marked blocked | Future-useful but risky to copy into manuscript. |  |
| Manuscript language upgrade | Allow conditional upgrade if results are strong | Would bypass Phase 10 artifact/claim guard. |  |

**User's choice:** Option 1 for all questions.
**Notes:** `SENSITIVITY_SUMMARY.md` should be a boundary map, not a claim upgrade. Tables and figures must come from generated artifacts. Phase 8 status is `diagnostic_provisional_blocked`.

---

## The Agent's Discretion

- Choose exact manifest and suite filenames.
- Choose exact split IDs, output roots, and report sections.
- Choose whether the sensitivity design is one study, multiple studies, or a suite, while preserving the baseline validation prerequisite.
- Choose focused script-style tests that protect the new contract.

## Deferred Ideas

- Candidate pool size sensitivity (`max_candidates`).
- Fleet/capacity stress.
- Pricing bounds or price sensitivity.
- High-uptake regime.
- `menu_k` values `1` and `5`.
- `soft_penalty` ETA mode and no-filter as main-comparison evidence.
