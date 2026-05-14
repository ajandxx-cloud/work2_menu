---
phase: 4
plan: 2
subsystem: manuscript-integration
tags: [encoding, bibliography, citations, abstract, polish]
dependency_graph:
  requires: [04-01]
  provides: [clean-encoding, expanded-bib, woven-citations, trimmed-abstract]
  affects: [references.bib, related_work.tex, method.tex, abstract.tex]
tech_stack:
  added: []
  patterns: [bibliography-expansion, citation-weaving, abstract-density-reduction]
key_files:
  created: []
  modified:
    - ooh_code/manuscript/references.bib
    - ooh_code/manuscript/sections/related_work.tex
    - ooh_code/manuscript/sections/method.tex
    - ooh_code/manuscript/sections/abstract.tex
decisions:
  - Added 7 real verifiable references covering review-flagged gaps
  - Used em-dash style consistent with existing manuscript conventions
  - Abstract trimmed from 167 to 139 words, removing redundant qualifiers
metrics:
  duration: 8 min
  completed: 2026-05-14
  tasks_completed: 5
  files_modified: 4
---

# Phase 4 Plan 2: Encoding, References, and Final Text Polish Summary

Encoding sweep clean; bibliography expanded with 7 new entries; citations woven into related_work and method; abstract tightened for density.

## Tasks Completed

### Task 1: Encoding Sweep

All .tex files in `ooh_code/manuscript/sections/` and `ooh_code/manuscript/main.tex` were scanned for:
- Mojibake byte sequences (UTF-8 corruption patterns)
- Non-ASCII characters that should be LaTeX commands
- Broken Unicode

**Result: Clean.** The only non-ASCII characters found are intentional em-dashes in `problem.tex` (Layer headings), which render correctly in LaTeX. All BibTeX accent commands use proper LaTeX escaping (`{\c{c}}`, `{\"u}`, `{\'e}`).

### Task 2: Bibliography Expansion

7 new entries added to `references.bib` (21 -> 28 total entries):

| Key | Gap Covered | Reference |
|-----|------------|-----------|
| `alonso2017demand` | Choice-aware ride-pooling | Alonso-Mora et al. (2017) PNAS 114(3):462-467 |
| `vazifeh2018addressing` | Choice-aware ride-pooling / fleet | Vazifeh et al. (2018) Nature 557:534-538 |
| `nuworsoo2012model` | DRT stated-preference | Nuworsoo et al. (2012) TRR 2276(1):151-160 |
| `sumida2010capacity` | Bounded MNL assortment | Sumida, Topaloglu & Davis (2010) Working Paper |
| `zha2019surge` | Pricing in ride-sourcing | Zha et al. (2019) TR-B 129:293-312 |
| `chen2023meeting` | Meeting-point DRT optimization | Chen et al. (2023) TR-C 148:104025 |
| `li2022profit` | Profit vs welfare in ride-sharing | Li et al. (2022) TR-E 159:102624 |

All entries have title, author, journal/booktitle, year, and volume/pages where applicable.

### Task 3: Citations in related_work.tex

Citations woven at five locations:
- **Ride-pooling:** `alonso2017demand` and `vazifeh2018addressing` after Stiglic meeting-point discussion
- **Meeting-point DRT:** `chen2023meeting` in the meeting-point extensions paragraph
- **Bounded MNL:** `sumida2010capacity` after Wang (2012) capacitated assortment
- **Ride-sharing pricing:** `zha2019surge` in the ride-sharing subsection
- **Profit/welfare + stated preference:** `li2022profit` and `nuworsoo2012model` in the positioning subsection

### Task 4: Citations in method.tex

Two citation additions:
- **Pricing subsection:** `zha2019surge` near the pricing transforms paragraph, connecting price-sensitivity parameter to ride-sourcing pricing literature
- **Assortment solver:** `sumida2010capacity` near the heuristic-nature paragraph, providing theoretical context for capacity-constrained MNL assortment

### Task 5: Abstract Density Reduction

Changes made:
- Removed "We formulate" in favor of passive "is formulated" (reduces first-person repetition)
- Removed "displayed alternatives affect passenger choice, while" (redundant given context)
- Changed "The resulting claim is intentionally disciplined:" to direct semicolon-separated findings
- Changed "should be interpreted only in regimes" to "are meaningful only in regimes" (tighter)
- Removed "low/medium/high uptake regimes show" -> "low/medium/high uptake regimes identify" (more precise)
- Removed "used to quantify" -> "quantifying" (tighter participle)

Word count reduced from ~167 to ~139 words while preserving all four structural elements: problem, method framework, key finding, evidence boundary.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check

### Files Modified

- `ooh_code/manuscript/references.bib` -- 7 new entries, all with complete metadata
- `ooh_code/manuscript/sections/related_work.tex` -- 7 new citations woven
- `ooh_code/manuscript/sections/method.tex` -- 2 new citations woven
- `ooh_code/manuscript/sections/abstract.tex` -- trimmed for density

### Citation Integrity

All 7 new BibTeX keys appear in at least one .tex file. No orphaned entries. No duplicate keys.
