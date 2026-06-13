# Phase 2: Service Product Contract - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-13
**Phase:** 2-Service Product Contract
**Areas discussed:** Service product definition, time-window contract, menu baseline contract, normalized row and artifact gates

---

## Service Product Definition

| Option | Description | Selected |
|--------|-------------|----------|
| Unified contract | Home, meeting point, and opt-out are all explicit in the service contract; opt-out is an outcome and does not mutate routes. | yes |
| Displayed services only | Home and meeting point are products; opt-out remains only in the choice model. | |
| Meeting-point only | Only meeting-point bundles are products; home is fallback/baseline. | |

**User's choice:** Unified contract.
**Notes:** Opt-out must stay separate from accepted home pickup.

| Option | Description | Selected |
|--------|-------------|----------|
| Incremental feature contract | `m`, `m+w`, and `m+w+p` progressively add location, window, and price/incentive. | yes |
| Operational capability contract | Modes describe which levers the operator can change. | |
| User display contract | Modes describe which attributes are visible to the user. | |

**User's choice:** Incremental feature contract.
**Notes:** This supports product-ablation evidence.

| Option | Description | Selected |
|--------|-------------|----------|
| Passenger price/incentive | `p` is the passenger-facing price or incentive in MNL utility. | yes |
| System revenue term | `p` is primarily an operator revenue/profit term. | |
| Broad monetary attribute | `p` covers all monetary concepts. | |

**User's choice:** Passenger price/incentive.
**Notes:** System profit and cost fields remain separate.

| Option | Description | Selected |
|--------|-------------|----------|
| Extend existing dataclasses and metadata | Minimal object changes around `ServiceBundle` and `MenuOffer`. | |
| Add independent `ServiceProduct` dataclass | Create a clean contract-layer dataclass for `j=(m,w,p)`. | yes |
| Manifest/schema only | Do not add a domain object. | |

**User's choice:** Add independent `ServiceProduct` dataclass.
**Notes:** Planning must avoid turning this into a broad algorithm rewrite.

---

## Time-Window Contract

| Option | Description | Selected |
|--------|-------------|----------|
| Paper semantics first | Define `no_time_window`, `fixed_window`, and `adaptive_window` by product semantics. | yes |
| Runtime flags first | Map modes directly from `menu_time_filtering` and `menu_eta_filter_mode`. | |
| Display result first | Define modes by whether/which window is displayed. | |

**User's choice:** Paper semantics first.
**Notes:** `no_filter` must not be confused with `no_time_window`.

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed width aligned to candidate ETA | Common window width, center varies by candidate ETA/target rule. | yes |
| Fixed width and fixed center | All candidates share one center. | |
| Fixed discrete slot set | Map candidates to predeclared time-window slots. | |

**User's choice:** Fixed width aligned to candidate ETA.
**Notes:** Best fit with existing display-window parameters.

| Option | Description | Selected |
|--------|-------------|----------|
| Adaptive generation and filtering | ETA/risk may affect both window generation and candidate retention. | yes |
| Adaptive filtering only | Generate windows by fixed rule, then filter adaptively. | |
| Adaptive generation only | Keep all candidates but adjust windows/penalties. | |

**User's choice:** Adaptive generation and filtering.
**Notes:** `no_filter` remains diagnostic only.

| Option | Description | Selected |
|--------|-------------|----------|
| Gate by `product_mode` | `m` disables window utility; `m+w` and `m+w+p` enable it. | yes |
| Gate by `time_window_mode` | Any non-`no_time_window` mode enables window utility. | |
| Always compute | Compute time/window info regardless of displayed product mode. | |

**User's choice:** Gate by `product_mode`.
**Notes:** Row metadata must record both `product_mode` and `time_window_mode`.

---

## Menu Baseline Contract

| Option | Description | Selected |
|--------|-------------|----------|
| Structured baseline contract | `no_menu`, `fixed_menu`, `random_menu`, and `optimized_menu` are semantic modes mapped through adapters. | yes |
| Direct current-policy mapping | Define modes directly as current `menu_policy` values. | |
| Display-count mapping | Define no-menu as one option and menu modes as multiple options. | |

**User's choice:** Structured baseline contract.
**Notes:** Adapters will map semantic modes to current runtime policies.

| Option | Description | Selected |
|--------|-------------|----------|
| Single default home product | `no_menu` is a single home product. | yes |
| Single nearest meeting point | `no_menu` is one OOH service product. | |
| Single cheapest product | `no_menu` is the cheapest system option. | |

**User's choice:** Single default home product.
**Notes:** Opt-out remains outside outcome.

| Option | Description | Selected |
|--------|-------------|----------|
| Nearest/top-k proximity | Primary fixed baseline selects by proximity. | yes |
| Top-k cheapest predicted cost | Primary fixed baseline selects by predicted cost. | |
| Keep both fixed baselines | Include nearest and cheapest as formal fixed baselines. | |

**User's choice:** Nearest/top-k proximity.
**Notes:** `top_k_cheapest` stays supplemental or diagnostic.

| Option | Description | Selected |
|--------|-------------|----------|
| Same pool, same k, seeded deterministic random | Random baseline is paired and reproducible. | yes |
| Free random each step | Random selection changes freely during simulation. | |
| Pregenerated random manifest | Precompute random menus as manifest inputs. | |

**User's choice:** Same pool, same k, seeded deterministic random.
**Notes:** Required for paired replay fairness.

| Option | Description | Selected |
|--------|-------------|----------|
| `service_guarded_expected_profit` | Main optimized menu balances profit with service/opt-out risk. | yes |
| `risk_adjusted_expected_profit` | Main optimized menu focuses on expected profit with ETA risk. | |
| Optimized family | Keep both and report one as primary. | |

**User's choice:** `service_guarded_expected_profit`.
**Notes:** This is the primary `optimized_menu` method.

| Option | Description | Selected |
|--------|-------------|----------|
| Home always retained outside OOH `menu_k` | Home is available in multi-option menus and does not count against OOH slots. | yes |
| Home only in `no_menu` | Multi-option menus contain only meeting points. | |
| Home counts toward menu size | Home is optional and consumes one displayed slot. | |

**User's choice:** Home always retained outside OOH `menu_k`.
**Notes:** Supports connection to home baseline.

| Option | Description | Selected |
|--------|-------------|----------|
| Main `menu_k={1,2,3,5}` | Compare multiple menu sizes in the main experiment. | yes |
| Main `menu_k={2,3,4}` | Narrower cost-saving comparison. | |
| Main `menu_k={1,3,5}` | Sensitivity-style comparison. | |

**User's choice:** Main `menu_k={1,2,3,5}`.
**Notes:** User first selected multi-k, then selected the specific set `{1,2,3,5}`.

---

## Normalized Row And Artifact Gates

| Option | Description | Selected |
|--------|-------------|----------|
| `normalized-row-v2` | Upgrade row schema for Phase 2 contract fields. | yes |
| Append to v1 | Keep `normalized-row-v1` and add fields. | |
| Metadata only | Put new fields into metadata. | |

**User's choice:** `normalized-row-v2`.
**Notes:** New contract fields become explicit schema fields.

| Option | Description | Selected |
|--------|-------------|----------|
| Full required contract field set | Require `product_mode`, `time_window_mode`, `menu_mode`, `pricing_mode`, `method`, `candidate_id`, `study_id`, `manifest_path`. | yes |
| Core modes only | Require only product/time-window/menu/pricing modes. | |
| Gate later | Make fields optional and rely on artifact gates. | |

**User's choice:** Full required contract field set.
**Notes:** These fields are mandatory in normalized rows.

| Option | Description | Selected |
|--------|-------------|----------|
| Aggregate rows use `candidate_id="aggregate"` | Keep aggregate rows compact and write true candidate IDs to per-product traces. | yes |
| One row per candidate | Normalize every candidate product into main rows. | |
| Empty candidate ID allowed | Keep field mandatory but allow empty string. | |

**User's choice:** Aggregate rows use `candidate_id="aggregate"`.
**Notes:** Avoids exploding aggregate rows.

| Option | Description | Selected |
|--------|-------------|----------|
| Canonical composed method | `method` is derived from product, time-window, menu, and pricing modes. | yes |
| Policy tag method | `method` equals `policy_tag`. | |
| Human-readable label | `method` is a prose label. | |

**User's choice:** Canonical composed method.
**Notes:** Artifact builders can derive display labels.

| Option | Description | Selected |
|--------|-------------|----------|
| Failed row per policy/split | Write `status=failed` rows with `error_type` and `error_message`; continue batch. | yes |
| Summary blocker only | Do not emit normalized failed rows. | |
| Abort formal run | Stop on first formal failure. | |

**User's choice:** Failed row per policy/split.
**Notes:** Enables auditability without losing batch progress.

| Option | Description | Selected |
|--------|-------------|----------|
| Separate cost/profit fields | Record `net_profit`, `operational_cost`, `total_cost`, and `net_price_revenue`. | yes |
| Objective proxy only | Keep only `net_objective_proxy`. | |
| Defer profit fields | Keep current revenue/discount/service fields for now. | |

**User's choice:** Separate cost/profit fields.
**Notes:** Do not conflate passenger price `p` with system profit.

| Option | Description | Selected |
|--------|-------------|----------|
| Full behavior metrics | Require accepted/served/optout/home/meeting/utilization/entropy metrics. | yes |
| Core acceptance metrics only | Defer utilization and entropy. | |
| Optional artifact metrics | Make all behavior metrics optional. | |

**User's choice:** Full behavior metrics.
**Notes:** Required behavior metrics are captured in CONTEXT.md.

| Option | Description | Selected |
|--------|-------------|----------|
| Hard formal-claim exclusion | Exclude diagnostic, no-filter, failed, placeholder, and contract-only rows from formal claims. | yes |
| Diagnostic can enter tables only | Allow diagnostic rows in tables but not claims. | |
| Manuscript-stage filtering only | Do not enforce at row/artifact stage. | |

**User's choice:** Hard formal-claim exclusion.
**Notes:** Formal claim gates must enforce this before manuscript claims.

| Option | Description | Selected |
|--------|-------------|----------|
| Phase directory context | Write `.planning/phases/02-service-product-contract/02-CONTEXT.md` and log. | yes |
| Flat planning file | Write a temporary root planning file. | |
| Chat only | Do not write planning files. | |

**User's choice:** Phase directory context.
**Notes:** Current standard GSD roadmap/state files are missing, so only the phase context/log are written.

---

## the agent's Discretion

None.

## Deferred Ideas

None.
