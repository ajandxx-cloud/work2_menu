# Phase 5: Formal Evidence Readiness - Context

**Gathered:** 2026-06-14T10:33:22.3319183+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 prepares the formal evidence readiness layer for Work2 V1 mainline
results. It should define and implement formal preflight checks, checkpoint
readiness, provenance snapshots, readiness reports, and claim-ready hard gates
before any formal rows can support manuscript claims.

This phase does not make empirical claims, edit manuscript source, hand-edit
generated rows, or treat smoke/pilot diagnostics as formal evidence. Formal
actual replay may be enabled only after readiness gates pass, and artifact
claim-readiness remains authoritative after replay.

</domain>

<decisions>
## Implementation Decisions

### Formal Checkpoint Lifecycle

- **D-01:** Phase 5 should implement a formal checkpoint preflight plus a clear
  train/generate step. If
  `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`
  is missing, the readiness workflow must report the missing prerequisite and
  provide the exact command or documented step needed to generate it.
- **D-02:** Phase 5 does not unlock formal claims merely by generating a
  checkpoint. Formal claims still require gated formal replay and artifact
  claim-ready checks.
- **D-03:** A generated formal checkpoint must be accepted only with path,
  SHA256 hash, a minimal load smoke, and proof that row metadata can report
  `checkpoint_load_status="loaded"`.
- **D-04:** If checkpoint generation or loading fails, Phase 5 should produce a
  blocked readiness report that explains the failed gate. It must not produce
  claim-ready artifacts from random or failed checkpoint state.
- **D-05:** Large checkpoint files stay under the runtime output tree rather
  than being committed to git. Phase 5 records immutable references: path,
  hash, generation command, load-smoke result, and provenance metadata.

### Provenance Snapshot Scope

- **D-06:** Formal-ready provenance should use a full reproducibility bundle:
  `pip freeze`, Python/package versions, platform, git commit, git dirty
  status, manifest hash, settings hash, checkpoint hash, run id, raw run
  directory, formal command, and key HGS/runtime/menu/checkpoint knobs.
- **D-07:** `git_dirty=true` must hard-block formal claim-ready status. Blocked
  readiness reports are still allowed so the cause is visible.
- **D-08:** Dependency snapshots should be saved in the formal run/output
  directory. Artifact and claim sidecars should reference the snapshot path and
  hash rather than becoming the only source of provenance.
- **D-09:** The snapshot should record both the original command and resolved
  configuration, including resolved paired settings and key parser arguments.

### Formal Replay Gate Shape

- **D-10:** Phase 5 should add or formalize a dedicated preflight/readiness
  script instead of folding all preflight behavior directly into
  `scripts/run_study.py` or leaving it solely to `build_artifacts.py`.
- **D-11:** The readiness script should emit both machine-readable JSON and a
  human-readable Markdown report.
- **D-12:** The readiness script should perform no formal replay. It checks
  strict prerequisites only: manifest contract validity, checkpoint path/hash,
  checkpoint load smoke, git/dependency provenance, resolved settings, output
  directory safety, and archive/reference paths.
- **D-13:** Formal `build_artifacts.py --claim-ready` should require and verify
  a passed readiness JSON for formal runs. The readiness report is a hard
  dependency for claim-ready artifacts, not an advisory note.

### Claim-Ready Failure Policy

- **D-14:** All formal evidence prerequisites hard-block claim-ready status:
  missing or failed checkpoint load, missing dependency snapshot,
  `git_dirty=true`, invalid manifest contract, missing or failed readiness JSON,
  failed/blocked/incomplete rows, placeholder or contract-only rows, bad
  checkpoint status, diagnostic-only rows, and no-filter-only evidence.
- **D-15:** Failure may still produce a blocked readiness report and
  diagnostic/status artifacts. Every claim guard in that state must report
  `claim_ready=false`.
- **D-16:** A single failed, blocked, or incomplete formal row blocks the whole
  formal run from claim-ready status. Failed rows are not excluded to salvage a
  formal claim.
- **D-17:** Artifact gates remain authoritative after readiness passes. If
  `build_artifacts.py --claim-ready` fails because metrics, tables, figures, or
  placeholder/status artifacts are incomplete, formal claim-ready status remains
  blocked.

### the agent's Discretion

The agent may choose exact helper names, report schemas, and command names as
long as the implementation preserves the decisions above, uses existing
manifest/run/artifact patterns, and adds script-style tests for the new gates.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning And Prior Phase Evidence

- `.planning/PROJECT.md` - Work2 V1 scope, seven-tag mainline family, and
  formal-evidence guardrails.
- `.planning/REQUIREMENTS.md` - Requirements for checkpoint provenance,
  artifact gates, normalized-row-v2, and generated artifacts.
- `.planning/ROADMAP.md` - Phase 5 boundary and success criteria.
- `.planning/STATE.md` - Current position and Phase 5 handoff notes.
- `.planning/repository_audit.md` - Active `work2_coding/` root, stale path
  mapping, reusable robust-menu inventory, and formal evidence gaps.
- `.planning/phases/02-service-product-contract/02-VERIFICATION.md` - Verified
  service product, row-v2, opt-out, and artifact-gate foundation.
- `.planning/phases/03-mainline-comparison-contract/03-VERIFICATION.md` -
  Verified seven-tag mainline manifest contract and smoke replay.
- `.planning/phases/04-mainline-artifact-pipeline-and-claim-guard/04-VERIFICATION.md`
  - Verified artifact pipeline and claim guard behavior before Phase 5.

### Formal Manifest And Runtime Outputs

- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Formal V1
  manifest requiring seven mainline tags, five splits, `menu_k=3`, and loaded
  shared checkpoint provenance.
- `work2_coding/outputs/shared_training/` - Runtime root for shared training
  checkpoints. Current inspection found the formal robust-menu checkpoint path
  missing.
- `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`
  - Required formal checkpoint target referenced by the formal manifest. This
  path did not exist during discussion.

### Readiness, Study, And Artifact Code

- `work2_coding/Src/study_execution.py` - Checkpoint path resolution,
  prerequisite inspection, checkpoint hashing, blocked rows, actual replay row
  generation, failed-row behavior, and git provenance collection.
- `work2_coding/scripts/run_study.py` - Study execution CLI, manifest snapshot
  writing, blocked formal behavior, normalized rows, and study summaries.
- `work2_coding/Src/artifact_status.py` - Claim-ready classification,
  checkpoint status checks, dependency snapshot handling, and environment
  provenance helper.
- `work2_coding/Src/artifact_builder.py` - Artifact generation, status JSON,
  claim-ready enforcement, environment provenance, sidecars, and mirror behavior.
- `work2_coding/Src/manuscript_claims.py` - Claim guard generation and
  manuscript-frame status language.
- `work2_coding/scripts/build_artifacts.py` - Artifact CLI and
  `--claim-ready` entry point.
- `work2_coding/scripts/build_manuscript_frame.py` - Manuscript-frame and claim
  guard CLI.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `formal_robust_menu.yaml` already declares the formal checkpoint contract:
  `shared_checkpoint.required=true`, `expected_status=loaded`, fixed
  `menu_k=3`, five paired splits, and the seven mainline policies.
- `study_execution.inspect_manifest_prerequisites()` already blocks pilot/formal
  runs when required checkpoints are missing.
- `study_execution.checkpoint_metadata_for_setting()` already resolves
  checkpoint paths and writes `checkpoint_load_status`, `checkpoint_hash`, and
  checkpoint required metadata.
- `study_execution.collect_git_provenance()` already captures git commit,
  dirty status, and a status summary.
- `artifact_status.collect_environment_provenance(include_freeze=True)` already
  captures Python/platform/package versions and optional `pip freeze`.
- `artifact_status.classify_artifact()` already blocks bad checkpoint status,
  failed/blocked/incomplete rows, placeholder rows, formal claim-ready without
  dependency snapshot, diagnostic rows, and no-filter-only rows.
- `artifact_builder.build_artifacts()` already has a `claim_ready` mode and
  writes `ARTIFACT_STATUS.json` plus sidecar metadata.

### Established Patterns

- Use script-style tests under `work2_coding/scripts/`.
- Keep studies manifest-driven under `work2_coding/Experiments/studies/`.
- Keep raw run outputs under `work2_coding/outputs/`; generated artifacts and
  lightweight mirrors should reference raw outputs rather than replace them.
- Keep checkpoint and dependency provenance explicit in machine-readable JSON,
  not only in terminal logs.
- Diagnostic/status artifacts may exist when gates fail, but formal
  claim-ready artifacts must fail closed.

### Integration Points

- Add a dedicated formal readiness/preflight script under
  `work2_coding/scripts/` or an equivalent thin CLI over reusable helpers.
- Add reusable readiness helpers near `work2_coding/Src/study_execution.py` or a
  new module if that keeps preflight/report logic clean.
- Extend formal artifact claim-ready behavior so `build_artifacts.py
  --claim-ready` requires a passed readiness JSON for formal runs.
- Extend artifact status or artifact builder metadata to reference the
  dependency snapshot path/hash and readiness JSON path/hash.
- Add tests for missing formal checkpoint, dirty git blocking, dependency
  snapshot presence, readiness JSON failure, readiness JSON success, and
  artifact claim-ready requiring readiness JSON.

</code_context>

<specifics>
## Specific Ideas

- Current inspection found no
  `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`;
  the readiness path should therefore produce a clear blocked report until the
  formal shared checkpoint is generated and load-smoked.
- Readiness JSON should be reusable by artifact/claim gates. Markdown report is
  for audit and human review only.
- Formal readiness proves that formal replay is safe to attempt and auditable.
  It does not by itself prove empirical superiority.

</specifics>

<deferred>
## Deferred Ideas

None. Discussion stayed within Phase 5 scope.

</deferred>

---

*Phase: 5-Formal Evidence Readiness*
*Context gathered: 2026-06-14T10:33:22.3319183+08:00*
