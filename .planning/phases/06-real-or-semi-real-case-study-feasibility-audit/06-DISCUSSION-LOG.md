# Phase 6: Real Or Semi-Real Case Study Feasibility Audit - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-15T21:12:11.9183949+08:00
**Phase:** 6-Real Or Semi-Real Case Study Feasibility Audit
**Areas discussed:** Case study route, Data source boundary, Semi-real minimum contract, Implementation and gate use, Case study decision strength, Data source priority, Minimum acceptable semi-real case, Paper narrative boundary

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

## Case Study Decision Strength

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Phase 7 positioning | Approve but wait for gate cleanup | Phase 6 approves the semi-real route in principle, but formal execution waits for upstream gates. | Yes |
| Phase 7 positioning | Approve diagnostic-only | Allow case execution only as diagnostic/appendix evidence. | |
| Phase 7 positioning | Defer case study | Skip Phase 7 and proceed to sensitivity. | |
| Phase 7 positioning | Conditional source approval | Approve only after enough reproducible source evidence is found. | |
| Diagnostic downgrade | Allow only after renewed confirmation | Gate cleanup remains default, but user could later approve diagnostic-only. | |
| Diagnostic downgrade | Do not allow downgrade | If gates remain blocked, do not execute case experiments. | Yes |
| Diagnostic downgrade | Automatically allow diagnostic-only | Let Phase 7 downgrade without renewed confirmation. | |
| Decision label | `approved_blocked_pending_gate_cleanup` | Route approved in principle; execution blocked by gate cleanup. | Yes |
| Decision label | `conditionally_approved` | Softer approval pending sources and gates. | |
| Decision label | `deferred_until_gates_pass` | Treat case study as deferred until gates pass. | |
| Pre-cleanup Phase 7 scope | Block only formal readiness/artifact gates | Once readiness/artifact gates clear, run case. | |
| Pre-cleanup Phase 7 scope | Wait for final RC rerun | Require final RC rerun before any Phase 7 work. | |
| Pre-cleanup Phase 7 scope | Allow scaffolding, block execution | Allow ingestion/validation/manifest scaffolding, but no formal case execution or case claims. | Yes |

**User's choice:** Approve the semi-real route with decision label
`approved_blocked_pending_gate_cleanup`; do not allow automatic diagnostic-only
downgrade; allow Phase 7 scaffolding before cleanup but block case execution and
case claims.
**Notes:** This creates a precise Phase 7 handoff: build reproducibility
infrastructure only until gates are cleaned.

---

## Data Source Priority

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Audit route | Public OSM/open network first | Prioritize reproducibility; keep Yanjiao as a bonus. | |
| Audit route | Yanjiao/Beijing commuting first | Prioritize research-story fit, with reproducibility risk. | |
| Audit route | Existing benchmark first | Use Amazon/HombergerGehring style external scenarios first. | |
| Audit route | Dual-track audit | Audit public OSM/open network and Yanjiao/Beijing commuting routes together. | Yes |
| If both feasible | Public OSM/open network first | Make public network the Phase 7 main route. | Yes |
| If both feasible | Yanjiao/Beijing commuting first | Make regional commuting context the main route. | |
| If both feasible | Keep both undecided | Leave final source selection to Phase 7. | |
| Region constraint | Prefer China/Jing-Jin-Ji context | Keep geography close to the research story if reproducible. | |
| Region constraint | Prefer international public sample cities | Use globally easy-to-reproduce examples. | |
| Region constraint | Let Phase 6 audit decide | Do not preset a city; rank by reproducibility and paper value. | Yes |
| Source discovery | Use web search | Search public sources online and record links. | Yes |
| Source discovery | Local materials only | Audit repository materials only. | |
| Source discovery | Local first, then web | Escalate to web only if local materials are insufficient. | |

**User's choice:** Dual-track audit, but public OSM/open network is the default
main route if both are feasible; no preset city; web search is required.
**Notes:** Reproducibility outranks regional story value.

---

## Minimum Acceptable Semi-Real Case

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Policy family | Seven-tag family required by default | Preserve the RC comparison family unless technically impossible. | |
| Policy family | Allow reduced six-tag family | Pre-approve removing one unsuitable baseline. | |
| Policy family | Define a reduced-family gate | Default seven tags; Phase 7 must justify any fair-run reduction before execution. | Yes |
| Demand pre-registration | Strong pre-registration | Lock OD/time pattern, scale, seeds, sampling rules, and uptake regime before results. | Yes |
| Demand pre-registration | Medium pre-registration | Lock broad direction but allow adjustment after smoke/pilot. | |
| Demand pre-registration | Light pre-registration | Only label demand as simulated. | |
| Distance standard | Real road distance, rebuildable | Require source/version/date/parameters/hash/rebuild instructions. | |
| Distance standard | Coordinates plus Euclidean distance | Accept real coordinates and simple distance. | |
| Distance standard | Two-level standard | Require road/rebuildable distance for case evidence; Euclidean diagnostic fallback only. | Yes |
| Meeting points | Public POI/station/network nodes first | Use explainable public pickup points. | |
| Meeting points | Grid/cluster generation first | Generate reproducible points automatically. | |
| Meeting points | Mixed rule | Public explainable points first; pre-registered synthetic grid/cluster candidates if needed. | Yes |

**User's choice:** Default seven tags with a reduced-family gate; strong demand
pre-registration; two-level distance standard; mixed meeting-point candidate
rule.
**Notes:** These decisions protect the case from tuning, selective baseline
removal, and weak distance evidence.

---

## Paper Narrative Boundary

| Question | Option | Description | Selected |
| --- | --- | --- | --- |
| Paper role | Supplemental robustness/external scenario evidence | RC formal remains the main evidence. | Yes |
| Paper role | Main experiment | Treat case and RC as co-primary empirical evidence. | |
| Paper role | Appendix diagnostic | Keep case outside main results. | |
| Paper role | Visualization/illustrative only | Use case mostly for maps and operational explanation. | |
| Conflict handling | Boundary condition | Report conflicts honestly in Discussion. | Yes |
| Conflict handling | Downgrade case weight | Move or minimize conflicting case results. | |
| Conflict handling | Pause case use | Do not include case until explained. | |
| Supported claims | Reproducibility/mechanism only | No external-validity language. | |
| Supported claims | Limited external-validity language | Allow real road-network/geography scenario language, not real passenger claims. | Yes |
| Supported claims | Main method advantage claim | Use good case results to reinforce superiority. | |
| Labels | Force labels everywhere | Label semi-real, simulated demand, and simulated choice status in tables, figures, and text. | Yes |
| Labels | Explain once in methods | Avoid repeated labels after method explanation. | |
| Labels | Force labels by artifact type | Strong labels in tables/figures, natural prose elsewhere. | |

**User's choice:** Case is supplemental robustness/external scenario evidence;
conflicts become boundary conditions; limited external-validity language is
allowed; labels are mandatory everywhere.
**Notes:** This preserves TR-E value while blocking claims about real passenger
behavior, real acceptance, and real operating profit.

---

## The Agent's Discretion

- The planner may choose the exact section structure of
  `.planning/data/CASE_STUDY_FEASIBILITY.md`.
- The planner may choose the exact external-data search strategy, provided the
  report distinguishes real geography/network data from simulated demand.
- The planner may decide whether to run the existing Phase 6 audit script as
  supporting evidence.
- The planner may choose exact public-source search terms and candidate ranking
  table structure, provided reproducibility and evidence limits are explicit.

## Deferred Ideas

None.
