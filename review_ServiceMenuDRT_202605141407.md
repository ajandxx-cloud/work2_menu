# Review: Service Menu Optimization for Many-to-One DRT

模型确认：本轮按你要求的 `gpt-5.5 high` 审稿口径执行。

主文稿确认：当前目录顶层未找到名为 `manuscript.tex` 的文件；实际可审主文稿定位为 `ooh_code/manuscript/main.tex`，并按其中 `\input{sections/...}` 的章节顺序连同附录和参考文献一起审阅。

Venue：Transportation Research Part E: Logistics and Transportation Review。

## 1. Overall Score

**5/10，低于弱接收线。**

按“6 = weak accept，7 = accept”的标准，我目前会给 **5 分**。论文选题有现实运营价值，问题设定也比一般 DRT 启发式论文更有“决策层”意识；但当前版本的可发表性主要受三类问题限制：第一，核心实证证据仍高度依赖模拟校准和低样本外部检查；第二，MNL 需求模型、outside option 和定价规则缺乏足够外部校准；第三，论文的理论贡献边界已经被作者主动收缩，但方法叙述仍显得比证据能支持的范围更强。若重新聚焦为“诊断框架 + 有限模拟证据”，并补强需求敏感性、统计表达和 baseline，论文有机会进入 major revision / borderline weak accept 区间。

## 2. Summary

本文研究 many-to-one demand-responsive transit 中“meeting point + pickup time window”服务 bundle 的菜单展示问题，将候选生成、MNL 乘客选择、预测 routing cost、common-offset pricing、exact-small/greedy-large menu construction 和 ETA filtering 放在一个分层模拟框架中评估。论文的主要经验发现是：ETA 过滤层会显著改变可见候选集；在近乎完全 opt-out 的 RC 设置中，结果更适合作机制诊断；在更高 uptake 的校准环境中，菜单/定价比较才更有行为解释意义。

整体上，论文最强的地方是诚实地区分了 mechanism diagnostic、behavioral stress test 和 descriptive external check，避免直接声称某个 heuristic 普遍占优。但作为 TR Part E 投稿，当前证据链仍偏弱：需求模型是人为设定，城市实验只有每城两个 split pair，Lambert-W 定价层更多是启发式而非理论最优，且主要结论尚未被足够强的 operational baselines 和稳健性分析支撑。

## 3. Strengths

1. **问题设定有清晰的运营意义。** 将 DRT 的 passenger-facing menu 视为独立运营决策，而不只是 routing 后的展示细节，这一点对 transportation operations 读者有吸引力。

2. **三层决策结构清楚。** Candidate generation、menu policy、passenger choice 的分层叙述让读者能区分过滤层、菜单层和选择层分别贡献了什么。

3. **作者对证据边界有自我约束。** 文中多次承认 RC outside-option benchmark 是 degenerate，Austin/Seattle 是 low-sample directional checks，Lambert-W pricing 是 heuristic transform。这种克制比过度宣称更可信。

4. **paired replay evaluation 设计合理。** 固定 predictor、request traces 和 simulator 条件来比较 policies，有助于隔离 menu policy 的影响。

5. **诊断指标丰富。** 除 net profit 外，还报告 FN pruning、home-only share、menu size、acceptance、non-home acceptance、surplus、floor hit 等指标，有利于解释机制，而不是只比较一个收益数。

6. **可复现意识较强。** YAML manifest、artifact table、runner command 和 appendix 中的 reproducibility section 能增强读者对实验流水线的信任。

## 4. Weaknesses

### CRITICAL 1. 核心实证证据不足以支撑 TR Part E 级别的主结论

论文目前的证据分为 RC mechanism diagnostic、higher-uptake RC behavioral calibration、Austin/Seattle descriptive external checks。这个分层是好的，但每一层都有明显约束：RC 原始设置下 acceptance 接近 0，几乎没有真实选择行为；higher-uptake 是人为校准的 stress test，不是外部验证的需求模型；Austin 和 Seattle 每城只有两个 split pair，只能作为方向性观察。

更关键的是，最新表格显示若干核心表的行为变化仍非常小。例如 phase31 中 high uptake 的 acceptance 也只有约 0.007 到 0.009，low/medium 几乎接近 0；phase30 的 robust filtering 表中多个 filter 的 gap vs full 均为 0，说明过滤诊断更像候选集暴露分析，而不是强运营收益证据。当前论文若被读成“某个 no-filter 或 flat-markdown 策略优越”，会超出证据能力。

### CRITICAL 2. MNL 需求模型和 outside-option 校准缺乏外部依据

MNL 参数被明确写成 simulator design parameters，而不是来自 stated preference、revealed preference、文献范围校准或实际运营数据估计。可是论文最重要的行为结论，包括 acceptance、non-home uptake、consumer surplus、pricing comparison，都由这些参数强烈驱动。

当前版本虽然承认 higher-uptake regime 是校准环境，但仍需要让读者相信：在合理需求参数范围内，过滤层和菜单层的主要机制是否稳定。如果没有系统 sensitivity 或外部校准，审稿人很容易认为 no-filter、flat markdown 或 home-retention 的表现只是某组 MNL 参数下的局部模拟现象。

### CRITICAL 3. Lambert-W pricing 的理论地位尴尬

正文和附录已经努力强调 Lambert-W rule 只是 reference transform，不是 full simulator objective 的最优解。但问题在于，它仍在摘要、方法和贡献叙述中占据较显眼位置，而实证上 flat markdown 在某些设置下反而更好，且 price clipping / floor hit 明显影响结果。

这会让理论贡献显得不稳定：Lambert-W 既不是最终目标的精确解，也不是实证上稳定最优的 pricing rule。如果保留它，应把它降级为一个 tested pricing baseline 或 reference transform，而不是作为方法核心贡献之一。

### MAJOR 1. 论文主线仍偏分散

当前论文同时讲 service-menu formulation、CNN predictor、exact-vs-greedy solver、ETA filtering、Lambert-W pricing、flat markdown、uptake regimes、city validation、welfare 和 reproducibility pipeline。每个部分都有意义，但组合后更像一个大型 simulation diagnostic report，而不是一篇主张高度聚焦的 journal article。

建议主线收缩为：DRT service-menu diagnostic framework -> ETA filtering 如何扭曲候选集 -> exact/greedy 只是菜单层 approximation diagnostic -> uptake calibration 决定何时可解释 profit/welfare -> pricing boundedness 是附带经验教训。

### MAJOR 2. Predictor 可靠性不足，且与过滤结论绑定过深

附录显示 CNN 的 ETA/IVT MAE 明显差于 naive mean baseline，随后依赖 0.35 CNN + 0.65 heuristic blend。由于 ETA filtering 是论文核心机制，读者会追问 deployed filtering signal 的误差分布、bias、quantile、false negative 的真实定义，以及不同 meeting-point 类型上的误判结构。

当前只报告 MAE、FN pruning 和 displayed-offer diagnostics 还不够。特别是当 FN pruning 接近 0.99 时，必须证明这个数不是由一个严重失准的 ETA signal 人为造成，而是一个有运营解释的过滤层现象。

### MAJOR 3. Baseline 不够贴近 transportation operations

现有 baselines 包括 full display、revenue-greedy、nearest、cheapest、passenger utility 等，偏向 assortment/menu 层。对 TR Part E 读者来说，还需要更接近 DRT 运营实践的 baseline，例如 insertion-cost greedy、minimum-lateness ranking、time-window-feasible ranking、walking plus route-delay score，或不依赖 MNL pricing 的 simple operational menu rule。

如果缺少这些 baseline，论文很难说明所提框架相对交通运营启发式有实质优势。

### MAJOR 4. 统计呈现需要更保守

论文已经意识到 split-level 是 inferential unit，这是正确方向。但 Austin/Seattle 每城只有两个 split pair，不应使用任何容易被理解为稳定置信区间的表达。建议只报告 two paired split gaps，并在主文中明确“descriptive only”。

此外，RC 中有些 net-profit gap 的绝对量相对总 profit 很小，即使方向一致，也未必有运营意义。建议同时报告 absolute effect、percentage effect、acceptance tradeoff 和一个管理上可解释的 minimum effect threshold。

### MAJOR 5. Welfare 和 passenger-facing tradeoff 解释不足

论文以 net profit 为 primary metric，但 DRT 系统通常还关心服务覆盖、接受率、乘客剩余和体验可信度。若 no-filter 提高 profit 但降低 acceptance，或提高菜单暴露但增加 ETA/IVT 误差，不能简单表述为 system performance improvement。

建议分解 profit gain 来源：是价格变化、服务成本下降、接受请求减少、failure cost 下降，还是选择更低成本 bundle？同时区分 all-request welfare 和 accepted-user-only welfare，并给出 consumer surplus 的计算公式。

### MINOR 1. LaTeX 源文件存在编码损坏

多个章节中出现 `鈥?`、`閳?` 一类 mojibake 字符，例如 related work 和 problem setting 中的破损破折号。这会严重影响投稿观感，应在正式投稿前全局修复编码。

### MINOR 2. 摘要信息密度偏高

摘要试图同时覆盖问题、模型、算法、诊断、证据分层和边界声明，读者较难抓住一句话贡献。建议压缩为：问题 -> 方法框架 -> 关键机制发现 -> 证据边界。

### MINOR 3. 工程化命名过多

`phase29`、`phase30`、`phase31`、`active-head evaluation state`、`artifact pipeline` 等表达更像项目记录。正式论文中建议改成 Study 1/2/3 或 descriptive experiment labels。

### MINOR 4. 部分 caption 仍显内部化

表格 caption 中的 “outside-option evaluation setup”、“benchmark-role bridge”、“phase” 等术语需要统一成面向读者的学术表述，并在首次出现时解释。

### MINOR 5. 参考文献覆盖仍可扩展

当前文献覆盖了 DARP、meeting points、MNL assortment 和 HGS，但 choice-aware ride-pooling、mobility-on-demand offer generation、DRT stated preference、bounded MNL pricing、service quality/profit tradeoff 的文献还偏少。

## 5. Actionable Fixes for CRITICAL/MAJOR Weaknesses

### Fix for CRITICAL 1

将论文贡献明确收缩为 **diagnostic framework with exploratory simulation evidence**。摘要、引言和结论中避免使用暗示稳健优越性的表达，如 “improves” 或 “dominates”；改为 “reveals”、“diagnoses”、“in calibrated regimes”。城市结果只称为 descriptive directional checks。若时间允许，增加更多 city split、demand seed 或 instance family；若不能增加，就不要把 Austin/Seattle 作为强外部验证。

### Fix for CRITICAL 2

新增系统 MNL sensitivity/calibration section。至少对 `bar u`、`u_home`、`beta`、walking scale、outside-option utility 做网格或 Latin hypercube sensitivity，报告各 policy 的 rank stability、acceptance regime 和 welfare tradeoff。若没有真实需求数据，应引用 travel behavior / DRT stated preference 文献给出 plausible ranges，并明确 higher-uptake 只是 stress-test regime。

### Fix for CRITICAL 3

重写 Lambert-W 定价叙述。将推导限定在 revenue-only、shared-offset、no clipping、no route-cost 的 reference problem；正文中把 Lambert-W 改为 “one pricing transform evaluated against simpler alternatives”。如果 flat markdown 在当前实验中表现更好，应把贡献改成：price bounds and floor/cap hits can invalidate closed-form-inspired pricing intuition。

### Fix for MAJOR 1

重组论文叙事，减少并列贡献。建议正文只保留三个主实验：exact-vs-greedy approximation diagnostic、ETA filtering diagnostic、behaviorally live uptake/pricing stress test。城市实验作为 external descriptive check。开发性或历史性 sensitivity 放到 supplement，主文避免反复出现 phase 编号。

### Fix for MAJOR 2

补强 predictor/filter validity：报告 deployed blended ETA/IVT signal 的 MAE、bias、P50/P90/P95 error；按 home/non-home、near/far meeting point、early/late request 分解 false-negative pruning；给出 filtering decision confusion matrix，即被过滤掉的 bundle 中有多少按 realized ETA 实际可接受。还需要解释 CNN ETA/IVT worse-than-naive 为什么不会破坏菜单过滤结论。

### Fix for MAJOR 3

加入至少 2 到 3 个运营导向 baseline：insertion-cost greedy、minimum lateness / earliest feasible pickup、walking-distance plus route-delay weighted score，或 no-filter + operational score without MNL pricing。这样可以说明框架不是只战胜了较弱的 assortment baselines。

### Fix for MAJOR 4

将统计呈现改得更保守。Austin/Seattle 只报告两个 paired split gap，不给 bootstrap-style CI。RC 结果同时给 split-level mean、range、percentage effect 和 acceptance tradeoff。避免把 episode-level uncertainty 与 split-level inference 混合解释。

### Fix for MAJOR 5

新增 passenger-facing tradeoff 分析。分解 net profit：charge revenue、discount cost、travel cost、service cost、failure cost、accepted-request count。报告 all-request surplus 和 accepted-user-only surplus，并在 appendix 给出 surplus 公式及 outside option 的处理方式。结论中明确区分 operator profit improvement 与 overall service quality improvement。

## 6. Missing References

建议补充或至少检查以下文献方向：

- Choice-aware mobility-on-demand / ride-pooling assignment，尤其是 offer generation、user acceptance 和 assignment 联合建模相关研究。
- DRT stated-preference、mode choice、walking tolerance、pickup point acceptance 的校准文献，用于支撑 MNL 参数范围。
- MNL assortment and pricing with outside option、bounded prices、heterogeneous costs 的更近研究。
- Meeting-point ride-sharing / DRT 的近年 computational studies，尤其关注 passenger inconvenience 和 pickup-point accessibility 的工作。
- Transportation service design 中 profit、acceptance、consumer surplus、service quality tradeoff 的相关文献。

## 7. Verdict

**Ready for submission? No.**

当前版本不建议直接投 TR Part E。论文有潜力，但现在更像一个认真整理过的 simulation diagnostic framework，而不是证据链完整的 journal article。最优先的修改是：收缩主张、补强 MNL/需求敏感性、重写 Lambert-W 定价边界、加入更贴近 DRT 运营的 baselines，并把城市结果作为低样本描述性检查来呈现。完成这些后，论文有希望达到 “Almost / major revision 后可投”。
