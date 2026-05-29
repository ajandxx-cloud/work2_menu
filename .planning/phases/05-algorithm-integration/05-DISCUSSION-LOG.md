# Phase 5: Algorithm Integration - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-29
**Phase:** 05-algorithm-integration
**Areas discussed:** 预测→菜单流程, 训练数据与 Huber loss, ETA/IVT 来源, Config/Parser 配置

---

## 预测→菜单流程 (Prediction-to-Menu Flow)

### Q1: CNNSetMenuNet 预测是否走 theta-blending？

| Option | Description | Selected |
|--------|-------------|----------|
| 保留 theta blending（推荐） | blended = (1-θ)*插入成本 + θ*模型预测，θ 退火。训练初期安全网，与其他方法公平比较 | ✓ |
| 直接使用模型预测 | 不走 blending，模型预测直接作为成本信号。训练初期风险大 | |
| 退火到纯模型预测 | 本质等同于选项 1（现有 theta 机制已做退火） | |

**User's choice:** 保留 theta blending（推荐）
**Notes:** 理由充分：(1) 训练初期安全网，(2) 公平比较，(3) 退火机制已存在

### Q2: 候选构建流程如何适配？

| Option | Description | Selected |
|--------|-------------|----------|
| 重写候选构建流程（推荐） | 一次性构建 option features → 一次性调用模型 → 使用全部 K 个预测 | ✓ |
| 保持逐候选循环 | 每次只传 K=1 给 CNNSetMenuNet。失去集合注意力优势 | |

**User's choice:** 重写候选构建流程（推荐）
**Notes:** 自然利用模型联合预测能力，集合注意力看到所有候选间关系

---

## 训练数据与 Huber Loss (Training Data Format)

### Q3: 每次转换存储什么？

| Option | Description | Selected |
|--------|-------------|----------|
| 完整 K 候选转换（推荐） | (grid, aux, option_features[K,6], mask[K], true_costs[K])。保留集合结构 | ✓ |
| 拆成单候选粒度 | 每次存一个 (grid, aux, feat[6], cost)。丢失集合结构 | |

**User's choice:** 完整 K 候选转换（推荐）
**Notes:** 与 CNNSetMenuNet 设计匹配，保留候选间关系信息

### Q4: 训练时机？

| Option | Description | Selected |
|--------|-------------|----------|
| Episode 结束时训练（推荐） | done=True 时收集数据并训练，与 CNN_2d 一致 | ✓ |
| 每步训练 | Online learning，频率高但与现有流程差异大 | |

**User's choice:** Episode 结束时训练（推荐）
**Notes:** 保持与现有训练节奏一致

---

## ETA/IVT 来源 (ETA/IVT Source)

### Q5: ETA/IVT 从哪来？

| Option | Description | Selected |
|--------|-------------|----------|
| 纯启发式（推荐） | 用 DSPO_Menu 已有的启发式估算，不增加复杂度 | |
| 保留 CNN_2d 辅助预测 | 冻结 CNN_2d 提供 ETA/IVT，可能更准确但增加复杂度 | ✓ |

**User's choice:** 保留 CNN_2d 辅助预测
**Notes:** 用户选择比推荐方案更积极的路线 — 保留 CNN_2d 作为辅助预测器以获得更好的 ETA/IVT 估计

### Q6: CNN_2d 辅助预测器的状态？

| Option | Description | Selected |
|--------|-------------|----------|
| 冻结 CNN_2d（推荐） | 从 Work 1 检查点加载后冻结，仅 CNNSetMenuNet 可训练 | ✓ |
| 两个模型一起训练 | 复杂度增加，且不是本研究贡献点 | |

**User's choice:** 冻结 CNN_2d（推荐）
**Notes:** CNNSetMenuNet 是唯一可训练模型，CNN_2d 仅提供冻结的 ETA/IVT 预测

---

## Config/Parser 配置 (Config & Parser Wiring)

### Q7: --menu_model 路由机制？

| Option | Description | Selected |
|--------|-------------|----------|
| Config 级路由（推荐） | config.py 根据 --menu_model 选择算法类。清晰简单 | ✓ |
| DSPO_Menu 内部分支 | __init__ 内部检查 config.menu_model。违反单一职责 | |

**User's choice:** Config 级路由（推荐）
**Notes:** config.py 中 `self.algo = CNN_SetMenu if menu_model=='cnn_setmenu' else DSPO_Menu`

### Q8: CNNSetMenuNet 超参数如何配置？

| Option | Description | Selected |
|--------|-------------|----------|
| 内部硬编码默认值（推荐） | d_model=64, nhead=4 等在算法类内部硬编码。MVP 不需要调参 | ✓ |
| Parser 注册全部超参数 | 灵活但增加 CLI 复杂度，MVP 阶段不需要 | |

**User's choice:** 内部硬编码默认值（推荐）
**Notes:** 超参数与 Phase 04 模型设计一致

---

## Claude's Discretion

- Memory buffer 批量处理细节
- 梯度裁剪策略
- 优化器超参数
- Warm-start 检查点路径解析
- CNN_2d 冻结预测器加载时机
- 新增训练转换的具体存储实现

## Deferred Ideas

None — discussion stayed within phase scope.
