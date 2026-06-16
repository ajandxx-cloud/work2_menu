# M2 Provenance Requirements

**Phase:** 02 - Gate Cleanup Plan Without Destructive Changes
**Created:** 2026-06-16
**Purpose:** Define the minimum checkpoint, dependency, manifest, git, source
row, and formal-readiness evidence contract required before any Work2 final
replay or claim upgrade can be treated as claim-supporting.

## Phase 2 Boundary

Phase 2 documents requirements only. Phase 2 does not smoke-load checkpoints,
does not run formal readiness, does not write readiness outputs, does not run
replay, and does not regenerate artifacts or package status.

Current read-only observations:

- `work2_coding/Experiments/studies/formal_robust_menu.yaml` requires shared
  checkpoint `outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`
  with expected status `loaded`.
- The checkpoint file currently exists at
  `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt`.
- The expected sidecar
  `work2_coding/outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt.sidecar.json`
  is currently missing.
- Existing historical readiness JSON at
  `work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json`
  has `status=blocked` and `claim_ready_allowed=false`.

These observations do not authorize a final replay or claim upgrade. They only
identify what later approved work must prove.

## Required Evidence Fields

Any claim-supporting formal readiness and artifact chain must record the
following fields with these exact names.

| Field | Required meaning |
| --- | --- |
| `checkpoint_manifest_path` | Checkpoint path declared by the study manifest or runtime args. |
| `checkpoint_resolved_path` | Repository-local or absolute checkpoint path resolved for the active runtime root. |
| `checkpoint_sha256` | SHA-256 recomputed directly from the resolved checkpoint file. |
| `checkpoint_sidecar_path` | Expected sidecar metadata path, normally `<checkpoint>.sidecar.json`. |
| `checkpoint_sidecar_sha256` | SHA-256 recomputed directly from the sidecar file. |
| `checkpoint_load_status` | Runtime checkpoint load result, with claim-supporting status exactly `loaded`. |
| `dependency_snapshot_path` | Path to the dependency snapshot generated for the same readiness run. |
| `dependency_snapshot_sha256` | SHA-256 recomputed directly from the dependency snapshot file. |
| `manifest_path` | Study manifest path used for readiness and replay. |
| `manifest_hash` | Stable manifest hash from the validated manifest contract. |
| `git_sha` | Git commit SHA of the source tree used for readiness and replay. |
| `git_dirty` | Boolean dirty-state flag. Claim-supporting runs require `false` unless a later approved protocol explicitly marks the run diagnostic-only. |
| `readiness_json_path` | Path to `FORMAL_READINESS.json` consumed by artifact classification. |
| `readiness_json_sha256` | SHA-256 recomputed directly from `FORMAL_READINESS.json`. |
| `source_row_checkpoint_hashes` | Set of checkpoint hashes recorded by all formal source rows. |
| `source_row_checkpoint_load_statuses` | Set of checkpoint load statuses recorded by all formal source rows. |

## Source-Code Contract

`work2_coding/Src/formal_readiness.py` establishes the formal preflight shape:

- writes a dependency snapshot with `manifest_path`, `manifest_hash`,
  resolved settings, and command metadata;
- collects git provenance and blocks `git_dirty=true` unless an explicit dirty
  diagnostic override is used;
- resolves the manifest checkpoint path, recomputes the checkpoint file hash,
  reads sidecar metadata when present, smoke-loads the checkpoint, and records
  `checkpoint.load_status`;
- writes `FORMAL_READINESS.json` and `FORMAL_READINESS.md` with
  `claim_ready_allowed=true` only when all blockers clear.

`work2_coding/Src/study_execution.py` establishes row-level provenance:

- `inspect_manifest_prerequisites()` blocks missing checkpoint paths and
  missing checkpoint files for pilot/formal runs;
- `checkpoint_metadata_for_setting()` records `checkpoint_load_status`,
  `checkpoint_path`, `checkpoint_hash`, and `checkpoint_required`;
- completed rows keep checkpoint metadata separate from runtime outcome
  metrics.

`work2_coding/Src/artifact_status.py` enforces artifact readiness:

- formal readiness JSON must have `status == "passed"`;
- formal readiness JSON must set `claim_ready_allowed=true`;
- readiness git provenance must have `git_dirty=false`;
- dependency snapshot path and hash must exist and match the file on disk;
- readiness checkpoint must be loaded and hashed;
- readiness manifest hash must match the source run manifest hash;
- formal source rows must all report loaded checkpoint status;
- formal source row checkpoint hashes must include the readiness checkpoint
  hash;
- formal source rows must include checkpoint hashes.

## Fail-Closed Blocker Codes

These blocker codes must be represented separately so Phase 3 can distinguish
missing evidence from failed load, hash mismatch, dirty provenance, and row
metadata gaps.

| Blocker code | Fail-closed meaning | Current source relationship |
| --- | --- | --- |
| `missing_checkpoint_path` | The manifest or runtime args do not declare a required checkpoint path. | Emitted by `study_execution.inspect_manifest_prerequisites()`. |
| `missing_checkpoint_file` | A required manifest checkpoint path resolves to no file on disk. | Emitted by `study_execution.inspect_manifest_prerequisites()`. |
| `missing_formal_checkpoint` | The formal readiness preflight cannot find the resolved formal checkpoint file. | Emitted by `formal_readiness.check_formal_readiness()`. |
| `missing_checkpoint_sidecar` | The required checkpoint sidecar metadata file is absent. | Required by this Phase 2 contract; current readiness code records sidecar absence and should fail closed before claim use. |
| `formal_checkpoint_not_loaded` | Checkpoint smoke-load ran but did not report `loaded`. | Emitted by `formal_readiness.check_formal_readiness()`. |
| `formal_checkpoint_hash_mismatch` | The smoke-load checkpoint hash differs from the recomputed checkpoint file hash. | Emitted by `formal_readiness.check_formal_readiness()`. |
| `formal_checkpoint_load_failed` | Checkpoint smoke-load raised an exception. | Emitted by `formal_readiness.check_formal_readiness()`. |
| `dirty_git` | Git provenance is dirty for a run that would otherwise claim formal readiness. | Emitted by `formal_readiness.check_formal_readiness()`. |
| `missing_dependency_snapshot` | Readiness or artifact classification lacks a dependency snapshot file/path/hash. | Required by `artifact_status.validate_formal_readiness_for_run()`. |
| `dependency_snapshot_hash_mismatch` | Recorded dependency snapshot hash does not match the file. | Required by `artifact_status.validate_formal_readiness_for_run()`. |
| `readiness_manifest_hash_mismatch` | Readiness manifest hash differs from source run rows or summary. | Required by `artifact_status.validate_formal_readiness_for_run()`. |

## Authoritative Hash Rule

The recomputed checkpoint SHA-256 is authoritative. Sidecar metadata is
supporting provenance and cannot substitute for hashing the checkpoint file.
Claim-supporting readiness must recompute and record both
`checkpoint_sha256` and `checkpoint_sidecar_sha256`; a sidecar-declared hash is
only useful if it matches the recomputed checkpoint file hash or records an
approved diagnostic mismatch reason.

## Readiness JSON Contract

A readiness JSON may support formal artifacts only when all of the following
hold:

1. `readiness_json_path` exists.
2. `readiness_json_sha256` is recomputed from the file consumed by artifact
   classification.
3. JSON `status` is `passed`.
4. JSON `claim_ready_allowed` is `true`.
5. `git_dirty` is `false`.
6. `dependency_snapshot_path` exists and
   `dependency_snapshot_sha256` matches the file.
7. `manifest_hash` matches the manifest hash in source rows or run summary.
8. `checkpoint_load_status` is `loaded`.
9. `checkpoint_sha256` exists and matches source-row checkpoint hashes.
10. `source_row_checkpoint_load_statuses` contains only `loaded` for required
    formal rows.

If any item fails, the evidence may be described only as blocked, diagnostic,
or status/provenance transparency according to the strict claim guard.

## Commands Not Executed In Phase 2

The following command templates are approval-required and were not executed in
Phase 2:

```powershell
cd work2_coding
python scripts/train_shared_checkpoint.py --study formal_robust_menu --checkpoint-path outputs/shared_training/work2_robust_menu/formal/supervised_ml.pt
python scripts/check_formal_readiness.py --study formal_robust_menu --output-root outputs/formal_readiness --diagnostic-ok
python scripts/run_study.py --study formal_robust_menu --execute
python scripts/build_artifacts.py --run-dir outputs/studies/<study>/<run_id> --claim-ready
python scripts/build_phase10_paper_artifacts.py --default-mirror
```

Phase 3 may use this contract to decide whether a clean, pre-registered final
replay is legitimate. Phase 2 does not make that decision.
