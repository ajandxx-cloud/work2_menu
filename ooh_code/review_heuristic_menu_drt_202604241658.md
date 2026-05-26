# 审稿意见（模型：gpt-5.4 / high）

原始主文稿：`manuscript/main.tex`  
审稿轮次：第 2 轮复审  
论文标题：*Heuristic Menu Design for Many-to-One Demand-Responsive Transit: Paired Evaluation and Filtering Diagnostics*

## Overall Score
6/10

## Summary
本轮修订较一审有明显进步，而且几项最突出的结构性问题已经被正面处理。具体而言，上轮关于“外部选项缺失导致模型定义不一致”“标题与方法将启发式表述成优化”“Austin/Seattle 被过度表述为真实世界 DRT 数据”的问题，我认为已基本解决；关于 ETA 过滤识别、样本外证据强度、乘客福利刻画、以及定价机制的理论与经济解释，则仍只是部分解决。

修订后，论文的真实贡献已经比上一版更清晰：这是一篇“多对一 DRT 菜单展示启发式 + 配对评估框架 + 过滤诊断”的论文，而不是一篇严格意义上的最优化论文。这种重新定位是正确的，但核心结论目前仍受到两个关键限制：一是过滤诊断仍未与 ETA 质量问题充分剥离，二是 RC 机制基准在外部选项下呈现高度退化，削弱了“机制诊断”证据的说服力。

## Strengths
- 1. 一审中最严重的建模一致性问题已被修复。外部选项现在贯穿问题定义、MNL 概率、结果解释与接受/放弃统计，这一点非常重要，也显著提升了论文的理论自洽性。
- 2. 论文定位明显更诚实、更匹配实际贡献。将“optimization”降格为“heuristic menu design”，并明确 Lambert-W 只是启发式模板而非最优性证明，这一修订是正确且必要的。
- 3. 实验框架仍然是本文最有价值的部分之一。冻结共享预测器、复用相同请求轨迹、做 split-level paired rerun，这种控制变量设计优于许多仅做松散仿真的论文。
- 4. 过滤诊断比上一版扎实得多。现在加入了 false-negative pruning、软过滤变体、displayed-offer ETA/IVT MAE 等诊断，且结论也从“ETA 过滤普遍失败”收缩为“候选集扭曲”，这是成熟的修订方向。
- 5. 对基准角色的重新划分是合理的。RC 被降为机制基准，Austin 为主影响基准，Seattle 为补充方向性检查，避免了上一版把不同证据层次混在一起的问题。
- 6. 限制讨论写得比上一版好。对预测器分布偏移、校准敏感性、外部效度不足、逼近边界等都有交代，说明作者愿意把证据边界讲清楚。

## Weaknesses
- `CRITICAL` 核心机制结论仍未被充分识别。上轮关于 ETA 过滤的质疑只是部分解决。虽然作者现在加入了 pruning 指标并收窄了结论，但附录仍表明原始 ETA/IVT 预测头明显差于 naive mean baseline，而部署时又“混合了 CNN 与 heuristic estimates”。在这种情况下，当前证据依然更像是在说明“不要用质量较差或失配的 ETA 信号做硬过滤”，而不是更一般性的“严格 ETA 过滤会系统性扭曲候选集”。缺少 stronger ETA / oracle ETA / noise-robustness 的对照，使核心机制主张尚未真正站稳。
- `CRITICAL` RC 作为“机制诊断基准”的有效性仍然不足，而且这是在本轮修订后暴露得更清楚的问题。作者修复了外部选项，这是对的；但修复之后 RC 的接受率至多约 0.11%，opt-out 高达 99.4%–99.6%。在如此退化的行为区间里，菜单变化主要反映“可展示集合如何变化”，却很难反映“现实可接受需求下的选择机制如何变化”。因此，RC 可以支持结构性观察，但很难支撑强机制论断。
- `MAJOR` 外部效度和统计证据仍然偏弱。上轮关于样本基础过窄的担忧只被部分解决。作者现在明确说明 Austin/Seattle 只有两个 split pair，因此只是 descriptive，这一表述更诚实；但证据本身并没有变强。既然实证影响结论主要依赖 Austin/Seattle，那么当前样本量仍不足以支撑较强的跨实例管理含义。
- `MAJOR` 乘客侧福利分析仍不够完整。上轮关于只看运营者净收益的问题只被部分解决。现在加入了 acceptance、opt-out 和 consumer surplus，是进步；但论文同时报告“接受率下降而消费者剩余略升”，这需要更细的分解与分布解释。否则读者很难判断该方法究竟是在改善匹配质量，还是在通过收缩菜单把部分边际乘客排除在外。
- `MAJOR` 定价部分虽然措辞更诚实，但理论与经济解释仍偏弱。上轮关于 pricing calibration 的担忧只被部分解决。现在作者承认 shared-offset + clipping 下 Lambert-W 不是该利润目标的精确最优解，这很好；但这也意味着论文需要进一步说明：为何还要使用这一变换？它相对更简单的 cost-plus / fixed-offset / clipped linear pricing 基线到底带来了什么？
- `MAJOR` 论文的自洽性仍受“主文不够自包含”影响。对于一篇核心发现依赖 ETA 过滤质量的论文，实际部署中 ETA/IVT 是如何由 CNN 与 heuristic 信号混合得到、过滤器究竟用的是哪一个量、诊断 MAE 对应的是哪一个量，这些都不应只留在附录。当前主文读起来仍会让读者误以为“冻结预测器”直接就是过滤依据。
- `MINOR` 记号和表述虽然比上一版统一，但“outside option”和“home bundle”之间的概念区分仍值得再强化。两者在行为与运营意义上并不相同，若正文中有几处表述不够谨慎，读者仍可能把“选择 home bundle”和“opt out”混同。
- `MINOR` “full display”作为 status-quo reference 而非 optimal benchmark 的说明已有改善，但仍建议在结果段落中反复提醒，否则容易被读者误读为近似上界。

## Actionable fixes
- 针对 ETA 过滤识别不足：至少补做一组四路对照实验，比较 `部署中的混合 ETA`、`纯 heuristic ETA`、`更强/校准后的 ETA`、`oracle ETA` 下的 false-negative pruning、菜单构成、profit、acceptance 与 welfare 指标。如果无法补足全部实验，则必须进一步收缩中心结论，明确限定为“在当前 ETA stack 下观察到的候选集扭曲”。
- 针对 RC 基准退化：重新校准 RC 的效用尺度或选择参数，使其落入非退化接受区间；更理想的是报告低/中/高接受率三个行为区间下，过滤诊断是否仍成立。如果不能做到，建议将 RC 明确降格为附属性结构诊断基准，并删除任何暗示其可支撑一般机制结论的表述。
- 针对外部效度不足：增加 Austin/Seattle 的 split pair 数量，或至少补充更多 demand intensity、fleet size、vehicle capacity、choice-parameter 设定下的 paired rerun。若实验资源有限，则请进一步收紧管理含义，把论文定位为“配对案例证据”而非“跨场景稳健发现”。
- 针对福利分析不完整：补充 walking、waiting、IVT、generalized cost/expected utility 的分布或分位数结果，并解释为何 acceptance 下降而 consumer surplus 上升。最好再加入按用户类型或空间区域的异质性分析，以排除“只让更容易服务的乘客受益”的可能。
- 针对定价机制薄弱：报告价格触碰上下界的比例、对 `R` 和 `price caps` 的敏感性，并加入至少两个更简单的价格基线，例如固定 offset 的 cost-plus pricing、统一 markdown、或 grid-search offset。若 Lambert-W-inspired 变换并无稳定增益，应进一步淡化其方法学地位。
- 针对主文不自包含：把“部署中的 ETA/IVT 混合方式、过滤器输入量、用于诊断的误差定义”移动到主文方法部分，并统一 `predicted / deployed / realized` 三类时间量的记号，避免读者在主文与附录之间来回推断。

## Missing References
从当前修订说明看，上轮指出的缺失文献大概率已补入，且本轮我没有看到必须新增的核心引用缺口。建议作者最后再核对一次：上轮列出的 `Stiglic et al. (2015)`, `Czioska et al. (2019)`, `Dong et al. (2020)`, `Cortenbach et al. (2024)`, `Wang (2012)`, `Stumpe et al. (2024)` 不仅应出现在参考文献中，也应在正文相应论证位置被实质性讨论，而非仅“补上引用”。

## Verdict
Almost
