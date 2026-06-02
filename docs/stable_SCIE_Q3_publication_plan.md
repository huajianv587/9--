<!-- SUPERSEDED 2026-06-01: Current route is analyst coverage / information environment. See docs/SUPERSEDED_BY_COVERAGE_ROUTE_20260601.md and docs/SSCI_Q3_transfer_ladder_coverage_route_20260601.md. -->

# Stable SSCI Q3 Publication Plan

Date: 2026-05-31

## 1. Bottom-Line Judgment

The most publication-stable direction is not a pure LLM or multi-agent paper.

Recommended primary direction:

**Analyst Disagreement and Financial Distress in Asia-Pacific Listed Firms: Explainable Evidence from S&P Capital IQ**

Core idea:

Use S&P Capital IQ Pro to build a firm-quarter panel for Asia-Pacific listed companies. Predict one-year-ahead financial distress using accounting ratios, market signals, and analyst-forecast variables from Capital IQ Estimates. Use logistic regression and XGBoost/LightGBM, then explain drivers with SHAP.

Why this is the safest route:

- Financial distress prediction is a mature reviewer-friendly framework.
- Capital IQ gives a real data advantage: company status, delisting/bankruptcy indicators, financials, estimates, analyst coverage, forecast dispersion, and market data.
- The contribution is financial, not algorithmic: analyst disagreement as an early-warning signal.
- If Estimates coverage is thin, the paper can still survive using accounting + market data.
- No A40, LLM, or fragile text pipeline is required.

Updated target:

**SSCI Q3, with 70-80% eventual acceptance probability across a verified journal ladder.**

No legitimate SSCI Q3 journal can honestly be treated as having a guaranteed 70-80% single-journal acceptance rate unless the journal itself publishes such data. The realistic planning target is eventual acceptance after one to three submissions, not a guaranteed first-shot acceptance.

## 2. Critical Indexing Clarification

The user has confirmed that SSCI and SCIE are treated as equivalent for the intended evaluation. Therefore, the target pool should be **SSCI Q3 finance/economics journals**, not SCIE-only journals.

Before submission, verify in Web of Science Master Journal List and JCR:

- database edition: SSCI preferred; avoid ESCI unless explicitly accepted;
- JIF quartile and category;
- whether the journal is Q3 in the relevant JCR year;
- whether "JCR Q3" or "Chinese Academy/CAS 3区" is the actual rule.

Do not rely on journal websites, Scopus quartiles, or third-party acceptance-rate claims alone.

## 3. Data Sources Available

Confirmed or likely available from current evidence:

- S&P Capital IQ Pro: logged in and usable in Safari; strongest source for financials, estimates, company status, market data, news, documents, and screening.
- Bloomberg: NTU Library FAQ states Bloomberg terminals are available in the Business Library and can be booked.
- NTU/NBS teaching-resource page lists Bloomberg, CEIC, Datastream, Refinitiv Eikon, and WRDS as finance teaching/research tools. Actual access should be confirmed through NTU Library/NBS account permissions.

Use Capital IQ as the authoritative source first. Use Bloomberg/Refinitiv/WRDS only to fill gaps or validate prices/status.

## 4. Primary Paper Design

### Working Title

**Analyst Forecast Dispersion and Financial Distress in Asia-Pacific Equity Markets: Evidence from S&P Capital IQ**

### Research Question

Do analyst forecast dispersion, downward estimate revisions, and analyst coverage improve one-year-ahead financial distress prediction beyond traditional accounting and market variables?

### Main Contribution

The paper is not "XGBoost predicts bankruptcy." That is too generic.

The contribution is:

- Capital IQ institutional data for Asia-Pacific listed firms;
- analyst disagreement and revision behavior as information-environment signals;
- explainable evidence on when analyst signals add value beyond accounting ratios;
- cross-market comparison across SGX, HKEx, ASX, and expanded Asia-Pacific markets if needed.

### Hypotheses

H1. Higher analyst forecast dispersion is associated with greater future distress risk.

H2. Downward analyst estimate revisions improve distress prediction beyond accounting ratios and market variables.

H3. Analyst-based signals add more value among firms with weaker information environments, such as smaller firms or lower-coverage markets.

H4. The relative importance of accounting, market, and analyst signals differs across Asia-Pacific markets.

## 5. Sample and Label

### Initial Universe

- Exchanges: SGX, HKEx, ASX.
- Expansion if event count is low: Japan, Korea, Taiwan, Malaysia, Thailand, Indonesia.
- Period: 2014-2024 if available; otherwise 2016-2024 minimum.
- Frequency: firm-quarter preferred; firm-year acceptable if quarterly status fields are weak.

### Main Dependent Variable

Financial distress event within the next four quarters.

Preferred label from Capital IQ:

- bankruptcy;
- liquidation;
- restructuring;
- receivership;
- default;
- delisting due to financial distress;
- inactive status with distress-related reason.

Fallback broader label:

- credit downgrade to high-risk category if ratings are available;
- negative equity;
- interest coverage below 1 for two consecutive periods;
- severe operating-loss state.

Use the broad label only if true event counts are too low, and label it as "financial stress" rather than "bankruptcy."

### Predictor Timing

All predictors at time t must predict distress over t+1 to t+4 quarters.

Financial statements must be lagged by reporting or filing date, not fiscal period end alone.

## 6. Feature Set

### Accounting Features

- ROA
- ROE
- net margin
- operating margin
- revenue growth
- cash flow from operations / total assets
- debt to equity
- total liabilities / total assets
- current ratio
- quick ratio
- interest coverage
- log total assets
- log market cap

### Market Features

- past 3-month return
- past 12-month return
- return volatility
- turnover or liquidity proxy
- market-to-book

### Analyst / Estimates Features

- number of analysts
- consensus EPS forecast
- forecast dispersion
- forecast high-low range
- 30-day revision direction
- 90-day revision direction
- change in analyst coverage
- prior forecast error if actual EPS is available

### Controls

- country
- exchange
- GICS sector
- year/quarter fixed effects
- firm size bucket

## 7. Model Strategy

Keep the method mature and reviewer-friendly.

Models:

1. Logistic regression with clustered or robust standard errors.
2. XGBoost.
3. LightGBM if useful, but do not overbuild.

Baseline comparisons:

- Altman/Zmijewski-style accounting-score baseline if variables are available.
- Accounting-only model.
- Accounting + market model.
- Accounting + market + analyst model.

Metrics:

- ROC-AUC;
- PR-AUC, because distress events are imbalanced;
- balanced accuracy;
- F1 for distress class;
- calibration plot or Brier score;
- confusion matrix at economically meaningful thresholds.

Explainability:

- SHAP global feature importance;
- SHAP dependence plots for forecast dispersion, leverage, liquidity, and revisions;
- subgroup SHAP by market and firm-size bucket.

## 8. Required Tables and Figures

Tables:

1. Sample construction and filtering.
2. Descriptive statistics by market.
3. Distress-event distribution by year and market.
4. Logistic regression results.
5. ML performance comparison.
6. Incremental value of analyst variables.
7. Robustness checks.

Figures:

1. Distress event timeline.
2. Forecast dispersion by market and distress status.
3. SHAP summary plot.
4. Calibration or precision-recall curve.

## 9. Robustness Checks

Minimum required:

- time split: train 2014-2020, test 2021-2024;
- market split: train on two markets, test on the third;
- analyst coverage robustness: all firms vs analyst coverage >= 2 vs >= 3;
- exclude microcaps;
- annual instead of quarterly panel;
- alternate distress definition.

Do not add LLM/text features until all of the above works.

## 10. SSCI Q3 Journal Ladder

The following ladder must be verified live in NTU Web of Science / JCR before submission. The list is designed around fit and probability, not prestige.

### Tier 1: Best Fit for the Recommended Paper

1. **Applied Economics Letters**
   - Verified on 2026-05-31: 2024 JCR SSCI, Economics Q3, JIF 1.3.
   - Official Taylor & Francis acceptance rate: 35%.
   - Why it fits: concise empirical finding, short paper format, applied finance/economics evidence.
   - Best manuscript angle: a clean letter showing that analyst forecast dispersion predicts future financial stress in Asia-Pacific listed firms.
   - Strategy: submit a short, tightly written version with one main result and two robustness checks.

2. **Journal of Behavioral Finance**
   - Verified on 2026-05-31: 2024 JCR SSCI, Business/Finance Q3 and Economics Q3, JIF 1.2.
   - Official Taylor & Francis acceptance rate: 4%.
   - Why it fits: analyst disagreement, forecast revision, investor/analyst behavior, behavioral information environment.
   - Best manuscript angle: do analyst disagreement and downward revisions reveal distress risk before accounting signals fully adjust?
   - Strategy: use only as a stretch target, not as the stability-first lead.

3. **Journal of Real Estate Research**
   - Why it fits: only if the sample is narrowed to listed REITs / real estate firms.
   - Best manuscript angle: analyst disagreement and distress risk among Asia-Pacific listed real estate firms or REITs after rate shocks.
   - Use only if Capital IQ can produce enough listed real-estate/REIT observations.

### Tier 2: Niche SSCI Q3 Targets if the Paper Is Reframed

4. **Review of Derivatives Research**
   - Use only if the paper changes to implied volatility/options-based distress or crash-risk prediction.
   - Requires Bloomberg/Refinitiv options data; higher technical burden.

5. **Finance a Uver - Czech Journal of Economics and Finance**
   - Lower-prestige backup. Verify current SSCI and Q3/Q4 status carefully because historical quartiles fluctuate.

### Avoid as Primary Targets for This Objective

- JAFEB: indexing risk.
- JRFM / IJFS / Asia-Pacific Financial Markets / Journal of Economics and Finance / Financial Markets and Portfolio Management: useful outlets, but public official pages or JCR checks show ESCI rather than SSCI. Do not use if the requirement is strict SSCI.
- RIBAF, FRL, PBFJ, Borsa Istanbul Review, Journal of Financial Stability: generally stronger/higher-quartile outlets now; not aligned with a "stable Q3" strategy.

### Probability Framing

Target 70-80% as a **portfolio probability**:

- first submission: Applied Economics Letters;
- second submission: a verified SSCI Q3/Q2 applied economics or finance outlet selected after pilot results;
- third submission: Journal of Real Estate Research only if sample is real-estate-focused, otherwise a verified SSCI Q3 economics/finance backup from current JCR.

This is more defensible than claiming any single journal has 70-80% acceptance.

## 11. Go/No-Go Gates

### Gate 1: Distress Events

Pass:

- at least 300 distress/stress events for ML;
- at least 150 clean severe distress events for logit + robustness.

If fail:

- expand markets;
- extend period;
- use broader stress definition;
- or switch to analyst-earnings-surprise paper.

### Gate 2: Estimates Coverage

Pass:

- analyst variables available for at least 30-40% of firm-periods;
- analyst-covered sample includes at least 1,000 firm-periods.

If fail:

- keep analyst signals as a subsample extension;
- main model becomes accounting + market distress prediction.

### Gate 3: Leakage Control

Pass:

- reporting dates and estimate dates are before prediction horizon;
- no use of post-distress information.

If fail:

- move to firm-year design with conservative lags.

### Gate 4: Predictive Value

Pass:

- analyst variables improve PR-AUC or ROC-AUC over accounting + market baseline;
- SHAP interpretation is economically coherent.

If fail:

- reframe as "limited incremental value of analyst disagreement" only if the null result is clean and interesting;
- otherwise switch to earnings-surprise direction.

## 12. Timeline

### Week 1: Data Feasibility

- Export 200-300 companies across SGX/HKEx/ASX.
- Confirm company status, delisting, bankruptcy, and inactive reason fields.
- Export 20-30 sample firms' Estimates fields.
- Count distress events and estimates coverage.

### Week 2: Full Data Export

- Export financials, market variables, status history, estimates.
- Normalize identifiers and firm-quarter dates.
- Build the initial label.

### Week 3: Data Audit

- Run missingness and leakage checks.
- Produce sample-construction table.
- Freeze final sample and label definition.

### Week 4: Baseline Models

- Logistic regression.
- Accounting-only and market-only baselines.
- Initial time-split evaluation.

### Week 5: ML Models

- XGBoost/LightGBM.
- Class imbalance handling.
- Performance tables.

### Week 6: Explainability and Robustness

- SHAP plots.
- Subgroup analysis.
- Alternate label and coverage thresholds.

### Week 7: Manuscript Draft

- Introduction.
- Literature review.
- Data and method.
- Main results.

### Week 8: Submission Package

- Final tables and figures.
- Cover letter.
- Data availability statement.
- Journal-specific formatting.

## 13. Backup Direction

If financial distress labels are weak, switch to:

**Analyst Forecast Dispersion and Earnings Surprise Magnitude in Asia-Pacific Markets**

This keeps the Capital IQ Estimates advantage but avoids bankruptcy-event sparsity.

Dependent variable:

- absolute earnings surprise;
- positive vs non-positive surprise;
- meet/beat/miss if a defensible threshold exists.

Core contribution:

- forecast dispersion as uncertainty signal;
- analyst disagreement in Asia-Pacific markets;
- cross-market comparison.

## 14. Final Recommendation

Primary route:

**Financial distress prediction with analyst disagreement and SHAP.**

Backup route:

**Earnings surprise / forecast dispersion.**

Avoid:

- LLM fine-tuning;
- multi-agent frameworks;
- RL trading strategy;
- heavy text pipelines;
- JAFEB-first strategy.

The project should be judged by verified journal index status and data gates, not by optimistic acceptance-rate estimates.
