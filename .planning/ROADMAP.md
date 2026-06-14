# Roadmap: Work2 Robust Time-Window Service Menu Optimization

## Execution Policy: Local-Only

This project is executed offline/local-only. Do not require git commit, git
push, remote branch creation, or PR publication as part of project progress,
verification, formal readiness, artifact generation, or manuscript preparation.

Git may be inspected only as a local provenance signal when useful, but project
completion must not depend on updating a remote git repository. For formal
evidence, prefer local reproducibility artifacts such as readiness JSON,
dependency snapshots, manifest hashes, checkpoint hashes, command logs, and
output-directory archives.

If a gate currently reports `dirty_git`, treat it as a local provenance warning
to document unless a later roadmap phase explicitly reinstates clean-git as a
hard requirement. Do not use `dirty_git` alone to force git commits or pushes.

## Phase 1: Repository Audit

**Goal:** Verify the active runtime root, audit stale planning/codebase references,
and inventory reusable Work2 robust-menu code, manifests, tests, and artifacts.

**Status:** Complete

**Evidence:** `.planning/repository_audit.md`

**Success Criteria**:
1. `work2_coding/` import smoke passes.
2. Stale `ooh_code/` references are mapped or marked obsolete.
3. Reusable robust-menu and attention/diagnostic assets are classified.
4. Phase 2 risks and coverage gaps are documented.

**Requirements:** RUN-01, RUN-02, RUN-03

## Phase 2: Service Product Contract

**Goal:** Define and verify the explicit service product, product-mode,
time-window-mode, menu-mode, pricing, normalized-row-v2, and artifact gate
contracts.

**Status:** Complete

**Evidence:** `.planning/phases/02-service-product-contract/02-VERIFICATION.md`

**Success Criteria**:
1. Product modes `m`, `m+w`, and `m+w+p` are represented and tested.
2. Time-window modes `no_time_window`, `fixed_window`, and `adaptive_window` are
   represented and tested.
3. Menu modes `no_menu`, `fixed_menu`, `random_menu`, and `optimized_menu` are
   represented and tested.
4. Row-v2 and failed-row contracts are validated.
5. Phase 2 smoke replay completes.

**Requirements:** SPC-01, SPC-02, SPC-03, SPC-04, SPC-05, ROW-01, ROW-02, ROW-03, ROW-04

## Phase 3: Mainline Comparison Contract

**Goal:** Migrate `work2_robust_menu` smoke, pilot, and formal manifests to the
seven-tag V1 mainline comparison family and verify smoke actual replay.

**Status:** Complete

**Evidence:** `.planning/phases/03-mainline-comparison-contract/03-VERIFICATION.md`

**Success Criteria**:
1. Seven mainline adapter tags are implemented and tested.
2. Smoke and pilot cover `menu_k={1,2,3,5}`.
3. Formal fixes `menu_k=3`, declares at least five paired splits, and requires
   checkpoint provenance.
4. Row, failure, paired fairness, and eligibility tests cover the mainline family.
5. Smoke actual replay completes with all seven policy tags.

**Requirements:** MLC-01, MLC-02, MLC-03, MLC-04, MLC-05, MLC-06, ROW-01, ROW-02, ROW-03, ROW-04, ROW-05

## Phase 4: Mainline Artifact Pipeline And Claim Guard

**Goal:** Make the artifact and claim pipeline consume normalized-row-v2
mainline outputs from the seven-tag family and generate manuscript-facing
evidence without hand-editing result rows or paper artifacts.

**Status:** Complete

**Evidence:** `.planning/phases/04-mainline-artifact-pipeline-and-claim-guard/04-VERIFICATION.md`

**Success Criteria**:
1. Artifact builder accepts mainline normalized-row-v2 study outputs.
2. Claim guards exclude diagnostic, failed, blocked, placeholder-only,
   no-filter-only, contract-only, and bad-checkpoint rows.
3. Generated tables/figures include source run IDs, manifest hashes,
   checkpoint status, and artifact status.
4. Mirrored artifact bundles are generated from `work2_coding/` outputs.
5. Phase 4 tests and smoke artifact build pass without formal replay.

**Requirements:** ART-01, ART-02, ART-03, ART-04, RUN-04

## Phase 5: Formal Evidence Readiness

**Goal:** Prepare formal replay prerequisites and evidence gates for claim-ready
V1 results.

**Status:** Complete

**Evidence:** `.planning/phases/05-formal-evidence-readiness/05-VERIFICATION.md`

**Success Criteria**:
1. Formal checkpoint provenance is available and explicit.
2. Dependency snapshot and run provenance are archived.
3. Formal replay plan is clear, reproducible, and gated.
4. Formal rows become claim-ready only after artifact and checkpoint gates pass.
5. Formal readiness supports local-only provenance without requiring git updates
   or remote publication.

**Requirements:** MLC-05, ART-02, ART-03

---
*Roadmap updated: 2026-06-14 for local-only/offline execution policy*
