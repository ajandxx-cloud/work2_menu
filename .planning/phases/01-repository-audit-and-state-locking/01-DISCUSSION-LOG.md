# Phase 1: Repository Audit And State Locking - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-14T22:54:31+08:00
**Phase:** 1-Repository Audit And State Locking
**Areas discussed:** STATE_LOCK 写到多细, 旧 `ooh_code` 地图如何处理, 阻塞项分类标准, Phase 1 允许跑哪些验证命令

---

## STATE_LOCK 写到多细

| Option | Description | Selected |
|--------|-------------|----------|
| 完整状态锁 | 包含运行根、dirty git、测试、manifest、outputs、checkpoint、artifact、阻塞项。 | Yes |
| 最小状态锁 | 只记录 import smoke 和 active runtime root。 | |
| 由 planner 决定 | 后续 planner 自行决定清单粒度。 | |

**User's choice:** 全部按推荐。
**Notes:** 锁定推荐方案：`.planning/STATE_LOCK.md` 应做完整仓库状态快照，作为后续算法变更前的基线。

---

## 旧 `ooh_code` 地图如何处理

| Option | Description | Selected |
|--------|-------------|----------|
| 建立映射表 | 将仍有价值的 `ooh_code/` 引用映射到当前 `work2_coding/` 路径，无法映射的标记 obsolete。 | Yes |
| 只标记过时 | 不逐项映射，只声明旧地图已过时。 | |
| 由 planner 决定 | 后续 planner 自行处理旧地图。 | |

**User's choice:** 全部按推荐。
**Notes:** 锁定推荐方案：旧地图不能覆盖当前文件系统。`work2_coding/Src/Algorithms/DSPO_Menu.py` 当前存在，旧地图中的缺失说法必须重新判定为 stale。

---

## 阻塞项分类标准

| Option | Description | Selected |
|--------|-------------|----------|
| 明确 blocker/warning 分类 | 把 import、checkpoint、readiness、artifact、claim、dirty-git 等分级记录。 | Yes |
| 只列问题清单 | 不做优先级和阻塞分类。 | |
| 由 planner 决定 | 后续 planner 自行分类。 | |

**User's choice:** 全部按推荐。
**Notes:** 锁定推荐方案：把 scientific guardrails 作为命名审计维度，包括 opt-out accounting、paired replay fairness、checkpoint load status、artifact readiness、claim guard state。

---

## Phase 1 允许跑哪些验证命令

| Option | Description | Selected |
|--------|-------------|----------|
| 只跑轻量诊断 | 允许 import smoke 和低成本脚本式契约检查；禁止 formal replay、训练和 artifact 生成。 | Yes |
| 跑完整验证 | 允许执行 formal/pilot/replay/artifact 相关命令。 | |
| 只读不执行任何命令 | 只看文件，不运行 Python 验证。 | |

**User's choice:** 全部按推荐。
**Notes:** 锁定推荐方案：Phase 1 是审计与状态锁，不应制造新的实验结果或论文产物。

---

## the agent's Discretion

- 后续 planner 可以决定 `.planning/STATE_LOCK.md` 的章节组织。
- 后续 planner 可以决定 Phase 1 是一个计划还是多个计划，但必须保持 read-only audit boundary。

## Deferred Ideas

None.
