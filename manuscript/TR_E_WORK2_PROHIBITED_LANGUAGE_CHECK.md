# Work2 TR-E Prohibited Language Check

**Purpose:** prevent the Phase 5 draft from exceeding the strict claim guard.
**Body scan target:** `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`
**Current body scan status:** complete on 2026-06-17.

## Forbidden Phrase Inventory

These terms may appear in this audit file as forbidden examples, but they must not appear in the manuscript body as unqualified positive claims:

| Term or phrase | Claim risk | Allowed handling |
| --- | --- | --- |
| dominance; dominate; dominates | C1, C4 | Only as prohibited-language quote or blocked-claim discussion |
| superiority; superior | C1 | Only as blocked claim status, not as a result |
| outperform; outperforms; outperformed | C1 | Avoid in body unless explicitly negated as unauthorized |
| improvement; improve; improves; advantage | C2, C3 | Avoid directional effect language |
| prove; proves; validated; validation | C2, C8 | Avoid proof or validation language for empirical claims |
| near-optimal; optimal greedy; greedy optimality | C6 | Only as prohibited-language quote |
| real passenger behavior; real passenger | C8 | Only as denied/scaffold-boundary language |
| case-study validation; semi-real validation | C8 | Only as prohibited-language quote |
| no-filter recommendation; operationally recommended | C5 | Only as prohibited-language quote |
| DSPO_PLUS | scope/framing | Legacy term; do not foreground in Phase 5 title, abstract, or contribution frame |
| Behavior-Aware | scope/framing | Legacy term; do not foreground |
| TR-C | venue/framing | Legacy draft venue; Phase 5 target is TR-E |
| ranking validation | C1 | Legacy promise; avoid as a claim |
| adaptive windows improve | C3 | Prohibited without future strict guard authorization |
| greedy optimal | C6 | Prohibited without future strict guard authorization |

## Legacy Draft Findings

`manuscript/main.tex` is a migration source only. Safe reusable material includes notation, mathematical model skeleton, MNL and menu-objective content, references, bibliography material, and Elsevier metadata. Unsafe legacy material to remove or rewrite includes TR-C framing, DSPO_PLUS foregrounding, Behavior-Aware foregrounding, policy-ranking promises, dominance language, validation language, and conclusion text that implies positive empirical support before claim gates pass.

## Final Draft Scan Results

Plan 03 ran:

```powershell
rg -n -i "dominat|superior|outperform|near[- ]optimal|real passenger|case-study validation|semi-real validation|no-filter recommendation|operationally recommended|DSPO_PLUS|Behavior-Aware|TR-C|ranking validation|adaptive windows improve|greedy optimal" manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md
```

Results:

| Draft line | Hit | Classification | Resolution |
| --- | --- | --- | --- |
| 101 | `C1_central_adaptive_menu_superiority` | allowed as blocked-claim/status discussion | The term appears only inside the strict claim ID table and is paired with `unsupported_blocked` and `Not allowed as a positive claim`. |
| 120 | `real passenger behavior` | allowed as blocked-claim/status discussion | The sentence explicitly answers that case material does not reflect real passenger behavior because C8 is scaffold-only. |

No unqualified positive claim was found using dominance, superiority, near-optimality, real-passenger validation, no-filter recommendation, DSPO_PLUS ranking, Behavior-Aware, TR-C, ranking validation, adaptive-window improvement, or greedy optimality language.
