# Claim-Gated Dynamic Service-Menu Optimization for Many-to-One Demand-Responsive Transit

## Abstract

Many-to-one demand-responsive transit (DRT) platforms increasingly face a
service-design decision that is richer than route insertion alone. For each
arriving request, the operator may display several feasible service bundles,
where each bundle combines a pickup location, a pickup time-window treatment,
and a price. This paper formulates that decision as dynamic service-menu
optimization. The service bundle is written as `b=(m,w,p)`, with `m` denoting
home or meeting-point pickup, `w` denoting pickup-window handling, and `p`
denoting the displayed price. Passenger response is modeled experimentally
with a multinomial-logit (MNL) choice model over displayed bundles and the
outside option. The outside option represents refusal or lost demand, not
accepted home pickup, so accepted home service, accepted meeting-point service,
and opt-out are kept as separate accounting outcomes.

The manuscript follows a conditional diagnostic evidence path. It describes
the formulation, the menu-construction and paired-replay evaluation pipeline,
and the package-level claim gates that govern manuscript interpretation. The
current generated package has `claim_ready=false`,
`strict_claim_guard_claim_ready=false`, and
`manuscript_positive_claims_allowed=false`. Positive empirical claims about
adaptive-menu effects, product ablations, adaptive-window increments,
menu-construction value, exact/greedy computational credibility, and
semi-real case evidence remain blocked by readiness and strict claim-guard
status. The contribution is therefore a claim-gated service-menu optimization
framework and a transparent diagnostic evidence architecture for future
claim-ready evaluation.

## Keywords

demand-responsive transit; service-menu optimization; meeting points; pickup
time windows; multinomial logit; paired replay; artifact gates; transportation
operations

## Introduction

Many-to-one DRT systems must coordinate route efficiency, passenger
convenience, service reliability, and price while requests arrive sequentially.
In a last-mile or feeder setting, a platform can sometimes serve a passenger at
home, sometimes ask the passenger to walk to a meeting point, and sometimes
decline to serve the request if service is unattractive or infeasible. These
outcomes are shaped not only by routing cost, but also by what the passenger is
shown. A displayed alternative is a service product: it tells the passenger
where to be picked up, when pickup is expected, and what price applies.

This paper makes the displayed service menu the central decision object. At
request epoch `i`, the platform observes the current fleet and route state,
generates feasible service bundles, and chooses a limited menu to display.
Each displayed bundle has the form `b=(m,w,p)`, where `m` is the pickup
location, `w` is the pickup time-window treatment, and `p` is the price. The
menu also competes with an outside option. If the passenger accepts a home
bundle, the request is served as accepted home pickup. If the passenger accepts
a meeting-point bundle, the request is served through the selected pickup
point. If the outside option is selected, the passenger opts out and the route
does not mutate. This separation is essential for transportation operations:
accepted service consumes capacity and changes routes, whereas opt-out is lost
demand.

The paper is written for Transportation Research Part E as a service
operations and logistics contribution. It connects meeting-point design,
pickup-window handling, pricing, passenger choice, route feasibility, and
evidence traceability in one dynamic optimization framework. The formulation
is not a pricing-only model, a pure route-insertion heuristic, a standalone
assortment model, or an attention-model paper. The service menu couples an
assortment-style display decision with route-dependent costs and
state-dependent feasibility.

The empirical status is deliberately stated at the beginning. The current
package is conditional diagnostic, not claim-ready empirical. Phase 4 did not
authorize final replay because the pre-replay gate remained blocked by dirty
git provenance and missing formal checkpoint evidence. The Phase 10 package
reports 74 artifacts, 70 existing artifacts, 4 missing artifacts, and 108
blockers. The strict claim guard allows only provenance/status transparency as
a supported claim, while ETA/no-filter material is diagnostic-only. This paper
therefore does not convert blocked artifacts into positive results. Instead,
it uses the blocker state as a reproducibility boundary: the manuscript can
formulate, evaluate diagnostically, audit, and identify conditions for future
claim upgrades.

The manuscript makes four claim-safe contributions. First, it formulates a
dynamic displayed service-menu problem for many-to-one DRT with bundles
`b=(m,w,p)`. Second, it provides a self-contained mathematical model covering
candidate bundles, displayed menus, MNL response, feasibility constraints,
objective components, and separate outcome accounting. Third, it describes an
auditable service-menu evaluation pipeline that connects candidate generation,
ETA/window handling, pricing, menu selection, replay logging, and claim-gate
reporting. Fourth, it documents how strict claim guards prevent diagnostic,
blocked, or scaffold-only material from being used as claim-ready empirical
evidence.

## Literature Review

The first stream of related work studies DRT, dial-a-ride, and flexible
last-mile service operations. These models usually emphasize routing,
capacity, time-window feasibility, fleet repositioning, and service quality.
Meeting-point DRT extends this setting by allowing passengers to walk to shared
pickup points, which can reduce route burden and improve consolidation. In the
present paper, meeting points are not treated as route nodes alone. They are
components of displayed service bundles, and their operational value depends
on time-window treatment, price, and passenger response.

The second stream concerns pickup-window design and service reliability.
Time-window promises affect both passenger acceptance and operational
feasibility. A narrow pickup window may make the service more attractive but
harder to route; a flexible window may reduce route pressure but lower
perceived convenience. Robust ETA filtering and adaptive-window logic are
therefore natural service-menu ingredients. Under the current evidence state,
however, these ingredients are model components and diagnostic comparison
slots rather than authorized effect claims.

The third stream is assortment and menu optimization under discrete choice.
Retail assortment models choose which products to offer when customers may
substitute or choose an outside option. A DRT service menu has a related
choice structure, but each product is state-dependent and operationally
endogenous. The cost of a bundle depends on the current route, capacity,
pickup location, time window, and feasibility checks. The menu decision is
therefore both a display decision and a transportation operations decision.

The fourth stream integrates pricing with operational decision-making.
Pricing can shape willingness to accept meeting-point service or time-window
trade-offs. In this paper, Lambert-W pricing is one price-generation component
inside a wider service-menu pipeline. It does not define the full contribution
by itself. The paper also separates price generation from menu feasibility,
choice response, route mutation, and artifact-gated evidence interpretation.

Finally, computational transportation studies increasingly need transparent
provenance and reproducibility controls. The current manuscript treats paired
replay, checkpoint load status, normalized rows, artifact status, package
status, and strict claim guards as first-class evidence controls. This framing
does not replace empirical evidence. It prevents a manuscript from overstating
what the generated evidence can support and clarifies what future work must
regenerate before stronger claims are available.

## Problem Description

Requests arrive sequentially. At epoch `i`, a passenger request is observed
together with the current system state `S_i`. The state includes the active
fleet and route plan, vehicle capacity, time information, the passenger's home
location, candidate meeting points, routing and insertion costs, pickup-window
metadata, price settings, and service guardrails. The platform must decide
which service alternatives to display before the passenger response is known.

A service alternative is a bundle `b=(m,w,p)`. The pickup component `m` may be
the passenger's home or a feasible meeting point. The time-window component
`w` records how pickup timing is offered, such as fixed-window or
adaptive-window handling. The price component `p` is the displayed fare or
discounted fare associated with the bundle. A displayed menu `M_i` is a subset
of feasible bundles and is constrained by a menu-size limit.

The passenger may choose one displayed bundle or choose the outside option.
The outside option is refusal or lost demand. It is not home service and
should not change the route. This distinction yields three accounting
outcomes. Accepted home pickup means the passenger chooses a home-service
bundle and the vehicle route is updated for home pickup. Accepted
meeting-point pickup means the passenger chooses a meeting-point bundle and
the route is updated for that location. Opt-out means the passenger chooses
the outside option and no pickup route is inserted.

The operator's decision is difficult because passenger attractiveness and
operational cost move together. A far meeting point may reduce vehicle cost
but reduce passenger utility. A home pickup may be attractive but costly. A
price can compensate or discourage acceptance. A pickup window can increase
reliability for one request but reduce downstream flexibility. Dynamic
service-menu optimization evaluates these trade-offs under current route
state, feasible products, and evidence gates that determine which results may
be interpreted as claim-bearing.

## Mathematical Model

Let `I` be the sequence of requests. For request `i in I`, let `S_i` denote
the system state before the menu is displayed. Let `L_i` be the feasible
pickup-location set, including home service and any feasible meeting-point
alternatives. For each `m in L_i`, let `W_i(m)` be the feasible set of
pickup-window treatments, and let `P_i(m,w)` be the feasible set of prices for
location-window pair `(m,w)`.

The candidate bundle set is

```text
B_i = { b=(m,w,p) : m in L_i, w in W_i(m), p in P_i(m,w),
        b satisfies route, capacity, ETA/window, and service guardrail checks }.
```

The platform chooses binary display variables `x_ib`, where `x_ib=1` if
bundle `b` is displayed. The menu is

```text
M_i = { b in B_i : x_ib = 1 },
```

with menu-size constraint

```text
sum_{b in B_i} x_ib <= K.
```

The feasibility constraints include the following conditions. Pickup-location
feasibility requires the location to be home service or an available meeting
point for request `i`. ETA/window feasibility requires the predicted pickup
time to be compatible with the bundle's time-window treatment. Capacity and
route feasibility require the insertion to respect vehicle capacity and route
state. Service guardrails exclude alternatives that violate the service
contract. Policy-comparison comparability requires paired replay settings,
seeds, demand splits, checkpoint requirements, and policy-only overrides to
remain controlled across policies.

Passenger response is represented by an MNL model over displayed bundles and
the outside option. Let `U_ib` be the systematic utility of displayed bundle
`b`:

```text
U_ib = a_0 + a_p p_ib + a_d d_ib + a_t t_ib + a_w q_ib + a_h h_ib,
```

where `d_ib` is walking distance, `t_ib` is pickup-time or in-vehicle-time
burden, `q_ib` summarizes time-window compatibility, and `h_ib` indicates
home service. Let `U_i0` denote outside-option utility. The probability of
choosing displayed bundle `b` is

```text
Pr_i(b | M_i) =
  exp(U_ib) / (exp(U_i0) + sum_{j in M_i} exp(U_ij)).
```

The outside-option probability is

```text
Pr_i(0 | M_i) =
  exp(U_i0) / (exp(U_i0) + sum_{j in M_i} exp(U_ij)).
```

The expected one-request menu objective can be written as

```text
max_x  sum_{b in B_i} x_ib Pr_i(b | M_i) [p_ib - c_ib(S_i)]
       - lambda_out Pr_i(0 | M_i)
       - Phi(M_i,S_i),
```

where `c_ib(S_i)` is predicted operational cost, `lambda_out` is an
opt-out/lost-demand penalty, and `Phi(M_i,S_i)` collects service-quality,
ETA/window, and guardrail penalties. This representation is intentionally
general: concrete runtime policies can use different menu-objective modes,
pricing modes, and solver contracts while preserving the same evidence
accounting.

The realized outcome after choice is recorded separately. If the chosen bundle
is home service, the row increments accepted home pickup. If the chosen bundle
is a meeting-point service, the row increments accepted meeting-point pickup.
If the outside option is chosen, the row increments opt-out and the route is
not mutated. Generated rows also record checkpoint status, policy tag,
settings hash, manifest hash, outside-option utility, and method metadata.
These fields are required because formal interpretation depends on provenance
and artifact gates, not only on numerical objective values.

## Solution Method

The method is an online diagnostic service-menu pipeline. It uses the current
request and route state to generate feasible products, score menus, record
choice and outcome metadata, and route the resulting evidence through claim
gates. The pipeline is written as pseudocode because the manuscript's purpose
is to describe an auditable evaluation contract, not to assert claim-ready
algorithmic performance.

```text
Algorithm 1. Diagnostic service-menu evaluation pipeline

Input: current state S_i, request i, policy tag, checkpoint contract,
       paired replay settings, artifact-gate configuration
Output: selected service outcome, normalized row metadata, claim-gate status

1. Read current route, capacity, request, and replay state.
2. Generate candidate pickup locations: home plus feasible meeting points.
3. For each location, generate candidate pickup-window treatments.
4. For each location-window pair, generate or assign prices.
5. Form candidate bundles b=(m,w,p).
6. Apply route, capacity, ETA/window, and service-guardrail filters.
7. Select a displayed menu subject to menu-size and policy contracts:
      a. use exact enumeration when candidate count is inside the exact limit;
      b. use greedy fallback when candidate count exceeds that limit;
      c. record solver diagnostics, candidate counts, fallback reason,
         build time, and selected menu metadata.
8. Evaluate the MNL response model over displayed bundles plus outside option.
9. Apply the selected outcome:
      a. accepted home pickup mutates the route through home service;
      b. accepted meeting-point pickup mutates the route through the chosen
         meeting point;
      c. opt-out records lost demand and does not mutate the route.
10. Emit normalized row fields, checkpoint load status, policy tag,
    method metadata, manifest/settings hashes, and outcome counts.
11. Classify generated artifacts through readiness, row, artifact, package,
    and strict claim-guard gates.
```

Candidate bundle generation starts from feasible service products. Home
service may be retained as a displayed option or may be part of the candidate
pool, depending on the policy contract. Meeting-point candidates carry walking
distance, predicted route cost, ETA, time-window metadata, and service-quality
features. The service guardrails prevent infeasible or contract-violating
alternatives from being displayed.

ETA and pickup-window handling are modeled as feasibility and scoring
components. Robust ETA filters can exclude or penalize bundles whose predicted
pickup timing is outside the relevant service window. A no-filter diagnostic
path can expose how the ETA filter changes the candidate set, but it is not an
operating recommendation in this manuscript. Fixed-window and adaptive-window
settings are comparison slots governed by the strict claim guard.

Pricing is applied after candidate construction or during menu evaluation. The
Lambert-W pricing component maps utility and cost terms into candidate prices
when that pricing mode is active. The paper treats this component as part of a
larger service-menu method, because the displayed decision also depends on
route feasibility, menu size, choice response, outside-option treatment, and
claim-gated evidence status.

Menu selection may use exact enumeration for small candidate sets and greedy
fallback for larger sets. Current computational material is diagnostic and C6
is blocked, so the method section does not assert computational credibility.
It reports the contract: the runtime records the effective solver, threshold,
candidate count, fallback flag, fallback reason, and related diagnostics so
future evidence can be audited.

## Experimental Design

The evaluation design is paired replay. Each policy comparison must preserve
the same demand splits, seeds, replay settings, checkpoint requirements,
manifest structure, and non-policy runtime settings. Only declared policy
overrides may differ. This design prevents a comparison from mixing policy
effects with changes in scenario, checkpoint provenance, or replay
conditions.

The primary policy family contains seven mainline tags:

| Policy tag | Role in paired comparison |
| --- | --- |
| `mainline_no_menu` | Baseline slot without displayed service-menu construction |
| `mainline_fixed_menu` | Fixed service-menu slot |
| `mainline_random_menu` | Random displayed-menu diagnostic slot |
| `mainline_optimized_m` | Optimized meeting-point-only product slot |
| `mainline_optimized_mw` | Optimized meeting-point and window product slot |
| `mainline_optimized_fixed_window` | Optimized menu with fixed-window handling |
| `mainline_optimized_adaptive` | Optimized menu with adaptive-window handling |

These tags define the comparison surface. Under the current strict claim
guard, they do not authorize directional effect language. They are used to
explain how the service-menu family is organized and what future claim-ready
evidence would need to compare.

The normalized rows record profit and service metrics, including `net_profit`,
`acceptance_rate`, `optout_rate`, accepted home count, accepted meeting-point
count, home share, meeting-point uptake, served rate, and status fields.
Provenance fields include policy tag, manifest hash, settings hash,
checkpoint path, checkpoint hash, checkpoint requirement, and
`checkpoint_load_status`. The checkpoint fields are not administrative
details: formal and pilot evidence cannot support manuscript claims without
explicit load status and matching metadata.

Evidence is classified into four tiers. Formal evidence can support
claim-bearing language only when readiness, row validity, artifact status,
package status, and strict claim guard all pass. Diagnostic evidence can
support mechanism and boundary discussion. Blocked evidence can support
status/provenance transparency but not positive empirical conclusions.
Scaffold-only material can define future study protocols but cannot establish
executed case evidence. The claim gates are therefore part of the experimental
design.

## Results

The Results section begins with the strict claim gate. The current package has
`claim_ready=false`, `strict_claim_guard_claim_ready=false`, and
`manuscript_positive_claims_allowed=false`. It contains 74 package artifacts,
70 existing artifacts, 4 missing artifacts, and 108 blockers. The package is
usable for diagnostic interpretation and provenance transparency, but it is
not claim-ready empirical evidence.

| Claim ID | Current status | Allowed manuscript use |
| --- | --- | --- |
| C1_central_adaptive_menu_superiority | unsupported_blocked | Not allowed as a positive claim; status and blockers only |
| C2_product_ablation_value | conditional_diagnostic_blocked | Diagnostic structure and future upgrade conditions only |
| C3_adaptive_window_increment | unsupported | Comparison slot only; no directional effect language |
| C4_menu_construction_value | conditional_diagnostic_blocked | Auditable mechanism discussion only |
| C5_eta_robustness_boundary | diagnostic_only | ETA/no-filter boundary discussion only |
| C6_exact_greedy_computational_credibility | blocked_diagnostic | Computational diagnostic appendix only |
| C7_provenance_status_transparency | status_supported | Provenance/status transparency only |
| C8_semi_real_case_validation | scaffold_only_blocked | Future-study scaffold only |

This claim table shapes the diagnostic findings. First, the service-menu
framework can be described as implemented and auditable, but central adaptive
menu performance claims remain blocked. Second, product and time-window
ablations can be described as diagnostic comparison structure, not as
claim-ready evidence of value. Third, ETA/no-filter material can identify a
robustness boundary, but no-filter is not presented as a deployment rule.
Fourth, exact/greedy output can document computational status and fallback
metadata, while computational credibility remains blocked. Fifth, case-study
material remains scaffold-only and future-study oriented.

The source-family status reinforces this interpretation. Main RC artifacts
are blocked because formal readiness and checkpoint evidence are unavailable.
Phase 8 sensitivity artifacts are diagnostic and provisional. Phase 9
tractability artifacts are diagnostic and provisional. Case material is
scaffold-only. Blocker-status documents are provenance/status material. The
result is a transparent diagnostic package rather than a positive empirical
result package.

This interpretation is not a paper weakness to hide; it is the paper's
evidence discipline. A reader can see which model components exist, which
comparison slots are planned, which generated artifacts are blocked, which
diagnostic boundaries are visible, and what future regenerated evidence would
need to change before any claim ID is upgraded.

## Discussion

The primary contribution is the formulation of a displayed service-menu
decision for many-to-one DRT. The model ties meeting points, pickup-window
handling, prices, MNL response, route feasibility, and outside-option
accounting into one sequential decision. That contribution is useful even
under a diagnostic evidence ceiling because it clarifies what the platform
actually controls and what generated evidence must preserve.

The second contribution is the evidence architecture. Paired replay controls
scenario comparability. Checkpoint metadata records whether required
prediction models were available and loaded. Normalized rows separate accepted
home pickup, accepted meeting-point pickup, and opt-out. Artifact gates
classify evidence into formal, diagnostic, blocked, and scaffold-only tiers.
Strict claim guards then translate those tiers into allowed manuscript
language. This makes the manuscript harder to overstate and easier to audit.

The limitation is equally explicit. Final replay was not run in this
milestone because the pre-replay gate remained blocked. The current package
has `claim_ready=false`, and the guard blocks positive claims for C1, C2, C3,
C4, C6, and C8. The manuscript therefore cannot conclude that one menu family
has claim-ready performance effects over another. It can only state the
formulation, diagnostic boundaries, blocker status, and future evidence path.

The reviewer implications are direct. If a reviewer asks where the adaptive
menu performance claim is, the answer is that C1 is blocked and not asserted.
If a reviewer asks whether no-filter should be used operationally, the answer
is that C5 is diagnostic boundary material only. If a reviewer asks whether
case material reflects executed passenger evidence, the manuscript explicitly
does not claim such behavior because C8 remains scaffold-only. If a
reviewer asks whether exact/greedy material establishes solver quality, the
answer is that C6 is blocked diagnostic and future evidence is required.

Future claim upgrades require new evidence, not editorial substitution. A
future milestone would need clean provenance, loaded checkpoint status and
sidecar metadata, complete formal rows, dependency snapshots, artifact-status
passes, package regeneration, and a strict claim guard that authorizes the
exact claim ID. Only then should the manuscript wording change from
conditional diagnostic to claim-ready empirical.

## Conclusion

This paper formulates dynamic displayed service-menu optimization for
many-to-one DRT. The central decision is the displayed bundle `b=(m,w,p)`,
combining pickup location, pickup-window handling, and price. The model
defines candidate bundles, menus, MNL response, objective components,
feasibility constraints, outside option, accepted home pickup, accepted
meeting-point pickup, and opt-out accounting. The method describes an
auditable diagnostic pipeline from candidate generation through claim-gate
reporting.

The current manuscript remains conditional diagnostic with `claim_ready=false`.
It provides a service-menu formulation, paired-replay evaluation architecture,
and transparent claim-boundary audit. Positive empirical claims remain blocked
by readiness and strict claim-guard status, and final replay was not
authorized in the current milestone. The paper is therefore a claim-gated
diagnostic manuscript and a foundation for future clean evidence
regeneration.

## Appendix

### Appendix A. Source Map And Claim Audit

The manuscript uses `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` as the
source map for planned manuscript objects. Each object is required to identify
source artifact path, claim ID, claim status, allowed manuscript use, and
evidence class. The strict claim boundary is documented in
`manuscript/TR_E_WORK2_CLAIM_AUDIT.md` and the generated
`work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`.

### Appendix B. ETA And No-Filter Diagnostic Boundary

ETA/no-filter material belongs to C5_eta_robustness_boundary and is
diagnostic-only under the current guard. It may be used to identify boundary
conditions created by ETA filtering and pickup-window handling. It does not
authorize a no-filter operating recommendation or any deployment language.

### Appendix C. Exact/Greedy Computational Diagnostics

Exact enumeration and greedy fallback are runtime contracts whose diagnostics
include candidate count, effective solver, threshold, fallback flag, fallback
reason, and build time. Current Phase 9 material is diagnostic and
provisional, and C6_exact_greedy_computational_credibility remains blocked.
The appendix may report computational status only within that boundary.

### Appendix D. Case-Scaffold Boundary

Case-study material under `.planning/data/case_studies/` is scaffold-only. It
may define future source contracts, route-selection ideas, and demand
protocols. It cannot be presented as executed case evidence, real passenger
evidence, or claim-ready validation in the current manuscript.

### Appendix E. Prohibited-Language Check

The revised prohibited-language check is maintained in
`manuscript/TR_E_WORK2_REVISED_PROHIBITED_LANGUAGE_CHECK.md`. Hits from the
scan must be classified as safe blocked-claim/status discussion, safe explicit
denial, or unsafe language requiring manuscript revision. The final status is
pass only when no unqualified positive claim remains.
