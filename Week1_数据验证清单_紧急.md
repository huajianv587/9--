# Week 1 数据验证清单（本周必须完成）🔴

**目标**：验证Capital IQ数据可行性，决定是否继续方向一  
**时间投入**：6-9小时（分散到7天）  
**决策点**：Week 1结束时做Go/No-Go决策

---

## 验证任务清单

### ✅ Task 1：Capital IQ访问与pilot样本导出（Day 1-2，2小时）

#### 步骤
1. **登录Capital IQ Pro**
   - 访问：https://www.capitaliq.com
   - 使用NTU机构账号登录
   - 确认可以访问Estimates模块

2. **设置筛选器**
   ```
   地区：Singapore (SGX) + Hong Kong (HKEx)
   市值：> USD 100M
   上市状态：Active
   数据可用性：Has Estimates Data
   ```

3. **导出pilot样本**
   - 目标：100家公司
   - 导出字段：
     * Company Name
     * Ticker Symbol
     * Market Cap (Latest)
     * Sector (GICS)
     * Country
     * Number of Analysts (Latest)

4. **保存文件**
   - 格式：CSV
   - 文件名：`pilot_companies_sgx_hkex.csv`
   - 保存到：`data/raw/`

#### 成功标准
- [ ] 成功导出100家公司列表
- [ ] 至少50家来自SGX，50家来自HKEx
- [ ] 所有公司市值 > USD 100M

#### 如果失败
- 如果无法访问Capital IQ → 联系NTU图书馆确认权限
- 如果公司数量不足 → 降低市值门槛到USD 50M

---

### ✅ Task 2：Estimates历史数据验证（Day 3，2小时）

#### 步骤
1. **选择10家pilot公司**（随机抽样）

2. **导出Estimates数据**
   - 时间范围：2019 Q1 - 2024 Q4（6年，24个季度）
   - 字段清单：
     * Company ID / Ticker
     * Fiscal Quarter
     * Announcement Date
     * **Consensus EPS Forecast (Mean)** ← 核心字段
     * **Actual EPS (Reported)** ← 核心字段
     * Number of Analysts
     * Forecast Dispersion (Std Dev)
     * Forecast High / Low

3. **数据质量检查**
   ```python
   import pandas as pd
   
   # 加载数据
   df = pd.read_csv('data/raw/pilot_estimates.csv')
   
   # 检查1：历史深度
   date_range = df['fiscal_quarter'].nunique()
   print(f"历史季度数：{date_range}")  # 目标：≥20个季度
   
   # 检查2：缺失率
   missing_consensus = df['consensus_eps'].isna().sum() / len(df)
   missing_actual = df['actual_eps'].isna().sum() / len(df)
   print(f"Consensus EPS缺失率：{missing_consensus:.1%}")  # 目标：<20%
   print(f"Actual EPS缺失率：{missing_actual:.1%}")      # 目标：<20%
   
   # 检查3：可用样本量
   valid_rows = df.dropna(subset=['consensus_eps', 'actual_eps'])
   print(f"有效样本数：{len(valid_rows)}")  # 目标：>150（10公司×20季度×75%）
   ```

4. **保存验证报告**
   - 文件名：`data_validation_report_day3.txt`

#### 成功标准
- [ ] 历史数据覆盖≥5年（20个季度）
- [ ] Consensus EPS缺失率<20%
- [ ] Actual EPS缺失率<20%
- [ ] 10家公司至少有150条有效记录

#### 如果失败
- **历史深度不足**（<5年）→ 样本量可能不够，Week 2启动方向四验证
- **缺失率过高**（>30%）→ 数据质量不足，考虑切换方向四
- **有效样本<100条** → 立即切换方向四

---

### ✅ Task 3：分析师覆盖度统计（Day 4，1.5小时）

#### 步骤
1. **统计分析师覆盖**
   ```python
   # 对100家pilot公司，统计每家的分析师数量
   df_companies = pd.read_csv('data/raw/pilot_companies_sgx_hkex.csv')
   
   # 筛选：≥3个分析师覆盖
   df_covered = df_companies[df_companies['num_analysts'] >= 3]
   
   print(f"总公司数：{len(df_companies)}")
   print(f"≥3个分析师覆盖：{len(df_covered)}")
   print(f"覆盖率：{len(df_covered)/len(df_companies):.1%}")
   
   # 按市场分组
   coverage_by_market = df_covered.groupby('country').size()
   print("\n各市场覆盖情况：")
   print(coverage_by_market)
   ```

2. **评估样本量**
   - 如果≥3个分析师的公司数 ≥ 50家 → OK
   - 如果30-50家 → 考虑降低标准到≥2个分析师
   - 如果<30家 → 需要扩大市场（加入澳大利亚ASX）

#### 成功标准
- [ ] ≥50家公司有≥3个分析师覆盖
- [ ] SGX和HKEx都有足够样本（各≥20家）
- [ ] 预估最终样本量：50公司 × 20季度 = 1000条记录

#### 如果失败
- **覆盖公司<50家** → 方案A：降低到≥2个分析师；方案B：扩大到ASX
- **某个市场样本太少** → 调整市场组合（如：HKEx + ASX）

---

### ✅ Task 4：文本数据获取测试（Day 5，2小时）

#### 步骤
1. **随机选10家公司**

2. **尝试获取年报文本**
   - 在Capital IQ中搜索公司
   - 进入"Filings & Reports"模块
   - 查找：Annual Report / 10-K / 年报
   - 测试下载格式：PDF / HTML / Text

3. **测试批量导出**
   - 方法1：Capital IQ Excel Plugin（推荐）
   - 方法2：手动下载PDF，用PyPDF2提取
   - 方法3：如果都不行 → 使用Capital IQ新闻摘要代替

4. **提取MD&A部分**（如果可获取）
   ```python
   # 简单测试：提取文本长度
   import PyPDF2
   
   def extract_text_from_pdf(pdf_path):
       with open(pdf_path, 'rb') as f:
           reader = PyPDF2.PdfReader(f)
           text = ""
           for page in reader.pages:
               text += page.extract_text()
       return text
   
   # 测试10份年报
   for company in test_companies:
       text = extract_text_from_pdf(f"data/raw/reports/{company}_annual.pdf")
       print(f"{company}: {len(text)} characters")
   ```

#### 成功标准
- [ ] 能够获取至少8/10家公司的年报文本
- [ ] 文本长度合理（>5000字符）
- [ ] 有可行的批量处理方案

#### 如果失败
- **无法批量获取年报** → 放弃文本特征，只用结构化+分析师特征
- **文本质量差**（扫描件、乱码）→ 改用Capital IQ新闻摘要
- **完全无法获取** → 不影响项目，继续用结构化特征

---

### ✅ Task 5：构造surprise标签与初步分析（Day 6-7，2.5小时）

#### 步骤
1. **构造标签**
   ```python
   import numpy as np
   
   # 加载Estimates数据
   df = pd.read_csv('data/raw/pilot_estimates.csv')
   
   # 计算surprise
   df['surprise_raw'] = df['actual_eps'] - df['consensus_eps']
   df['surprise_direction'] = np.sign(df['surprise_raw'])  # 1: 正向, -1: 负向, 0: 符合
   df['surprise_magnitude'] = df['surprise_raw'] / np.abs(df['consensus_eps'])
   
   # 二分类标签（去掉0）
   df['surprise_binary'] = df['surprise_direction'].replace(0, np.nan)
   df_binary = df.dropna(subset=['surprise_binary'])
   
   # 统计分布
   print("Surprise方向分布：")
   print(df['surprise_direction'].value_counts())
   print(f"\n正向惊喜比例：{(df['surprise_direction']==1).sum()/len(df):.1%}")
   print(f"负向惊喜比例：{(df['surprise_direction']==-1).sum()/len(df):.1%}")
   ```

2. **可视化**
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   # 图1：Surprise分布
   plt.figure(figsize=(10, 4))
   plt.subplot(1, 2, 1)
   sns.histplot(df['surprise_magnitude'].clip(-1, 1), bins=50)
   plt.title('Surprise Magnitude Distribution')
   
   # 图2：时间趋势
   plt.subplot(1, 2, 2)
   df.groupby('fiscal_quarter')['surprise_direction'].mean().plot()
   plt.title('Surprise Direction Over Time')
   plt.tight_layout()
   plt.savefig('outputs/figures/pilot_surprise_distribution.png')
   ```

3. **跨市场对比**
   ```python
   # 按市场分组
   market_stats = df.groupby('country').agg({
       'surprise_direction': ['mean', 'std'],
       'surprise_magnitude': ['mean', 'std']
   })
   print("\n各市场Surprise统计：")
   print(market_stats)
   ```

#### 成功标准
- [ ] 标签构造成功，无异常值
- [ ] 正向/负向惊喜分布相对平衡（不是90%/10%）
- [ ] 有明显的时间趋势或市场差异（说明有研究价值）

#### 如果失败
- **标签严重不平衡**（如95%正向）→ 调整标签定义或筛选条件
- **无明显模式** → 不影响，ML模型可能仍能发现隐藏模式

---

## Week 1结束：Go/No-Go决策

### 决策矩阵

| 验证项 | 通过标准 | 状态 | 权重 |
|-------|---------|------|------|
| Estimates历史深度 | ≥5年（20季度） | [ ] | 🔴 关键 |
| 数据缺失率 | <20% | [ ] | 🔴 关键 |
| 分析师覆盖公司数 | ≥50家 | [ ] | 🔴 关键 |
| 有效样本量 | ≥1000条 | [ ] | 🟡 重要 |
| 文本数据可获取 | ≥8/10成功 | [ ] | 🟢 加分项 |

### 决策规则

#### ✅ 继续方向一（3个关键项都通过）
- Estimates数据≥5年 ✓
- 缺失率<20% ✓
- ≥50家公司符合条件 ✓

**下一步**：
- Week 2：扩大样本到500家，导出完整数据
- Week 3：特征工程 + Baseline模型
- Week 4：SHAP分析 + 跨市场对比

#### ⚠️ 并行验证方向四（1-2个关键项不通过）
- 历史深度不足（<5年）或
- 缺失率过高（>30%）或
- 覆盖公司太少（<30家）

**下一步**：
- Week 2：同时拉取亚太破产/退市公司数据
- 对比两个方向的数据质量
- Week 3做最终方向选择

#### 🔴 立即切换方向四（数据完全不可用）
- 无法访问Capital IQ Estimates或
- 有效样本<500条或
- 数据质量无法支撑ML建模

**下一步**：
- 立即启动方向四：破产预测 + XAI + 亚太
- 放弃方向一

---

## 时间分配建议

| 日期 | 任务 | 时间 | 累计 |
|-----|------|------|------|
| Day 1-2 | Task 1: 导出pilot样本 | 2h | 2h |
| Day 3 | Task 2: Estimates数据验证 | 2h | 4h |
| Day 4 | Task 3: 分析师覆盖统计 | 1.5h | 5.5h |
| Day 5 | Task 4: 文本数据测试 | 2h | 7.5h |
| Day 6-7 | Task 5: 标签构造与分析 | 2.5h | 10h |

**总时间**：10小时（分散到7天，每天1-2小时）

---

## 输出文件清单

### 必须产出
- [ ] `data/raw/pilot_companies_sgx_hkex.csv` - 100家公司列表
- [ ] `data/raw/pilot_estimates.csv` - Estimates数据（10家×24季度）
- [ ] `data_validation_report_day3.txt` - 数据质量报告
- [ ] `outputs/figures/pilot_surprise_distribution.png` - Surprise分布图
- [ ] `Week1_Decision_Report.md` - 决策报告（Go/No-Go）

### 可选产出
- [ ] `data/raw/reports/` - 年报PDF文件（如果可获取）
- [ ] `analyst_coverage_stats.csv` - 分析师覆盖统计

---

## 常见问题与解决方案

### Q1: 无法登录Capital IQ
**解决**：
1. 确认使用NTU机构网络（校园网或VPN）
2. 联系NTU图书馆：library@ntu.edu.sg
3. 备选：使用Bloomberg Terminal（如果有权限）

### Q2: 找不到Estimates模块
**解决**：
1. 在Capital IQ主界面搜索公司
2. 进入公司页面 → "Estimates" tab
3. 或使用Excel Plugin：CIQ → Estimates → Consensus

### Q3: 数据导出格式混乱
**解决**：
1. 优先使用Excel Plugin（格式最规范）
2. 手动调整列名和日期格式
3. 参考：`docs/capital_iq_export_schema.md`

### Q4: 亚太公司分析师覆盖太少
**解决**：
1. 降低标准：≥2个分析师（而非3个）
2. 扩大市场：加入澳大利亚(ASX)、韩国(KRX)
3. 聚焦大盘股：市值>USD 500M

---

## 紧急联系

**数据问题**：
- NTU图书馆数据库支持：library@ntu.edu.sg
- Capital IQ技术支持：https://www.capitaliq.com/support

**项目问题**：
- 导师/合作者
- 或立即切换到方向四（破产预测）

---

**创建日期**：2026-05-31  
**最后更新**：2026-05-31  
**状态**：🔴 本周必须完成
