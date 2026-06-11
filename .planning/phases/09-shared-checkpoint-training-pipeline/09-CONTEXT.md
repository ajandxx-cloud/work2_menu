# Phase 09 Context: Shared Checkpoint Training Pipeline

**Gathered:** 2026-06-11
**Status:** Ready for planning
**Mode:** Autonomous smart discuss; defaults accepted by prior user instruction to continue.

## Phase Boundary

Phase 09 creates a stable shared checkpoint training entry point for the attention evidence family. It must produce real checkpoint files and provenance sidecars for the pilot and formal manifests, and prove those checkpoints load through the same model path used by `run_study.py`.

This phase does not decide the attention-improves-DSPO claim. A checkpoint can remove the missing-checkpoint blocker, but later pilot/formal evidence must still decide whether the claim is supported.

## Decisions

- Build `work2_coding/scripts/train_shared_checkpoint.py` as the stable training entry point.
- Generate the manifest-declared checkpoints:
  - `work2_coding/outputs/shared_training/work2_attention_dspo/pilot/supervised_ml.pt`
  - `work2_coding/outputs/shared_training/work2_attention_dspo/formal/supervised_ml.pt`
- Write sidecars next to each checkpoint with sha256, command, seed, split/dataset fields, run_id, git commit, dirty status, manifest, training args, architecture, timestamp, and training data source.
- Use deterministic lightweight supervised training to produce non-placeholder model weights compatible with `DSPO_Menu.supervised_ml`.
- Record the training data source honestly. If the checkpoint is trained from a deterministic proxy rather than a full historical-data trainer, later evidence must not overclaim behavioral superiority.
- Validate loading through `model.load_checkpoint(...)`, the same aggregate path used by `run_study.py`.
- Keep generated checkpoint binaries and sidecars local/ignored under `work2_coding/outputs/`, consistent with Phase 08.

## Current Code Findings

- `pilot_attention_dspo.yaml` and `formal_attention_dspo.yaml` already require shared checkpoints.
- `run_study.py --execute` checks for checkpoint existence before actual pilot execution.
- `Src.study_execution._row_from_actual_replay` instantiates `Config`, builds `DSPO_Menu`, then calls `model.load_checkpoint(...)`.
- `Agent.load_checkpoint(...)` accepts either a file path or directory path and loads `supervised_ml.pt` via each module's `load(...)`.
- `DSPO_Menu` replaces the inherited predictor with a 3-output predictor (`output_dim=3`, `aux_dim=4`).
- Formal actual replay is still intentionally disabled until Phase 12.

## Risks

- A synthetic/proxy-trained checkpoint can remove engineering blockers but does not by itself make the attention claim scientifically true.
- The root `.gitignore` ignores `*.pt` and `work2_coding/outputs/`; generated checkpoint files are expected to remain local.
- Legacy tracked checkpoints still exist in historical experiment directories but are not Phase 09 evidence checkpoints.

