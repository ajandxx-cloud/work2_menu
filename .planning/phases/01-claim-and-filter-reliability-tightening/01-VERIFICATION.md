---
phase: 01-claim-and-filter-reliability-tightening
verified: 2026-05-15T03:00:00Z
status: passed
score: 4/4 must-haves verified
overrides_applied: 0
re_verification: false
---

# Phase 01: Claim and Filter-Reliability Tightening Verification Report

**Phase Goal:** Soften outside-option claims and directly address large ETA/IVT errors.
**Verified:** 2026-05-15T03:00:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

Truths are derived from the union of ROADMAP.md Success Criteria (4 items) and PLAN frontmatter must_haves (7 truths across both plans, with overlap). After deduplication, the 4 ROADMAP success criteria are the authoritative contract.

| # | Truth (from ROADMAP Success Criteria) | Status | Evidence |
|---|---------------------------------------|--------|----------|
| 1 | Outside-option scan language avoids broad "stable across demand assumptions" claims. | VERIFIED | results.tex lines 54, 65 use "directionally consistent"; no "stable" at former softening targets (lines 53/64 in pre-edit file). Remaining "stable" instances at lines 91, 103 refer to external-validation context, not outside-option/MNL claims. |
| 2 | Results or limitations explains that the scan shows "not obvious brittleness within the RC stress test." | VERIFIED | limitations.tex line 10 contains exact phrase "not obviously brittle within this RC stress test across five $u_0$ levels". |
| 3 | The manuscript explicitly states how large ETA/IVT errors affect the filter diagnostic interpretation. | VERIFIED | results.tex line 26 explains FN pruning concentrates in far distance band, near-band FN rate below 0.04, and "operationally it preferentially removes distant bundles while preserving nearby options". limitations.tex line 6 names "a key limitation" with the coarse prediction signal argument. |
| 4 | The final filter claim remains useful but bounded. | VERIFIED | results.tex line 26 states "the filtering diagnostic remains informative because false-negative pruning concentrates in the far distance band". limitations.tex line 6 states "the operational reliability of filtering-based assortment decisions cannot be fully established from the current diagnostics alone". Both directions (useful + bounded) are present. |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `ooh_code/manuscript/sections/results.tex` | "directionally consistent" at MNL + outside-option claims; FN concentration explanation | VERIFIED | Lines 54, 65: "directionally consistent". Line 26: 2 new sentences with FN far-band concentration, near-band rate below 0.04, "operationally conservative" framing. |
| `ooh_code/manuscript/sections/limitations.tex` | "not obviously brittle" + "a key limitation" + "directional consistency" | VERIFIED | Line 10: "not obviously brittle within this RC stress test". Line 6: "a key limitation". Line 14: "directional consistency". Zero instances of "directional stability". |
| `ooh_code/manuscript/sections/appendix.tex` | "directional consistency" replacing "directional stability" | VERIFIED | Line 125: "directional consistency rather than as precise interval estimates". |
| `ooh_code/manuscript/sections/conclusion.tex` | No stable/stability references to outside-option/MNL findings | VERIFIED | grep for "stable" and "stability" returns zero hits in conclusion.tex. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| results.tex quantile error paragraph (line 26) | filter_validity_summary.tex FN near/mid/far columns | textual reference to concentration pattern | WIRED | Line 26 references "Table~\ref{tab:filter_validity_summary}" and cites near-band FN rate "below 0.04" matching artifact data (0.011-0.035). |
| limitations.tex filter validity paragraph (line 6) | large ETA/IVT error acknowledgment | explicit limitation statement | WIRED | Line 6: "The large prediction errors documented above represent a key limitation" connects to results.tex quantile error paragraph. |
| results.tex line 54 | MNL sensitivity claim | text replacement | WIRED | "directionally consistent across the tested MNL parameterizations" replaces former "stable". |
| results.tex line 65 | outside-option scan claim | text replacement | WIRED | "directionally consistent across the tested $u_0$ range" replaces former "stable". |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| results.tex line 26 | FN near-band rate "below 0.04" | filter_validity_summary.tex lines 13-16 | FLOWING | Artifact shows FN Near: 0.011, 0.035, 0.035, 0.035 across four filter variants -- all below 0.04. |
| results.tex line 26 | "far distance band" FN ~8.4-8.7 | filter_validity_summary.tex lines 13-16 | FLOWING | Artifact shows FN Far: 8.698, 8.421, 8.449, 8.421 -- matches "approximately 8.4--8.7". |
| limitations.tex line 6 | "ETA P95 errors of approximately 3,600 seconds" | filter_validity_summary.tex lines 13-16 | FLOWING | Artifact shows ETA P95: 3631, 0, 727, 3612 -- deployed blended is ~3631, consistent with "approximately 3,600". |

### Behavioral Spot-Checks

Step 7b: SKIPPED -- this phase modifies LaTeX manuscript text only. There are no runnable entry points to test. Verification is through textual grep and data cross-reference.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| CLAIM-02 | 01-01 | Outside-option scan language is softened to "not obviously brittle within this RC stress test" rather than "stable across demand assumptions." | SATISFIED | All "stable" instances describing outside-option/MNL sensitivity replaced with "directionally consistent" (results.tex lines 54, 65) or "not obviously brittle" (limitations.tex line 10). Conclusion.tex clean. Appendix.tex updated. |
| FILT-04 | 01-02 | Manuscript explains why large ETA/IVT errors do not fully invalidate the filtering diagnostic, or explicitly names them as a key limitation. | SATISFIED | results.tex line 26 explains FN concentration mechanism. limitations.tex line 6 names "a key limitation" explicitly. Dual framing achieved. |

No orphaned requirements found. REQUIREMENTS.md maps CLAIM-02 and FILT-04 both to Phase 1, and both are covered by plans 01-01 and 01-02 respectively.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | - | - | - | - |

No TODO/FIXME/PLACEHOLDER/empty-implementation patterns found in modified files.

### Human Verification Required

1. **LaTeX rendering check**
   **Test:** Compile the manuscript PDF and visually inspect the new sentences at results.tex line 26 and limitations.tex lines 6, 10, 14 for correct rendering, no orphaned references, and natural flow.
   **Expected:** No LaTeX warnings for the new text. Table~\ref{tab:filter_validity_summary} resolves. Sentences read naturally in context.
   **Why human:** Automated grep verifies text presence and data accuracy but cannot assess readability, flow, or LaTeX compilation success.

2. **Overall narrative coherence**
   **Test:** Read the full results section and limitations section to confirm the softened claims and new filter-error framing read as a coherent narrative without internal contradictions.
   **Expected:** "Directionally consistent" in results aligns with "not obviously brittle" in limitations. FN concentration argument in results is consistent with "key limitation" in limitations.
   **Why human:** Narrative coherence and tonal consistency across sections require human judgment.

### Gaps Summary

No gaps found. All 4 ROADMAP success criteria are satisfied. Both requirements (CLAIM-02, FILT-04) are fully met. The dual framing achieves the intended goal: claims are softened without eliminating the diagnostic value, and filter errors are explicitly bounded.

Commits verified: `155b73c` (plan 01-01, claim softening) and `a40399f` (plan 01-02, filter-error framing) both exist in git history.

---

_Verified: 2026-05-15T03:00:00Z_
_Verifier: Claude (gsd-verifier)_
