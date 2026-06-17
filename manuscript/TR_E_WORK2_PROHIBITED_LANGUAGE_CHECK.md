# Work2 TR-E Prohibited Language Check

**Purpose:** prevent the Phase 5 draft from exceeding the strict claim guard.
**Body scan target:** `manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md`
**Current body scan status:** pending until Plan 03.

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

Pending Plan 03 scan:

```powershell
rg -n -i "dominat|superior|outperform|near[- ]optimal|real passenger|case-study validation|semi-real validation|no-filter recommendation|operationally recommended|DSPO_PLUS|Behavior-Aware|TR-C|ranking validation|adaptive windows improve|greedy optimal" manuscript/TR_E_WORK2_MANUSCRIPT_DRAFT.md
```

Each hit will be classified as `removed`, `allowed only as prohibited-language quote`, `allowed as blocked-claim/status discussion`, or `requires Phase 6 review`.
