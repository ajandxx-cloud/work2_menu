# Phase 9: Exact Versus Greedy And Computational Tractability - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-16T10:02:14.2694067+08:00
**Phase:** 9-Exact Versus Greedy And Computational Tractability
**Areas discussed:** Phase 9 boundary, Candidate-set scale design, Run tier and paired fairness, Outputs and claim-narrowing rules

---

## Phase 9 Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Keep as prerequisite gate | Treat existing `phase9_dspo_family_validation` as a passed prerequisite status gate while Phase 9 focuses on exact-greedy tractability. | yes |
| Merge into Phase 9 main result | Treat `dspo_clip` / `dspo_wide` as core Phase 9 computation evidence. | |
| Demote to appendix/historical status | Cite it only as historical context and do not plan around it. | |

**User's choice:** Keep as prerequisite gate.
**Notes:** The existing DSPO validation is status-only and passed, but it is not the exact-versus-greedy tractability result.

| Option | Description | Selected |
|--------|-------------|----------|
| Preserve blockers and do not clean them | Keep `claim_ready=false` blockers visible and avoid turning Phase 9 into provenance cleanup. | yes |
| Clean claim-ready blockers inside Phase 9 | Add dependency snapshot and git provenance cleanup to Phase 9. | |
| Mention only in the report | Cite blockers without making them a planning decision. | |

**User's choice:** Preserve blockers and do not clean them.
**Notes:** Phase 9 remains diagnostic/status-gated.

| Option | Description | Selected |
|--------|-------------|----------|
| Do not rerun full study; cite existing passed report | Use the existing passed DSPO validation report and allow only light status checks if needed. | yes |
| Only rebuild validation report | Regenerate JSON/Markdown from the existing run directory. | |
| Rerun full DSPO validation study | Re-execute the 10-row DSPO validation study. | |

**User's choice:** Do not rerun full study; cite existing passed report.
**Notes:** Avoid pulling Phase 9 back toward DSPO-family status work.

| Option | Description | Selected |
|--------|-------------|----------|
| Tractability diagnostic passed/open, claim-ready still blocked | Allow computational status language while preserving claim-ready blockers. | yes |
| Claim-ready computational evidence | Treat Phase 9 as claim-ready after completion. | |
| Planning-only computational contract | Write contract only without new exact-greedy evidence. | |

**User's choice:** Tractability diagnostic passed/open, claim-ready still blocked.
**Notes:** This phrase is the intended status boundary.

---

## Candidate-Set Scale Design

| Option | Description | Selected |
|--------|-------------|----------|
| Use current exact threshold: `max_candidates=8`, `menu_exact_threshold=8` | Reuses current exact benchmark scale and existing diagnostics. | yes |
| Use smaller conservative exact set: `max_candidates=6` | Faster but less convincing. | |
| Push exact to `max_candidates=10` | More aggressive but riskier for runtime. | |

**User's choice:** Use `max_candidates=8` and `menu_exact_threshold=8`.
**Notes:** This is the small exact benchmark.

| Option | Description | Selected |
|--------|-------------|----------|
| Use `max_candidates=12` and `16` | Two large greedy scales for controlled scaling evidence. | yes |
| Use only `max_candidates=12` | Lighter but weaker trend evidence. | |
| Use `max_candidates=12`, `16`, and `20` | Stronger scaling curve but higher runtime risk. | |

**User's choice:** Use `max_candidates=12` and `16`.
**Notes:** These are the large greedy scales.

| Option | Description | Selected |
|--------|-------------|----------|
| Fix `menu_k=3` | Keeps Phase 9 centered on solver tractability and frozen/default settings. | yes |
| Vary `menu_k` across `2`, `3`, and `4` | Mixes Phase 8 menu-size sensitivity into Phase 9. | |
| Use only `menu_k=4` | Stressful but off-center from the main setting. | |

**User's choice:** Fix `menu_k=3`.
**Notes:** Phase 8 already handled menu-size sensitivity.

| Option | Description | Selected |
|--------|-------------|----------|
| Use threshold fallback and record `above_exact_threshold` | Uses existing fallback metadata to express exact infeasibility. | yes |
| Force exact until timeout | Would need timeout machinery and may destabilize runs. | |
| Only report theoretical enumeration without large greedy replay | Too weak for runtime credibility. | |

**User's choice:** Use threshold fallback and record `above_exact_threshold`.
**Notes:** Do not force exact enumeration for large candidate sets.

---

## Run Tier And Paired Fairness

| Option | Description | Selected |
|--------|-------------|----------|
| Formal-equivalent diagnostic | Formal-like paired replay with diagnostic/status-gated output. | yes |
| Pilot-style diagnostic | Faster but weaker computational evidence. | |
| Smoke/contract only | Validates fields/scripts only. | |

**User's choice:** Formal-equivalent diagnostic.
**Notes:** Satisfies COMP-01/02 without claiming readiness.

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse Phase 8 / Phase 9 DSPO validation 5 splits | Aligns with existing low/medium uptake paired surface. | yes |
| Use only 3 splits | Lighter but weaker than current gate surface. | |
| Expand to more splits | Stronger but too close to a formal rerun. | |

**User's choice:** Reuse the five existing paired splits.
**Notes:** Preserve low/medium uptake coverage and paired fairness.

| Option | Description | Selected |
|--------|-------------|----------|
| Same split compares solver-scale variants | Each split has comparable exact/greedy scale rows with shared replay settings. | yes |
| Exact and greedy run independently then aggregate | Simpler but weaker pairing. | |
| Request-level internal diagnostic only | Harder for artifact builders and tables to consume. | |

**User's choice:** Same split compares solver-scale variants.
**Notes:** Solver-scale variants should share seeds, traces, checkpoint, choice parameters, and HGS settings.

| Option | Description | Selected |
|--------|-------------|----------|
| Require loaded shared checkpoint and record hash/status | Protects formal-equivalent comparability. | yes |
| Allow missing checkpoint/random model | Easier to run but scientifically noisy. | |
| Use synthetic unit benchmark without checkpoint | Fast but detached from online DRT replay. | |

**User's choice:** Require loaded shared checkpoint and record hash/status.
**Notes:** Checkpoint failure should become blocked row/report status.

---

## Outputs And Claim-Narrowing Rules

| Option | Description | Selected |
|--------|-------------|----------|
| Write planning summary and generate runtime report/artifacts | Produces `.planning/results/COMPUTATIONAL_TRACTABILITY_SUMMARY.md` plus row-backed artifacts. | yes |
| Only generate runtime artifacts | Less context for claim boundaries. | |
| Only write planning summary | Insufficient for table/figure success criteria. | |

**User's choice:** Write planning summary and generate runtime report/artifacts.
**Notes:** Planning summary interprets; generated artifacts remain source for paper-facing tables and figures.

| Option | Description | Selected |
|--------|-------------|----------|
| Include candidate count, enumerated count, build time, gap, overlap, fallback/status | Full COMP-01/02 metric coverage. | yes |
| Only build time and gap | Simpler but incomplete. | |
| Only status/fallback and build time | Shows online execution but not greedy quality. | |

**User's choice:** Include all core solver diagnostics.
**Notes:** Candidate count, enumerated menu count, build time, relative gap, overlap, fallback/status are mandatory.

| Option | Description | Selected |
|--------|-------------|----------|
| Computationally fast but approximate; quality is regime-dependent | Narrows claim if greedy gap is large. | yes |
| Block Phase 9 and require greedy redesign | Strict but outside scope. | |
| Report gap without changing claim language | Conflicts with roadmap claim-narrowing rule. | |

**User's choice:** Computationally fast but approximate; quality is regime-dependent.
**Notes:** Phase 9 does not force algorithm redesign when gaps are large.

| Option | Description | Selected |
|--------|-------------|----------|
| 15 solver-scale rows complete or explicitly blocked, plus artifact/report, `claim_ready=false` | 5 splits x 3 variants with explicit status. | yes |
| Any one scale runs successfully | Too weak. | |
| All outputs must be claim-ready | Conflicts with current blocker state. | |

**User's choice:** 15 solver-scale rows complete or explicitly blocked, plus artifact/report, `claim_ready=false`.
**Notes:** Failed rows/reports must be explicit, not silent.

## The Agent's Discretion

- Exact manifest, suite, report, and artifact filenames.
- Whether to extend the existing artifact builder or add a Phase 9-specific builder.
- Exact script-style test names and blocked-report wording, as long as the locked decisions are enforced.

## Deferred Ideas

- Provenance cleanup and dependency snapshot cleanup.
- Full DSPO validation rerun.
- `max_candidates=20`, varying `menu_k`, forced exact timeout experiments, and greedy algorithm redesign.
