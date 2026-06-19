# Research Summary: Work2 TR-E Manuscript Completion

**Created:** 2026-06-16

## Source Basis

This regenerated summary is based on the TR-E manuscript completion prompt,
the current workspace, current `.planning/codebase/` maps, the existing Phase
10 paper artifact package, and a runtime import smoke check.

No internet research, final replay, artifact regeneration, or generated-row
editing was performed during this initialization.

## Current Evidence Facts

- Active runtime root: `work2_coding/`.
- Import smoke from repository root passed:
  `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`.
- Phase 10 paper package exists under:
  - `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`
  - `artifacts/work2_robust_menu/phase10_paper_artifacts/`
- `PACKAGE_STATUS.json` reports:
  - `artifact_count`: 74
  - `existing_artifact_count`: 70
  - `missing_artifact_count`: 4
  - `blocker_count`: 108
  - `claim_ready`: false
  - `strict_claim_guard_claim_ready`: false
- Source families currently have these statuses:
  - `main_rc`: blocked
  - `phase8_sensitivity`: diagnostic_provisional_blocked
  - `phase9_tractability`: diagnostic_provisional_blocked
  - `case_scaffold`: scaffold_only_no_result_evidence
  - `blocker_status`: blocked
- The current root `ARTIFACT_STATUS.json` is blocked by missing pilot
  checkpoint provenance and skipped formal evidence.

## Claim Guard Summary

Current strict claim statuses:

| Claim ID | Status | Manuscript use |
| --- | --- | --- |
| C1_central_adaptive_menu_superiority | unsupported_blocked | Not allowed |
| C2_product_ablation_value | conditional_diagnostic_blocked | Not allowed as positive claim |
| C3_adaptive_window_increment | unsupported | Not allowed |
| C4_menu_construction_value | conditional_diagnostic_blocked | Not allowed as positive claim |
| C5_eta_robustness_boundary | diagnostic_only | Allowed only as diagnostic boundary |
| C6_exact_greedy_computational_credibility | blocked_diagnostic | Not allowed as computational credibility claim |
| C7_provenance_status_transparency | status_supported | Allowed as status/provenance transparency only |
| C8_semi_real_case_validation | scaffold_only_blocked | Not allowed |

## Paper Framing

The paper should be framed as a transportation logistics and service operations
study of dynamic service-menu optimization for many-to-one DRT. It should not
be framed as an attention model paper, pricing-only paper, or pure
algorithm-ranking exercise.

The central decision object is the displayed menu of service bundles:

```text
b = (meeting point, pickup time window, price)
```

The contribution ceiling depends on evidence:

- If strict readiness and claim guard gates pass, the paper may state only the
  specific positive or conditional claims authorized by the regenerated guard.
- If `claim_ready=false`, the paper must be a conditional diagnostic manuscript
  about formulation, paired replay, service trade-offs, and transparent
  claim-boundary control.

## Main Risks

- Dirty or missing provenance can block formal claim readiness.
- Missing checkpoint files or failed checkpoint loading can block claim-ready
  evidence.
- Main RC artifacts currently remain blocked.
- Phase 8 and Phase 9 outputs are useful as diagnostic boundary evidence but
  do not authorize positive claims.
- Case-study scaffolds do not validate real passenger behavior.
- Manuscript wording can easily overstep the generated claim ceiling.

## Planning Implication

The regenerated roadmap should start with repository and evidence boundary
audit, then decide whether a legitimate claim-ready rerun exists. Manuscript
drafting should happen only after the claim path is selected.

---
*Research summary regenerated: 2026-06-16*
