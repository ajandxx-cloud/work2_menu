# Phase 4: Manuscript Integration - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Integrate revised narrative, tables, captions, terminology, references, and encoding fixes. Addresses reviewer Major 1 (dispersed storyline) and Minor 1-5 (mojibake, abstract density, internal names, table captions, reference gaps). This phase edits all manuscript .tex files but no experiment code.

</domain>

<decisions>
## Implementation Decisions

### Internal Name Replacement
- All phase numbers in prose replaced with descriptive labels ("exact-vs-greedy study", "robust-filtering study", "uptake-regime study", "MNL sensitivity study")
- Table LaTeX labels renamed to reader-facing labels with backward-compatible aliases where needed
- Appendix verbatim blocks (reproducibility CLI commands) keep phase names since they are literal commands
- Code variable names (menu_optimization etc.) remain in texttt but get reader-facing description on first use

### Bibliography Expansion
- Add 5-8 new references covering: choice-aware ride-pooling, DRT stated preference calibration, bounded MNL pricing, service quality/profit tradeoffs, meeting-point computational studies
- Citations woven into related_work.tex and method.tex where they provide context

### Narrative Compression
- Add a brief paragraph at the start of experiments section framing the three-experiment structure: mechanism diagnostics, filtering diagnostics, behavioral stress tests + descriptive external checks
- No section restructuring — the paragraph unifies the storyline

### Encoding and Captions
- Final encoding sweep across all .tex files, fix any mojibake
- Update table captions to journal-facing language (replace "outside-option evaluation setup" with descriptive terms, add first-use explanations)

### Claude's Discretion
- Exact replacement labels for phase-numbered references
- Which specific references to add (must cover the review-flagged gaps)
- Exact caption wording improvements
- How to handle abstract density (Minor 2)

</decisions>

<code_context>
## Existing Code Insights

### Files with Internal Names
- `experiments.tex` lines 20, 37-38: phase29, phase30, phase31, phase27 in prose
- `results.tex` lines 11, 13, 20, 22, 29, 31: phase names in table labels and ArtifactTable paths
- `appendix.tex` line 119: "Phase 19" reference in prose
- `appendix.tex` lines 172-186: phase names in verbatim blocks (keep as-is)

### Caption Issues
- "outside-option evaluation setup" in rc_main_optout_summary.tex caption
- "benchmark-role bridge" in benchmark_bridge_summary.tex caption
- Several tables use "RC benchmark" without defining it for first-time readers

### Reference Gaps
- Missing: choice-aware ride-pooling assignment, DRT stated-preference, bounded MNL pricing, service quality/profit tradeoffs, recent meeting-point computational studies
- Current bib has 16 entries, mostly DARP, MNL assortment, HGS, and meeting-point ride-sharing

### Established Patterns
- The manuscript uses booktabs table format
- Section structure follows standard TR Part E conventions
- Captions should be self-contained (TR Part E requirement)

</code_context>

<specifics>
## Specific Ideas

- The experiments.tex companion-studies paragraph is the densest concentration of internal names — rewriting it as a unified study-structure paragraph solves both Major 1 and Minor 3 simultaneously
- Table labels in results.tex (tab:phase29_exact_greedy_gap etc.) can use \providecommand to maintain backward compatibility
- The review's Minor 2 (abstract density) can be addressed by trimming redundant qualifications from the abstract — Phase 1 already added evidence-tier language
- Mojibake may have been cleaned already; verify with binary search of problematic byte sequences

</specifics>

<deferred>
## Deferred Ideas

None — this phase covers all Minor 1-5 issues
