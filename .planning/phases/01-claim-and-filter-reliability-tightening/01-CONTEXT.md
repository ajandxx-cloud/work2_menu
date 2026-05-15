# Phase 1: Claim and Filter-Reliability Tightening - Context

**Gathered:** 2026-05-15
**Status:** Ready for planning

<domain>
## Phase Boundary

Soften outside-option claims and directly address large ETA/IVT errors in the manuscript. Two specific requirements: CLAIM-02 (soften "stable" language to "not obviously brittle within this RC stress test") and FILT-04 (explain why large ETA/IVT errors do not fully invalidate the filtering diagnostic, or name as key limitation).

Key files: `ooh_code/manuscript/sections/results.tex` (lines 53, 64 use "stable"; lines 24-28 have quantile diagnostics), `ooh_code/manuscript/sections/limitations.tex` (filter validity already partially addressed), `ooh_code/manuscript/sections/conclusion.tex` (check for consistency).

</domain>

<decisions>
## Implementation Decisions

### Outside-Option Claim Softening
- Soften both "stable" instances: MNL sensitivity section (line 53) and outside-option scan section (line 64) in results.tex
- Replace "stable" with "directionally consistent" — conveys the finding without claiming stability
- Keep calibration-scope paragraph (line 67) as-is — already clearly states "literature-bounded sensitivity testing, not external demand validation"
- Add minor clarification to limitations paragraph: explicitly say the scan shows "no obvious brittleness" rather than external robustness

### Large ETA/IVT Error Framing
- Address in both results.tex and limitations.tex — results explains mechanism, limitations names it as constraint
- Dual framing: explain filtering remains useful because FN pruning concentrates in far band (nearby points preserved), while naming large errors as key limitation
- Use "a key limitation" language explicitly in limitations section
- Add 1-2 sentences to results quantile paragraph (lines 24-28) explaining why large errors don't invalidate near-band FN finding

### Cross-Section Consistency
- No abstract change needed
- Check and align conclusion.tex — if conclusion restates stability, soften there too
- No method section change — method describes mechanism, not empirical claim strength
- Quick scan of table captions for "stable" or similar overclaiming language

### Claude's Discretion
Specific wording and sentence structure choices are at Claude's discretion within the above constraints.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ooh_code/artifacts/tables/filter_validity_summary.tex` — quantile diagnostics table (ETA P95 ~3,600s, IVT P95 ~3,370s, FN far-band rate ~8.4-8.7)
- `ooh_code/artifacts/tables/outside_option_scan_summary.tex` — outside-option scan across five u0 levels
- `ooh_code/artifacts/tables/mnl_sensitivity_summary.tex` — MNL regime sensitivity

### Established Patterns
- Results sections use italic tier labels like `\textit{[Behavioral stress test.]}`
- Quantile diagnostics already reference P50/P90/P95 explicitly
- Limitations section uses careful hedging language throughout
- Tables are included via `\ArtifactTable{}` command

### Integration Points
- `results.tex` Section 5.5 (Outside-Option Sensitivity) — main softening target
- `results.tex` Section 5.2 (Robust ETA Filtering) — quantile error paragraph
- `limitations.tex` — filter validity paragraph (paragraph 2) and demand calibration paragraph (paragraph 4)
- `conclusion.tex` — check for any stability restatement

</code_context>

<specifics>
## Specific Ideas

The review's exact language for outside-option softening: "not obviously brittle within this RC stress test" — use this as a guiding phrase but "directionally consistent" as the primary replacement term per user acceptance.

For filter errors: the near-band FN rate (<500m) is 0.011-0.035, far-band (>1500m) is 8.4-8.7 — this concentration pattern is the key argument for why filtering remains useful despite large errors.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.
