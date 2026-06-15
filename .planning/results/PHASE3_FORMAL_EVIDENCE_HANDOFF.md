---
phase: 03-formal-rc-evidence-pipeline-repair-and-completion
plan: 03-03
status: diagnostic_handoff_ready
created: 2026-06-15T12:10:00+08:00
timezone: Asia/Shanghai
---

# Phase 3 Formal Evidence Handoff

## Source Run For Phase 4

Use this completed formal run for Phase 4 RC result diagnosis:

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a
```

| Field | Value |
| --- | --- |
| Run ID | `formal_robust_menu-20260614T032323Z-c672286a` |
| Study | `formal_robust_menu` |
| Tier | `formal` |
| Execution status | `completed` |
| Row count | `35` |
| Splits | `5` |
| Policies per split | `7` |
| Uptake regimes | `low`, `medium` |
| Checkpoint status | `loaded` |
| Placeholder-only | `false` |
| Failed row count | `0` |
| Manifest hash in source run | `c672286a45342771a92d28d14f8f7e85fd20dea9a5f89ab50a8aca375e54296c` |

The prior failed run remains documented in
`.planning/results/FORMAL_FAILURE_DIAGNOSIS.md` and should be treated as
runtime-failure history, not empirical performance evidence.

## Readiness Gate

Readiness artifact:

```text
work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json
```

| Field | Value |
| --- | --- |
| Readiness status | `blocked` |
| Claim-ready allowed | `false` |
| Blocking code | `dirty_git` |
| Checkpoint hash | `d351dd62c3b2cdb008d6952cf81b1b041b64244aa20b82fab9f742b502b7acf4` |
| Checkpoint load status | `loaded` |
| Dependency snapshot | `work2_coding/outputs/phase5_readiness/formal_robust_menu/DEPENDENCY_SNAPSHOT.json` |

Dirty-git readiness details and non-destructive cleanup recommendations are in:

```text
.planning/results/FORMAL_BLOCKER_DIAGNOSIS.md
```

## Artifact Bundle

Artifact root:

```text
work2_coding/outputs/phase3_formal_artifacts
```

Build command used from `work2_coding/`:

```powershell
python scripts/build_artifacts.py --run-dir outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a --output-root outputs/phase3_formal_artifacts --allow-incomplete --readiness-json outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json
```

The artifact bundle was generated through the builder only. No tables, figures,
rows, or claim-guard files were edited by hand.

| Field | Value |
| --- | --- |
| Artifact status file | `work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json` |
| Artifact status | `blocked` |
| Claim-ready | `false` |
| Formal claim-ready | `false` |
| Source run dir | `outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a` |
| Artifact row count | `35` |
| Artifact checkpoint statuses | `loaded` |
| Artifact reasons | `pilot/formal rows require outside_option_util metadata`; `pilot/formal rows require valid method_family metadata` |

Generated diagnostic outputs include policy summaries, LaTeX tables, acceptance
and exact/greedy figures, provenance status, manuscript outlines, and status
JSON files under `work2_coding/outputs/phase3_formal_artifacts/`.

## Claim Guard

Claim guard artifact:

```text
work2_coding/outputs/phase3_formal_artifacts/manuscript/CLAIM_GUARD.json
```

Manuscript frame command used from `work2_coding/`:

```powershell
python scripts/build_manuscript_frame.py --artifact-root outputs/phase3_formal_artifacts
```

| Field | Value |
| --- | --- |
| Claim-ready | `false` |
| Formal claim-ready | `false` |
| Artifact status | `blocked` |
| Source run ID | `formal_robust_menu-20260614T032323Z-c672286a` |
| Allowed conditional output | Diagnostic/status tables and blocked-artifact explanations |

Blocked claim IDs include:

1. `universal_dominance`
2. `real_passenger_validation`
3. `no_filter_operational_recommendation`
4. `full_dynamic_exact_optimality`
5. `ungated_dspo_plus_ranking`
6. `empirical_superiority`
7. `pilot_formal_completed`

Allowed claims remain implementation/gate transparency claims only:

- robust service-menu framework implementation
- robust pruning mode availability
- exact-small/greedy-large auditability
- paired replay contract definition
- artifact status transparency
- generated model-consistency metadata contracts

## Verification

Run from `work2_coding/`:

| Command | Result |
| --- | --- |
| `python scripts/build_artifacts.py --run-dir outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a --output-root outputs/phase3_formal_artifacts --allow-incomplete --readiness-json outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json` | Generated diagnostic bundle; artifact status `blocked` |
| `python scripts/build_manuscript_frame.py --artifact-root outputs/phase3_formal_artifacts` | Generated manuscript frame; claim guard `claim_ready: false` |
| `python scripts/test_artifact_gates.py` | PASS: 22 artifact gate tests |

## Phase 4 Guidance

Phase 4 should diagnose the completed formal rows for effect sizes, paired
split differences, uptake-regime behavior, and trade-offs. It should not treat
the current artifact bundle as support for strong empirical superiority claims.

The immediate scientific input is:

```text
work2_coding/outputs/formal_v1/formal_robust_menu/formal_robust_menu-20260614T032323Z-c672286a/normalized_rows.json
```

The immediate gate input is:

```text
work2_coding/outputs/phase3_formal_artifacts/ARTIFACT_STATUS.json
work2_coding/outputs/phase3_formal_artifacts/manuscript/CLAIM_GUARD.json
work2_coding/outputs/phase5_readiness/formal_robust_menu/FORMAL_READINESS.json
```

Phase 4 may classify claims as strong, conditional, weak/diagnostic, or
unsupported only after analyzing the row metrics. This handoff does not make
that classification.
