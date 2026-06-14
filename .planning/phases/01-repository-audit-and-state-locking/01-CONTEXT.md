# Phase 1: Repository Audit And State Locking - Context

**Gathered:** 2026-06-14T22:54:31+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 1 delivers a repository audit and state lock before any algorithm behavior
changes. It confirms the active runtime root, inventories current manifests,
tests, scripts, outputs, checkpoint/readiness/artifact status, maps stale
`ooh_code/` planning references to the current filesystem, and writes
`.planning/STATE_LOCK.md`.

This phase is diagnostic and documentary. It must not repair algorithm behavior,
rerun formal evidence, edit generated rows, revert dirty files, or upgrade
paper claims.

</domain>

<decisions>
## Implementation Decisions

### STATE_LOCK Scope
- **D-01:** Use a complete state lock, not a minimal smoke note. The planned
  `.planning/STATE_LOCK.md` must include active runtime root, import-smoke
  result, git dirty-state summary, manifest inventory, test/script inventory,
  key output/artifact/checkpoint presence, formal readiness/claim-gate pointers,
  stale planning references, and current blockers.
- **D-02:** Record timestamps as ISO-8601 with timezone. Planning timestamps
  default to Beijing time unless a generated run artifact explicitly reports
  UTC.
- **D-03:** Treat the current dirty worktree as audit input, not as something
  Phase 1 may clean up. The plan may require listing modified/deleted/untracked
  paths by category, but must not stage, revert, delete, or rewrite unrelated
  user changes.

### Stale `ooh_code/` Reference Handling
- **D-04:** Phase 1 must produce a practical `ooh_code/` to `work2_coding/`
  mapping section. For each stale map claim that matters to the current roadmap,
  either identify the current `work2_coding/` path or mark the old reference
  obsolete.
- **D-05:** The old `.planning/codebase/` maps are useful as historical memory
  only. They must not override the current filesystem. In particular, the old
  concern that `ooh_code/Src/Algorithms/DSPO_Menu.py` was missing is stale for
  the active runtime because `work2_coding/Src/Algorithms/DSPO_Menu.py` exists
  and `import Src.config` passed from `work2_coding/`.
- **D-06:** Do not create or revive a parallel `ooh_code/` runtime root. Any
  future planning should prefer `work2_coding/` unless Phase 1 finds explicit,
  documented evidence that a different root is required.

### Blocker Classification
- **D-07:** Classify blockers separately from warnings. Blockers include failed
  import smoke, missing active runtime files, missing required formal checkpoint
  for formal/pilot evidence, failed formal readiness, claim-ready artifact gate
  failure, placeholder-only formal artifacts, row status failures for formal
  runs, and unresolved dirty-git state when a later formal-readiness command
  requires a clean tree.
- **D-08:** Warnings include stale `ooh_code/` references, uncommitted manuscript
  or build artifacts, local outputs that need provenance review, diagnostic
  no-filter evidence, and optional attention artifacts that remain outside v1
  scope.
- **D-09:** Keep opt-out accounting, paired replay fairness, checkpoint load
  status, artifact readiness, and claim guard state as named audit dimensions.
  These are not generic quality notes; they are scientific guardrails for the
  paper.

### Verification Command Boundary
- **D-10:** Phase 1 may run only lightweight, diagnostic, script-style checks.
  Recommended baseline: from `work2_coding/`, run
  `python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"`.
- **D-11:** Phase 1 may identify focused test scripts for later or optionally
  run cheap contract tests when planning/execution judges them safe, such as
  `scripts/test_optout_accounting.py`, `scripts/test_paired_replay_contract.py`,
  `scripts/test_artifact_gates.py`, `scripts/test_formal_readiness.py`,
  `scripts/test_policy_fairness_contract.py`, and
  `scripts/test_study_execution_status.py`.
- **D-12:** Phase 1 must not run formal replay, checkpoint training, heavy HGS
  studies, artifact regeneration, or manuscript claim upgrades. Formal evidence
  execution belongs to later roadmap phases after the state lock is written.

### the agent's Discretion
- The planner may decide the exact internal structure of `.planning/STATE_LOCK.md`
  as long as all decisions above are represented and each audit claim is tied to
  a concrete file path, command output, or explicitly marked missing artifact.
- The planner may split Phase 1 into one or more plans, but the first plan must
  preserve the no-behavior-change audit boundary.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, active runtime root, paper framing,
  and research guardrails.
- `.planning/REQUIREMENTS.md` - Phase 1 requirements `STATE-01`, `STATE-02`,
  and `STATE-03`.
- `.planning/ROADMAP.md` - Phase 1 scope, success criteria, verification
  command, and global gate rules.
- `.planning/STATE.md` - Current GSD state, initialization evidence, dirty-tree
  caution, and verification baseline.
- `.planning/research/SUMMARY.md` - Research summary and scientific boundary
  for TR-E service-menu optimization.
- `AGENTS.md` - Repository-level instructions, runtime assumption, research
  guardrails, and verification baseline.

### Existing Codebase Maps
- `.planning/codebase/STRUCTURE.md` - Historical directory map; contains stale
  `ooh_code/` references that Phase 1 must verify against `work2_coding/`.
- `.planning/codebase/TESTING.md` - Historical test patterns and script-style
  test conventions; useful but stale where paths use `ooh_code/`.
- `.planning/codebase/CONCERNS.md` - Historical concerns and fragile areas;
  useful for audit categories, but each claim must be rechecked against the
  current filesystem.

### Active Runtime And Experiment Contracts
- `work2_coding/Src/config.py` - Import-smoke target and runtime configuration
  entry point.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Current active robust/menu
  algorithm module; verifies that the old missing-`DSPO_Menu.py` concern is
  stale for `work2_coding/`.
- `work2_coding/Src/paired_replay.py` - Paired replay row and fairness contract.
- `work2_coding/Src/policy_adapters.py` - Mainline policy family adapter.
- `work2_coding/Src/study_execution.py` - Study status and execution metadata.
- `work2_coding/Src/formal_readiness.py` - Formal readiness checks.
- `work2_coding/Src/artifact_builder.py` - Artifact generation and claim-ready
  gate behavior.
- `work2_coding/Src/artifact_status.py` - Artifact status classification.
- `work2_coding/Src/manuscript_claims.py` - Manuscript claim guard/frame logic.

### Mainline Manifests And Outputs
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml` - Smoke seven-tag
  mainline family and diagnostic checkpoint semantics.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` - Pilot seven-tag
  mainline family with shared checkpoint provenance.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Formal seven-tag
  mainline family, checkpoint requirements, paired fields, required metadata,
  and status fields.
- `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`
  - Current formal shared checkpoint path observed during discussion.
- `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
  - Current formal readiness artifact path observed during discussion.
- `work2_coding/outputs/phase4_artifacts/ARTIFACT_STATUS.json` - Current
  artifact status path observed during discussion.
- `work2_coding/outputs/phase4_artifacts/manuscript/CLAIM_GUARD.json` - Current
  manuscript claim guard path observed during discussion.

### Focused Test Scripts
- `work2_coding/scripts/test_optout_accounting.py` - Opt-out accounting contract.
- `work2_coding/scripts/test_paired_replay_contract.py` - Paired replay contract.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Policy-family
  fairness and paired settings.
- `work2_coding/scripts/test_artifact_gates.py` - Artifact gate behavior.
- `work2_coding/scripts/test_formal_readiness.py` - Formal readiness contract.
- `work2_coding/scripts/test_study_execution_status.py` - Study status and
  blocker row behavior.
- `work2_coding/scripts/test_checkpoint_provenance.py` - Checkpoint provenance
  contract.
- `work2_coding/scripts/test_smoke_study_rows.py` - Smoke row metadata contract.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/scripts/train_shared_checkpoint.py`: shared checkpoint training
  script; Phase 1 should inventory it but not run it.
- `work2_coding/scripts/check_formal_readiness.py`: formal readiness wrapper;
  Phase 1 may record its path and existing output status, but heavy readiness
  reruns should be planned carefully.
- `work2_coding/scripts/run_study.py`: study execution wrapper; Phase 1 should
  inventory it, not launch formal studies.
- `work2_coding/scripts/build_artifacts.py`: artifact builder wrapper; Phase 1
  should inventory current artifacts and gates, not regenerate paper outputs.
- `work2_coding/scripts/build_manuscript_frame.py`: manuscript frame builder;
  Phase 1 should record presence only.

### Established Patterns
- Tests are executable Python scripts under `work2_coding/scripts/test_*.py`,
  using direct `assert` and script-level `main()` functions rather than a
  repository-wide pytest configuration.
- Study contracts are YAML manifests under `work2_coding/Experiments/studies/`.
  The robust menu smoke, pilot, and formal manifests all enumerate the seven
  mainline policy tags.
- Generated outputs live under `work2_coding/outputs/`; committed or mirrored
  paper-facing artifacts have different trust levels and must not be treated as
  equivalent to raw formal run provenance without explicit metadata.

### Integration Points
- `.planning/STATE_LOCK.md` should connect planning state to runtime evidence:
  manifests, scripts, test scripts, outputs, checkpoint/readiness/artifact
  paths, and dirty git status.
- Future `gsd-plan-phase 1` should use this context to plan a read-only audit
  before any behavior-changing work.

</code_context>

<specifics>
## Specific Ideas

- User accepted all recommended decisions for Phase 1 discussion.
- The repository currently has a large dirty worktree. During the previous
  planning gate, `git status --short` showed many modified/deleted/untracked
  files; during this discussion the short-status count was 110. This must be
  audited, not cleaned automatically.
- `python -c "import sys; sys.path.insert(0, 'work2_coding'); import Src.config; print('IMPORT_OK')"`
  passed during discussion from the repository root.
- Observed current files include `work2_coding/Src/Algorithms/DSPO_Menu.py`,
  `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`,
  `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`,
  `work2_coding/outputs/phase4_artifacts/ARTIFACT_STATUS.json`, and
  `work2_coding/outputs/phase4_artifacts/manuscript/CLAIM_GUARD.json`.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within Phase 1 scope.

</deferred>

---

*Phase: 1-Repository Audit And State Locking*
*Context gathered: 2026-06-14T22:54:31+08:00*
