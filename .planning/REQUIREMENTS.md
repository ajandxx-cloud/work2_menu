# Requirements: Work2 TR-E Claim-Ready Manuscript Completion

**Defined:** 2026-06-16
**Core Value:** Produce a credible TR-E manuscript package whose empirical
claims are no stronger than the generated evidence, readiness gates, and strict
`CLAIM_GUARD.json` allow.

## v1 Requirements

### Evidence Boundary

- [x] **EVID-01**: The project reconstructs the exact current workspace,
  artifact, manuscript, and experiment state before any repair, final replay,
  or manuscript writing.
- [x] **EVID-02**: The project records current `CLAIM_GUARD.json`,
  `PACKAGE_STATUS.json`, `PACKAGE_INDEX.json`, and
  `ARTIFACT_TO_SECTION_MAP.json` status using generated files only.
- [x] **EVID-03**: The project identifies every cause of current
  `claim_ready=false`, grouped into provenance/readiness,
  empirical-performance, artifact-packaging, manuscript-language, case-study,
  and computational-tractability blockers.
- [x] **EVID-04**: The project states whether a claim-ready path is feasible
  or whether only diagnostic manuscript writing is feasible from current
  evidence.

### Gate Decision

- [x] **GATE-01**: The project inspects dirty git state without reverting,
  deleting, stashing, or overwriting unrelated files.
- [x] **GATE-02**: The project documents checkpoint provenance requirements:
  checkpoint path, checkpoint hash, sidecar metadata, and checkpoint load
  status fields.
- [x] **GATE-03**: The project decides whether frozen final settings are valid
  and pre-registered enough to support a legitimate final replay.
- [x] **GATE-04**: The project classifies the manuscript path as claim-ready
  empirical, conditional diagnostic, or not ready, based on evidence rather
  than desired conclusions.

### Final Replay Or Diagnostic Lock

- [ ] **PATH-01**: If a final replay is legitimate, the project runs only
  frozen or explicitly pre-registered final settings without tuning on final
  outputs.
- [ ] **PATH-02**: If a final replay is run, completed, failed, timeout,
  infeasible, blocked, and missing rows are all represented durably.
- [ ] **PATH-03**: If claim-ready evidence is not available, the project locks
  the paper as a conditional diagnostic TR-E manuscript.
- [ ] **PATH-04**: Strict `CLAIM_GUARD.json` output determines the final claim
  ceiling after any artifact regeneration.

### Manuscript Construction

- [ ] **MS-01**: The project creates a full TR-E manuscript draft in Markdown
  or LaTeX, depending on the available source format.
- [ ] **MS-02**: The manuscript uses academic English paragraph prose rather
  than outline fragments in the body.
- [ ] **MS-03**: The manuscript includes Introduction, Literature Review,
  Problem Description, Mathematical Model, Solution Method, Experimental
  Design, Results, Discussion, Conclusion, and Appendix.
- [ ] **MS-04**: Every table and figure has a source artifact path, claim ID,
  claim status, and allowed manuscript use.
- [ ] **MS-05**: The manuscript contains no prohibited positive language unless
  strict claim guard output authorizes that exact claim.

### Submission Readiness

- [ ] **SUB-01**: The project audits novelty, model rigor, empirical
  credibility, claim safety, traceability, reproducibility, English quality,
  and reviewer attack points.
- [ ] **SUB-02**: The project produces a final recommendation:
  submit-ready, revise-before-submission, diagnostic-only but draftable, or not
  ready.
- [ ] **SUB-03**: The final decision answers whether the paper can be submitted
  to TR-E as a claim-ready empirical optimization paper or only as a
  conditional diagnostic service-menu optimization paper.

## v2 Requirements

Deferred until v1 claim path is complete.

- **CASE-EXEC-01**: Execute a reproducible semi-real case study with runtime
  rows, generated artifacts, and claim guard approval.
- **GREEDY-01**: Generate exact-vs-greedy stress evidence that actually
  exercises greedy fallback and records gap/overlap diagnostics.
- **ENV-LOCK-01**: Add a reproducible dependency lock or environment spec for
  final formal reruns.
- **RUNNER-01**: Add a canonical local verification runner for all script-style
  tests.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Hand-editing generated rows, tables, figures, package status, or claim guards | Violates reproducibility and claim traceability. |
| Tuning on final test results to force a desired ranking | Invalidates empirical claims. |
| Removing inconvenient baselines such as random menu | Baselines are part of the scientific comparison. |
| Claiming adaptive-window value while fixed and adaptive outputs remain indistinguishable | Current evidence blocks the increment claim. |
| Treating no-filter variants as recommendations | No-filter is diagnostic unless gates authorize stronger use. |
| Calling scaffold-only case materials validation | No reproducible case rows or real passenger behavior are established. |
| Framing v1 as an attention model paper | Attention-based choice/scoring is out of v1 scope. |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| EVID-01..EVID-04 | Phase 1 | Pending |
| GATE-01..GATE-02 | Phase 2 | Complete |
| GATE-03..GATE-04 | Phase 3 | Pending |
| PATH-01..PATH-04 | Phase 4 | Pending |
| MS-01..MS-05 | Phase 5 | Pending |
| SUB-01..SUB-03 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements regenerated: 2026-06-16*
