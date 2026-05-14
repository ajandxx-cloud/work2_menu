# Phase 5: Submission QA and Traceability - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify compile, consistency, review-response coverage, and final readiness. Addresses requirement QA-01. This is the final phase before the milestone is complete. No experiment code or manuscript content creation — only verification, consistency checks, and traceability documentation.

</domain>

<decisions>
## Implementation Decisions

### Compile and Reference QA
- Manual LaTeX consistency review: verify all \ref{} and \citep{} resolve correctly
- Check all ArtifactTable and ArtifactFigure paths point to existing files
- Verify table captions match the manuscript claims in their respective sections
- Check for consistent terminology across all sections

### Review-Response Traceability
- Create a traceability matrix mapping each review issue (3 Critical, 5 Major, 4 Minor) to specific changes
- Format as a reviewer-facing response document
- Each entry: review concern → phase that addressed it → specific manuscript/evidence change → file location

### Claude's Discretion
- Exact format of the traceability matrix
- Whether to create a standalone response document or embed in planning docs
- Which consistency checks to prioritize

</decisions>

<code_context>
## Existing Code Insights

### Review Issues to Trace
- Critical 1: Evidence insufficient for strong claims → Phase 1
- Critical 2: MNL/outside-option calibration → Phase 2
- Critical 3: Lambert-W theoretical status ambiguous → Phase 1
- Major 1: Dispersed storyline → Phase 4
- Major 2: ETA filtering evidence → Phase 2
- Major 3: Baseline comparisons → Phase 2
- Major 4: Statistical presentation too liberal → Phase 3
- Major 5: Welfare interpretation insufficient → Phase 3
- Minor 1: Mojibake → Phase 4
- Minor 2: Abstract density → Phase 4
- Minor 3: Internal names in manuscript → Phase 4
- Minor 4: Table captions → Phase 4
- Minor 5: Reference gaps → Phase 4

</code_context>

<specifics>
## Specific Ideas

- The traceability matrix is the most valuable deliverable of this phase — it proves the revision addresses every reviewer concern
- Cross-reference checks can be done by reading all .tex files and checking every \ref and \citep
- Consistency terminology check: ensure "RC", "MNL", "ETA", "IVT" are used consistently

</specifics>

<deferred>
## Deferred Ideas

None — this is the final phase
