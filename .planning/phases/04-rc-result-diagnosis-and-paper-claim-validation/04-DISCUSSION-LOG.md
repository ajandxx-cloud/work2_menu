# Phase 4: RC Result Diagnosis And Paper-Claim Validation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-15T12:22:20+08:00
**Phase:** 4-RC Result Diagnosis And Paper-Claim Validation
**Areas discussed:** Claim 判级规则, Paired 统计呈现口径, Formal run 与 gate 的使用边界, 输出文件结构与下游分叉

---

## Claim 判级规则

| Question | Option | Description | Selected |
|---|---|---|---|
| 中心 claim 的默认门槛是什么？ | A | 严格联合改进：只有 `profit` 和服务质量指标都稳定优于关键基线，才允许 strong claim。 | Yes |
| 中心 claim 的默认门槛是什么？ | B | Profit 优先、服务不恶化：只要利润明显更好，acceptance/opt-out/home share 不明显变差，就可 strong。 | |
| 中心 claim 的默认门槛是什么？ | C | 分层 claim：profit、acceptance、opt-out、meeting-point uptake 分别判级，不强行合成一个总 claim。 | |
| `optimized_adaptive` 输给 `random_menu` 的 profit 均值时怎么处理？ | A | 阻止 universal/strong dominance：明确写成 mixed evidence；可保留服务质量或机制性 claim。 | |
| `optimized_adaptive` 输给 `random_menu` 的 profit 均值时怎么处理？ | B | 看 paired split 是否多数胜出：如果部分 split 有优势，可给 conditional claim。 | Yes |
| `optimized_adaptive` 输给 `random_menu` 的 profit 均值时怎么处理？ | C | 先不定论：Phase 4 只列事实，Phase 5 决定 claim。 | |
| `optimized_adaptive` 与 `optimized_fixed_window` 当前结果完全相同，怎么解释？ | A | 作为重大诊断信号：说明 adaptive window 机制在当前 formal 设置下没有产生可见增量，必须写入诊断。 | Yes |
| `optimized_adaptive` 与 `optimized_fixed_window` 当前结果完全相同，怎么解释？ | B | 作为实现/manifest 核查项：先要求 planner 检查两者是否实际配置不同，再判 claim。 | |
| `optimized_adaptive` 与 `optimized_fixed_window` 当前结果完全相同，怎么解释？ | C | 两者合并为 optimized window family：减少对 fixed/adaptive 差异的单独 claim。 | |
| 如果没有 central strong claim，Phase 4 的结论应该怎么落地？ | A | 进入 Phase 5 校准：按 roadmap，弱/不稳定/不支持则 Phase 5 mandatory。 | |
| 如果没有 central strong claim，Phase 4 的结论应该怎么落地？ | B | 直接改写为 conditional paper：不再追求 strong claim，转成条件性服务菜单设计研究。 | |
| 如果没有 central strong claim，Phase 4 的结论应该怎么落地？ | C | 双路径：先写 failure/reframing guidance，同时建议 Phase 5 是否值得做。 | Yes |

**User's choice:** `1A, 2B, 3A, 4C`
**Notes:** The strong-claim bar is strict, but conditional claim reasoning may use paired split behavior where appropriate.

---

## Paired 统计呈现口径

| Question | Option | Description | Selected |
|---|---|---|---|
| Phase 4 统计主表应该以什么为主？ | A | Paired split differences：每个 split 内比较 `optimized_adaptive - baseline`，再汇总均值/方向。 | Yes |
| Phase 4 统计主表应该以什么为主？ | B | Policy-level aggregate means：先按 policy 汇总均值/标准差，再补充 paired diff。 | |
| Phase 4 统计主表应该以什么为主？ | C | Uptake regime 分层表：先按 low/medium uptake 分开，再在每层内做 paired diff。 | |
| 小样本 5 个 split 时，CI 怎么处理？ | A | 报告 exploratory CI：给均值差、标准差、简单置信区间，但明确是探索性。 | |
| 小样本 5 个 split 时，CI 怎么处理？ | B | 不报告 CI：只报告 paired differences 和方向，避免伪精确。 | Yes |
| 小样本 5 个 split 时，CI 怎么处理？ | C | CI 只放附录：正文用方向和效应量，详细 CI 放诊断附录。 | |
| 指标优先级怎么排？ | A | Profit first, service guardrails second：先 profit/cost，再服务指标。 | |
| 指标优先级怎么排？ | B | Joint scorecard：利润和服务指标并列，不允许单一利润排序掩盖服务退化。 | |
| 指标优先级怎么排？ | C | Claim-specific metric blocks：每个 claim 自带对应指标块，不做统一总排序。 | Yes |
| Uptake regime 怎么呈现？ | A | 必须分 low/medium：如果方向不同，claim 必须降级为 conditional。 | Yes |
| Uptake regime 怎么呈现？ | B | 合并为整体正式结果：regime 只作为解释性附表。 | |
| Uptake regime 怎么呈现？ | C | 只在发现冲突时分层：先合并；冲突再展开。 | |

**User's choice:** `6A, 7B, 8C, 9A`
**Notes:** Small-sample caution is explicit: no CI and no strong significance language.

---

## Formal run 与 gate 的使用边界

| Question | Option | Description | Selected |
|---|---|---|---|
| 35 行 formal run 的身份怎么写？ | A | Formal diagnostic input：可用于 Phase 4 诊断和 claim classification，但不等于 claim-ready manuscript evidence。 | Yes |
| 35 行 formal run 的身份怎么写？ | B | Provisional formal evidence：只要 rows completed/comparable，就可作为初步正式证据。 | |
| 35 行 formal run 的身份怎么写？ | C | Claim-ready only after gates：除非 readiness/artifact/claim guard 全部通过，否则 Phase 4 不基于它判 claim。 | |
| dirty git blocker 怎么影响 Phase 4？ | A | 只限制 claim-ready，不限制诊断：Phase 4 可以诊断结果，但必须标注 provenance blocker。 | |
| dirty git blocker 怎么影响 Phase 4？ | B | 阻止所有 claim classification：dirty git 未解决前只写 blocker，不分类结果。 | Yes |
| dirty git blocker 怎么影响 Phase 4？ | C | 作为敏感性说明：正文里弱化，只在 provenance 表说明。 | |
| 旧的 smoke artifact/claim guard 怎么处理？ | A | 作为历史 gate 状态：只能说明现有 artifact 是 diagnostic，不能替代 formal run 的 Phase 4 诊断。 | |
| 旧的 smoke artifact/claim guard 怎么处理？ | B | 作为 Phase 4 claim guard 起点：Phase 4 直接更新它，直到 claim-ready。 | |
| 旧的 smoke artifact/claim guard 怎么处理？ | C | 忽略旧 artifact：只看 formal normalized rows。 | Yes |
| Phase 4 是否允许生成新的 artifact/claim guard？ | A | 允许生成诊断 artifact：可以从 formal rows 生成诊断表、claim matrix、provenance status，但不能升级 manuscript claim。 | Yes |
| Phase 4 是否允许生成新的 artifact/claim guard？ | B | 不生成 artifact：只写 `.planning/results/RC_FORMAL_DIAGNOSIS.md`。 | |
| Phase 4 是否允许生成新的 artifact/claim guard？ | C | 允许生成 claim-ready artifact：如果诊断发现支持，就直接升级。 | |

**User's choice:** `10A, 11B, 12C, 13A`
**Notes:** Dirty-git provenance makes claim classification blocked/provisional, even if result patterns are analyzed.

---

## 输出文件结构与下游分叉

| Question | Option | Description | Selected |
|---|---|---|---|
| `RC_FORMAL_DIAGNOSIS.md` 的核心结构怎么定？ | A | 先 blocker，再结果诊断：先写 dirty-git/provenance blocker，再写 paired result diagnostics，最后写 claim status。 | Yes |
| `RC_FORMAL_DIAGNOSIS.md` 的核心结构怎么定？ | B | 先结果，再 blocker：让读者先看到实验现象，再说明 claim 受限。 | |
| `RC_FORMAL_DIAGNOSIS.md` 的核心结构怎么定？ | C | 只写 blocker：dirty git 未解决前不展开结果分析。 | |
| Claim matrix 在 dirty git 下怎么呈现？ | A | 暂不分类：只列 planned claims 和 required evidence，不给 strong/conditional/weak/unsupported。 | |
| Claim matrix 在 dirty git 下怎么呈现？ | B | 给 provisional diagnostic classification：可以分类，但每项标注 blocked by provenance。 | Yes |
| Claim matrix 在 dirty git 下怎么呈现？ | C | 只分类 unsupported：能明确不支持的 claim 先判掉，其余 pending。 | |
| Phase 5 gate 建议怎么写？ | A | 默认 Phase 5 mandatory：因为 strong central claim 尚未成立且 dirty git 阻断 claim classification。 | |
| Phase 5 gate 建议怎么写？ | B | 条件建议：如果 provenance cleanup 后 paired 诊断仍混合，则 Phase 5 mandatory；否则可 skipped-by-gate。 | |
| Phase 5 gate 建议怎么写？ | C | 直接给双路径：写明先 cleanup/rebuild gate，再按诊断决定 Phase 5 mandatory 或 paper reframing。 | Yes |
| Phase 4 允许 planner 做到什么程度？ | A | 只规划诊断，不修代码：planner 只生成诊断/表格/文档计划，不改 runtime 行为。 | Yes |
| Phase 4 允许 planner 做到什么程度？ | B | 可以加诊断脚本：允许新增只读分析脚本，从 formal rows 生成 paired tables 和 markdown。 | |
| Phase 4 允许 planner 做到什么程度？ | C | 可以修 artifact gate：如果发现 claim guard 不适配 formal rows，可以改 builder/gate 逻辑。 | |

**User's choice:** `14A, 15B, 16C, 17A`
**Notes:** The final context write was approved with option `18A`.

---

## The Agent's Discretion

- Exact section headings and table formats for `RC_FORMAL_DIAGNOSIS.md`.
- Exact wording of provisional diagnostic claim labels, while respecting the dirty-git blocker.
- Whether diagnostic evidence is rendered as Markdown-only tables or separate diagnostic artifacts.

## Deferred Ideas

None - discussion stayed within Phase 4 scope.
