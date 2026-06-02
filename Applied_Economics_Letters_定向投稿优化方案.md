# Applied Economics Letters 定向投稿优化方案

创建日期：2026-05-31

## 一、最终投稿定位

目标期刊：

**Applied Economics Letters**

已核验：

- 2024 JCR：SSCI。
- 分类：Economics。
- 分区：Q3。
- JIF：1.3。
- Taylor & Francis官方接收率：35%。

核心判断：

Applied Economics Letters不是适合写成长篇AI金融论文的期刊。它适合的是：

- 一个清楚的经济/金融问题；
- 一个短实证结果；
- 方法透明；
- 表格少；
- 贡献边界克制。

因此，本项目必须从“AI/ML预测框架”改写为：

**分析师预测分歧是否能提前预警亚太上市公司的财务压力。**

## 二、AEL版本题目

首选：

**Analyst Disagreement and Financial Stress in Asia-Pacific Listed Firms**

备选：

**Analyst Forecast Dispersion and Corporate Distress in Asia-Pacific Markets**

不要在题目中使用：

- XGBoost；
- machine learning；
- AI；
- framework；
- multimodal；
- trading strategy。

这些词会让编辑误判为技术论文，而不是Applied Economics Letters偏好的短实证论文。

## 三、主研究问题

**Does analyst forecast disagreement predict future financial stress among Asia-Pacific listed firms beyond accounting and market indicators?**

中文表达：

分析师预测分歧是否在传统会计指标和市场指标之外，对亚太上市公司的未来财务压力具有增量预警信息？

## 四、核心假设压缩

AEL主文只保留两个假设：

H1：分析师预测分歧越高，未来财务压力/财务困境概率越高。

H2：分析师变量在会计指标和市场指标之外具有增量预测信息。

以下内容移到稳健性或补充材料：

- 分析师预测下调；
- 分析师覆盖下降；
- 不同国家/市场异质性；
- SHAP详细解释；
- XGBoost完整模型细节。

## 五、因变量策略

### 主标签：Financial Stress

如果严格distress事件不足，AEL主文使用financial stress更稳：

Financial Stress = 1，如果未来12个月内出现以下任一情况：

- interest coverage < 1.5，连续两个期间；
- negative equity；
- consecutive operating losses；
- severe downgrade/default signal；
- distress-related delisting。

优点：

- 事件数更够；
- 更容易估计logit；
- 更符合短实证论文的统计稳定性。

### 稳健性标签：Strict Distress

严格财务困境作为robustness：

- bankruptcy filing；
- debt default；
- restructuring；
- receivership / liquidation；
- distress-related delisting；
- severe credit downgrade，如果评级覆盖足够。

关键规则：

不要把普通退市当distress。并购、私有化、自愿退市、转板、行政变化必须排除。

## 六、主模型设计

AEL主文不以XGBoost为主模型。

主模型：

```text
Pr(Stress_{i,t+4}=1)
= logit(alpha
  + beta * AnalystDispersion_{i,t}
  + gamma * AccountingControls_{i,t}
  + delta * MarketControls_{i,t}
  + Country FE
  + Sector FE
  + Time FE)
```

主文重点报告：

- AnalystDispersion的系数方向；
- marginal effect；
- 显著性或经济意义；
- 加入analyst block后预测指标是否改善。

辅助模型：

- XGBoost：只用于增量预测对比；
- SHAP：放补充材料，除非一张图能非常清楚地服务主结论；
- LightGBM：除非XGBoost不稳定，否则不要写进主文。

## 七、主文表格设计

AEL主文最多三张表。

### Table 1：Sample and Stress Distribution

内容：

- market；
- firms；
- firm-quarters；
- stress events；
- analyst-covered firm-quarters；
- stress events with analyst coverage。

目的：

证明样本、事件数、分析师覆盖率足够。

### Table 2：Main Logit Results

列设计：

1. Accounting + market。
2. Accounting + market + analyst dispersion。
3. Accounting + market + analyst dispersion + revisions / coverage change。

报告：

- coefficient；
- standard error；
- marginal effect，最好；
- country / sector / time controls。

### Table 3：Incremental Prediction and Robustness

内容：

- ROC-AUC；
- PR-AUC；
- Brier score；
- strict distress robustness；
- analyst coverage >= 2；
- analyst coverage >= 3。

目的：

一张表完成“增量价值+稳健性”。

## 八、补充材料设计

主文放不下的全部进入supplement：

- variable definitions；
- sample construction；
- delisting reason audit；
- strict distress事件定义；
- 6/12/24-month horizons；
- market split；
- excluding microcaps；
- financial vs non-financial；
- full XGBoost hyperparameters；
- SHAP summary plot；
- SHAP dependence plot。

AEL主文不能承担完整技术附录，否则会失去短文优势。

## 九、字数预算

保守按2,000词以内准备主文。

| 部分 | 目标词数 |
|---|---:|
| Abstract | 100-120 |
| Introduction | 350-450 |
| Data and variables | 350-450 |
| Method | 200-250 |
| Results | 500-650 |
| Conclusion | 150-200 |

写作原则：

- 不写完整literature review；
- 每段只承担一个功能；
- 引文控制在10-15篇；
- 不解释XGBoost原理；
- 不展开行为金融理论，只点明信息不对称和分析师分歧即可。

## 十、结果门槛

### 绿色结果：可以投AEL

- analyst dispersion方向为正；
- marginal effect有经济意义；
- 加入analyst变量后PR-AUC、ROC-AUC或Brier score改善；
- strict distress或coverage robustness不推翻主结论。

### 黄色结果：谨慎投AEL

- 主样本效果弱，但高分析师覆盖样本有效；
- 或预测改善小，但方向稳定、经济解释清楚；
- 需要写成“limited but economically meaningful evidence”。

### 红色结果：不要按当前题目投AEL

- analyst变量符号不稳定；
- 结果完全依赖XGBoost；
- stress标签无法审计；
- 加入会计和市场变量后analyst效果消失；
- 需要很长方法解释才能说清楚。

## 十一、摘要模板

```text
This letter examines whether analyst forecast disagreement contains early-warning
information about financial stress among Asia-Pacific listed firms. Using
S&P Capital IQ Estimates matched to firm-quarter accounting and market data, we
show that higher analyst forecast dispersion is associated with a higher
probability of financial stress over the following year. The result remains after
controlling for profitability, leverage, liquidity, market performance, and fixed
effects, and analyst variables improve out-of-sample prediction relative to
accounting and market indicators alone. The evidence suggests that analyst
disagreement captures information-environment risk before financial stress is
fully reflected in conventional firm fundamentals.
```

## 十二、执行顺序

1. 先导出事件和状态数据，不先随机拉公司。
2. 确认financial stress / strict distress事件数。
3. 确认analyst estimates覆盖率。
4. 构造firm-quarter panel。
5. 先跑logit，不先跑XGBoost。
6. 如果logit方向稳定，再跑XGBoost增量预测。
7. 只在结果足够清楚后做SHAP。
8. 先生成三张主表，再写正文。

## 十三、最终判断

按照AEL目标，最稳路线不是“更复杂”，而是“更窄、更短、更干净”。

本项目的投稿形态应固定为：

**一篇2,000词左右的短实证论文，证明Capital IQ Estimates中的分析师预测分歧对亚太上市公司财务压力有增量预警价值。**
