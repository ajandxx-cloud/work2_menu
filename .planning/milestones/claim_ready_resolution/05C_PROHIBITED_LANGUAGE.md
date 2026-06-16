---
phase: 17
status: prohibited_language_locked
selected_path: Path C
final_claim_ready_status: false
generated_at: 2026-06-16T19:45:00+08:00
timezone: Asia/Shanghai
---

# Phase 17 Prohibited Manuscript Language

## Global Rule

The manuscript must not use language that implies `claim_ready=true` or
positive empirical superiority. The binding status is:

```text
final_claim_ready_status=false
```

The following prohibitions apply to abstract, introduction, methods, results,
discussion, conclusion, highlights, figure captions, table captions, cover
letters, and reviewer responses.

## Explicitly Prohibited Phrases And Meanings

| prohibited language or meaning | reason | allowed replacement |
| --- | --- | --- |
| "adaptive-menu dominance" | C1 is `unsupported_blocked`; random menu has higher mean realized net profit. | "diagnostic comparison of adaptive and baseline menus" |
| "adaptive-menu superiority" | Positive central superiority is prohibited by Phase 16 and Phase 17. | "optimized adaptive improves some service metrics but does not support a superiority claim" |
| "adaptive menu dominates all baselines" | Universal dominance is false under current tracked metrics. | "baseline comparisons expose trade-offs and blockers" |
| "robust menu is better than all baselines" | The random baseline currently outperforms adaptive on mean net profit. | "robust-menu evidence is diagnostic under current gates" |
| "adaptive-window increment" | C3 is unsupported and optimized adaptive equals optimized fixed-window across tracked metrics. | "adaptive-window increment is blocked under current evidence" |
| "adaptive-window superiority" | Current implementation/configuration appears behaviorally degenerate for fixed versus adaptive windows. | "fixed/adaptive equality motivates future implementation verification" |
| "near-optimal greedy" | Phase 9 did not establish exact-vs-greedy quality or fallback behavior. | "diagnostic tractability artifacts report candidate counts and build-time evidence where available" |
| "online tractability" | Current evidence does not prove online scalability or greedy quality. | "computational credibility remains future work" |
| "case-study validation" | Case material is scaffold-only and has no executed rows or result artifacts. | "case-study scaffold for future validation" |
| "validated on real data" | No executed semi-real or real-data validation exists. | "future semi-real validation protocol" |
| "real passenger behavior" | Current demand and choice evidence is simulated or scaffold-only. | "simulated demand and choice under documented assumptions" |
| "no-filter operational recommendation" | No-filter evidence is diagnostic only. | "no-filter diagnostic boundary check" |
| "`claim_ready=true`" | Phase 17 locks `final_claim_ready_status=false`. | "`claim_ready=false` under current strict claim guard" |
| "claim-ready empirical paper" | Phase 17 locks a conditional diagnostic manuscript path. | "conditional diagnostic TR-E manuscript" |
| "frozen final settings authorize rerun" | Phase 16 says frozen settings are historical anti-p-hacking record, not rerun authorization. | "frozen settings preserve anti-p-hacking history but do not authorize Phase 17 rerun" |
| "random baseline is irrelevant" | `mainline_random_menu` is a serious comparator and currently profit-favorable. | "`mainline_random_menu` is retained as a primary comparator" |
| "sensitivity proves robustness" | Phase 8 remains diagnostic/provisional with `claim_ready=false`. | "sensitivity diagnostics identify boundary conditions" |
| "tractability is established" | Phase 9 remains diagnostic/provisional. | "tractability evidence is incomplete and diagnostic" |
| "provenance transparency proves effectiveness" | C7 supports status/provenance only, not empirical effectiveness. | "provenance transparency supports auditability" |

## Section-Specific Prohibitions

### Abstract

Do not write:

- "We show that adaptive menus outperform all baselines."
- "The proposed adaptive menu is superior."
- "The method is claim-ready."
- "The case study validates the approach."
- "The greedy algorithm is near-optimal and online tractable."

Allowed ceiling:

- "We formulate and audit a service-menu optimization pipeline and report
  diagnostic paired-replay evidence that identifies current claim boundaries."

### Introduction

Do not motivate the paper by promising proof of adaptive-menu superiority,
adaptive-window value, online tractability, or real-case validation.

Allowed ceiling:

- The introduction may motivate wait, walk, price, and reliability trade-offs
  and explain why service menus are an important design object.

### Results

Do not suppress or soften the result that `mainline_random_menu` currently
beats `mainline_optimized_adaptive` on mean net profit. Do not report only
metrics favorable to optimized adaptive.

Allowed ceiling:

- Results may state that optimized adaptive improves acceptance and reduces
  opt-out while incurring higher realized operating and discount costs that
  block a net-profit superiority claim.

### Discussion And Conclusion

Do not turn diagnostic findings into managerial recommendations. Do not say
transport operators should deploy no-filter policies, adaptive windows, or
optimized adaptive menus based on current evidence.

Allowed ceiling:

- The conclusion may state that the evidence supports a transparent
  conditional diagnostic contribution and identifies what future evidence is
  needed.

## Captions And Tables

Captions must not create stronger claims than the body text. Table and figure
captions for policy comparisons must include diagnostic status where needed
and must not use "best", "dominant", "superior", "validated", "optimal",
"near-optimal", or "claim-ready" unless the text is explicitly describing a
prohibited or blocked claim.

## Enforcement Note

Any future manuscript edit that uses prohibited language must be revised before
submission or review. Wording cannot override `CLAIM_GUARD.json`.
