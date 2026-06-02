# Capital IQ / Safari 补充数据下载清单

日期：2026-06-02
项目：Analyst Coverage and Accounting-Based Financial Stress
用途：补强SSCI/JCR Q3投稿路线，降低因变量、时间泄漏、幸存者偏误和数据透明度审稿风险。

---

## 0. 严格结论

原来的“只补4个字段”不够。为了冲击正规SSCI/JCR Q3项目级70-80%目标，最低下载目标应是：

1. Altman-style distress关键字段；
2. fiscal-year-end historical market fields；
3. event/status fields；
4. company_id列表或历史universe重建字段；
5. 每个字段的fiscal year / as-of date / currency / units。

不能使用：

- current/no-date market cap；
- current operating company screen直接替代历史面板；
- 没有as-of date的市场变量；
- 无会计依据的retained earnings估算；
- 直接上传或公开Capital IQ raw exports。

---

## 1. 保存位置和命名规则

所有下载文件先保存到：

`/Users/guohuiwen/华健 论文/9- 金融/data/raw/capital_iq/`

推荐命名：

- `capital_iq_apac_identifier_status_events_YYYYMMDD.xlsx`
- `capital_iq_apac_financials_altman_fy2014_fy2024_YYYYMMDD.xlsx`
- `capital_iq_apac_market_fye_fy2014_fy2024_YYYYMMDD.xlsx`
- `capital_iq_apac_distress_events_YYYYMMDD.xlsx`
- `capital_iq_apac_company_id_targeted_batch_<suffix>_YYYYMMDD.xlsx`

如果Safari下载到Downloads，下载后再移动到上述目录，并记录原始文件名、下载时间、文件大小、SHA-256。

---

## 2. 首选下载方式

### 方法A：按现有2,335个company_id导出

优先使用当前模型面板中的company_id列表，而不是只用当前Operating/Public筛选。

原因：

- current screen会漏历史公司；
- 已有审计显示current/public导出无法覆盖全部模型ID；
- 只下载current operating firms会造成survivorship bias。

最低字段：

- company_id / Entity ID
- company_name / Entity Name
- ticker
- exchange
- country
- fiscal_year
- fiscal_period_end
- as_of_date / data_item_date

### 方法B：分批筛选导出

如果Capital IQ不能按company_id列表导出，则分批：

1. ASX active/public/common equity；
2. ASX inactive/delisted/former listed；
3. SGX/Catalist active/public/common equity；
4. SGX/Catalist inactive/delisted/former listed；
5. 针对missing model IDs按Entity ID或ticker suffix补导。

每批必须记录筛选条件。

---

## 3. 第一优先级：Altman-style distress字段

| 变量名 | Capital IQ可能字段名 | 时间要求 | 用途 |
|---|---|---|---|
| total_assets | Total Assets | FY2014-FY2024 | 分母、规模控制 |
| total_liabilities | Total Liabilities | FY2014-FY2024 | Altman X4分母 |
| total_debt | Total Debt | FY2014-FY2024 | 杠杆控制，不替代total liabilities |
| total_equity | Total Equity | FY2014-FY2024 | 负权益标签 |
| current_assets | Current Assets / Total Current Assets | FY2014-FY2024 | working capital |
| current_liabilities | Current Liabilities / Total Current Liabilities | FY2014-FY2024 | working capital |
| retained_earnings | Retained Earnings / Accumulated Deficit | FY2014-FY2024 | Altman X2 |
| revenue | Total Revenue / Sales | FY2014-FY2024 | Altman X5 |
| EBIT | EBIT | FY2014-FY2024 | Altman X3 |
| EBITDA | EBITDA | FY2014-FY2024 | 稳健性 |
| net_income | Net Income | FY2014-FY2024 | 盈利控制 |
| operating_income | Operating Income | FY2014-FY2024 | operating loss |
| interest_expense | Interest Expense | FY2014-FY2024 | interest coverage |
| cash_and_equivalents | Cash and Equivalents | FY2014-FY2024 | liquidity |
| operating_cash_flow | Cash from Operations / Operating Cash Flow | FY2014-FY2024 | cash-flow stress |

关键要求：

- 每个字段必须导出所有年份；
- 每个字段必须有fiscal-year标签；
- 如果有as-of date参数，设为对应年度的12/31/YYYY或fiscal-year-end；
- 不能只导FY2023或current values。

---

## 4. 第二优先级：historical market fields

这些字段用于Altman X4和控制公司可见度、流动性、市场风险。

| 变量名 | Capital IQ可能字段名 | 时间要求 | 用途 |
|---|---|---|---|
| market_cap_fye | Market Capitalization | fiscal-year-end / 12/31/YYYY | Altman X4、可见度 |
| price_fye | Stock Price / Close Price | fiscal-year-end / 12/31/YYYY | 市值核验 |
| shares_outstanding | Shares Outstanding | fiscal-year-end | 市值核验 |
| total_return_12m | Total Return 1 Year | ending fiscal-year-end | 市场表现 |
| return_volatility_12m | Volatility 1 Year | ending fiscal-year-end | 风险控制 |
| trading_volume | Trading Volume | year-end or annual average | 流动性 |
| turnover | Turnover | year-end or annual average | 流动性 |
| market_to_book | Market to Book | fiscal-year-end | 估值控制 |

硬性规则：

- `Market Capitalization`必须是历史日期值；
- 当前市值不能用于2014-2023预测；
- 如果导出表头没有日期或fiscal-year label，先做schema proof，不进入模型；
- 如果market cap缺失严重，Altman标签只能降级为稳健性或不用。

---

## 5. 第三优先级：事件和状态字段

用于构建或审计real distress event label。

| 变量名 | Capital IQ可能字段名 | 用途 |
|---|---|---|
| company_status | Company Status | active/inactive/bankrupt/delisted边界 |
| status_date | Status Date | 时间审计 |
| IPO_date | IPO Date | 样本起点 |
| delisting_date | Delisting Date | 退市事件 |
| delisting_reason | Delisting Reason | 区分困境退市和并购/私有化 |
| bankruptcy_filing_date | Bankruptcy Filing Date | 严格困境 |
| bankruptcy_status | Bankruptcy Status | 严格困境 |
| liquidation_date | Liquidation Date | 严格困境 |
| receivership_date | Receivership / Administration Date | 严格困境 |
| default_event_date | Default / Debt Default Date | 严格困境 |
| restructuring_date | Distressed Restructuring Date | 严格困境 |
| trading_suspension_date | Trading Suspension Date | 辅助信号 |
| trading_suspension_reason | Trading Suspension Reason | 排除非财务原因 |

使用规则：

- 事件字段优先用于outcome，不作为预测特征；
- delisting必须区分financial distress、M&A、privatization、voluntary delisting；
- 如果事件数不足，只做描述性验证，不强行做主模型。

---

## 6. 第四优先级：分析师字段核验

当前已有EPS estimates和analyst coverage，但下载时若可顺带核验：

| 变量名 | 用途 |
|---|---|
| num_analysts | 主变量强度 |
| analyst_covered | num_analysts > 0 |
| consensus_eps | 预测水平 |
| eps_stddev | forecast dispersion |
| eps_high | high-low spread |
| eps_low | high-low spread |
| forecast_date | look-ahead audit |
| as_of_date | snapshot timing |
| forecast_period | FY+1匹配 |
| recommendation_consensus | 附录稳健性 |
| target_price_consensus | 附录稳健性 |
| estimate_revision_30d/90d | 可选，不作为当前主线 |

注意：

- 分歧变量不再作为主假设；
- analyst coverage是主变量；
- estimates必须是FY+1、as-of fiscal-year-end之前或当天。

---

## 7. 下载完成后的审计清单

每个Excel必须检查：

- [ ] 文件存在且大小稳定；
- [ ] 记录原始下载路径和SHA-256；
- [ ] workbook sheet数量；
- [ ] row count / column count；
- [ ] unique company_id数量；
- [ ] 与现有2,335 company_id的overlap；
- [ ] missing model IDs清单；
- [ ] 每个字段每年non-missing count；
- [ ] 字段表头是否含FY或as-of date；
- [ ] market cap是否为historical date；
- [ ] currency和units是否一致；
- [ ] 是否有重复company_id-year；
- [ ] 是否存在future/outcome-after predictor leakage；
- [ ] 是否只覆盖current operating universe。

---

## 8. 合并前Go/No-Go

可以进入merge：

- company_id overlap覆盖主面板大部分ID；
- 关键字段缺失率可接受；
- historical market cap有明确日期；
- fiscal-year labels完整；
- 没有明显当前值泄漏；
- current/inactive/delisted边界可解释。

不能进入merge：

- 只导出current operating public companies；
- market cap无日期；
- retained earnings、current assets/current liabilities大面积缺失；
- fiscal-year labels混乱；
- missing model IDs无法解释；
- 工作簿只有表头或少量行。

---

## 9. 下载失败时的降级方案

如果Retained Earnings拿不到：

- 不做错误估算；
- 使用简化Altman-style指标作为稳健性；
- 主标签改为persistent accounting stress或strict accounting stress。

如果historical Market Cap拿不到：

- 不使用Altman完整公式；
- market controls降级为缺失说明；
- 标题和正文必须写accounting-based financial stress。

如果事件字段拿不到或事件太少：

- event distress只做描述性审计；
- 不做主回归；
- 用样本边界和persistent stress降低审稿风险。

如果只能导current universe：

- 只能作为schema proof或补充审计；
- 不得替换主模型面板；
- 必须继续按company_id targeted export补历史ID。

---

## 10. 下载后要运行的本地工作

下载完成后，按顺序执行：

1. raw workbook inventory；
2. field/date/ID audit；
3. missing-ID reconciliation；
4. merge supplemental fields；
5. build Altman / strict / persistent / event labels；
6. leakage audit；
7. rerun models and AME；
8. update manuscript tables；
9. update Data Availability；
10. rebuild APJFS submission package。

当前不应运行不存在的脚本。若需要合并，应先创建并测试新的审计脚本，再执行merge。
