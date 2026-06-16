# Phase 2: Gate Cleanup Plan Without Destructive Changes - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-16T22:11:39+08:00
**Phase:** 2-Gate Cleanup Plan Without Destructive Changes
**Areas discussed:** Dirty git accounting, Checkpoint provenance contract, Blocker cleanup mapping scope, Non-destructive boundary and forbidden commands

---

## Dirty Git Accounting

### Dirty state treatment

| Option | Description | Selected |
|--------|-------------|----------|
| Classify plus approval list | Record dirty categories and route restore/delete/stash/revert/overwrite-style actions to `M2_USER_ACTIONS_REQUIRED.md`. | Yes |
| Classify only | Record provenance risk in the cleanup plan without a separate user action list. | |
| Summary only | Record counts and representative paths only. | |

**User's choice:** Classify plus approval list.
**Notes:** Phase 2 must not execute worktree-changing actions.

### Dirty classification detail

| Option | Description | Selected |
|--------|-------------|----------|
| Group by risk category | Use representative paths, risk, and approval requirement by category. | Yes |
| List every path | Produce a full table of all changed paths. | |
| Counts plus examples | Keep the document short, with counts and key examples only. | |

**User's choice:** Group by risk category.
**Notes:** This balances traceability with readability.

### Approval list boundary

| Option | Description | Selected |
|--------|-------------|----------|
| All worktree/evidence changes | Require approval for git operations, legacy restoration/deletion, artifact rebuilds, mirror replacement, checkpoint training, and formal/final replay. | Yes |
| Only git operations | Require approval only for restore/stash/revert/delete style actions. | |
| Only irreversible actions | Allow new generated outputs but block deletion or overwrite. | |

**User's choice:** All worktree/evidence changes.
**Notes:** Approval is required for any action that changes the worktree or evidence chain.

### Deleted legacy files

| Option | Description | Selected |
|--------|-------------|----------|
| Provenance risk, do not auto-restore | Record as a provenance risk but do not restore or mine history unless needed. | |
| Recommend restoring for reference | Put restoration in the recommended user actions. | |
| Treat as superseded | Treat deleted legacy planning/results as replaced by regenerated planning unless a specific blocker depends on them. | Yes |

**User's choice:** Treat as superseded.
**Notes:** Do not restore or deeply inspect legacy deleted files by default.

---

## Checkpoint Provenance Contract

### Minimum provenance fields

| Option | Description | Selected |
|--------|-------------|----------|
| Four checkpoint fields plus readiness evidence | Require path, hash, sidecar, load status, dependency snapshot, manifest hash, git SHA/dirty state, and readiness JSON path/hash. | Yes |
| Only roadmap four fields | Require only checkpoint path, hash, sidecar metadata, and load status. | |
| Full field extraction from current code | Extract every related field from current gate modules. | |

**User's choice:** Four checkpoint fields plus readiness evidence.
**Notes:** This reflects both roadmap requirements and current readiness/artifact gate behavior.

### Checkpoint failure representation

| Option | Description | Selected |
|--------|-------------|----------|
| Separate fail-closed blockers | Represent missing checkpoint, missing sidecar, load failure, and hash mismatch as separate blocker codes. | Yes |
| Single combined checkpoint blocker | Use one broad incomplete-checkpoint blocker. | |
| Fatal/warning split | Treat some issues as fatal and others as warnings. | |

**User's choice:** Separate fail-closed blockers.
**Notes:** Every checkpoint provenance failure blocks claim-ready interpretation.

### Sidecar and hash authority

| Option | Description | Selected |
|--------|-------------|----------|
| File hash is authoritative, sidecar is evidence | Recompute checkpoint SHA-256 and require sidecar to match or explain it. | Yes |
| Sidecar hash is authoritative | Trust the sidecar's recorded checkpoint hash. | |
| Any hash is sufficient | Accept either file hash or sidecar hash. | |

**User's choice:** File hash is authoritative, sidecar is evidence.
**Notes:** Sidecar metadata cannot replace hashing the actual checkpoint file.

### Smoke-load and readiness execution

| Option | Description | Selected |
|--------|-------------|----------|
| Do not execute, record command templates only | Phase 2 records later commands and expected fields but does not smoke-load or write readiness outputs. | Yes |
| Allow read-only smoke-load | Permit smoke-load if outputs go to a temporary location. | |
| Allow generating readiness output | Run `check_formal_readiness.py` and create new readiness files in Phase 2. | |

**User's choice:** Do not execute, record command templates only.
**Notes:** Phase 2 is planning only for checkpoint readiness.

---

## Blocker Cleanup Mapping Scope

### Blocker coverage

| Option | Description | Selected |
|--------|-------------|----------|
| Prioritize Phase 3 go/no-go blockers | Understand all blockers, but prioritize provenance/readiness, checkpoint, dirty git, formal readiness, and artifact packaging. | Yes |
| Only cover the 4 missing artifact entries | Focus on package completeness only. | |
| Cover all 108 blockers | Produce a complete blocker-action matrix. | |

**User's choice:** Prioritize Phase 3 go/no-go blockers.
**Notes:** Non-Phase 2 blockers are recorded but not repaired here.

### Missing artifact entries

| Option | Description | Selected |
|--------|-------------|----------|
| Locate cause only; do not fill files | Identify source directories and expected patterns without creating files or running builders. | Yes |
| Recommend filling scaffold files | Suggest adding the missing case scaffold `.yml`/`.json` files. | |
| Recommend rerunning package/artifact builders | Use generated flows to repair missing entries. | |

**User's choice:** Locate cause only; do not fill files.
**Notes:** User asked what the missing entries mean. They are generated `missing.*` placeholder paths from unmatched patterns in `.planning/data/case_studies/` and `work2_coding/artifacts/work2_robust_menu/figures/`.

### Matrix shape

| Option | Description | Selected |
|--------|-------------|----------|
| Blocker -> Action -> Approval -> Verification | Include blocker/source, recommended action, approval requirement, what Phase 2 will not do, and verification. | Yes |
| Blocker -> Action only | Keep the matrix shorter. | |
| Segment only by deliverable | Avoid a single matrix and split content by output document. | |

**User's choice:** Blocker -> Action -> Approval -> Verification.
**Notes:** This should reduce downstream ambiguity.

### Non-Phase 2 blockers

| Option | Description | Selected |
|--------|-------------|----------|
| Mark Not Phase 2 and route later | Record empirical, tractability, and case-validation blockers but defer them to Phase 3/4+. | Yes |
| Put all into long-term cleanup backlog | Include rough future suggestions. | |
| Do not mention them | Keep Phase 2 purely provenance/readiness-focused. | |

**User's choice:** Mark Not Phase 2 and route later.
**Notes:** Phase 2 should avoid expanding into empirical repair.

---

## Non-Destructive Boundary And Forbidden Commands

### Allowed command boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Read-only checks plus planning document writes | Allow inspection and Phase 2 docs only; no evidence/readiness/artifact/checkpoint generation. | Yes |
| Allow diagnostic output generation | Allow readiness/package/artifact commands to temporary outputs. | |
| Allow non-final builders | Allow artifact/package builders but prohibit final replay. | |

**User's choice:** Read-only checks plus planning document writes.
**Notes:** Phase 2 remains non-destructive and non-generative.

### Forbidden-without-approval command list

| Option | Description | Selected |
|--------|-------------|----------|
| Full forbidden command list | Include replay, checkpoint training, formal readiness, artifact builders, package builders, case execution, git restore/stash/revert/delete, and mirror replacement. | Yes |
| Only evidence-generation commands | Omit git operations from the command list. | |
| Principle only, no command list | State the rule without enumerating commands. | |

**User's choice:** Full forbidden command list.
**Notes:** Specific command names should be written to avoid later ambiguity.

### Command templates

| Option | Description | Selected |
|--------|-------------|----------|
| Allow templates with approval-before-execution labels | Include later command templates only in approval-required/not-executed sections. | Yes |
| Do not write command templates | Avoid commands to prevent accidental execution. | |
| Only write read-only command templates | Include inspection commands only. | |

**User's choice:** Allow templates with approval-before-execution labels.
**Notes:** Templates are allowed, execution is not.

### Verification baseline

| Option | Description | Selected |
|--------|-------------|----------|
| Document consistency plus smoke import | Verify deliverables, blocker-action mappings, non-execution of approval-required actions, and import smoke. | Yes |
| Only verify documents exist | Check file existence only. | |
| Run readiness/artifact tests | Run formal readiness, checkpoint provenance, and artifact gate tests. | |

**User's choice:** Document consistency plus smoke import.
**Notes:** Do not run readiness/artifact generation tests as Phase 2 verification.

---

## The Agent's Discretion

- Choose exact table formatting and grouping names for the Phase 2 planning
  documents.
- Add concise source-code observations from current gate modules while staying
  within the non-destructive planning boundary.

## Deferred Ideas

None.
