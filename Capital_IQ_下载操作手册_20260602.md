# Capital IQ 数据下载操作手册
## 策略C - 完整版数据下载

---

## 第1步：设置筛选条件

### 1.1 地区筛选
1. 在 "Search for criteria" 框输入：**Primary Country**
2. 点击出现的 "Primary Country"
3. 在国家列表中勾选：
   - ☑️ **Australia**
   - ☑️ **Singapore**
4. 点击 **Apply** 或 **OK**

### 1.2 公司状态筛选
1. 搜索：**Company Status**
2. 选择：
   - ☑️ **Public**
   - ☑️ **Delisted**
   - ☑️ **Private** (如果需要)
3. 点击 **Apply**

### 1.3 时间范围
1. 搜索：**IPO Date**
2. 设置：
   - From: **2010-01-01**
   - To: **2024-12-31**
3. 点击 **Apply**

### 1.4 退市/破产事件
1. 搜索：**Key Developments**
2. 选择：
   - ☑️ **Bankruptcy**
   - ☑️ **Delisting**
3. 点击 **Apply**

---

## 第2步：选择输出字段

点击 **"Output"** 或 **"Columns"** 按钮，添加以下字段：

### 2.1 公司识别信息
- [ ] Capital IQ Company ID
- [ ] Company Name
- [ ] Ticker Symbol
- [ ] Primary Exchange
- [ ] Primary Country
- [ ] Primary Industry (GICS)
- [ ] GICS Sector
- [ ] GICS Industry Group

### 2.2 公司状态与事件
- [ ] Company Status (Active/Delisted/Inactive)
- [ ] IPO Date
- [ ] Delisting Date
- [ ] Bankruptcy Date
- [ ] Bankruptcy Type
- [ ] Event Type
- [ ] Event Date

### 2.3 财务数据字段
#### 资产负债表
- [ ] Total Assets (最新财年)
- [ ] Current Assets (最新财年)
- [ ] Total Liabilities (最新财年)
- [ ] Current Liabilities (最新财年)
- [ ] Total Equity (最新财年)
- [ ] Retained Earnings (最新财年)
- [ ] Cash and Equivalents (最新财年)

#### 利润表
- [ ] Total Revenue (最新财年)
- [ ] EBITDA (最新财年)
- [ ] Net Income (最新财年)
- [ ] Operating Income (最新财年)

### 2.4 市场数据字段
- [ ] Market Capitalization (最新)
- [ ] Stock Price - Close (最新)
- [ ] Stock Price - 52 Week High
- [ ] Stock Price - 52 Week Low
- [ ] Total Return 1 Year (%)
- [ ] Total Return 3 Year (%)
- [ ] Volatility (Std Deviation) 1 Year
- [ ] Beta

### 2.5 分析师数据
- [ ] Number of Analysts (买方 + 卖方)
- [ ] Consensus Recommendation
- [ ] Mean Target Price
- [ ] Consensus EPS Estimate (当年)
- [ ] Consensus EPS Estimate (下一年)

### 2.6 其他重要字段
- [ ] Fiscal Year End
- [ ] Latest Filing Date
- [ ] Number of Employees
- [ ] Total Debt (最新)
- [ ] Net Debt (最新)

---

## 第3步：运行筛选并导出

### 3.1 运行筛选
1. 点击 **"Run Screen"** 或 **"Search"**
2. 等待结果加载（可能需要1-2分钟）
3. 查看结果数量（应该在几百到几千家公司之间）

### 3.2 导出数据
1. 点击 **"Excel Export"** 或 **"Export to Excel"**
2. 选择 **"Export Current Results"**
3. 选择导出格式：
   - ✅ **Excel (.xlsx)**
   - 包含列标题：✅
4. 点击 **Download** 或 **Export**
5. 保存文件到：`/Users/guohuiwen/华健 论文/9- 金融/Capital_IQ_原始数据/`

---

## 第4步：下载时间序列数据（重要！）

由于单次导出可能只包含最新数据，需要额外下载时间序列数据：

### 4.1 财务时间序列（2010-2024）
1. 返回到筛选结果页面
2. 点击 **"Templates"** 或 **"Export Templates"**
3. 选择：**"Financial Time Series"**
4. 设置时间范围：
   - Frequency: **Annual**
   - Start: **2010**
   - End: **2024**
5. 选择指标：
   - Total Assets
   - Total Liabilities
   - Total Revenue
   - Net Income
   - EBITDA
   - Retained Earnings
6. 点击 **Export**

### 4.2 市场数据时间序列（2010-2024）
1. 选择模板：**"Market Data Time Series"**
2. 设置：
   - Frequency: **Monthly** 或 **Daily**（根据需要）
   - Start: **2010-01-01**
   - End: **2024-12-31**
3. 选择指标：
   - Market Cap
   - Stock Price (Close)
   - Returns
   - Volatility
4. 点击 **Export**

---

## 第5步：验证数据完整性

下载完成后，检查：

1. ✅ 文件包含 Australia + Singapore 的公司
2. ✅ 包含 active + delisted + inactive 公司
3. ✅ 时间范围覆盖 2010-2024
4. ✅ 所有必需字段都已导出
5. ✅ 没有明显的数据缺失（检查关键字段的填充率）

---

## 注意事项

### 数据限制
- Capital IQ 可能限制单次导出的行数（通常5000-10000行）
- 如果结果超过限制，需要分批导出（按国家或行业分开）

### 时间序列数据
- 时间序列导出是**独立**的，需要单独下载
- 确保使用相同的公司ID列表匹配横截面数据和时间序列数据

### 数据更新
- Delisting Date 和 Bankruptcy Date 可能在不同的数据表中
- 如果在公司主数据中找不到，查看 "Key Developments" 或 "Corporate Events"

---

## 预计时间

- 设置筛选条件：5-10分钟
- 选择字段：10-15分钟
- 运行并导出横截面数据：5分钟
- 导出时间序列数据：10-15分钟 × 2（财务 + 市场）
- **总计：约45-60分钟**

---

## 下载后的文件命名

建议使用以下命名规则：

```
CapitalIQ_AustraliaSingapore_Company_Master_20260602.xlsx
CapitalIQ_AustraliaSingapore_Financials_Annual_2010_2024.xlsx
CapitalIQ_AustraliaSingapore_Market_Data_Monthly_2010_2024.xlsx
CapitalIQ_AustraliaSingapore_Analyst_Data_20260602.xlsx
```

---

## 如遇问题

### 问题1：找不到某个字段
- 尝试搜索同义词（如 "Market Cap" vs "Market Capitalization"）
- 查看不同的字段类别（Financial vs Company vs Market）

### 问题2：导出数据不完整
- 检查筛选条件是否过于严格
- 尝试放宽某些条件（如公司状态）

### 问题3：数据量过大无法导出
- 分国家导出：先导出 Australia，再导出 Singapore
- 或按行业分批导出

---

**开始下载！** 按照以上步骤操作，每完成一步勾选 ✅
