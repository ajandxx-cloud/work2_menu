# Work2 Implementation Boundaries

## Problem Scope

The current codebase implements a front-end spatiotemporal service menu layer for many-to-one DRT. The contribution being tested is the display policy over bundle candidates, not a new exact routing engine.

Each displayed alternative is a bundle of:

- one meeting point
- one displayed pickup time window

The home-pickup option remains available as a retained alternative.

## What The Predictor Does

The shared predictor is used to estimate bundle-level operational signals, including:

- marginal operating cost
- pickup ETA
- in-vehicle travel time

The time-related outputs blend learned heads with heuristic proxies. This is intentional and should be described as an approximation layer, not as exact dispatch-time supervision.

## Feasibility And Time Windows

The current implementation does **not** solve a strict VRPTW feasibility problem during menu construction.

Instead, bundle feasibility is screened through:

- candidate-neighborhood logic
- remaining-capacity screening
- predicted pickup ETA
- passenger acceptable pickup interval filtering

This means pickup windows are front-end approximate service promises rather than guaranteed back-end VRPTW commitments.

## Route-Cost Realization

Online menu construction uses predicted values, but end-of-episode operating cost is still recovered through HGS-based route re-optimization.

Interpretation:

- front-end menu logic is approximate and online
- final route-cost accounting is ex post and routing-based

## Intended Use

This repository should be used to answer work2-style questions such as:

- Does menu optimization outperform full display under a shared predictor?
- How do menu-size limits affect profit, home-pickup share, and displayed menu size?
- How sensitive are conclusions to `menu_k`?

It should not be described as:

- a strict VRPTW solver
- a complete dispatching platform
- a general-purpose work1/work2 umbrella codebase
