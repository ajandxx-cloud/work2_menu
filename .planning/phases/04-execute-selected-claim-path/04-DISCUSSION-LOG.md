# Phase 4: Execute Selected Claim Path - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or
> execution agents. Decisions are captured in CONTEXT.md; this log preserves
> the alternatives considered.

**Date:** 2026-06-17T17:25:47.8071034+08:00
**Phase:** 4-Execute Selected Claim Path
**Areas discussed:** Path Routing, Gate Cleanup Authorization, Final Artifact
And Mirror Strategy, Diagnostic Lock Strength

---

## Path Routing

| Decision | Selected Option | Alternatives Considered |
| --- | --- | --- |
| Default route | Try Path A first: strict gate cleanup/readiness, final replay only after all gates pass, otherwise Path B. | Direct Path B; assess only. |
| Cleanup attempt depth | One strict gate pass only; blockers after that pass trigger Path B. | Limited remediation loop; decide per blocker. |
| Technical replay failure | Allow one same-settings technical rerun. | No rerun; pause for user confirmation. |
| Completed replay with `claim_ready=false` | Strictly switch to Path B; no tuning, scale reduction, or additional replay. | Preserve local claims separately; pause for human interpretation. |

**User's choice:** Recommended option for all Path Routing questions.
**Notes:** Phase 4 remains gate-bound. Evidence failure is not treated as a
technical failure.

---

## Gate Cleanup Authorization

| Decision | Selected Option | Alternatives Considered |
| --- | --- | --- |
| Freeze/protocol records | Create current pre-run/non-tuning records from current manifests and filesystem state. | Only report missing records; write drafts and wait. |
| Checkpoint provenance | Use existing checkpoint only; allow sidecar, hash, dependency snapshot, load-status, and readiness metadata. | Retrain checkpoint; do not touch checkpoint evidence chain. |
| Formal readiness | Execute the formal readiness command once. | Run tests only; list commands and wait. |
| Replay/artifact authorization | Chained authorization after all gates pass. | Pause before replay; stop at readiness report. |

**User's choice:** Recommended option for all Gate Cleanup Authorization
questions.
**Notes:** Phase 4 may write necessary gate evidence, but must not retrain the
checkpoint or change result-affecting knobs.

---

## Final Artifact And Mirror Strategy

| Decision | Selected Option | Alternatives Considered |
| --- | --- | --- |
| Final evidence directory | Use an explicit `final_rc` directory marked by timestamp and/or manifest hash. | Reuse main artifact root; keep both. |
| Root mirror | Update root `artifacts/` only after package pass, as paper-facing copy with SHA/drift check. | Do not update mirror; always sync mirror. |
| Missing package entries | Never hand-fill placeholders or hand-edit package/status/claim guard outputs. | Allow document scaffold fills; allow non-result metadata fills. |
| Phase 5 handoff detail | Provide complete traceability for every usable and unusable claim. | List only usable claims; provide only claim guard path. |

**User's choice:** Recommended option for all Final Artifact And Mirror Strategy
questions.
**Notes:** Canonical evidence remains under `work2_coding/artifacts/...`.

---

## Diagnostic Lock Strength

| Decision | Selected Option | Alternatives Considered |
| --- | --- | --- |
| Path B deliverable strength | Full lock package: diagnostic lock, safe claim table, and reviewer risk response plan. | Minimal lock; failure report only. |
| Diagnostic manuscript narrative | Claim-gated diagnostic service-menu optimization. | Conditional regime-specific manuscript; methods-and-audit manuscript. |
| Reviewer risk priority | Evidence boundary and honest claims. | Method novelty/model reasonableness; reproducibility/engineering credibility. |
| Language handoff | Include prohibited/allowed wording list for Phase 5. | Only cite existing docs; let Phase 5 handle wording. |

**User's choice:** Recommended option for all Diagnostic Lock Strength
questions.
**Notes:** The Path B output should be immediately useful for Phase 5
diagnostic manuscript drafting.

---

## The Agent's Discretion

None. The user selected explicit decisions for all discussed areas.

## Deferred Ideas

None. Discussion stayed within Phase 4 scope.
