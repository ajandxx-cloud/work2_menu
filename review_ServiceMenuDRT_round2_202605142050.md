# Round 2 Review: Service Menu Optimization for Many-to-One DRT

Model stance: Round 2 reassessment using the same high-depth Transportation Research Part E review standard as `review_ServiceMenuDRT_202605141407.md`.

Manuscript reviewed: `ooh_code/manuscript/main.tex`, including included section files, appendix, bibliography, and artifact tables.

## Score

**6/10**, up from the previous **5/10**, but still not cleanly submission-ready for Transportation Research Part E.

## Summary

The revision meaningfully improves the paper's honesty and positioning. The manuscript now reads much less like a universal "heuristic dominates" paper and more like a diagnostic framework with exploratory simulation evidence. The evidence-tier structure, Lambert-W demotion, conservative city framing, MNL stress-test section, welfare discussion, and split-level wording all address the spirit of the first review.

However, the core empirical evidence remains thin. The demand model is still not externally calibrated; the MNL sensitivity is a limited regime stress test, not a true outside-option or preference-range validation; Austin/Seattle still have only two split pairs each; and filter validity remains a central threat because ETA/IVT diagnostics show large, directional errors without confusion-matrix or quantile support. Also, the claimed new operational baselines appear in artifact files but are not integrated into the manuscript's baseline/results narrative, so they do not yet function as review-facing evidence.

## Strengths

The revised contribution framing is much stronger. The paper now explicitly separates mechanism diagnostics, behavioral stress tests, and descriptive external checks, which prevents the results from being over-read.

Lambert-W is now appropriately treated as one pricing transform rather than the theoretical heart of the paper. That removes a major conceptual overclaim.

The welfare and managerial interpretation are more mature. The paper now distinguishes profit from passenger outcomes and acknowledges acceptance/composition effects.

The statistical presentation is more conservative, especially for Austin/Seattle. The two-pair city evidence is no longer presented as strong external validation.

The manuscript is much closer to a coherent journal article than the previous version.

## Weaknesses

External demand calibration remains the largest blocker. The MNL parameters are still simulator design choices, and the sensitivity table does not substitute for stated-preference, revealed-preference, literature-bounded, or systematic outside-option calibration.

Filter validity remains under-supported. The new bias diagnostics help, but the reported ETA/IVT errors are large and directional. Without P50/P90/P95 errors, filter-decision confusion matrices, and false-negative breakdowns, the central filtering claim is still vulnerable.

The operational baselines are not yet convincingly incorporated. The artifact table exists, but the manuscript's Method still describes only five empirical policies, and the Results section does not present the insertion-cost, minimum-lateness, or random-top-k comparison as part of the core evidence.

The quantitative results are still behaviorally fragile. Several tables show near-zero acceptance/non-home uptake in low and even some medium/high settings, so profit gaps often diagnose simulator mechanics more than operational value.

City evidence remains descriptive only. Austin and Seattle help show the mechanism is not purely RC-specific, but two split pairs per city are not enough for TR Part E-level external validation.

There are still visible encoding/polish problems in the LaTeX source, e.g. mojibake characters in related work/problem text. This must be fixed before submission.

## Actionable fixes

Integrate the operational baselines into the manuscript: update the baseline-policy section, add the operational-baseline table to Results or Appendix with explicit interpretation, and explain what these baselines do or do not show.

Add a stronger MNL calibration/sensitivity layer: at minimum, run an explicit outside-option utility scan and cite plausible parameter ranges from DRT/stated-preference literature.

Strengthen filter validation: report error quantiles, realized-feasibility confusion matrices for filtered bundles, and false-negative pruning by meeting-point type or distance band.

Make the high-uptake/pricing result more careful: flat markdown appears to dominate Lambert-W in some rows, but acceptance and surplus tradeoffs need clearer interpretation.

Remove all remaining mojibake and re-check captions/labels for internal project language.

## Verdict

**Major revision before TR Part E submission.**

The paper has improved from "not ready, 5/10" to "borderline but still risky, 6/10." I would not recommend direct submission yet, mainly because external demand calibration, filter validity, and manuscript-integrated operational baselines remain unresolved. With those fixed, it could plausibly move into a stronger weak-accept / submission-ready range.
