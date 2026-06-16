---
phase: 17
status: safe_claim_table_locked
selected_path: Path C
final_claim_ready_status: false
generated_at: 2026-06-16T19:45:00+08:00
timezone: Asia/Shanghai
source_claim_guard: work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json
---

# Phase 17 Safe Claim Table

## Use Rule

This table converts planned manuscript claims into one of four allowed status
classes:

- supported status/provenance claim;
- conditional diagnostic claim;
- unsupported claim;
- future-work claim.

No row below authorizes `claim_ready=true` for empirical effectiveness. The
overall manuscript status remains:

```text
final_claim_ready_status=false
```

## Claim Table

| planned claim | status class | evidence source | allowed manuscript section | wording ceiling |
| --- | --- | --- | --- | --- |
| Dynamic service-menu formulation for many-to-one DRT with meeting point, pickup-window, price, home service, and outside option. | supported status/provenance claim | `.planning/paper/TR_E_RESEARCH_DESIGN.md`; Phase 13 evidence boundary; codebase map of `DSPO_Menu.py`, service-product containers, and choice/outside-option accounting. | Abstract, Introduction, Model, Methods | "We formulate a dynamic service-menu optimization problem and implement a gated evaluation pipeline." Do not say the formulation is empirically superior. |
| Paired replay evaluation design over the seven mainline policy tags. | supported status/provenance claim | Phase 13 EB-001; `formal_robust_menu` selected source run; paired replay and policy fairness contracts. | Methods, Experimental Design, Reproducibility | "The pipeline compares policies under paired replay settings." Do not say the resulting comparisons are claim-ready superiority evidence. |
| Artifact status, provenance, and claim gates are transparently reported (`C7_provenance_status_transparency`). | supported status/provenance claim | Phase 10 `CLAIM_GUARD.json`; Phase 13 EB-020; Phase 14 gate repair plan. | Abstract only if phrased as auditability; Methods; Reproducibility; Limitations | "Generated status artifacts disclose blockers, diagnostic scope, scaffold scope, and claim gates." Do not say transparency resolves empirical blockers. |
| Current main RC evidence identifies a profit-service-quality trade-off. | conditional diagnostic claim | Phase 15 random-baseline diagnosis; Phase 15 objective/evaluation alignment; selected 35-row formal source run. | Results, Discussion, Limitations | "In the selected diagnostic replay, optimized adaptive improves uptake/service metrics but realizes lower mean net profit than `mainline_random_menu` because additional service cost and discount cost dominate." Do not call this superiority. |
| ETA filter and robust time-window modes define diagnostic boundaries (`C5_eta_robustness_boundary`). | conditional diagnostic claim | Phase 8 sensitivity summary; Phase 10 `CLAIM_GUARD.json` C5 `diagnostic_only`; Phase 13 CF-007. | Results appendix, Sensitivity, Limitations | "ETA and no-filter variants are diagnostic boundary checks." Do not recommend no-filter operation. |
| Product and time-window ablations identify possible value drivers (`C2_product_ablation_value`). | conditional diagnostic claim | Phase 10 claim guard C2 `conditional_diagnostic_blocked`; Phase 13 CF-007; Phase 15 adaptive-window diagnosis. | Results, Discussion, Limitations | "Ablation tables are diagnostic structure for interpreting mechanisms." Do not say product ablation proves value. |
| Menu construction choices create measurable value (`C4_menu_construction_value`). | conditional diagnostic claim | Phase 10 claim guard C4 `conditional_diagnostic_blocked`; Phase 15 random-baseline diagnosis; Phase 15 objective/evaluation alignment. | Methods, Results, Discussion | "Menu construction is an auditable mechanism whose current realized-profit value is mixed and diagnostic." Do not say menu construction proves value. |
| Adaptive robust-menu policy superiority over baselines (`C1_central_adaptive_menu_superiority`). | unsupported claim | Phase 10 claim guard C1 `unsupported_blocked`; Phase 13 EB-004; Phase 15 random-baseline diagnosis. | Not allowed as a positive claim. Mention only as a blocked claim in limitations or evidence-boundary table. | "The current evidence does not support adaptive-menu superiority." Do not say adaptive menu dominates, outperforms, or is better than all baselines. |
| Adaptive time windows add a positive increment over fixed windows (`C3_adaptive_window_increment`). | unsupported claim | Phase 10 claim guard C3 `unsupported`; Phase 13 EB-005; Phase 15 adaptive-window diagnosis. | Not allowed as a positive claim. Mention only as a blocker. | "Adaptive-window increment is blocked because optimized adaptive and optimized fixed-window remain identical across tracked metrics." Do not say adaptive windows improve. |
| Exact-small and greedy-large solver behavior supports computational credibility (`C6_exact_greedy_computational_credibility`). | unsupported claim | Phase 9 tractability summary; Phase 10 claim guard C6 `blocked_diagnostic`; Phase 13 EB-012..EB-014. | Not allowed as a positive claim. Diagnostics may appear in appendix. | "Current tractability artifacts report diagnostic exact-solver behavior and unavailable greedy-quality evidence." Do not say near-optimal greedy or online tractability. |
| Semi-real case study validates the robust-menu findings (`C8_semi_real_case_validation`). | unsupported claim | Phase 7 scaffold-only status; Phase 10 claim guard C8 `scaffold_only_blocked`; Phase 13 EB-019. | Not allowed as validation. Scaffold may appear in Future Work only. | "Semi-real case material is scaffold-only." Do not say case-study validation, validated on real data, or real passenger behavior. |
| No-filter policies are operationally recommended. | unsupported claim | Phase 8 diagnostic-only boundary; Phase 13 CF-010; Phase 16 prohibited actions. | Not allowed. | "No-filter variants are diagnostic stress checks." Do not recommend deployment. |
| Adaptive-window value after fixing fixed/adaptive degeneracy. | future-work claim | Phase 15 adaptive-window diagnosis; Phase 16 Path C decision. | Future Work only | "A later pre-registered implementation-fix protocol would be needed to test adaptive-window value." Do not imply the current paper proves it. |
| Claim-ready final replay under frozen final settings. | future-work claim | `.planning/results/FROZEN_FINAL_SETTINGS.md`; Phase 16 decision sections 11-12. | Future Work only | "Frozen final settings remain a historical anti-p-hacking record, not Phase 17 rerun authorization." Do not say final rerun is authorized. |
| Exact-vs-greedy quality under large candidate pools. | future-work claim | Phase 9 tractability summary; Phase 13 CF-008; Phase 16 Path C decision. | Future Work only | "Future stress evidence must guarantee realized candidate counts above the greedy fallback threshold and report gap/overlap." Do not claim current near-optimality. |
| Executed semi-real case evidence over real geography. | future-work claim | Phase 7 case scaffold; Phase 13 CF-009; Phase 16 Path C decision. | Future Work only | "Future case execution would require reproducible data, matrices, demand, replay rows, and claim gates." Do not imply current validation. |

## Section-Level Ceiling

| manuscript section | maximum allowed claim |
| --- | --- |
| Abstract | Formulation, paired replay, transparent evidence boundaries, and diagnostic findings. No superiority, dominance, claim-ready, case-validation, or online-tractability wording. |
| Introduction | Motivation for service-menu design and wait-walk-price trade-offs. No statement that Work2 proves optimized adaptive menus outperform baselines. |
| Methods | Full service-menu formulation, paired replay design, policy family, checkpoint/provenance gates, and claim-guard logic. |
| Results | Diagnostic comparison only, including random-menu profit advantage and adaptive/fixed-window equality. |
| Sensitivity/Appendix | Diagnostic ETA, no-filter, sensitivity, and tractability boundary evidence only. |
| Conclusion | Conditional diagnostic contribution and future-work requirements. No claim upgrade. |

## Non-Conversion Rule

Supported status/provenance claims and conditional diagnostic claims must not be
converted into empirical superiority claims by placement, summary wording,
figure captions, abstracts, conclusions, highlights, or reviewer-response
language.
