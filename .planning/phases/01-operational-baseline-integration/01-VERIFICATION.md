---
phase: 01-operational-baseline-integration
verified: 2026-05-14T15:30:00Z
status: passed
score: 7/7 must-haves verified
overrides_applied: 0
---

# Phase 1: Operational Baseline Integration Verification Report

**Phase Goal:** Make the existing insertion-cost, minimum-lateness, and random-top-k operational baselines visible and interpretable in the manuscript.
**Verified:** 2026-05-14T15:30:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

Truths are merged from ROADMAP Success Criteria (SC1-SC4) and PLAN frontmatter must-haves (T1-T3 from Plan 01, T4-T7 from Plan 02), deduplicated where PLAN truths add specificity to ROADMAP SCs.

| # | Truth | Source | Status | Evidence |
|---|-------|--------|--------|----------|
| 1 | Method/experiments text names the three operational baselines (insertion-cost greedy, minimum-lateness ranking, random-top-k) and explains their DRT-facing role | ROADMAP SC1, PLAN T1 | VERIFIED | method.tex line 140: "Insertion-cost greedy... Minimum-lateness ranking... Random-top-k floor" with dispatch-floor framing; experiments.tex line 12: "ten policies... three operational baselines (insertion-cost greedy, minimum-lateness ranking, and random-top-k floor)" |
| 2 | Results section includes the operational-baseline table with a reader-facing caption and interpretation | ROADMAP SC2, PLAN T4 | VERIFIED | results.tex line 57: \ArtifactTable referencing operational_baselines_summary.tex with caption "dispatch-floor reference points that do not apply menu optimization or ETA filtering"; lines 59: interpretation paragraph follows |
| 3 | Manuscript states what operational baselines do and do not prove relative to menu optimization | ROADMAP SC3, PLAN T5 | VERIFIED | results.tex line 59: "does not establish service-quality bounds or generalize to higher-uptake regimes; it benchmarks the starting point from which menu optimization seeks improvement"; method.tex line 140: "benchmark menu optimization against dispatch-floor selection rather than against alternative optimization objectives" |
| 4 | Round 2's "artifact exists but is not integrated" criticism is directly addressed | ROADMAP SC4, PLAN T7 | VERIFIED | operational_baselines_summary.tex table appears in main results narrative (results.tex line 57) between RC Outside-Option Benchmark (line 46) and Cross-Instance Evaluation (line 61) with full interpretation |
| 5 | Experiments paragraph states correct total policy count (ten) and notes operational baselines use same evaluation protocol without menu optimization | PLAN T2 | VERIFIED | experiments.tex line 12: "ten policies: the seven heuristic and menu-optimization policies... plus three operational baselines... that use the same evaluation protocol but do not optimize the menu"; line 19: "also use $k = 3$ and the same common-offset pricing heuristic, but bypass the menu-value surrogate and ETA-based filtering" |
| 6 | Operational baselines are clearly distinguished from heuristic baselines by structural paragraph break and dispatch-floor label | PLAN T3 | VERIFIED | method.tex: heuristic baselines end at line 138, operational baselines start at line 140 as a separate paragraph beginning "Three additional operational baselines provide dispatch-floor and greedy-policy reference points." No new subsection added. |
| 7 | Limitations section notes operational-baseline evidence is limited to RC low-uptake regime | PLAN T6 | VERIFIED | limitations.tex line 7: "The operational-baseline comparison in Table~\ref{tab:operational_baselines} covers only the RC low-uptake regime and does not span the calibrated higher-uptake or city instances; extending this reference to additional demand conditions is left as future work." |

**Score:** 7/7 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `ooh_code/manuscript/sections/method.tex` | Updated baseline taxonomy with operational-baseline paragraph | VERIFIED | Line 140 contains operational-baseline paragraph with all three policy names, dispatch-floor framing, and structural distinction from heuristic baselines |
| `ooh_code/manuscript/sections/experiments.tex` | Updated policy count and operational-baseline evaluation note | VERIFIED | Line 12: "ten policies"; line 19: operational baselines use k=3 and same pricing but bypass surrogate and filtering |
| `ooh_code/manuscript/sections/results.tex` | ArtifactTable reference to operational_baselines_summary.tex with interpretation paragraph | VERIFIED | Line 57: \ArtifactTable call; line 59: interpretation paragraph with Table ref, dispatch-floor gap, negation scope, cross-reference to tab:rc_main_optout |
| `ooh_code/manuscript/sections/limitations.tex` | Scope note on operational-baseline evidence coverage | VERIFIED | Line 7: sentence appended to existing instance-coverage paragraph noting RC low-uptake limitation |
| `ooh_code/artifacts/tables/operational_baselines_summary.tex` | Source artifact table with real data | VERIFIED | Contains real data: net profit values (-4348.507 to -4354.325), gaps (-1.094 to -5.818), win rates (0.278-0.333). Label: tab:operational_baselines. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| method.tex | sec:baselines | Paragraph addition after heuristic baselines | WIRED | Line 140 operational-baseline paragraph follows line 138 heuristic baselines, within sec:baselines subsection |
| experiments.tex | sec:baselines | Policy count and cross-reference | WIRED | Line 12 references "three operational baselines" linking to method description; line 19 specifies evaluation protocol |
| results.tex | operational_baselines_summary.tex | \ArtifactTable macro | WIRED | Line 57: exact \ArtifactTable call referencing ../artifacts/tables/operational_baselines_summary.tex |
| results.tex | tab:operational_baselines | Table reference in interpretation text | WIRED | Line 59: "Table~\ref{tab:operational_baselines}" |
| results.tex | tab:rc_main_optout | Cross-reference in interpretation text | WIRED | Line 59: "The menu-optimization policies in Table~\ref{tab:rc_main_optout}" |
| limitations.tex | tab:operational_baselines | Table reference in scope note | WIRED | Line 7: "Table~\ref{tab:operational_baselines}" |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| operational_baselines_summary.tex | Table rows (Policy, net profit, gap, win rate, acceptance, menu size, meeting-point count) | Experiment pipeline output | Yes -- real numeric values with non-zero/non-empty data for all cells | FLOWING |
| results.tex interpretation | References to operational baseline findings | Derived from table data + author interpretation | Yes -- specific gap range "4--6 units" matches table data (-4.516, -5.818, -3.774) | FLOWING |

### Behavioral Spot-Checks

Step 7b: SKIPPED -- this phase produces LaTeX manuscript text, not runnable code. No executable entry points to test.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| BASE-01 | 01-01-PLAN | Operational baselines described in empirical-policy taxonomy and interpreted in main evidence narrative | SATISFIED | method.tex line 140 (taxonomy), results.tex lines 57-59 (interpretation) |
| BASE-02 | 01-02-PLAN | Operational-baseline table placed where reviewers see it, connected to transportation-operations relevance | SATISFIED | results.tex line 57 (table in main narrative), interpretation paragraph with dispatch-floor framing |

No orphaned requirements: REQUIREMENTS.md maps only BASE-01 and BASE-02 to Phase 1, both covered by plans.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | -- | -- | -- | -- |

No TODO/FIXME/PLACEHOLDER comments found. No self-referential language ("we now include", "the revised manuscript") found in any modified file. No empty implementations or stub patterns detected.

### Human Verification Required

No items require human testing. All verification targets are textual content in LaTeX files that can be fully verified by content analysis.

### Gaps Summary

No gaps found. All seven merged truths verified against the actual codebase:

1. The three operational baselines are named and described in method.tex sec:baselines with dispatch-floor framing and structural distinction from heuristic baselines.
2. The policy count is updated from seven to ten in experiments.tex with an explicit note that operational baselines use the same protocol without menu optimization.
3. The operational-baseline table appears in the main Results narrative via \ArtifactTable, placed between RC Outside-Option Benchmark and Cross-Instance Evaluation.
4. The interpretation paragraph explicitly states what baselines do NOT prove (no service-quality bounds, no generalization to higher-uptake regimes) and frames the dispatch-floor reference gap.
5. The limitations section restricts operational-baseline evidence scope to RC low-uptake.
6. Round 2's "artifact exists but is not integrated" criticism is addressed by the table appearing in the main results flow with full interpretation.
7. All four commits (ad71bf7, abc67db, 04b49ec, b147d01) verified as existing in the repository.

---

_Verified: 2026-05-14T15:30:00Z_
_Verifier: Claude (gsd-verifier)_
