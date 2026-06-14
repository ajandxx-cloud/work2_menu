# Phase 9: DSPO Family Full Run - Context

**Gathered:** 2026-06-14T20:03:59.5478499+08:00
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 9 runs and gates the DSPO family clip/wide configurations under the
same paired replay contract as the passed Phase 8 baseline validation. It
should add explicit DSPO-internal `dspo_clip` and `dspo_wide` policy tags,
execute actual paired replay rows across the Phase 8 formal-equivalent splits,
and produce a Phase 9 JSON/Markdown validation report.

This phase does not rerun Phase 8 baselines in the main manifest, does not
generate publication artifact bundles, does not assert manuscript ranking
claims, and does not use or validate DSPO_PLUS. The user's latest decision is
that DSPO_PLUS has no relationship to this project; any existing DSPO_PLUS
references in planning documents are treated as stale planning residue to be
excluded from Phase 9 and cleaned up later.

</domain>

<decisions>
## Implementation Decisions

### DSPO Clip/Wide Identity

- **D-01:** Add explicit Phase 9 policy tags `dspo_clip` and `dspo_wide`.
  Do not reuse old mainline tags as the paper-facing DSPO clip/wide names.
- **D-02:** Both tags are DSPO-internal variants and must emit
  `method_family=DSPO`.
- **D-03:** Use `policy_tag` to distinguish `dspo_clip` from `dspo_wide`, and
  add or reuse a role such as `comparison_role=dspo_family` so gates and
  reports do not infer purpose only from tag strings.
- **D-04:** Define `clip` and `wide` by DSPO internal service-risk threshold,
  not by time-window mode, candidate-pool size, or DSPO_PLUS semantics.
- **D-05:** Use `dspo_clip` as the stricter DSPO setting with threshold `0.35`.
- **D-06:** Use `dspo_wide` as the looser DSPO setting with threshold `0.45`.
- **D-07:** `dspo_clip` and `dspo_wide` must not inherit, align with, compare
  to, or mention DSPO_PLUS parameters or penalty terms.

### Comparison Bundle Shape

- **D-08:** The Phase 9 primary manifest should contain only `dspo_clip` and
  `dspo_wide`.
- **D-09:** Do not rerun Phase 8 no-pricing or static-pricing baselines inside
  the Phase 9 primary manifest.
- **D-10:** Reuse the five Phase 8 formal-equivalent splits exactly, including
  `seed`, `data_seed`, `data_seed_test`, `uptake_regime`, `home_util`,
  `base_util`, and `incentive_sens`.
- **D-11:** The Phase 9 report may reference the latest passed Phase 8
  validation report and run ID as a cross-run sanity/status reference.
- **D-12:** Any sanity comparison against Phase 8 baselines must be described
  as a gate/status check only, not as same-run formal ranking evidence.

### Pass And Failure Gate

- **D-13:** Any failed, blocked, incomplete, placeholder-only, or contract-only
  DSPO row blocks Phase 9.
- **D-14:** Any checkpoint status other than `loaded`, paired setting drift,
  missing row-v2 field, manifest/hash/provenance anomaly, or opt-out/home/
  meeting-point accounting error blocks Phase 9.
- **D-15:** Every failed row or split must report `reason`, `minimal_fix`, and
  a concrete local `rerun_command`.
- **D-16:** A passed Phase 9 unlocks DSPO result organization and manuscript
  status language only. It does not unlock final ranking claims or language
  such as "DSPO improves over baselines."
- **D-17:** If Phase 9 is blocked, the report must provide a debug handoff and
  stop in a debug-ready state. It should not automatically repair or rerun the
  failure inside this phase.

### Runtime Budget And Outputs

- **D-18:** Use the Phase 8 formal-equivalent lightweight runtime budget rather
  than the heavier `formal_robust_menu` budget.
- **D-19:** Keep menu and candidate parameters aligned with Phase 8, including
  `menu_k=3`, `max_candidates=8`, `menu_exact_threshold=8`, and
  `menu_exact_gap_threshold=8`.
- **D-20:** Keep HGS and replay runtime settings aligned with Phase 8 unless
  planning discovers a direct incompatibility that must be documented.
- **D-21:** Require the same checkpoint/provenance strength as Phase 8:
  `require_checkpoint=true`, `checkpoint_load_status=loaded`, and recorded
  checkpoint path/hash.
- **D-22:** Keep claim-ready status separate from Phase 9 DSPO validation.
  Local provenance blockers may leave `claim_ready=false` even when Phase 9
  DSPO validation passes.
- **D-23:** Generate a Phase 9 JSON validation report and a Phase 9 Markdown
  validation report. Do not generate a new artifact bundle and do not invoke
  claim-ready artifact building for Phase 9 completion.

### Report Language

- **D-24:** Use gate-first report language: `dspo_validation_status`,
  `phase9_gate`, `claim_ready`, Phase 8 baseline reference status, and a short
  sanity summary.
- **D-25:** The report must explicitly state that any sanity comparison is
  status-only and is not a manuscript ranking conclusion.
- **D-26:** If DSPO clip/wide execution and gates pass but sanity comparison
  does not support DSPO advantage over the Phase 8 baselines, Phase 9 may still
  pass. The report must state that ranking sanity did not support an advantage
  conclusion.
- **D-27:** The Phase 9 context and runtime report must state that DSPO_PLUS is
  unrelated to this project and that Phase 9 does not inherit, compare, or
  validate DSPO_PLUS. Existing DSPO_PLUS planning text is a cleanup risk, not a
  Phase 9 objective.
- **D-28:** Include one clear next step in the report: debug handoff if blocked;
  if passed but sanity does not support advantage, proceed only to Phase 11
  status language/risk analysis and do not write a ranking claim.

### the agent's Discretion

The agent may choose exact helper names, report file names, JSON schema field
names, and test file names as long as the implementation preserves the
decisions above, follows existing script-style test patterns, keeps
`work2_coding/` as the runtime root, and does not hand-edit generated rows,
generated tables, generated figures, or claim-ready artifacts.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planning And Prior Decisions

- `.planning/PROJECT.md` - Current milestone scope, runtime root, evidence
  guardrails, and stale DSPO_PLUS references that must not override the latest
  Phase 9 decision.
- `.planning/REQUIREMENTS.md` - EXP-04 and gate requirements relevant to
  executable DSPO clip/wide validation; DSPO_PLUS references are stale for this
  project unless separately cleaned up.
- `.planning/ROADMAP.md` - Phase 9 goal and success criteria; DSPO_PLUS
  roadmap references are stale residue relative to the latest user decision.
- `.planning/STATE.md` - Current project state, Phase 8 release gate status,
  and recent verification commands.
- `.planning/repository_audit.md` - Active `work2_coding/` path mapping and
  stale `ooh_code/` warning.
- `.planning/phases/06-code-and-experiment-audit/06-CONTEXT.md` - Prior audit
  decisions on factual policy classification, pricing modes, and claim gates.
- `.planning/phases/07-model-consistency-repair/07-CONTEXT.md` - Prior MNL,
  method-family, and opt-out accounting contracts. Treat DSPO_PLUS content in
  that file as superseded by the latest Phase 9 user decision.
- `.planning/phases/08-baseline-validation/08-CONTEXT.md` - Locked Phase 8
  baseline semantics, paired replay fairness, and reporting/gate style.
- `.planning/phases/08-baseline-validation/08-SUMMARY.md` - Passed Phase 8 run
  ID and handoff to Phase 9.
- `.planning/phases/08-baseline-validation/08-VERIFICATION.md` - Passed Phase
  8 checks and evidence locations.

### Runtime Contracts And Manifests

- `work2_coding/Src/policy_adapters.py` - Add `dspo_clip` and `dspo_wide`
  tags here, keeping `method_family=DSPO` and excluding DSPO_PLUS semantics.
- `work2_coding/Src/paired_replay.py` - Paired setting resolution, normalized
  row-v2 fields, method construction, row validation, and checkpoint metadata.
- `work2_coding/Src/study_execution.py` - Study execution, completed/blocked
  row handling, checkpoint metadata, and normalized row construction.
- `work2_coding/Src/artifact_status.py` - Claim-ready row classification and
  formal exclusion gates to preserve when validating Phase 9 rows.
- `work2_coding/Src/baseline_validation.py` - Phase 8 validation/report style
  to mirror for Phase 9 row checks, failure records, and manuscript-safe status
  language.
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - DSPO service-guarded menu
  policy behavior, guardrail thresholds, metadata emission, and effective
  pricing/menu behavior.
- `work2_coding/Src/parser.py` - Parser choices and runtime knobs used by
  manifest overrides.
- `work2_coding/Experiments/studies/phase8_baseline_validation.yaml` - Source
  for the Phase 9 split set and lightweight formal-equivalent runtime budget.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Existing formal
  manifest pattern to read only as a schema/reference, not as Phase 9's runtime
  budget.

### Phase 8 Evidence To Reference

- `work2_coding/outputs/studies/phase8_baseline_validation/phase8_baseline_validation-20260614T111317Z-1e1ee9fb` - Latest passed Phase 8 actual replay run.
- `work2_coding/outputs/phase8_baseline_validation/PHASE8_BASELINE_VALIDATION.json` - Latest passed Phase 8 validation report to reference from Phase 9.
- `work2_coding/outputs/phase8_baseline_validation/PHASE8_BASELINE_VALIDATION.md` - Human-readable Phase 8 validation status.

### Tests And Verification Scripts

- `work2_coding/scripts/test_phase8_baseline_validation.py` - Report/gate test
  pattern to adapt for Phase 9.
- `work2_coding/scripts/test_experiment_contracts.py` - Manifest and row-v2
  contract checks to extend for the Phase 9 DSPO manifest.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Paired fairness
  expectations to extend for `dspo_clip`/`dspo_wide`.
- `work2_coding/scripts/test_paired_replay_contract.py` - Row method, pricing,
  product, window, and pairing contract tests.
- `work2_coding/scripts/test_method_family_contract.py` - Existing
  method-family contract checks; update so Phase 9 DSPO tags remain DSPO-only
  and do not depend on DSPO_PLUS.
- `work2_coding/scripts/test_artifact_gates.py` - Artifact eligibility and
  gate checks to preserve.
- `work2_coding/scripts/test_checkpoint_provenance.py` - Checkpoint loaded/hash
  provenance checks.
- `work2_coding/scripts/test_optout_accounting.py` - Opt-out, accepted-home,
  and accepted-meeting-point separation tests.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `policy_adapters.py` already contains the mainline DSPO-side tags and can
  host explicit `dspo_clip`/`dspo_wide` tags.
- `phase8_baseline_validation.yaml` already defines the exact five splits and
  lightweight formal-equivalent runtime budget Phase 9 should reuse.
- `baseline_validation.py` provides a strong local pattern for row validation,
  blocker objects, report JSON/Markdown, claim-ready separation, and rerun
  command wording.
- `paired_replay.py` and `study_execution.py` already emit row-v2 metadata,
  trace hashes, settings hashes, checkpoint status/hash, method family, and
  separated opt-out/home/meeting-point accounting.
- Existing script-style tests under `work2_coding/scripts/test_*.py` can be
  extended without adding a new test framework.

### Established Patterns

- Run commands from `work2_coding/` so imports like `Src.config` resolve.
- Keep experiment execution manifest-driven under
  `work2_coding/Experiments/studies/`.
- Keep generated rows and generated paper-facing artifacts unmodified by hand.
- Distinguish validation gate status from claim-ready artifact status.
- Use JSON plus Markdown phase reports for machine-readable and human-readable
  gate results.

### Integration Points

- Add a Phase 9 study manifest, likely under
  `work2_coding/Experiments/studies/`, with only `dspo_clip` and `dspo_wide`.
- Add or extend a Phase 9 validation helper that consumes normalized rows,
  checks paired split completeness, checkpoint loaded status, row-v2 fields,
  manifest/settings hashes, opt-out/home accounting, and references the latest
  passed Phase 8 report.
- Add a Phase 9 report CLI under `work2_coding/scripts/` that writes JSON and
  Markdown under a Phase 9 output directory.
- Extend focused contract tests for Phase 9 manifest tags, DSPO-only
  method-family metadata, paired fairness, validation report behavior, and
  DSPO_PLUS exclusion.

</code_context>

<specifics>
## Specific Ideas

- Recommended Phase 9 run shape:
  `cd work2_coding; python scripts/run_study.py --study phase9_dspo_family_validation --execute --output-root outputs/studies`
- Recommended Phase 9 report shape:
  `PHASE9_DSPO_FAMILY_VALIDATION.json` and
  `PHASE9_DSPO_FAMILY_VALIDATION.md`.
- Recommended Phase 9 status fields include `dspo_validation_status`,
  `phase9_gate`, `claim_ready`, `phase8_reference_run_id`,
  `phase8_reference_status`, `sanity_status`, and `next_step`.
- Recommended minimum checks include import smoke, Phase 9 validation tests,
  experiment contracts, policy fairness contracts, method-family contracts,
  artifact gates, checkpoint provenance, and opt-out accounting.
- DSPO_PLUS should be explicitly excluded in Phase 9 outputs because the user
  clarified that it has no relationship to this project.

</specifics>

<deferred>
## Deferred Ideas

- Cleaning DSPO_PLUS references from `.planning/PROJECT.md`,
  `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, prior contexts, and any
  runtime contracts is a follow-up documentation/scope cleanup task outside
  the Phase 9 discussion artifact.
- Final manuscript result claims and reviewer-risk synthesis belong to a later
  paper-writing/status phase after the DSPO validation report exists.
- Expanding experiments beyond the Phase 8 lightweight formal-equivalent budget
  belongs in a separate future phase or explicit user request.

</deferred>

---

*Phase: 9-DSPO Family Full Run*
*Context gathered: 2026-06-14T20:03:59.5478499+08:00*
