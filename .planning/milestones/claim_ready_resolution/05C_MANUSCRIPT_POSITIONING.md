---
phase: 17
status: manuscript_positioning_locked
selected_path: Path C
final_claim_ready_status: false
generated_at: 2026-06-16T19:45:00+08:00
timezone: Asia/Shanghai
---

# Phase 17 Manuscript Positioning

## Safe Thesis

The safe paper thesis is:

> This paper formulates dynamic service-menu optimization for many-to-one DRT
> and uses paired replay with explicit artifact and claim gates to diagnose
> when optimized service menus improve service-quality outcomes, when they fail
> to recover realized net profit, and which stronger claims remain unsupported
> under current evidence.

This is a conditional diagnostic thesis. It is not a superiority thesis.

## Positioning Pillars

### 1. Service-Menu Formulation

The paper may center the methodological object:

- the displayed service menu;
- service bundles with meeting point, pickup-time window, price, home service,
  and outside option;
- the platform decision over limited menus for sequential requests;
- explicit opt-out accounting separate from accepted home pickup.

Allowed contribution wording:

- "We formulate and implement a service-menu optimization pipeline for
  many-to-one DRT."
- "The formulation exposes the joint wait-walk-price-service trade-off."

Prohibited escalation:

- "The optimized adaptive menu is empirically superior."

### 2. Paired-Replay Evaluation

The paper may present paired replay as the evaluation discipline:

- shared splits and settings across policies;
- seven mainline policy tags including `mainline_random_menu`;
- checkpoint and provenance metadata;
- row, artifact, and claim-guard status.

Allowed contribution wording:

- "Paired replay enables auditable policy comparisons under shared demand and
  configuration settings."
- "The current package makes claim boundaries explicit through strict status
  artifacts."

Prohibited escalation:

- "The paired replay proves adaptive-menu dominance."

### 3. Transparent Evidence-Boundary Analysis

The paper should make the boundary itself part of the contribution:

- random-menu profit advantage remains visible;
- adaptive/fixed-window equality remains a blocker;
- sensitivity and tractability outputs remain diagnostic/provisional;
- case-study material remains scaffold-only;
- C7 provenance/status transparency is supported but not effectiveness
  evidence.

Allowed contribution wording:

- "The evidence identifies a conditional profit-service trade-off and blocks
  stronger empirical claims."
- "The claim guard prevents diagnostic evidence from being promoted into
  unsupported manuscript language."

Prohibited escalation:

- "The limitations are minor and do not affect the main claim."

## Safe Abstract-Level Wording

Safe abstract wording may use this ceiling:

> We study dynamic service-menu optimization for many-to-one demand-responsive
> transit, where each arriving request can be offered a limited menu combining
> meeting points, pickup-time windows, prices, home service, and an outside
> option. We implement a paired-replay evaluation pipeline with explicit
> checkpoint, artifact, and claim-status gates. Current diagnostic evidence
> shows that optimized adaptive menus can improve acceptance and reduce
> opt-out, but the selected formal replay does not support a positive
> superiority claim: the random-menu comparator has higher mean realized net
> profit, and optimized adaptive and optimized fixed-window policies remain
> identical across tracked metrics. The paper therefore contributes a
> service-menu formulation, a transparent paired-replay evidence protocol, and
> a conditional diagnosis of when stronger TR-E claims remain blocked.

This wording must not be strengthened unless a later strict claim guard
authorizes it.

## Safe Conclusion-Level Wording

Safe conclusion wording may use this ceiling:

> The current Work2 evidence supports a conditional diagnostic manuscript, not
> a claim-ready superiority paper. The service-menu formulation and paired
> replay pipeline make the wait-walk-price-service trade-off auditable, and the
> generated claim gates identify where evidence is sufficient for transparency
> but insufficient for empirical effectiveness claims. In the selected replay,
> optimized adaptive menus improve some service outcomes but do not beat the
> random-menu baseline on mean realized net profit, and the adaptive-window
> increment remains blocked by fixed/adaptive equality. Future claim-ready work
> would require pre-registered implementation verification, schema-complete
> paired replay, preserved baselines, and regenerated strict claim guards.

This conclusion must not say that adaptive menus dominate, that adaptive
windows add value, that no-filter operation is recommended, that greedy is
near-optimal, or that case evidence validates the findings.

## How To Use Qi's Stall-Economy Paper

Qi's stall-economy paper may be cited as motivation for why passenger waiting,
walking, service reliability, and mobility friction matter in shared mobility
or transit-service design. It may help motivate the general managerial
question: DRT menus redistribute burdens and benefits across time, walking,
and service availability.

It must not be used as direct evidence for Work2 claims. In particular, it
must not be cited to support:

- adaptive-menu superiority;
- adaptive-window value;
- the random-menu comparison;
- realized net-profit effects;
- opt-out rates or acceptance rates in Work2;
- real passenger behavior in this repository;
- case-study validation;
- no-filter operational recommendations.

Safe use:

- "Prior work on waiting, walking, and mobility friction motivates examining
  service-menu trade-offs; our evidence about Work2 remains limited to the
  paired replay and claim-guarded artifacts reported here."

Unsafe use:

- "Qi's evidence validates our adaptive-menu gains."

## Manuscript Shape

Recommended paper structure under Path C:

1. Introduction: motivate service-menu design and claim-gated evidence.
2. Model: define requests, bundles, menus, outside option, and objective.
3. Evaluation protocol: paired replay, policy family, checkpoint/provenance
   gates, and strict claim guard.
4. Diagnostic results: service-quality improvements, random-menu profit
   advantage, adaptive/fixed-window equality, and objective/evaluation
   alignment limits.
5. Boundary analyses: ETA/no-filter diagnostics, sensitivity, tractability,
   and case scaffold status.
6. Limitations and future work: implementation verification, legitimate
   pre-registered rerun, greedy stress evidence, and case execution.
7. Conclusion: conditional diagnostic contribution only.

## Final Positioning Lock

The paper is draftable as a conditional diagnostic TR-E paper only. It is not
draftable as a positive central superiority paper while
`final_claim_ready_status=false`.
