# AEL APAC v2 Sample Freeze and Cleaning Audit

Date: 2026-06-03T04:17:34
Input panel: `/Users/guohuiwen/华健 论文/9- 金融/data/processed/ael_apac_firm_year_panel_v2_capital_iq_20260603.csv`
Local frozen candidate panel: `/Users/guohuiwen/华健 论文/9- 金融/data/processed/ael_apac_firm_year_panel_v2_frozen_candidate_20260603.csv`

## Decision

Status: PROVISIONAL_SAMPLE_FREEZE_NOT_FINAL_SUBMISSION_SAMPLE

The v2 panel has been converted into auditable candidate samples with explicit exclusion flags, winsorized controls, next-year label candidates, and preliminary logit checks. This is progress toward the data-freeze gate, not a final no-risk submission dataset.

## Freeze Rules Applied

- Drop duplicate company-year rows from model samples; current duplicate count is shown below.
- Keep only recognized markets: ASX and SINGAPORE.
- Drop rows where a covered analyst forecast date is after its as-of date; uncovered rows are not penalized for missing forecast/as-of dates.
- Keep FY2024 out of forward 12-month event/broad-stress samples and FY2023-FY2024 out of 24-month forward samples when the event window is not observable.
- Build next-year strict accounting stress from negative equity, operating loss, and low interest coverage.
- Build next-year Altman distress by shifting the full-component Altman distress-zone candidate one fiscal year ahead.
- Exclude name-flagged REIT/fund/trust/SPAC-like firms from the Altman candidate sample only; this is a conservative proxy until industry classifications are available.
- Winsorize continuous controls and candidate Altman components at the 1st/99th percentiles.

## Exclusion Counts

- Total rows: 21,737
- Unique companies: 2,335
- Duplicate company-year rows: 0
- Analyst timing violations: 58
- Suspect structure name rows: 653
- Suspect structure companies: 72
- Non-operating status rows: 365

## Candidate Sample Counts

| sample | rows | firms | events | event_rate | covered_rate | asx_rows | singapore_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Broad stress appendix | 19344 | 2322 | 12285 | 0.6351 | 0.2695 | 13946 | 5398 |
| Strict accounting stress 12m | 19322 | 2322 | 7874 | 0.4075 | 0.2698 | 13936 | 5386 |
| Persistent broad stress 24m | 16984 | 2278 | 9772 | 0.5754 | 0.2673 | 12251 | 4733 |
| Altman distress zone 12m | 3459 | 618 | 1418 | 0.4099 | 0.2423 | 3280 | 179 |
| Broad event candidate 12m | 19353 | 2322 | 4026 | 0.2080 | 0.2694 | 13947 | 5406 |
| Broad event candidate 24m | 17037 | 2282 | 4728 | 0.2775 | 0.2665 | 12271 | 4766 |

## Preliminary Logit Checks

| label | n | events | event_rate | coef | cluster_se | p_value | odds_ratio | ame | error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Broad stress appendix | 19344 | 12285 | 0.6351 | -0.5712 | 0.0784 | 0.0000 | 0.5649 | -0.0877 |  |
| Strict accounting stress 12m | 19322 | 7874 | 0.4075 | -0.3417 | 0.0729 | 0.0000 | 0.7106 | -0.0721 |  |
| Persistent broad stress 24m | 16984 | 9772 | 0.5754 | -0.6215 | 0.0846 | 0.0000 | 0.5371 | -0.1010 |  |
| Altman distress zone 12m | 3459 | 1418 | 0.4099 | -0.3422 | 0.2021 | 0.0905 | 0.7102 | -0.0715 |  |
| Broad event candidate 12m | 19353 | 4026 | 0.2080 | -0.7504 | 0.0954 | 0.0000 | 0.4722 | -0.0982 |  |

## Winsorization Rules

| variable | n | p01 | p99 | rule |
| --- | --- | --- | --- | --- |
| roa | 21578 | -9.0702 | 0.4513 | clip_p01_p99 |
| roe | 21591 | -10.4815 | 7.9322 | clip_p01_p99 |
| leverage | 21501 | 0.0000 | 3.2992 | clip_p01_p99 |
| interest_coverage | 16209 | -9947.6315 | 1516.7563 | clip_p01_p99 |
| operating_margin | 17822 | -3177.0496 | 1.4509 | clip_p01_p99 |
| revenue_growth | 15612 | -0.9967 | 58.6425 | clip_p01_p99 |
| log_assets | 21584 | 4.2131 | 17.2046 | clip_p01_p99 |
| altman_z_ciq_candidate | 4102 | -235.2188 | 210.9106 | clip_p01_p99 |
| altman_x1_working_capital_assets_ciq | 20104 | -4.4347 | 0.9638 | clip_p01_p99 |
| altman_x2_retained_earnings_assets_ciq | 20156 | -130.4952 | 0.6419 | clip_p01_p99 |
| altman_x3_ebit_assets_ciq | 21259 | -7.0154 | 0.4060 | clip_p01_p99 |
| altman_x4_market_value_liabilities_ciq | 6990 | 0.0886 | 448.5191 | clip_p01_p99 |
| altman_x5_sales_assets_ciq | 18049 | 0.0000 | 4.2049 | clip_p01_p99 |
| market_cap_ciq_usd_m | 18739 | 1.0146 | 19305.8170 | clip_p01_p99 |

## Descriptive Statistics

| variable | n | mean | std | p25 | median | p75 |
| --- | --- | --- | --- | --- | --- | --- |
| analyst_covered | 21679 | 0.2405 | 0.4274 | 0.0000 | 0.0000 | 0.0000 |
| num_analysts | 5213 | 4.9956 | 4.6701 | 1.0000 | 3.0000 | 8.0000 |
| roa_w | 21520 | -0.3725 | 1.1896 | -0.2931 | -0.0460 | 0.0405 |
| leverage_w | 21443 | 0.2165 | 0.4290 | 0.0000 | 0.0747 | 0.2855 |
| log_assets_w | 21526 | 10.5683 | 2.6209 | 8.7671 | 10.2945 | 12.2355 |
| revenue_growth_w | 15558 | 1.1992 | 6.8040 | -0.1423 | 0.0468 | 0.3183 |
| broad_stress_12m_appendix | 19344 | 0.6351 | 0.4814 | 0.0000 | 1.0000 | 1.0000 |
| strict_accounting_stress_12m_candidate | 19322 | 0.4075 | 0.4914 | 0.0000 | 0.0000 | 1.0000 |
| persistent_broad_stress_24m_candidate | 16984 | 0.5754 | 0.4943 | 0.0000 | 1.0000 | 1.0000 |
| altman_distress_12m_candidate | 3731 | 0.4339 | 0.4957 | 0.0000 | 0.0000 | 1.0000 |
| event_distress_12m_candidate | 21679 | 0.1857 | 0.3889 | 0.0000 | 0.0000 | 0.0000 |

## Reviewer-Level Interpretation

- Broad stress remains appendix-only because its event rate is high and was already identified as too broad for the main Q3 claim.
- Strict accounting stress is the most defensible current main-label candidate from the available data because it is forward-looking, uses transparent accounting components, and has full-panel coverage after timing exclusions.
- Altman distress is not yet strong enough as the main label because the full-component sample is much smaller and total-liabilities coverage is the binding bottleneck, especially for Singapore.
- Broad Key Developments event labels are useful as a validation/robustness candidate, but not as formal bankruptcy/default evidence because event matching currently uses conservative company-name matching rather than clean direct Entity ID overlap.
- Tone/text cleaning cannot be marked complete from this panel because no tone or raw text quality fields are present in the v2 firm-year file; this remains a separate data/input gap if the final paper keeps a tone-extraction component.

## Next Gate

Use this frozen candidate panel to rerun the full table suite around the strict accounting stress label, then decide whether the result pattern is strong enough for the SSCI/JCR Q3 route. If strict accounting and event/Altman robustness do not align, downgrade the paper story rather than forcing a stronger claim.
