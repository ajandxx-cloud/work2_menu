---
phase: 01-claim-and-theory-reset
plan: 01
subsystem: manuscript
tags: [latex, claim-framing, evidence-hierarchy, diagnostic-language]

# Dependency graph
requires: []
provides:
  - "Diagnostic-framed abstract, introduction, and conclusion replacing universal-dominance language"
  - "Evidence hierarchy table moved from appendix to method section as 'Evidence Scope and Limitations' subsection"
  - "Tier labels on all five results subsections"
  - "MNL parameter caveat in method section"
  - "Expanded 'Does not support' column entries addressing Critical 1 concerns"
affects: [02-lambert-w-structural-demotion, all later phases that reference claims or evidence]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Evidence-tier parenthetical qualifiers on contribution statements"
    - "Tier labels in italics at start of results subsections"
    - "Conditional framing with 'In the studied settings' for practical lessons"

key-files:
  created: []
  modified:
    - "ooh_code/manuscript/sections/abstract.tex"
    - "ooh_code/manuscript/sections/introduction.tex"
    - "ooh_code/manuscript/sections/conclusion.tex"
    - "ooh_code/manuscript/sections/method.tex"
    - "ooh_code/manuscript/sections/results.tex"
    - "ooh_code/manuscript/sections/appendix.tex"

key-decisions:
  - "Replaced 'materially shrink' with 'can reshape' in abstract for diagnostic framing (D-01)"
  - "Replaced 'robust eligibility layer' with 'diagnostic eligibility comparison' in introduction contribution 3 (D-03)"
  - "Added inline evidence-tier qualifiers to introduction contributions 2, 3, and 4"
  - "Replaced prescriptive conclusion language with conditional framing referencing 'In the studied settings' (D-04)"
  - "Moved evidence hierarchy table from appendix to new method subsection 'Evidence Scope and Limitations' (D-05)"
  - "Added MNL parameter caveat paragraph to method section (D-07)"
  - "Expanded 'Does not support' column with Critical 1 specific concerns"
  - "Updated appendix to cross-reference main-text table instead of duplicating"

patterns-established:
  - "Evidence-tier inline tags: parenthetical qualifiers like '(mechanism-diagnostic evidence)' on contribution statements"
  - "Tier labels in results: italic bracket labels like '\\textit{[Mechanism diagnostic.]}' at start of subsections"
  - "Conditional framing: practical lessons qualified with 'In the studied settings' and explicit generalization caveats"

requirements-completed: [CLAIM-01]

# Metrics
duration: 3min
completed: 2026-05-14
---

# Phase 1 Plan 1: Claim and Evidence Reset Summary

**Diagnostic claim framing across abstract, introduction, and conclusion; evidence hierarchy table moved to method section with MNL caveat; tier labels added to all results subsections**

## Performance

- **Duration:** 3 min
- **Started:** 2026-05-14T06:38:48Z
- **Completed:** 2026-05-14T06:41:44Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- Replaced all universal-dominance claim language with diagnostic/exploratory framing across abstract, introduction, and conclusion
- Added inline evidence-tier qualifiers (mechanism-diagnostic evidence, behavioral stress-test and descriptive evidence) to three of four introduction contributions
- Moved evidence hierarchy table from appendix to new "Evidence Scope and Limitations" subsection in method, with expanded "Does not support" column entries
- Added MNL parameter caveat paragraph flagging that results are conditional on a single stylized parameterization
- Added tier labels to all five results subsections (3x mechanism diagnostic, 1x behavioral stress test, 1x descriptive external check)
- Updated appendix to cross-reference the main-text table instead of duplicating it

## Files Created/Modified
- `ooh_code/manuscript/sections/abstract.tex` - Replaced "materially shrink" with "can reshape"; added "whose gap is empirically auditable" to operational approximation phrase
- `ooh_code/manuscript/sections/introduction.tex` - Replaced "robust eligibility layer" with "diagnostic eligibility comparison"; added evidence-tier parenthetical qualifiers to contributions 2, 3, and 4
- `ooh_code/manuscript/sections/conclusion.tex` - Replaced prescriptive "Operators should audit" language with conditional framing: "In the studied settings, ETA filtering was the most impactful layer; generalization is an open question"
- `ooh_code/manuscript/sections/method.tex` - Added "Evidence Scope and Limitations" subsection with evidence hierarchy table (label: tab:evidence_hierarchy_main), expanded "Does not support" column, and MNL parameter caveat paragraph
- `ooh_code/manuscript/sections/results.tex` - Added tier labels to all 5 subsections; updated appendix table reference to tab:evidence_hierarchy_main
- `ooh_code/manuscript/sections/appendix.tex` - Replaced full evidence hierarchy table with cross-reference to main-text table

## Decisions Made
- Used "can reshape" rather than stronger alternatives to preserve directional signal while removing magnitude claim
- Kept contribution 1 (formulation) without an evidence-tier qualifier since it is a formal contribution, not empirical
- Placed the evidence scope subsection at the end of method section (after baselines) so it immediately precedes results
- Used consistent `\textit{[Tier name.]}` format for all results subsection tier labels

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All CLAIM-01 requirements addressed: claims are diagnostic/exploratory-framed, evidence hierarchy is in main text, MNL caveat is present, results carry tier labels
- Ready for Plan 01-02 (Lambert-W structural demotion) which addresses the remaining Critical 3 reviewer concern
- No blockers

---
*Phase: 01-claim-and-theory-reset*
*Completed: 2026-05-14*

## Self-Check: PASSED

All 7 files verified present on disk:
- abstract.tex, introduction.tex, conclusion.tex, method.tex, results.tex, appendix.tex
- 01-01-SUMMARY.md
