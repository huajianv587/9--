# 最终视觉 QA 检查表

日期：2026-06-03
目标：在上传前对 PDF/DOCX 进行最终视觉质量检查

---

## 为什么需要视觉 QA？

自动检查可以验证内容正确性，但无法检测：
- 表格格式错乱
- 文字溢出页面边界
- 分页不当
- 字体不一致
- 公式显示错误

**上传前的视觉检查可以避免因格式问题被编辑部要求重新提交。**

---

## 检查文件

### **主要文件**：
```
submission_package/ael_strict_v2_20260603/Manuscript_AEL_strict_v2_preview.pdf
```

### **备用文件（如果 PDF 有问题）**：
```
submission_package/ael_strict_v2_20260603/Manuscript_AEL_strict_v2_draft.docx
```

---

## 检查步骤

### **步骤1：打开 PDF 预览文件**

1. 双击打开 `Manuscript_AEL_strict_v2_preview.pdf`
2. 使用 **Preview** (Mac) 或 **Adobe Reader** (Windows/Mac)
3. 调整缩放到 **100%** 或 **适合页面宽度**

---

### **步骤2：整体外观检查（5 分钟）**

快速翻阅整个文档，检查：

#### ✅ **页数正确**
- [ ] 总页数：约 6 页（匿名稿）
- [ ] 没有意外的空白页
- [ ] 没有多余的分页

#### ✅ **页边距正常**
- [ ] 左右页边距对称
- [ ] 文字没有超出页面边界
- [ ] 页眉页脚位置正常（如果有）

#### ✅ **字体一致**
- [ ] 正文字体一致（通常 Times New Roman 或 Arial, 12pt）
- [ ] 标题字体一致
- [ ] 没有意外的字体变化

#### ✅ **整体布局专业**
- [ ] 段落间距合理
- [ ] 标题层级清晰
- [ ] 没有明显的排版错误

---

### **步骤3：逐页详细检查（10-15 分钟）**

#### **第 1 页：标题和摘要**

- [ ] **标题完整显示**：
  - "Analyst Coverage and Subsequent Accounting-Based Financial Stress: Evidence from Singapore and Australia"
  - 没有截断或换行不当

- [ ] **摘要段落**：
  - 一个完整段落，没有不必要的换行
  - 关键数字正确：
    - ✅ 19,322 firm-years
    - ✅ 7,874 strict-stress events
    - ✅ Odds ratio 0.711
    - ✅ -7.2 percentage points

- [ ] **关键词**：
  - 显示完整，用分号分隔
  - "analyst coverage; accounting-based stress; information environment; Singapore; Australia; S&P Capital IQ"

- [ ] **JEL codes**：
  - "G14; G17; G24; G32"

---

#### **第 2-3 页：Introduction 和 Data**

- [ ] **节标题清晰**：
  - "1. Introduction"
  - "2. Data and Variables"
  
- [ ] **段落对齐**：
  - 两端对齐（justified）或左对齐
  - 没有奇怪的行距

- [ ] **数字和文字**：
  - 所有提到的数字清晰可读
  - 没有乱码或特殊符号错误

- [ ] **参考文献引用**：
  - 格式正确（如 "Merton, 1987" 或 "(Merton, 1987)"）
  - 没有断裂的引用

---

#### **第 3 页：Empirical Specification**

- [ ] **公式显示正确**：
  ```
  Pr(StrictAccountingStress_{i,t+1}=1) =
  logit(alpha + beta AnalystCovered_{i,t} + gamma Controls_{i,t}
        + market fixed effects + fiscal-year fixed effects).
  ```
  
  检查：
  - [ ] 下标正确显示（i, t, t+1）
  - [ ] 希腊字母正确显示（alpha, beta, gamma）
  - [ ] 没有公式断行错误
  - [ ] 对齐合理

---

#### **第 4-5 页：Results 和 Tables**

- [ ] **表格完整性**：

  **Table 1: Candidate Samples**
  - [ ] 表头清晰
  - [ ] 7 列数据完整显示：Sample, Firm-years, Firms, Stress events, Event rate, Coverage rate, ASX rows, Singapore rows
  - [ ] 数字对齐（通常右对齐）
  - [ ] 没有列重叠或溢出
  - [ ] 关键行可见（如 "Strict accounting stress 12m"）

  **Table 2: Main Estimates** (如果在这一页)
  - [ ] 表头清晰
  - [ ] 系数、标准误、OR、p值列对齐
  - [ ] 星号显示正确（*, **, ***）
  - [ ] 没有数据截断

  **Table 3: Robustness Checks** (如果在这一页)
  - [ ] 表格宽度适合页面
  - [ ] 所有行完整显示
  - [ ] 数字精度一致（小数位数）

- [ ] **表格标题和注释**：
  - [ ] 标题在表格上方
  - [ ] 注释在表格下方
  - [ ] 字体略小但清晰可读

---

#### **第 5-6 页：Conclusion, References, 剩余 Tables**

- [ ] **结论段落**：
  - 完整，没有截断
  - 关键结论清晰呈现

- [ ] **Data Availability 声明**：
  - 完整显示
  - 措辞与你确认的版本一致

- [ ] **参考文献列表**：
  - [ ] 按字母顺序排列
  - [ ] 格式一致（APA 或 Chicago style）
  - [ ] 没有断行错误
  - [ ] 关键参考文献存在：
    - Altman (1968)
    - Beaver (1966)
    - Bhushan (1989)
    - Hong et al. (2000)
    - Lang & Lundholm (1996)
    - Merton (1987)
    - Ohlson (1980)

- [ ] **剩余表格**（如果有）：
  - 格式与前面的表格一致
  - 完整显示

---

### **步骤4：关键数字最终核对（5 分钟）**

在整个文档中，确认以下关键数字**一致且正确**：

#### **样本量**
- [ ] **19,322** firm-years（主样本）
- [ ] **2,322** firms
- [ ] **7,874** strict-stress events
- [ ] **40.8%** event rate
- [ ] **27.0%** coverage rate

#### **主要结果**
- [ ] Odds ratio: **0.711**
- [ ] Average marginal effect: **-7.2** percentage points
- [ ] ASX OR: **0.778**
- [ ] Singapore OR: **0.492**

#### **没有出现的旧数字（必须确认不存在）**
- [ ] ❌ 19,402（旧broad样本）
- [ ] ❌ 0.568（旧broad OR）
- [ ] ❌ 12,303（旧broad事件数）

**如果发现任何旧数字，立即停止并报告！**

---

### **步骤5：Title Page 检查（3 分钟）**

打开：`submission_package/ael_strict_v2_20260603/Title_page_and_declarations_strict_v2.docx`

- [ ] **标题一致**：与主稿件相同
- [ ] **作者信息完整**：
  - [ ] 姓名
  - [ ] 单位
  - [ ] 邮箱
  - [ ] ORCID（如果有）
- [ ] **没有 [TEMPLATE] 标记**
- [ ] **Funding 声明完整**
- [ ] **COI 声明完整**
- [ ] **Data Availability 声明一致**

---

## 常见问题和解决方案

### 问题1：表格右侧被截断

**解决方案**：
1. 打开 DOCX 文件
2. 选中表格
3. 右键 → Table Properties → 调整宽度
4. 或减少列宽、字体大小
5. 重新生成 PDF

### 问题2：公式显示不正常

**解决方案**：
1. 检查是否使用了 MathType 或 Equation Editor
2. 如果用纯文本，确保下标用正常格式
3. 可以截图公式作为图片插入（不推荐，但可用）

### 问题3：参考文献格式不一致

**解决方案**：
1. 使用 Zotero 或 Mendeley 等文献管理工具
2. 或手动统一格式：
   - 作者姓氏在前
   - 年份用括号
   - 期刊名斜体
   - 卷号粗体或正常

### 问题4：PDF 生成失败或乱码

**解决方案**：
1. 使用 Word 自带的"导出为 PDF"功能
2. 或使用 Mac 的 "打印 → 另存为 PDF"
3. 确保字体嵌入（在 PDF 选项中勾选）

---

## 完成检查

完成所有检查后，在这里签字确认：

```
视觉 QA 检查完成

检查日期：2026-06-__ __:__
检查人：[你的姓名]

整体评分：
- [ ] ✅ 完美，可以上传
- [ ] ⚠️ 有小问题，已修复
- [ ] ❌ 有严重问题，需要重新生成

主要发现：
[在此记录任何问题或修改]

最终确认：
- [ ] 我确认所有关键数字正确
- [ ] 我确认没有旧数据出现
- [ ] 我确认表格和公式显示正常
- [ ] 我确认文档可以上传
```

---

## 完成后

✅ 视觉 QA 检查完成

**标记在 FINAL_SUBMISSION_READINESS_STATUS 中**：
- [x] 最终视觉 QA 完成

**你现在可以开始上传投稿了！** 🎉

---

## 上传提醒

在 Taylor & Francis 投稿门户上传时：
1. 先上传 PDF 预览一次
2. 确认门户生成的预览正常
3. 如果有问题，可以替换文件
4. 最终提交前再检查一次

**不要在最后一秒匆忙提交！留出时间检查门户预览！**

Good luck! 🚀
