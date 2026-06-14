---
phase: 2
phase_name: Service Product Contract
type: implementation
status: complete
evidence:
  - .planning/phases/02-service-product-contract/02-CONTEXT.md
  - .planning/phases/02-service-product-contract/02-VERIFICATION.md
---

# Phase 2 Plan: Service Product Contract

## Objective

Define and verify the explicit Work2 service product contract for
`product_mode`, `time_window_mode`, `menu_mode`, pricing, normalized-row-v2, and
artifact eligibility.

## Tasks

1. Expose product modes `m`, `m+w`, and `m+w+p`.
2. Expose time-window modes `no_time_window`, `fixed_window`, and
   `adaptive_window`.
3. Expose menu modes `no_menu`, `fixed_menu`, `random_menu`, and
   `optimized_menu`.
4. Upgrade normalized rows and failed-row handling to the V1 contract.
5. Verify the contract with script-style tests and a Phase 2 smoke replay.

## Verification

See `.planning/phases/02-service-product-contract/02-VERIFICATION.md`.
