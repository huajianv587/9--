# AEL APAC Firm-Year Panel v2 Capital IQ Audit

Date: 2026-06-03T04:08:43
Output panel: `/Users/guohuiwen/华健 论文/9- 金融/data/processed/ael_apac_firm_year_panel_v2_capital_iq_20260603.csv`

## Decision

Status: PROVISIONAL_V2_PANEL_BUILT_NOT_SAMPLE_FROZEN

The script built one auditable v2 panel from the baseline firm-year panel and the Capital IQ supplemental raw workbooks. This is not yet the final submission dataset because sample exclusions, winsorization, and model Go/No-Go decisions still need to be frozen after reviewing this audit.

## Panel Shape

- Baseline rows: 21,737
- v2 rows: 21,737
- Unique companies: 2,335
- Fiscal years: 2014-2024
- Duplicate company-year rows: 0

## Raw Source Evidence

### liquidity_market
- `capital_iq_asx_altman_liquidity_marketcap_2014_2024_full_20260602.xlsx`: rows=1,696, sha256=`1ad69aa99d85b21606956923ce2f9d176551c70cc12c6475921d1df77618ef42`
- `capital_iq_sgx_altman_liquidity_marketcap_2014_2024_20260602.xlsx`: rows=354, sha256=`e27e8d8eb8074add68b3ee64cca322e56b7cc6bd52bd0f36a84b5b25cf4d8c2b`
- `capital_iq_catalist_altman_liquidity_marketcap_2014_2024_20260602.xlsx`: rows=190, sha256=`251188716e26d762ca22630b11466e20450badba5a0008c408cb476fe3994e14`
- Duplicate field-key/parameter pairs handled by first-nonmissing rule: `{'SP_CURRENT_LIAB|Latest Fiscal Year': 2, 'SP_CURRENT_LIAB|Latest Fiscal Quarter': 2, 'SP_CURRENT_LIAB|Year-to-Date': 2, 'SP_CURRENT_LIAB|Last Twelve Months': 2, 'SP_CURRENT_LIAB|Latest Half-Year': 2, 'SP_CURRENT_LIAB|FY2025': 2, 'SP_CURRENT_LIAB|FY2024': 2, 'SP_CURRENT_LIAB|FY2023': 2, 'SP_CURRENT_LIAB|FY2022': 2, 'SP_CURRENT_LIAB|FY2021': 2, 'SP_CURRENT_LIAB|FY2020': 2, 'SP_CURRENT_LIAB|FY2019': 2, 'SP_CURRENT_LIAB|FY2018': 2, 'SP_CURRENT_LIAB|FY2017': 2, 'SP_CURRENT_LIAB|FY2016': 2, 'SP_CURRENT_LIAB|FY2015': 2, 'SP_CURRENT_LIAB|FY2014': 2, 'SP_CURRENT_LIAB|FY2013': 2, 'SP_CURRENT_LIAB|FY2012': 2, 'SP_CURRENT_LIAB|FY2011': 2}`

### total_liabilities
- `capital_iq_asx_total_liabilities_candidate_snl_2014_2024_20260602.xlsx`: rows=1,696, sha256=`cb270800bd9bc5d610a5df7c826eb73a5496582011838afe92aee1bca10b5111`
- `capital_iq_sgx_catalist_total_liabilities_candidate_snl_2014_2024_20260602.xlsx`: rows=544, sha256=`87e510af0f465d4ce5121ac2e4b3fb95b30528594d655d2c7a3444a8f5425346`

### retained_earnings
- `capital_iq_asx_retained_earnings_iq_2014_2024_20260602.xlsx`: rows=1,696, sha256=`d79d515c34ef20cfbf7412f6e38555ce8e3631879ebad86af9cdb5e3ee26cfc4`
- `capital_iq_sgx_catalist_retained_earnings_iq_2014_2024_20260602.xlsx`: rows=544, sha256=`7c4ef295435c526c188b82d8afb9cc324819412d0098a6dac7e6c2a1df139c42`
- Duplicate field-key/parameter pairs handled by first-nonmissing rule: `{'IQ_RETAINED_EARNINGS|Latest Fiscal Year': 2, 'IQ_RETAINED_EARNINGS|Latest Fiscal Quarter': 2, 'IQ_RETAINED_EARNINGS|Year-to-Date': 2, 'IQ_RETAINED_EARNINGS|Last Twelve Months': 2, 'IQ_RETAINED_EARNINGS|Latest Half-Year': 2, 'IQ_RETAINED_EARNINGS|FY2025': 2, 'IQ_RETAINED_EARNINGS|FY2024': 2, 'IQ_RETAINED_EARNINGS|FY2023': 2, 'IQ_RETAINED_EARNINGS|FY2022': 2, 'IQ_RETAINED_EARNINGS|FY2021': 2, 'IQ_RETAINED_EARNINGS|FY2020': 2, 'IQ_RETAINED_EARNINGS|FY2019': 2, 'IQ_RETAINED_EARNINGS|FY2018': 2, 'IQ_RETAINED_EARNINGS|FY2017': 2, 'IQ_RETAINED_EARNINGS|FY2016': 2, 'IQ_RETAINED_EARNINGS|FY2015': 2, 'IQ_RETAINED_EARNINGS|FY2014': 2, 'IQ_RETAINED_EARNINGS|FY2013': 2, 'IQ_RETAINED_EARNINGS|FY2012': 2, 'IQ_RETAINED_EARNINGS|FY2011': 2}`

### status_universe
- `capital_iq_aus_sg_public_company_broad_identifier_status_ipo_20260602.xlsx`: rows=3,005, sha256=`d30bab03d9c916051d277b68fc61fb903fd70fdae8744e070205a3063f3e10cc`

### distress_events
- `capital_iq_key_developments_distress_events_aus_sg_2010_2024_20260602.xlsx`: raw rows=44,682, parseable dates=44,682, distress-keyword rows in 2010-2024=14,105, sha256=`8b2b560221947c7a39578ec1a1110b60d6a9afab27c0c57dbfd22af6ddb57545`
- Direct `SPCIQ ID` overlap with baseline `company_id`: 1
- Conservative unique-name map keys: 1,859
- Mapped distress-event rows after conservative name matching: 5,492
- Unique mapped event company IDs: 1,172
- Event matching is therefore a candidate mapping, not a clean direct-ID mapping; a reviewer-facing strict-event label should either disclose this limitation or be rebuilt from an event export that includes the same Entity ID used in the baseline panel.

## Model-ID Coverage

| Source block | Export IDs | Overlap with baseline IDs | Missing baseline IDs |
|---|---:|---:|---:|
| Liquidity/market | 2,240 | 2,162 | 173 |
| Total liabilities | 2,240 | 2,162 | 173 |
| Retained earnings | 2,240 | 2,162 | 173 |
| Broad status universe | 3,005 | 2,274 | 61 |
| Distress events | 1,172 | 1,172 | 1,163 |

## Key Field Coverage by Market-Year

| market | fiscal_year | rows | current_assets_ciq_usd_000_nonmissing | current_assets_ciq_usd_000_missing_pct | current_liabilities_ciq_usd_000_nonmissing | current_liabilities_ciq_usd_000_missing_pct | market_cap_ciq_usd_m_nonmissing | market_cap_ciq_usd_m_missing_pct | total_liabilities_ciq_usd_000_nonmissing | total_liabilities_ciq_usd_000_missing_pct | retained_earnings_ciq_usd_000_nonmissing | retained_earnings_ciq_usd_000_missing_pct | altman_z_ciq_candidate_nonmissing | altman_z_ciq_candidate_missing_pct | distress_event_12m_ciq_nonmissing | distress_event_12m_ciq_missing_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASX | 2014 | 1095 | 1065 | 2.74 | 1058 | 3.38 | 915 | 16.44 | 480 | 56.16 | 1076 | 1.74 | 313 | 71.42 | 1095 | 0.0 |
| ASX | 2015 | 1150 | 1117 | 2.87 | 1117 | 2.87 | 980 | 14.78 | 491 | 57.3 | 1130 | 1.74 | 312 | 72.87 | 1150 | 0.0 |
| ASX | 2016 | 1209 | 1173 | 2.98 | 1177 | 2.65 | 1055 | 12.74 | 500 | 58.64 | 1192 | 1.41 | 305 | 74.77 | 1209 | 0.0 |
| ASX | 2017 | 1290 | 1257 | 2.56 | 1258 | 2.48 | 1133 | 12.17 | 531 | 58.84 | 1270 | 1.55 | 313 | 75.74 | 1290 | 0.0 |
| ASX | 2018 | 1376 | 1335 | 2.98 | 1338 | 2.76 | 1203 | 12.57 | 562 | 59.16 | 1353 | 1.67 | 315 | 77.11 | 1376 | 0.0 |
| ASX | 2019 | 1450 | 1405 | 3.1 | 1405 | 3.1 | 1239 | 14.55 | 587 | 59.52 | 1426 | 1.66 | 306 | 78.9 | 1450 | 0.0 |
| ASX | 2020 | 1495 | 1457 | 2.54 | 1460 | 2.34 | 1313 | 12.17 | 623 | 58.33 | 1478 | 1.14 | 326 | 78.19 | 1495 | 0.0 |
| ASX | 2021 | 1589 | 1562 | 1.7 | 1563 | 1.64 | 1488 | 6.36 | 712 | 55.19 | 1571 | 1.13 | 370 | 76.71 | 1589 | 0.0 |
| ASX | 2022 | 1649 | 1621 | 1.7 | 1622 | 1.64 | 1576 | 4.43 | 762 | 53.79 | 1631 | 1.09 | 369 | 77.62 | 1649 | 0.0 |
| ASX | 2023 | 1676 | 1649 | 1.61 | 1651 | 1.49 | 1611 | 3.88 | 785 | 53.16 | 1664 | 0.72 | 396 | 76.37 | 1676 | 0.0 |
| ASX | 2024 | 1684 | 1658 | 1.54 | 1659 | 1.48 | 1642 | 2.49 | 792 | 52.97 | 1674 | 0.59 | 413 | 75.48 | 1684 | 0.0 |
| SINGAPORE | 2014 | 442 | 390 | 11.76 | 390 | 11.76 | 366 | 17.19 | 46 | 89.59 | 386 | 12.67 | 28 | 93.67 | 442 | 0.0 |
| SINGAPORE | 2015 | 467 | 404 | 13.49 | 404 | 13.49 | 374 | 19.91 | 47 | 89.94 | 398 | 14.78 | 28 | 94.0 | 467 | 0.0 |
| SINGAPORE | 2016 | 499 | 419 | 16.03 | 419 | 16.03 | 385 | 22.85 | 49 | 90.18 | 414 | 17.03 | 30 | 93.99 | 499 | 0.0 |
| SINGAPORE | 2017 | 513 | 422 | 17.74 | 422 | 17.74 | 403 | 21.44 | 50 | 90.25 | 414 | 19.3 | 30 | 94.15 | 513 | 0.0 |
| SINGAPORE | 2018 | 530 | 436 | 17.74 | 436 | 17.74 | 415 | 21.7 | 53 | 90.0 | 424 | 20.0 | 33 | 93.77 | 530 | 0.0 |
| SINGAPORE | 2019 | 546 | 443 | 18.86 | 443 | 18.86 | 422 | 22.71 | 57 | 89.56 | 430 | 21.25 | 35 | 93.59 | 546 | 0.0 |
| SINGAPORE | 2020 | 574 | 455 | 20.73 | 455 | 20.73 | 434 | 24.39 | 60 | 89.55 | 439 | 23.52 | 38 | 93.38 | 574 | 0.0 |
| SINGAPORE | 2021 | 594 | 455 | 23.4 | 455 | 23.4 | 439 | 26.09 | 60 | 89.9 | 439 | 26.09 | 35 | 94.11 | 594 | 0.0 |
| SINGAPORE | 2022 | 627 | 468 | 25.36 | 468 | 25.36 | 445 | 29.03 | 61 | 90.27 | 452 | 27.91 | 35 | 94.42 | 627 | 0.0 |
| SINGAPORE | 2023 | 640 | 468 | 26.88 | 468 | 26.88 | 448 | 30.0 | 60 | 90.62 | 456 | 28.75 | 36 | 94.38 | 640 | 0.0 |
| SINGAPORE | 2024 | 642 | 467 | 27.26 | 467 | 27.26 | 453 | 29.44 | 60 | 90.65 | 454 | 29.28 | 36 | 94.39 | 642 | 0.0 |

## Label Candidate Rates

| Label | Non-missing rows | Positive rows | Positive rate among non-missing |
|---|---:|---:|---:|
| altman_distress_zone_ciq_candidate | 4,102 | 1,820 | 0.4437 |
| altman_gray_zone_ciq_candidate | 4,102 | 374 | 0.0912 |
| altman_safe_zone_ciq_candidate | 4,102 | 1,908 | 0.4651 |
| distress_event_12m_ciq | 21,737 | 4,029 | 0.1854 |
| distress_event_24m_ciq | 21,737 | 5,341 | 0.2457 |

## Timing and Leakage Checks

- Forecast-date rows after as-of date: 58
- Rows with 12-month event window observable through 2024: 19,411
- Rows with 24-month event window observable through 2024: 17,095
- Event labels are generated only from post-fiscal-year-end Key Developments dates and are kept as outcome candidates, not predictors.
- Market capitalization uses explicit historical date parameters, not `Current` market cap.

## Remaining Reviewer Risks

- `SNL_TOTAL_LIAB` remains a candidate total-liabilities field family and should be disclosed/reconciled before a strict Altman claim.
- Altman formulas are candidate labels until unit consistency, industry exclusions, REIT/fund/financial-firm rules, and winsorization are frozen.
- Event labels rely on keyword filtering of Key Developments text; distress versus non-distress delisting still needs manual or rule-based categorization before being used as a main outcome.
- FY2024 cannot support forward 12m/24m event labels from a 2010-2024 event export; FY2023 cannot support 24m labels.
- This audit does not yet apply final winsorization or exclusion rules.

## Next Gate

Proceed to sample-freeze and cleaning rules: exclude/flag ineligible industry structures, deduplicate company-years, set final missingness thresholds, apply winsorization, and then rerun descriptive statistics plus main/robustness models.
