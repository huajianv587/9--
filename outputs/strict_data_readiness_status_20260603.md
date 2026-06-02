# Strict Data Readiness Status

Date: 2026-06-03
Project: Analyst Coverage and Accounting-Based Financial Stress

## Reviewer-Level Decision

If "all required data" means local raw downloads plus base field audits, the Capital IQ supplemental raw layer is complete.

If "all required data" means an auditable dataset that can directly support sample freezing, unified cleaning, final labels, regressions, robustness tests, and a defensible SSCI/JCR Q3 manuscript, the project is not complete yet.

Current strict estimate:

| Scope | Readiness | Reason |
|---|---:|---|
| Raw Capital IQ supplemental downloads | 100% | The current raw completion audit lists all required Altman/liquidity/market-cap, liabilities, retained-earnings, event/status, and broad status-universe workbooks as downloaded and base-audited. |
| Raw workbook base audit layer | 100% | Each required supplemental workbook has a base audit and field/event audit, but most decisions remain `PASS_WITH_NOTES`, not clean unconditional pass. |
| Download checklist at reviewer-data-package level | 80-85% | The critical raw blocks are present, but the checklist still requires missing-ID reconciliation, duplicate handling, leakage checks, and market/current-universe boundary decisions after merge. |
| Unified cleaned v2 panel | 35-45% | Baseline processed panels exist and two supplemental pilot/partial CSVs exist, but the new Capital IQ raw workbooks have not yet been merged into one audited v2 panel. |
| Sample freeze and exclusion audit | 25-35% | The 2,335-company model panel and broad 3,005-company status universe are available, but final inclusion/exclusion rules for financial firms, REITs, funds, former/inactive firms, duplicates, low-quality text, and event windows are not frozen. |
| Label construction readiness | 45-55% | Raw inputs for Altman-style and event labels are available, but final Altman/strict/persistent/event labels have not been constructed and audited for missingness, leakage, and event rates. |
| Overall data readiness for final model rerun | 60-65% | Raw acquisition is done, but the binding work is now unified cleaning, fiscal-year joins, label construction, missingness rules, and leakage/timing audit. |
| Full paper-to-submission readiness | 30-35% | Model reruns, result judgment, manuscript rewrite, tables, target-journal packaging, and final submission QA remain incomplete. |

## Evidence Inspected

- `data/raw/capital_iq/` currently contains 48 local `.xlsx` raw Capital IQ workbooks.
- `data/processed/` currently contains 9 `.csv` processed files.
- Existing baseline panel: `data/processed/ael_apac_firm_year_panel.csv`, 21,737 firm-years and 2,335 unique companies over FY2014-FY2024.
- Existing processed market/Altman supplements:
  - `data/processed/capital_iq_asx_altman_market_supplement_20260602.csv`
  - `data/processed/capital_iq_catalist_altman_market_pilot_20260602.csv`
- Current raw completion audit: `outputs/capital_iq_raw_data_completion_audit_20260603.md`.

## Why This Is Not Yet 100% Data Readiness

The raw-data layer is complete, but a Q3 reviewer will not evaluate raw downloads. They will evaluate the final empirical panel and whether the paper can defend:

1. which company-years enter the sample;
2. which observations are excluded and why;
3. whether market cap is historical and date-labelled;
4. whether analyst variables are observable before the outcome window;
5. whether Altman/event labels are outcome variables, not leaked predictors;
6. whether missingness is quantified by field, year, market, and status;
7. whether inactive/delisted/former-listed companies are handled transparently.

Those checks require a unified v2 cleaning/merge pipeline. They cannot be proven by raw-workbook inventory alone.

## Binding Next Step

Do not continue blind downloading before merge diagnostics. The next highest-value step is to build one unified v2 panel from the baseline firm-year panel plus the audited Capital IQ supplements, then generate:

1. sample-freeze table;
2. field/year/market missingness audit;
3. duplicate company-year audit;
4. historical-market-cap date audit;
5. analyst timing/leakage audit;
6. Altman/strict/persistent/event label construction audit;
7. Go/No-Go decision for using Altman as main label versus robustness-only label.

