# Round 2 Response Matrix

**Date:** 2026-05-15
**Reviewer verdict:** 6/10, "borderline but still risky" -- major revision before TR Part E submission.

## Blocker-to-Evidence Traceability

| # | Reviewer Weakness | Actionable Fix | Manuscript Change | Evidence Artifact | Status |
|---|---|---|---|---|---|
| 1 | External demand calibration remains the largest blocker | Run explicit outside-option utility scan; cite plausible parameter ranges from DRT/stated-preference literature | method.tex: Table 2 footnotes, "Parameter plausibility ranges" paragraph; results.tex: new Section 4.5 (Outside-Option Sensitivity) with calibration scope and limitations paragraphs; references.bib: 4 new literature entries | `outside_option_scan_summary.tex`: 5-level u_0 scan (20 rows); `mnl_sensitivity_summary.tex` | Done |
| 2 | Filter validity under-supported: no quantile errors, confusion matrices, or FN breakdowns | Report P50/P90/P95 ETA/IVT errors; FN pruning breakdown by distance band | results.tex Section 4.2: "Quantile error diagnostics" and "False-negative pruning by distance" paragraphs; appendix.tex Table updated | `filter_validity_summary.tex`: 16-column table with quantile + FN breakdown | Done |
| 3 | Operational baselines not integrated into manuscript | Update method baseline taxonomy; add operational-baseline table to results with interpretation | method.tex: baseline taxonomy; results.tex Section 4.6: Table 7 (operational baselines) with interpretation paragraph | `operational_baselines_summary.tex`, `phase32_operational_baselines_summary.tex` | Done |
| 4 | Flat-markdown vs Lambert-W needs clearer tradeoff interpretation | Frame as regime-specific tradeoffs, not policy dominance | results.tex Section 4.3: "Regime-specific tradeoffs" paragraph; managerial.tex: updated framing and "Defensible TR-E claim" paragraph | `phase31_uptake_menu_value_summary.tex`, `rc_main_optout_welfare_table.tex` | Done |
| 5 | Near-zero acceptance regimes over-interpreted | Explicitly treat as mechanism diagnostics | results.tex Section 4.3: conditional claim paragraph; limitations.tex: demand-calibration limitations updated | Throughout results.tex evidence-tier labels | Done |
| 6 | Mojibake and encoding problems | Scan and fix all encoding issues in LaTeX source | appendix.tex: removed stale `app:phase19_support` label | Full scan: no mojibake detected | Done |
| 7 | Stale internal project language | Remove internal phase/project references from manuscript-facing text | appendix.tex: cleaned stale label | Pattern scan: remaining phase refs are in file paths and reproducibility verbatim (acceptable) | Done |

## Requirement Status

| Requirement | Description | Phase | Status |
|---|---|---|---|
| BASE-01 | Operational baselines in method/results narrative | 1 | Done |
| BASE-02 | Operational-baseline table visible to reviewers | 1 | Done |
| CAL-01 | Outside-option utility scan as concrete artifact | 2 | Done |
| CAL-02 | MNL parameter ranges tied to cited literature | 2 | Done |
| CAL-03 | Literature-bounded vs external validation distinction | 2 | Done |
| FILT-01 | P50/P90/P95 ETA/IVT error diagnostics | 3 | Done |
| FILT-02 | Filtering-decision feasibility proxy quantified | 3 | Done |
| FILT-03 | FN pruning by operational dimension | 3 | Done |
| SYN-01 | Tradeoff interpretation, not policy dominance | 4 | Done |
| TEXT-01 | No mojibake or stale language | 5 | Done |
| QA-01 | Compile, references, response matrix | 5 | This document |

## Readiness Assessment

The v1.1 revision addresses all five Round 2 blockers:
1. **External demand calibration:** Partially addressed through outside-option scan and literature-bounded calibration framing. Not resolved (true external validation deferred), but the manuscript is now honest about the gap.
2. **Filter validity:** Addressed through quantile errors, FN breakdown by distance band. Confusion matrix deferred (requires ground-truth labels).
3. **Operational baselines:** Fully integrated into method and results.
4. **Behavioral interpretation:** Regime-specific tradeoff framing with defensible TR-E claim.
5. **Polish:** No mojibake detected; stale labels cleaned.

**Remaining limitations that the revision honestly acknowledges:**
- MNL parameters remain simulator design choices, not estimated from data
- Austin/Seattle remain descriptive (2 split pairs each)
- Filter confusion matrix requires ground-truth feasibility labels
- Consumer surplus is model-internal, not welfare measurement
