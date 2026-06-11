# Method Outline

## Service Bundles

Each displayed alternative is a service bundle combining a pickup location, pickup time-window handling, and price. Home pickup and meeting-point pickup remain distinct accepted outcomes, while the outside option is represented as opt-out rather than accepted service.

## Menu Decision

For each request, the platform chooses a limited displayed menu from feasible candidate bundles. The menu objective combines expected profit, opt-out penalty, ETA risk penalty, and service guardrails.

## Robust Time Windows

The method supports hard, calibrated, interval-overlap, chance-constraint, soft-penalty, and no-ETA-pruning diagnostic modes. The no-filter mode disables ETA pruning only and does not disable routing or capacity feasibility.

## Choice And Pricing

Passenger selection is modeled with an MNL choice layer over displayed bundles plus an outside option. Pricing and system-aware cost definitions are held fixed across paired policy comparisons.

## Solver

Small candidate sets use exact enumeration for auditability. Larger candidate sets use greedy forward selection with diagnostics for candidate count, enumerated menu count, build time, relative gap when available, and overlap with exact selections.
