<!-- SUPERSEDED 2026-06-01: Current route is analyst coverage / information environment. See docs/SUPERSEDED_BY_COVERAGE_ROUTE_20260601.md and docs/SSCI_Q3_transfer_ladder_coverage_route_20260601.md. -->

# Execution Freeze: SSCI Q3 Stable Publication Route

Date: 2026-05-31

## 0. Frozen Objective

Target:

**SSCI Q3 publication, with a planned 70-80% eventual acceptance probability across a verified submission ladder.**

Strict interpretation:

- SSCI: must be verified in Web of Science / JCR.
- Q3: must be verified in the current JCR year/category accepted by the user's evaluation rule.
- 70-80%: cannot be claimed as a verified single-journal acceptance rate unless the journal officially publishes that number.

Therefore, the actionable target is:

**Build a paper strong and conservative enough to plausibly reach 70-80% eventual acceptance after one to three submissions to verified SSCI Q3-compatible journals.**

Journal verification update, 2026-05-31:

- Applied Economics Letters is verified as SSCI Q3 in 2024 JCR and has an official Taylor & Francis acceptance rate of 35%. It is the lead stability-first target.
- Journal of Behavioral Finance is verified as SSCI Q3 in 2024 JCR but has an official Taylor & Francis acceptance rate of 4%. It is not the lead stability-first target.
- Journal of Economics and Finance is currently ESCI in JCR, not SSCI. It is excluded from the strict SSCI route.

Do not write or assume:

- "Journal X has 70-80% acceptance" without official evidence.
- "This is guaranteed SSCI Q3" before NTU JCR verification.
- "Any delisting is distress."
- "A pure replication is enough."

## 1. Frozen Main Direction

Final main direction:

**Analyst Disagreement and Financial Distress in Asia-Pacific Listed Firms: Evidence from S&P Capital IQ**

This is the route to execute unless one of the formal stop conditions below is triggered.

## 2. Why This Route Is the Most Aligned

Compared with earnings surprise prediction:

- lower dependence on analyst EPS coverage;
- survives if Estimates coverage is partial;
- easier to frame for behavioral finance and applied economics;
- financial distress / stress prediction has a mature empirical-review template.

Compared with plain bankruptcy prediction:

- stronger data moat through S&P Capital IQ Estimates;
- clearer behavioral-finance mechanism through analyst disagreement;
- less likely to be dismissed as another XGBoost bankruptcy paper.

Compared with LLM/RL/multimodal:

- better aligned with SSCI Q3 reviewer expectations;
- less execution risk;
- easier to audit for leakage and robustness.

## 3. Frozen Research Question

Does analyst forecast disagreement provide incremental early-warning information about future financial distress among Asia-Pacific listed firms, beyond accounting and market indicators?

Applied Economics Letters submission version:

Does analyst forecast disagreement predict future financial stress or distress in Asia-Pacific listed firms beyond standard accounting and market indicators?

## 4. Frozen Hypotheses

H1. Higher analyst forecast dispersion predicts higher future financial distress risk.

H2. Downward analyst forecast revisions predict higher future financial distress risk.

H3. Declining analyst coverage predicts higher future financial distress risk.

H4. Analyst variables improve distress prediction beyond accounting and market variables.

H5. The predictive value of analyst disagreement differs across Asia-Pacific markets because information environments differ.

No hypothesis will claim that Asia-Pacific effects are stronger than U.S./European effects unless a U.S./European comparison sample is actually built.

## 5. Frozen Data Scope

Initial markets:

- SGX;
- HKEx;
- ASX.

Expansion markets if event count is weak:

- Japan;
- Korea;
- Taiwan;
- Malaysia;
- Thailand;
- Indonesia;
- India, only if needed and if data coverage is manageable.

Period:

- preferred: 2014-2024;
- minimum: 2016-2024.

Unit:

- firm-quarter if feasible;
- firm-year only if quarterly status/event timing is too noisy.

## 6. Frozen Label Definitions

### Strict Distress Label

Distress = 1 if any occur in the next 12 months:

- bankruptcy filing;
- debt default;
- receivership / liquidation / restructuring;
- credit rating downgrade to severe speculative grade, if ratings coverage is sufficient;
- distress-related delisting.

Important:

Delisting is only valid if the reason is distress-related. M&A, privatization, voluntary delisting, listing transfer, and administrative changes are not distress events.

### Broader Financial Stress Label

Use only if strict distress events are insufficient:

- interest coverage below 1.5 for two consecutive periods;
- negative equity;
- consecutive operating losses;
- severe rating downgrade/default signal;
- severe market collapse indicator, used only as robustness and not as the main accounting label.

Do not use Altman Z-score as both label and feature. If Z-score is used to define stress, remove Z-score and its direct components from that model specification.

## 7. Frozen Feature Blocks

Accounting:

- ROA;
- ROE;
- operating margin;
- net margin;
- revenue growth;
- leverage;
- current ratio;
- interest coverage;
- cash-flow-to-assets;
- log assets.

Market:

- log market cap;
- prior 3-month return;
- prior 12-month return;
- return volatility;
- market-to-book;
- liquidity or turnover.

Analyst / Estimates:

- number of analysts;
- forecast dispersion;
- forecast high-low spread;
- 30-day revision;
- 90-day revision;
- coverage change;
- prior forecast error when actual EPS is available.

Controls:

- country;
- exchange;
- sector;
- year-quarter;
- firm-size bucket.

## 8. Frozen Model Plan

Main models:

1. Logistic regression / discrete-time logit as the main AEL result.
2. XGBoost as secondary incremental prediction evidence.
3. LightGBM only if it adds stability, not as a required contribution.

No LLM, RL, neural network, or multi-agent model in the first submission.

Model comparisons:

- accounting only;
- accounting + market;
- accounting + market + analyst.

Metrics:

- ROC-AUC;
- PR-AUC;
- balanced accuracy;
- distress-class F1;
- calibration / Brier score;
- false-positive and false-negative rates.

Interpretation:

- marginal effects for the main logit specification;
- compact SHAP summary only if XGBoost is reported;
- detailed SHAP dependence and subgroup SHAP go to supplement, not the main AEL manuscript.

## 9. Frozen Robustness Requirements

Required:

- strict vs broader distress definition;
- 6-month, 12-month, and 24-month prediction windows;
- analyst coverage thresholds: all available, >=2 analysts, >=3 analysts;
- excluding microcaps;
- time split;
- market split;
- financial vs non-financial firms, or exclude financial firms if accounting ratios are not comparable.

Optional:

- pandemic-period split;
- country-specific models;
- annual-panel fallback.

## 10. Frozen Journal Ladder

The lead journal is now corrected after JCR and publisher-metric verification.

### Lead Target

**Applied Economics Letters**

Use as the primary stability-first SSCI Q3 outlet.

Verified evidence, 2026-05-31:

- 2024 JCR edition: SSCI.
- 2024 JCR category: Economics.
- 2024 JIF quartile: Q3.
- 2024 JIF: 1.3.
- Publisher-disclosed acceptance rate: 35%.

Paper form:

- short empirical letter;
- one clean main result;
- minimal method complexity;
- strong leakage audit and robustness.

Applied Economics Letters manuscript constraint:

- working target: <= 2,000 words in the main manuscript;
- no full literature review;
- no more than three main tables;
- online supplement for variable definitions, extra robustness, SHAP, and alternative horizons.

### Stretch Target

**Journal of Behavioral Finance**

Use only if analyst disagreement and behavioral/information-environment framing are very strong, and only if the user accepts low single-journal odds.

Verified evidence, 2026-05-31:

- 2024 JCR edition: SSCI.
- 2024 JCR categories: Business, Finance; Economics.
- 2024 JIF quartile: Q3 in both verified categories.
- 2024 JIF: 1.2.
- Publisher-disclosed acceptance rate: 4%.

Do not use this as the lead journal under a stability-first objective.

### Conditional Target

**Journal of Real Estate Research**

Use only if the final sample is narrowed to REIT / real-estate firms.

Publicly visible evidence:

- Clarivate link list includes related real-estate finance/research titles, but current exact SSCI/Q3 status must be verified in NTU JCR.

### Not a Stable SSCI Q3 Backup

**Research in International Business and Finance**

Use only as higher-tier transfer/candidate. Do not treat it as SSCI Q3 stable target.

**Journal of Economics and Finance**

Do not use for the strict SSCI route. It was checked in JCR on 2026-05-31 and its current edition is ESCI, not SSCI.

## 11. Frozen Acceptance-Probability Interpretation

Do not claim verified single-journal acceptance rates.

Planning estimate:

- first submission: moderate probability;
- second submission after targeted rewrite: moderate probability;
- third verified SSCI Q3-compatible outlet: enough to target 70-80% eventual acceptance if data and results clear the gates.

This is a strategy probability, not a source-backed journal statistic.

## 12. Formal Go / No-Go Gates

### Gate A: Journal Gate

Completed on 2026-05-31 for the first two candidate journals:

- Applied Economics Letters: pass as lead target.
- Journal of Behavioral Finance: pass on SSCI Q3 status, fail as a stability-first lead target because official acceptance rate is 4%.

Before submitting beyond Applied Economics Letters:

- verify each backup journal in NTU JCR;
- record exact title, ISSN, edition, category, JIF, quartile, year, scope, and publisher-disclosed acceptance rate if available.

If no additional SSCI Q3/Q2-compatible backup is verified after pilot results, pause before full manuscript formatting and build the backup list first.

### Gate B: Event Gate

Continue primary route if:

- strict distress events >= 150; or
- broader financial stress events >= 300.

If not:

- expand markets and period once;
- if still not enough, switch to earnings surprise / analyst dispersion backup.

### Gate C: Analyst Coverage Gate

Continue analyst-disagreement framing if:

- analyst variables cover at least 30% of firm-periods; and
- analyst-covered observations include enough distress/stress events for a subsample analysis.

If not:

- downgrade analyst variables to supplementary analysis;
- main paper becomes Asia-Pacific accounting + market distress prediction and must be reframed.

### Gate D: Leakage Gate

Continue only if:

- all accounting, market, and analyst variables are timestamped before the prediction horizon;
- event dates and delisting reasons are auditable;
- no post-event variables leak into predictors.

### Gate E: Results Gate

Continue with Applied Economics Letters if:

- analyst variables improve ROC-AUC, PR-AUC, calibration, or key subsample performance; and
- SHAP results are economically coherent; and
- the result can be expressed as one concise empirical contribution.

For AEL, a publishable result does not require the ML model to be novel. It requires the analyst-disagreement coefficient/marginal effect and incremental prediction evidence to be clean, interpretable, and short enough to defend in a letter format.

Consider Journal of Behavioral Finance only if:

- analyst disagreement is central rather than supplementary;
- the behavioral/information mechanism is strong; and
- the user explicitly accepts the low-probability stretch route.

If analyst variables do not help:

- rewrite for Applied Economics Letters as a focused empirical/null-boundary result only if the null is clean;
- otherwise execute the accounting + market fallback.

## 13. Execution Order

1. Verify SSCI Q3 target journals in NTU JCR.
2. In Capital IQ Screener, count distress/status events first; do not start with random companies.
3. Build event-led pilot sample.
4. Check analyst coverage and firm-period availability.
5. Export full accounting, market, analyst, and event data only after Gates A-C.
6. Build leakage-safe firm-quarter panel.
7. Run baseline models.
8. Run analyst-increment models.
9. Produce SHAP and robustness tables.
10. Freeze target journal based on actual results.

## 14. Locked Decision

Execute this route next.

Do not switch to:

- LLM;
- RL trading;
- earnings surprise prediction;
- multi-agent frameworks;
- generic bankruptcy prediction;

unless one of the formal Go/No-Go gates fails.
