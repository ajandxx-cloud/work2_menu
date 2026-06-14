# Phase 09: DSPO Family Full Run - Validation Contract

**Created:** 2026-06-14
**Status:** Ready for execution planning
**Scope:** Nyquist validation artifact for Phase 9 plans

## Validation Objective

Phase 9 is valid only if the executor can prove that `dspo_clip` and
`dspo_wide` run as DSPO-only paired replay policies over the exact Phase 8
formal-equivalent split contract, and that the resulting report blocks unsafe
evidence without creating ranking claims.

## Required Evidence

| Requirement | Evidence | Gate |
| --- | --- | --- |
| EXP-04 | `phase9_dspo_family_validation` produces ten actual rows: five splits times `dspo_clip` and `dspo_wide`. | Blocking |
| GATE-01 | Every DSPO row records `checkpoint_load_status=loaded`, checkpoint path, and checkpoint hash. | Blocking |
| GATE-02 | Failed, blocked, incomplete, placeholder-only, diagnostic, no-filter, or contract-only rows are not claim-eligible. | Blocking |
| GATE-04 | Every failure record includes reason, minimal fix, rerun command, and evidence location. | Blocking |

## Sampling Plan

1. **Contract sampling:** Unit/script tests validate adapters, manifest shape,
   paired fields, method family, checkpoint contract, and DSPO_PLUS exclusion.
2. **Gate sampling:** Synthetic completed and broken rows exercise the Phase 9
   validator before any expensive run.
3. **Runtime sampling:** The actual Phase 9 study executes the five Phase 8
   formal-equivalent splits with both DSPO policies.
4. **Report sampling:** JSON and Markdown outputs are inspected for gate-first
   language, status-only sanity comparison, claim-ready separation, and debug
   handoff details.

## Commands

Run from `work2_coding/`:

```powershell
python -c "import sys; sys.path.insert(0, '.'); import Src.config; print('IMPORT_OK')"
python scripts/test_phase9_dspo_family_validation.py
python scripts/test_experiment_contracts.py
python scripts/test_policy_fairness_contract.py
python scripts/test_method_family_contract.py
python scripts/test_artifact_gates.py
python scripts/test_checkpoint_provenance.py
python scripts/test_optout_accounting.py
python scripts/run_study.py --study phase9_dspo_family_validation --execute --output-root outputs/studies
python scripts/build_phase9_dspo_family_validation_report.py --output-root outputs/phase9_dspo_family_validation
```

## Pass Criteria

- The import smoke passes from `work2_coding/`.
- Contract tests prove `dspo_clip=0.35`, `dspo_wide=0.45`,
  `method_family=DSPO`, and `comparison_role=dspo_family`.
- The manifest contains only `dspo_clip` and `dspo_wide`, copies the Phase 8
  split values exactly, and preserves the Phase 8 loaded-checkpoint contract.
- The report returns `dspo_validation_status=passed` and `phase9_gate=open`, or
  returns a blocked/debug-ready report with complete failure records.
- The report explicitly states that DSPO_PLUS is excluded from Phase 9 and that
  any sanity comparison is not a manuscript ranking conclusion.

## Fail Criteria

- Any Phase 9 row is failed, blocked, incomplete, placeholder-only, contract-only,
  diagnostic, no-filter-only, or missing row-v2 provenance.
- Any required checkpoint field is missing or `checkpoint_load_status` is not
  `loaded`.
- Clip/wide paired rows drift on shared replay fields other than declared DSPO
  threshold/policy identity fields.
- Opt-out, accepted-home, and accepted-meeting-point accounting does not sum or
  rate correctly.
- The report unlocks ranking claims, generates a claim-ready artifact bundle, or
  validates DSPO_PLUS.

## Resolved Research Decisions

- Preserve Phase 8 split IDs exactly in the Phase 9 manifest.
- Use `net_profit`, `served_rate`, and `optout_rate` only as status-only sanity
  indicators, never as ranking-claim unlocks.
- Add Phase 9 DSPO-only tests and avoid broad DSPO_PLUS cleanup unless existing
  tests directly block Phase 9.
