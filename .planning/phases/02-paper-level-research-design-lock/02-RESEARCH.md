---
phase: 02-paper-level-research-design-lock
status: completed
researched: 2026-06-15T10:26:05+08:00
language: zh-CN
sources:
  - .planning/PROJECT.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
  - .planning/STATE_LOCK.md
  - .planning/research/SUMMARY.md
  - .planning/phases/02-paper-level-research-design-lock/02-CONTEXT.md
  - work2_coding/Src/Algorithms/DSPO_Menu.py
  - work2_coding/Src/policy_adapters.py
  - work2_coding/Src/paired_replay.py
  - work2_coding/Src/study_execution.py
  - work2_coding/Src/artifact_builder.py
  - work2_coding/Src/artifact_status.py
  - work2_coding/Src/manuscript_claims.py
  - work2_coding/Experiments/studies/formal_robust_menu.yaml
  - work2_coding/artifacts/work2_robust_menu/manuscript/method_outline.md
  - work2_coding/artifacts/work2_robust_menu/manuscript/experiment_outline.md
  - work2_coding/artifacts/work2_robust_menu/manuscript/result_outline.md
---

# Phase 2 Research: Paper-Level Research Design Lock

## RESEARCH COMPLETE

本研究只使用仓库内规划、代码、manifest 和既有 artifact 轮廓。未运行正式 replay、未训练 checkpoint、未重建 artifact、未升级 manuscript claim。

## 目标

Phase 2 应把 Work2 从一组实验脚本和状态产物，锁定为一篇面向 TR Part E 的服务菜单优化论文设计。核心产物应是 `.planning/paper/TR_E_RESEARCH_DESIGN.md`，它要在正式实验之前定义问题、服务产品、数学模型骨架、policy comparison、metric gate、claim ladder、表图计划和非声明边界。

## 关键发现

1. 当前项目的 V1 贡献应是 dynamic service menu optimization for many-to-one DRT，而不是 attention、不是 pricing-only extension，也不是旧 TR-C DSPO_PLUS 梯子。
2. 服务产品应定义为 `(meeting point, pickup time window, price)`。Accepted home pickup 可以是一个服务 bundle；outside option 必须是拒绝/流失状态，不应混入 accepted home pickup 或 route service。
3. Phase 2 必须先锁定数学模型骨架：集合与索引、顺序请求、车辆、候选 meeting points、service bundle、菜单决策变量、MNL choice probability、expected profit objective、opt-out/service guardrail、ETA/time-window feasibility、exact/greedy solver。
4. `work2_coding/Src/policy_adapters.py` 已经给出 V1 mainline 七标签：`mainline_no_menu`、`mainline_fixed_menu`、`mainline_random_menu`、`mainline_optimized_m`、`mainline_optimized_mw`、`mainline_optimized_fixed_window`、`mainline_optimized_adaptive`。研究设计应把这些标签解释为主证据链，而不是后续临时挑选对照组。
5. `work2_coding/Src/paired_replay.py` 和 `work2_coding/Src/study_execution.py` 已经把 paired trace、checkpoint metadata、row status、acceptance/opt-out/home/meeting-point accounting 放进 normalized row contract。所有主 claim 都必须绑定这些字段和同 split/seed/request trace 的 paired comparison。
6. `work2_coding/Src/artifact_status.py`、`artifact_builder.py`、`manuscript_claims.py` 已经提供 claim gate 语义：formal/pilot row 必须有 loaded checkpoint provenance、有效 accounting、非 placeholder、claim-ready artifact status 和 claim guard。Phase 2 文档应把这些写成论文声明的硬门槛。
7. `work2_coding/Src/Algorithms/DSPO_Menu.py` 支持 exact enumeration、greedy forward selection、service-constrained expected profit、Lambert-W pricing、ETA/window robustness 和 no-filter diagnostic metadata。论文设计应把 exact 定位为小规模 benchmark，把 greedy 定位为在线可扩展算法，并要求 candidate count、enumerated menu count、build time、gap、overlap 等诊断。
8. 现有 `method_outline.md`、`experiment_outline.md`、`result_outline.md` 可以作为设计文档素材，但当前 artifact README 和 Phase 1 state lock 都说明现有 evidence 不是 claim-ready。Phase 2 不能把它们写成结论，只能写成结构、约束和将来证据需求。

## 推荐设计结构

`.planning/paper/TR_E_RESEARCH_DESIGN.md` 建议包含以下 sections：

1. Paper positioning and contribution boundary
2. Problem setting and service product
3. Mathematical model skeleton
4. Menu optimization and solver definitions
5. V1 comparison family and evidence ladder
6. Claim-to-evidence matrix
7. Metrics and guardrails
8. Table and figure plan
9. Non-claims, diagnostics, and gated optional evidence
10. Downstream phase handoff

## Claim Ladder

Phase 2 应锁定四级 claim ladder，供 Phase 4 和 manuscript gate 使用：

| Level | Meaning | Allowed Manuscript Use |
| --- | --- | --- |
| strong | Optimized adaptive `m+w+p` improves profit-side metrics while preserving or improving service-quality guardrails under paired formal evidence. | Abstract, contribution, conclusion only after gates pass. |
| conditional | Advantage holds in named uptake/ETA/capacity regimes, with explicit failure regimes. | Main results/discussion with conditions. |
| weak-diagnostic | Mechanism evidence is informative but not enough for positive main claim. | Diagnosis, limitations, redesign rationale. |
| unsupported | Evidence fails or is blocked. | Not a positive claim; route to calibration/rerun or reframing. |

## Table And Figure Research Notes

The design should define tables before formal runs so later artifact builders know what evidence to produce:

- Table: policy design and seven-tag family.
- Table: main paired results with profit and service guardrails.
- Table: product and window ablations.
- Table: ETA robustness/no-filter diagnostics.
- Table: exact-vs-greedy computation and quality.
- Table: provenance/status/claim gate.
- Figure: service bundle/menu schematic.
- Figure: profit-service trade-off.
- Figure: acceptance, opt-out, home share, meeting-point uptake.
- Figure: ETA/window feasibility and pruning diagnostics.
- Figure: exact/greedy runtime and gap diagnostics.

## Risks To Preserve

- Dirty git and blocked readiness remain later formal-claim blockers.
- Smoke, pilot blocked, diagnostic, placeholder, or status-only rows cannot support empirical superiority claims.
- No-filter is diagnostic only unless later formal evidence explicitly justifies a stronger role.
- Attention remains V2/diagnostic only for this milestone.
- If strong evidence fails, the project should route to calibrated rerun before writing positive paper claims.

## Planning Recommendation

Create one Phase 2 execution plan that writes `.planning/paper/TR_E_RESEARCH_DESIGN.md` and verifies coverage against `PAPER-01` through `PAPER-05` plus decisions `D-01` through `D-19`. The plan should be documentation-only and must not run heavy experiments, change algorithm behavior, edit generated rows, or modify manuscript claim language.
