---
phase: 04-manuscript-integration
verified: 2026-05-14T12:00:00Z
status: human_needed
score: 5/5 must-haves verified
overrides_applied: 0
human_verification:
  - test: "Read the abstract aloud in one pass and verify it communicates problem, method, finding, and evidence boundary without requiring re-reading"
    expected: "A reader unfamiliar with the paper can state the problem, method, key mechanism finding, and evidence boundary after a single reading"
    why_human: "Abstract readability and flow are subjective qualities that cannot be verified programmatically"
  - test: "Read experiments.tex study-structure paragraph and confirm the three-tier organization is immediately clear to a journal reader"
    expected: "A transportation researcher can identify the three tiers and their evidence roles without prior knowledge of the project"
    why_human: "Narrative clarity and journal-readability are human-judgment qualities"
  - test: "Read the full manuscript sequentially and assess whether it reads as a self-contained journal article rather than an internal experiment report"
    expected: "No sentence or paragraph requires knowledge of internal project phases, code directory names, or pipeline numbering to understand"
    why_human: "Overall manuscript tone and reader-facing quality requires human reading and judgment"
---

# Phase 4: Manuscript Integration Verification Report

**Phase Goal:** Integrate revised narrative, tables, captions, terminology, references, and encoding fixes.
**Verified:** 2026-05-14
**Status:** human_needed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Internal names such as phase-numbered studies are replaced by reader-facing study labels in the manuscript | VERIFIED | Zero matches for `Phase \d+` or `phase\d+_` in prose across all 11 manuscript section files. `experiments.tex` uses descriptive suite names ("MNL sensitivity suite", "exact-vs-greedy suite", "robust-filtering suite", "uptake-regime suite"). `results.tex` uses reader-facing `\ref{tab:exact_greedy_gap}`, `\ref{tab:robust_filtering}`, `\ref{tab:uptake_menu_value}`. Remaining phase-numbered references are limited to: (a) artifact file paths in `\ArtifactTable{}` calls (expected -- they reference actual files), (b) backward-compatible `\label{app:phase19_support}` kept alongside new `\label{app:split_uncertainty}` (line 117, appendix), (c) verbatim code blocks in appendix reproducibility section (lines 172-187, intentional). |
| 2 | Mojibake characters are removed from manuscript source files | VERIFIED | Grep for mojibake patterns (U+00C3, smart-quote corruption, Chinese replacement characters) across all .tex files in `sections/` and .bib file returned zero matches. The only non-ASCII content is intentional em-dashes in `problem.tex`, which render correctly in LaTeX. |
| 3 | Captions and table names use journal-facing language | VERIFIED | `rc_main_optout_summary.tex` caption: "Policy comparison on the RC benchmark under the outside-option evaluation setup, where passengers may reject all offered bundles..." (explains setup, not just terse labels). `benchmark_bridge_summary.tex` caption: "Evidence-role summary separating the RC mechanism benchmark...from the Austin and Seattle impact benchmarks..." (explains roles). `mnl_sensitivity_summary.tex` caption: "MNL-regime sensitivity summary across low, medium, and higher-uptake RC regimes..." (no internal phase references). All artifact table captions verified. |
| 4 | Missing reference directions are covered or explicitly deferred | VERIFIED | Review flagged 5 reference directions in section "6. Missing References". All 5 are covered: (1) choice-aware ride-pooling -- `alonso2017demand`, `vazifeh2018addressing` in `related_work.tex` line 9; (2) DRT stated-preference -- `nuworsoo2012model` in `related_work.tex` line 33; (3) bounded MNL assortment -- `sumida2010capacity` in `related_work.tex` line 17 and `method.tex` line 120; (4) meeting-point DRT computational -- `chen2023meeting` in `related_work.tex` line 11; (5) profit/welfare tradeoff -- `li2022profit`, `zha2019surge` in `related_work.tex` lines 23, 33 and `method.tex` lines 60. All 7 new BibTeX keys confirmed present in `references.bib` and cited in at least one .tex file. No orphaned entries. |
| 5 | The manuscript reads as a journal article rather than an internal experiment report | VERIFIED (automated checks) | No phase-numbered prose in any section. No TODO/FIXME/PLACEHOLDER markers. Code variable names have reader-facing descriptions on first use (`\texttt{menu\_optimization}` described as "the strict-filter menu-optimization policy", `\texttt{menu\_optimization\_v2}` as "the no-filter variant"). Study-structure paragraph organizes evidence into reader-facing tiers with italicized tier names. Abstract trimmed to ~149 words with passive voice replacing first-person repetition. Final readability assessment deferred to human verification. |

**Score:** 5/5 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `ooh_code/manuscript/sections/experiments.tex` | Unified study-structure paragraph, no phase numbers in prose | VERIFIED | Line 20: three-tier paragraph present. Lines 37-40: descriptive suite names. No phase-numbered prose references. |
| `ooh_code/manuscript/sections/results.tex` | Reader-facing table labels | VERIFIED | Uses `\ref{tab:exact_greedy_gap}`, `\ref{tab:robust_filtering}`, `\ref{tab:uptake_menu_value}`. Zero `\ref{tab:phase*}` references. |
| `ooh_code/manuscript/sections/appendix.tex` | No phase numbers in prose (verbatim OK) | VERIFIED | Line 117: backward-compatible label only. Lines 172-187: verbatim code blocks (acceptable). No phase numbers in running prose. |
| `ooh_code/manuscript/sections/related_work.tex` | New citations woven | VERIFIED | 5 citation locations confirmed: `alonso2017demand`, `vazifeh2018addressing` (line 9), `chen2023meeting` (line 11), `sumida2010capacity` (line 17), `zha2019surge` (line 23), `li2022profit` + `nuworsoo2012model` (line 33). |
| `ooh_code/manuscript/sections/method.tex` | New citations woven | VERIFIED | `zha2019surge` at line 60 (pricing subsection), `sumida2010capacity` at line 120 (heuristic-nature paragraph). |
| `ooh_code/manuscript/sections/abstract.tex` | Trimmed for density | VERIFIED | ~149 words. Removed verbose phrases confirmed absent: "We formulate", "displayed alternatives affect", "should be interpreted only", "used to quantify". |
| `ooh_code/manuscript/references.bib` | Expanded with 7 new entries | VERIFIED | 28 total entries. All 7 new keys present: `alonso2017demand`, `vazifeh2018addressing`, `nuworsoo2012model`, `sumida2010capacity`, `zha2019surge`, `chen2023meeting`, `li2022profit`. Each has title, author, journal/booktitle, year, volume/pages. |
| `ooh_code/artifacts/tables/rc_main_optout_summary.tex` | Journal-facing caption | VERIFIED | Caption explains outside-option setup, gap/win-rate computation against full display, and split-level evaluation. |
| `ooh_code/artifacts/tables/benchmark_bridge_summary.tex` | Journal-facing caption | VERIFIED | Caption explains RC mechanism role vs city impact benchmarks, gate status, and bridge-use column. |
| `ooh_code/artifacts/tables/phase29_exact_greedy_gap_summary.tex` | Backward-compatible label | VERIFIED | Both `\label{tab:phase29_exact_greedy_gap}` and `\label{tab:exact_greedy_gap}` present. |
| `ooh_code/artifacts/tables/phase30_robust_filtering_summary.tex` | Backward-compatible label | VERIFIED | Both `\label{tab:phase30_robust_filtering}` and `\label{tab:robust_filtering}` present. |
| `ooh_code/artifacts/tables/phase31_uptake_menu_value_summary.tex` | Backward-compatible label | VERIFIED | Both `\label{tab:phase31_uptake_menu_value}` and `\label{tab:uptake_menu_value}` present. |
| `ooh_code/artifacts/tables/phase32_operational_baselines_summary.tex` | Backward-compatible label | VERIFIED | Both `\label{tab:phase32_operational_baselines}` and `\label{tab:operational_baselines_paired}` present. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `results.tex` | `phase29_exact_greedy_gap_summary.tex` | `\ref{tab:exact_greedy_gap}` in prose, `\ArtifactTable{}` with file path | WIRED | Line 13 references `tab:exact_greedy_gap`; artifact file has matching label. |
| `results.tex` | `phase30_robust_filtering_summary.tex` | `\ref{tab:robust_filtering}` in prose, `\ArtifactTable{}` with file path | WIRED | Line 22 references `tab:robust_filtering`; artifact file has matching label. |
| `results.tex` | `phase31_uptake_menu_value_summary.tex` | `\ref{tab:uptake_menu_value}` in prose, `\ArtifactTable{}` with file path | WIRED | Line 31 references `tab:uptake_menu_value`; artifact file has matching label. |
| `related_work.tex` | `references.bib` | `\citet{}`, `\citep{}` citations | WIRED | All 7 new BibTeX keys appear in related_work via cite commands. |
| `method.tex` | `references.bib` | `\citep{}` citations | WIRED | `zha2019surge` (line 60), `sumida2010capacity` (line 120) both have matching bib entries. |
| `appendix.tex` | `phase19_support` / `split_uncertainty` | `\label{}` entries | WIRED | Both labels present on line 117-118. Cross-references from main text resolve to `\ref{app:split_uncertainty}`. |
| `main.tex` | All section files | `\input{}` commands | WIRED | Lines 65-73, 79 include all sections in correct order. |

### Data-Flow Trace (Level 4)

Not applicable -- this phase is a manuscript text-editing phase, not a data-pipeline phase. No dynamic data flows through these artifacts.

### Behavioral Spot-Checks

Step 7b: SKIPPED (no runnable entry points). This phase modifies LaTeX manuscript source files; there are no executable code artifacts to test.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| TEXT-01 | 04-01, 04-02 | Manuscript removes phase-number/internal pipeline language and fixes mojibake encoding issues | SATISFIED | Phase numbers removed from all prose; encoding sweep clean; terminology reader-facing; captions journal-facing; 7 references added covering all flagged gaps. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | -- | -- | -- | No anti-patterns found across all 9 key files. Zero TODO/FIXME/PLACEHOLDER markers. No empty implementations. No hardcoded stubs. |

### Human Verification Required

### 1. Abstract Readability Test

**Test:** Read the abstract (in `ooh_code/manuscript/sections/abstract.tex`) aloud in a single pass.
**Expected:** A transportation researcher unfamiliar with the paper can identify: (a) the problem (service-menu optimization for DRT), (b) the method framework (MNL assortment with exact-small/greedy-large), (c) the key mechanism finding (tiered evidence with uptake-regime conditioning), and (d) the evidence boundary (results meaningful only where acceptance is observable).
**Why human:** Abstract readability, flow, and information density are subjective qualities that require human judgment. The automated word count (149 words) and absence of verbose phrases confirms mechanical trimming, but whether the result communicates effectively requires reading.

### 2. Study-Structure Paragraph Clarity

**Test:** Read the study-structure paragraph in `experiments.tex` (lines 20) and assess whether the three-tier organization (mechanism diagnostics, behavioral stress tests, descriptive external checks) is immediately clear.
**Expected:** A journal reader can distinguish the three tiers and understand which evidence supports which type of claim without re-reading.
**Why human:** Paragraph organization clarity and reader-friendliness are human-judgment qualities. The paragraph exists and uses italicized tier names, but whether the flow is natural for a journal reader requires human assessment.

### 3. Full-Manuscript Journal-Readability Assessment

**Test:** Read the full manuscript sequentially (all sections via `main.tex`) and assess whether it reads as a self-contained journal article.
**Expected:** No paragraph or sentence requires knowledge of internal project phases, code directory structures, or pipeline numbering to understand. The manuscript stands alone as a journal submission.
**Why human:** Overall manuscript tone, narrative coherence, and journal-readability are inherently human-judgment qualities. Automated checks confirmed the absence of internal names, but holistic readability requires human assessment.

### Gaps Summary

No gaps found. All 5 success criteria are substantively met by the codebase evidence:

- **SC1 (reader-facing labels):** Zero phase-numbered prose references in any manuscript section. Descriptive suite names replace all internal labels. Backward-compatible labels preserved for LaTeX cross-references.
- **SC2 (mojibake removed):** Encoding sweep across all .tex and .bib files returned zero matches for corruption patterns.
- **SC3 (journal-facing captions):** All artifact table captions explain their content in plain language without internal references.
- **SC4 (reference gaps covered):** All 5 review-flagged reference directions have at least one new citation. 7 new BibTeX entries, all cited in text, no orphans.
- **SC5 (journal article quality):** Automated checks confirm absence of internal language, placeholders, and verbose construction. Final readability requires human confirmation.

The phase has one requirement (TEXT-01) which is fully satisfied.

---

_Verified: 2026-05-14T12:00:00Z_
_Verifier: Claude (gsd-verifier)_
