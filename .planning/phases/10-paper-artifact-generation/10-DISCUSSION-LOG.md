# Phase 10: Paper Artifact Generation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-16T11:43:00+08:00
**Phase:** 10-paper-artifact-generation
**Areas discussed:** Evidence sources, artifact package structure, claim guard strictness, manuscript frame depth

---

## Evidence Sources

| Option | Description | Selected |
|--------|-------------|----------|
| Full inclusion with tiers | Include main RC, Phase 8, Phase 9, and case scaffold, with claim-ready/diagnostic/scaffold tiers to prevent overclaiming. | yes |
| Only usable results | Include only artifacts backed by rows; omit case scaffold from the paper artifact package. | |
| Minimal mainline | Include only main RC and required artifact/claim gates; leave Phase 8/9 to later appendix work. | |

**User's choice:** Full inclusion with tiers.
**Notes:** Case scaffold is included only as scaffold/no-result evidence, not as case validation.

---

## Artifact Package Structure

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal main package plus diagnostic appendix | Generate a focused main-paper package and a separate diagnostic appendix package for Phase 8/9/blocker material. | yes |
| One unified large package | Put all artifacts in one bundle and distinguish tiers only through metadata. | |
| Minimal main package only | Generate only roadmap-required main tables/figures and do not integrate Phase 8/9 diagnostic artifacts. | |

**User's choice:** Minimal main package plus diagnostic appendix.
**Notes:** Diagnostic appendix should include Phase 8 sensitivity, Phase 9 tractability, blocked/gate notes, and case scaffold placeholders.

---

## Claim Guard Strictness

| Option | Description | Selected |
|--------|-------------|----------|
| Strict per-claim mapping | Each claim records support status, source artifacts, blockers, safe language, forbidden language, manuscript permission, and claim readiness. | yes |
| Medium strictness | Each claim records support status and source artifacts; safe/forbidden language goes to a Markdown checklist. | |
| Overall gate only | `CLAIM_GUARD.json` only reports overall readiness and blocked claims; details wait for Phase 11. | |

**User's choice:** Strict per-claim mapping.
**Notes:** Overall `claim_ready` remains false unless all gates explicitly pass; current planning assumes false.

---

## Manuscript Frame Depth

| Option | Description | Selected |
|--------|-------------|----------|
| Artifact-facing frame only | Generate result/method/experiment outlines, artifact-to-section map, source index, and claim checklist; no body paragraphs. | yes |
| Section skeleton | Generate Phase 11-ready section skeleton with table/figure references but no conclusions. | |
| Safe draft snippets | Generate conservative manuscript-ready sentences while avoiding strong claims. | |

**User's choice:** Artifact-facing frame only.
**Notes:** Phase 10 should not write manuscript body text, abstract/conclusion upgrades, or polished claim prose.

---

## The Agent's Discretion

- The planner may choose exact file names and directory layout for the main and diagnostic appendix packages.
- The planner may decide whether to extend existing builders or add a Phase 10 orchestration helper.
- The planner may choose exact claim IDs and section labels, as long as strict claim mapping is enforced.

## Deferred Ideas

- Gate cleanup, final formal replay, case execution, and Phase 11 manuscript writing remain deferred.
