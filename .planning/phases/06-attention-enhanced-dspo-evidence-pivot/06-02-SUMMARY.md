---
phase: 06-attention-enhanced-dspo-evidence-pivot
plan: 02
subsystem: experiment-contracts
tags: [attention, paired-replay, manifests, normalized-rows, fairness]
requires:
  - phase: 06-attention-enhanced-dspo-evidence-pivot
    provides: deterministic DSPO attention scoring and parser knobs
provides:
  - DSPO_original and DSPO_attention policy adapters
  - attention-specific smoke, pilot, formal, and suite manifests
  - normalized row method and attention fields
  - pair-completeness annotation for attention rows
affects: [attention-artifacts, smoke-execution, claim-guard]
tech-stack:
  added: []
  patterns: [comparison_family manifest branch, explicit attention row schema]
key-files:
  created:
    - work2_coding/experiments/studies/smoke_attention_dspo.yaml
    - work2_coding/experiments/studies/pilot_attention_dspo.yaml
    - work2_coding/experiments/studies/formal_attention_dspo.yaml
    - work2_coding/experiments/suites/work2_attention_dspo.yaml
    - work2_coding/scripts/test_attention_manifest_contracts.py
    - work2_coding/scripts/test_attention_paired_rows.py
  modified:
    - work2_coding/Src/policy_adapters.py
    - work2_coding/Src/experiment_contracts.py
    - work2_coding/Src/paired_replay.py
    - work2_coding/Src/study_execution.py
    - work2_coding/scripts/run_study.py
key-decisions:
  - "Attention manifests use comparison_family: attention_dspo and require only DSPO_original and DSPO_attention."
  - "Main attention pairing varies only method_variant, attention_enabled, attention_mode, and attention_strength."
  - "Normalized rows carry explicit method, attention, pair, and net_objective_proxy fields."
patterns-established:
  - "Contract-only and blocked rows are annotated for attention pair completeness before validation."
requirements-completed: [ATTN-01, ATTN-03]
duration: 28min
completed: 2026-06-11
---

# Phase 06 Plan 02: Attention Contracts Summary

**Paired DSPO_original versus DSPO_attention manifests and normalized rows with explicit method identity**

## Performance

- **Duration:** 28 min
- **Started:** 2026-06-11T18:45:00+08:00
- **Completed:** 2026-06-11T19:13:00+08:00
- **Tasks:** 4
- **Files modified:** 11

## Accomplishments

- Added `DSPO_original` and `DSPO_attention` adapters as non-diagnostic method variants with identical robust-menu settings except attention switches.
- Added `attention_dspo` manifest validation so attention studies require the two main method tags without pulling robust diagnostics into the main ranking.
- Extended normalized rows with method identity, attention metadata, `attention_pair_id`, `attention_pair_complete`, and `net_objective_proxy`.
- Added attention smoke, pilot, formal, and suite manifests plus focused contract tests.
- Updated contract-only and actual replay row generation to annotate attention pair completeness.

## Task Commits

1. **Tasks 1-3: Method adapters, manifest family support, and row schema** - `a38fda6` (feat)
2. **Task 4: Attention study and suite manifests** - `3193652` (test)

**Plan metadata:** pending in this summary commit.

## Files Created/Modified

- `work2_coding/Src/policy_adapters.py` - Adds attention method tags and allows method/attention fields as policy-only variation.
- `work2_coding/Src/experiment_contracts.py` - Adds `attention_dspo` required-tag and main-method validation.
- `work2_coding/Src/paired_replay.py` - Adds explicit attention row fields and pair completeness helper.
- `work2_coding/Src/study_execution.py` - Propagates attention diagnostics from actual replay and annotates pair completeness.
- `work2_coding/scripts/run_study.py` - Annotates contract-only attention pairs before row validation.
- `work2_coding/experiments/studies/*attention_dspo.yaml` - Defines smoke, pilot, and formal attention contracts.
- `work2_coding/experiments/suites/work2_attention_dspo.yaml` - Defines the Phase 6 suite.
- `work2_coding/scripts/test_attention_manifest_contracts.py` - Tests attention manifest and adapter fairness.
- `work2_coding/scripts/test_attention_paired_rows.py` - Tests row schema defaults, diagnostics, and pair IDs.

## Decisions Made

- The two method variants share `risk_adjusted_expected_profit` and `chance_constraint` settings, leaving attention as the substantive treatment.
- Smoke attention studies are allowed to be contract-only or actual smoke; pilot/formal still require checkpoint provenance.
- Robust/no-filter/cost-bound policies remain outside the attention main comparison.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Forced ignored attention manifests into git**
- **Found during:** Task 4 (attention study manifests)
- **Issue:** New YAML files under `work2_coding/experiments/` were ignored by repository rules, so the first commit did not include them.
- **Fix:** Used `git add -f` for the four attention study/suite manifests and committed them separately.
- **Files modified:** attention study and suite YAML files.
- **Verification:** `git show --name-status 3193652` lists all four manifests.
- **Committed in:** `3193652`

---

**Total deviations:** 1 auto-fixed (blocking)
**Impact on plan:** Required manifests are now versioned; no behavioral scope change.

## Issues Encountered

None beyond the ignored-manifest handling documented above.

## Verification

- `cd work2_coding; python scripts/test_policy_fairness_contract.py` - PASS
- `cd work2_coding; python scripts/test_paired_replay_contract.py` - PASS
- `cd work2_coding; python scripts/test_experiment_contracts.py` - PASS
- `cd work2_coding; python scripts/test_attention_manifest_contracts.py` - PASS
- `cd work2_coding; python scripts/test_attention_paired_rows.py` - PASS
- `cd work2_coding; python scripts/run_study.py --study smoke_attention_dspo --contract-only` - PASS, emitted two paired rows
- `cd work2_coding; python -m py_compile Src/policy_adapters.py Src/experiment_contracts.py Src/paired_replay.py Src/study_execution.py scripts/test_attention_manifest_contracts.py scripts/test_attention_paired_rows.py scripts/run_study.py` - PASS

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Ready for Plan 06-03 to build the `work2_attention_dspo` artifact family and fail-closed attention claim guard.

---
*Phase: 06-attention-enhanced-dspo-evidence-pivot*
*Completed: 2026-06-11*
