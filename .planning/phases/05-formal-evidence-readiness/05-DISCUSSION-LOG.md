# Phase 5: Formal Evidence Readiness - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md. This log preserves the alternatives considered.

**Date:** 2026-06-14T10:33:22.3319183+08:00
**Phase:** 5-Formal Evidence Readiness
**Areas discussed:** Formal checkpoint lifecycle, Provenance snapshot scope, Formal replay gate shape, Claim-ready failure policy

---

## Formal Checkpoint Lifecycle

| Option | Description | Selected |
|--------|-------------|----------|
| Preflight + train step | Check the target checkpoint first; if missing, provide explicit train/generate steps while keeping claims gated by later formal replay. | Yes |
| Preflight only | Only report checkpoint existence, hash, and status; do not plan generation. | |
| Train and verify | Include formal checkpoint training, load verification, and archival in Phase 5. | |

**User's choice:** Preflight + train step
**Notes:** The formal target checkpoint path currently does not exist. Phase 5 should expose that as a blocker and define how to generate it, without unlocking claims.

| Option | Description | Selected |
|--------|-------------|----------|
| Hash + load smoke + metadata | Record path/hash and perform a minimal load smoke proving `checkpoint_load_status=loaded` can appear in row metadata. | Yes |
| Hash only | Require only file existence and SHA256 hash. | |
| Full pilot replay validation | Validate the checkpoint through pilot or small replay before readiness. | |

**User's choice:** Hash + load smoke + metadata
**Notes:** File existence alone is not enough for formal readiness.

| Option | Description | Selected |
|--------|-------------|----------|
| Blocked readiness report | Write a clear readiness/blocker report and avoid claim-ready artifact generation. | Yes |
| Diagnostic artifacts allowed | Continue to diagnostic/status artifacts while keeping claim-ready false. | |
| Stop without artifacts | Stop after terminal output only. | |

**User's choice:** Blocked readiness report
**Notes:** Missing or failed checkpoint state should be visible as structured evidence.

| Option | Description | Selected |
|--------|-------------|----------|
| Keep in runtime outputs, record immutable refs | Keep large checkpoint files in runtime outputs and record path/hash/command/load/provenance references. | Yes |
| Copy into phase evidence archive | Copy checkpoint files or archives into Phase 5 evidence storage. | |
| External archive pointer only | Record only an external archive pointer and hash. | |

**User's choice:** Keep in runtime outputs, record immutable refs
**Notes:** Do not commit large checkpoint files to git.

---

## Provenance Snapshot Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Full reproducibility bundle | Include `pip freeze`, package versions, platform, git commit/dirty state, manifest/settings/checkpoint hashes, run id, raw run dir, command, and key runtime knobs. | Yes |
| Environment + hashes only | Include environment and hashes, but not full freeze or git dirty details. | |
| Artifact-status only | Reuse only current artifact status summary fields. | |

**User's choice:** Full reproducibility bundle
**Notes:** Formal readiness should be audit-grade, not just artifact-grade.

| Option | Description | Selected |
|--------|-------------|----------|
| Block claim-ready if dirty | Allow blocked readiness reports, but never formal claim-ready when git is dirty. | Yes |
| Warn but allow | Record dirty status and still allow claim-ready. | |
| Ignore dirty state | Record only commit hash. | |

**User's choice:** Block claim-ready if dirty
**Notes:** A commit hash is insufficient if the working tree differs from it.

| Option | Description | Selected |
|--------|-------------|----------|
| Run dir + artifact sidecar | Save the full snapshot in the run directory and reference path/hash from artifact sidecars. | Yes |
| Phase planning dir only | Store only under `.planning/phases/05-.../`. | |
| Artifact dir only | Store only next to `ARTIFACT_STATUS.json`. | |

**User's choice:** Run dir + artifact sidecar
**Notes:** Raw output is the evidence source. Artifacts summarize and reference it.

| Option | Description | Selected |
|--------|-------------|----------|
| Command + resolved config | Store the original command, manifest path/hash, resolved paired settings, and key runtime arguments. | Yes |
| Command only | Store command and manifest hash only. | |
| Resolved config only | Store resolved configuration but omit original command. | |

**User's choice:** Command + resolved config
**Notes:** Both provenance angles are needed for reproducibility.

---

## Formal Replay Gate Shape

| Option | Description | Selected |
|--------|-------------|----------|
| Dedicated preflight/readiness script | Create or formalize a separate entry point for manifest, checkpoint, git/provenance, and settings checks. | Yes |
| Extend `run_study.py` directly | Put preflight, snapshot, and blocked report behavior into `run_study.py --execute`. | |
| Artifact gate only | Let replay run first and rely mainly on `build_artifacts.py --claim-ready`. | |

**User's choice:** Dedicated preflight/readiness script
**Notes:** Preflight should be distinct from actual replay and artifact generation.

| Option | Description | Selected |
|--------|-------------|----------|
| Machine + human report | Emit JSON for downstream gates and Markdown for audit. | Yes |
| JSON only | Emit only machine-readable output. | |
| Markdown only | Emit only human-readable output. | |

**User's choice:** Machine + human report
**Notes:** JSON feeds artifact/claim gates; Markdown supports review.

| Option | Description | Selected |
|--------|-------------|----------|
| No replay, strict prerequisites | Check manifest, checkpoint, load smoke, git/dependencies, resolved settings, and output/archive safety without replay. | Yes |
| One-row replay smoke | Also run a minimal replay smoke. | |
| Full dry-run contract rows | Generate contract-only rows, despite formal placeholder constraints. | |

**User's choice:** No replay, strict prerequisites
**Notes:** Readiness proves prerequisites, not empirical results.

| Option | Description | Selected |
|--------|-------------|----------|
| Artifact claim-ready requires readiness JSON | Formal `--claim-ready` must read and verify a passed readiness JSON. | Yes |
| Readiness report advisory only | Treat readiness as human reference only. | |
| Duplicate checks independently | Keep readiness and artifact checks separate without cross-reference. | |

**User's choice:** Artifact claim-ready requires readiness JSON
**Notes:** The readiness report is a hard dependency for formal claim-ready artifacts.

---

## Claim-Ready Failure Policy

| Option | Description | Selected |
|--------|-------------|----------|
| All formal evidence prerequisites | Hard-block claim-ready for checkpoint, dependency, git, manifest, readiness, row, placeholder, bad checkpoint, diagnostic, and no-filter failures. | Yes |
| Only row/artifact failures | Treat git/dependency/readiness gaps as warnings. | |
| Minimal hard blocks | Block only failed rows and missing checkpoint. | |

**User's choice:** All formal evidence prerequisites
**Notes:** Formal evidence should fail closed.

| Option | Description | Selected |
|--------|-------------|----------|
| Blocked readiness + diagnostic artifact only | Allow blocked readiness reports and diagnostic/status artifacts with `claim_ready=false`. | Yes |
| Readiness report only | Do not run artifact builder on failure. | |
| Nothing beyond logs | Rely only on terminal output. | |

**User's choice:** Blocked readiness + diagnostic artifact only
**Notes:** Failed gates can still produce auditable status outputs.

| Option | Description | Selected |
|--------|-------------|----------|
| Whole formal run blocked | Any failed, blocked, or incomplete row blocks the whole formal run from claim-ready. | Yes |
| Exclude failed rows and continue claims | Drop failed rows and claim on remaining rows. | |
| Per-policy claim readiness | Claim on complete policy/split subsets. | |

**User's choice:** Whole formal run blocked
**Notes:** No partial formal claim salvage.

| Option | Description | Selected |
|--------|-------------|----------|
| Artifact gate remains authoritative | Readiness permits replay/audit, but artifact gates still block claim-ready on missing metrics or placeholder outputs. | Yes |
| Readiness overrides artifact gaps | Allow missing non-core artifact data if readiness passes. | |
| Manual override allowed | Permit manual override of artifact gaps. | |

**User's choice:** Artifact gate remains authoritative
**Notes:** Readiness and artifact gates are cumulative.

---

## the agent's Discretion

- The agent may choose exact helper names, report schemas, and command names if
  they preserve the locked behavior and existing project patterns.

## Deferred Ideas

- None. Discussion stayed within Phase 5 scope.
