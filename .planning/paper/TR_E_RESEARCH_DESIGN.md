# TR-E Research Design

## Framing

This paper studies dynamic service-menu optimization for many-to-one
demand-responsive transit and last-mile mobility. For each sequential
passenger request, the platform displays a limited menu of feasible service
bundles. Each bundle combines a meeting point, pickup time window, and price.

The target journal framing is transportation logistics, service operations,
online decision-making, passenger choice, and optimization. The paper is not
an attention model paper, pricing-only paper, or pure algorithm ranking paper.

## Core Research Question

How can a many-to-one DRT operator formulate, evaluate, and audit dynamic
displayed service menus that jointly choose meeting point, pickup time window,
and price under paired replay, explicit opt-out accounting, and claim-gated
artifact control?

## Service Product

Let a displayed service bundle be:

```text
b = (m, w, p)
```

where:

- `m` is the offered pickup location, including meeting-point or home-service
  alternatives where feasible.
- `w` is the pickup time-window handling for that alternative.
- `p` is the offered price.

The outside option is refusal or lost demand. It is not accepted home pickup.
Accepted home pickup and accepted meeting-point pickup are both accepted
service outcomes.

## Sequential Decision Setting

Requests arrive sequentially. At each request, the platform observes the
current fleet and route state, feasible candidate meeting points, time-window
feasibility, pricing settings, and service guardrails. It then chooses a
displayed menu of feasible bundles.

The platform objective is to evaluate profit-service-quality trade-offs under
paired replay. Claim-bearing evaluation must preserve identical demand splits,
seeds, replay settings, checkpoint provenance, and policy-family contracts.

## Model Skeleton

Sets and indices:

- `i`: passenger request
- `m in M_i`: feasible pickup alternatives for request `i`
- `w in W_i(m)`: feasible pickup time-window alternatives for pickup option
  `m`
- `p in P_i(m,w)`: feasible price alternatives for bundle `(m,w)`
- `b in B_i`: candidate service bundle for request `i`
- `S_t`: system state before request `i`

Decision:

- `x_{ib} in {0,1}` indicates whether bundle `b` is displayed.
- `M_i = {b: x_{ib}=1}` is the displayed menu.
- `|M_i| <= K` limits menu size.

Choice:

- Passenger utility is represented through an MNL-style model over displayed
  bundles and the outside option.
- Choice probabilities are defined for displayed bundles and the outside
  option.
- Outside-option probability contributes to opt-out or lost demand.

Objective:

- Maximize expected operational value using revenue, service cost, opt-out
  penalties, ETA/window feasibility, and service guardrails.
- Claim-ready manuscript interpretation requires generated rows and strict
  claim guard approval.

Constraints:

- Menu-size limit.
- Pickup-location feasibility.
- Time-window and ETA feasibility.
- Capacity and route feasibility.
- Service guardrail constraints.
- Paired replay comparability constraints for policy evaluation.

## Primary Policy Family

1. `mainline_no_menu`
2. `mainline_fixed_menu`
3. `mainline_random_menu`
4. `mainline_optimized_m`
5. `mainline_optimized_mw`
6. `mainline_optimized_fixed_window`
7. `mainline_optimized_adaptive`

The primary method is `mainline_optimized_adaptive`.

## Evidence Tiers

- `formal`: claim-bearing only when readiness, rows, artifact status, and
  strict claim guard pass.
- `diagnostic`: useful for mechanism and boundary analysis, not positive
  manuscript claims.
- `blocked`: not usable as empirical evidence, but useful as status or
  provenance evidence.
- `scaffold-only`: design or case-study setup without runtime evidence.

## Current Claim Boundary

Current Phase 10 evidence has `claim_ready=false`. The only strict supported
claim is provenance/status transparency. All positive empirical claims must be
treated as blocked or diagnostic unless regenerated evidence changes the guard.
