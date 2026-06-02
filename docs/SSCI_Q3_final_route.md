<!-- SUPERSEDED 2026-06-01: Current route is analyst coverage / information environment. See docs/SUPERSEDED_BY_COVERAGE_ROUTE_20260601.md and docs/SSCI_Q3_transfer_ladder_coverage_route_20260601.md. -->

# SSCI Q3 Final Route

Date: 2026-05-31

## Final Recommendation

Primary paper:

**Analyst Disagreement and Financial Distress in Asia-Pacific Listed Firms: Evidence from S&P Capital IQ**

This is the best compromise between:

- SSCI Q3 fit;
- high data defensibility;
- reviewer familiarity;
- Capital IQ data advantage;
- execution stability.

## Why This Is Better Than Earnings Surprise Prediction

Earnings surprise prediction uses Capital IQ Estimates more directly, but it depends heavily on analyst coverage and clean consensus EPS / actual EPS history. In Asia-Pacific markets, coverage may be thin for smaller firms.

Financial distress prediction is safer because:

- labels can be built from company status, delisting, bankruptcy, restructuring, credit risk, and financial stress indicators;
- accounting and market data are broadly available;
- analyst variables become an incremental contribution rather than the entire foundation;
- if Estimates coverage is incomplete, the paper still survives.

## Journal Positioning

The paper should not be written as:

"XGBoost predicts bankruptcy."

It should be written as:

"Analyst forecast disagreement provides early-warning information about firm distress in Asia-Pacific markets, beyond accounting and market signals."

This makes the paper suitable for behavioral finance / applied economics SSCI Q3 outlets.

For **Applied Economics Letters**, the paper should be even narrower:

"Analyst forecast dispersion predicts future financial stress in Asia-Pacific listed firms."

The AEL version should not try to sell a full prediction framework. It should sell one concise applied-economics result.

## Target Journal Ladder

1. **Applied Economics Letters**
   - Verified 2024 JCR status: SSCI, Economics Q3.
   - Official Taylor & Francis acceptance rate checked on 2026-05-31: 35%.
   - Lead target under the user's stability-first requirement.
   - Positioning: one clean empirical finding with Capital IQ institutional data.

2. **Journal of Behavioral Finance**
   - Verified 2024 JCR status: SSCI, Business/Finance Q3 and Economics Q3.
   - Official Taylor & Francis acceptance rate checked on 2026-05-31: 4%.
   - Not suitable as the lead route for a stability-first plan.
   - Use only as a low-probability stretch target if the final paper has a strong behavioral-finance mechanism.

3. **Journal of Real Estate Research**
   - Use only if full-sample event count is weak but REIT / real estate firms are strong.
   - Positioning: distress risk in Asia-Pacific listed real estate / REIT firms.
   - Must be verified in current JCR before use.

4. **Verified SSCI Q3 backup**
   - To be selected from NTU JCR after confirming current category, quartile, and scope.

Do not use **Journal of Economics and Finance** for this strict SSCI route. It was checked in JCR on 2026-05-31 and its current edition is ESCI, not SSCI.

## Paper Architecture

### Applied Economics Letters Form

- Main text target: 1,800-2,000 words.
- Main result: logit / marginal effects.
- Secondary evidence: XGBoost incremental prediction.
- Supplement: detailed robustness, SHAP, extra horizons, variable definitions.
- Main manuscript tables: no more than three.

### Research Question

Does analyst forecast disagreement predict one-year-ahead financial stress or distress in Asia-Pacific listed firms beyond accounting and market indicators?

### Data

- Region: SGX, HKEx, ASX first.
- Expansion: Japan, Korea, Taiwan, Malaysia, Thailand, Indonesia if event count is too low.
- Period: 2014-2024 preferred; 2016-2024 minimum.
- Unit: firm-quarter.

### Dependent Variable

For Applied Economics Letters, use the statistically strongest clean label:

- main label: financial stress within next four quarters if strict distress events are sparse;
- robustness label: strict financial distress within next four quarters.

Preferred event labels:

- bankruptcy;
- liquidation;
- restructuring;
- receivership;
- default;
- distress-related delisting;
- inactive status caused by financial distress.

Fallback stress labels:

- negative equity;
- interest coverage below 1 for two periods;
- severe operating losses;
- large credit-rating downgrade if ratings data are available.

### Feature Blocks

Accounting:

- ROA, ROE, margins, revenue growth, leverage, current ratio, interest coverage, cash flow ratio, log assets.

Market:

- market cap, prior returns, volatility, market-to-book, turnover.

Analyst / Estimates:

- number of analysts, forecast dispersion, high-low spread, 30/90-day revision direction, coverage change, prior forecast error.

Controls:

- country, sector, year-quarter, exchange, firm-size bucket.

### Models

- Main manuscript: logistic regression or discrete-time logit with marginal effects.
- Secondary prediction check: XGBoost.
- Supplement: SHAP interpretation.
- LightGBM optional only if needed for stability.

### Evaluation

- ROC-AUC.
- PR-AUC.
- balanced accuracy.
- distress-class F1.
- calibration / Brier score.

### Required Robustness

- time split;
- market split;
- analyst coverage >= 2 and >= 3;
- excluding microcaps;
- alternate distress definition.

## Success Gates

Continue the primary direction only if:

- at least 150 clean severe distress events or 300 broader stress events;
- analyst variables available for at least 30-40% of firm-periods;
- no timestamp leakage;
- analyst variables improve the accounting + market baseline or produce a publishable null finding.

If these fail, switch to:

**Analyst Forecast Dispersion and Earnings Surprise Magnitude in Asia-Pacific Markets**

## Execution Order

1. Verify target journals in NTU JCR: SSCI, Q3, current year.
2. Export Capital IQ pilot: 300 companies across SGX/HKEx/ASX.
3. Count distress events and Estimates coverage.
4. Expand markets if event count is low.
5. Build firm-quarter panel.
6. Run baseline logistic and XGBoost.
7. Freeze the AEL paper after the first stable logit, incremental prediction table, and compact robustness table.
