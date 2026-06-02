# AI+金融论文研究计划（Q3策略修正版）

**目标**：SCIE Q3期刊发表，接收率70-80%  
**时间线**：2个月（8周）  
**首选期刊**：Journal of Asian Finance, Economics and Business (JAFEB)

---

## 一、核心策略调整

### 从Q2策略到Q3策略的关键变化

| 维度 | 原计划（Q2） | 修正计划（Q3） | 原因 |
|------|------------|--------------|------|
| **目标期刊** | RIBAF, FRL, PBFJ | JAFEB, JRFM, IJFS | 接收率从30%提升到70% |
| **研究重点** | 方法创新 | 实证发现 | Q3期刊重视应用而非算法 |
| **方法复杂度** | XGBoost+LightGBM+LLM | XGBoost+SHAP | 简化，降低技术风险 |
| **时间线** | 3-4个月 | 2个月 | Q3审稿快，方法简单 |
| **贡献点** | 多模态融合 | 亚太市场首次系统研究 | 地域novelty足够 |

---

## 二、研究问题（重新聚焦）

### 核心问题
**"Predicting Analyst Earnings Surprises in Asian Markets: A Machine Learning Approach with Cross-Market Comparison"**

### 三个子问题（对应三个结果部分）
1. **描述性发现**：亚太三市场（SGX/HKEx/ASX）的分析师预测偏差有何特征？与美股有何不同？
2. **预测模型**：机器学习方法能否有效预测盈利惊喜方向？哪些特征最重要？
3. **跨市场对比**：不同市场的预测难度和驱动因素有何差异？

### 为什么这个问题适合Q3期刊？
- ✅ 地域novelty明确（亚太市场研究少）
- ✅ 实证导向（描述性统计 + 预测模型）
- ✅ 方法成熟（XGBoost是验证过的工具）
- ✅ 数据可靠（Capital IQ机构级数据）
- ✅ 对JAFEB读者有价值（亚洲金融学者）

---

## 三、目标期刊详细分析

### 首选：Journal of Asian Finance, Economics and Business (JAFEB)

**期刊信息**：
- **分区**：SCIE Q3
- **Impact Factor**：1.9 (2023)
- **接收率**：约70-75%（基于MDPI类似期刊估算）
- **审稿周期**：8-12周
- **出版商**：Korean Distribution Science Association
- **开放获取**：部分开放

**为什么是最佳选择**：
1. **地域完美匹配**：专注亚洲金融市场，你的研究正是目标受众
2. **方法门槛低**：接受传统ML方法，不要求算法创新
3. **接收率高**：实证研究为主，只要数据可靠、方法稳健就容易接受
4. **审稿友好**：审稿人多为亚洲学者，理解地域数据的价值

**典型发表论文类型**：
- "Determinants of Stock Returns in Asian Markets"
- "Machine Learning for Credit Risk in Southeast Asia"
- "Analyst Forecast Accuracy in Emerging Markets"

**投稿要求**：
- 字数：6000-8000词（比Q2期刊短）
- 格式：APA 7th edition
- 结构：Introduction, Literature Review, Methodology, Results, Conclusion
- 重点：实证结果 > 理论贡献

### 备选1：Journal of Risk and Financial Management (JRFM)

**期刊信息**：
- **分区**：SCIE Q3
- **Impact Factor**：2.5 (2023)
- **接收率**：约60-70%
- **审稿周期**：6-8周（MDPI快速审稿）
- **出版商**：MDPI
- **开放获取**：是（APC约1800 CHF）

**优势**：
- 审稿最快（6-8周）
- 接受AI+金融方法论
- 国际化程度高

**劣势**：
- 需要支付APC（约1800瑞士法郎 = 1.5万人民币）
- 对方法论要求比JAFEB稍高

### 备选2：International Journal of Financial Studies (IJFS)

**期刊信息**：
- **分区**：SCIE Q3
- **Impact Factor**：2.3 (2023)
- **接收率**：约65-75%
- **审稿周期**：6-10周
- **出版商**：MDPI
- **开放获取**：是（APC约1600 CHF）

**适合场景**：如果JAFEB拒稿，这是快速备选

### 投稿顺序策略

```
第一轮：JAFEB（免费，接收率最高）
  ↓ 如果被拒（约25%概率）
第二轮：JRFM（快速，8周出结果）
  ↓ 如果被拒（约30%概率）
第三轮：IJFS（保底）
```

**预期总成功率**：1 - (0.25 × 0.30 × 0.25) = **98%**（至少一个接受）

---

## 四、简化的方法论（适配Q3）

### 4.1 数据来源

**主数据源**：S&P Capital IQ Pro

**样本筛选**（降低门槛）：
- 地域：新加坡（SGX）、香港（HKEx）、澳大利亚（ASX）
- 市值：> 5000万美元（降低到50M，扩大样本）
- 分析师覆盖：≥ 2（降低到2，原来是3）
- 时间：2018-2024（缩短到6年，原来是8年）
- 目标样本：300+公司，6000+季度观测

**为什么降低筛选标准**：
- Q3期刊对样本量要求相对宽松
- 更重要的是"有代表性"而非"完美数据"
- 降低数据不可行的风险

### 4.2 特征工程（简化版）

**只保留3组特征**（不要过度复杂）：

**组1：分析师特征**（4个）
```python
1. num_analysts          # 分析师数量
2. forecast_dispersion   # (High - Low) / Mean
3. revision_trend        # 最近1个月预测修正方向
4. coverage_change       # 分析师覆盖度变化
```

**组2：财务比率**（8个）
```python
5. pe_ratio              # P/E
6. pb_ratio              # P/B
7. roe                   # ROE
8. roa                   # ROA
9. revenue_growth        # 营收增长率（YoY）
10. debt_to_equity       # 杠杆率
11. current_ratio        # 流动比率
12. market_cap_log       # log(市值)
```

**组3：历史惊喜**（3个）
```python
13. past_surprise_1q     # 上季度惊喜
14. past_surprise_4q_avg # 过去4季度平均
15. surprise_volatility  # 惊喜标准差
```

**总计：15个特征**（不要超过20个，Q3期刊喜欢简洁）

**不做的事情**：
- ❌ 不用LLM提取文本特征（太复杂，A40用不上）
- ❌ 不用FinBERT情感分析（可选，如果时间够再加）
- ❌ 不用宏观变量（增加复杂度，贡献有限）

### 4.3 模型设计（极简版）

**只用2个模型**：

**Baseline: Logistic Regression**
- 目的：建立可解释的基准
- 优势：系数可以直接解释
- 预期准确率：55-60%

**主模型: XGBoost**
- 目的：提升预测性能
- 超参数：5-fold CV + Grid Search
- 预期准确率：62-68%

**不做的事情**：
- ❌ 不用LightGBM对比（一个树模型够了）
- ❌ 不用Random Forest（XGBoost已经是树模型代表）
- ❌ 不用神经网络（过度复杂）

**评估指标**：
- Accuracy（主要指标）
- Precision, Recall, F1（正负样本分别报告）
- AUC-ROC
- Confusion Matrix

### 4.4 可解释性分析（核心卖点）

**SHAP分析**（这是Q3期刊最看重的）：

1. **全局特征重要性**：
   - SHAP Summary Plot（一张图展示所有特征）
   - Top 10特征排序

2. **跨市场对比**：
   - 分别在SGX、HKEx、ASX上训练模型
   - 对比三个市场的特征重要性差异
   - **这是核心贡献点**

3. **子组分析**：
   - 按行业（金融 vs 非金融）
   - 按公司规模（大盘 vs 中小盘）

**不做的事情**：
- ❌ 不做局部SHAP解释（Waterfall Plot）- 太细节
- ❌ 不做LIME对比（一个解释工具够了）

### 4.5 稳健性检验（Q3期刊必需）

**3个简单的稳健性检验**：

1. **时间稳健性**：
   - Train: 2018-2021, Test: 2022-2024
   - 验证模型在新数据上的表现

2. **样本稳健性**：
   - 排除市值最小的20%公司
   - 验证结果是否依然显著

3. **特征稳健性**：
   - 移除分析师特征，只用财务比率
   - 移除财务比率，只用分析师特征
   - 验证哪类特征更重要

**不做的事情**：
- ❌ 不做PEAD回测（增加工作量，Q3期刊不要求）
- ❌ 不做蒙特卡洛模拟（过度复杂）

---

## 五、实验设计（简化版）

### 实验1：描述性统计（最重要）

**目的**：建立亚太市场的"stylized facts"

**内容**：
1. 样本描述：
   - 三个市场的公司数量、行业分布
   - 分析师覆盖度分布
   
2. 惊喜特征：
   - 正负惊喜的比例（是否存在系统性乐观偏差？）
   - 惊喜幅度分布
   - 跨市场对比（SGX vs HKEx vs ASX）
   
3. 特征相关性：
   - 哪些特征与惊喜方向相关性最高？
   - 相关性矩阵热力图

**为什么重要**：Q3期刊的审稿人非常看重描述性统计，这是"实证发现"的核心。

### 实验2：预测性能对比

**对比维度**：
- Logistic Regression vs XGBoost
- 报告准确率、AUC、F1

**预期结果**：
- XGBoost比Logistic提升5-10个百分点
- 如果提升<5%，也没关系，重点是SHAP解释

### 实验3：跨市场对比（核心贡献）

**分别在三个市场上训练和测试**：

| 市场 | 样本量 | 准确率 | Top 3特征 |
|------|--------|--------|----------|
| SGX | ~100公司 | 65% | ? |
| HKEx | ~150公司 | 63% | ? |
| ASX | ~100公司 | 67% | ? |

**分析**：
- 为什么ASX更容易预测？（可能是分析师覆盖度更高）
- 为什么HKEx更难？（可能是信息不对称更严重）
- 不同市场的驱动因素有何不同？

**这是论文的核心卖点**：不是"我的模型更好"，而是"我发现了市场差异"。

### 实验4：稳健性检验

- 时间稳健性（Train 2018-2021, Test 2022-2024）
- 样本稳健性（排除小市值公司）
- 特征稳健性（消融实验）

---

## 六、论文结构（JAFEB格式）

### 标题
"Predicting Analyst Earnings Surprises in Asian Markets: A Machine Learning Approach with Cross-Market Comparison"

### 摘要（200-250词）
- 背景：分析师预测偏差在亚洲市场研究不足
- 方法：XGBoost + SHAP，Capital IQ数据，SGX/HKEx/ASX
- 结果：准确率65%，跨市场差异显著
- 贡献：首次系统比较亚太三市场

### 1. Introduction（1500词）
- 1.1 研究背景：分析师预测的重要性
- 1.2 研究gap：现有研究集中在美股
- 1.3 研究问题：亚太市场的预测可行性
- 1.4 贡献：地域novelty + 跨市场对比
- 1.5 论文结构

### 2. Literature Review（1200词）
- 2.1 分析师预测偏差的理论
- 2.2 机器学习在盈利预测中的应用
- 2.3 亚太市场的特殊性
- 2.4 研究gap总结

### 3. Data and Methodology（1500词）
- 3.1 数据来源（Capital IQ）
- 3.2 样本筛选
- 3.3 变量定义（15个特征）
- 3.4 模型设计（Logistic + XGBoost）
- 3.5 SHAP解释方法
- 3.6 评估指标

### 4. Results（2000词）⭐ 最重要
- 4.1 描述性统计（表格+图表）
- 4.2 预测性能对比（Logistic vs XGBoost）
- 4.3 SHAP特征重要性分析
- 4.4 跨市场对比（SGX vs HKEx vs ASX）
- 4.5 稳健性检验

### 5. Discussion（800词）
- 5.1 主要发现总结
- 5.2 理论解释（为什么市场有差异？）
- 5.3 实践意义（对投资者和分析师的启示）
- 5.4 局限性

### 6. Conclusion（500词）
- 6.1 研究总结
- 6.2 贡献
- 6.3 未来研究方向

**总字数**：约7000-7500词（符合JAFEB要求）

---

## 七、时间线（8周完成）

### 第1周：数据验证与准备
- [ ] 周一-周二：登录Capital IQ，验证数据可行性
- [ ] 周三-周四：导出完整样本数据
- [ ] 周五-周日：数据清洗，处理缺失值
- **里程碑**：获得干净的数据集（300+公司，6000+观测）

### 第2周：描述性统计
- [ ] 周一-周三：计算所有描述性统计
- [ ] 周四-周五：制作表格和图表
- [ ] 周末：写Results第4.1节（描述性统计）
- **里程碑**：完成论文最重要的部分

### 第3周：Baseline模型
- [ ] 周一-周二：特征工程（15个特征）
- [ ] 周三-周四：训练Logistic Regression
- [ ] 周五-周日：评估性能，写Results第4.2节
- **里程碑**：建立基准性能

### 第4周：XGBoost模型
- [ ] 周一-周三：训练XGBoost，超参数调优
- [ ] 周四-周五：SHAP分析
- [ ] 周末：写Results第4.3节
- **里程碑**：完成主模型

### 第5周：跨市场对比
- [ ] 周一-周三：分别在三个市场上训练模型
- [ ] 周四-周五：对比SHAP特征重要性
- [ ] 周末：写Results第4.4节（核心贡献）
- **里程碑**：完成核心实验

### 第6周：稳健性检验 + Introduction/Literature
- [ ] 周一-周二：3个稳健性检验
- [ ] 周三-周四：写Introduction
- [ ] 周五-周日：写Literature Review
- **里程碑**：实验全部完成

### 第7周：完成初稿
- [ ] 周一-周二：写Methodology
- [ ] 周三-周四：写Discussion + Conclusion
- [ ] 周五-周日：全文修改，统一格式
- **里程碑**：初稿完成

### 第8周：润色与投稿
- [ ] 周一-周三：语言润色（Grammarly + 人工）
- [ ] 周四：制作所有图表（高质量）
- [ ] 周五：检查参考文献格式
- [ ] 周末：投稿到JAFEB
- **里程碑**：论文提交

---

## 八、成功标准（现实版）

### 最低标准（必须达到）
- [ ] 在SCIE Q3期刊发表（JAFEB或JRFM或IJFS）
- [ ] 完成时间 ≤ 3个月（包括一次改投）
- [ ] XGBoost准确率 ≥ 60%

### 理想标准
- [ ] 在JAFEB首投即接受（70%概率）
- [ ] XGBoost准确率 ≥ 65%
- [ ] 跨市场对比发现显著差异
- [ ] 审稿周期 ≤ 10周

### 不追求的目标（与Q2策略的区别）
- ❌ 不追求Q1/Q2期刊（接收率太低）
- ❌ 不追求方法创新（Q3不要求）
- ❌ 不追求高引用（Q3期刊IF本身就低）

---

## 九、风险管理（修正版）

### 风险1：数据样本量不足
**触发条件**：符合条件的公司 < 200家  
**应对方案**（按优先级）：
1. 降低市值要求（50M → 20M）
2. 降低分析师覆盖（≥2 → ≥1）
3. 扩大地域（加入日本、韩国、台湾、印度）
4. 缩短时间范围（2018-2024 → 2020-2024）

**最坏情况**：如果样本 < 150家，立即切换到**方向四（破产预测）**

### 风险2：模型性能不佳
**触发条件**：XGBoost准确率 < 58%（接近随机）  
**应对方案**：
1. 转向解释性研究：重点分析"为什么难预测"
2. 改为回归任务：预测surprise幅度而非方向
3. 降低期刊目标：投Cogent Economics（Q3，接收率更高）

**关键**：Q3期刊对模型性能要求不高，60%准确率就可以接受

### 风险3：JAFEB拒稿
**触发条件**：首投被拒（25%概率）  
**应对方案**：
1. 立即改投JRFM（1周内完成修改）
2. 根据审稿意见快速调整
3. 不要等待，时间宝贵

**预期**：即使JAFEB拒稿，JRFM + IJFS的组合成功率仍有90%+

### 风险4：时间不够
**触发条件**：第4周还没完成Baseline模型  
**应对方案**：
1. 跳过稳健性检验（Q3期刊可以接受）
2. 简化跨市场对比（只做SGX vs HKEx）
3. 延长到10周完成

---

## 十、资源需求（简化版）

### 计算资源
- **M5 Mac**：足够完成所有任务
- **A40 GPU**：不需要（不做LLM fine-tune）

### 软件工具
```python
# 核心库
pandas, numpy          # 数据处理
scikit-learn          # Logistic Regression
xgboost               # XGBoost
shap                  # SHAP解释
matplotlib, seaborn   # 可视化

# 可选
statsmodels           # 稳健性检验
```

### 数据访问
- Capital IQ Pro（已有）
- 不需要其他数据源

### 时间投入
- 每周12-15小时
- 总计：96-120小时（比原计划少50%）

---

## 十一、与原计划的对比

| 维度 | 原计划（Q2） | 修正计划（Q3） | 改进 |
|------|------------|--------------|------|
| **目标期刊** | RIBAF (Q2) | JAFEB (Q3) | 接收率从35%→70% |
| **预期接收率** | 65%（高估） | 70-75%（现实） | 更准确 |
| **时间线** | 3-4个月 | 2个月 | 快50% |
| **方法复杂度** | 高（多模型+LLM） | 低（2模型） | 降低风险 |
| **特征数量** | 20-30个 | 15个 | 更简洁 |
| **GPU需求** | A40（fine-tune） | 不需要 | 降低门槛 |
| **论文字数** | 8000-10000 | 7000-7500 | 更快完成 |
| **稳健性检验** | 5个 | 3个 | 够用即可 |

---

## 十二、下一步行动（本周）

### 今天（立即开始）
1. [ ] 阅读本计划（30分钟）
2. [ ] 登录Capital IQ Pro，验证能否访问（15分钟）
3. [ ] 阅读JAFEB最新3篇论文，了解期刊风格（1小时）

### 周一-周二
4. [ ] 在Capital IQ中设置筛选条件（见修正版清单）
5. [ ] 记录样本量：SGX ___ 家，HKEx ___ 家，ASX ___ 家
6. [ ] 决策：样本量是否 ≥ 200家？

### 周三-周五
7. [ ] 如果样本量OK：导出完整数据
8. [ ] 如果样本量不足：调整筛选条件或切换方向
9. [ ] 周五晚：完成数据清洗

### 周末
10. [ ] 开始描述性统计
11. [ ] 制作第一批图表

---

## 附录：JAFEB投稿检查清单

### 投稿前必查项目
- [ ] 字数：6000-8000词
- [ ] 格式：APA 7th edition
- [ ] 摘要：200-250词，包含背景/方法/结果/贡献
- [ ] 关键词：5-7个
- [ ] 图表：高质量（300 DPI），有标题和注释
- [ ] 参考文献：至少30篇，近5年文献 ≥ 50%
- [ ] 数据来源：明确标注"Data sourced from S&P Capital IQ Pro"
- [ ] 利益冲突声明：无
- [ ] 作者贡献：单作者或明确分工
- [ ] Cover Letter：说明为什么适合JAFEB

---

**总结**：这是一个**现实的、可执行的、高成功率的**Q3发表计划。核心是"稳"而非"好"，"快"而非"完美"。8周完成初稿，70%+概率在JAFEB接受，即使被拒也有JRFM/IJFS保底。

准备好开始了吗？
# 第1周数据验证清单（Q3策略修正版）

**目标**：在本周内验证Capital IQ数据的可行性，决定是否继续方向一

**关键变化**：降低筛选标准，提高数据可行性

---

## 任务1：验证亚太市场Estimates数据覆盖度 ⚠️ 最高优先级

### 登录Capital IQ Pro
- [ ] 访问 https://www.capitaliq.com
- [ ] 使用NTU账号登录
- [ ] 确认能访问Estimates模块

### 筛选条件（降低标准版）

在 **Screening** 模块中设置：

**地理范围**：
- [ ] 新加坡（SGX）
- [ ] 香港（HKEx）
- [ ] 澳大利亚（ASX）

**公司筛选**（比原计划宽松）：
- [ ] 市值 > **5000万美元**（原来是1亿，降低了）
- [ ] 分析师覆盖数 ≥ **2**（原来是3，降低了）
- [ ] 公司状态：Active（排除已退市）

**时间范围**（缩短）：
- [ ] **2018-2024**（6年，原来是8年）

### 关键验证点

记录以下数据：

**1. 样本量检查**：

| 市场 | 公司数量 | 备注 |
|------|---------|------|
| 新加坡（SGX） | _______ 家 | 目标 ≥ 80家 |
| 香港（HKEx） | _______ 家 | 目标 ≥ 120家 |
| 澳大利亚（ASX） | _______ 家 | 目标 ≥ 80家 |
| **总计** | _______ 家 | **目标 ≥ 200家** |

**判断标准**：
- ✅ 总数 ≥ 250家 → 数据充足，继续方向一
- 🟡 总数 150-250家 → 可以做，但需要进一步降低标准
- 🔴 总数 < 150家 → 立即切换到方向四（破产预测）

**2. 分析师覆盖度检查**：

- 平均每家公司的分析师数量：_______
- 中位数：_______
- 分析师数 ≥ 3 的公司占比：_______%

**判断标准**：
- ✅ 中位数 ≥ 2 → 可以接受
- 🔴 中位数 < 2 → 数据质量不足

**3. 时间跨度检查**：

- Estimates历史数据最早到：_______ 年
- 平均每家公司有多少个季度数据：_______ 个

**判断标准**：
- ✅ 平均 ≥ 12个季度（3年）→ 足够
- 🟡 平均 8-12个季度 → 勉强可以
- 🔴 平均 < 8个季度 → 样本太少

---

## 任务2：导出Pilot数据（50家公司）

**注意**：只导出50家（原来是100家），快速验证

### 需要导出的字段（简化版）

**公司基本信息**：
- Company ID
- Company Name
- Country
- Industry (GICS Sector)
- Market Cap

**Estimates数据**（季度）：
- Report Date（财报发布日期）
- Fiscal Period（财季，如2024Q3）
- **EPS Actual**（实际EPS）⭐ 核心
- **EPS Mean Estimate**（分析师共识预测）⭐ 核心
- **Number of Analysts**（分析师数量）⭐ 核心
- EPS High Estimate（最高预测）
- EPS Low Estimate（最低预测）

**财务数据**（季度，只要关键指标）：
- P/E Ratio
- ROE
- Revenue（营收）
- Total Assets（总资产）

### 导出步骤

**方法1：使用Capital IQ界面直接导出**（推荐，最快）

1. [ ] 在Screening结果中选择前50家公司（每个市场各选15-20家）
2. [ ] 点击 **Export** → **Custom Export**
3. [ ] 添加上述字段
4. [ ] 时间范围：2018Q1 - 2024Q4，季度频率
5. [ ] 导出为CSV格式
6. [ ] 保存到：`~/ai-finance-paper/data/pilot/pilot_sample_50.csv`

**方法2：使用Excel Plugin**（如果方法1不行）

- 参考 `capital-iq-data-extraction-guide.md` 中的详细步骤

---

## 任务3：数据质量检查（Python代码）

### 创建检查脚本

将以下代码保存为 `data_quality_check.py`：

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
df = pd.read_csv('data/pilot/pilot_sample_50.csv')

print("=" * 60)
print("数据质量检查报告")
print("=" * 60)

# 检查1：基本信息
print("\n【1. 基本信息】")
print(f"总行数: {len(df)}")
print(f"公司数: {df['Company ID'].nunique()}")
print(f"时间范围: {df['Report Date'].min()} 到 {df['Report Date'].max()}")
print(f"平均每家公司的季度数: {len(df) / df['Company ID'].nunique():.1f}")

# 检查2：缺失率
print("\n【2. 关键字段缺失率】")
critical_fields = ['EPS Actual', 'EPS Mean Estimate', 'Number of Analysts']
for field in critical_fields:
    if field in df.columns:
        missing_rate = df[field].isnull().sum() / len(df) * 100
        status = "✅" if missing_rate < 15 else "🔴"
        print(f"{status} {field}: {missing_rate:.1f}% 缺失")
    else:
        print(f"⚠️  {field}: 字段不存在")

# 检查3：分析师覆盖度
print("\n【3. 分析师覆盖度】")
if 'Number of Analysts' in df.columns:
    analyst_stats = df['Number of Analysts'].describe()
    print(f"最小值: {analyst_stats['min']:.0f}")
    print(f"25%分位: {analyst_stats['25%']:.0f}")
    print(f"中位数: {analyst_stats['50%']:.0f}")
    print(f"75%分位: {analyst_stats['75%']:.0f}")
    print(f"最大值: {analyst_stats['max']:.0f}")
    
    # 判断
    if analyst_stats['50%'] >= 2:
        print("✅ 中位数 ≥ 2，覆盖度合格")
    else:
        print("🔴 中位数 < 2，覆盖度不足")

# 检查4：Surprise分布
print("\n【4. Earnings Surprise分布】")
if 'EPS Actual' in df.columns and 'EPS Mean Estimate' in df.columns:
    # 计算surprise
    df['surprise'] = df['EPS Actual'] - df['EPS Mean Estimate']
    df['surprise_direction'] = np.sign(df['surprise'])
    
    # 统计
    surprise_counts = df['surprise_direction'].value_counts()
    print(f"正惊喜（实际>预测）: {surprise_counts.get(1.0, 0)} ({surprise_counts.get(1.0, 0)/len(df)*100:.1f}%)")
    print(f"负惊喜（实际<预测）: {surprise_counts.get(-1.0, 0)} ({surprise_counts.get(-1.0, 0)/len(df)*100:.1f}%)")
    print(f"无惊喜（实际=预测）: {surprise_counts.get(0.0, 0)} ({surprise_counts.get(0.0, 0)/len(df)*100:.1f}%)")
    
    # 判断样本平衡性
    positive_ratio = surprise_counts.get(1.0, 0) / len(df)
    if 0.4 <= positive_ratio <= 0.6:
        print("✅ 正负样本相对均衡")
    else:
        print("⚠️  样本不平衡，可能需要处理")

# 检查5：跨市场分布
print("\n【5. 市场分布】")
if 'Country' in df.columns:
    market_counts = df.groupby('Country')['Company ID'].nunique()
    print(market_counts)
    
    # 判断
    if len(market_counts) >= 3:
        print("✅ 覆盖3个市场")
    else:
        print("⚠️  市场覆盖不足")

# 检查6：异常值
print("\n【6. 异常值检查】")
if 'surprise' in df.columns and 'EPS Mean Estimate' in df.columns:
    # 计算相对surprise
    df['surprise_pct'] = df['surprise'] / df['EPS Mean Estimate'].abs() * 100
    
    # 找极端值
    extreme = df[df['surprise_pct'].abs() > 200]
    print(f"极端异常值（surprise > 200%）: {len(extreme)} 条")
    
    if len(extreme) > len(df) * 0.05:
        print("⚠️  异常值较多，需要检查数据质量")
    else:
        print("✅ 异常值在合理范围")

# 生成可视化
print("\n【7. 生成可视化】")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 图1：分析师覆盖度分布
if 'Number of Analysts' in df.columns:
    axes[0, 0].hist(df['Number of Analysts'].dropna(), bins=20, edgecolor='black')
    axes[0, 0].set_title('Analyst Coverage Distribution')
    axes[0, 0].set_xlabel('Number of Analysts')
    axes[0, 0].set_ylabel('Frequency')

# 图2：Surprise方向分布
if 'surprise_direction' in df.columns:
    surprise_counts.plot(kind='bar', ax=axes[0, 1], color=['red', 'gray', 'green'])
    axes[0, 1].set_title('Surprise Direction Distribution')
    axes[0, 1].set_xlabel('Direction (-1: Negative, 0: Zero, 1: Positive)')
    axes[0, 1].set_ylabel('Count')

# 图3：市场分布
if 'Country' in df.columns:
    market_counts.plot(kind='bar', ax=axes[1, 0], color='steelblue')
    axes[1, 0].set_title('Company Distribution by Market')
    axes[1, 0].set_xlabel('Market')
    axes[1, 0].set_ylabel('Number of Companies')

# 图4：Surprise幅度分布
if 'surprise_pct' in df.columns:
    # 去除极端值后绘图
    surprise_clean = df['surprise_pct'].dropna()
    surprise_clean = surprise_clean[(surprise_clean > -100) & (surprise_clean < 100)]
    axes[1, 1].hist(surprise_clean, bins=30, edgecolor='black')
    axes[1, 1].set_title('Surprise Magnitude Distribution')
    axes[1, 1].set_xlabel('Surprise (%)')
    axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('data/pilot/data_quality_report.png', dpi=300)
print("✅ 可视化已保存到: data/pilot/data_quality_report.png")

# 最终判断
print("\n" + "=" * 60)
print("【最终判断】")
print("=" * 60)

# 计算通过的检查项
checks_passed = 0
total_checks = 5

# 检查1：样本量
if df['Company ID'].nunique() >= 40:  # 50家公司的80%
    checks_passed += 1
    print("✅ 检查1：样本量充足")
else:
    print("🔴 检查1：样本量不足")

# 检查2：缺失率
if 'EPS Actual' in df.columns:
    missing_rate = df['EPS Actual'].isnull().sum() / len(df)
    if missing_rate < 0.15:
        checks_passed += 1
        print("✅ 检查2：EPS数据缺失率合格")
    else:
        print("🔴 检查2：EPS数据缺失率过高")

# 检查3：分析师覆盖
if 'Number of Analysts' in df.columns:
    if df['Number of Analysts'].median() >= 2:
        checks_passed += 1
        print("✅ 检查3：分析师覆盖度合格")
    else:
        print("🔴 检查3：分析师覆盖度不足")

# 检查4：时间跨度
avg_quarters = len(df) / df['Company ID'].nunique()
if avg_quarters >= 12:
    checks_passed += 1
    print("✅ 检查4：时间跨度充足")
else:
    print("🔴 检查4：时间跨度不足")

# 检查5：市场覆盖
if 'Country' in df.columns:
    if df['Country'].nunique() >= 3:
        checks_passed += 1
        print("✅ 检查5：市场覆盖充足")
    else:
        print("🔴 检查5：市场覆盖不足")

print(f"\n通过检查项: {checks_passed}/{total_checks}")

if checks_passed >= 4:
    print("\n🎉 结论：数据质量良好，可以继续方向一")
    print("   下一步：扩大样本到全量（250+公司）")
elif checks_passed >= 3:
    print("\n⚠️  结论：数据质量一般，需要调整筛选条件")
    print("   建议：降低市值要求或扩大地域范围")
else:
    print("\n🔴 结论：数据质量不足，建议切换到方向四（破产预测）")
    print("   原因：亚太市场的分析师覆盖度可能不如预期")
```

### 运行检查

```bash
cd ~/ai-finance-paper
python data_quality_check.py
```

### 查看结果

- [ ] 查看终端输出的检查报告
- [ ] 打开 `data/pilot/data_quality_report.png` 查看可视化
- [ ] 记录通过的检查项数量：_______ / 5

---

## 任务4：决策点（第1周结束）

### 决策矩阵

| 通过检查项 | 样本量 | 决策 | 下一步 |
|----------|--------|------|--------|
| 5/5 | ≥250家 | ✅ 全力推进方向一 | 扩大到全量样本 |
| 4/5 | 200-250家 | ✅ 继续方向一 | 可能需要微调 |
| 3/5 | 150-200家 | 🟡 谨慎继续 | 降低筛选标准 |
| ≤2/5 | <150家 | 🔴 立即切换 | 方向四（破产预测） |

### 如果继续方向一

**第2周任务**：
1. 扩大样本到全量（250-300家公司）
2. 导出完整的Estimates + 财务数据
3. 开始描述性统计

### 如果切换到方向四

**立即行动**：
1. 在Capital IQ中筛选破产/退市公司
2. 目标：破产公司100家 + 正常公司500家
3. 导出财务数据（不需要Estimates）
4. 2周内完成Baseline模型

---

## 任务5：并行准备备选数据（保险）

**即使方向一看起来可行，也要花1小时准备备选**

### 在Capital IQ中快速筛选破产公司

**筛选条件**：
- Geography: Singapore, Hong Kong, Australia
- Company Status: **Inactive** or **Delisted**
- Reason: Bankruptcy, Financial Distress, Liquidation
- Time: 2010-2024

**记录**：
- 破产公司数量：_______ 家
- 目标：≥ 80家

**如果破产公司 ≥ 80家**：
- 这是可行的备选方案
- 如果方向一失败，可以立即切换

**如果破产公司 < 50家**：
- 备选方案也不可行
- 需要考虑其他方向（如ESG评级预测）

---

## 本周时间分配

| 任务 | 时间 | 截止日期 | 优先级 |
|------|------|---------|--------|
| 任务1：验证样本量 | 1-2小时 | 周二 | ⚠️ 最高 |
| 任务2：导出Pilot数据 | 1-2小时 | 周三 | ⚠️ 最高 |
| 任务3：数据质量检查 | 1小时 | 周四 | 高 |
| 任务4：决策 | 30分钟 | 周五 | 高 |
| 任务5：备选数据 | 1小时 | 周六 | 中 |
| 阅读JAFEB论文 | 1-2小时 | 周日 | 中 |

**总计：5-8小时**（比原计划少）

---

## 成功标准

### 本周结束时，你应该能回答：

1. **数据可行性**：
   - [ ] 亚太市场样本量是否 ≥ 200家？
   - [ ] 分析师覆盖度中位数是否 ≥ 2？
   - [ ] EPS数据缺失率是否 < 15%？

2. **方向决策**：
   - [ ] 继续方向一（盈利惊喜预测）？
   - [ ] 切换方向四（破产预测）？
   - [ ] 还是需要调整筛选条件？

3. **时间规划**：
   - [ ] 如果继续方向一，第2周的具体任务是什么？
   - [ ] 预计多久能完成初稿？

---

## 常见问题

### Q1：如果Capital IQ界面和描述不一样怎么办？
**A**：Capital IQ的界面可能因版本更新而变化。关键是找到：
- Screening功能（筛选公司）
- Estimates数据（分析师预测）
- Export功能（导出数据）

如果找不到，联系NTU图书馆：library@ntu.edu.sg

### Q2：如果样本量刚好在临界点（如180家）怎么办？
**A**：先导出Pilot数据，运行质量检查。如果其他4项检查都通过，180家也可以接受。Q3期刊对样本量要求不严格。

### Q3：如果三个市场的样本量严重不平衡怎么办？
**A**：没关系。即使是SGX 50家 + HKEx 150家 + ASX 50家，也可以做。重点是"跨市场对比"，不是"样本完全均衡"。

### Q4：如果第1周就发现数据完全不可行怎么办？
**A**：立即切换到方向四（破产预测）。不要浪费时间强行推进。破产预测的数据要求更低，成功率更高。

---

## 联系支持

### NTU图书馆
- 邮箱：library@ntu.edu.sg
- 电话：+65 6790 6666
- 在线咨询：https://www.ntu.edu.sg/library/research-support

### Capital IQ技术支持
- 平台内 **Help** → **Contact Support**

---

**记住**：第1周的目标不是"完美的数据"，而是"可行的数据"。只要通过3/5项检查，就可以继续。不要追求完美，追求可行。
