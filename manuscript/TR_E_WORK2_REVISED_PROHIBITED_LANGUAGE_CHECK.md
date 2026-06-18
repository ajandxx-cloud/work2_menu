# Work2 TR-E Revised Prohibited Language Check

**Purpose:** verify that `manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md`
preserves the strict claim ceiling after the Phase 7 rewrite.
**Body scan target:** `manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md`
**Current strict status:** `claim_ready=false`

## Forbidden Phrase Inventory

This check uses the Phase 5 prohibited-language inventory and the Phase 7
plan scan. The following families remain unsafe when used as unqualified
positive claims:

| Term or phrase family | Claim risk | Allowed handling |
| --- | --- | --- |
| dominance or superiority language | C1, C4 | Only as blocked claim IDs or status discussion |
| outperform language | C1 | Avoid unless explicitly denied as unauthorized |
| near-optimal or greedy optimal language | C6 | Only as prohibited-language discussion |
| real passenger language | C8 | Only as explicit denial or scaffold-boundary discussion |
| case-study or semi-real validation language | C8 | Only as prohibited-language discussion |
| no-filter recommendation language | C5 | Only as prohibited-language discussion |
| legacy DSPO_PLUS, Behavior-Aware, TR-C, or ranking-validation framing | scope/framing | Do not foreground in the revised manuscript |
| adaptive windows improve | C3 | Prohibited without future strict guard authorization |

## Scan Command

```powershell
rg -n -i "dominat|superior|outperform|near[- ]optimal|real passenger|case-study validation|semi-real validation|no-filter recommendation|operationally recommended|DSPO_PLUS|Behavior-Aware|TR-C|ranking validation|adaptive windows improve|greedy optimal" manuscript/TR_E_WORK2_MANUSCRIPT_REVISED.md
```

## Scan Results

| Revised line | Hit | Classification | Resolution |
| --- | --- | --- | --- |
| 380 | `C1_central_adaptive_menu_superiority` | safe blocked-claim/status discussion | The hit appears only as a strict claim ID in the claim-boundary table, with status `unsupported_blocked` and allowed use `Not allowed as a positive claim; status and blockers only`. |
| 502 | `real passenger` | safe explicit denial | The sentence says the case scaffold cannot be presented as executed case evidence or real passenger evidence. |

## Final Status

PASS. No unqualified positive claim was found in the revised manuscript. The
remaining hits are safe because they appear only as blocked-claim/status
discussion or explicit denial under the current `claim_ready=false`
conditional diagnostic ceiling.
