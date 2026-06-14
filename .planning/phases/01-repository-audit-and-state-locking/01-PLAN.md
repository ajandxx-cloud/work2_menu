---
phase: 1
phase_name: Repository Audit And State Locking
plan: 1
type: audit
status: ready
wave: 1
depends_on: []
files_modified:
  - .planning/STATE_LOCK.md
autonomous: true
requirements_addressed:
  - STATE-01
  - STATE-02
  - STATE-03
requirements:
  - STATE-01
  - STATE-02
  - STATE-03
must_haves:
  truths:
    - "D-01: .planning/STATE_LOCK.md records a complete state lock, including runtime root, import smoke result, dirty git summary, manifest inventory, test/script inventory, checkpoint/readiness/artifact status, stale planning references, and current blockers."
    - "D-02: .planning/STATE_LOCK.md uses ISO-8601 timestamps with explicit timezone, defaulting planning timestamps to Beijing time unless a source artifact states UTC."
    - "D-03: Dirty worktree paths are categorized as audit evidence only; no unrelated files are staged, reverted, deleted, or cleaned."
    - "D-04: The state lock contains a practical ooh_code to work2_coding mapping for roadmap-relevant stale references, with obsolete references marked explicitly."
    - "D-05: Stale .planning/codebase claims are checked against the current filesystem before being repeated, including the old missing-DSPO_Menu concern."
    - "D-06: The plan preserves work2_coding as the active runtime root and does not create or revive a parallel ooh_code runtime."
    - "D-07: Blockers are separated from warnings, with formal checkpoint, readiness, artifact, row-status, and dirty-git formal-readiness risks classified explicitly."
    - "D-08: Warnings include stale planning references, uncommitted manuscript/build artifacts, local-output provenance gaps, diagnostic no-filter evidence, and v2 attention artifacts."
    - "D-09: Opt-out accounting, paired replay fairness, checkpoint load status, artifact readiness, and claim guard state are named audit dimensions."
    - "D-10: Verification includes the lightweight work2_coding import smoke and avoids formal replay, checkpoint training, heavy studies, artifact regeneration, and manuscript claim upgrades."
    - "D-11: Focused script-style tests are inventoried, and any optional test execution is recorded as diagnostic rather than formal evidence."
    - "D-12: Phase 1 produces no algorithm behavior changes and no generated result-row or paper-artifact edits."
  artifacts:
    - .planning/STATE_LOCK.md
  key_links:
    - .planning/PROJECT.md
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - .planning/STATE.md
    - .planning/research/SUMMARY.md
    - .planning/phases/01-repository-audit-and-state-locking/01-CONTEXT.md
---

# Phase 1 Plan: Repository Audit And State Locking

<objective>
Create a durable repository state lock before any algorithm behavior changes.
The lock must confirm `work2_coding/` as the active runtime root, inventory the
current robust-menu experiment surface, classify evidence blockers and warnings,
translate stale `ooh_code/` planning references into current `work2_coding/`
paths where possible, and write `.planning/STATE_LOCK.md`.
</objective>

<scope>
## In Scope

- Run lightweight diagnostic commands and file-existence checks.
- Read project planning files, active manifests, scripts, and existing JSON
  evidence artifacts.
- Summarize the current dirty worktree without modifying unrelated changes.
- Write `.planning/STATE_LOCK.md`.

## Out Of Scope

- Algorithm behavior edits.
- Formal replay or heavy HGS study execution.
- Shared checkpoint training.
- Artifact regeneration or generated row edits.
- Manuscript claim upgrades.
- Git cleanup, revert, reset, deletion, or broad formatting.
</scope>

<tasks>
## Task 1: Establish Audit Baseline

**Type:** audit
**Files:** `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`,
`.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/research/SUMMARY.md`,
`.planning/phases/01-repository-audit-and-state-locking/01-CONTEXT.md`

**Action:**

1. Record an ISO-8601 Beijing-time audit timestamp.
2. Read the planning files listed above and extract Phase 1 success criteria,
   requirements, guardrails, and context decisions.
3. Run `git status --short` and categorize changed paths into planning,
   runtime, manuscript/paper, outputs/artifacts, and other notes.
4. Treat all dirty paths as audit evidence; do not stage or modify them.

**Verify:**

- The audit notes identify Phase 1 requirements `STATE-01`, `STATE-02`, and
  `STATE-03`.
- The dirty-worktree summary includes a total count and category examples.
- No file outside `.planning/STATE_LOCK.md` is intentionally modified.

**Acceptance Criteria:**

- Baseline evidence is ready to be included in `.planning/STATE_LOCK.md`.
- The audit boundary is explicit: diagnostic only, no behavior changes.

## Task 2: Verify Active Runtime Root And Core Files

**Type:** audit
**Files:** `work2_coding/Src/config.py`,
`work2_coding/Src/Algorithms/DSPO_Menu.py`,
`work2_coding/Src/paired_replay.py`,
`work2_coding/Src/policy_adapters.py`,
`work2_coding/Src/study_execution.py`,
`work2_coding/Src/formal_readiness.py`,
`work2_coding/Src/artifact_builder.py`,
`work2_coding/Src/artifact_status.py`,
`work2_coding/Src/manuscript_claims.py`

**Action:**

1. From `work2_coding/`, run:

   ```powershell
   python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
   ```

2. Verify the core runtime files above exist.
3. Record file presence and the import-smoke command/result in
   `.planning/STATE_LOCK.md`.
4. Note that `work2_coding/Src/Algorithms/DSPO_Menu.py` makes the old
   `ooh_code` missing-module concern stale for the active runtime.

**Verify:**

- Import smoke returns `IMPORT_OK`.
- `work2_coding/` is recorded as the active runtime root.
- No `ooh_code/` runtime root is created or revived.

**Acceptance Criteria:**

- Requirement `STATE-01` is satisfied by a recorded command, result, timestamp,
  and path evidence.

## Task 3: Inventory Manifests, Policy Family, Scripts, And Tests

**Type:** audit
**Files:** `work2_coding/Experiments/studies/*.yaml`,
`work2_coding/scripts/*.py`, `work2_coding/Src/policy_adapters.py`

**Action:**

1. List robust-menu manifests, especially `smoke_robust_menu.yaml`,
   `pilot_robust_menu.yaml`, and `formal_robust_menu.yaml`.
2. Confirm the seven-tag mainline family appears in both the robust manifests
   and `work2_coding/Src/policy_adapters.py`.
3. Inventory script-style tests relevant to opt-out accounting, menu runtime
   contracts, paired replay, policy fairness, artifact gates, formal readiness,
   checkpoint provenance, smoke rows, and study execution status.
4. Inventory key execution/build scripts without running heavy workflows:
   `train_shared_checkpoint.py`, `check_formal_readiness.py`, `run_study.py`,
   `build_artifacts.py`, and `build_manuscript_frame.py`.

**Verify:**

- The state lock names all seven mainline tags.
- Tests are listed as available, missing, or out-of-scope, without pretending
  inventory equals proof.
- Attention manifests/tests are marked diagnostic or v2 unless later phases
  upgrade their scope.

**Acceptance Criteria:**

- Requirement `STATE-02` has concrete manifest, script, and test inventories.

## Task 4: Inventory Checkpoint, Readiness, Artifact, And Claim-Guard Status

**Type:** audit
**Files:** `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`,
`work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`,
`work2_coding/outputs/phase4_artifacts/ARTIFACT_STATUS.json`,
`work2_coding/outputs/phase4_artifacts/manuscript/CLAIM_GUARD.json`

**Action:**

1. Check whether the formal shared checkpoint path exists.
2. Read existing readiness, artifact-status, and claim-guard JSON files when
   present.
3. Record the status fields without upgrading claims. Current known values to
   verify are `FORMAL_READINESS.json` status `blocked`,
   `ARTIFACT_STATUS.json` `claim_ready: False`, and `CLAIM_GUARD.json`
   `claim_ready: False`.
4. Classify missing or blocked evidence as blockers for later formal claims,
   not as Phase 1 execution failures unless the state lock cannot be written.

**Verify:**

- The lock separates checkpoint existence from checkpoint load success.
- Readiness and claim-guard status are explicit.
- No formal study, checkpoint training, or artifact builder is launched.

**Acceptance Criteria:**

- Formal evidence status is recorded honestly and remains non-claim-ready when
  gates do not pass.

## Task 5: Map Stale `ooh_code/` References

**Type:** audit
**Files:** `.planning/codebase/STRUCTURE.md`,
`.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/CONCERNS.md`,
`.planning/codebase/TESTING.md`, `.planning/codebase/CONVENTIONS.md`,
`.planning/codebase/INTEGRATIONS.md`, `.planning/codebase/STACK.md`

**Action:**

1. Extract roadmap-relevant stale `ooh_code/` references from the existing
   codebase maps.
2. For each important claim, either map it to a current `work2_coding/` path or
   mark it obsolete.
3. Highlight stale claims that must not be repeated as current facts, including
   the old missing `DSPO_Menu.py` concern.
4. Preserve useful historical warnings as categories for future audits, but
   tie every current-state claim to actual `work2_coding/` evidence.

**Verify:**

- The state lock has an `ooh_code -> work2_coding` mapping section.
- Obsolete references are explicitly named.
- Requirement `STATE-03` is covered.

**Acceptance Criteria:**

- Future phases can safely read `.planning/codebase/` maps with clear knowledge
  of which path references are stale.

## Task 6: Write And Self-Check `.planning/STATE_LOCK.md`

**Type:** docs
**Files:** `.planning/STATE_LOCK.md`

**Action:**

1. Write `.planning/STATE_LOCK.md` with sections for:
   - audit metadata and timestamp
   - active runtime root and import smoke
   - dirty worktree summary
   - manifests and seven-tag policy family
   - scripts and script-style tests
   - key runtime modules
   - checkpoint/readiness/artifact/claim-guard status
   - stale planning-reference mapping
   - blockers and warnings
   - allowed next steps and prohibited actions
2. Use explicit path evidence and command outputs for each major claim.
3. Mark formal empirical claims as not yet supported when gates are blocked or
   `claim_ready` is false.

**Verify:**

1. Rerun the import smoke:

   ```powershell
   cd work2_coding
   python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
   ```

2. Confirm `.planning/STATE_LOCK.md` exists and covers `STATE-01`,
   `STATE-02`, and `STATE-03`.
3. Confirm no generated result rows or paper artifacts were hand-edited.

**Acceptance Criteria:**

- `.planning/STATE_LOCK.md` exists and is sufficient for later phases to know
  the current runtime, evidence, blockers, and stale-map status.
- Phase 1 can be summarized as complete without changing algorithm behavior.
</tasks>

<verification>
## Required Verification

Run from the repository root:

```powershell
cd work2_coding
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
```

Expected output:

```text
IMPORT_OK
```

Then inspect `.planning/STATE_LOCK.md` for the following coverage:

- `STATE-01`: runtime root and import smoke are recorded.
- `STATE-02`: manifests, tests, scripts, artifacts, checkpoints, readiness,
  claim guard, and blockers are inventoried.
- `STATE-03`: stale `ooh_code/` planning references are mapped to
  `work2_coding/` paths or marked obsolete.

No formal replay, checkpoint training, artifact regeneration, or manuscript
claim upgrade is part of verification for this phase.
</verification>

<success_criteria>
- Import smoke passes from `work2_coding/`.
- `work2_coding/` is confirmed as active runtime root.
- Current Work2 objective is recorded as TR-E service-menu optimization, not old
  Akkerman reproduction and not an old TR-C DSPO_PLUS ladder.
- Seven-tag mainline family is confirmed from manifests and adapters.
- Formal replay/checkpoint/readiness/artifact/claim-guard status is verified
  from actual files.
- Available tests for service-product contracts, menu adapters, paired replay,
  artifact gates, formal readiness, and study execution are inventoried.
- `.planning/STATE_LOCK.md` is written.
</success_criteria>
