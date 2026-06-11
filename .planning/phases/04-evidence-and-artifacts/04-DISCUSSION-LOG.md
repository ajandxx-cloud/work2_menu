# Phase 4: Evidence And Artifacts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md; this log preserves the alternatives considered.

**Date:** 2026-06-11T14:50:02+08:00
**Phase:** 4-Evidence And Artifacts
**Areas discussed:** Run Ladder, Artifact Set, Artifact Gate, Provenance Pack
**Response format requested by user:** `1A,2B` style batched answers.

---

## Run Ladder

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| Minimum completion bar | A | Smoke real run is enough; pilot/formal can record blockers. | |
| Minimum completion bar | B | Pilot must produce real non-placeholder results; formal may be deferred with a gate report. | Yes |
| Minimum completion bar | C | Formal must produce real non-placeholder results. | |
| `contract_only` artifact use | A | Only diagnostic reports; no paper tables/figures. | |
| `contract_only` artifact use | B | Placeholder/incomplete artifacts allowed if visibly marked and barred from claims. | Yes |
| `contract_only` artifact use | C | Artifact builder must not consume `contract_only` rows. | |
| Missing required checkpoint | A | Fail closed and produce no results. | |
| Missing required checkpoint | B | Produce incomplete status and blocker report; no formal claim artifact. | Yes |
| Missing required checkpoint | C | Continue with random initialization marked diagnostic. | |
| Shared checkpoint training | A | Do not train; only consume existing checkpoints. | |
| Shared checkpoint training | B | Smoke/pilot may train or reuse checkpoints; formal needs explicit provenance. | Yes |
| Shared checkpoint training | C | Phase 4 must include full formal checkpoint training. | |

**User's choice:** `1B,2B,3B,4B`

---

## Artifact Set

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| Builder priority | A | Generate only JSON/CSV first. | |
| Builder priority | B | Generate JSON/CSV, core LaTeX tables, and PNG figures. | Yes |
| Builder priority | C | Generate only Markdown reports first. | |
| Core tables | A | One policy aggregate summary table. | |
| Core tables | B | Five table families: policy summary, robust filtering, exact/greedy, uptake regime, provenance/status. | Yes |
| Core tables | C | As many tables as possible, including all candidate diagnostics. | |
| Core figures | A | Only a net profit gap figure. | |
| Core figures | B | 4-6 reviewer-facing plots: profit gap, acceptance/opt-out, ETA pruning, home-only share, exact/greedy time/gap. | Yes |
| Core figures | C | No figures yet; tables only. | |
| Output locations | A | Only `work2_coding/outputs/`. | |
| Output locations | B | Raw outputs in `work2_coding/outputs/`, lightweight artifacts in `work2_coding/artifacts/`, mirrored to `artifacts/work2_robust_menu/`. | Yes |
| Output locations | C | Everything under root `artifacts/`. | |

**User's choice:** `1B,2B,3B,4B`

---

## Artifact Gate

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| Placeholder handling | A | Generate all tables/figures if title marks placeholder. | |
| Placeholder handling | B | Only incomplete/diagnostic reports; no claim-ready tables/figures. | Yes |
| Placeholder handling | C | Artifact builder fails immediately. | |
| Bad checkpoint status | A | Generate formal artifacts but note provenance. | |
| Bad checkpoint status | B | Block claim-ready artifacts and generate blocker/status artifacts. | Yes |
| Bad checkpoint status | C | Stop completely and write no artifacts. | |
| Missing uptake regime | A | Allow results for available regimes. | Yes |
| Missing uptake regime | B | Mark evidence incomplete and block formal robust-menu conclusion. | |
| Missing uptake regime | C | Fail until all regimes are rerun. | |
| `no_filter_diagnostic` in main results | A | Show equally with other policies. | |
| `no_filter_diagnostic` in main results | B | Show as diagnostic upper bound; do not include in recommended-policy ranking. | Yes |
| `no_filter_diagnostic` in main results | C | Only appendix diagnostics. | |

**User's choice:** `1B,2B,3A,4B`
**Notes:** The uptake-regime decision is intentionally permissive: available-regime results may be emitted, but artifact metadata should state coverage to prevent overgeneralization.

---

## Provenance Pack

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| Row provenance fields | A | Only `run_id`, `policy_tag`, `seed`, and `split_id`. | |
| Row provenance fields | B | Full provenance: `run_id`, `manifest_hash`, `settings_hash`, `trace_id/hash`, checkpoint status/path/hash, git marker, schema version. | Yes |
| Row provenance fields | C | Full provenance plus all candidate-level menu diagnostics. | |
| Artifact source metadata | A | Study name in filename is enough. | |
| Artifact source metadata | B | Adjacent metadata/status JSON for source rows, source run, manifest hash, generation time, and placeholder/incomplete status. | Yes |
| Artifact source metadata | C | Only one global README. | |
| Dependency provenance | A | Do not record dependencies; rely on `requirements.txt`. | |
| Dependency provenance | B | Record Python version and key package versions or `pip freeze`; formal artifacts require the snapshot. | Yes |
| Dependency provenance | C | Require a full lockfile for Phase 4 completion. | |
| Git status | A | Record commit/dirty marker; dirty worktree allowed but explicitly marked. | Yes |
| Git status | B | Dirty worktree blocks all artifacts. | |
| Git status | C | Do not record git status. | |

**User's choice:** `1B,2B,3B,4A`

---

## The Agent's Discretion

- Exact helper/module names.
- Exact metadata sidecar filenames and status vocabulary.
- Whether artifact logic starts as one script or is split into reusable helpers.

## Deferred Ideas

- Manuscript claim wording and final claim checklist belong to Phase 5.
- Attention-based choice/scoring and advanced ETA calibration remain outside Phase 4.
