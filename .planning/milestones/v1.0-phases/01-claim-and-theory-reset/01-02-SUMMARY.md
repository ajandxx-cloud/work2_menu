---
phase: 01-claim-and-theory-reset
plan: 02
subsystem: manuscript
tags: [latex, lambert-w, structural-demotion, pricing-transforms]

# Dependency graph
requires:
  - phase: 01-claim-and-theory-reset
    provides: "Prior wave (01-01) established diagnostic framing and evidence hierarchy in main text"
provides:
  - "Pricing subsection restructured as three equal transforms (cost-plus, flat-markdown, Lambert-W) under 'Pricing transforms evaluated'"
  - "Flat-markdown empirical advantage over Lambert-W noted in method text"
  - "Lambert-W presented last and with appendix forward reference"
  - "Appendix section renamed to 'Lambert-W Reference Transform (Supplementary)'"
affects: [all later phases that reference pricing transforms or Lambert-W]

# Tech tracking
tech-stack:
  added: []
patterns:
  - "Symmetric presentation of pricing transforms with no featured/default rule"
  - "Empirical caveat on Lambert-W via flat-markdown advantage sentence"
  - "Supplementary framing of appendix derivation section"

key-files:
  created: []
  modified:
    - "ooh_code/manuscript/sections/method.tex"
    - "ooh_code/manuscript/sections/appendix.tex"

key-decisions:
  - "Presented three pricing transforms as \\emph{} sub-paragraphs under single \\paragraph{Pricing transforms evaluated.} header (D-09)"
  - "Flat-markdown placed second with explicit outperforming sentence over Lambert-W (D-11)"
  - "Lambert-W placed third and last with condensed heuristic disclaimer and appendix forward reference (D-10)"
  - "Renamed appendix section from 'Common-Offset Pricing Reference' to 'Reference Transform (Supplementary)' (D-10)"
  - "No explicit reviewer-response paragraph added; structural demotion is the response (D-12)"

patterns-established:
  - "Equal-footing pricing transform presentation: three rules in sequence with no default or featured rule"
  - "Regime-dependent caveat: flat-markdown outperforming Lambert-W noted explicitly in method"

requirements-completed: [THEORY-01]

# Metrics
duration: 2min
completed: 2026-05-14
---

# Phase 1 Plan 2: Lambert-W Structural Demotion Summary

**Method section restructured to present cost-plus, flat-markdown, and Lambert-W as three equal pricing transforms; Lambert-W moved to last position with appendix forward reference; appendix renamed to 'Supplementary' framing**

## Performance

- **Duration:** 2 min
- **Started:** 2026-05-14T06:43:46Z
- **Completed:** 2026-05-14T06:45:28Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Restructured pricing subsection: removed "Reference common-offset pricing rule" header, replaced with "Pricing transforms evaluated" as umbrella for all three transforms
- Reordered transforms: cost-plus first (simplest baseline), flat-markdown second (with empirical advantage note), Lambert-W third and last (condensed with appendix reference)
- Added explicit sentence noting flat-markdown outperforms Lambert-W in some calibrated uptake regimes
- Condensed Lambert-W heuristic disclaimer to one sentence with forward reference to Appendix~\ref{app:lambertw}
- Renamed appendix section from "Lambert-W Common-Offset Pricing Reference" to "Lambert-W Reference Transform (Supplementary)"
- Preserved all equation labels (eq:lambertw, eq:price) and cross-references (app:lambertw)

## Files Created/Modified
- `ooh_code/manuscript/sections/method.tex` - Restructured pricing paragraphs (lines 60-89 rewritten): three equal transforms under "Pricing transforms evaluated" heading; cost-plus first, flat-markdown second with outperforming note, Lambert-W third and last with condensed disclaimer and appendix reference
- `ooh_code/manuscript/sections/appendix.tex` - Renamed Lambert-W section title from "Lambert-W Common-Offset Pricing Reference" to "Lambert-W Reference Transform (Supplementary)"; label app:lambertw preserved; all derivation content unchanged

## Decisions Made
- Used \emph{} sub-paragraphs for each transform rather than nested \paragraph{} to maintain equal visual weight within the single "Pricing transforms evaluated" paragraph
- Kept the introductory sentence about shared evaluation conditions (same costs, feasible-set logic, scoring, clipping) as the umbrella paragraph before the three transforms
- Condensed the Lambert-W disclaimer from its original multi-sentence form to one sentence plus the appendix forward reference, since the appendix already contains the full derivation and disclaimers
- Did not add any reviewer-response language; the structural demotion itself addresses Critical 3

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- THEORY-01 requirement addressed: Lambert-W is now presented as one of three equal pricing transforms, not as a core contribution
- Combined with 01-01 (CLAIM-01), Phase 1 is now complete
- Ready for Phase 2 execution
- No blockers

---
*Phase: 01-claim-and-theory-reset*
*Completed: 2026-05-14*

## Self-Check: PASSED

All 3 files verified present on disk:
- method.tex (restructured pricing subsection)
- appendix.tex (renamed Lambert-W section)
- 01-02-SUMMARY.md
