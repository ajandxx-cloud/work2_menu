---
phase: 03-statistical-and-welfare-reframing
verified: 2026-05-14T12:00:00Z
status: passed
score: 4/4 must-haves verified
overrides_applied: 0
---

# Phase 3: Statistical and Welfare Reframing Verification Report

**Phase Goal:** Rework inference language and passenger-facing tradeoff analysis.
**Verified:** 2026-05-14T12:00:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Austin and Seattle are presented as descriptive two-pair checks only | VERIFIED | results.tex line 60: explicit "descriptive two-pair checks, not as stable generalization estimates" parenthetical; uncertainty table rows 14-17 all labeled "Two-pair descriptive range"; results.tex line 72: "do not constitute replication or external validation in the inferential sense" |
| 2 | RC effects include split-level mean/range, percentage effect, and operational interpretation where available | VERIFIED | uncertainty table rows 12-13: "Mean gap", "Split-level range (6 pairs)", "Gap as % of \|full\|" columns all populated with values; results.tex line 53: "split-level paired means with the observed range; the percentage effect is computed relative to the full-display net profit"; acceptance tradeoff note at same location |
| 3 | Profit changes are separated from acceptance and service-quality changes | VERIFIED | results.tex line 33: "profit improvement does not automatically imply a service-quality improvement"; results.tex line 55: profit decomposition paragraph referencing tab:profit_decomposition; managerial.tex line 11: four-dimension tradeoff listing (profit, acceptance, service metrics, volume) |
| 4 | Welfare framing distinguishes all-request and accepted-user interpretations, with surplus formula treatment documented | VERIFIED | appendix.tex lines 200-215: Consumer Surplus Computation section with MNL formula, all-request definition (line 211), accepted-user definition (line 212), divergence note (line 215); limitations.tex line 11: selection-effect caveat; managerial.tex line 11: "can move in opposite directions when a policy changes the acceptance rate" |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `ooh_code/artifacts/tables/policy_gap_uncertainty_summary.tex` | Relabeled uncertainty table | VERIFIED | Caption says "gap summary" not "uncertainty summary"; column header "Range type" instead of "Interval type"; RC rows: "Split-level range (6 pairs)"; city rows: "Two-pair descriptive range"; caption includes descriptive-only caveat |
| `ooh_code/artifacts/tables/profit_decomposition_summary.tex` | New profit decomposition table | VERIFIED | 7 policies, 8 columns (Fare revenue, Discount cost, Travel cost, Service cost, Failure cost, Net profit, Accepted reqs); label tab:profit_decomposition; non-trivial varying numeric values from pipeline data |
| `ooh_code/manuscript/sections/results.tex` | Statistical rework + welfare caveat + profit decomposition paragraph | VERIFIED | Line 60: descriptive-only parenthetical; line 53: RC statistical context with split-level mean/range/percentage; line 33: welfare caveat separating profit from service quality; line 55: profit decomposition paragraph with tab:profit_decomposition reference |
| `ooh_code/manuscript/sections/managerial.tex` | Tradeoff narrative | VERIFIED | Line 9: descriptive two-pair check sentence; line 11: four-dimension tradeoff narrative referencing tab:profit_decomposition and app:consumer_surplus |
| `ooh_code/manuscript/sections/limitations.tex` | Surplus caveat | VERIFIED | Line 11: selection-effect paragraph noting accepted-user surplus can increase without individual improvement |
| `ooh_code/manuscript/sections/appendix.tex` | Consumer surplus formula | VERIFIED | Lines 200-215: section Consumer Surplus Computation with label app:consumer_surplus; MNL surplus formula; all-request and accepted-user definitions with itemized explanation |
| `ooh_code/scripts/build_artifacts.py` | New builder function + uncertainty table relabeling | VERIFIED | Line 1664: build_profit_decomposition_artifacts() reads real pipeline data; line 979: "Two-pair descriptive range" for cities; line 982: "Split-level range (6 pairs)" for RC; line 1026: "Range type" column header |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| results.tex | tab:profit_decomposition | Table~\ref{tab:profit_decomposition} | WIRED | results.tex line 55, managerial.tex line 11 both reference the table defined in profit_decomposition_summary.tex line 6 |
| results.tex | tab:policy_gap_uncertainty_summary | Table~\ref{tab:policy_gap_uncertainty_summary} | WIRED | results.tex line 53 references the table defined in policy_gap_uncertainty_summary.tex line 6 |
| managerial.tex | app:consumer_surplus | Appendix~\ref{app:consumer_surplus} | WIRED | managerial.tex line 11 references the appendix section defined at appendix.tex line 201 |
| limitations.tex | app:consumer_surplus | Appendix~\ref{app:consumer_surplus} | WIRED | limitations.tex line 11 references the appendix section defined at appendix.tex line 201 |
| build_artifacts.py | profit_decomposition_summary.tex | write_tex_table() call at line 1693 | WIRED | Function generates the .tex file with real data from aggregate_variant_summary.json |
| build_artifacts.py | policy_gap_uncertainty_summary.tex | write_tex_table() call at line 1012 | WIRED | Function generates the .tex file with relabeled range types |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| profit_decomposition_summary.tex | Per-policy financial metrics | build_profit_decomposition_artifacts() reads aggregate_variant_summary.json | Yes -- 7 policies with varying non-trivial values across 8 columns | FLOWING |
| policy_gap_uncertainty_summary.tex | Per-policy gap statistics | build_artifacts.py reads split-level paired means, computes range | Yes -- RC and city rows with distinct numeric values | FLOWING |

### Behavioral Spot-Checks

Step 7b: SKIPPED (manuscript LaTeX project -- no runnable entry points for behavioral testing)

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| STAT-01 | 03-01 | City and RC inference are presented with conservative split-level language | SATISFIED | Cities labeled "Two-pair descriptive range"; RC labeled "Split-level range (6 pairs)"; results.tex explicit descriptive-only parenthetical; no CI/interval language for city results |
| WELF-01 | 03-02 | Profit, acceptance, and passenger welfare tradeoffs are decomposed | SATISFIED | Profit decomposition table (7 policies x 8 cost channels); welfare caveat in results.tex; consumer surplus formula in appendix with all-request/accepted-user distinction; selection-effect caveat in limitations.tex |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| appendix.tex | 116 | Section title still says "Split-Level Uncertainty and Policy-Conditioned Diagnostics" | Info | Pre-existing section title not in scope for Phase 3 plans; the visible table caption and column headers are correctly relabeled. This can be addressed in Phase 4 (Manuscript Integration) which covers terminology and caption cleanup. |

### Human Verification Required

No items require human verification. All success criteria are verifiable through text inspection of manuscript source files and generated LaTeX tables.

### Gaps Summary

No gaps found. All four success criteria from ROADMAP.md are satisfied with substantive, wired, and data-flowing artifacts. Both requirements (STAT-01, WELF-01) are addressed.

One informational note: the appendix section title at appendix.tex line 116 retains "Uncertainty" in its name. This was not in scope for Phase 3 plans (which targeted the table and results.tex) and is appropriately deferred to Phase 4 (Manuscript Integration), whose success criteria include "Captions and table names use journal-facing language."

---

_Verified: 2026-05-14T12:00:00Z_
_Verifier: Claude (gsd-verifier)_
