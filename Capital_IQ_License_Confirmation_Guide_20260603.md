# Capital IQ 数据授权确认指南

日期：2026-06-03
问题：确认 Data Availability 声明措辞是否符合机构 Capital IQ 授权条款

---

## 当前稿件中的数据可用性声明

```
Data Availability

The data used in this study were obtained from S&P Capital IQ under 
institutional database access and are subject to database licensing and 
redistribution restrictions. The author cannot redistribute raw Capital IQ 
exports or firm-level Capital IQ-derived panels. Researchers with their own 
Capital IQ access may reconstruct the sample using the reported variable 
definitions, sample filters, and replication code. Non-proprietary aggregate 
tables and audit outputs are included in the submission materials.
```

---

## 这段措辞的关键点

### ✅ **我们声明了**：
1. 数据来自 S&P Capital IQ
2. 受机构数据库访问授权
3. 受许可证和再分发限制约束
4. **不会**再分发原始 Capital IQ 导出数据
5. **不会**再分发公司级 Capital IQ 派生面板
6. 其他研究者需要自己的 Capital IQ 访问权限
7. 会提供变量定义、样本筛选条件和复制代码
8. 会提供非专有的汇总表格和审计输出

### ✅ **我们没有做**：
- ❌ 上传任何原始 Capital IQ Excel 文件
- ❌ 上传任何包含 Capital IQ 公司级数据的面板（.csv, .parquet 等）
- ❌ 在补充材料中包含可识别公司的 Capital IQ 派生数据
- ❌ 声称数据"公开可用"（我们明确说了需要授权）

---

## 你需要确认什么

### **选项A：自行判断（推荐用于常规学术授权）**

如果你的机构 Capital IQ 订阅是**标准学术研究授权**，通常允许：
- ✅ 在学术论文中报告研究结果
- ✅ 发表汇总统计表格
- ✅ 引用 Capital IQ 作为数据来源
- ✅ 提供方法论描述和变量定义
- ❌ 不允许再分发原始数据或微观数据

**如果符合上述标准学术授权，当前措辞是保守且合规的。**

**你的判断**：
- [ ] ✅ 我确认当前措辞符合我的机构授权，可以使用
- [ ] ⚠️ 我不确定，需要进一步检查（见选项B）
- [ ] ❌ 当前措辞有问题，需要修改（见选项C）

---

### **选项B：联系图书馆确认（最保险）**

如果你不确定，可以：

1. **联系你的大学图书馆**
   - 找到负责 Capital IQ / S&P 数据库的图书馆员
   - 通常在图书馆网站的"数据库"或"商业数据库"页面有联系方式

2. **发送以下邮件**：

```
主题：Capital IQ 学术出版数据使用政策咨询

您好，

我正在使用学校的 S&P Capital IQ 订阅进行学术研究，准备投稿到 SSCI 
期刊。我想确认以下数据使用方式是否符合我们的授权条款：

1. 在论文中引用 Capital IQ 作为数据来源
2. 在论文中报告汇总统计表格（如均值、标准差、样本量）
3. 在数据可用性声明中说明数据来自 Capital IQ，受授权限制，
   不会再分发原始数据
4. 向期刊提供变量定义和方法论描述（不含原始数据）

我不会上传任何原始 Capital IQ 导出文件或公司级微观数据。

请问这样的使用方式是否符合我们学校的 Capital IQ 授权条款？

谢谢！

[你的姓名]
[你的院系]
```

3. **等待回复**（通常 1-2 个工作日）

4. **根据回复**：
   - 如果确认可以：继续使用当前措辞 ✅
   - 如果需要修改：见选项C

---

### **选项C：修改措辞（如果图书馆要求）**

如果图书馆反馈需要更保守的措辞，可以改为：

**替代版本1（更保守）**：
```
Data Availability

The empirical analysis uses data from S&P Capital IQ, which is a proprietary 
commercial database available under institutional subscription. Due to 
licensing restrictions, the author cannot share the underlying microdata. 
Researchers with institutional access to S&P Capital IQ can reconstruct the 
sample using the variable definitions, sample filters, and selection criteria 
described in the manuscript. Summary statistics and non-proprietary analytical 
outputs are provided in the submission materials.
```

**替代版本2（最保守）**：
```
Data Availability

This study uses data from S&P Capital IQ, a proprietary commercial database. 
Licensing restrictions prohibit sharing of the underlying data. Researchers 
may obtain access through institutional subscriptions to S&P Capital IQ.
```

**替代版本3（如果图书馆要求署名 S&P Global）**：
```
Data Availability

The data used in this study were obtained from S&P Capital IQ (S&P Global 
Market Intelligence) under institutional database access and are subject to 
licensing restrictions. The author cannot redistribute the underlying data. 
Researchers with S&P Capital IQ access may reconstruct the sample using the 
reported methodology. Summary statistics are provided in the submission 
materials.
```

---

## 修改数据可用性声明的步骤

如果需要修改：

1. **打开文件**：
   - `submission_package/ael_strict_v2_20260603/Manuscript_AEL_strict_v2_draft.docx`
   - `submission_package/ael_strict_v2_20260603/Title_page_and_declarations_strict_v2.docx`

2. **找到 "Data Availability" 部分**

3. **替换为新措辞**

4. **保存文件**

5. **重新运行检查**：
   ```bash
   cd "/Users/guohuiwen/华健 论文/9- 金融"
   python3 scripts/check_ael_strict_v2_package.py
   ```

6. **如果通过**：继续下一步

---

## 常见问题

### Q1: 我的机构没有 Capital IQ，我用的是个人账号？
**A**: 这种情况比较复杂。建议：
- 在 Acknowledgments 中说明数据访问方式
- 数据可用性声明改为"obtained through authorized access"
- 联系 Capital IQ 销售代表确认学术使用政策

### Q2: 期刊要求我提供数据，怎么办？
**A**: 回复编辑部说明：
```
Due to licensing restrictions of the S&P Capital IQ database, we cannot 
share the underlying microdata. However, we provide:
1. Detailed variable definitions
2. Sample construction procedures  
3. Replication code (excluding proprietary data)
4. Summary statistics and analytical outputs

Reviewers or researchers with Capital IQ access can fully replicate our 
analysis using these materials.
```

### Q3: 可以上传汇总统计表格吗？
**A**: 可以，只要是汇总层级的（如均值、中位数、标准差），不包含可识别公司的微观数据。

**可以上传**：
- ✅ Table 1: Sample Distribution (firm-years, event counts)
- ✅ Table 2: Descriptive Statistics (means, SDs)
- ✅ Table 3: Regression Results (coefficients, SEs)
- ✅ Correlation matrices (aggregate level)

**不能上传**：
- ❌ Company-level panels with Capital IQ data
- ❌ Raw Excel exports from Capital IQ
- ❌ Firm identifiers + Capital IQ variables

### Q4: 我能否提供 company IDs 列表？
**A**: 不建议。Company IDs 虽然不直接是财务数据，但结合 Capital IQ 访问权限可以重建完整数据集，可能违反授权。

**安全做法**：
- 提供样本筛选标准（如"2014-2024 Singapore and Australia listed firms with fiscal-year accounting data"）
- 提供样本统计（如"2,322 firms, 19,322 firm-years"）
- 不提供具体公司列表

---

## 完成确认

请在下面勾选：

- [ ] ✅ 我确认当前 Data Availability 措辞符合授权要求
- [ ] ✅ 如果不确定，我已联系图书馆确认
- [ ] ✅ 如果需要修改，我已按照指南修改并重新检查

**完成后，标记在 FINAL_SUBMISSION_READINESS_STATUS 中**：
- [x] Capital IQ 授权确认完成

继续下一步：最终视觉 QA！✅

---

## 法律免责声明

本指南仅提供一般性建议，不构成法律意见。具体授权条款以你的机构与 S&P Global 签订的合同为准。如有疑问，请咨询你的机构图书馆或法务部门。
