---
phase: 05
slug: tr-e-manuscript-draft-construction
status: complete
created: 2026-06-17
---

# Phase 05 Pattern Map

## Purpose

This map identifies the closest local analogs and source-of-truth files for
Phase 5 manuscript planning. It is a planning artifact only; it does not
modify generated evidence.

## Files To Create

| Target file | Role | Closest analogs | Source-of-truth inputs |
| --- | --- | --- | --- |
| `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md` | Main TR-E diagnostic manuscript draft | `manuscript/main.tex`, `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`, generated manuscript-frame outlines under `work2_coding/artifacts/work2_robust_menu/manuscript/` when present | `.planning/phases/05-.../05-CONTEXT.md`, `.planning/paper/TR_E_RESEARCH_DESIGN.md`, `M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`, `CLAIM_GUARD.json` |
| `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md` | Paper object traceability table | `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`, `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/artifact_to_section_map.md` | `ARTIFACT_TO_SECTION_MAP.json`, `PACKAGE_INDEX.json`, `PACKAGE_STATUS.json`, `M4B_SAFE_CLAIM_TABLE.md` |
| `manuscript/TR_E_WORK2_CLAIM_AUDIT.md` | Claim-by-claim manuscript audit | `M4B_SAFE_CLAIM_TABLE.md`, `claim_checklist.md`, `safe_language_boundaries.md` | `CLAIM_GUARD.json`, `.planning/paper/CLAIM_SAFE_LANGUAGE.md` |
| `manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md` | Body wording audit | `.planning/paper/CLAIM_SAFE_LANGUAGE.md`, `safe_language_boundaries.md` | `TR_E_WORK2_MANUSCRIPT_DRAFT.md`, `M4B_SAFE_CLAIM_TABLE.md` |
| `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md` | Migration and reviewer-risk response record | `M4B_REVIEWER_RISK_RESPONSE_PLAN.md`, legacy GSD execution report in `manuscript/main.tex` | legacy unsafe-term scan, Phase 4 risk plan, claim audit |

## Existing Code And Document Patterns

### Manuscript Frame Builder

`work2_coding/Src/manuscript_claims.py` generates method, experiment, result,
and claim-checklist frames from artifact status. Useful patterns:

- Claim guards are derived from status data, not manual optimism.
- Blocked claims are explicitly enumerated.
- No-filter and real-passenger validation claims are always blocked unless
  evidence changes.
- Method and experiment outlines use status language rather than performance
  superiority language.

Phase 5 should use those patterns in manuscript prose and companion audits, but
the deliverable is a full academic manuscript draft, not just generated frame
snippets.

### Package Status And Claim Guard

`PACKAGE_STATUS.json` and `CLAIM_GUARD.json` provide the canonical current
claim boundary. Useful fields:

- `claim_ready`
- `strict_claim_guard_claim_ready`
- `manuscript_positive_claims_allowed`
- `source_family_status`
- `blocked_claim_ids`
- per-claim `support_status`
- per-claim `manuscript_allowed`
- per-claim `safe_language`
- per-claim `forbidden_language`
- per-claim `source_artifacts`

Phase 5 should not infer stronger language from any single source artifact.

### Legacy Manuscript

`manuscript/main.tex` is a migration source, not the main drafting surface.

Reusable:

- Elsevier metadata and bibliography context.
- MNL formula and service bundle notation.
- Literature references.
- Basic problem/method skeleton.

Rewrite or remove:

- `Behavior-Aware` title framing.
- TR-C framing.
- `DSPO_PLUS` as central v1 narrative.
- dominance, improvement, superiority, validation, or ranking-validation
  language.
- results language that promises a future ranking test instead of reporting
  current diagnostic-lock status.

### Script-Style Verification

Existing test style uses direct Python scripts and explicit `PASS` lines. For
Phase 5, plan verification should combine:

- `cd work2_coding; python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`
- `cd work2_coding; python scripts/test_manuscript_claim_guard.py`
- PowerShell source assertions for manuscript sections and audit/source-map
  columns.

## Data Flow For Execution

1. Read current claim/evidence sources.
2. Build source map and claim audit before drafting.
3. Draft body paragraphs with source-map references for every object.
4. Run prohibited-language scan against the draft body.
5. Record migration decisions and reviewer-risk responses.
6. Re-run source assertions and script-style tests.

## Landmines

- Do not update `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`,
  generated tables, figures, mirrors, or normalized rows by hand.
- Do not cite root `artifacts/` as canonical when a `work2_coding/artifacts/`
  source exists.
- Do not treat `C7_provenance_status_transparency` as empirical support.
- Do not move no-filter material out of diagnostic boundary language.
- Do not describe case scaffolds as executed, semi-real validation, or real
  passenger behavior.
- Do not describe Phase 9 exact/greedy diagnostics as near-optimality or
  computational credibility evidence.
- Keep opt-out separate from accepted home pickup and accepted meeting-point
  pickup in the model, metrics, and result prose.

## PATTERN MAPPING COMPLETE

