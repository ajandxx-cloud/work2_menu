# Phase 1: Claim and Theory Reset - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Reframe contribution language, integrate evidence hierarchy into main text, and structurally demote Lambert-W pricing from core contribution to one of several tested transforms. Addresses reviewer Critical 1 (evidence insufficient for strong claims) and Critical 3 (Lambert-W theoretical status ambiguous). This phase edits abstract.tex, introduction.tex, method.tex, appendix.tex, and conclusion.tex only — no experiment code or new evidence generation.

</domain>

<decisions>
## Implementation Decisions

### Claim Language Scope
- "materially shrink" in abstract → "can reshape" (diagnostic framing, acknowledges direction without claiming magnitude)
- Contribution statements in introduction → integrate evidence-tier qualifier as inline tags, e.g., "(mechanism-diagnostic evidence)" per contribution
- "robust eligibility layer" (contribution 3) → "diagnostic eligibility comparison"
- Conclusion's prescriptive "Operators should audit ETA filtering" → conditional framing: "In the studied settings, ETA filtering was the most impactful layer; generalization is an open question"

### Evidence Hierarchy Integration
- Move evidence hierarchy table from appendix to method section as subsection "Evidence scope and limitations" (before results)
- Add short parenthetical tier labels at start of each results subsection, e.g., "[Mechanism diagnostic]"
- Add explicit MNL parameter caveat in method: "Results are conditional on this parameterization and should not be interpreted as behaviorally validated predictions"
- Expand "Does not support" column entries with Critical 1's specific concerns

### Lambert-W Structural Demotion
- Rename method subsection from "Reference common-offset pricing rule" to "Pricing transforms evaluated" — present Lambert-W as one of three equal transforms (cost-plus, flat markdown, Lambert-W) with ~1 paragraph each
- Keep full Lambert-W derivation in appendix but rename to "Lambert-W Reference Transform (Supplementary)"
- Add one sentence in method noting flat markdown's empirical advantage in some calibrated regimes
- No explicit Critical 3 response paragraph — structural demotion itself is the response

### Claude's Discretion
- Specific wording choices within the above framework are at Claude's discretion
- Cross-reference formatting details (how tier labels look, exact caveat phrasing) can follow the manuscript's existing style

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- Evidence hierarchy table already exists in appendix.tex (lines 1-22) — can be moved/adapted for main text
- Lambert-W disclaimers already exist in method.tex (line 79) and appendix.tex (lines 31, 72) — can be restructured
- Introduction already has a self-limiting sentence ("deliberately narrower than a universal dominance claim") at line 12

### Established Patterns
- The manuscript uses `\textit{}` for emphasis and `\textbf{}` for key terms
- Tables use booktabs format
- Section structure follows standard TR Part E conventions

### Integration Points
- abstract.tex → main.tex via \input
- introduction.tex → main.tex via \input
- method.tex → main.tex via \input (contains MNL parameter table, pricing subsections)
- appendix.tex → main.tex via \input
- conclusion.tex → main.tex via \input

</code_context>

<specifics>
## Specific Ideas

- The manuscript is already more self-limiting than typical submissions — the primary work is structural demotion and evidence hierarchy integration, not inserting new disclaimers
- Lambert-W's prominence is a visual/structural problem (full derivation, numbered equations, default rule) more than a textual one — the disclaimers are already there but readers skip them
- Flat markdown outperforming Lambert-W in some regimes should be visible in the method section to preempt reviewer concerns about why Lambert-W is featured at all

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>
