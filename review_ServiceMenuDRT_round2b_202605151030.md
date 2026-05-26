# Round 2b Review: Service Menu Optimization for Many-to-One DRT

Model stance: follow-up reassessment using the same Transportation Research Part E critical review standard as the prior Round 2 review.

Manuscript reviewed: latest `ooh_code/manuscript/main.tex` after v1.1 revision work.

## Score

**6.5/10**, improved from the previous **6/10** and clearly above the original **5/10**. Still short of a confident TR Part E submission, but now closer to "major revision with plausible submission path."

## Summary

The new revision closes several Round 2 blockers in a real way: operational baselines are now visible in Method/Results, the outside-option scan is concrete rather than deferred, filter diagnostics include quantiles and false-negative distance bands, and the pricing/uptake discussion is more appropriately framed as tradeoffs. This materially strengthens review readiness.

The remaining issue is that the new evidence mostly reduces risk rather than creating a strong positive empirical case. Acceptance remains extremely low in many regimes, the outside-option scan is still RC-limited and low-sample, filter errors remain very large, and Austin/Seattle remain descriptive two-pair checks.

## Strengths

The operational-baseline integration is now reviewer-facing and no longer hidden in artifacts.

The outside-option scan directly addresses a major prior criticism and improves transparency around demand-model fragility.

The filter-validity table is much stronger with P50/P90/P95 diagnostics and distance-band false-negative breakdowns.

The manuscript's interpretation is now appropriately cautious: flat markdown, Lambert-W, uptake, acceptance, and surplus are treated as regime-specific tradeoffs.

The response matrix is useful and shows disciplined traceability from reviewer blockers to manuscript changes.

## Weaknesses

External demand validation is still unresolved. Literature-bounded framing and a five-level outside-option scan are helpful, but they do not replace estimated demand parameters.

The outside-option scan itself remains behaviorally weak: many acceptance and non-home acceptance values are still near zero, so stability claims should be framed carefully.

Filter validity remains a vulnerability. The new diagnostics reveal very large ETA/IVT errors; they do not fully reassure that filtering decisions are operationally reliable.

Operational baselines are now integrated, but only in the RC low-uptake setting, where behavioral signal is limited.

City evidence remains low-sample and descriptive only, so external generalization is still not strong.

## Actionable fixes

Soften the outside-option scan claim: emphasize "not obviously brittle within this RC stress test," not "stable across demand assumptions."

Add one sentence explaining why very large ETA/IVT errors do not invalidate the main filtering diagnostic, or state that they remain a key limitation.

Move any remaining encoding/polish check to compiled PDF verification, especially around dash characters in source text.

If time permits, rerun operational baselines in the medium/high uptake setting; that would make them much more persuasive.

## Verdict

Not a clean accept-level paper yet, but now plausibly submission-preparable after a final tightening pass. I would rate it as borderline major-revision-ready for TR Part E: stronger than before, honest, and substantially improved, but still exposed on external demand calibration, filter reliability, and limited city validation.
