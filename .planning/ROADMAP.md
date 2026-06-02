# Roadmap: Work2_CNN_SetMenuNet_DRT_Menu_Experiments

**Created:** 2026-06-01  
**Mode:** standard research phases  
**Default command after initialization:** `$gsd-plan-phase 1`

## Phase 1: Project Baseline And Boundaries

**Goal:** 建立 Work 2 独立规划基线，明确研究问题、贡献边界、结果规范和验证模板�? 
**Requirements:** PLAN-01..PLAN-06, BND-01..BND-05
**Status:** Complete - 2026-06-01
**Verification:** `.planning/phases/01-project-baseline-and-boundaries/VERIFICATION.md`

**Success Criteria:**
1. `.planning/PROJECT.md`、`.planning/REQUIREMENTS.md`、`.planning/ROADMAP.md`、`.planning/STATE.md` 均存在并与本项目新叙事一致�?2. `.planning/research/SUMMARY.md` 总结 `实验讨论5.26.md` 的核心研究定位、模型路线、实验设计和 TR-E 风险�?3. `.planning/RESULTS_CONVENTIONS.md` 定义 result root、artifact root、CSV columns、seed naming �?summary markdown�?4. `.planning/verification/PHASE_VERIFICATION_TEMPLATE.md` 定义每个 phase �?verification report 必填项�?5. Work 1 保护规则被明确写入规划文档�?
## Phase 2: Smoke Experiment Pipeline

**Goal:** 建立最�?RC smoke suite，确认实验入口、统一 CSV �?summary markdown 能跑通�? 
**Requirements:** EXP-01, OUT-01, VER-01..VER-07
**Status:** Complete - 2026-06-01
**Verification:** `.planning/phases/02-smoke-experiment-pipeline/VERIFICATION.md`

**Success Criteria:**
1. Smoke suite 使用 `instance=RC`、小 episode 数、至少一�?seed�?2. Smoke suite 至少覆盖 Nearest-L、Cost-L、CNN-Menu、CNN-SetMenuNet、Oracle Menu；若 SetMenuNet 可用则一并纳入�?3. 每个 method 都输出统一 CSV 行，包含 required columns�?4. 生成 smoke summary markdown，明确是否支持进�?Phase 3�?5. Phase 2 verification report 说明改动文件、Work 1 影响、smoke test、CSV 生成和下一步状态�?
## Phase 3: Candidate Feature And Label Contract

**Goal:** 锁定候选集合输入、mask、home-option 语义、真实边际插入成本标签和第一版训练目标�? 
**Requirements:** MOD-01..MOD-06
**Status:** Complete - 2026-06-01
**Verification:** `.planning/phases/03-candidate-feature-and-label-contract/VERIFICATION.md`

**Success Criteria:**
1. 明确 `K` �?meeting point candidates �?always-shown home option 的数据流�?2. 明确 `L` 只表�?displayed meeting points，不包含 home�?3. 明确 option feature schema、mask 语义、padding 规则和候选无序集合处理方式�?4. 明确真实边际插入成本标签计算方式，且不改�?HGS/Hygese 核心评估逻辑�?5. 明确 Huber/MSE loss 为第一版目标，SPO/SPO+ 不进入主线�?
**Plans:** 3/3 plans complete

Plans:
- [x] `03-01-PLAN.md` - Wave 1: Lock public K/L/home semantics and home-first option feature tensors. (completed 2026-06-01)
- [x] `03-02-PLAN.md` - Wave 2, blocked on 03-01: Implement candidate-specific labels and mask-aware Huber/MSE losses. (completed 2026-06-01)
- [x] `03-03-PLAN.md` - Wave 3, blocked on 03-01 and 03-02: Verify cross-method comparability, artifact metadata, and Phase 3 closeout. (completed 2026-06-01)

## Phase 4: Model Comparison Suite

**Goal:** 运行 pilot �?seed 模型比较，验�?CNN-SetMenuNet 相对 baseline 的菜单质量、运营绩效和乘客体验�? 
**Requirements:** EXP-02..EXP-06, OUT-02..OUT-05
**Status:** Complete - 2026-06-02
**Verification:** `.planning/phases/04-model-comparison-suite/VERIFICATION.md`

**Plans:** 3/3 plans complete

Plans:
- [x] `04-01-PLAN.md` - Wave 1: Align the Phase 4 pilot manifest and comparability checks. (completed 2026-06-02)
- [x] `04-02-PLAN.md` - Wave 2: Implement Phase 4 pilot summary and diagnostic reporting. (completed 2026-06-02)
- [x] `04-03-PLAN.md` - Wave 3: Run the three-seed pilot, build artifacts, and verify readiness. (completed 2026-06-02)

**Success Criteria:**
1. 主比较覆�?Home only、Nearest-L、Cost-L heuristic、Full-candidate CNN、MLP-Menu、CNN-Menu、SetMenuNet、CNN-SetMenuNet、Oracle Menu�?2. Pilot 使用 `training episodes=80`、`test episodes=20`，并至少覆盖多个 seeds�?3. 输出 prediction/ranking、operational、passenger-experience 三类指标�?4. Summary markdown 判断 CNN-SetMenuNet 是否�?`net_profit`、`menu_regret`、`top_L_overlap`、`quit_rate`、`avg_walk` 上支持论文结论�?5. Phase 4 verification report 明确是否可以进入 formal robustness�?
## Phase 5: Robustness Experiments

**Goal:** 检�?CNN-SetMenuNet 在关键实验维度下是否稳定，而不是只在单一 RC 设置上有效�? 
**Requirements:** EXP-07
**Status:** Blocked - verification gaps found 2026-06-02
**Verification:** `.planning/phases/05-robustness-experiments/VERIFICATION.md`

**Plans:** 3/3 plans complete

Plans:
- [x] `05-01-PLAN.md` - Wave 1: Define Work2 robustness manifests and fast contract checks. (completed 2026-06-02)
- [x] `05-02-PLAN.md` - Wave 2, blocked on 05-01: Build robustness artifact summaries and diagnostic gates. (completed 2026-06-02)
- [x] `05-03-PLAN.md` - Wave 3, blocked on 05-01 and 05-02: Run or resume robustness suite and verify Phase 5 readiness. (completed 2026-06-02)

**Success Criteria:**
1. Menu size 实验覆盖多个 `L` 值，至少包含默认 `L=3`�?2. Candidate pool size 实验覆盖多个 `K` 值，至少包含默认 `K=10`�?3. Demand intensity 实验覆盖低、中、高需求或等价实例设置�?4. Outside option utility 实验覆盖不同竞争强度�?5. Cross-instance generalization 至少覆盖 RC 外的一个实例或数据切分�?
## Phase 6: Formal Results And Diagnostics

**Goal:** 生成正式�?seed 结果、论文表图、summary markdown 和负结果诊断机制�? 
**Requirements:** OUT-06, VER-08

**Success Criteria:**
1. Formal 默认使用 seeds `0,1,2,3,4`，test episodes `50`，training episodes `150-300`�?2. Raw outputs 位于 `outputs/work2_cnn_setmenunet/<study>/<run_id>/`�?3. Committed summaries 位于 `artifacts/work2_cnn_setmenunet/`�?4. 生成主表：Method、Net profit、Total cost、Quit rate、MP share、Avg walk、Menu regret、Top-L overlap、Runtime�?5. �?CNN-SetMenuNet 不支持预期结论，输出 diagnostic report 和下一轮调参建议�?
## Phase Verification Rule

每个 phase 完成后必须生�?verification report，至少回答：

1. 修改了哪些文件？
2. 是否影响 Work 1�?3. 是否能运�?smoke test�?4. 是否生成预期 CSV�?5. 当前结果是否支持论文结论�?6. 下一 phase 是否可以推进�?
## Requirement Coverage

All v1 requirements in `.planning/REQUIREMENTS.md` are mapped to exactly one phase.

---
*Roadmap created: 2026-06-01*
