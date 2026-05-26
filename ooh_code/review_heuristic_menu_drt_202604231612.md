# 审稿意见（模型：gpt-5.4 / high）

原始主文稿：`manuscript/main.tex`

论文标题：*Heuristic Menu Design for Many-to-One Demand-Responsive Transit: Paired Evaluation and Filtering Diagnostics*

## 总评分

`5/10`

## 摘要评价

这篇论文讨论了一个重要但较少被系统研究的问题：在 many-to-one DRT 中，运营者不仅要决定如何定价和调度，还要决定向乘客展示哪些 meeting-point / pickup-window bundle。论文最有价值的部分是配对评估设计，以及对严格 ETA 过滤会大幅裁剪可行菜单这一机制问题的诊断。然而，当前稿件对“真实世界管理效果”的证据强度仍然表述过强，而且理论贡献的严谨性还不足以支撑现在的 framing。

## 优点

- `1.` 问题定位清晰，抓住了 DRT 运营与乘客侧菜单展示之间的关键接口层，这个切入点有现实意义。
- `2.` 实验设计原则较好：共享训练、冻结评估、相同 request trace、相同初始化，有助于减少评估噪声并隔离 policy effect。
- `3.` 机制层诊断结果很强：严格 ETA filtering 会删除约 `85%–88%` 的可行 bundle，这一点既重要又有实际操作含义。
- `4.` 机制证据与效果证据分层是合理的：把 RC 作为结构/机制 benchmark，把 Austin/Seattle 作为 impact benchmark，这个设计是加分项。
- `5.` 文中已有一定程度的自我克制，承认了城市样本量小、冻结 predictor 的分布漂移、以及方法本质上是 heuristic。
- `6.` 管理启示具有可操作性，“先审计过滤规则，再谈复杂排序优化”比简单宣称某个 heuristic 普遍最优更可信。

## 缺点

- `CRITICAL 1.` 关于真实世界 impact 的论断，证据仍然不够强。
  Austin 和 Seattle 各只有 2 个 split pair，但摘要和结果仍然突出展示 `+32.1`、`+52.0` 这样的利润改善。即便文中说明这些结果只是 descriptive，这样的证据基础仍不足以支撑较强的管理层比较性结论。

- `CRITICAL 2.` 理论贡献的 framing 仍然偏强，超出了目前实际建立的内容。
  论文强调“三层框架”与“Lambert-W pricing adapted to bundle menus”，但核心 policy 明确是 heuristic，pricing 也是带 clipping 的 common-offset heuristic，没有给出最优性、一致性或逼近保证。按现在写法，理论部分更像是合理的工程构造，而不是严格的方法论推进。

- `MAJOR 1.` RC benchmark 在行为上高度退化，限制了性能比较的可解释性。
  Acceptance 约为 `0.11%` 或更低，opt-out 接近 `99.4%–99.6%`。在这种区间内，RC 上的 net-profit 差异很难从行为角度解释，因此 RC 更适合支持 filtering pathology，而不适合作为政策优劣的强证据。

- `MAJOR 2.` 稿件的自洽性和自包含性还不够，读起来仍有“修正版说明文档”的痕迹。
  如 “corrected evaluation pipeline”、“v1 / v2”、“legacy sensitivity analysis” 等表达，暗示读者需要知道前一版稿件或早期 pipeline 的历史，才容易完全理解当前稿件。

- `MAJOR 3.` 符号与方法定义对 ML/OR 读者来说仍然略显不够严密。
  论文包含 surrogate menu objective、outside option、common-offset pricing、predicted cost / ETA / IVT、多种 filtering variant，但这些量之间的依赖关系、定义域以及何时近似、何时精确，还可以更严格。

- `MAJOR 4.` 冻结 predictor 的 paired evaluation 是合理的，但 policy-induced distribution mismatch 分析还不够。
  用 full-display 训练 predictor，再拿它去评估更 selective 的 policies，会改变被展示 bundle 的分布以及最终被接受 bundle 的分布。论文提到了这一点，但目前只是 limitation，分析力度还不够。

- `MINOR 1.` 整体写作是清楚的，但部分 contribution statement 仍偏宽泛。
- `MINOR 2.` “false-negative pruning” 需要更早、更严格地定义。
- `MINOR 3.` 某些数值缺少比例感和规模感，例如 RC 上 `+6.61` 相对于 `-4377.5` 的基线其实非常小。
- `MINOR 4.` 管理含义部分比证据基础更干净，应该更明确强调：城市实验中利润改善并没有伴随 acceptance 改善。

## 对每个 CRITICAL / MAJOR 问题的可执行修改建议

### 对 CRITICAL 1 的建议

- 增加不确定性量化，而不是只报 mean gap。
- 至少补充：
  - split-level 结果
  - confidence interval
  - paired significance test 或非参数检验
  - effect size 的不确定性
- 将城市部分的表述从“v2 remains ahead”进一步收紧成：
  - “在当前有限 rerun 中，v2 在方向上更有利”
- 如果条件允许，实质性增加 Austin / Seattle 的 split pair 数量。

### 对 CRITICAL 2 的建议

两种路线二选一：

- `路线 A：弱化 framing`
  - 明确把方法定位为 heuristic decision architecture
  - 强调其 diagnostic value，而不是理论最优性

- `路线 B：增强理论`
  - 对 Lambert-W pricing 在当前 bundle-MNL 设定下给出更严格的推导
  - 明确哪些步骤是 exact，哪些是 approximation
  - 明确 menu objective 成立所需的假设
  - 若没有保证，就在主文中更显著地说明“无最优性/逼近保证”

### 对 MAJOR 1 的建议

- 把 RC 明确写成 mechanism-stress-test benchmark，而不是 operational-advantage benchmark。
- 在 RC 上：
  - 强化结构性指标
  - 弱化 financial / welfare headline 比较
- 在正文中解释为什么 RC 在 corrected outside-option pipeline 下进入了 degenerate regime。
- 增加至少一个 non-degenerate acceptance benchmark，用于衔接 mechanism 与 impact。

### 对 MAJOR 2 的建议

- 按 stand-alone paper 的标准重写若干表述：
  - 用一两句话明确说明 earlier pipeline 的问题是什么、修正了什么
  - 把 `v1 / v2` 用实质性定义替代版本号叙述
  - legacy 分析放到非常清楚的 appendix 小节，或进一步淡化
  - 确保新读者不需要知道此前手稿历史也能完整理解文章

### 对 MAJOR 3 的建议

- 增加一个更完整的 notation / definition 汇总。
- 明确：
  - candidate set
  - feasible bundle
  - displayed menu
  - outside option utility
  - choice probability
- 全文清晰区分：
  - predicted quantities
  - realized quantities
- 进一步明确：
  - pricing 是 per-bundle、per-menu，还是 shared-offset approximation
  - exhaustive subset enumeration 在什么条件下触发
  - greedy search 在什么条件下触发

### 对 MAJOR 4 的建议

- 增加一组 dedicated robustness study：
  - shared predictor evaluation vs. policy-specific retraining
- 至少在部分实例上比较：
  - 排名是否变化
  - 效果是否稳定
- 如果 retraining 成本过高，则至少增加：
  - predictor 在各 policy 实际 displayed bundle 上的 calibration / error 诊断

## 可能缺失或应更显式强调的参考文献

- `Classical MNL assortment optimization / revenue management`
  - Talluri and van Ryzin
  - Rusmevichientong, Shen, and Shmoys

- `Discrete choice foundations`
  - Ben-Akiva and Lerman

- `Contextual / personalized assortment or learning-to-assort`
  - 可帮助加强“predicted attributes + dynamic candidates”这一定位

- `Meeting-point / stop aggregation in ride-pooling or DRT`
  - 应更明显地与共享接驳点、meeting point 相关文献衔接

- `Dial-a-ride / DRT surveys`
  - 应更明确用 survey 文献定位 many-to-one DRT 在经典 DARP 与现代 DRT 中的位置

注：如果这些文献已在正文中引用，审稿意见的重点仍是“应让这些文献在 related work 的定位里更显眼”。

## 是否准备好投稿

`Almost`

## 总体判断

这篇论文有一个扎实的核心问题意识，也有一个真正有价值的机制诊断结果；但按当前版本，还不能算完全 ready for submission。若要达到更强的投稿状态，需要：

- 进一步收紧 impact claim
- 增强自包含性
- 在理论贡献上要么更强，要么更谦逊

最现实的路径不是大改实验框架，而是：

- 更谨慎地重写 claim
- 更明确地区分 mechanism vs impact
- 更清楚地把方法定位成 heuristic + diagnostic contribution

