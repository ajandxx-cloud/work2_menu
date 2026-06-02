# Requirements: Work2_CNN_SetMenuNet_DRT_Menu_Experiments

**Defined:** 2026-06-01  
**Core Value:** 证明或诚实诊断 CNN-SetMenuNet 是否比传统 CNN-Menu、MLP-Menu、Nearest-L、Cost-L heuristic 等方法更适合 DRT 动态服务菜单设计。

## v1 Requirements

### Planning

- [x] **PLAN-01**: 项目包含独立的 `.planning/PROJECT.md`，明确 Work 2 的研究问题、贡献边界和默认实验设定。
- [x] **PLAN-02**: 项目包含 `.planning/ROADMAP.md`，从 smoke validation 到 formal experiments 拆分清晰 phases。
- [x] **PLAN-03**: 项目包含 `.planning/STATE.md`，记录当前 phase、下一步和验证状态。
- [x] **PLAN-04**: 项目包含 `.planning/research/SUMMARY.md`，总结 `实验讨论5.26.md` 中的研究定位、实验设计和 TR-E 风险。
- [x] **PLAN-05**: 项目包含 `.planning/RESULTS_CONVENTIONS.md`，定义结果目录、CSV schema、seed 命名和 summary markdown 规则。
- [x] **PLAN-06**: 项目包含 `.planning/verification/PHASE_VERIFICATION_TEMPLATE.md`，每个 phase 都能按统一模板出 verification report。

### Boundaries

- [x] **BND-01**: 实施阶段不得修改 Work 1 定价模块核心逻辑，除非用户明确批准。
- [x] **BND-02**: 实施阶段不得修改 MNL 乘客选择模型核心逻辑，除非用户明确批准。
- [x] **BND-03**: 实施阶段不得修改 HGS/Hygese 路径成本评估核心逻辑，除非用户明确批准。
- [x] **BND-04**: Work 2 改动范围限定在候选点评分、菜单选择、候选集合表征和候选特征构造。
- [x] **BND-05**: SPO 或 SPO+ 不作为 Work 2 主贡献和第一版训练目标。

### Model Contract

- [x] **MOD-01**: 候选集合输入支持 `K` 个 meeting points，默认 `K=10`。
- [x] **MOD-02**: 菜单选择输出展示 `L` 个 meeting points，默认 `L=3`，且 `home option` 始终展示。
- [x] **MOD-03**: 第一版监督标签为每个候选点真实边际插入成本。
- [x] **MOD-04**: 第一版训练 loss 为 Huber 或 MSE，不依赖 SPO/SPO+。
- [x] **MOD-05**: CNN-Menu、MLP-Menu、SetMenuNet、CNN-SetMenuNet 使用可比较的候选集合和菜单语义。
- [x] **MOD-06**: CNN-SetMenuNet 的贡献解释为全局状态编码与候选集合关系建模结合，而不是单纯参数量增加。

### Experiments

- [x] **EXP-01**: 提供 RC smoke suite，至少能运行 Nearest-L、Cost-L、CNN-Menu、CNN-SetMenuNet 和 Oracle Menu。
- [ ] **EXP-02**: 主实验比较 Home only、Nearest-L、Cost-L heuristic、Full-candidate CNN、MLP-Menu、CNN-Menu、SetMenuNet、CNN-SetMenuNet、Oracle Menu。
- [ ] **EXP-03**: 主实验使用多 seed，正式默认 seeds 为 `0,1,2,3,4`。
- [ ] **EXP-04**: 主实验默认 `instance=RC`、`K=10`、`L=3`。
- [ ] **EXP-05**: pilot 实验默认 train/test episodes 为 `80/20`。
- [ ] **EXP-06**: formal 实验默认 train/test episodes 为 `150-300/50`。
- [x] **EXP-07**: Robustness 实验覆盖 menu size、candidate pool size、demand intensity、outside option utility 和 cross-instance generalization。

### Metrics And Outputs

- [x] **OUT-01**: 每个实验输出统一 CSV，至少包含 `study`, `method`, `seed`, `instance`, `K`, `L`, `net_profit`, `total_cost`, `quit_rate`, `avg_walk`, `menu_regret`, `top_L_overlap`, `spearman_cost_ranking`, `runtime_per_decision`。
- [ ] **OUT-02**: 每个 study 生成统一 summary markdown，总结设置、指标、主要结果、结论支持度和风险。
- [ ] **OUT-03**: 输出 prediction/ranking metrics，包括 MAE、RMSE、Spearman、Top-L overlap、NDCG@L、menu regret。
- [ ] **OUT-04**: 输出 operational metrics，包括 net profit、total operating cost、travel cost、service cost、discount cost、charge revenue、base revenue、runtime per decision。
- [ ] **OUT-05**: 输出 passenger-experience metrics，包括 quit rate、acceptance rate、meeting-point share、home pickup share、average walking distance、average in-vehicle time、average price/discount。
- [ ] **OUT-06**: Result root 使用 `outputs/work2_cnn_setmenunet/<study>/<run_id>/`，committed summaries 使用 `artifacts/work2_cnn_setmenunet/`。

### Verification

- [x] **VER-01**: 每个 phase 完成后生成 verification report。
- [x] **VER-02**: Verification report 必须说明修改了哪些文件。
- [x] **VER-03**: Verification report 必须说明是否影响 Work 1。
- [x] **VER-04**: Verification report 必须说明是否能运行 smoke test。
- [x] **VER-05**: Verification report 必须说明是否生成预期 CSV。
- [x] **VER-06**: Verification report 必须说明当前结果是否支持论文结论。
- [x] **VER-07**: Verification report 必须说明下一 phase 是否可以推进。
- [ ] **VER-08**: 若结果不支持预期结论，必须生成诊断报告和下一轮调参建议。

## v2 Requirements

### Extended Evidence

- **V2-01**: 加入半真实或真实通勤案例，增强 TR-E 投稿竞争力。
- **V2-02**: 加入 attention 可解释性或候选点替代关系可视化。
- **V2-03**: 加入参数量控制实验，进一步排除“模型更复杂所以更好”的解释。
- **V2-04**: 加入更细的 MNL 参数敏感性实验，包括价格、步行、车内时间敏感度。

## Out of Scope

| Feature | Reason |
|---------|--------|
| SPO/SPO+ main contribution | Work 2 贡献点是 service menu design + set representation learning |
| Routing solver rewrite | HGS/Hygese 是稳定后端评估依赖，本项目不做路径求解器创新 |
| Pricing model rewrite | 动态定价模块保持不动，以隔离菜单表征贡献 |
| Manual result editing | 违反多 seed 可复现研究原则 |
| Candidate filtering / full-display as main narrative | 用户要求按 CNN-SetMenuNet 表征比较全新规划 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLAN-01..PLAN-06 | Phase 1 | Complete |
| BND-01..BND-05 | Phase 1 | Complete |
| EXP-01, OUT-01, VER-01..VER-07 | Phase 2 | Complete |
| MOD-01..MOD-06 | Phase 3 | Complete |
| EXP-02..EXP-06, OUT-02..OUT-05 | Phase 4 | Pending |
| EXP-07 | Phase 5 | Complete |
| OUT-06, VER-08 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 40 total
- Mapped to phases: 40
- Unmapped: 0

---
*Requirements defined: 2026-06-01*  
*Last updated: 2026-06-01 after Phase 3 execution*
