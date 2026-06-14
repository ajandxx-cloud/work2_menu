# Phase 9: DSPO Family Full Run - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-14T20:03:59.5478499+08:00
**Phase:** 9-DSPO Family Full Run
**Areas discussed:** DSPO clip/wide tag identity, Comparison bundle shape, Pass/fail gate strength, Runtime budget and evidence tier, Ranking sanity output wording

---

## DSPO Clip/Wide Tag Identity

| Option | Description | Selected |
|--------|-------------|----------|
| Add explicit `dspo_clip` / `dspo_wide` tags | Cleaner Phase 9 policy identity; avoids treating old mainline tags as the paper-facing DSPO clip/wide names. | Yes |
| Reuse existing mainline tags | Less implementation change, but Phase 9 naming would remain ambiguous. | |
| Dual-track aliases | Add Phase 9 names while mapping to existing semantics. | |

**User's choice:** Add explicit `dspo_clip` / `dspo_wide` tags.
**Notes:** The user clarified later that DSPO_PLUS has no relationship to this project, so the explicit tags are DSPO-internal only and must not be designed around DSPO_PLUS symmetry.

| Option | Description | Selected |
|--------|-------------|----------|
| Define `clip/wide` by service-risk threshold | `clip` is stricter and `wide` is looser inside DSPO. | Yes |
| Define by time-window shape | Could confuse clip/wide with fixed/adaptive time-window ablations. | |
| Define by candidate/menu scope | Would mix risk threshold with candidate-pool size. | |

**User's choice:** Define `clip/wide` by service-risk threshold.
**Notes:** The user selected strict/wide risk threshold semantics.

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed values `0.35` and `0.45` | `dspo_clip=0.35`, `dspo_wide=0.45`; simple and reportable. | Yes |
| Derive from existing mainline semantics | Planner would infer from current code. | |
| Lock only relative relation | Only require clip stricter and wide looser. | |

**User's choice:** Fixed values.
**Notes:** The user selected `0.35` for clip and `0.45` for wide after clarifying DSPO_PLUS is unrelated.

| Option | Description | Selected |
|--------|-------------|----------|
| `method_family=DSPO` plus `policy_tag` and role | Clear row metadata; prevents DSPO_PLUS from entering Phase 9 semantics. | Yes |
| `policy_tag` only | Lower schema impact but weaker report/gate semantics. | |
| Add a new `dspo_variant` field | Strong semantics but broader row schema change. | |

**User's choice:** Use `method_family=DSPO`, distinguish by `policy_tag`, and add a role such as `comparison_role=dspo_family`.
**Notes:** Phase 9 should not include DSPO_PLUS semantics.

---

## Comparison Bundle Shape

| Option | Description | Selected |
|--------|-------------|----------|
| Run only `dspo_clip` / `dspo_wide` | Keeps Phase 9 focused on DSPO family validation; references Phase 8 baseline status instead of rerunning baselines. | Yes |
| Run four tags including baselines | Direct sanity table, but higher cost and broader scope. | |
| Primary DSPO manifest plus optional diagnostic bundle | Clean gate plus optional same-run diagnostics, but more implementation work. | |

**User's choice:** Phase 9 primary manifest only runs `dspo_clip` and `dspo_wide`.
**Notes:** Phase 8 baselines are not rerun in the Phase 9 primary manifest.

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse Phase 8 five formal-equivalent splits | Strongest comparability to Phase 8 baselines. | Yes |
| Use `formal_robust_menu` splits | Aligns with old formal manifest but weakens Phase 8 comparability. | |
| Add Phase 9-specific splits | Clean isolation but weaker baseline comparability. | |

**User's choice:** Reuse Phase 8 splits exactly.
**Notes:** Includes seeds, data seeds, uptake regimes, and utility parameters.

| Option | Description | Selected |
|--------|-------------|----------|
| Do sanity comparison as gate/status only | Meets Phase 9 sanity requirement without making ranking claims. | Yes |
| Do not compare with baselines | Cleaner, but weakens ranking sanity checks. | |
| Produce a full ranking table | More direct but risks overclaiming. | |

**User's choice:** Do gate/status sanity comparison only.
**Notes:** The report can reference Phase 8 baseline status but cannot present a final ranking claim.

| Option | Description | Selected |
|--------|-------------|----------|
| Reference latest passed Phase 8 validation report | Low-cost, explicit cross-run status reference. | Yes |
| Regenerate baseline report each time | Stricter but higher cost. | |
| Only state Phase 8 passed | Too little evidence detail for sanity reference. | |

**User's choice:** Reference the latest passed Phase 8 validation report and run ID.
**Notes:** Must label the comparison as cross-run sanity/status reference, not same-run ranking evidence.

---

## Pass/Fail Gate Strength

| Option | Description | Selected |
|--------|-------------|----------|
| Any failed DSPO row/split blocks | Strongest gate; mirrors Phase 8 validation style. | Yes |
| Allow partial pass | More flexible but weaker evidence gate. | |
| Distinguish failure types | More nuanced but unnecessarily complex for 5x2 rows. | |

**User's choice:** Any failed DSPO row/split blocks Phase 9.
**Notes:** Failures include row status, checkpoint, paired drift, schema, accounting, and provenance anomalies.

| Option | Description | Selected |
|--------|-------------|----------|
| Per-row/split reason, minimal fix, rerun command | Directly actionable debug handoff. | Yes |
| Overall failure only | Shorter but less useful. | |
| Layered examples by failure type | More complex than needed. | |

**User's choice:** Every failure gets reason, minimal fix, and rerun command.
**Notes:** Follow Phase 8 gate/report style.

| Option | Description | Selected |
|--------|-------------|----------|
| Unlock DSPO result organization/status language only | Avoids premature ranking claims. | Yes |
| Unlock preliminary DSPO-over-baseline claim | Too risky for gate-first workflow. | |
| Unlock no paper language | Too conservative for later Phase 11 reuse. | |

**User's choice:** Passing Phase 9 unlocks DSPO result organization and status language only.
**Notes:** No "DSPO improves over baselines" claim is unlocked.

| Option | Description | Selected |
|--------|-------------|----------|
| Debug handoff but no automatic repair | Keeps Phase 9 bounded while satisfying GATE-04. | Yes |
| Automatically debug/fix | Too broad for this discussion/plan boundary. | |
| Only record failure | Too weak for downstream work. | |

**User's choice:** Blocked Phase 9 reports must provide debug handoff but not auto-fix.
**Notes:** The report should stop in a debug-ready state.

---

## Runtime Budget And Evidence Tier

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse Phase 8 lightweight formal-equivalent budget | Keeps runtime low and DSPO comparable with Phase 8 baselines. | Yes |
| Use heavier `formal_robust_menu` settings | Stronger but costlier and less comparable to Phase 8. | |
| Two-stage light then optional formal | More robust but broader scope. | |

**User's choice:** Reuse Phase 8 lightweight formal-equivalent budget.
**Notes:** Phase 9 should not escalate to `formal_robust_menu` settings.

| Option | Description | Selected |
|--------|-------------|----------|
| Keep menu/candidate parameters identical to Phase 8 | Preserves fairness and isolates clip/wide threshold difference. | Yes |
| Let wide use larger candidate pool | Would conflate wide with candidate scope. | |
| Lock only core parameters | Too much planning ambiguity. | |

**User's choice:** Keep menu/candidate parameters identical to Phase 8.
**Notes:** `wide` is not defined by larger candidate pool.

| Option | Description | Selected |
|--------|-------------|----------|
| Same checkpoint/provenance strictness as Phase 8 | Requires loaded checkpoint and recorded checkpoint path/hash. | Yes |
| Allow diagnostic fallback | Useful for debugging but not a pass condition. | |
| Only require checkpoint path | Too weak. | |

**User's choice:** Same checkpoint/provenance strictness as Phase 8.
**Notes:** Claim-ready status remains separate and may remain false.

| Option | Description | Selected |
|--------|-------------|----------|
| Only generate JSON/Markdown validation report | Avoids packaging status-only outputs as paper artifacts. | Yes |
| Generate diagnostic artifact bundle | More browsable but broader scope. | |
| Try claim-ready artifact builder | Not appropriate for Phase 9. | |

**User's choice:** Only generate Phase 9 JSON/Markdown validation report.
**Notes:** No artifact bundle and no claim-ready artifact build for Phase 9 completion.

---

## Ranking Sanity Output Wording

| Option | Description | Selected |
|--------|-------------|----------|
| Gate-first status language plus short sanity summary | Enough for sanity without becoming a ranking claim. | Yes |
| Include per-policy metric table | More detailed but riskier for overclaiming. | |
| Only passed/blocked | Too weak for ranking sanity success criteria. | |

**User's choice:** Gate-first status language plus short sanity summary.
**Notes:** Must state sanity comparison is status-only.

| Option | Description | Selected |
|--------|-------------|----------|
| Explicitly mark DSPO_PLUS as unrelated/stale residue | Prevents planner/executor from inheriting old DSPO_PLUS scope. | Yes |
| Record only in CONTEXT | Report readers may still misread old scope. | |
| Do not address DSPO_PLUS residue | High risk of repeated scope drift. | |

**User's choice:** CONTEXT and report must state DSPO_PLUS is unrelated to this project.
**Notes:** Existing planning references should be treated as cleanup risk.

| Option | Description | Selected |
|--------|-------------|----------|
| Gate passed but sanity does not support advantage | Separates execution/gate success from ranking strength. | Yes |
| Block Phase 9 if DSPO does not outperform baselines | Mixes performance result with execution gate. | |
| Do not evaluate direction | Too weak for sanity check. | |

**User's choice:** If execution gates pass but DSPO does not outperform Phase 8 baselines, Phase 9 may still pass while reporting that advantage is not supported.
**Notes:** No advantage claim should be made.

| Option | Description | Selected |
|--------|-------------|----------|
| Include a clear next step | Debug handoff if blocked; status/risk language if passed without advantage. | Yes |
| No next step | Harder for workflow continuation. | |
| Recommend experiment expansion | Scope creep for Phase 9. | |

**User's choice:** Include one clear next step.
**Notes:** Do not recommend experiment expansion inside Phase 9.

---

## the agent's Discretion

- Exact helper names, report filenames, JSON field names, and test filenames
  are left to the planner/executor, provided the locked decisions are
  preserved.

## Deferred Ideas

- Clean up DSPO_PLUS references from planning/runtime documents in a follow-up
  scope cleanup task.
- Heavier formal reruns or expanded experiments are deferred unless the user
  explicitly creates a new phase/request.
