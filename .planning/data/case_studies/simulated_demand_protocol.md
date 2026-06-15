# Simulated Demand And Choice Protocol Placeholder

status: scaffolding_only_blocked_execution
case_execution_allowed: false
result_artifacts_allowed: false
manuscript_claim_upgrade_allowed: false

This protocol is a placeholder for future semi-real geography/network case
execution with simulated demand and simulated choice. Phase 7 produces no
generated demand rows, no replay-ready inputs, and no simulated choice outputs.

## Required Future Fields

| Field | Placeholder | Phase 7 status |
| --- | --- | --- |
| seeds | Future fixed list for demand generation and policy replay. | placeholder only |
| OD/time pattern | Future many-to-one origin, destination, and request-time sampling contract. | placeholder only |
| volume/range | Future request-count and scenario-intensity ranges. | placeholder only |
| sampling rules | Future rules for origins, departure times, candidate points, and exclusions. | placeholder only |
| demand labels | Must include `simulated demand` and `semi-real geography/network`. | placeholder only |
| choice labels | Must include `simulated choice`; no real passenger behavior is implied. | placeholder only |

## no-outcome-tuning

Future case-study outcomes must not tune RC calibration settings, final formal
settings, or manuscript claim strength. Route choice, demand generation, and
policy-family reduction must be predeclared before any case replay output is
available.

## Future Unlock Conditions

Case demand generation remains blocked until all of these conditions pass:

- upstream provenance gate cleanup;
- formal readiness gate cleanup;
- artifact gate cleanup for non-placeholder case evidence;
- claim guard cleanup for any manuscript claim upgrade;
- a later phase creates an executable runtime manifest and data-generation
  script with explicit approval.

## Boundary

The future case may describe real geography or a real road network only if the
source and matrix are pinned. It must not claim real passenger behavior, real
acceptance, real opt-out, real meeting-point uptake, or real operating profit.
