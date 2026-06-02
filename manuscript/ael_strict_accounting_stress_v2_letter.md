# Analyst Coverage and Subsequent Accounting-Based Financial Stress: Evidence from Singapore and Australia

Draft status: Applied Economics Letters strict-accounting-stress v2 draft generated on 2026-06-03.
Target use: Applied Economics Letters submission route after final portal metadata and JCR screen check.

## Abstract

This letter examines whether analyst coverage is associated with subsequent accounting-based financial stress in Singapore and Australian listed firms. Using S&P Capital IQ accounting data and fiscal-year-end analyst estimate snapshots, I build a firm-year panel for fiscal years 2014-2024. The main dependent variable equals one when the following fiscal year has at least two accounting-stress symptoms: negative equity, operating loss, and low interest coverage. In the main sample of 19,322 firm-years and 7,874 strict-stress events, analyst-covered firm-years have lower subsequent strict-stress odds after accounting controls, market fixed effects, fiscal-year fixed effects, and firm-clustered standard errors. The main odds ratio is 0.711, with an average marginal effect of -7.2 percentage points. The association is negative in both ASX and Singapore subsamples and survives structure-name exclusions, operating-status restrictions, COVID outcome-year exclusion, analyst-intensity checks, and alternative stress labels. Altman and event labels are treated as robustness or validation evidence because coverage and ID-matching limitations are material. The result supports a narrow information-environment interpretation rather than a causal or prediction-performance claim.

Keywords: analyst coverage; accounting-based stress; information environment; Singapore; Australia; S&P Capital IQ

JEL codes: G14; G17; G24; G32

## 1. Introduction

Analyst coverage is a visible part of a firm's information environment. In markets with many thinly followed listed firms, the presence of coverage may be informative even before forecast content is examined. Covered firms are usually easier for investors to monitor and compare, while uncovered firms are more likely to be small, opaque, illiquid, or outside regular intermediary attention. This letter asks a narrow empirical question: conditional on observable accounting fundamentals, are analyst-covered firm-years less likely to enter subsequent accounting-based financial stress?

The setting is Singapore and Australia. Both markets contain many listed firms without analyst estimate snapshots, and S&P Capital IQ provides enough historical accounting and analyst data to construct a two-market firm-year panel. The contribution is deliberately bounded. I do not claim that analysts prevent financial stress, that analyst coverage is randomly assigned, or that analyst variables generate a materially better distress-prediction model. The paper instead tests whether coverage is a stable information-environment marker associated with lower future accounting-stress risk.

The design uses a stricter outcome than the earlier broad-stress route. A firm-year is classified as subsequently stressed only if the following fiscal year has at least two accounting symptoms: negative equity, operating loss, and low interest coverage. This definition is still accounting-based, but it reduces single-symptom noise and avoids relying on sparse legal default or bankruptcy events in listed-firm samples.

## 2. Data and Variables

The data come from S&P Capital IQ historical accounting exports, fiscal-year-end analyst estimate snapshots, and supplemental Capital IQ workbooks downloaded and audited for the v2 revision. The local v2 panel contains 21,737 firm-years, 2,335 companies, and fiscal years 2014-2024. One-year-ahead outcome models exclude fiscal years without observable next-year labels. Analyst timing checks remove rows in which a covered forecast date occurs after the fiscal-year-end as-of date.

The main estimation sample contains 19,322 firm-years, 2,322 firms, and 7,874 subsequent strict accounting-stress events. The event rate is 40.8%. ASX contributes 13,936 rows and Singapore contributes 5,386 rows. Analyst coverage is present in 27.0% of the strict sample.

The main analyst variable, `AnalystCovered`, equals one when a firm has at least one analyst estimate in the fiscal-year-end snapshot. Analyst intensity is measured as log one plus the number of analysts. Controls include ROA, leverage, log assets, and revenue growth. Continuous controls are winsorized at the 1st and 99th percentiles. The main model includes market and fiscal-year fixed effects and reports standard errors clustered at the firm level.

Alternative labels are used conservatively. Broad accounting stress is retained only as appendix-style robustness because its event rate is high. Altman-style distress is not used as the primary outcome because the full-component formula has limited coverage, especially where total liabilities are unavailable. Key Developments event labels are treated as candidate validation evidence because the event workbook's direct SPCIq ID does not cleanly align with the baseline company identifier and therefore requires conservative name matching.

## 3. Empirical Specification

The main model is a firm-year logit:

```text
Pr(StrictAccountingStress_{i,t+1}=1) =
logit(alpha + beta AnalystCovered_{i,t} + gamma Controls_{i,t}
      + market fixed effects + fiscal-year fixed effects).
```

The coefficient of interest is beta. A negative beta indicates that covered firm-years have lower subsequent strict accounting-stress odds than comparable uncovered firm-years in the same market and fiscal-year environment. The specification is associational. Analyst coverage may proxy for size, liquidity, governance quality, disclosure quality, investor recognition, or other unobserved firm characteristics.

## 4. Results

Table 1 reports the candidate samples and label scope. The strict accounting-stress sample is the main sample. The broad, persistent, Altman, and event-candidate samples are retained to show how the result behaves under alternative definitions.

Table 2 reports the main estimates. In the combined sample, analyst coverage has a coefficient of -0.342, a firm-clustered standard error of 0.073, and an odds ratio of 0.711. The average marginal effect is -7.2 percentage points. The result is negative and statistically significant after accounting controls, market fixed effects, and fiscal-year fixed effects.

The market split supports the two-market framing. The ASX odds ratio is 0.778 and the Singapore odds ratio is 0.492. The Singapore estimate is larger, but the direction is negative in both markets. Replacing the coverage indicator with analyst intensity gives an odds ratio of 0.630 per log-one-plus analyst count, which is consistent with the information-environment interpretation.

Table 3 reports robustness checks. The result survives dropping suspect structure names, restricting to operating-status rows, and excluding COVID outcome years. The onset sample, which removes firm-years already in strict accounting stress, remains negative but weakens to an odds ratio of 0.856 with p = 0.077. This is an important limitation: part of the main association reflects persistence and selection around already weak firms. The Altman label is directionally supportive but underpowered, while the event-candidate label is significant but remains a validation result rather than a formal bankruptcy/default outcome.

Prediction checks do not support a prediction-performance claim. Adding analyst coverage changes AUC from 0.7101 to 0.7100 and improves Brier score only from 0.2111 to 0.2106. The contribution is therefore a robust conditional association, not a new high-performing stress-prediction model.

## 5. Conclusion

Analyst-covered firm-years in Singapore and Australia have lower subsequent strict accounting-stress odds after accounting controls, market fixed effects, fiscal-year fixed effects, and firm-clustered errors are included. The result is negative in both markets and survives several sample and label checks. The strongest defensible interpretation is narrow: analyst coverage is a marker of the firm information environment associated with lower future accounting-based stress. The evidence does not support causal language, broad Asia-Pacific generalization, tone-based claims, or prediction-performance claims. That conservative framing is the appropriate route for an Applied Economics Letters submission.

## Data Availability

The data used in this study were obtained from S&P Capital IQ under institutional database access and are subject to database licensing and redistribution restrictions. The author cannot redistribute raw Capital IQ exports or firm-level Capital IQ-derived panels. Researchers with their own Capital IQ access may reconstruct the sample using the reported variable definitions, sample filters, and replication code. Non-proprietary aggregate tables and audit outputs are included in the submission materials.

## Tables

### Table 1. Candidate Samples

### Table 2. Main and Market-Split Logit Estimates

### Table 3. Robustness Checks

## References

Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *Journal of Finance*, 23(4), 589-609.

Beaver, W. H. (1966). Financial ratios as predictors of failure. *Journal of Accounting Research*, 4, 71-111.

Bhushan, R. (1989). Firm characteristics and analyst following. *Journal of Accounting and Economics*, 11(2-3), 255-274.

Hong, H., Lim, T., and Stein, J. C. (2000). Bad news travels slowly: Size, analyst coverage, and the profitability of momentum strategies. *Journal of Finance*, 55(1), 265-295.

Lang, M. H., and Lundholm, R. J. (1996). Corporate disclosure policy and analyst behavior. *The Accounting Review*, 71(4), 467-492.

Merton, R. C. (1987). A simple model of capital market equilibrium with incomplete information. *Journal of Finance*, 42(3), 483-510.

Ohlson, J. A. (1980). Financial ratios and the probabilistic prediction of bankruptcy. *Journal of Accounting Research*, 18(1), 109-131.
