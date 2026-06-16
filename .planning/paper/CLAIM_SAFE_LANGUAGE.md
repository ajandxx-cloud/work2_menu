---
phase: 11
status: claim_safe_language_plan
generated_at: 2026-06-16T14:11:38+08:00
timezone: Asia/Shanghai
source_claim_guard: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json
claim_guard_schema: phase10-strict-claim-guard-v1
phase10_claim_count: 8
claim_ready: false
manuscript_positive_claims_allowed: false
---

# Claim-Safe Language For TR Part E Manuscript Drafting

## Conversion Rule

This file converts the eight Phase 10 strict-guard claims into manuscript-safe
language categories. Because Phase 10 reports overall `claim_ready=false`, no
claim is upgraded beyond the strict guard. "Supported" below means supported
only for the stated narrow status/provenance purpose, not for empirical
effectiveness.

Category definitions:

- **supported:** may be stated in the manuscript for the narrow claim described.
- **conditional:** reserved for future evidence that passes gates; no current
  Phase 10 claim is upgraded to this category.
- **diagnostic/provisional:** may be discussed as diagnostic boundary evidence
  or artifact structure only, with `claim_ready=false` visible.
- **unsupported:** must not be written as a positive manuscript claim.

## Claim Language Matrix

| Phase 10 claim | Strict support status | Converted category | Manuscript use |
| --- | --- | --- | --- |
| `C1_central_adaptive_menu_superiority` | `unsupported_blocked` | unsupported | Do not make a positive central performance claim |
| `C2_product_ablation_value` | `conditional_diagnostic_blocked` | diagnostic/provisional | Use only as blocked diagnostic ablation structure |
| `C3_adaptive_window_increment` | `unsupported` | unsupported | Do not make directional adaptive-window claims |
| `C4_menu_construction_value` | `conditional_diagnostic_blocked` | diagnostic/provisional | Use only as auditable mechanism and diagnostic structure |
| `C5_eta_robustness_boundary` | `diagnostic_only` | diagnostic/provisional | May discuss ETA/no-filter boundaries as diagnostic only |
| `C6_exact_greedy_computational_credibility` | `blocked_diagnostic` | diagnostic/provisional | May report available solver diagnostics; no credibility upgrade |
| `C7_provenance_status_transparency` | `status_supported` | supported | May state artifact/status/claim gates are transparently reported |
| `C8_semi_real_case_validation` | `scaffold_only_blocked` | unsupported | Do not present case scaffold as validation |

## Per-Claim Safe Wording

### C1: Central Adaptive Menu Superiority

Converted category: unsupported.

Safe manuscript wording:

- "The Phase 10 package records the adaptive robust-menu comparison as a
  generated artifact and status structure, but strict claim guards block any
  superiority interpretation."
- "The current package identifies formal-readiness and checkpoint/provenance
  blockers that must be resolved before central empirical claims can be made."

Prohibited manuscript wording:

- "adaptive menu dominates"
- "universal dominance"
- "claim-ready superiority"
- "robust menu is better than all baselines"

Required boundary:

- Any mention of the central comparison must include `claim_ready=false` or an
  equivalent sentence stating that positive empirical superiority is blocked.

### C2: Product Ablation Value

Converted category: diagnostic/provisional.

Safe manuscript wording:

- "The ablation artifacts define diagnostic comparison slots for product and
  time-window variants."
- "The current ablation interpretation remains blocked pending formal
  claim-ready evidence."

Prohibited manuscript wording:

- "product ablation proves"
- "adaptive window increment is validated"
- "claim-ready ablation value"

Required boundary:

- Product and time-window ablation content can appear in Results or Appendix
  only as diagnostic structure, not as a claim that a product dimension has
  been validated.

### C3: Adaptive Window Increment

Converted category: unsupported.

Safe manuscript wording:

- "The fixed-window and adaptive-window full-product variants are included as
  planned comparison slots in the artifact package."
- "The current strict guard does not authorize directional language about the
  adaptive-window increment."

Prohibited manuscript wording:

- "adaptive windows improve"
- "adaptive window increment"
- "adaptive window advantage"

Required boundary:

- Avoid all directional verbs for adaptive windows until future claim-ready
  evidence exists.

### C4: Menu Construction Value

Converted category: diagnostic/provisional.

Safe manuscript wording:

- "Menu construction is treated as an auditable mechanism with generated
  diagnostic artifacts."
- "Exact and greedy rows should be interpreted as computational-boundary
  diagnostics under the current `claim_ready=false` package."

Prohibited manuscript wording:

- "menu construction proves value"
- "near-optimal greedy"
- "greedy is optimal"

Required boundary:

- Menu construction language must describe mechanism, diagnostics, or artifact
  structure only.

### C5: ETA Robustness Boundary

Converted category: diagnostic/provisional.

Safe manuscript wording:

- "ETA filter and no-filter variants are reported as diagnostic boundary
  checks."
- "No-filter results are retained as diagnostic stress-test evidence, not as
  an operational recommendation."

Prohibited manuscript wording:

- "no-filter recommendation"
- "no-filter is operationally recommended"
- "no-filter policy should be deployed"

Required boundary:

- Each no-filter reference must include "diagnostic" or "stress-test" language.

### C6: Exact-Greedy Computational Credibility

Converted category: diagnostic/provisional.

Safe manuscript wording:

- "Phase 9 reports auditable computational diagnostics, including candidate
  counts, enumerated menu counts, effective solver mode, build time, and
  blocked gap/overlap fields where unavailable."
- "The configured large-scale rows did not establish greedy fallback quality,
  so computational-credibility claims remain blocked."

Prohibited manuscript wording:

- "near-optimal greedy"
- "full dynamic exact optimality"
- "greedy optimality"

Required boundary:

- Computational sections may report observed diagnostics but must not present
  exact-vs-greedy quality, gap, overlap, or online tractability as claim-ready.

### C7: Provenance Status Transparency

Converted category: supported.

Safe manuscript wording:

- "The generated package discloses artifact status, source paths, diagnostic
  scope, scaffold scope, and strict claim gates."
- "This transparency claim concerns provenance and manuscript claim control; it
  does not establish empirical effectiveness."

Prohibited manuscript wording:

- "status transparency proves effectiveness"
- "provenance resolves empirical blockers"

Required boundary:

- C7 is the only Phase 10 claim that is claim-ready, and only for
  provenance/status transparency.

### C8: Semi-Real Case Validation

Converted category: unsupported.

Safe manuscript wording:

- "The semi-real case materials are documented as a future-study scaffold."
- "Case-study scaffold artifacts are excluded from result-table and validation
  language."

Prohibited manuscript wording:

- "case-study validation"
- "semi-real validation"
- "real passenger behavior"
- "validated on real data"

Required boundary:

- Case material belongs in Appendix or future work unless a later phase
  produces executed, reproducible, claim-gated case evidence.

## Global Prohibited Wording

The manuscript must not include the following wording outside a prohibited
language checklist:

- "adaptive menu dominates"
- "universal dominance"
- "claim-ready superiority"
- "robust menu is better than all baselines"
- "product ablation proves"
- "adaptive window increment is validated"
- "claim-ready ablation value"
- "adaptive windows improve"
- "adaptive window increment"
- "adaptive window advantage"
- "menu construction proves value"
- "near-optimal greedy"
- "greedy is optimal"
- "no-filter recommendation"
- "no-filter is operationally recommended"
- "no-filter policy should be deployed"
- "full dynamic exact optimality"
- "greedy optimality"
- "status transparency proves effectiveness"
- "provenance resolves empirical blockers"
- "case-study validation"
- "semi-real validation"
- "real passenger behavior"
- "validated on real data"

## Required Manuscript Disclaimers

Use these disclaimers where relevant:

- "All empirical result language in this section is bounded by Phase 10
  `claim_ready=false`."
- "This table is included for source/status traceability and diagnostic
  context, not as claim-ready evidence."
- "No-filter variants are diagnostic stress tests, not operational
  recommendations."
- "The semi-real case materials are scaffold-only and do not validate
  performance or passenger behavior."
- "Provenance transparency does not resolve empirical blockers."
