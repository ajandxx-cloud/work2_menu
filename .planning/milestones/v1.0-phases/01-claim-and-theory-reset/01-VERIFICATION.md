---
phase: 01-claim-and-theory-reset
verified: 2026-05-14T07:00:00Z
status: passed
score: 10/10 must-haves verified
overrides_applied: 0
---

# Phase 1: Claim and Theory Reset Verification Report

**Phase Goal:** Reframe contribution, evidence hierarchy, and Lambert-W theory before experiments are expanded.
**Verified:** 2026-05-14T07:00:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

Truths are merged from ROADMAP success criteria (4 items) and PLAN frontmatter must-haves (6 truths from Plan 01 + 5 truths from Plan 02, deduplicated with roadmap SCs).

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Abstract, introduction, and conclusion no longer imply unsupported universal dominance (ROADMAP SC-1) | VERIFIED | abstract.tex: "materially shrink" removed (0 hits), replaced with "can reshape" (1 hit). introduction.tex: "robust eligibility layer" removed (0 hits), replaced with "diagnostic eligibility comparison" (1 hit); self-limiting sentence "deliberately narrower than a universal dominance claim" retained at line 11. conclusion.tex: "In the studied settings" present (1 hit); "generalization...open question" present (1 hit). |
| 2 | Evidence hierarchy is visible in the main text and separates diagnostic, stress-test, and descriptive evidence (ROADMAP SC-2) | VERIFIED | method.tex lines 140-166: subsection "Evidence Scope and Limitations" present with label sec:evidence_scope. Table tab:evidence_hierarchy_main defines 4 tiers: Mechanism diagnostic, Behavioral stress test, Descriptive external check, Archival diagnostic. "Does not support" column expanded with Critical 1 specific language. MNL caveat paragraph at line 165. |
| 3 | Lambert-W pricing is described as a bounded reference transform tested against alternatives (ROADMAP SC-3) | VERIFIED | method.tex: "Pricing transforms evaluated" paragraph (line 60) presents 3 equal transforms: cost-plus (lines 62-66), flat-markdown (lines 68-72), Lambert-W last (lines 74-88). Lambert-W described as "implemented common-offset pricing heuristic, not the exact optimizer." Appendix section renamed to "Lambert-W Reference Transform (Supplementary)" (appendix.tex line 10). |
| 4 | Reviewer Critical 1 and Critical 3 each have a clear manuscript response path (ROADMAP SC-4) | VERIFIED | Critical 1 path: diagnostic framing in abstract/intro/conclusion, evidence hierarchy table in method with expanded "Does not support" column, MNL caveat, tier labels on results subsections. Critical 3 path: Lambert-W structurally demoted to third of three equal pricing transforms, flat-markdown advantage noted, appendix renamed to "Supplementary", no explicit reviewer-response paragraph (structural demotion is the response). |
| 5 | Introduction contribution statements carry inline evidence-tier qualifiers (PLAN 01 truth) | VERIFIED | introduction.tex line 9: contributions 2 and 3 carry "(mechanism-diagnostic evidence)", contribution 4 carries "(behavioral stress-test and descriptive evidence)". Contribution 1 (formal) has no tier qualifier as designed. |
| 6 | Each results subsection has a short tier label at its start (PLAN 01 truth) | VERIFIED | results.tex: 5 subsections, 5 tier labels. Exact-vs-Greedy (line 9): Mechanism diagnostic. Robust ETA Filtering (line 18): Mechanism diagnostic. Uptake-Regime Menu Value (line 27): Behavioral stress test. RC Outside-Option Benchmark (line 35): Mechanism diagnostic. Cross-Instance Evaluation (line 45): Descriptive external check. |
| 7 | Method section presents Lambert-W as one of three equal pricing transforms (PLAN 02 truth) | VERIFIED | method.tex lines 60-88: single paragraph header "Pricing transforms evaluated", three emph sub-paragraphs -- cost-plus first, flat-markdown second, Lambert-W third and last. Each transform receives comparable space. |
| 8 | Method section includes a sentence noting flat markdown's empirical advantage in some calibrated regimes (PLAN 02 truth) | VERIFIED | method.tex line 72: "Notably, the flat-markdown rule outperforms the Lambert-W transform in some calibrated uptake regimes, suggesting that the closed-form optimization does not always dominate simpler alternatives." |
| 9 | Appendix Lambert-W section is titled "Lambert-W Reference Transform (Supplementary)" (PLAN 02 truth) | VERIFIED | appendix.tex line 10: section title matches exactly. Old title "Lambert-W Common-Offset Pricing Reference" removed (0 hits). Label app:lambertw preserved. |
| 10 | MNL parameter caveat is present in method.tex stating results are conditional on the parameterization (PLAN 01 truth) | VERIFIED | method.tex line 165: "Results are conditional on the MNL parameterization reported in Table~\ref{tab:mnl_params} and should not be interpreted as behaviorally validated predictions." |

**Score:** 10/10 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `ooh_code/manuscript/sections/abstract.tex` | Diagnostic-framed abstract containing "can reshape" | VERIFIED | 1 line, contains "can reshape", no "materially shrink" |
| `ooh_code/manuscript/sections/introduction.tex` | Evidence-tier-qualified contributions containing "diagnostic eligibility comparison" | VERIFIED | 1 instance of "diagnostic eligibility comparison", 1 instance of "mechanism-diagnostic" evidence tag, 1 instance of "behavioral stress-test and descriptive evidence" |
| `ooh_code/manuscript/sections/conclusion.tex` | Conditionally framed conclusion containing "In the studied settings" | VERIFIED | Conditional framing present, generalization caveat present |
| `ooh_code/manuscript/sections/method.tex` | Evidence hierarchy subsection with "Evidence Scope and Limitations" | VERIFIED | Subsection at lines 140-166 with table, caveat, expanded "Does not support" column |
| `ooh_code/manuscript/sections/method.tex` | Restructured pricing subsection containing "Pricing transforms evaluated" | VERIFIED | Paragraph at line 60, three equal transforms, Lambert-W last |
| `ooh_code/manuscript/sections/results.tex` | Tier-labeled results subsections | VERIFIED | All 5 subsections carry tier labels in \textit{[...]} format |
| `ooh_code/manuscript/sections/appendix.tex` | Renamed Lambert-W section containing "Lambert-W Reference Transform (Supplementary)" | VERIFIED | Section title at line 10, label app:lambertw preserved |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| method.tex (Evidence Scope subsection) | appendix.tex (Evidence Hierarchy section) | Table moved from appendix to method; appendix cross-references tab:evidence_hierarchy_main | WIRED | appendix.tex line 4: "The evidence hierarchy table is presented in the main text as Table~\ref{tab:evidence_hierarchy_main}" |
| method.tex (Lambert-W pricing paragraph) | appendix.tex (Lambert-W section) | Forward reference from method to appendix derivation | WIRED | method.tex line 88: "The full derivation is provided in Appendix~\ref{app:lambertw}" |
| results.tex (tier labels) | method.tex (evidence scope definitions) | Tier labels reference evidence scope definitions | WIRED | results.tex line 4 references tab:evidence_hierarchy_main; all 5 subsections carry tier labels defined in the method table |
| method.tex (Lambert-W equations) | method.tex (equation labels) | Cross-reference integrity within method | WIRED | eq:lambertw (1 hit), eq:price (2 hits) preserved in method.tex |

### Data-Flow Trace (Level 4)

Not applicable -- this is a LaTeX manuscript revision, not a software system with dynamic data flows. All "data" is static text content verified through grep above.

### Behavioral Spot-Checks

Step 7b: SKIPPED (no runnable entry points -- this is a LaTeX manuscript revision project).

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| CLAIM-01 | 01-01 | Paper claims are reframed as diagnostic/exploratory unless evidence supports stronger language | SATISFIED | Abstract, introduction, conclusion all use diagnostic/conditional framing; universal-dominance language removed; evidence-tier qualifiers added |
| THEORY-01 | 01-02 | Lambert-W pricing is rewritten as a bounded reference transform, not a core optimality contribution | SATISFIED | Method presents Lambert-W as third of three equal transforms; flat-markdown advantage noted; appendix renamed to "Supplementary"; structural demotion replaces explicit disclaimer |

No orphaned requirements: REQUIREMENTS.md maps CLAIM-01 and THEORY-01 to Phase 1 only, and both are covered by plans 01-01 and 01-02 respectively.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | - | - | - | No TODO/FIXME/placeholder markers, no stub patterns, no empty implementations found in any of the 6 modified files |

### Human Verification Required

| # | Test | Expected | Why Human |
|---|------|----------|-----------|
| 1 | Read the full abstract paragraph for narrative coherence | The abstract reads as a single coherent paragraph with diagnostic framing and no unsupported claims | Automated checks verify individual phrases but cannot assess whether the overall paragraph flows naturally |
| 2 | Read the three pricing transforms in method.tex for equal-footing presentation | All three transforms should feel symmetrically presented with no implied default or featured rule | grep confirms structural order and presence of key phrases, but visual weight and reader perception require human judgment |
| 3 | Verify LaTeX compilation produces no errors | main.tex should compile without undefined references or missing labels | Compilation requires a LaTeX toolchain not available in this verification environment |
| 4 | Assess whether "In the studied settings" framing in conclusion is sufficiently prominent | The conditional framing should be the dominant message of the practical-lessons paragraph | Automated grep confirms the phrase exists but cannot judge whether it is the rhetorical focal point |

Note: Items 1-4 above are provided for completeness and human judgment. They do not indicate automated failures. All programmatic checks passed. The status remains **passed** because these are standard human-judgment items for any manuscript revision phase, not gaps.

### Gaps Summary

No gaps found. All 10 observable truths verified. All 7 artifacts exist, are substantive, and are correctly wired. Both requirement IDs (CLAIM-01, THEORY-01) are satisfied. Cross-references between method and appendix are intact. No anti-patterns detected.

---

_Verified: 2026-05-14T07:00:00Z_
_Verifier: Claude (gsd-verifier)_
