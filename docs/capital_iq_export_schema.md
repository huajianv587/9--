# Capital IQ Export Schema

Use this as the first export checklist for the locked SSCI Q3 route:

**Analyst disagreement and financial distress prediction in Asia-Pacific listed firms.**

Export a small event-led pilot first. Do not export the full universe until the
event and analyst-coverage gates pass.

## Sample Definition

- Region, first pass: Singapore, Hong Kong, Australia.
- Expansion markets: Japan, Korea, Taiwan, Malaysia, Thailand, Indonesia, India if event count is weak.
- Firms: listed common equities; include active and inactive/delisted firms.
- Period: preferred 2014-2024; minimum 2016-2024.
- Frequency: firm-quarter if feasible; firm-year only if event timing is too noisy.
- Timing: all predictors must be available before the prediction window.

## Required Identifier Fields

| Field | Purpose |
| --- | --- |
| company_id | Stable Capital IQ company identifier |
| security_id | Security-level merge key if available |
| ticker | Human-readable identifier |
| company_name | Manual event audit |
| exchange | Listing venue |
| isin | Cross-source merge key |
| country | Country fixed effects and market split |
| sector | Sector fixed effects |
| fiscal_period_end | Accounting period |
| fiscal_quarter | Firm-quarter panel key |
| data_item_date | Leakage audit |

## Event and Status Fields

| Field | Purpose |
| --- | --- |
| company_status | Active, inactive, bankrupt, liquidated, acquired, delisted, etc. |
| status_date | Event timing |
| delisting_date | Event timing |
| delisting_reason | Must distinguish distress from M&A, privatization, voluntary delisting, transfer |
| bankruptcy_filing_date | Strict distress label |
| default_event_date | Strict distress label |
| restructuring_date | Strict distress label |
| receivership_liquidation_date | Strict distress label |
| credit_rating | Optional severity signal |
| credit_rating_date | Leakage audit |
| severe_downgrade_flag | Optional strict/broader label if ratings coverage is sufficient |
| going_concern_flag | Optional stress signal if available |
| event_source_note | Manual audit trail |

## Financial Statement Fields

| Field | Purpose |
| --- | --- |
| total_assets | Size |
| total_liabilities | Leverage |
| total_equity | Negative-equity stress label and controls |
| revenue | Growth and scale |
| revenue_growth | Operating momentum |
| ebit | Interest coverage |
| interest_expense | Interest coverage |
| operating_income | Profitability and loss history |
| net_income | Profitability and loss history |
| cash_and_equivalents | Liquidity |
| operating_cash_flow | Cash-flow risk |
| current_assets | Current ratio |
| current_liabilities | Current ratio |
| roa | Profitability |
| roe | Profitability |
| operating_margin | Profitability |
| net_margin | Profitability |
| leverage | Financial risk |
| current_ratio | Liquidity |
| interest_coverage | Stress label and controls; avoid circular use if label uses it |

## Market Fields

| Field | Purpose |
| --- | --- |
| market_cap | Size and microcap exclusion |
| price | Return construction |
| total_return_3m | Market signal |
| total_return_12m | Market signal |
| return_volatility_12m | Market risk |
| market_to_book | Valuation |
| turnover | Liquidity |
| trading_volume | Liquidity |
| exchange_market_index_return | Market control if available |

## Estimates / Analyst Fields

| Field | Purpose |
| --- | --- |
| forecast_period | Match to fiscal period |
| forecast_date | Must precede prediction date |
| consensus_eps | Analyst expectation level |
| eps_actual | Prior forecast error when available |
| num_analysts | Analyst coverage |
| eps_high | High-low spread |
| eps_low | High-low spread |
| eps_stddev | Forecast dispersion |
| estimate_revision_30d | Analyst revision signal |
| estimate_revision_90d | Analyst revision signal |
| coverage_change | Change in analyst attention |

## Derived Label Fields

| Field | Formula / rule |
| --- | --- |
| strict_distress_12m | 1 if bankruptcy, default, restructuring, receivership/liquidation, severe downgrade, or distress-related delisting occurs within next 12 months |
| stress_12m | 1 if broader stress rule is triggered within next 12 months |
| distress_event_type | Main event type used for label |
| event_audit_ok | Manual check that event timing and reason are valid |

Do not use Altman Z-score as both a label and a feature. If a stress definition
uses interest coverage or negative equity, run a robustness model excluding the
direct label components.

## Pilot Export Pass Criteria

- strict distress events >= 150, or broader stress events >= 300 after expansion is realistic.
- Analyst variables cover at least 30% of firm-periods and include enough event cases.
- Delisting reasons are auditable; non-distress delistings are excluded from strict labels.
- No duplicate firm-quarter rows after key normalization.
- At least 70% completeness for core accounting and market fields.
- Forecast dates, financial-statement dates, and market-window endpoints precede the prediction horizon.

## 2026-05-31 Analyst Export Update

The first Singapore historical analyst export was parsed successfully:

`data/raw/capital_iq/capital_iq_estimates_singapore_fyplus1_asof_20231231_20260531.xlsx`

Important parsing detail:

- Sheet1 is the financial-stress accounting report.
- Sheet2 is the analyst estimates report.
- The parser reads Sheet2.

Required historical export batch:

- Market: Singapore first.
- Years: 2014-2024.
- Frequency: one export per as-of date.
- As-of date: 12/31/YYYY.
- Forecast period: FY+1.

Required columns for every year:

| Capital IQ display field | Parser alias |
| --- | --- |
| Entity Name | SP_ENTITY_NAME |
| Entity ID | SP_ENTITY_ID |
| CIQ EPS Est - Std Dev | SP_EPS_STDDEV_EST |
| CIQ EPS Est High | SP_EPS_HIGH_EST |
| CIQ EPS Est Low | SP_EPS_LOW_EST |
| CIQ EPS Est - # of Est | SP_EPS_NUM_EST |
| CIQ EPS Est | SP_EPS_EST |
| CIQ EPS Est Date | SP_EPS_DATE_OF_EST |

File naming convention:

`capital_iq_estimates_<market>_fyplus1_asof_YYYY1231_20260531.xlsx`

For the current Singapore parser, filenames must match:

`capital_iq_estimates_singapore_fyplus1_asof_*_*.xlsx`

Current gate result:

- 2023 Singapore analyst-covered firm-years: 135.
- 2023 Singapore analyst-covered stress events after merge: 34.
- Current status: underpowered; not AEL submission-ready.

If Singapore remains underpowered after all historical as-of exports, expand in this order based on the APAC estimates snapshot:

1. ASX
2. SEHK
3. TSE
4. SZSE / SHSE
5. NSEI
6. KLSE
7. SET
8. KOSE
