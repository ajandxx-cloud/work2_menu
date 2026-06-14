# Phase 4: Mainline Artifact Pipeline And Claim Guard - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-14
**Phase:** 4-Mainline Artifact Pipeline And Claim Guard
**Areas discussed:** Artifact output scope, Claim-ready gates, Recommended ranking scope

---

## Artifact Output Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Full bundle plus manuscript frame | Generate aggregates, LaTeX tables, figures/status sidecars, `ARTIFACT_STATUS.json`, README, metadata sidecars, manuscript frame, and claim guard. | Yes |
| Artifact bundle only | Generate artifact/status/aggregate/table/figure outputs, but not manuscript frame. | |
| Gate/status only | Generate only gate and status artifacts. | |

**User's choice:** `1A`
**Notes:** Phase 4 should produce the full generated artifact bundle and manuscript-frame claim guard, while still avoiding manuscript source edits and hand-edited result rows.

---

## Claim-Ready Gates

| Option | Description | Selected |
|--------|-------------|----------|
| Smoke diagnostic, pilot eligible, formal strict | Smoke is diagnostic/status only; pilot may be claim-ready; formal requires dependency snapshot and loaded checkpoint provenance. | Yes |
| Formal only | Pilot remains diagnostic; only formal may become claim-ready. | |
| Any tier eligible | Smoke, pilot, and formal may all be claim-ready if row and checkpoint gates pass. | |

**User's choice:** `2A`
**Notes:** Formal evidence must be stricter than pilot evidence. Formal claim-ready artifacts require dependency snapshot and loaded checkpoint provenance.

---

## Recommended Ranking Scope

| Option | Description | Selected |
|--------|-------------|----------|
| All seven mainline tags | Include every mainline tag in recommended-policy ranking. | |
| Operational strategies except no-menu | Include fixed, random, and optimized mainline strategies; keep no-menu in baseline/boundary reporting. | Yes |
| Optimized only | Include only optimized policies in ranking; keep no-menu, fixed, and random as baselines. | |

**User's choice:** `3B`
**Notes:** `mainline_no_menu` should be reported as a baseline/boundary row, not a recommended policy. Fixed, random, and optimized mainline strategies remain ranking-eligible when row and provenance gates pass.

---

## the agent's Discretion

- The agent may choose exact artifact filenames and helper boundaries as long as outputs are generated, provenance-driven, and test-covered.
- The agent may decide whether to integrate manuscript-frame generation into `build_artifacts.py` or keep it as a separate tested CLI, provided the Phase 4 bundle can be produced reliably.

## Deferred Ideas

- Formal replay and checkpoint training.
- Manuscript source edits.
- Attention-based V2 or diagnostic artifacts.
