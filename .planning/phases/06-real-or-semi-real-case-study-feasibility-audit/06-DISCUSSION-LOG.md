# Phase 6: Real Or Semi-Real Case Study Feasibility Audit - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-15T20:45:31+08:00
**Phase:** 6-Real Or Semi-Real Case Study Feasibility Audit
**Areas discussed:** Case study route, Data source boundary, Semi-real minimum contract, Implementation and gate use

---

## Case Study Route

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Phase 6 default route | Semi-real case | Real/documented geography plus reproducible distance matrix and simulated sequential demand. | Yes |
| Phase 6 default route | Real case | Requires auditable real demand or operational data. | |
| Phase 6 default route | Defer case | Skip Phase 7 and move to sensitivity/computation. | |
| Yanjiao fallback | General auditable semi-real case | Do not hard-bind to Yanjiao if materials are insufficient. | Yes |
| Yanjiao fallback | Yanjiao first only | If Yanjiao is insufficient, defer rather than switch. | |
| Yanjiao fallback | Defer Phase 7 | Defer if strong real materials are unavailable. | |
| Paper positioning | External feasibility/robustness supplement | Use as a sanity check, not real passenger behavior validation. | Yes |
| Paper positioning | Main result | Make it co-primary with RC formal evidence. | |
| Paper positioning | Appendix diagnostic | Keep it appendix-only. | |
| Gate timing | Gate cleanup first | Phase 7 waits for gate cleanup or diagnostic downgrade. | Yes |
| Gate timing | Parallel data prep | Allow data preparation before paper-facing runs. | |
| Gate timing | Full diagnostic case first | Run a full diagnostic case despite blockers. | |

**User's choice:** Semi-real case, general fallback allowed, external supplement,
gate cleanup first.
**Notes:** This locks Phase 6 as a feasibility gate, not a real-data claim upgrade.

---

## Data Source Boundary

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Audit order | Yanjiao first | Yanjiao/commuting materials first, then public networks, then benchmarks. | |
| Audit order | Public networks/benchmarks first | Prioritize reproducibility and feasibility. | Yes |
| Audit order | Yanjiao only | Highest narrative focus, highest failure risk. | |
| Real/semi-real label | Geography/road/distance only | Demand and choice behavior stay simulated. | Yes |
| Real/semi-real label | Geography plus empirical demand distribution | Needs statistics or POI evidence. | |
| Real/semi-real label | Actual orders/traces only | Higher standard; otherwise defer. | |
| Existing benchmark positioning | Public benchmark/external scenario | Do not call it a real-city DRT case. | Yes |
| Existing benchmark positioning | Semi-real case | Treat real coordinates/distance matrix as semi-real. | |
| Existing benchmark positioning | Fallback only | Do not include in case study. | |
| External source audit | Required | Search and record public data/network candidates. | Yes |
| External source audit | Internal only | Only audit repository materials. | |
| External source audit | Leave search to Phase 7 | Phase 6 only does internal feasibility. | |

**User's choice:** Public networks/public benchmarks first; only geography,
network, and distances can be called real foundations; external source search
is required.
**Notes:** `Amazon_data` and `HombergerGehring_data` remain benchmark/external
scenario sources, not real DRT passenger-behavior evidence.

---

## Semi-Real Minimum Contract

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Minimum composition | Complete minimum contract | Geography, depot/destination, meeting points, distance matrix, simulated demand, labels. | Yes |
| Minimum composition | Lightweight contract | Real coordinates plus Euclidean distance and simulated demand. | |
| Minimum composition | Strict contract | Require real road-network matrix and public source or defer. | |
| Policy family | Seven first, six-tag fallback | Preserve seven tags unless predefined reduction is justified. | Yes |
| Policy family | Seven required | No full seven tags means no case study. | |
| Policy family | Smaller diagnostic set | Four-category diagnostic comparison only. | |
| Demand generation | Pre-register rules | Parameters, seeds, OD/time pattern, scale/range locked before results. | Yes |
| Demand generation | Reuse RC split/seed logic | Minimize separate demand protocol. | |
| Demand generation | Let Phase 7 decide | Only require simulated label. | |
| Distance standard | Reproducibility first | Record source/version/date/parameters/hash; Euclidean diagnostic only. | Yes |
| Distance standard | Road network required | No road-network matrix means no semi-real case. | |
| Distance standard | Euclidean acceptable | Real coordinates alone are enough. | |

**User's choice:** Complete minimum contract, seven tags first with justified
six-tag fallback, pre-registered demand generation, reproducible distance
evidence.
**Notes:** This prevents the semi-real case from becoming a tuned or fabricated
result source.

---

## Implementation And Gate Use

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| `phase6_audit.py` use | Supporting experiment-state audit | Keep it for runtime/manifests/readiness/gates only. | Yes |
| `phase6_audit.py` use | Main report generator | Extend it to cover case feasibility. | |
| `phase6_audit.py` use | Do not use it | Ignore the scaffold. | |
| Phase 6 implementation | No ingestion/run code | Write feasibility and Phase 7 contract only. | Yes |
| Phase 6 implementation | Validation scaffold only | Add small schema/test placeholders. | |
| Phase 6 implementation | Start ingestion | Begin implementation if source seems feasible. | |
| Blocked gates handling | Approve but blocked pending cleanup | Decision can be positive while execution waits. | Yes |
| Blocked gates handling | Direct defer | Blockers mean no Phase 7 approval. | |
| Blocked gates handling | Diagnostic Phase 7 | Allow full diagnostic execution despite blockers. | |
| Output organization | One primary plus one support | `CASE_STUDY_FEASIBILITY.md` plus optional audit outputs. | Yes |
| Output organization | Context only | Do not create `.planning/data/` report. | |
| Output organization | Audit outputs only | No planning data report. | |

**User's choice:** Use `phase6_audit.py` as support only; no Phase 6 ingestion
implementation; approve with `blocked_pending_gate_cleanup` if gates remain
blocked; write one primary feasibility report plus optional audit evidence.
**Notes:** The main Phase 6 deliverable remains
`.planning/data/CASE_STUDY_FEASIBILITY.md`.

---

## The Agent's Discretion

- The planner may choose the exact section structure of
  `.planning/data/CASE_STUDY_FEASIBILITY.md`.
- The planner may choose the exact external-data search strategy, provided the
  report distinguishes real geography/network data from simulated demand.
- The planner may decide whether to run the existing Phase 6 audit script as
  supporting evidence.

## Deferred Ideas

None.
