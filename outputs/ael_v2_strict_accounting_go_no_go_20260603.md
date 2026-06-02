# AEL v2 Strict Accounting Stress Go/No-Go Audit

Date: 2026-06-03T04:23:09
Input frozen candidate panel: `/Users/guohuiwen/华健 论文/9- 金融/data/processed/ael_apac_firm_year_panel_v2_frozen_candidate_20260603.csv`

## Decision

Status: CONDITIONAL_GO_FOR_STRICT_ACCOUNTING_STRESS_ROUTE

The current v2 result pattern supports a stricter accounting-stress manuscript route, but not a no-risk submission package. The claim should be framed as an association between analyst coverage and subsequent accounting-based stress, not as causal prevention or formal bankruptcy prediction.

## Model Suite

| specification | n | events | event_rate | coef | cluster_se | p_value | odds_ratio | ame | auc | brier | error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main strict accounting stress | 19322 | 7874 | 0.4075 | -0.3417 | 0.0729 | 0.0000 | 0.7106 | -0.0721 | 0.7100 | 0.2106 |  |
| Main without analyst | 19322 | 7874 | 0.4075 |  |  |  |  |  | 0.7101 | 0.2111 |  |
| ASX split | 13936 | 6017 | 0.4318 | -0.2508 | 0.0856 | 0.0034 | 0.7781 | -0.0549 | 0.6950 | 0.2174 |  |
| Singapore split | 5386 | 1857 | 0.3448 | -0.7089 | 0.1466 | 0.0000 | 0.4922 | -0.1208 | 0.8035 | 0.1694 |  |
| Onset sample excluding current strict stress | 11744 | 1717 | 0.1462 | -0.1558 | 0.0881 | 0.0771 | 0.8557 | -0.0181 | 0.6678 | 0.1196 |  |
| Drop suspect structure names | 18760 | 7821 | 0.4169 | -0.3316 | 0.0742 | 0.0000 | 0.7177 | -0.0711 | 0.7020 | 0.2139 |  |
| Operating-status rows only | 19003 | 7666 | 0.4034 | -0.3556 | 0.0741 | 0.0000 | 0.7007 | -0.0749 | 0.7087 | 0.2104 |  |
| COVID outcome-year exclusion | 15291 | 6026 | 0.3941 | -0.3388 | 0.0751 | 0.0000 | 0.7127 | -0.0706 | 0.7108 | 0.2086 |  |
| Analyst intensity log1p count | 19322 | 7874 | 0.4075 | -0.4628 | 0.0521 | 0.0000 | 0.6295 | -0.1240 | 0.7117 | 0.2094 |  |
| Broad stress appendix label | 19344 | 12285 | 0.6351 | -0.5712 | 0.0784 | 0.0000 | 0.5649 | -0.0877 | 0.8845 | 0.1325 |  |
| Persistent broad stress label | 16984 | 9772 | 0.5754 | -0.6215 | 0.0846 | 0.0000 | 0.5371 | -0.1010 | 0.8733 | 0.1428 |  |
| Altman distress robustness label | 3459 | 1418 | 0.4099 | -0.3422 | 0.2021 | 0.0905 | 0.7102 | -0.0715 | 0.7181 | 0.2094 |  |
| Broad event candidate label | 19353 | 4026 | 0.2080 | -0.7504 | 0.0954 | 0.0000 | 0.4722 | -0.0982 | 0.7515 | 0.1438 |  |

## Prediction Increment

| comparison | auc_accounting_only | auc_plus_analyst | delta_auc | brier_accounting_only | brier_plus_analyst | delta_brier |
| --- | --- | --- | --- | --- | --- | --- |
| strict_label_accounting_plus_analyst_minus_accounting_only | 0.7101 | 0.7100 | -0.0001 | 0.2111 | 0.2106 | -0.0005 |

## Reviewer-Level Reading

- Main strict-accounting OR: 0.711; AME: -0.072; p-value: 2.8e-06.
- Market split directions: ASX coef -0.251; Singapore coef -0.709.
- Altman robustness is directionally consistent but weaker: p-value 0.0905; this supports robustness-only treatment.
- Event candidate is directionally strong, but still candidate-level because event matching is not clean direct Entity ID matching.
- Prediction increment is small: delta AUC -0.0001, delta Brier -0.0005. Do not sell this as a prediction-performance paper.

## Route Decision

- Main route: strict accounting-based stress, market/year FE, firm-clustered standard errors.
- Robustness: broad stress appendix, persistent stress, event candidate, Altman candidate, market split, onset sample, COVID exclusion, analyst intensity.
- Do not use Altman as the main dependent variable unless total-liabilities coverage is improved.
- Do not call event evidence bankruptcy/default distress without direct-ID event data or a stricter event taxonomy.
- The result pattern is promising for SSCI/JCR Q3, but the package still needs final table rebuild, manuscript rewrite, journal fit screen, and submission QA.
