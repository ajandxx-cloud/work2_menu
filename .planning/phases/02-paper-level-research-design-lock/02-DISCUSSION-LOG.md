# Phase 2: Paper-Level Research Design Lock - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-15T10:19:09+08:00
**Phase:** 2-Paper-Level Research Design Lock
**Areas discussed:** Central paper story and fallback claim, Mathematical model skeleton granularity, Claim-to-evidence mapping, Main tables/figures and non-claims boundary

---

## Central Paper Story And Fallback Claim

| Decision | Options Considered | Selected |
| --- | --- | --- |
| Default positioning | Stable conditional claim; strong-claim reserved framing; diagnostic research framing | Strong-claim reserved framing |
| Fallback classification | Four-level claim ladder; strong vs not-ready; three-level supported/conditional/unsupported | Four-level claim ladder |
| Strong claim meaning | Profit-service-quality joint improvement; net-profit dominance; mechanism decomposition | Profit-service-quality joint improvement |
| If strong claim fails | Conditional design study; diagnostic paper; calibration/rerun before paper claims | Calibration/rerun before paper claims |

**User's choice:** Strong-claim reserved framing, four-level ladder, profit-service-quality joint improvement, and no paper-claim progression if strong evidence fails.

**Notes:** The user first selected a stable conditional framing, then explicitly revised the default to strong-claim reserved. The user later clarified: "just do not write the paper first; directly redo experiments."

---

## Mathematical Model Skeleton Granularity

| Decision | Options Considered | Selected |
| --- | --- | --- |
| Model granularity | Complete paper-level skeleton; medium formalization; conceptual model first | Complete paper-level skeleton |
| Home/outside modeling | Home is a bundle and outside is not; both special bundles; only meeting-point bundles in math | Home is a bundle and outside is not |
| Time-window and ETA layer | Core bundle dimension with feasibility/risk constraints; post-processing check; experiment-only treatment | Core bundle dimension with feasibility/risk constraints |
| Exact/greedy positioning | Exact benchmark and greedy online method; greedy main with exact appendix; unspecified solver family | Exact benchmark and greedy online method |

**User's choice:** Complete formal model skeleton with home as a service bundle, outside as refusal state, time windows as a core bundle dimension, and exact/greedy solver roles locked.

**Notes:** This directly supports ROADMAP success criterion requiring a mathematical model skeleton.

---

## Claim-To-Evidence Mapping

| Decision | Options Considered | Selected |
| --- | --- | --- |
| Main comparison family | Full seven-tag mainline family; strongest baselines only; two-layer main/appendix comparison | Full seven-tag mainline family |
| Metric gate | Profit primary plus service guardrails; balanced scorecard; claim-specific metrics | Profit primary plus service guardrails |
| Paired replay requirement | All main claims paired; only main table paired; manifest fairness declaration only | All main claims paired |
| Unsupported claims | Excluded from positive manuscript claims; weak discussion allowed; leave to Phase 4 | Excluded from positive manuscript claims |

**User's choice:** Full seven-tag comparison, profit-primary claim gate with service constraints, strict paired replay for all main claims, and no unsupported positive claims.

**Notes:** Unsupported evidence can still appear in diagnosis, limitations, or experimental redesign rationale.

---

## Main Tables/Figures And Non-Claims Boundary

| Decision | Options Considered | Selected |
| --- | --- | --- |
| Table plan | Complete paper table plan; main results table only; principles only | Complete paper table plan |
| Figure plan | Mechanism plus result plus diagnostic figures; result figures only; defer figures | Mechanism plus result plus diagnostic figures |
| Attention boundary | V2/diagnostic only; appendix ablation; do not mention attention | V2/diagnostic only |
| No-filter/case boundary | No-filter diagnostic and case study optional gated; no-filter robustness baseline and case main text; both future work | No-filter diagnostic and case study optional gated |

**User's choice:** Phase 2 should define the complete table/figure plan, keep attention outside V1 main contribution, keep no-filter diagnostic, and gate any case study through Phase 6.

**Notes:** No deferred ideas were introduced.

---

## The Agent's Discretion

- Choose exact section ordering, symbol names, and table/figure labels for the research design document.
- Choose whether the claim map is a compact matrix or a longer evidence table, as long as every claim maps to comparisons, metrics, and required artifacts.

## Deferred Ideas

None.
