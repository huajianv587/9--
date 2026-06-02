# Analyst Coverage and Subsequent Accounting-Based Financial Stress: Evidence from Singapore and Australia

Draft status: v2 strict-accounting-stress route generated on 2026-06-03.
Target use: SSCI/JCR Q3 submission draft after final journal screen and formatting QA.

## Abstract

This paper examines whether analyst coverage is associated with subsequent accounting-based financial stress in Singapore and Australian listed firms. Using S&P Capital IQ accounting data and fiscal-year-end analyst estimate snapshots, I build a firm-year panel covering fiscal years 2014-2024 and estimate forward-looking stress models for fiscal years with observable one-year-ahead outcomes. The main dependent variable is a strict accounting-stress indicator equal to one when the next fiscal year has at least two stress symptoms: negative equity, operating loss, and low interest coverage. The main estimation sample contains 19,322 firm-years, 2,322 firms, and 7,874 subsequent strict accounting-stress events. Analyst-covered firm-years have significantly lower subsequent strict-stress odds after accounting controls, market fixed effects, fiscal-year fixed effects, and firm-clustered standard errors. The main odds ratio is 0.711, with an average marginal effect of -7.2%. The association is negative in both ASX and Singapore subsamples and survives structure-name exclusions, operating-status restrictions, COVID outcome-year exclusion, analyst-intensity checks, and alternative stress labels. Altman and Key Developments event labels are used as robustness or validation evidence rather than as the primary outcome because their coverage and ID-matching limitations are material. Analyst variables do not materially improve predictive AUC, so the paper is framed as an information-environment association rather than a prediction-performance study.

Keywords: analyst coverage; accounting-based stress; information environment; Singapore; Australia; S&P Capital IQ

JEL codes: G14; G17; G24; G32

## 1. Introduction

Analyst coverage is a visible part of a firm's information environment. In listed markets with many thinly followed firms, the extensive margin of coverage may be informative even before the content of analyst forecasts is examined. Covered firms are usually easier for investors to monitor, compare, and value. Uncovered firms are more likely to be small, opaque, illiquid, or outside the regular attention set of intermediaries. These differences motivate a narrow empirical question: conditional on observable accounting fundamentals, are analyst-covered firm-years less likely to move into subsequent accounting-based financial stress?

This paper studies that question using Singapore and Australian listed firms. The setting is useful because both markets contain many firms with no analyst estimate snapshot, while S&P Capital IQ provides enough accounting and analyst data to construct a two-market firm-year panel. The empirical contribution is deliberately bounded. I do not claim that analysts prevent financial stress, that coverage is randomly assigned, or that analyst variables provide a large predictive-performance improvement. The claim is narrower: analyst coverage is a stable marker of lower subsequent accounting-stress risk after standard accounting controls and time/market structure are included.

The earlier broad-stress version of the paper was too vulnerable to reviewer criticism because its event rate was high and the dependent variable was close to general operating weakness. The revised design therefore makes strict subsequent accounting stress the main label. A firm-year is classified as subsequently stressed only if the next fiscal year has at least two accounting stress symptoms. This definition reduces single-symptom noise and creates a more defensible outcome for an SSCI/JCR Q3 submission.

The main result supports the strict route. In the combined sample, analyst coverage has an odds ratio of 0.711 for subsequent strict accounting stress. The estimate is negative and significant in ASX, with an odds ratio of 0.778, and in Singapore, with an odds ratio of 0.492. The onset sample, which excludes firm-years already in strict accounting stress, remains negative but weakens statistically. This pattern is useful for positioning: analyst coverage is not a cure for financial stress, but it is a robust conditional marker of lower subsequent stress risk.

The paper contributes to applied empirical finance in three ways. First, it provides two-market evidence on analyst coverage and accounting-based stress in Singapore and Australia rather than relying on a single-country sample. Second, it separates broad accounting weakness, strict accounting stress, Altman-style distress, and event-based stress evidence instead of forcing one dependent variable to carry every claim. Third, it explicitly reports that analyst variables add little predictive-performance value once accounting controls are included. This keeps the contribution in the information-environment literature rather than overselling the paper as a distress-prediction model.

## 2. Literature and Hypothesis Development

Analyst coverage can reduce information frictions through monitoring, forecasts, reports, and investor attention. Classic information-environment arguments imply that firms followed by analysts are more visible and easier to evaluate than unfollowed firms. Work on investor recognition, analyst following, disclosure, and information diffusion provides the conceptual basis for treating coverage as a marker of capital-market attention.

Financial-stress models traditionally emphasize accounting fundamentals, leverage, profitability, liquidity, and market information. Bankruptcy and distress studies show that accounting and market variables can be powerful predictors. However, listed-firm stress is not purely a balance-sheet outcome. Visibility, financing access, monitoring, and investor attention may also correlate with a firm's ability to avoid or delay accounting deterioration. Analyst coverage may therefore be informative even after accounting controls are included.

The first hypothesis is framed as an association rather than a causal effect:

**H1.** Analyst-covered firm-years have lower subsequent strict accounting-stress odds than otherwise comparable uncovered firm-years.

Among covered firms, analyst intensity may also matter. A larger number of analysts could indicate a stronger information environment, but analyst counts are endogenous and highly correlated with firm size and visibility. I therefore treat analyst intensity as a robustness check:

**H2.** Greater analyst intensity is negatively associated with subsequent strict accounting stress, but this evidence is secondary to the coverage indicator.

## 3. Data and Variables

The data come from S&P Capital IQ historical accounting exports, fiscal-year-end analyst estimate snapshots, and supplemental Capital IQ raw workbooks downloaded and audited for this revision. The local v2 panel has 21,737 firm-years, 2,335 companies, and fiscal years 2014-2024. Modelled one-year-ahead outcomes exclude fiscal years without an observable next-year label. Analyst timing checks remove rows in which a covered forecast date occurs after the as-of date.

The main estimation sample is the strict accounting-stress 12-month sample. It contains 19,322 firm-years, 2,322 firms, and 7,874 stress events, with an event rate of 40.8%. ASX contributes 13,936 rows and Singapore contributes 5,386 rows. Analyst coverage is present in 27.0% of the strict sample.

The main dependent variable, `StrictAccountingStress_{t+1}`, equals one if the next fiscal year satisfies at least two of three conditions: negative equity, operating loss, and interest coverage below 1.5. This label is more conservative than the earlier broad-stress label, whose sample contains 19,344 rows and an event rate of 63.5%. Broad stress is retained as appendix evidence only.

I also construct Altman-style and event-based candidates. The Altman sample contains 3,459 firm-years and 1,418 events, but its coverage is much smaller because the full-component formula requires current assets, current liabilities, retained earnings, market capitalization, total liabilities, EBIT, revenue, and total assets. Total-liabilities coverage is the binding bottleneck, especially for Singapore, so Altman is not used as the main outcome. The Key Developments event candidate sample contains 19,353 firm-years and 4,026 events, but the event export's direct SPCIq ID does not cleanly overlap with the baseline company ID. Event labels therefore rely on conservative name matching and are used as validation evidence rather than formal bankruptcy/default outcomes.

The main analyst variable is `AnalystCovered`, equal to one when a firm has at least one analyst estimate in the fiscal-year-end snapshot. Analyst intensity is measured as log one plus the number of analysts. Controls include ROA, leverage, log assets, and revenue growth. Continuous controls and candidate Altman components are winsorized at the 1st and 99th percentiles. The main model includes market and fiscal-year fixed effects and reports firm-clustered standard errors.

Table 1 reports the candidate samples. Table 2 reports descriptive statistics in the common cleaned sample.

## 4. Empirical Specification

The main model is a firm-year logit:

```text
Pr(StrictAccountingStress_{i,t+1} = 1) =
logit(alpha + beta AnalystCovered_{i,t} + gamma Controls_{i,t}
      + market fixed effects + fiscal-year fixed effects).
```

The coefficient of interest is beta. A negative beta indicates that covered firm-years have lower subsequent strict accounting-stress odds than comparable uncovered firm-years in the same market and fiscal-year environment. Standard errors are clustered at the firm level to account for repeated firm-year observations.

The model is intentionally associational. Analyst coverage is not randomly assigned. Analysts tend to follow larger and more visible firms, and the controls cannot remove all selection. The paper therefore avoids causal wording and treats analyst coverage as an information-environment marker.

The robustness design has four layers. First, the model is estimated separately for ASX and Singapore. Second, sample restrictions remove already-stressed firm-years, suspect REIT/fund/trust/SPAC-like names, non-operating status rows, and COVID outcome years. Third, the dependent variable is replaced by broad stress, persistent stress, Altman distress, and a broad event candidate. Fourth, analyst coverage is replaced by log one plus the number of analysts. Prediction checks compare AUC and Brier score with and without the analyst variable.

## 5. Results

Table 3 reports the main and market-split estimates. In the combined strict accounting-stress sample, analyst coverage has a coefficient of -0.342, a firm-clustered standard error of 0.073, and an odds ratio of 0.711. The average marginal effect is -7.2%. The association is economically meaningful but should not be read as a treatment effect.

The market split supports the two-market story. The ASX coefficient is -0.251, with an odds ratio of 0.778. The Singapore coefficient is -0.709, with an odds ratio of 0.492. The effect is larger in Singapore, but the direction is negative in both markets.

Table 4 reports robustness checks. Excluding suspect structure names gives an odds ratio of 0.718. Restricting to operating-status rows gives an odds ratio of 0.701. Excluding COVID outcome years gives an odds ratio of 0.713. Replacing the coverage indicator with analyst intensity gives an odds ratio of 0.630 per log-one-plus analyst count. These checks support the interpretation that analyst attention is a stable marker of lower subsequent accounting-stress risk.

The onset sample is more cautious. Excluding firm-years already in strict accounting stress reduces the coefficient to -0.156, with an odds ratio of 0.856 and p-value 0.077. The sign remains negative, but significance weakens. This is an important limitation: part of the main association reflects persistence and the fact that already-weak firms are less likely to attract analyst coverage.

Alternative labels are informative but should not become the main story. The broad-stress appendix label produces a stronger negative association, but its event rate is too high for a clean financial-distress claim. The persistent stress label is also negative and significant. The Altman label has an odds ratio of 0.710 but p-value 0.090, which is directionally supportive but underpowered. The broad event candidate has an odds ratio of 0.472, but because event matching is not clean direct-ID matching, the paper should describe it as validation evidence rather than a formal event-distress result.

Table 5 reports prediction increments. Adding analyst coverage changes AUC from 0.7101 to 0.7100, a delta of -0.0001. The Brier score improves only from 0.2111 to 0.2106. The prediction increment is therefore negligible. This result strengthens the paper's positioning: the contribution is a robust conditional association, not a new high-performing prediction model.

## 6. Discussion and Scope

The revised evidence is stronger than the old broad-stress version because the main dependent variable is stricter and the story is less vulnerable to the criticism that any weak operating outcome is labelled as financial distress. The strict accounting-stress label still has a high event rate, but it requires multiple symptoms and is more defensible for a Q3 empirical paper.

The most important limitation is endogeneity. Analyst coverage may proxy for firm visibility, liquidity, governance quality, disclosure quality, or investor recognition. The negative coefficient should therefore be interpreted as a conditional association. The paper should not say that analyst coverage reduces stress or that expanding coverage would mechanically lower default risk.

The second limitation is label taxonomy. Altman is not strong enough to be the main label because full-component coverage is limited. Event evidence is not clean enough to be a formal distress label because the current event export lacks direct ID alignment with the baseline panel. The manuscript should be explicit that these labels are robustness or validation checks.

The third limitation is text and tone. The current v2 firm-year panel does not contain tone fields or raw text quality indicators. The final paper should not claim tone extraction unless a separate text dataset is audited and merged. For the present route, tone is removed from the core claim.

The fourth limitation is journal fit. The paper is best positioned as an applied empirical finance or applied economics article about analyst coverage and accounting-based stress in two Asia-Pacific markets. It is not a causal identification paper, not a machine-learning prediction paper, and not evidence for all Asia-Pacific markets.

## 7. Conclusion

This paper shows that analyst-covered firm-years in Singapore and Australia have lower subsequent strict accounting-stress odds after accounting controls, market fixed effects, fiscal-year fixed effects, and firm-clustered errors are included. The result is negative in both markets and survives several sample and label robustness checks. The strongest defensible contribution is narrow: analyst coverage is a marker of the firm information environment associated with lower future accounting-based stress. The evidence does not support causal language or a prediction-performance claim, but it does support a disciplined SSCI/JCR Q3 route built around strict accounting-based stress.

## Data Availability

The data used in this study were obtained from S&P Capital IQ under institutional database access and are subject to database licensing and redistribution restrictions. The author cannot redistribute raw Capital IQ exports or firm-level Capital IQ-derived panels. Researchers with their own Capital IQ access may reconstruct the sample using the reported variable definitions, sample filters, and replication code. Non-proprietary aggregate tables and audit outputs are included in the submission materials.

## Tables

### Table 1. Candidate Samples

| Sample | Firm-years | Firms | Stress events | Event rate | Coverage rate | ASX rows | Singapore rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Broad stress appendix | 19344 | 2322 | 12285 | 63.5% | 26.9% | 13946 | 5398 |
| Strict accounting stress 12m | 19322 | 2322 | 7874 | 40.8% | 27.0% | 13936 | 5386 |
| Persistent broad stress 24m | 16984 | 2278 | 9772 | 57.5% | 26.7% | 12251 | 4733 |
| Altman distress zone 12m | 3459 | 618 | 1418 | 41.0% | 24.2% | 3280 | 179 |
| Broad event candidate 12m | 19353 | 2322 | 4026 | 20.8% | 26.9% | 13947 | 5406 |
| Broad event candidate 24m | 17037 | 2282 | 4728 | 27.8% | 26.6% | 12271 | 4766 |

### Table 2. Descriptive Statistics

| Variable | N | Mean | SD | P25 | Median | P75 |
| --- | --- | --- | --- | --- | --- | --- |
| Analyst covered | 21679 | 0.240 | 0.427 | 0.000 | 0.000 | 0.000 |
| Number of analysts | 5213 | 4.996 | 4.670 | 1.000 | 3.000 | 8.000 |
| ROA | 21520 | -0.372 | 1.190 | -0.293 | -0.046 | 0.041 |
| Leverage | 21443 | 0.217 | 0.429 | 0.000 | 0.075 | 0.285 |
| Log assets | 21526 | 10.568 | 2.621 | 8.767 | 10.295 | 12.235 |
| Revenue growth | 15558 | 1.199 | 6.804 | -0.142 | 0.047 | 0.318 |
| Broad stress t+1 | 19344 | 0.635 | 0.481 | 0.000 | 1.000 | 1.000 |
| Strict accounting stress t+1 | 19322 | 0.408 | 0.491 | 0.000 | 0.000 | 1.000 |
| Persistent broad stress t+1/t+2 | 16984 | 0.575 | 0.494 | 0.000 | 1.000 | 1.000 |
| Altman distress-zone t+1 | 3731 | 0.434 | 0.496 | 0.000 | 0.000 | 1.000 |
| Broad event candidate t+1 | 21679 | 0.186 | 0.389 | 0.000 | 0.000 | 0.000 |

### Table 3. Main and Market-Split Logit Estimates

| Specification | N | Events | Event rate | Coefficient | Cluster SE | Odds ratio | AME | AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main strict accounting stress | 19322 | 7874 | 40.8% | -0.342*** | 0.073 | 0.711 | -0.072 | 0.710 |
| ASX split | 13936 | 6017 | 43.2% | -0.251*** | 0.086 | 0.778 | -0.055 | 0.695 |
| Singapore split | 5386 | 1857 | 34.5% | -0.709*** | 0.147 | 0.492 | -0.121 | 0.804 |
| Analyst intensity log1p count | 19322 | 7874 | 40.8% | -0.463*** | 0.052 | 0.630 | -0.124 | 0.712 |

### Table 4. Robustness Checks

| Specification | N | Events | Coefficient | Cluster SE | Odds ratio | AME |
| --- | --- | --- | --- | --- | --- | --- |
| Onset sample excluding current strict stress | 11744 | 1717 | -0.156* | 0.088 | 0.856 | -0.018 |
| Drop suspect structure names | 18760 | 7821 | -0.332*** | 0.074 | 0.718 | -0.071 |
| Operating-status rows only | 19003 | 7666 | -0.356*** | 0.074 | 0.701 | -0.075 |
| COVID outcome-year exclusion | 15291 | 6026 | -0.339*** | 0.075 | 0.713 | -0.071 |
| Broad stress appendix label | 19344 | 12285 | -0.571*** | 0.078 | 0.565 | -0.088 |
| Persistent broad stress label | 16984 | 9772 | -0.622*** | 0.085 | 0.537 | -0.101 |
| Altman distress robustness label | 3459 | 1418 | -0.342* | 0.202 | 0.710 | -0.072 |
| Broad event candidate label | 19353 | 4026 | -0.750*** | 0.095 | 0.472 | -0.098 |

### Table 5. Prediction Increment

| Comparison | AUC controls | AUC + analyst | Delta AUC | Brier controls | Brier + analyst | Delta Brier |
| --- | --- | --- | --- | --- | --- | --- |
| strict_label_accounting_plus_analyst_minus_accounting_only | 0.7101 | 0.7100 | -0.0001 | 0.2111 | 0.2106 | -0.0005 |

## References

Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *Journal of Finance*, 23(4), 589-609.

Beaver, W. H. (1966). Financial ratios as predictors of failure. *Journal of Accounting Research*, 4, 71-111.

Bhushan, R. (1989). Firm characteristics and analyst following. *Journal of Accounting and Economics*, 11(2-3), 255-274.

Brennan, M. J., and A. Subrahmanyam. (1995). Investment analysis and price formation in securities markets. *Journal of Financial Economics*, 38(3), 361-381.

Campbell, J. Y., J. Hilscher, and J. Szilagyi. (2008). In search of distress risk. *Journal of Finance*, 63(6), 2899-2939.

Healy, P. M., and K. G. Palepu. (2001). Information asymmetry, corporate disclosure, and the capital markets: A review of the empirical disclosure literature. *Journal of Accounting and Economics*, 31(1-3), 405-440.

Hong, H., T. Lim, and J. C. Stein. (2000). Bad news travels slowly: Size, analyst coverage, and the profitability of momentum strategies. *Journal of Finance*, 55(1), 265-295.

Kelly, B., and A. Ljungqvist. (2012). Testing asymmetric-information asset pricing models. *Review of Financial Studies*, 25(5), 1366-1413.

Lang, M. H., and R. Lundholm. (1996). Corporate disclosure policy and analyst behavior. *The Accounting Review*, 71(4), 467-492.

Merton, R. C. (1987). A simple model of capital market equilibrium with incomplete information. *Journal of Finance*, 42(3), 483-510.

Ohlson, J. A. (1980). Financial ratios and the probabilistic prediction of bankruptcy. *Journal of Accounting Research*, 18(1), 109-131.

Piotroski, J. D. (2000). Value investing: The use of historical financial statement information to separate winners from losers. *Journal of Accounting Research*, 38, 1-41.

Shumway, T. (2001). Forecasting bankruptcy more accurately: A simple hazard model. *Journal of Business*, 74(1), 101-124.
