# Phase 2: Paper-Level Research Design Lock - Context

**Gathered:** 2026-06-15T10:19:09+08:00
**Status:** Ready for planning
**Language:** Chinese user-facing workflow; technical paths and commands stay in English.

<domain>
## Phase Boundary

Phase 2 turns the current Work2 project into a TR Part E paper research design,
not an experiment-script collection. It should produce
`.planning/paper/TR_E_RESEARCH_DESIGN.md` with a paper-level problem
definition, service-product definition, mathematical model skeleton,
claim-to-evidence map, main table/figure plan, and non-claim boundaries.

This phase is documentary and design-locking. It must not run formal replay,
train checkpoints, tune parameters, edit generated evidence rows, regenerate
paper artifacts, upgrade manuscript claims, or change algorithm behavior.

</domain>

<decisions>
## Implementation Decisions

### Central Paper Story And Claim Ladder
- **D-01:** Use a strong-claim reserved framing. The paper design may be
  organized around a possible central advantage claim for optimized adaptive
  `m+w+p` service menus, but it must explicitly gate any conclusion on formal
  readiness, paired formal rows, artifact status, and claim guard approval.
- **D-02:** Do not present current smoke, pilot, diagnostic, blocked,
  placeholder, or status-only outputs as empirical superiority evidence.
- **D-03:** Use a four-level claim ladder for Phase 4 and manuscript gating:
  `strong`, `conditional`, `weak-diagnostic`, and `unsupported`.
- **D-04:** A strong central claim means profit-service-quality joint
  improvement, not net-profit dominance alone. `mainline_optimized_adaptive`
  must improve profit-side metrics while preserving or improving service
  dimensions such as acceptance, opt-out, home/home-only share, non-home uptake,
  and service guardrail behavior.
- **D-05:** If formal evidence does not support the strong central claim, do
  not keep writing or upgrading the paper claim. Stop manuscript-claim
  progression and route to Phase 5's pre-registered calibration and experiment
  rerun path before deciding whether to resume paper writing.

### Mathematical Model Skeleton
- **D-06:** Phase 2 must produce a complete paper-level mathematical skeleton,
  not only prose. It must include sets and indices, sequential requests,
  vehicles, candidate meeting points, service bundles, menu decision variables,
  MNL choice probability, expected-profit objective, opt-out/service guardrails,
  ETA/time-window feasibility, and exact/greedy solver definitions.
- **D-07:** Define a displayed service bundle as `(meeting point, pickup time
  window, price)`, while allowing accepted home pickup as a service bundle.
- **D-08:** The outside option is not a service bundle. It is a refusal or
  lost-demand state in the choice set and opt-out accounting, and it must not
  enter accepted service or route service.
- **D-09:** Pickup time window is a core service-bundle dimension. The model
  must include ETA/window feasibility or risk treatment, and the no-filter
  setting must remain diagnostic only.
- **D-10:** Define exact menu optimization as the small-scale benchmark and
  greedy forward selection as the online scalable algorithm. Require
  diagnostics such as candidate count, enumerated menu count, build time, exact
  gap, and overlap where available.

### Claim-To-Evidence Map
- **D-11:** Map the central claim to the full seven-tag mainline family:
  `mainline_optimized_adaptive` versus `mainline_no_menu`,
  `mainline_fixed_menu`, `mainline_random_menu`, `mainline_optimized_m`,
  `mainline_optimized_mw`, and `mainline_optimized_fixed_window`.
- **D-12:** Use profit primary plus service guardrails. Primary profit metrics
  include `net_profit`, `adjusted_profit`, and
  `service_constrained_net_profit`; claim constraints include
  `acceptance_rate`, `opt_out_rate`, `home_only_share`, `non_home_uptake`, and
  service guardrail behavior.
- **D-13:** All main claims require paired replay evidence with the same split,
  seed/request trace, checkpoint provenance, pricing settings, routing/HGS
  settings, and reported paired differences.
- **D-14:** Unsupported claims cannot enter manuscript positive claims,
  including the abstract, introduction contributions, or conclusion. They may
  appear only in diagnosis, limitations, or experimental-redesign rationale.

### Tables, Figures, And Non-Claims
- **D-15:** Phase 2 must define a complete paper table plan, including
  experimental design, policy comparison, main paired results, product/window
  ablation, ETA robustness, exact-vs-greedy, and provenance/status tables.
- **D-16:** Phase 2 must define mechanism, result, and diagnostic figure
  families: service-menu framework or bundle schematic, profit-service
  tradeoff, acceptance/opt-out behavior, ETA/risk filtering, and exact-greedy
  computation diagnostics.
- **D-17:** Attention remains V2/diagnostic only. It does not enter the V1 main
  contribution unless a later phase explicitly changes scope with independent
  evidence.
- **D-18:** No-filter remains diagnostic, upper-bound, or stress-test evidence
  only, not an operational recommendation.
- **D-19:** A real or semi-real case study is optional and gated by Phase 6
  feasibility. Phase 2 must not pre-commit it to the main paper or appendix.

### The Agent's Discretion
- The planner may choose the exact section structure, symbol names, and table
  or figure labels for `.planning/paper/TR_E_RESEARCH_DESIGN.md`, as long as
  all decisions above are represented.
- The planner may include concise manuscript-facing prose, but must keep
  empirical claim language conditional on later evidence gates.
- The planner may decide whether to include a compact claim matrix or a longer
  claim-to-evidence table, provided every planned claim maps to policies,
  metrics, and required artifacts.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Planning State
- `.planning/PROJECT.md` - Project purpose, active runtime root, core value,
  and research guardrails.
- `.planning/REQUIREMENTS.md` - Phase 2 requirements `PAPER-01` through
  `PAPER-05`.
- `.planning/ROADMAP.md` - Phase 2 scope, success criteria, and global gate
  rules for claims, calibration, case study, and sensitivity.
- `.planning/STATE.md` - Current GSD state and current focus on Phase 2.
- `.planning/STATE_LOCK.md` - Phase 1 baseline, active runtime confirmation,
  artifact/readiness status, blockers, stale path mapping, and claim limits.
- `.planning/research/SUMMARY.md` - TR-E service-menu optimization framing and
  scientific boundary.
- `AGENTS.md` - Repository-level instructions, runtime assumption, research
  guardrails, and verification baseline.

### Prior Phase Context
- `.planning/phases/01-repository-audit-and-state-locking/01-CONTEXT.md` -
  Decisions about active runtime root, stale `ooh_code/` handling, blocker
  classification, opt-out accounting, paired replay fairness, and checkpoint
  provenance.
- `.planning/phases/01-repository-audit-and-state-locking/01-SUMMARY.md` -
  Phase 1 completion summary and audit outcome.
- `.planning/phases/01-repository-audit-and-state-locking/01-VERIFICATION.md`
  - Verification record for Phase 1.

### Active Runtime And Evidence Contracts
- `work2_coding/Src/Algorithms/DSPO_Menu.py` - Active robust/menu algorithm
  module and exact/greedy menu optimization behavior.
- `work2_coding/Src/policy_adapters.py` - Seven-tag mainline policy family
  and policy adapter contract.
- `work2_coding/Src/paired_replay.py` - Paired replay contract and row fields
  that main claims must rely on.
- `work2_coding/Src/study_execution.py` - Study execution status and metadata.
- `work2_coding/Src/formal_readiness.py` - Formal readiness checks and
  claim-ready blockers.
- `work2_coding/Src/artifact_builder.py` - Artifact generation contract for
  paper-facing tables, figures, and summaries.
- `work2_coding/Src/artifact_status.py` - Artifact status classification.
- `work2_coding/Src/manuscript_claims.py` - Claim guard and manuscript-frame
  logic.

### Manifests And Existing Paper Outlines
- `work2_coding/Experiments/studies/smoke_robust_menu.yaml` - Smoke contract
  for the seven-tag family.
- `work2_coding/Experiments/studies/pilot_robust_menu.yaml` - Pilot
  robust-menu family and checkpoint provenance expectations.
- `work2_coding/Experiments/studies/formal_robust_menu.yaml` - Formal
  robust-menu family, checkpoint requirements, paired fields, required
  metadata, and status fields.
- `work2_coding/artifacts/work2_robust_menu/manuscript/method_outline.md` -
  Existing method outline for service bundles, menu decision, robust windows,
  choice/pricing, and solver.
- `work2_coding/artifacts/work2_robust_menu/manuscript/experiment_outline.md`
  - Existing experiment outline for scenarios, baselines, metrics, paired
  replay, checkpoints, and uptake regimes.
- `work2_coding/artifacts/work2_robust_menu/manuscript/result_outline.md` -
  Existing result outline and current non-claim evidence status.
- `work2_coding/artifacts/work2_robust_menu/README.md` - Current robust-menu
  artifact bundle status.

### Focused Test Scripts For Later Phases
- `work2_coding/scripts/test_optout_accounting.py` - Opt-out accounting
  contract.
- `work2_coding/scripts/test_paired_replay_contract.py` - Paired replay
  contract.
- `work2_coding/scripts/test_policy_fairness_contract.py` - Policy-family
  fairness and paired settings.
- `work2_coding/scripts/test_artifact_gates.py` - Artifact gate behavior.
- `work2_coding/scripts/test_formal_readiness.py` - Formal readiness contract.
- `work2_coding/scripts/test_checkpoint_provenance.py` - Checkpoint
  provenance contract.
- `work2_coding/scripts/test_study_execution_status.py` - Study status and
  blocker row behavior.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `work2_coding/scripts/train_shared_checkpoint.py`: Shared checkpoint
  training entry point; Phase 2 should reference it only as later evidence
  infrastructure, not run it.
- `work2_coding/scripts/check_formal_readiness.py`: Formal readiness wrapper;
  informs the evidence gate language in the research design.
- `work2_coding/scripts/run_study.py`: Manifest study runner for smoke, pilot,
  and formal robust-menu evidence.
- `work2_coding/scripts/build_artifacts.py`: Artifact builder for generated
  tables, figures, aggregate outputs, and status metadata.
- `work2_coding/scripts/build_manuscript_frame.py`: Manuscript-frame builder;
  useful for later paper structure, but Phase 2 should not upgrade claims.
- `work2_coding/artifacts/work2_robust_menu/manuscript/*.md`: Existing outline
  material that can seed the design document, with current status caveats.

### Established Patterns
- The active runtime root is `work2_coding/`; old `.planning/codebase/`
  `ooh_code/` references are historical memory only.
- Study definitions are YAML manifests under `work2_coding/Experiments/`.
- Tests are executable script-style checks under `work2_coding/scripts/test_*.py`.
- Generated evidence has trust levels: raw outputs, artifact snapshots,
  artifact status, and claim guard must not be collapsed into one informal
  "results exist" claim.
- Formal claim language must be gated by readiness, completed paired rows,
  artifact status, and claim guard.

### Integration Points
- `.planning/paper/TR_E_RESEARCH_DESIGN.md` should connect roadmap
  requirements `PAPER-01` through `PAPER-05` to the current runtime contracts,
  seven-tag family, model skeleton, claim matrix, and table/figure plan.
- Later Phase 3 should use the design's claim map to repair and complete the
  formal RC pipeline without changing paper claims by hand.
- Later Phase 4 should classify each planned claim using the four-level claim
  ladder and should stop manuscript-claim progression when strong evidence is
  unsupported.

</code_context>

<specifics>
## Specific Ideas

- The user initially selected the stable conditional framing, then explicitly
  changed the default paper positioning to strong-claim reserved framing.
- The user explicitly chose that if the strong claim is not supported, the
  project should not write the paper anyway; it should redo experiments through
  the calibrated rerun path.
- The service-product definition must make the outside option separate from
  accepted home pickup.
- The paper design should be complete enough that downstream planning does not
  need to re-ask whether to include the mathematical skeleton, claim ladder,
  paired replay requirements, main table/figure plan, attention boundary,
  no-filter boundary, or case-study gate.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within Phase 2 scope.

</deferred>

---

*Phase: 2-Paper-Level Research Design Lock*
*Context gathered: 2026-06-15T10:19:09+08:00*
