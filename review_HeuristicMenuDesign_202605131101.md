# Review: Heuristic Menu Design for Many-to-One Demand-Responsive Transit

模型确认：本轮按已确认的 `gpt-5.5 high` 深度审稿口径执行。  
主文稿确认：审稿对象为 `ooh_code/manuscript/main.tex` 及其 `\input{...}` 章节，参考文献为 `ooh_code/manuscript/references.bib`。  
Venue：Transportation Research Part E: Logistics and Transportation Review。

## 1. Overall Score

**5/10，低于弱接收线。**

按“6 = weak accept, 7 = accept”的标准，我目前会给 **5 分**。论文有清楚的运营问题意识和较完整的实验流水线，但作为 TR Part E 投稿，当前版本的核心结论仍过度依赖低样本、校准性和诊断性证据；理论部分也存在 Lambert-W 定价推导与实际目标函数之间的关键断裂。若作者显著收缩贡献表述，并补强需求校准、统计证据和定价推导，论文有机会进入“major revision / borderline weak accept”的区间。

## 2. Summary

本文研究 many-to-one DRT 中“会议点 + 接送时间窗”服务 bundle 的菜单展示问题，将候选生成、MNL 乘客选择、启发式菜单构造和定价层连接起来，并通过配对 replay 实验比较 strict-filter、no-filter、full display 及若干 baseline。论文的主要经验发现是：ETA 预过滤会显著改变候选集合；原始 RC benchmark 因 outside-option 下近乎全体 opt-out 而更适合作机制诊断；在 higher-uptake 校准环境下，简单 flat-markdown pricing 反而优于 Lambert-W-inspired pricing。

整体上，论文的问题选得有应用价值，也比较诚实地承认了启发式和低样本限制。但目前贡献链条较松：理论上没有足够支撑“Lambert-W pricing layer”的方法贡献，实证上 city evidence 只有每城两个 split pair，需求模型也没有外部估计或强 sensitivity 支撑，因此还不足以支撑 TR Part E 级别的主结论。

## 3. Strengths

1. **问题设定有现实运营意义。** 把 DRT 乘客端菜单展示视为运营决策，而不是 UI 细节，这一点对 TR Part E 读者是有吸引力的。

2. **三层结构清楚。** 候选生成、菜单策略、乘客选择的分层表述有助于读者理解各个机制分别影响什么。

3. **配对评估思想合理。** 使用相同 predictor、相同 request traces 和相同 simulator initialization 来隔离 policy 差异，是本文最稳健的方法设计之一。

4. **作者对主张边界已有明显自我修正。** 文中多次承认 RC outside-option benchmark 是 degenerate、城市实验低样本、Lambert-W 是 heuristic 而不是全局最优，这比过度宣称更可信。

5. **诊断指标较丰富。** 除 net profit 外，论文还报告 menu size、home-only menus、FN pruning、acceptance、consumer surplus、boundary-hit rates 等，有利于解释机制而不仅是比较一个总收益数字。

## 4. Weaknesses

### CRITICAL 1. 核心实证证据不足以支撑投稿级主结论

论文当前把贡献建立在三类证据上：RC 机制诊断、higher-uptake RC 行为校准、Austin/Seattle 外部方向性检查。但三者都有限制：RC 原始环境 full-display acceptance 约 0.001，几乎没有真实选择行为；higher-uptake RC 是校准环境，不是外部验证需求模型；Austin 和 Seattle 每城只有 2 个 split pair，只能描述方向，不能提供强统计证据。  

这导致论文最重要的管理结论，例如“no-filter 更优”“flat markdown 更优”“过滤层是一阶设计选择”，目前更像 pipeline diagnostic，而不是足够稳健的运营研究发现。尤其是城市结果中 no-filter 虽提升 net profit，但 acceptance 明显下降，且 Seattle no-filter 的 displayed ETA/IVT MAE 极高，这会削弱“运营可信菜单”的解释。

### CRITICAL 2. MNL 需求模型和 outside-option 校准缺乏外部依据

MNL 参数被定义为 simulator design parameters，而不是从 survey、revealed-preference 数据或文献范围校准得到。论文又表明原始 outside-option 设置导致 RC 几乎完全 opt-out，higher-uptake setting 才恢复行为变化。也就是说，主要行为结论高度依赖一个人为校准选择。  

对 TR Part E 而言，这会被视为较大威胁：乘客接受率、non-home uptake、consumer surplus、pricing comparison 全部由需求模型驱动。如果没有系统 sensitivity 或外部 calibration，审稿人很难判断 flat markdown 或 no-filter 的优势是否只是某组 MNL 参数下的局部现象。

### CRITICAL 3. Lambert-W 定价推导和实际目标函数之间存在理论断裂

正文已经承认 Lambert-W rule 是 heuristic reference transform，但 appendix 的推导仍有明显问题。Appendix 中先写 expected profit objective，然后将
\[
\Pi(\delta)=\sum_b \pi_b(\delta)(p_b-\hat c(b))
\]
化简为 \(-R-\delta\)，这一步忽略了 outside option denominator 对选择概率总和的影响；严格来说，bundle 被选择的总概率并不等于 1，因为有 outside option。随后又转向 revenue-based derivation。这个结构会让读者觉得定价层的数学基础不稳定。  

更重要的是，论文后文发现 Lambert-W-inspired rule 并不是最佳 pricing rule，且大部分价格 hit floor/cap。这样一来，“Lambert-W pricing layer”作为方法贡献的地位变得尴尬：它既不是理论最优，也不是实证最优，但仍在摘要和贡献中占据显著位置。

### MAJOR 1. 论文贡献表述仍显分散，主线不够聚焦

论文同时讲 menu filtering、predictor diagnostics、Lambert-W pricing、flat markdown、welfare distribution、city validation、benchmark degeneracy。每一条都重要，但当前版本像是多阶段实验报告的整合稿，而不是一个单一、强主张的 journal paper。正文中频繁出现 Phase 22/23/24、saved calibration、archival diagnostic 等表述，也会让论文显得像内部项目记录。

### MAJOR 2. Predictor 的作用与可靠性不足

菜单策略依赖预测 cost、ETA、IVT，但 predictor validation 显示 ETA/IVT CNN MAE 比 naive mean baseline 更差，随后依靠 0.35 CNN + 0.65 heuristic blend。既然 ETA filtering 是全文的核心机制，读者会期待更深入的 predictor calibration 分析，例如误差分布、是否系统性偏向某些 meeting point、filter false negative 的 ground-truth 定义是否可靠。当前仅报告 MAE 和 pruning rate 还不够。

### MAJOR 3. Baseline 和比较对象还不够强

现有 baselines 包括 full display、revenue-greedy、nearest、cheapest、passenger utility 等，但对 TR Part E/transportation OR 读者来说，还缺少更接近 DRT 文献的 operational baseline，例如 route-insertion-cost greedy、time-window-feasible ranking、meeting-point accessibility ranking、或基于 expected insertion delay 的 simple policy。当前 baseline 更偏 assortment toy comparison，未充分展示相对交通运营启发式的优势。

### MAJOR 4. 统计推断与表述需要更严格地区分

论文已经声明 split-level 是 inferential unit，这是好的。但 Austin/Seattle 的 bootstrap CI 在 n=2 时容易造成过度精确的视觉印象，即使标注 descriptive。建议不要用“95% CI”式语言描述 n=2 城市结果，而改为 “two paired split gaps”。此外，RC no-filter gap 仅约 full-display 绝对值的 0.15%，即使 CI 为正，其运营意义非常小，应避免在摘要或结论中被读成强效果。

### MAJOR 5. Welfare 和 passenger-facing interpretation 仍不充分

城市结果显示 no-filter 相对 full display 提高 profit，但 acceptance 下降 4.7 到 11.8 个百分点；consumer surplus 只小幅改善，且 Seattle no-filter displayed ETA/IVT MAE 很高。对 DRT 系统而言，接受率下降可能意味着平台服务质量或市场覆盖下降。论文需要更明确地区分“operator profit improves”与“system performance improves”，并解释 profit-surplus-acceptance 三者的权衡是否符合管理目标。

### MINOR 1. LaTeX 文本存在编码异常

正文中多处出现 “鈥?” 这类编码损坏字符，例如 “Layer 1 鈥?”、“methodology 鈥?”。这会严重影响投稿观感，需要全文修复。

### MINOR 2. Abstract 信息密度过高

摘要几乎把所有限制、阶段和数值都塞进去，读者难以抓住一句话贡献。建议压缩为：问题、方法、最关键机制发现、主限制。

### MINOR 3. 术语和命名略显工程化

如 “Phase 22/23/24”、“saved run”、“artifact pipeline”、“active-head evaluation state” 更像项目记录。正式论文中应改为 study names 或 experiment labels。

### MINOR 4. 部分表格 caption 不够 journal-ready

例如 “RC Main Opt-out Validation policy comparison” 命名略内部化；建议统一为 “RC mechanism benchmark under outside-option evaluation” 等学术表述。

### MINOR 5. 参考文献覆盖偏窄

DRT、meeting-point、assortment、MNL 的核心文献有覆盖，但缺少近年的 ride-pooling assignment、choice-based mobility-on-demand、assortment with outside option / pricing under MNL 的更系统引用。

## 5. Actionable Fixes for CRITICAL/MAJOR Weaknesses

### Fix for CRITICAL 1

收缩主结论，把本文定位为 **diagnostic framework + exploratory evidence**，而不是证明某个 no-filter 或 pricing rule 稳健占优。具体建议：

- 摘要和结论中将 “improves” 改为 “is associated with” 或 “in the calibrated runs”。
- 对城市结果只报告两个 split gaps，不使用强 inferential language。
- 新增一张 “Evidence hierarchy table”，明确哪些结论由 confirmatory evidence 支持，哪些只是 diagnostic/descriptive。
- 若时间允许，至少增加更多 city split pairs 或更多 demand seeds；否则不要把 Austin/Seattle 作为强外部验证。

### Fix for CRITICAL 2

补一个系统的 MNL sensitivity/calibration section：

- 对 \(\bar u\)、\(u^{home}\)、\(\beta\)、walking scale、outside utility 做网格或 Latin hypercube sensitivity。
- 报告 no-filter、strict-filter、flat markdown 在不同 acceptance regimes 下的 rank stability。
- 给出参数来源：若无真实数据，应引用 travel behavior/DRT stated preference 文献作为 plausible range。
- 将 higher-uptake regime 明确定义为 “stress-test behavioral regime”，不要暗示它是被验证的真实需求模型。

### Fix for CRITICAL 3

重写 Lambert-W 定价部分：

- 删除或修正 appendix 中错误的 profit simplification。
- 将 Lambert-W derivation 限定在 revenue-only/shared-offset/no-clipping/no-route-cost 的 reference problem。
- 正文中不要把 Lambert-W pricing 放在主要方法贡献中心，而应表述为 “one pricing transform tested against simpler alternatives”。
- 既然 flat markdown 实证更好，建议把 pricing contribution 改成 “boundary-hit diagnostics reveal that closed-form-inspired pricing can fail under platform price bounds”。

### Fix for MAJOR 1

重组论文叙事：

- 主线建议改为：问题设定 -> diagnostic framework -> filter distortion -> behaviorally live calibration -> pricing boundary-hit lesson。
- 删除 Phase 编号和 saved-run 语言，换成 “Study 1/2/3”。
- 把 archival sensitivity 和开发性实验移到 supplementary，不在正文中反复提。

### Fix for MAJOR 2

加强 predictor/filter validity：

- 报告 ETA/IVT blended signal 的 MAE、bias、quantiles，而不只是 raw CNN。
- 按 policy 和 offer type 分解 false-negative pruning：home/non-home、near/far meeting point、early/late request。
- 给出 filtering decision 的 confusion matrix：被 filter 掉的 bundle 中有多少按 realized ETA 实际可接受。
- 解释 CNN ETA/IVT worse-than-naive 为什么不会破坏主结论。

### Fix for MAJOR 3

加入更交通运营导向的 baseline：

- insertion-cost greedy；
- earliest-feasible pickup / minimum lateness ranking；
- walking-distance plus route-delay weighted heuristic；
- no-filter + simple operational score without MNL pricing。

若无法新增实验，至少在 related work 和 limitations 中承认当前 baseline 更偏菜单/assortment 层，而非完整 DRT policy benchmark。

### Fix for MAJOR 4

调整统计呈现：

- n=2 城市实验只显示两个 paired gaps，不给 bootstrap 95% CI。
- 对 RC gap 同时报告 absolute effect、percentage effect 和 operational threshold。
- 避免把 split-level bootstrap 与 episode-level uncertainty 混合叙述。

### Fix for MAJOR 5

补充 passenger-facing tradeoff 分析：

- 明确 net profit 增加是否主要来自 fewer accepted rides、lower cost accepted rides、price change，还是 failure/travel cost 变化。
- 报告 accepted-user-only welfare 与 all-request welfare。
- 对 no-filter acceptance 下降给出管理解释：平台是否愿意以较低接受率换取更高 profit？
- 将 consumer surplus 的计算公式放入正文或 appendix，说明 outside option 如何处理。

## 6. Missing References

建议补充或检查以下方向的文献，不一定全部引用，但至少应覆盖相关脉络：

- Choice-based mobility-on-demand / ride-pooling assignment with user acceptance：Alonso-Mora 系列 ride-pooling dispatch work，以及 choice-aware assignment/offer generation 文献。
- DRT stated-preference 或 mode-choice calibration 文献，用于支持 MNL 参数范围和 outside-option calibration。
- MNL assortment/pricing with outside option、price bounds、heterogeneous costs 的更近文献；当前仅靠 Talluri and van Ryzin、Rusmevichientong、Wang 不够完整。
- Meeting-point ride-sharing/DRT 的近年综述或 computational studies，尤其是与 walking tolerance、pickup point accessibility 和 passenger inconvenience 相关的研究。
- Transportation service design 中 profit-service quality tradeoff、consumer surplus 或 welfare evaluation 的相关文献。

## 7. Verdict

**Ready for submission? No.**

更准确地说：**不建议以当前版本直接投 TR Part E**。论文有潜力，但现在更像一篇认真整理过的 simulation diagnostic report，而不是证据链完整的 journal article。最需要优先修的是三件事：第一，重写 Lambert-W 定价理论边界；第二，补强或收缩 MNL 校准与统计证据；第三，把文章主线从“某 heuristic 更优”改成“过滤与定价层的诊断框架，以及在当前校准下观察到的管理 tradeoff”。完成这些后，论文有希望达到 “Almost / major revision 后可投”。
