---
phase: "05"
plan: "01"
subsystem: "manuscript-qa"
tags: [cross-references, citations, artifacts, terminology, consistency]
dependency_graph:
  requires: []
  provides: [verified-manuscript-references, verified-citations, verified-artifacts, consistent-terminology]
  affects: [abstract.tex, problem.tex]
tech_stack:
  added: []
  patterns: [grep-extraction, awk-field-split, comm-diff]
key_files:
  created:
    - .planning/phases/05-submission-qa-and-traceability/05-01-SUMMARY.md
  modified:
    - ooh_code/manuscript/sections/abstract.tex
    - ooh_code/manuscript/sections/problem.tex
decisions:
  - "Expanded MNL, RC, and ETA acronyms on first use in abstract for reader accessibility"
  - "Introduced ETA and IVT abbreviations in notation table (problem.tex) for consistent reference"
  - "Kept outside-option/outside option hyphenation as-is (correct compound-modifier pattern)"
  - "Did not remove orphaned bib entry anderson1992discrete (harmless, not a defect)"
metrics:
  duration: "4m"
  completed: "2026-05-14"
  tasks: 5
  files_modified: 2
---

# Phase 05 Plan 01: Compile, Reference, and Artifact QA Summary

Comprehensive cross-reference, citation, artifact-path, and terminology audit across the full manuscript with acronym-expansion fixes in the abstract and notation table.

## Task Results

### Task 1: Label/Reference Verification -- PASS

Extracted 36 labels from section files and 35 additional labels from artifact table files. Extracted 31 unique references from section files. Result: **zero broken references**. All `\ref{}` calls resolve to matching `\label{}` definitions.

Orphaned labels exist (defined but never referenced) but are benign -- they are section/subsection labels and artifact table labels that provide structural anchors.

### Task 2: Bibliography Citation Verification -- PASS

- 24 unique citation keys extracted from all `.tex` files
- 25 entries defined in `references.bib`
- All 24 cited keys resolve to bib entries
- 1 orphaned bib entry: `anderson1992discrete` (defined but never cited) -- harmless, not removed

### Task 3: Artifact Path Verification -- PASS

All 15 artifact files verified to exist at their expected paths relative to the manuscript directory:
- 14 artifact tables in `../artifacts/tables/` (all exist)
- 1 artifact figure in `../artifacts/figures/` (exists)

### Task 4: Terminology Consistency Check -- 4 issues found

| Item | Issue | Severity |
|------|-------|----------|
| RC | Used in abstract without expansion; defined only in experiments.tex as "RC (Clustered-Random)" | Medium |
| MNL | Used in abstract and introduction without expansion; first expanded in problem.tex | Medium |
| ETA | Never expanded to "Estimated Time of Arrival" anywhere in the manuscript | Low |
| IVT | Never expanded to "In-Vehicle Time" anywhere; used as abbreviation in scoring-weight row | Low |
| outside option / outside-option | Mixed hyphenation | No issue (correct usage pattern) |

### Task 5: Fixes Applied

**Fix 1: Abstract acronym expansion (abstract.tex)**
- "MNL assortment problem" -> "Multinomial Logit (MNL) assortment problem"
- "the RC benchmark" -> "the RC (Clustered-Random) benchmark"
- "ETA-based filtering" -> "Filtering based on estimated time of arrival (ETA)"

**Fix 2: Notation table abbreviation introduction (problem.tex)**
- "Predicted pickup ETA for bundle $b$" -> "Predicted pickup estimated time of arrival (ETA) for bundle $b$"
- "Predicted in-vehicle time for bundle $b$" -> "Predicted in-vehicle time (IVT) for bundle $b$"

## Deviations from Plan

None -- plan executed exactly as specified. All five tasks completed without requiring deviation rules.

## Build Verification

The existing build log (`build/main.log`) contains zero reference warnings, zero citation warnings, and zero multiply-defined label warnings. The fixes maintain this clean state.

## Self-Check: PASSED

- FOUND: .planning/phases/05-submission-qa-and-traceability/05-01-SUMMARY.md
- FOUND: ooh_code/manuscript/sections/abstract.tex
- FOUND: ooh_code/manuscript/sections/problem.tex
