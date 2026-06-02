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
| Unified cleaned v2 panel | 70-75% | A provisional Capital IQ v2 panel has now been built from the baseline firm-year panel plus supplemental raw workbooks, with 21,737 rows, 2,335 companies, FY2014-FY2024, and zero duplicate company-year rows. It is not yet sample-frozen. |
| Sample freeze and exclusion audit | 35-45% | The 2,335-company model panel and broad 3,005-company status universe are available, but final inclusion/exclusion rules for financial firms, REITs, funds, former/inactive firms, duplicates, low-quality text, and event windows are not frozen. |
| Label construction readiness | 60-70% | Altman and event-label candidates now exist in the v2 panel, but Altman availability is constrained by total-liabilities coverage and event labels currently rely on conservative name matching rather than direct Entity ID matching. |
| Overall data readiness for final model rerun | 70-75% | The v2 merge exists and passed basic structural checks, but final missingness rules, sample exclusions, winsorization, event-ID reconciliation, and leakage/timing decisions still need to be frozen before final model reruns. |
| Full paper-to-submission readiness | 35-40% | Model reruns, result judgment, manuscript rewrite, tables, target-journal packaging, and final submission QA remain incomplete. |

## Evidence Inspected

- `data/raw/capital_iq/` currently contains 48 local `.xlsx` raw Capital IQ workbooks.
- `data/processed/` currently contains 9 `.csv` processed files.
- Existing baseline panel: `data/processed/ael_apac_firm_year_panel.csv`, 21,737 firm-years and 2,335 unique companies over FY2014-FY2024.
- Existing processed market/Altman supplements:
  - `data/processed/capital_iq_asx_altman_market_supplement_20260602.csv`
  - `data/processed/capital_iq_catalist_altman_market_pilot_20260602.csv`
- Provisional v2 panel: `data/processed/ael_apac_firm_year_panel_v2_capital_iq_20260603.csv`.
- Provisional v2 audit: `outputs/ael_apac_firm_year_panel_v2_capital_iq_audit_20260603.md`.
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

## 2026-06-03 v2 Panel Update

The first unified v2 panel has now been generated and audited.

Key structural results:

- Rows: 21,737.
- Unique companies: 2,335.
- Fiscal years: 2014-2024.
- Duplicate company-year rows: 0.
- Altman candidate rows with all required components: 4,102.
- Altman distress-zone candidate positives: 1,820.
- Broad distress-event 12m candidate positives: 4,029.
- Broad distress-event 24m candidate positives: 5,341.
- Forecast-date rows after as-of date: 58.

Binding caveats:

- The event workbook's direct `SPCIQ ID` does not overlap with baseline `company_id`; event labels currently use conservative normalized-name matching and must be treated as candidate labels.
- Total liabilities coverage is still the binding Altman bottleneck, especially for Singapore rows.
- The v2 panel has not yet applied final sample exclusions, winsorization, or journal-facing label selection.

## Binding Next Step

Do not continue blind downloading before reviewing the v2 diagnostics. The next highest-value step is sample freeze and unified cleaning based on the v2 panel:

1. sample-freeze table;
2. field/year/market missingness audit;
3. duplicate company-year audit;
4. historical-market-cap date audit;
5. analyst timing/leakage audit;
6. Altman/strict/persistent/event label construction audit;
7. Go/No-Go decision for using Altman as main label versus robustness-only label.

Specific next decisions:

- whether to keep Altman as a main label given only 4,102 full-component candidate rows;
- whether to treat Key Developments as broad going-concern/delisting event evidence rather than strict bankruptcy/default evidence;
- whether to re-download Key Developments with baseline-compatible Entity ID before using event labels in a reviewer-facing main model;
- whether to exclude FY2024 from forward-event labels and FY2023 from 24-month labels;
- whether the 58 analyst timing violations are dropped, repaired, or used only after leakage-safe correction.
