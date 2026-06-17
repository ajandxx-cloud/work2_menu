# Claim-Gated Dynamic Service-Menu Optimization for Many-to-One Demand-Responsive Transit

## Abstract

This paper studies dynamic service-menu optimization for many-to-one demand-responsive transit (DRT), where a platform responds to each passenger request by displaying a limited menu of feasible service bundles. Each bundle combines a pickup location, a pickup time window, and a price, so the operator's decision is not only whether to serve a request but which alternatives to make visible under route, capacity, passenger-choice, and provenance constraints. The manuscript is written on a conditional diagnostic path: it formulates the service-menu problem, documents an auditable paired-replay evaluation design, and reports the current claim-gated evidence boundary. The current generated package has `claim_ready=false`, with positive empirical claims blocked by readiness and strict claim-guard gates. Consequently, the paper does not claim performance effects from the adaptive menu, adaptive time windows, product ablations, exact/greedy computation, or scaffold-only case material. Its contribution is instead a claim-safe formulation and evidence architecture for evaluating such claims once clean provenance, loaded checkpoint status, complete generated rows, artifact gates, and strict claim-guard authorization are available.

## Keywords

demand-responsive transit; service-menu optimization; meeting points; pickup time windows; multinomial logit; paired replay; claim-gated evidence; transportation operations

## Introduction

Many-to-one demand-responsive transit systems face a recurring operational question: how should a platform present service choices when each request can be served through several combinations of pickup location, time-window handling, and price? Meeting points can reduce route burden and support consolidation, but they also impose walking and timing costs on passengers. Pickup windows shape perceived reliability, while prices affect willingness to accept the displayed service. Treating these elements separately can hide the actual decision problem faced by the platform. The passenger sees a menu, and each displayed item is a bundle whose feasibility and attractiveness depend on the current fleet state.

This paper frames the platform decision as dynamic service-menu optimization. For each arriving request, the operator constructs feasible bundles and displays a limited menu. Passenger choice is represented through a multinomial-logit (MNL) model over the displayed bundles and the outside option. The outside option is refusal or lost demand; it is not accepted home pickup. Accepted home pickup and accepted meeting-point pickup are accepted service outcomes, while opt-out remains a distinct non-service outcome. This separation is important because operational cost, service rate, route mutation, and claim-gated artifacts all depend on whether a request is served or declined.

The manuscript has three claim-safe contributions. First, it formulates a service-menu optimization model for many-to-one DRT in which a bundle is `b=(m,w,p)`, with meeting point or home pickup location `m`, pickup time-window handling `w`, and price `p`. Second, it describes a diagnostic evaluation design based on paired replay, explicit checkpoint provenance, source-family status, and generated artifact gates. Third, it shows how a strict claim guard controls manuscript interpretation, so current diagnostic, blocked, or scaffold-only evidence is not converted into positive empirical claims. The claim-gated pipeline is therefore an evidence constraint and transparency mechanism, not a substitute for the transportation optimization problem itself.

The current evidence state is conditional diagnostic. Phase 4 locked the paper to this path because the one authorized pre-replay gate for `final_robust_menu` remained blocked by dirty git provenance and missing formal checkpoint evidence. Final replay was not run. The current Phase 10 package reports 74 artifacts, 70 existing artifacts, 4 missing artifacts, and 108 blockers, with `claim_ready=false` and `manuscript_positive_claims_allowed=false`. The draft therefore identifies what can be formulated, diagnosed, and audited, while preserving the boundary that positive empirical claims require future regenerated evidence and strict guard authorization.

## Literature Review

DRT research has long studied the operational structure of dial-a-ride, pickup-and-delivery, and flexible-route service systems. Classical models emphasize routing, capacity, time-window feasibility, and service reliability, while more recent meeting-point work examines how walking to shared pickup locations can change route structure and passenger burden. In the setting studied here, meeting points are not just routing nodes. They are components of displayed service products, so their role must be analyzed together with pickup timing, pricing, and passenger choice.

A second relevant stream is assortment and service-menu optimization under discrete choice. In retail assortment models, a firm chooses which products to offer, anticipating substitution and outside-option behavior. A DRT menu has similar choice structure but a different operational coupling: each product is an endogenous service bundle whose cost depends on current routes, capacity, travel time, time-window feasibility, and meeting-point availability. The displayed set changes both expected passenger acceptance and expected downstream operating cost.

A third stream integrates prediction, pricing, and operations. Decision-focused methods and pricing models can be useful when downstream decisions depend on predicted costs or utilities. In this manuscript, Lambert-W pricing is treated as one bundle price generation component inside the service-menu method. It is not the sole contribution. Likewise, exact enumeration and greedy fallback are described as menu-construction contracts and diagnostic computation paths, not as claim-ready computational-credibility evidence under the current strict guard.

Finally, computational transportation studies increasingly require reproducibility and explicit evidence boundaries. The current project makes that boundary first class. Paired replay, normalized rows, checkpoint load status, artifact status, source-family status, and strict claim guards define what the manuscript can and cannot say. This design is especially important because blocked or diagnostic artifacts can still be useful for model diagnosis, reviewer-risk analysis, and future work, even when they cannot support positive claims.

## Problem Description

Requests arrive sequentially to a many-to-one DRT platform. At decision epoch `i`, the platform observes the current route and fleet state, the passenger's home location, feasible meeting-point candidates, pickup-window feasibility, pricing settings, and service guardrails. It then constructs a candidate set of service bundles. A bundle has the form `b=(m,w,p)`, where `m` is a pickup location, `w` is the pickup time-window treatment, and `p` is the displayed price. The location may be the passenger's home or a feasible meeting point.

The platform displays a menu `M_i` containing a limited number of feasible bundles. The passenger then chooses one displayed bundle or the outside option. If a home-service bundle is accepted, the request is counted as accepted home pickup and the route mutates accordingly. If a meeting-point bundle is accepted, the request is counted as accepted meeting-point pickup and the route mutates through the chosen pickup point. If the outside option is chosen, the passenger opts out or is lost demand, and the route should not mutate. The model and the generated row schema therefore keep opt-out accounting separate from accepted home service and accepted meeting-point service.

This setting creates a joint transportation and service-design problem. A menu that is operationally attractive may be unattractive to passengers if walking, timing, or price burdens are high. A passenger-attractive menu may create route or capacity costs that exceed the value of service. The goal of the formulation is to evaluate this trade-off while preserving the evidence boundary needed for claim-bearing comparisons.

## Mathematical Model

Let `I` denote the sequence of passenger requests and let `S_i` denote the system state immediately before request `i`. For request `i`, let `M_i^loc` be the feasible pickup-location set, including home service and feasible meeting points. Let `W_i(m)` be the feasible pickup-window alternatives for location `m`, and let `P_i(m,w)` be feasible price alternatives for the pair `(m,w)`. The candidate bundle set is

```text
B_i = { b=(m,w,p): m in M_i^loc, w in W_i(m), p in P_i(m,w), b satisfies feasibility gates }.
```

The menu decision can be written with a binary variable `x_ib`, where `x_ib=1` if bundle `b` is displayed to request `i`. The displayed menu is `M_i={b in B_i: x_ib=1}`, with a menu-size limit `sum_b x_ib <= K`. Feasibility constraints require candidate pickup locations to satisfy location availability, capacity, route insertion, ETA/window feasibility, and service guardrails. Diagnostic no-filter variants can relax ETA pruning, but they do not remove route, capacity, or service feasibility, and they remain diagnostic unless a future strict guard changes their status.

For a displayed bundle `b`, passenger utility is represented as

```text
U_ib = alpha + beta_p p_ib + beta_walk d_ib + beta_time tau_ib + beta_w q_ib + gamma_home h_ib,
```

where `d_ib` is walking distance, `tau_ib` is predicted in-vehicle or pickup-timing burden, `q_ib` summarizes time-window compatibility, and `h_ib` marks home service. The outside option has utility `U_i0`, implemented in the runtime as `outside_option_util`. The MNL probability of choosing a displayed bundle is

```text
P_ib(M_i) = exp(U_ib) / (exp(U_i0) + sum_{j in M_i} exp(U_ij)).
```

The outside-option probability is

```text
P_i0(M_i) = exp(U_i0) / (exp(U_i0) + sum_{j in M_i} exp(U_ij)).
```

The expected menu objective combines passenger choice, displayed price, predicted operating cost, and service guardrail terms:

```text
max_x sum_{b in B_i} x_ib P_ib(M_i) [p_ib - c_ib(S_i)] - lambda_out P_i0(M_i) - guardrail_penalties(M_i,S_i).
```

This expression is a compact manuscript representation of the runtime contract. The implementation records menu objective mode, outside-option probability, checkpoint metadata, policy tags, and service outcome counts in generated rows. Formal interpretation requires generated evidence to pass readiness, artifact, and strict claim-guard gates.

## Solution Method

The solution method builds a candidate menu in stages. First, the runtime generates feasible home and meeting-point candidate bundles from the current request and system state. Each candidate carries route-related cost information, walking and time-window metadata, and capacity or feasibility flags. Candidate generation is constrained by service guardrails so that infeasible alternatives do not become displayed products.

Second, the method applies time-window and ETA handling. The deployed robust path can use hard, calibrated, chance, or soft-penalty style filtering. The no-filter path is useful for diagnosis because it exposes the boundary created by ETA filtering, but it is not an operating recommendation in the current manuscript. Adaptive-window and fixed-window settings are comparison slots, not authorized effect claims under the current guard.

Third, prices are generated for candidate bundles. Lambert-W pricing appears here as a component that maps candidate utilities, costs, and price sensitivity into displayed prices. The manuscript treats this as part of a wider service-menu method that also includes candidate generation, feasibility filtering, menu selection, outside-option handling, and paired replay.

Fourth, the displayed menu is selected. For smaller candidate sets, exact enumeration can evaluate feasible menu subsets. For larger candidate sets, greedy fallback is used as a computational contract. Current Phase 9 tractability material is diagnostic and C6 remains blocked, so this method description does not claim computational credibility or solver quality. It states what the runtime is designed to do and what evidence would be needed before stronger computational language could be used.

## Experimental Design

The evaluation design is paired replay. Policy comparisons must share demand splits, seeds, replay settings, checkpoint provenance, candidate and utility settings, and policy-family contracts. This prevents the manuscript from attributing differences to a policy when the underlying request stream or replay conditions changed.

The primary policy family contains seven mainline tags: `mainline_no_menu`, `mainline_fixed_menu`, `mainline_random_menu`, `mainline_optimized_m`, `mainline_optimized_mw`, `mainline_optimized_fixed_window`, and `mainline_optimized_adaptive`. These tags define the intended comparison surface for service-menu construction, product mode, time-window mode, and pricing behavior. Under the current evidence boundary, the tags may be listed as design and diagnostic comparison slots, but directional claims remain blocked unless the strict guard later authorizes them.

The generated row contract records outcome and provenance fields such as `net_profit`, `acceptance_rate`, `optout_rate`, `count_accepted_home`, `count_accepted_meeting_point`, `outside_option_util`, `checkpoint_load_status`, `checkpoint_path`, `checkpoint_hash`, `checkpoint_required`, policy tag, settings hash, and manifest hash. The checkpoint provenance fields are central. Formal or pilot rows cannot support claims unless checkpoint load status and related metadata satisfy the corresponding gates.

The evidence tiers are formal, diagnostic, blocked, and scaffold-only. Formal evidence can support claim-bearing manuscript language only when readiness, row validity, artifact status, and strict claim guard all pass. Diagnostic evidence can support boundary and mechanism discussion. Blocked evidence can support status transparency but not empirical conclusions. Scaffold-only material can document future-study design but not real-world behavior. Artifact status, package status, source-family status, and the strict claim guard control result interpretation.

## Results

The current Results section begins with the claim gate because `claim_ready=false`. The Phase 10 package reports 74 artifacts, 70 existing artifacts, 4 missing artifacts, and 108 blockers. It also reports `strict_claim_guard_claim_ready=false` and `manuscript_positive_claims_allowed=false`. These facts set the manuscript ceiling.

| Claim ID | Current status | Manuscript use in this draft |
| --- | --- | --- |
| C1_central_adaptive_menu_superiority | unsupported_blocked | Not allowed as a positive claim; status and blockers only |
| C2_product_ablation_value | conditional_diagnostic_blocked | Diagnostic structure only |
| C3_adaptive_window_increment | unsupported | Not allowed as directional language |
| C4_menu_construction_value | conditional_diagnostic_blocked | Auditable mechanism only |
| C5_eta_robustness_boundary | diagnostic_only | Diagnostic boundary only |
| C6_exact_greedy_computational_credibility | blocked_diagnostic | Computational diagnostic appendix only |
| C7_provenance_status_transparency | status_supported | Status/provenance transparency only |
| C8_semi_real_case_validation | scaffold_only_blocked | Future-study scaffold only |

The source-family status is also non-claim-ready. Main RC artifacts are blocked, Phase 8 sensitivity artifacts are diagnostic and provisional, Phase 9 tractability artifacts are diagnostic and provisional, case material is scaffold-only, and blocker-status documents are status material. This does not make the artifacts useless. It means that their current manuscript use is limited to diagnosis, provenance, and boundary setting.

For C5_eta_robustness_boundary, Phase 8 and no-filter material can be discussed only as diagnostic boundary evidence. A no-filter variant can help identify what the ETA filter changes, but the current guard does not authorize language that recommends no-filter operation. For C6_exact_greedy_computational_credibility, exact/greedy material belongs in the appendix as diagnostic computation status. For C8_semi_real_case_validation, case-study files remain scaffold-only and future-study oriented. For C7_provenance_status_transparency, the manuscript may state that the generated package discloses blockers, diagnostic scope, scaffold scope, and claim gates.

## Discussion

The main transportation-operations contribution is the service-menu formulation. It makes the displayed menu the decision object and ties meeting points, pickup windows, prices, passenger choice, and route feasibility into one auditable framework. This is useful even under a diagnostic evidence ceiling because it clarifies which operational mechanisms must be evaluated together.

The main empirical limitation is also explicit. Final replay was not run because Phase 4 did not authorize it after the pre-replay gates remained blocked. Current blockers include dirty provenance and missing formal checkpoint evidence, and the strict guard blocks positive empirical claims. The manuscript therefore reports claim status rather than trying to soften or hide the blocked state. Stronger language would require a clean, regenerated evidence package with loaded checkpoint metadata, complete final rows, passing artifact gates, and strict guard authorization for the exact claim ID.

Several reviewer risks follow directly from this boundary. A reviewer may ask why the paper does not claim the adaptive menu has a positive effect; the answer is that C1 remains blocked. A reviewer may ask whether no-filter should be deployed; the answer is no, because C5 is diagnostic boundary material. A reviewer may ask whether case material reflects real passenger behavior; the answer is no, because C8 is scaffold-only. A reviewer may ask whether greedy fallback has established computational credibility; the answer is no, because C6 remains blocked diagnostic. The value of the current manuscript is that these limits are visible and traceable, not hidden behind selective wording.

This positioning still leaves a constructive path. Future work can clean provenance, provide checkpoint sidecar metadata and load status, execute formal replay without result tuning, regenerate package artifacts, and rerun the strict claim guard. If the guard changes, the manuscript can be upgraded claim by claim. Until then, the conditional diagnostic interpretation is the defensible path.

## Conclusion

This paper formulates dynamic service-menu optimization for many-to-one DRT with service bundles that combine meeting point, pickup time window, and price. It describes a menu-construction method with candidate generation, time-window handling, Lambert-W price generation, exact enumeration, greedy fallback, and explicit outside-option accounting. It also defines a paired-replay and artifact-gated evidence architecture that keeps opt-out separate from accepted service and keeps manuscript language aligned with generated claim status.

The current manuscript conclusion is conditional diagnostic. The project provides a service-menu formulation, diagnostic evaluation structure, and transparent claim-boundary audit. Positive empirical claims remain blocked by readiness and strict claim-guard gates, and final replay was not authorized in the current milestone. The paper is therefore draftable as a claim-gated diagnostic manuscript, while claim-ready empirical submission requires regenerated evidence that changes the strict guard.

## Appendix

### Appendix A. Source Map And Claim Audit

The manuscript uses `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` as the source map for all planned tables and figures. It uses `manuscript/TR_E_WORK2_CLAIM_AUDIT.md` as the C1 through C8 claim ceiling. Every result-facing object must retain source artifact path, claim ID, claim status, allowed manuscript use, and evidence class.

### Appendix B. Diagnostic Sensitivity Boundary

Phase 8 sensitivity material is available as diagnostic evidence only. It may be used to describe ETA and no-filter boundary conditions, but it cannot be used as an operational recommendation or as evidence for product-ablation value unless a future strict guard changes C2 or C5 status.

### Appendix C. Computational Diagnostics

Phase 9 exact/greedy material is available as diagnostic computation status only. It may document candidate counts, fallback reasons, build-time artifacts, and missing evidence conditions, but it cannot support C6 computational-credibility language in the current draft.

### Appendix D. Case-Scaffold Boundary

Case-study material under `.planning/data/case_studies/` is scaffold-only. It may define future source contracts, route-selection ideas, and demand protocols, but it cannot be presented as executed case evidence or passenger-behavior evidence.

### Appendix E. Prohibited-Language Check

The prohibited-language inventory and final scan procedure are maintained in `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md`. Any term hit in the manuscript body must be classified as removed, allowed as blocked-claim/status discussion, or carried into Phase 6 review.
