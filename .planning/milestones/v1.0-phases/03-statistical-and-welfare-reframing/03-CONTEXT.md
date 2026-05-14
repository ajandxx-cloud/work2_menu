# Phase 3: Statistical and Welfare Reframing - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Rework inference language and passenger-facing tradeoff analysis. Addresses reviewer Major 4 (conservative statistical presentation) and Major 5 (welfare and passenger-facing tradeoff explanation). This phase edits results.tex, managerial.tex, limitations.tex, and creates a supplementary profit decomposition table and welfare appendix material.

</domain>

<decisions>
## Implementation Decisions

### Statistical Presentation Scope
- Austin/Seattle report only raw paired split gaps with explicit "descriptive only" label — no CI language anywhere
- RC results report split-level mean, range, percentage effect, and acceptance tradeoff alongside profit gap
- Existing uncertainty table (policy_gap_uncertainty_summary.tex) relabeled to emphasize "split-level paired range" not "confidence interval"
- Add explicit parenthetical in results.tex: "Austin and Seattle each provide only two split pairs; results are reported as descriptive two-pair checks only"

### Profit Decomposition Approach
- Decompose net profit into: fare revenue, discount cost, trip cost, service cost, failure cost, and accepted request count
- Create new supplementary table with per-policy decomposition columns
- Add results.tex paragraph explaining profit-gap sources with reference to the supplementary table
- No new experiment runs needed — decomposition data available from existing pipeline outputs

### Welfare Framing
- Distinguish "all-request surplus" (includes rejected users with outside-option utility) from "accepted-user surplus" (only users who chose a menu bundle)
- Add consumer surplus formula to appendix with outside-option treatment documented
- Add explicit statement in results.tex: "Profit improvements do not automatically imply service-quality improvements when acceptance changes"
- Conclusion/managerial sections reference the dual-surplus framing

### Integration and Scope
- Results.tex gets the statistical rework (conservative labels, profit decomposition reference, welfare caveat)
- Managerial.tex gets the operational tradeoff narrative linking profit, acceptance, and service quality
- Limitations.tex gets updated with explicit surplus-formula caveat and acceptance-change interpretation note
- No changes to experiment code or new experiment runs — this phase is purely manuscript editing

### Claude's Discretion
- Exact wording choices within the above framework
- Supplementary table column formatting and layout
- Surplus formula notation and placement in appendix
- How to rephrase existing uncertainty language to be more conservative

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ooh_code/artifacts/tables/policy_gap_uncertainty_summary.tex` — existing uncertainty table to relabel
- `ooh_code/artifacts/tables/city_split_gap_table.tex` — existing city split-gap table
- `ooh_code/artifacts/tables/rc_main_optout_welfare_table.tex` — existing welfare table reference
- `ooh_code/outputs/` — pipeline outputs containing per-policy revenue/cost breakdown data
- `ooh_code/artifacts/tables/rc_main_optout_summary.tex` — main RC policy summary (source for decomposition)

### Established Patterns
- Manuscript uses booktabs table format
- Supplementary tables referenced via Table~\ref{} with appendix labels
- Sections use \textit{} for tier labels and emphasis
- Welfare/surplus language currently minimal — needs expansion

### Integration Points
- `ooh_code/manuscript/sections/results.tex` — statistical rework, profit decomposition paragraph, welfare caveat
- `ooh_code/manuscript/sections/managerial.tex` — operational tradeoff narrative
- `ooh_code/manuscript/sections/limitations.tex` — surplus formula caveat, acceptance-change note
- `ooh_code/manuscript/sections/appendix.tex` — consumer surplus formula addition
- `ooh_code/artifacts/tables/` — new profit decomposition table

</code_context>

<specifics>
## Specific Ideas

- The uncertainty table's current language may already be split-level but could use "range" instead of language implying interval estimates
- Profit decomposition may require checking if existing pipeline output logs fare revenue and cost components separately, or if these need to be reconstructed from net profit + known cost structure
- The all-request vs accepted-user surplus distinction is conceptually clean but requires careful formula treatment in appendix
- Managerial.tex already discusses filter and regime tradeoffs — the new tradeoff narrative extends this with profit-source decomposition

</specifics>

<deferred>
## Deferred Ideas

- Full bootstrap-style uncertainty quantification — reviewer explicitly flagged this as inappropriate for 2-pair cities
- Stochastic dominance analysis between policies — out of scope
- New experiment runs for additional welfare metrics — this phase reinterprets existing data

</deferred>
