# Phase 1: Repository And Evidence Boundary Audit - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-16
**Phase:** 1-Repository And Evidence Boundary Audit
**Areas discussed:** Canonical Evidence Source, Blocker Taxonomy, Feasibility Wording, Deleted Legacy Planning State, Audit Command Boundary

---

## Canonical Evidence Source

| Option | Description | Selected |
|--------|-------------|----------|
| A | Treat `work2_coding/artifacts/...` as canonical and root `artifacts/...` as mirror drift check only. | Yes |
| B | Audit both locations equally; any difference becomes a blocker. | |
| C | Let the agent decide, as long as path authority is explicit. | |

**User's choice:** `1A`
**Notes:** The canonical generated package is under `work2_coding/artifacts/work2_robust_menu/phase10_paper_artifacts/`. Root `artifacts/` is a mirror for drift checks.

### Follow-up: Mirror Drift Scope

| Option | Description | Selected |
|--------|-------------|----------|
| A | Compare only key JSON files: `CLAIM_GUARD.json`, `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and `ARTIFACT_TO_SECTION_MAP.json`. | Yes |
| B | Compare size/hash for every file under the Phase 10 package. | |
| C | Record only existence and timestamp consistency. | |

**User's choice:** `1A`
**Notes:** Phase 1 should avoid exhaustive mirror hashing unless the four key JSON files show drift.

### Follow-up: Key JSON Recording

| Option | Description | Selected |
|--------|-------------|----------|
| A | Record only top-level fields and summary counts. | |
| B | Record top-level fields, `source_family_status`, blocked claim IDs, and each claim's `support_status`. | Yes |
| C | Copy full JSON contents into the audit document. | |

**User's choice:** `1B`
**Notes:** This keeps the audit traceable without bloating the milestone documents.

---

## Blocker Taxonomy

| Option | Description | Selected |
|--------|-------------|----------|
| A | Concise category summary by six blocker classes. | |
| B | Detailed matrix by claim ID, source family, artifact role, and blocker reason. | |
| C | Mixed format: six-class summary plus traceable matrix. | Yes |

**User's choice:** `2C`
**Notes:** The body of `M1_BLOCKER_LIST.md` should be readable, while the matrix preserves audit traceability.

### Follow-up: Matrix Scope

| Option | Description | Selected |
|--------|-------------|----------|
| A | Cover only the 8 claim guard claims. | |
| B | Cover the package's 74 artifacts plus the claim guard's 8 claims. | Yes |
| C | Cover only the 108 package blockers. | |

**User's choice:** `2B`
**Notes:** The matrix should bridge artifact package state and claim status.

### Follow-up: Classification Method

| Option | Description | Selected |
|--------|-------------|----------|
| A | Classify strictly by artifact/source family fields without interpretation. | |
| B | Use automatic classification plus short human explanation for each blocker class. | Yes |
| C | Classify only by claim ID, not the six-class taxonomy. | |

**User's choice:** `2B`
**Notes:** Human explanation is needed to make the taxonomy scientifically meaningful.

---

## Feasibility Wording

| Option | Description | Selected |
|--------|-------------|----------|
| A | Make only a preliminary current evidence boundary statement. | |
| B | Directly conclude that the paper can only be diagnostic. | |
| C | State that current evidence points diagnostic-only, while Phase 2/3 may still validate a legitimate final replay path. | Yes |

**User's choice:** `3C`
**Notes:** Phase 1 should not over-decide the final claim path, but it should be honest about the current package.

### Follow-up: Feasibility Phrase

| Option | Description | Selected |
|--------|-------------|----------|
| A | Current package is not claim-ready; diagnostic manuscript is the only currently authorized path. | |
| B | Claim-ready may be possible only after Phase 2/3 prove clean provenance and valid frozen final settings. | Yes |
| C | Include both statements, with current conclusion first and conditional path second. | |

**User's choice:** `3B`
**Notes:** The emphasis should stay on gated legitimacy rather than prematurely closing the path.

### Follow-up: Handoff

| Option | Description | Selected |
|--------|-------------|----------|
| A | Write only current audit results. | |
| B | Add a short handoff: Phase 2 checks provenance/readiness; Phase 3 checks final replay legitimacy. | Yes |
| C | Write a detailed action list equivalent to Phase 2/3 plans. | |

**User's choice:** `3B`
**Notes:** Handoff should be brief and not become Phase 2/3 planning.

### Follow-up: `M1_DECISION.md`

| Option | Description | Selected |
|--------|-------------|----------|
| A | Current evidence is not claim-ready; proceed diagnostic unless later gates pass. | |
| B | Do not decide yet; Phase 1 only reconstructs boundary. | |
| C | Recommend Phase 3 decide between legitimate final replay and diagnostic lock, with current package leaning diagnostic. | Yes |

**User's choice:** `3C`
**Notes:** This preserves the roadmap gate sequence.

---

## Deleted Legacy Planning State

| Option | Description | Selected |
|--------|-------------|----------|
| A | Mention deleted legacy files only as git-state boundary facts. | |
| B | Read git history to identify removed historical evidence. | |
| C | List deletion categories and impact; do not restore or deeply mine unless they affect Phase 1 evidence boundary. | Yes |

**User's choice:** `4C`
**Notes:** Current evidence should be based on present generated package files, while deletions remain a provenance risk.

### Follow-up: Impact Level

| Option | Description | Selected |
|--------|-------------|----------|
| A | Treat deleted old files as blockers because they may contain historical evidence. | |
| B | Treat deleted old files as provenance risk, not automatic blocker; present generated package is current evidence. | Yes |
| C | Exclude from Phase 1 and leave entirely for Phase 2 dirty git. | |

**User's choice:** `4B`
**Notes:** The dirty state matters, but Phase 1 should not restore old planning.

### Follow-up: `manuscript/main.tex`

| Option | Description | Selected |
|--------|-------------|----------|
| A | Record as dirty git fact only, no content review. | |
| B | Record as manuscript availability risk. | |
| C | Read git history to restore or inspect old manuscript content. | |
| User clarification | `manuscript/main.tex` has been restored. | Yes |

**User's choice:** `4 already restored`
**Notes:** Follow-up check confirmed `manuscript/main.tex` exists and is not currently shown as changed by `git status -- manuscript/main.tex manuscript`.

### Follow-up: Manuscript Check Depth

| Option | Description | Selected |
|--------|-------------|----------|
| A | Record only existence, size, and path. | |
| B | Read-only check for possibly overreaching claim wording; do not edit text. | Yes |
| C | Leave manuscript entirely to Phase 5. | |

**User's choice:** `1B`
**Notes:** Phase 1 may inspect claim-boundary wording but must not edit manuscript content.

---

## Audit Command Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| A | Allow only file existence, JSON summaries, git status, and import smoke. | |
| B | Allow read-only audit scripts/parsing commands, but no study execution, builder runs, or artifact regeneration. | Yes |
| C | Allow artifact builder runs to refresh status. | |

**User's choice:** `2B`
**Notes:** Phase 1 is read-only. It may parse and summarize current files, but it must not regenerate evidence.

---

## Agent Discretion

- The agent may choose exact table formatting and extraction helpers for the Phase 1 milestone documents.
- The agent may add concise read-only evidence facts discovered during inspection.

## Deferred Ideas

None.
