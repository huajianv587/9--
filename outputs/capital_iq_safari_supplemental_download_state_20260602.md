# Capital IQ Safari Supplemental Download State

Date: 2026-06-02

## Safari State Checked

- Safari is logged into S&P Capital IQ Pro.
- Current reachable page: Office Screener / Companies / New Screen.
- Manage My Screens showed only system screens, not a custom APAC model-panel screen.
- Companies screener can be opened from the Screener menu.

## Tested Path

1. Opened `Screener -> Manage My Screens`.
2. Entered `Companies` screener.
3. Opened `Add Companies`.
4. Result: the dialog supports company-name/ticker/LEI search, but is not suitable for pasting 2,335 Capital IQ company IDs.
5. Searched criteria for `Entity ID`.
6. Found `SPCIQ ID [Company Details] / [Company Identification]`.
7. Selected `SPCIQ ID -> Includes`.
8. Pilot-entered five IDs:
   - 4005723
   - 4021467
   - 4041225
   - 4045293
   - 4048862
9. Result: the input collapsed comma-separated IDs into one concatenated number, so this online field is not safe for multi-ID list filtering.
10. The pilot condition was cleared. No screen was run and no workbook was downloaded from this invalid condition.

## Decision

Do not use Safari online Screener `SPCIQ ID Includes` for the full 2,335-ID universe.

Use one of these instead:

1. Capital IQ Office/Excel plugin list import, if available;
2. saved list upload/import feature, if available elsewhere in Capital IQ;
3. exchange/status segmented screens with active + inactive/delisted coverage, followed by model-ID overlap audit;
4. targeted single-ID or small-batch exports only for missing-ID reconciliation.

## Local Files Prepared

- `outputs/capital_iq_model_company_ids_20260602.csv`
- `outputs/capital_iq_model_company_ids_20260602.txt`

These contain the 2,335 model-panel company IDs and can be used for an Office plugin/list-import workflow.

## Next Safe Action

Find a Capital IQ workflow that imports a list from file or creates a saved company list from the prepared ID file. If unavailable, build segmented Safari screens:

1. ASX active/current public operating;
2. ASX inactive/delisted/former listed;
3. SGX/Catalist active/current public operating;
4. SGX/Catalist inactive/delisted/former listed;
5. targeted missing-ID batches by ticker suffix or company ID.

Every downloaded workbook must be audited with:

```bash
python3 scripts/audit_capital_iq_supplemental_workbook.py /path/to/workbook.xlsx
```

## 2026-06-02 ASX Supplemental Download Progress

### Completed ASX Screen

- Capital IQ page: Office Screener / Companies.
- Criteria used:
  - Company Type: Public Company.
  - Exchange [Current]: ASX.
- Screener result count: 1,696 records.
- Model-panel overlap after workbook audit:
  - Unique Capital IQ Entity IDs in export: 1,696.
  - Overlap with model-panel IDs: 1,685.
  - Missing model-panel IDs after ASX-current screen: 650.
  - Extra export IDs outside model panel: 11.

### Local Raw Workbooks

Raw Capital IQ workbooks are local-only and intentionally ignored by git:

- `data/raw/capital_iq/capital_iq_asx_altman_liquidity_marketcap_test_20260602.xlsx`
- `data/raw/capital_iq/capital_iq_asx_altman_liquidity_marketcap_2020_2024_attempt_20260602.xlsx`
- `data/raw/capital_iq/capital_iq_asx_altman_liquidity_marketcap_2014_2024_attempt_20260602.xlsx`

Do not push these files to the public GitHub repository.

### Audited ASX Fields

Latest audited workbook:

- `data/raw/capital_iq/capital_iq_asx_altman_liquidity_marketcap_2014_2024_attempt_20260602.xlsx`
- Rows: 1,702 worksheet rows.
- Columns: 101.
- Data rows with Entity ID: 1,696.
- Generic audit report:
  - `outputs/audit_asx_altman_liquidity_marketcap_2014_2024_attempt_20260602.md`
- Field-parameter audit report:
  - `outputs/audit_asx_altman_field_parameters_2014_2024_20260602.md`

Usable numeric ASX coverage from the field-parameter audit:

| Field | Parameter/date | Usable numeric rows |
|---|---:|---:|
| Total Current Assets | FY2024 | 1,658 |
| Total Current Assets | FY2023 | 1,649 |
| Total Current Assets | FY2022 | 1,621 |
| Total Current Assets | FY2021 | 1,562 |
| Total Current Assets | FY2020 | 1,457 |
| Total Current Assets | FY2019 | 1,405 |
| Total Current Assets | FY2018 | 1,335 |
| Total Current Assets | FY2017 | 1,257 |
| Total Current Assets | FY2016 | 1,173 |
| Total Current Assets | FY2015 | 1,117 |
| Total Current Assets | FY2014 | 1,065 |
| Total Current Liabilities | FY2024 | 1,659 |
| Total Current Liabilities | FY2023 | 1,651 |
| Total Current Liabilities | FY2022 | 1,622 |
| Total Current Liabilities | FY2021 | 1,563 |
| Total Current Liabilities | FY2020 | 1,460 |
| Total Current Liabilities | FY2019 | 1,405 |
| Total Current Liabilities | FY2018 | 1,338 |
| Total Current Liabilities | FY2017 | 1,258 |
| Total Current Liabilities | FY2016 | 1,177 |
| Total Current Liabilities | FY2015 | 1,117 |
| Total Current Liabilities | FY2014 | 1,058 |
| Market Capitalization | 12/31/2024 | 1,645 |
| Market Capitalization | 12/29/2023 | 1,612 |
| Market Capitalization | 12/30/2022 | 1,577 |
| Market Capitalization | 12/31/2021 | 1,495 |
| Market Capitalization | 12/31/2020 | 1,316 |
| Market Capitalization | 12/31/2019 | 1,241 |
| Market Capitalization | 12/31/2018 | 1,206 |
| Market Capitalization | 12/29/2017 | 1,135 |
| Market Capitalization | 12/30/2016 | 1,057 |
| Market Capitalization | 12/31/2015 | 984 |

Important audit notes:

- `12/31/2023` and `12/31/2022` market-cap columns have zero numeric observations. They are invalid year-end dates for this export and must be replaced by `12/29/2023` and `12/30/2022`.
- `12/29/2017` appears twice; keep one column only during cleaning.
- `12/31/2015` appears twice; keep one column only during cleaning.
- `Current` market capitalization is present but must not be used as historical market value.
- `12/31/2014` market capitalization is still missing from the latest export and remains an ASX gap.

### Current Data-Preparation Percentage

If 100% means a reviewer-defensible SSCI/JCR Q3 empirical data package:

- Main panel: about 85-90%.
- Altman financial-field supplement: about 55-60%.
- Historical market-cap supplement: about 35-45%.
- Event/distress-date supplement: about 10-15%.
- Overall data-preparation status: about 55%.

The next highest-priority data work is:

1. Add ASX `12/31/2014` market capitalization or document an acceptable fallback.
2. Repeat the same current-assets/current-liabilities/historical-market-cap workflow for SGX/Catalist.
3. Download event/date fields from Key Developments, Transactions, company-status history, delisting/suspension, ratings, bankruptcy/liquidation/restructuring, or equivalent Capital IQ fields.
4. Build a merge script that excludes current market cap, de-duplicates duplicate date columns, maps valid historical dates to fiscal years, and audits leakage.

## 2026-06-02 ASX Cleaning Script Progress

Added a public-safe cleaning script:

- `scripts/build_asx_altman_market_supplement.py`

Local generated outputs are intentionally ignored by git:

- `data/processed/capital_iq_asx_altman_market_supplement_20260602.csv`
- `outputs/asx_altman_market_supplement_merge_audit_20260602.md`

Cleaning rules implemented:

- Output window is restricted to fiscal years 2014-2024.
- `Current` market capitalization is excluded.
- `12/31/2023` and `12/31/2022` market capitalization are excluded because they have zero numeric observations in the audited export.
- Valid replacements used:
  - 2023: `12/29/2023`.
  - 2022: `12/30/2022`.
  - 2017: `12/29/2017`.
  - 2016: `12/30/2016`.
- Duplicate `12/29/2017` and duplicate `12/31/2015` columns are reduced by retaining the first occurrence.
- Market cap remains in USD millions; current assets and current liabilities remain in USD thousands.

ASX panel merge coverage from the generated audit:

| Fiscal year | ASX panel rows | Current assets | Current liabilities | Historical market cap |
|---:|---:|---:|---:|---:|
| 2014 | 1,075 | 1,046 | 1,039 | 0 |
| 2015 | 1,130 | 1,097 | 1,097 | 967 |
| 2016 | 1,184 | 1,149 | 1,153 | 1,038 |
| 2017 | 1,261 | 1,229 | 1,230 | 1,115 |
| 2018 | 1,345 | 1,304 | 1,307 | 1,184 |
| 2019 | 1,417 | 1,373 | 1,373 | 1,216 |
| 2020 | 1,461 | 1,423 | 1,426 | 1,288 |
| 2021 | 1,552 | 1,526 | 1,527 | 1,458 |
| 2022 | 1,612 | 1,584 | 1,585 | 1,545 |
| 2023 | 1,636 | 1,609 | 1,611 | 1,577 |
| 2024 | 1,644 | 1,618 | 1,619 | 1,607 |

Remaining ASX gaps:

- `12/31/2014` historical market capitalization is absent, so 2014 X4-style market value cannot be computed from this export.
- Retained earnings is still missing.
- This script does not complete a strict Altman Z-score; it prepares working-capital and market-value pieces only.

## 2026-06-02 Catalist Identifier-Only Export

### Completed Catalist Screen

- Capital IQ page: Office Screener / Companies.
- Criteria used:
  - Exchange [Current]: Catalist.
- Screener result count: 190 records.
- Display columns at export time:
  - Entity Name.
  - Entity ID.
  - Exchange Current.

### Local Raw Workbook

Raw Capital IQ workbook is local-only and intentionally ignored by git:

- `data/raw/capital_iq/capital_iq_catalist_current_exchange_identifiers_20260602.xlsx`

Do not push this file to the public GitHub repository.

### Audit Result

Audit report generated locally and intentionally ignored by git:

- `outputs/capital_iq_catalist_current_exchange_identifiers_20260602_supplemental_workbook_audit.md`

Workbook audit summary:

- Worksheet rows: 196.
- Worksheet columns: 3.
- Data rows: 191.
- Unique Entity IDs: 190.
- Model-panel overlap: 162.
- Extra export IDs outside model panel: 28.
- Missing model-panel IDs after this identifier-only workbook: 2,173.
- Date-like columns: none detected.
- Critical-like financial/event columns: none detected.

### Merge Decision

This export is useful only as a Catalist current-listing universe and ID-overlap check. It must not be merged into the empirical model as Altman, market-cap, distress-event, or historical accounting data.

Current data-preparation percentage remains about 55%. The percentage does not materially improve until SGX/Catalist current-assets, current-liabilities, historical market capitalization, retained-earnings/proxy, and event/date fields are downloaded and audited.

## 2026-06-02 Catalist Altman/Market Pilot

### Completed Catalist Pilot Export

- Capital IQ page: Office Screener / Companies.
- Criteria used:
  - Exchange [Current]: Catalist.
- Screener result count: 190 records.
- Export includes:
  - Entity Name.
  - Entity ID.
  - Exchange Current.
  - `SP_CURRENT_ASSETS` Fiscal Year / All.
  - `SP_CURRENT_LIAB` Fiscal Year / All.
  - `SP_MARKETCAP` with explicit `12/31/2024` pricing date.

### Local Raw Workbook

Raw Capital IQ workbook is local-only and intentionally ignored by git:

- `data/raw/capital_iq/capital_iq_catalist_altman_liquidity_marketcap_pilot_20260602.xlsx`

Do not push this file to the public GitHub repository.

### Audit Result

Audit report generated locally and intentionally ignored by git:

- `outputs/capital_iq_catalist_altman_liquidity_marketcap_pilot_20260602_supplemental_workbook_audit.md`

Workbook audit summary:

- Worksheet rows: 196.
- Worksheet columns: 87.
- Unique Entity IDs: 190.
- Model-panel overlap: 162.
- Extra export IDs outside model panel: 28.
- Critical-like columns detected:
  - `Total Current Assets ($000)`.
  - `Total Current Liabilities ($000)`.
  - `Market Capitalization ($M)`.

Field-parameter check:

- `SP_CURRENT_ASSETS`: FY2014-FY2024 available, plus non-model latest/YTD/older-year columns that must be excluded during cleaning.
- `SP_CURRENT_LIAB`: FY2014-FY2024 available, plus non-model latest/YTD/older-year columns that must be excluded during cleaning.
- `SP_MARKETCAP`: `12/31/2024` only, duplicated twice; cleaning keeps the first duplicate.
- Market-cap years still missing for Catalist: 2014-2023.

### Cleaning Script Progress

Added a public-safe Catalist pilot cleaning script:

- `scripts/build_catalist_altman_market_pilot.py`

Local generated outputs are intentionally ignored by git:

- `data/processed/capital_iq_catalist_altman_market_pilot_20260602.csv`
- `outputs/catalist_altman_market_pilot_merge_audit_20260602.md`

Catalist pilot merge coverage against the Singapore panel:

| Fiscal year | Singapore panel rows | Current assets | Current liabilities | Historical market cap |
|---:|---:|---:|---:|---:|
| 2014 | 442 | 116 | 116 | 0 |
| 2015 | 467 | 126 | 126 | 0 |
| 2016 | 499 | 135 | 135 | 0 |
| 2017 | 513 | 137 | 137 | 0 |
| 2018 | 530 | 141 | 141 | 0 |
| 2019 | 546 | 145 | 145 | 0 |
| 2020 | 574 | 152 | 152 | 0 |
| 2021 | 594 | 156 | 156 | 0 |
| 2022 | 627 | 162 | 162 | 0 |
| 2023 | 640 | 162 | 162 | 0 |
| 2024 | 642 | 161 | 161 | 151 |

### Merge Decision

This pilot is valid as a Catalist current-listing sub-sample supplement for working-capital fields and 2024 market capitalization. It is not a complete Singapore supplement and must not be used as a claim that SGX/Catalist historical market data are complete.

Current data-preparation percentage moves only slightly, from about 55% to about 57%. The binding gaps remain: SGX mainboard coverage, Catalist historical market capitalization for 2014-2023, ASX 2014 market capitalization, retained earnings/proxy policy, total-liabilities supplement if strict Altman X4 is used, and event/distress-date fields.
