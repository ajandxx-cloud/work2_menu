---
phase: 4
plan: 04-03-manuscript-frame-and-end-to-end-verification
status: complete
completed: 2026-06-14
key_files:
  - work2_coding/Src/artifact_builder.py
  - work2_coding/Src/manuscript_claims.py
  - work2_coding/scripts/test_artifact_gates.py
---

# 04-03 Summary: Manuscript Frame And End-To-End Verification

## Result

Manuscript-frame and claim-guard generation is now part of the Phase 4 artifact
bundle path.

- `build_artifacts()` writes manuscript-frame files from `ARTIFACT_STATUS.json`.
- `build_manuscript_frame.py` remains a working standalone entry point.
- Generated claim language now reflects the seven-tag V1 mainline family.
- Smoke artifacts remain diagnostic/status evidence and do not unlock empirical
  superiority or formal ranking claims.
- `CLAIM_GUARD.json` is generated and blocks unsupported claims.

## Verification

Run from `work2_coding/`:

```powershell
python scripts/test_artifact_gates.py
python scripts/run_study.py --study smoke_robust_menu --execute --output-root outputs/phase4_verification
python scripts/build_artifacts.py --run-dir outputs/phase4_verification/smoke_robust_menu/smoke_robust_menu-20260614T021107Z-759dc2ce --output-root outputs/phase4_artifacts --allow-incomplete
python scripts/build_manuscript_frame.py --artifact-root outputs/phase4_artifacts
```

Results:

```text
PASS: 13 artifact gate tests
artifact_status=diagnostic
claim_ready=False
row_count=28
guard_status=diagnostic
guard_claim_ready=False
```

Ranking/baseline checks:

- recommended ranking contains six operational mainline tags
- baseline/boundary output contains `mainline_no_menu`

## Deviations

None.

## Self-Check

PASSED. The implementation covers D-02 through D-08 and completes the Phase 4
end-to-end smoke artifact verification without editing manuscript source or
generated result rows by hand.
