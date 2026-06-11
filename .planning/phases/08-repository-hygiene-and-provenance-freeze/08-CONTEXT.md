# Phase 08: Repository Hygiene And Provenance Freeze - Context

**Gathered:** 2026-06-11T21:48:50+08:00
**Status:** Ready for planning
**Mode:** Smart discuss; user accepted all recommended answers.
**Language:** Chinese discussion; downstream code, file paths, field names, and requirement IDs remain English.

<domain>
## Phase Boundary

Phase 08 reduces provenance risk before new empirical evidence runs. It classifies current dirty, untracked, ignored, generated, and local-output state; tightens ignore rules; documents what generated artifacts should be tracked versus kept local; and defines the cleanliness/provenance gate for Phase 09 and later evidence runs.

This phase does not train checkpoints, run pilot/formal evidence, edit generated result rows by hand, or decide the attention-improves-DSPO claim. It prepares the repository so later evidence can honestly report clean or narrowly documented dirty provenance.

</domain>

<decisions>
## Implementation Decisions

### Dirty And Untracked Classification
- **D-01:** Classify current dirty and untracked state first. Do not delete files during the audit unless a later explicit plan step proves the cleanup is safe and in scope.
- **D-02:** Classify `.planning/reports/MILESTONE_SUMMARY-v2.0.md` as a planning/generated report and document whether it should be tracked or kept local.
- **D-03:** Treat ignored `__pycache__`, raw `outputs/`, and runtime `Experiments/` directories as local/generated state, not evidence artifacts.
- **D-04:** If deleted user documents or user-facing notes are found, document them before any restore/remove decision. Do not automatically restore or remove them.

### `.gitignore` Policy
- **D-05:** Add or update a root `.gitignore` for repository-level hygiene, while preserving `work2_coding/.gitignore` for runtime-local ignores.
- **D-06:** Ignore Python caches, virtual environments, temporary files, local raw outputs, and LaTeX build byproducts.
- **D-07:** Do not ignore committed artifact bundles intended for review. Review-facing status/snapshot/table/figure artifacts must remain trackable.
- **D-08:** Add comments that distinguish raw local outputs from trackable artifact snapshots so future evidence is not accidentally hidden.

### Generated Artifact Tracking Policy
- **D-09:** Record generated-artifact policy in Phase 08 docs and include a concise artifact policy note where useful.
- **D-10:** Keep raw outputs local/ignored unless a formal archive process is explicitly created later.
- **D-11:** Track only lightweight status, snapshot, table, figure, and manuscript-support bundles intended for review.
- **D-12:** Keep checkpoint files local/ignored by default, but require sidecars and hashes for evidence-stage use.

### Provenance Gate For Future Evidence
- **D-13:** Phase 09 and later evidence runs should aim for `git_dirty=false`. If `git_dirty=true`, it must be narrowly documented and limited to known local-output exceptions.
- **D-14:** Classify and resolve the current untracked `.planning/reports/` state before evidence runs.
- **D-15:** Phase 08 should run an import check plus relevant provenance/artifact contract tests, not the entire empirical suite.
- **D-16:** Phase 09 may proceed only after dirty files are classified and ignore policy is updated.

### Claim Honesty
- **D-17:** Later evidence phases must not compromise if results fail to support the desired attention-improves-DSPO conclusion. If pilot or formal evidence does not support the claim, artifacts, claim guards, validation, and summaries must mark the claim as failed or blocked rather than softening unsupported results into positive language.

### the agent's Discretion
- The agent may choose exact hygiene report filenames and `.gitignore` pattern grouping.
- The agent may decide whether `.planning/reports/MILESTONE_SUMMARY-v2.0.md` should be tracked or documented as local, provided the classification is explicit.
- The agent may choose the smallest relevant verification command set that proves ignore policy and provenance classification without running expensive empirical studies.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `git status --short --ignored` already reveals the current provenance surface: one untracked `.planning/reports/` directory plus ignored Python caches, raw outputs, runtime `Experiments/`, and study outputs.
- `work2_coding/.gitignore` currently ignores `.idea`, `venv/`, `Experiments/`, `outputs/`, and `__pycache__/`.
- Phase 4-6 artifact builders already separate raw outputs under `work2_coding/outputs/` from lightweight review artifacts under `work2_coding/artifacts/` and root `artifacts/`.

### Established Patterns
- Use `work2_coding/` as the active runtime root. `.planning/codebase/` maps still contain stale `ooh_code/` references and should not drive path choices unless revalidated.
- Generated raw run state stays local; lightweight review artifacts may be committed when they carry status/provenance.
- Claim guards must fail closed when required evidence is blocked, placeholder-only, or directionally unsupported.

### Integration Points
- `.gitignore` at repo root should cover root-level temp/cache/build files without hiding intended artifact bundles.
- `work2_coding/.gitignore` can remain the local runtime-output ignore layer.
- Phase 08 outputs should feed Phase 09 checkpoint training by documenting whether `git_dirty=false` is reachable before evidence runs.

</code_context>

<specifics>
## Specific Ideas

- Create a hygiene/provenance report that classifies files into planning docs, generated artifacts, local outputs, dependency files, deleted user documents, and other local state.
- Explicitly mention `.planning/reports/MILESTONE_SUMMARY-v2.0.md` in the classification.
- Add comments to ignore rules that separate raw outputs from trackable artifact snapshots.
- Carry the user's claim-honesty instruction into later evidence phases: unsupported results must be marked failed or blocked.

</specifics>

<deferred>
## Deferred Ideas

- Training checkpoints is Phase 09 work.
- Running pilot attention evidence is Phase 10 work.
- Attention ablation and formal claim decisions are Phases 11-13 work.
- Full historical validation for Phases 1, 3, 4, 5, and 6 remains a residual milestone-level task if archive requires it.

</deferred>

---

*Phase: 08-Repository Hygiene And Provenance Freeze*
*Context gathered: 2026-06-11T21:48:50+08:00*
