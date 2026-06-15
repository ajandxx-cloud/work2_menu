---
phase: 02-paper-level-research-design-lock
status: design-locked
generated: 2026-06-15T10:32:33+08:00
timezone: Asia/Shanghai
language: zh-CN
requirements_covered:
  - PAPER-01
  - PAPER-02
  - PAPER-03
  - PAPER-04
  - PAPER-05
evidence_status: documentary-design-only
claim_gate_boundary: formal claims require passed formal readiness, completed paired formal rows, claim-ready artifact status, and CLAIM_GUARD approval
runtime_root: work2_coding/
primary_artifact: .planning/paper/TR_E_RESEARCH_DESIGN.md
---

# TR Part E Research Design: Dynamic Service Menu Optimization

本文档是 Work2 的论文级研究设计锁定文件。它定义 TR Part E 论文的问题、服务产品、数学模型骨架、主证据链、claim-to-evidence map、表图计划和非声明边界。本文档只做设计锁定, 不运行 formal replay, 不训练 checkpoint, 不重建 artifacts, 不编辑 generated rows, 不升级 manuscript claims, 不改变算法行为。

当前证据状态不是 claim-ready。已有 smoke, pilot, diagnostic, blocked, placeholder, status-only 输出只能说明流程和 schema 可审计, 不能支持 `mainline_optimized_adaptive` 相对基线的经验优越性声明。任何正向实证结论都必须等 Phase 3 formal pipeline 和 Phase 4 claim diagnosis 通过后再进入 manuscript。

## 1. 论文定位和贡献边界

**PAPER-01:** 本文的 V1 贡献定位为 many-to-one DRT 中的 dynamic service menu optimization, 而不是 attention paper, 不是 pricing-only extension, 也不是旧 TR-C DSPO_PLUS ladder。

核心问题是: 对每个顺序到达的 passenger request, 平台在实时路由和容量约束下展示一个有限服务菜单, 菜单项是可接受的服务 bundle。目标是在 paired RC replay 下检验优化的 adaptive `m+w+p` service menu 是否能改善 profit-service-quality trade-off。

V1 主方法是:

```text
mainline_optimized_adaptive
```

它表示 optimized menu, adaptive pickup time window, Lambert-W pricing, product mode `m+w+p`, menu-contract mode `optimized_menu`, and pricing mode `lambertw`。

强声明保留原则:

- **D-01:** 可以把论文组织成 optimized adaptive `m+w+p` service menus 的潜在中心优势声明, 但结论必须被 formal readiness, paired formal rows, artifact status, and claim guard approval 同时门控。
- **D-02:** 不把 smoke, pilot, diagnostic, blocked, placeholder, status-only outputs 当作 empirical superiority evidence。
- **D-04:** strong central claim 必须是 profit-service-quality joint improvement, 不只是 `net_profit` dominance。
- **D-05:** 如果 formal evidence 不支持 strong central claim, 停止 manuscript claim progression, 进入 Phase 5 calibrated rerun path, 而不是继续写强结论。

## 2. 服务产品定义

**PAPER-02:** 展示给乘客的服务 bundle 定义为:

```text
b = (meeting point, pickup time window, price)
```

其中:

- `meeting point`: 可以是 home pickup 或候选 meeting point。accepted home 是一种 accepted service bundle。
- `pickup time window`: 是服务产品的核心维度, 不能被简化成只看 meeting point 或 price。
- `price`: 可以包含 fare, discount, Lambert-W pricing, 或 policy-specific price setting。

Outside option 的定义必须独立:

- **D-07:** displayed service bundle 是 `(meeting point, pickup time window, price)`, accepted home pickup 可以作为 service bundle。
- **D-08:** `outside option` 不是 service bundle。它是 passenger refusal 或 lost-demand state, 不进入 accepted service, route service, accepted home pickup, 或 meeting-point service accounting。
- `count_accepted_home` 和 `count_accepted_meeting_point` 构成 accepted service。
- `count_opted_out` 是拒绝/流失需求, 与 accepted home pickup 分开计算。

因此, 论文中的 acceptance, opt-out, home share, non-home uptake 必须采用同一 accounting boundary:

```text
accepted_count = count_accepted_home + count_accepted_meeting_point
opt_out_rate = count_opted_out / total_choices
home_only_share or home_share = count_accepted_home / total_choices
non_home_uptake or meeting_point_uptake_rate = count_accepted_meeting_point / total_choices
```

## 3. 问题设置

系统是 many-to-one DRT/last-mile service。请求顺序到达, 车辆服务乘客到共同 destination 或核心活动区, 平台在每次请求到达时基于当前 fleet state, candidate meeting points, ETA/window feasibility, capacity, route insertion cost, and pricing policy 选择展示菜单。

研究对象不是离线全局路线优化本身, 而是前端服务菜单决策如何改变乘客选择、服务质量和运营 profit。Route/HGS 设置、pricing 设置、checkpoint provenance 和 replay traces 必须在 policy comparison 中配对一致。

## 4. 数学模型骨架

**PAPER-05** 和 **D-06** 要求本文档锁定完整 paper-level mathematical skeleton。

### 4.1 Sets and Indices

```text
R = {1, ..., T}: sequential passenger requests, indexed by i
V: vehicle set, indexed by v
M_i: candidate meeting points for request i, indexed by m
B_i: feasible service bundles for request i, indexed by b
S: replay splits/scenarios, indexed by s
K: maximum displayed menu size
Omega_i: ETA or operational uncertainty scenarios for request i, indexed by omega
```

每个请求 `i` 到达时, 系统状态为 `x_i`, 包含 fleet routes, capacities, current time, candidate point availability, pricing settings, checkpoint/model state, and request features。

### 4.2 Service Bundle

每个 bundle `b in B_i` 包含:

```text
b = (m_b, w_b, p_b)
```

属性:

- `m_b`: home 或 candidate meeting point。
- `w_b`: pickup time window, 可以是 fixed window 或 adaptive window。
- `p_b`: passenger price 或 discount-adjusted price。
- `eta_b(x_i)`: predicted pickup ETA under current route state。
- `c_b(x_i)`: expected insertion/service cost。
- `q_b(x_i)`: service-quality or risk features, such as lateness or ETA uncertainty。
- `a_b`: accepted outcome type, one of accepted-home or accepted-meeting-point。

Outside option 记为 `0`, 它进入 choice set, 但不属于 `B_i`:

```text
C_i(M_i) = displayed bundles M_i subset B_i plus outside option 0
```

### 4.3 Menu Decision Variable

菜单决策:

```text
y_{ib} in {0,1}
y_{ib} = 1 if bundle b is displayed to request i
```

菜单大小约束:

```text
sum_{b in B_i} y_{ib} <= K
```

Feasibility constraints:

```text
y_{ib} <= route_feasible_{ib}(x_i)
y_{ib} <= capacity_feasible_{ib}(x_i)
y_{ib} <= window_feasible_{ib}(x_i)
y_{ib} <= service_guardrail_feasible_{ib}(x_i)
```

ETA/window feasibility:

- hard filter: `eta_b <= upper(w_b)` and route/capacity feasible。
- calibrated/risk filter: require risk-adjusted ETA to fit the pickup window。
- soft penalty: allow display but penalize ETA risk in objective。
- no-filter diagnostic: disables ETA pruning only; it is diagnostic/upper-bound/stress-test evidence, not an operational recommendation。

This encodes **D-09** and **D-18**.

### 4.4 Passenger Utility and MNL Choice

Passenger utility for displayed bundle `b`:

```text
U_{ib} = alpha_m f_m(m_b, i) + alpha_w f_w(w_b, eta_b, i) + alpha_p p_b
         + alpha_q q_b(x_i) + epsilon_{ib}
```

Outside option utility:

```text
U_{i0} = u_0 + epsilon_{i0}
```

MNL probability:

```text
P_{ib}(M_i) = exp(V_{ib}) / (exp(V_{i0}) + sum_{h in M_i} exp(V_{ih}))
P_{i0}(M_i) = exp(V_{i0}) / (exp(V_{i0}) + sum_{h in M_i} exp(V_{ih}))
```

where `V` is deterministic utility. `P_{i0}` is opt-out probability, not service acceptance probability。

### 4.5 Expected Profit Objective

For one request, expected platform objective:

```text
max_{M_i subset B_i, |M_i| <= K}
  sum_{b in M_i} P_{ib}(M_i) * [revenue_b - operating_cost_b - discount_b]
  - P_{i0}(M_i) * opt_out_penalty
  - eta_risk_penalty(M_i)
  - service_guardrail_penalty(M_i)
```

Primary profit-side metrics:

- `net_profit`
- `adjusted_profit`
- `service_constrained_net_profit`

Service guardrails:

- `acceptance_rate`
- `opt_out_rate`
- `home_only_share`
- `non_home_uptake` / `meeting_point_uptake_rate`
- service guardrail behavior and row/status validity

This implements **D-12**.

### 4.6 Exact and Greedy Solvers

**D-10:** exact menu optimization is the small-scale benchmark; greedy forward selection is the online scalable algorithm。

Exact enumeration:

```text
M_i^exact = argmax objective(M) over all M subset B_i, |M| <= K
```

It is used only when candidate count is small enough. Required diagnostics:

- candidate count
- enumerated menu count
- exact build time
- exact objective value
- selected menu composition

Greedy forward selection:

```text
M_0 = empty
for step in 1..K:
  add bundle b that gives the largest positive marginal objective gain
```

Required diagnostics:

- greedy build time
- relative optimality gap when exact benchmark exists
- overlap with exact selection
- fallback reason when exact is infeasible

## 5. V1 Evidence Family

**D-11:** central claim must map to the full seven-tag mainline family:

| Role | Policy tag | Purpose |
| --- | --- | --- |
| Baseline | `mainline_no_menu` | default home product plus outside option |
| Baseline | `mainline_fixed_menu` | fixed menu contract |
| Baseline | `mainline_random_menu` | random menu baseline |
| Product ablation | `mainline_optimized_m` | optimized meeting-point dimension only |
| Product ablation | `mainline_optimized_mw` | optimized meeting point plus pickup window |
| Window ablation | `mainline_optimized_fixed_window` | optimized menu with fixed pickup window |
| Primary method | `mainline_optimized_adaptive` | optimized adaptive `m+w+p` service menu with Lambert-W pricing |

Formal evidence must use the manifest family anchored in `work2_coding/Experiments/studies/formal_robust_menu.yaml` and downstream normalized rows. The seven policy tags must share split/request traces, seeds, checkpoint provenance, pricing settings, routing/HGS settings, and manifest/settings hashes.

## 6. Evidence Tiers and Non-Claims

**PAPER-04:** V1 evidence, V2 diagnostics, appendix evidence, and non-claims are separate.

| Evidence class | Allowed use | Boundary |
| --- | --- | --- |
| V1 main evidence | Central TR-E service-menu claims after gates pass | formal paired rows plus claim-ready artifacts required |
| V1 ablation evidence | Explain product, window, ETA, and solver mechanisms | must remain tied to paired metrics and gates |
| V2 attention diagnostics | Appendix or future work only | **D-17:** attention is not V1 main contribution |
| No-filter diagnostics | Stress test, upper bound, or diagnostic contrast | **D-18:** not operational recommendation |
| Smoke evidence | Contract/schema smoke | no empirical superiority claim |
| Pilot evidence | Debug/calibration signal | no formal claim unless gates explicitly allow |
| Status/blocked/placeholder rows | Readiness diagnosis | cannot support positive manuscript claims |
| Case study | Optional Phase 6 gated extension | **D-19:** not pre-committed as main evidence |

Unsupported claims may appear only in diagnosis, limitations, or redesign rationale. This implements **D-14**.

## 7. Claim Ladder

**D-03:** Phase 4 and manuscript gating use this four-level ladder:

| Level | Meaning | Allowed manuscript use |
| --- | --- | --- |
| `strong` | `mainline_optimized_adaptive` improves profit-side metrics while preserving or improving service-quality guardrails under paired formal evidence | Abstract, contribution, conclusion only after all gates pass |
| `conditional` | Advantage holds in named uptake, ETA, capacity, or guardrail regimes, with explicit failure regimes | Main results and discussion with conditions |
| `weak-diagnostic` | Mechanism evidence is informative but insufficient for positive central claim | Diagnosis, limitations, redesign rationale |
| `unsupported` | Evidence fails, is blocked, or does not pass artifacts/claim guard | Not a positive claim; route to Phase 5 calibration/rerun or reframing |

Strong central claim test:

```text
profit-side improvement AND service-quality non-degradation or improvement
```

Profit improvement alone is insufficient if `acceptance_rate`, `opt_out_rate`, `home_only_share`, `non_home_uptake`, or service guardrails deteriorate beyond documented tolerance.

## 8. Claim-to-Evidence Matrix

**PAPER-03:** every planned claim maps to policy comparisons, metrics, artifacts, and gates.

| Claim ID | Type | Comparison | Required metrics | Required artifacts/gates | Allowed use |
| --- | --- | --- | --- | --- | --- |
| C1 | central | `mainline_optimized_adaptive` vs all six mainline baselines | `net_profit`, `adjusted_profit`, `service_constrained_net_profit`, `acceptance_rate`, `opt_out_rate`, `home_only_share`, `non_home_uptake` | passed formal readiness, completed paired formal rows, loaded checkpoint, artifact status `claim_ready`, `CLAIM_GUARD.json` approval | positive main claim only if `strong` or `conditional` |
| C2 | product ablation | `mainline_optimized_adaptive` vs `mainline_optimized_m`, `mainline_optimized_mw` | profit metrics plus uptake and opt-out metrics | same split/seed/request trace, same pricing/routing settings, source artifact path | mechanism claim |
| C3 | window ablation | `mainline_optimized_adaptive` vs `mainline_optimized_fixed_window` | profit metrics, acceptance, opt-out, ETA/window diagnostics | paired formal or declared diagnostic rows, filter-mode provenance | mechanism or conditional robustness claim |
| C4 | menu construction | optimized menus vs fixed/random/no-menu | menu composition, acceptance, opt-out, non-home uptake, service guardrail behavior | normalized rows and artifact status | main or mechanism claim depending on gates |
| C5 | ETA robustness | hard/calibrated/soft modes vs no-filter diagnostic | pruning behavior, ETA risk, service outcomes, profit-service tradeoff | no-filter clearly labeled diagnostic | diagnostic/robustness only unless later gates upgrade |
| C6 | exact-vs-greedy | exact small candidate sets vs greedy large candidate sets | build time, candidate count, enumerated menu count, exact gap, overlap | solver diagnostics table and figure | computational credibility claim |
| C7 | provenance/status | claim-ready rows vs blocked/diagnostic/status rows | row status, checkpoint load status, artifact status, claim guard state | `FORMAL_READINESS.json`, `ARTIFACT_STATUS.json`, `CLAIM_GUARD.json` | reproducibility and limitation claim |

All positive claims require **D-13:** paired replay evidence with same split, seed/request trace, checkpoint provenance, pricing settings, routing/HGS settings, and paired differences.

## 9. Metrics and Guardrails

Primary profit metrics:

- `net_profit`
- `adjusted_profit`
- `service_constrained_net_profit`

Service-quality metrics:

- `acceptance_rate`
- `opt_out_rate`
- `home_only_share` / `home_share`
- `non_home_uptake` / `meeting_point_uptake_rate`
- `served_rate`
- service guardrail status

Provenance and validity fields:

- `policy_tag`
- `split_id`
- `seed`
- request trace identifier or paired trace metadata
- `checkpoint_load_status`
- `checkpoint_path`
- `checkpoint_hash`
- `checkpoint_required`
- row `status`
- `placeholder_only`
- artifact source path
- artifact status and claim guard decision

Solver and feasibility diagnostics:

- `menu_k`
- candidate count
- enumerated menu count
- menu build time
- exact-vs-greedy relative gap
- exact/greedy overlap
- ETA filter mode
- no-filter diagnostic flag

## 10. Required Tables

**D-15:** table plan is locked before formal experiments.

| Table | Purpose | Source evidence |
| --- | --- | --- |
| T1 Policy design and seven-tag family | Define each mainline policy and its product/window/pricing/menu mode | `policy_adapters.py`, `formal_robust_menu.yaml` |
| T2 Main paired results | Compare profit and service guardrails for seven mainline tags | formal normalized rows and paired differences |
| T3 Product and window ablations | Decompose `m`, `m+w`, `m+w+p`, fixed vs adaptive window | formal or explicitly diagnostic ablation rows |
| T4 ETA robustness and no-filter diagnostics | Show filter/risk behavior without recommending no-filter | diagnostic rows with filter provenance |
| T5 Exact-vs-greedy computation | Report candidate count, enumerated count, build time, gap, overlap | solver diagnostics from rows/artifacts |
| T6 Provenance/status/claim gate | Show row status, checkpoint status, artifact status, claim guard | readiness JSON, `ARTIFACT_STATUS.json`, `CLAIM_GUARD.json` |

Paper-facing tables must be generated from rows and artifact builders only. No generated result rows or tables may be hand-edited.

## 11. Required Figures

**D-16:** mechanism, result, and diagnostic figure families:

| Figure | Purpose | Source evidence |
| --- | --- | --- |
| F1 Service-menu schematic | Show `(meeting point, pickup time window, price)`, accepted home, meeting-point service, outside option | design diagram from model contract |
| F2 Profit-service tradeoff | Plot profit-side metrics against acceptance/opt-out or service guardrail metrics | claim-ready rows only for main result use |
| F3 Acceptance and opt-out behavior | Compare `acceptance_rate`, `opt_out_rate`, home share, non-home uptake | normalized rows and artifact builder |
| F4 ETA/risk filtering diagnostics | Show pruning/risk/filter effects and no-filter status | diagnostic/filter rows |
| F5 Exact-greedy diagnostics | Show runtime/gap/overlap as candidate count grows | solver diagnostic rows |

Paper-facing figures must be generated from rows and artifact builders only. Placeholder or no-data figures are status artifacts, not empirical result figures.

## 12. Downstream Handoff

Phase 3 should use this design to repair and complete the formal RC pipeline:

- inspect `formal_robust_menu.yaml` and related manifests;
- verify or generate required shared checkpoint;
- run formal readiness without bypassing blockers;
- run formal paired replay and write comparable normalized rows;
- build claim-ready artifacts only after readiness and row gates pass.

Phase 4 should use the claim ladder and claim matrix:

- compute paired differences by split and uptake regime;
- report means, standard deviations, effect sizes, and confidence intervals where feasible;
- avoid strong significance language if seed count is too small;
- classify each claim as `strong`, `conditional`, `weak-diagnostic`, or `unsupported`;
- route unsupported strong claim attempts to Phase 5 calibration/rerun before manuscript claim progression.

Phase 5 and later phases remain gated. Case study work is optional and must wait for Phase 6 feasibility; sensitivity and exact-vs-greedy expansion should follow the roadmap gates, not ad hoc manuscript pressure.

## 13. Decision Coverage Checklist

- **D-01:** strong-claim reserved framing with formal gates.
- **D-02:** smoke/pilot/diagnostic/blocked/placeholder/status outputs are not empirical superiority evidence.
- **D-03:** four-level claim ladder defined.
- **D-04:** strong central claim requires profit-service-quality joint improvement.
- **D-05:** unsupported strong evidence routes to Phase 5 calibration/rerun.
- **D-06:** mathematical skeleton includes sets, requests, vehicles, candidate points, bundles, menu variables, MNL, objective, guardrails, ETA/window feasibility, exact/greedy solvers.
- **D-07:** displayed service bundle is `(meeting point, pickup time window, price)` and accepted home is allowed as a service bundle.
- **D-08:** outside option is separate refusal/lost-demand state.
- **D-09:** pickup time window and ETA/window feasibility are core dimensions; no-filter is diagnostic.
- **D-10:** exact small-scale benchmark and greedy online algorithm are defined with diagnostics.
- **D-11:** full seven-tag mainline family is mapped.
- **D-12:** profit primary plus service guardrail metrics are listed.
- **D-13:** paired replay requirements are explicit.
- **D-14:** unsupported claims are blocked from positive manuscript sections.
- **D-15:** table plan is defined.
- **D-16:** figure plan is defined.
- **D-17:** attention remains V2/diagnostic only.
- **D-18:** no-filter remains diagnostic, upper-bound, or stress-test only.
- **D-19:** real/semi-real case study is optional and Phase 6 gated.

## 14. Requirement Coverage

- **PAPER-01:** TR Part E dynamic service-menu optimization contribution boundary is defined.
- **PAPER-02:** service bundle, accepted home, outside option, and opt-out accounting semantics are defined.
- **PAPER-03:** every planned claim maps to policy comparisons, metrics, artifacts, and gates.
- **PAPER-04:** V1 main evidence, V2 attention diagnostics, appendix/diagnostic evidence, and non-claims are separated.
- **PAPER-05:** mathematical model skeleton includes sets/indices, service bundles, menu variables, utility and MNL probability, expected-profit objective, guardrails, ETA/time-window feasibility, exact solver, and greedy solver.

## 15. Closeout Boundary

This design intentionally does not claim that `mainline_optimized_adaptive` is superior. It defines what evidence would be required to make, narrow, reject, or reframe that claim. The safe current statement is:

> The implementation and experiment pipeline support paired comparison of service-menu policies and artifact-gated reporting, but formal empirical superiority claims remain blocked until readiness, formal replay, artifact status, and claim guard gates pass.
