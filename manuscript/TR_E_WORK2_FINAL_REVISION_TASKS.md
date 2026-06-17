# Work2 TR-E Final Revision Tasks

## Overall Recommendation

Recommendation: revise-before-submission.

The manuscript is not claim-ready empirical. It is currently a conditional
diagnostic service-menu optimization manuscript. The Phase 6 hard-contract
checks passed, so the package is not classified as `not ready`, but it should
not be submitted to TR-E as-is. The revision should improve journal fit,
model rigor, empirical-credibility framing, and prose quality while preserving
the strict `claim_ready=false` claim ceiling.

## Submission Blockers

No hard manuscript-package blockers were found for the conditional diagnostic
route during Phase 6 verification.

Claim-ready empirical submission remains blocked by evidence state, not by a
Phase 6 file-contract failure:

- Source references:
  - `.planning/milestones/tr_e_completion/M4A_FINAL_REPLAY_REPORT.md`
  - `.planning/milestones/tr_e_completion/M4B_DIAGNOSTIC_MANUSCRIPT_LOCK.md`
  - `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
  - `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`
- Completion criteria:
  - Do not submit the paper as claim-ready empirical while `claim_ready=false`.
  - Keep final recommendation and conclusion language conditional diagnostic.
  - Treat any future claim upgrade as a new evidence-regeneration milestone,
    not an editorial change.

## Major Revisions

### 1. Sharpen the TR-E novelty argument

Source references:

- `.planning/paper/TR_E_RESEARCH_DESIGN.md`
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`
- `.planning/milestones/tr_e_completion/M6_FINAL_TR_E_READINESS_AUDIT.md`

Action:

Rewrite the Introduction and Literature Review so the central contribution is
dynamic displayed service-menu optimization for many-to-one DRT. Make clear
that the decision object is a displayed bundle `b=(m,w,p)` and that meeting
points, pickup windows, pricing, passenger choice, route feasibility, and
opt-out accounting are jointly modeled.

Completion criteria:

- Introduction states the service-menu decision object in the first two pages.
- Literature Review distinguishes the paper from generic DRT routing,
  assortment optimization, pricing-only, and algorithm-ranking papers.
- No paragraph implies empirical superiority or dominance.

### 2. Expand model rigor for reviewer readability

Source references:

- `.planning/paper/TR_E_MANUSCRIPT_STRUCTURE.md`
- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`
- `work2_coding/Src/paired_replay.py`
- `work2_coding/Src/policy_adapters.py`

Action:

Strengthen the Mathematical Model and Solution Method sections. Define sets,
decision variables, feasibility constraints, outside-option accounting,
choice probabilities, objective terms, menu-size constraints, and
menu-construction contracts in a way that can be reviewed independently of the
planning documents.

Completion criteria:

- Mathematical Model has explicit notation for candidate bundles, displayed
  menu, outside option, accepted home pickup, accepted meeting-point pickup,
  and opt-out.
- Solution Method separates candidate generation, ETA/window handling,
  pricing, menu selection, and diagnostic computational limits.
- Exact/greedy material is framed as contract/diagnostic status only.

### 3. Reframe empirical credibility as claim-gated diagnostic evidence

Source references:

- `manuscript/TR_E_WORK2_CLAIM_AUDIT.md`
- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/CLAIM_GUARD.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_STATUS.json`

Action:

Revise Results and Discussion so package status, source-family status,
claim-guard status, and blocked claims are clearly reported without making the
paper feel like only a status memo. Use C5 only as diagnostic boundary
material and C7 only as status/provenance transparency.

Completion criteria:

- Results begins with claim-gate status and then explains what diagnostic
  evidence can and cannot support.
- C1, C2, C3, C4, C6, and C8 remain blocked from positive claim language.
- C5 and C7 are described with their exact allowed-use boundaries.
- No-filter, case-scaffold, and exact/greedy material are not presented as
  operational recommendations or validation.

### 4. Improve reproducibility and traceability presentation

Source references:

- `manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md`
- `.planning/paper/TABLE_FIGURE_CLAIM_MAP.md`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/PACKAGE_INDEX.json`
- `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/ARTIFACT_TO_SECTION_MAP.json`

Action:

Convert the source-map material into submission-ready tables or appendix text.
Every manuscript object should identify source path, claim ID, claim status,
allowed manuscript use, and evidence class.

Completion criteria:

- Every planned table and figure has a source path and claim ID.
- Conceptual objects are labeled conceptual and do not support empirical
  claims.
- Root `artifacts/` paths are treated as mirrors, not independent evidence
  sources.

### 5. Perform a full academic prose pass

Source references:

- `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`
- `manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md`
- `.planning/milestones/tr_e_completion/M4B_REVIEWER_RISK_RESPONSE_PLAN.md`

Action:

Edit the draft for journal tone, paragraph flow, contribution hierarchy,
concise limitations, and reviewer-facing clarity. Keep claim-safe verbs such
as `formulate`, `evaluate`, `diagnose`, `audit`, and `identify boundary
conditions`.

Completion criteria:

- Abstract, Introduction, Results, Discussion, and Conclusion use polished
  academic prose.
- Limitations are explicit but not apologetic.
- Reviewer-risk responses are integrated into the manuscript rather than left
  only in planning files.

## Minor Revisions

### 1. Standardize terminology

Action:

Use consistent terms for outside option, opt-out, accepted home pickup,
accepted meeting-point pickup, displayed menu, service bundle, diagnostic
evidence, and claim guard.

Completion criteria:

- Terminology is consistent across Abstract, Problem Description, Model,
  Experimental Design, Results, and Conclusion.

### 2. Prepare final table and appendix labels

Action:

Add submission-ready captions that identify diagnostic, blocked, scaffold-only,
or conceptual status.

Completion criteria:

- Captions do not imply claim-ready empirical evidence.
- Appendix labels match the source-map evidence class.

### 3. Preserve prohibited-language scan discipline

Action:

Re-run the prohibited-language scan after each major prose revision and record
allowed hits.

Completion criteria:

- Any hit is either removed or classified as blocked/status discussion.

## Section-by-Section Implementation Map

| Section | Revision focus | Evidence guard |
| --- | --- | --- |
| Abstract | Make conditional diagnostic status and service-menu contribution concise. | State `claim_ready=false`; no positive empirical effects. |
| Introduction | Strengthen novelty and transportation operations motivation. | Avoid superiority, dominance, and validation language. |
| Literature Review | Position against DRT, meeting points, assortment/menu design, pricing, and reproducibility. | Do not claim the paper closes all empirical gaps. |
| Problem Description | Clarify displayed bundles, route state, outside option, and opt-out separation. | Keep outside option separate from accepted home pickup. |
| Mathematical Model | Expand notation, constraints, choice model, and objective interpretation. | Treat the model as formulation, not proof of performance. |
| Solution Method | Explain candidate generation, ETA/window handling, pricing, exact enumeration, and greedy fallback. | Keep exact/greedy credibility diagnostic only. |
| Experimental Design | Explain paired replay, policy tags, evidence tiers, and claim gates. | Preserve paired fairness and checkpoint/load-status boundaries. |
| Results | Lead with claim-gate status, source-family status, and diagnostic findings. | C1/C2/C3/C4/C6/C8 blocked; C5 diagnostic; C7 status only. |
| Discussion | Convert blocked claims into limitations and future work. | No evidence upgrade without regenerated strict guard. |
| Conclusion | End with conditional diagnostic contribution and future claim-ready path. | Do not conclude empirical superiority. |
| Appendix | Place source map, diagnostics, computational status, case scaffold, and prohibited-language check. | Label evidence class for every object. |

## Final Pre-Submission Checklist

Run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_artifact_gates.py
python scripts/test_paired_replay_contract.py
python scripts/test_policy_fairness_contract.py
python scripts/test_manuscript_claim_guard.py
python scripts/test_manuscript_readiness_package.py
```

Run from repository root:

```powershell
Test-Path manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md
Test-Path manuscript/TR_E_WORK2_CLAIM_AUDIT.md
Test-Path manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md
Test-Path manuscript/TR_E_WORK2_PROHIBITED_LANGUAGE_CHECK.md
Test-Path manuscript/TR_E_WORK2_RESPONSE_TO_INTERNAL_REVIEW.md
rg -n "C1_central_adaptive_menu_superiority|C2_product_ablation_value|C3_adaptive_window_increment|C4_menu_construction_value|C5_eta_robustness_boundary|C6_exact_greedy_computational_credibility|C7_provenance_status_transparency|C8_semi_real_case_validation" manuscript/TR_E_WORK2_CLAIM_AUDIT.md
rg -n "Source artifact path|Claim ID|Claim status|Allowed manuscript use|Evidence class" manuscript/TR_E_WORK2_TABLE_FIGURE_SOURCE_MAP.md
rg -n -i "dominat|superior|outperform|near[- ]optimal|real passenger|case-study validation|semi-real validation|no-filter recommendation|operationally recommended|DSPO_PLUS|Behavior-Aware|TR-C|ranking validation|adaptive windows improve|greedy optimal" manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md
```

Human review checklist:

- Final recommendation remains `revise-before-submission` or a later
  evidence-backed status.
- The manuscript states conditional diagnostic status explicitly.
- No table, figure, or paragraph upgrades blocked claims.
- Every new table or figure has source path, claim ID, claim status, allowed
  use, and evidence class.
- The conclusion does not imply claim-ready empirical support.
