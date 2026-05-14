# Phase 1: Operational Baseline Integration - Context

**Gathered:** 2026-05-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Make the existing insertion-cost, minimum-lateness, and random-top-k operational baselines visible and interpretable in the manuscript. These three policies are fully implemented and have artifact tables already generated, but are completely absent from the manuscript text (method, experiments, results). The phase is purely editorial LaTeX work — no new code or experiments needed.

</domain>

<decisions>
## Implementation Decisions

### Baseline Taxonomy Structure
- Fold operational baselines into the existing "Baseline Policies" section (sec:baselines) with a paragraph distinguishing "heuristic baselines" from "operational/dispatch-floor baselines" — no separate subsection.
- Update experiments.tex policy count from "seven" to reflect all policies including operational baselines.
- Use "operational baselines" label — matches artifact table label and review language.
- Brief one-line descriptions for each: insertion-cost greedy (cheapest-k by predicted cost), min-lateness (k by time deviation), random-top-k (random k-sample).

### Table Placement
- Place operational-baseline table in main Results section — review explicitly wants it visible where reviewers will see it.
- Use `operational_baselines_summary.tex` (label: tab:operational_baselines) — cleaner single-label version.
- Include both a reader-facing caption summarizing key findings AND a 2-3 sentence interpretation paragraph below the table.
- Integrate into the existing results narrative flow — add a paragraph where it naturally follows the heuristic comparison, not a standalone subsection.

### Interpretation Tone
- Explicitly state what baselines do NOT prove — they show dispatch-floor reference performance, not service-quality bounds.
- Frame comparison as "reference performance gap" — menu optimization benchmarked against what dispatch floors already achieve.
- Address Round 2's criticism indirectly — the integration itself addresses the criticism; no self-referential "we now include..." language.
- Be transparent that the table covers the RC low-uptake regime and does not span all demand conditions.

### Narrative Integration
- Add a sentence in experiments.tex noting that operational baselines use the same evaluation protocol but do not optimize the menu.
- Add a brief comparative note linking the operational-baseline table to the main results table.
- Update limitations section to note operational-baseline evidence scope (low-uptake RC only).

### Claude's Discretion
Exact paragraph wording, sentence placement order, and caption text are at Claude's discretion — the structural decisions above are the constraints.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ooh_code/artifacts/tables/operational_baselines_summary.tex` — clean artifact table with label `tab:operational_baselines`, contains RC low-uptake results for full display, strict-filter, insertion-cost greedy, min-lateness, random-top-k.
- `ooh_code/Src/Algorithms/DSPO_Menu.py` lines 785-798 — all three operational baseline policies implemented and working.
- `ooh_code/scripts/build_artifacts.py` line 1614 — `build_operational_baselines_artifacts` function generates the tables.

### Established Patterns
- Manuscript uses `\ArtifactTable{label}` to reference artifact tables from results.tex.
- Method section (sec:baselines) currently lists five heuristic baselines at lines 135-138 of method.tex.
- Experiments.tex line 12 claims "seven policies" evaluated.
- Results section has 6 subsections — operational baselines should integrate into the existing flow.

### Integration Points
- `ooh_code/manuscript/sections/method.tex` sec:baselines — add operational baseline descriptions.
- `ooh_code/manuscript/sections/experiments.tex` — update policy count and add operational-baseline evaluation note.
- `ooh_code/manuscript/sections/results.tex` — add \ArtifactTable reference and interpretation paragraph.
- `ooh_code/manuscript/sections/limitations.tex` — add operational-baseline scope note.

</code_context>

<specifics>
## Specific Ideas

- Round 2 review (line 35) explicitly states: "The operational baselines are not yet convincingly incorporated. The artifact table exists, but the manuscript's Method still describes only five empirical policies."
- The fix is straightforward: add the three baselines to method, update the count in experiments, place the table in results with interpretation, and note limitations.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>
