# Capital IQ Raw Data Completion Audit

Date: 2026-06-03
Project: Analyst Coverage and Accounting-Based Financial Stress

## Decision

Status: RAW_DATA_DOWNLOAD_AUDIT_COMPLETE

Strict interpretation: the raw-data download and base audit layer is now complete for the current SSCI/JCR Q3 revision plan. This does not mean the paper is finished. It means the project now has an auditable raw-data base for unified cleaning, merge, label construction, model reruns, and manuscript rewriting.

## Completed Raw Workbooks

Raw Capital IQ workbooks are local-only and must not be pushed to GitHub.

| Data block | Local raw workbook | Base audit | Field audit | Decision |
|---|---|---|---|---|
| ASX Altman liquidity and historical market cap | `data/raw/capital_iq/capital_iq_asx_altman_liquidity_marketcap_2014_2024_full_20260602.xlsx` | `outputs/capital_iq_asx_altman_liquidity_marketcap_2014_2024_full_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_asx_altman_field_parameters_2014_2024_full_20260602.md` | PASS_WITH_NOTES |
| SGX Altman liquidity and historical market cap | `data/raw/capital_iq/capital_iq_sgx_altman_liquidity_marketcap_2014_2024_20260602.xlsx` | `outputs/capital_iq_sgx_altman_liquidity_marketcap_2014_2024_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_sgx_altman_field_parameters_2014_2024_20260602.md` | PASS_WITH_NOTES |
| Catalist Altman liquidity and historical market cap | `data/raw/capital_iq/capital_iq_catalist_altman_liquidity_marketcap_2014_2024_20260602.xlsx` | `outputs/capital_iq_catalist_altman_liquidity_marketcap_2014_2024_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_catalist_altman_field_parameters_2014_2024_20260602.md` | PASS_WITH_NOTES |
| ASX total liabilities candidate | `data/raw/capital_iq/capital_iq_asx_total_liabilities_candidate_snl_2014_2024_20260602.xlsx` | `outputs/capital_iq_asx_total_liabilities_candidate_snl_2014_2024_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_asx_total_liabilities_candidate_snl_2014_2024_20260602_field_audit.md` | PASS_WITH_NOTES |
| SGX/Catalist total liabilities candidate | `data/raw/capital_iq/capital_iq_sgx_catalist_total_liabilities_candidate_snl_2014_2024_20260602.xlsx` | `outputs/capital_iq_sgx_catalist_total_liabilities_candidate_snl_2014_2024_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_sgx_catalist_total_liabilities_candidate_snl_2014_2024_20260602_field_audit.md` | PASS_WITH_NOTES |
| ASX retained earnings | `data/raw/capital_iq/capital_iq_asx_retained_earnings_iq_2014_2024_20260602.xlsx` | `outputs/capital_iq_asx_retained_earnings_iq_2014_2024_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_asx_retained_earnings_iq_2014_2024_20260602_field_audit.md` | PASS_WITH_NOTES |
| SGX/Catalist retained earnings | `data/raw/capital_iq/capital_iq_sgx_catalist_retained_earnings_iq_2014_2024_20260602.xlsx` | `outputs/capital_iq_sgx_catalist_retained_earnings_iq_2014_2024_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_sgx_catalist_retained_earnings_iq_2014_2024_20260602_field_audit.md` | PASS_WITH_NOTES |
| Key Developments distress/status events | `data/raw/capital_iq/capital_iq_key_developments_distress_events_aus_sg_2010_2024_20260602.xlsx` | `outputs/capital_iq_key_developments_distress_events_aus_sg_2010_2024_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_key_developments_distress_events_aus_sg_2010_2024_20260602_event_workbook_audit.md` | PASS_WITH_NOTES |
| ASX identifier/status/IPO schema proof | `data/raw/capital_iq/capital_iq_asx_identifier_status_ipo_schema_proof_20260602.xlsx` | `outputs/capital_iq_asx_identifier_status_ipo_schema_proof_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_asx_identifier_status_ipo_schema_proof_20260602_field_audit.md` | PASS_WITH_NOTES |
| SGX/Catalist identifier/status/IPO schema proof | `data/raw/capital_iq/capital_iq_sgx_catalist_identifier_status_ipo_schema_proof_20260602.xlsx` | `outputs/capital_iq_sgx_catalist_identifier_status_ipo_schema_proof_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_sgx_catalist_identifier_status_ipo_schema_proof_20260602_field_audit.md` | PASS_WITH_NOTES |
| Australia/Singapore broader public-company status universe | `data/raw/capital_iq/capital_iq_aus_sg_public_company_broad_identifier_status_ipo_20260602.xlsx` | `outputs/capital_iq_aus_sg_public_company_broad_identifier_status_ipo_20260602_supplemental_workbook_audit.md` | `outputs/capital_iq_aus_sg_public_company_broad_identifier_status_ipo_20260602_field_audit.md` | PASS_WITH_NOTES |

## Reviewer-Relevant Findings

- The Altman raw-data gap that mattered most is now filled: current assets, current liabilities, historical fiscal-year-end market cap, total liabilities, and retained earnings all have auditable raw workbooks.
- `SNL_TOTAL_LIAB` is usable as a raw total-liabilities candidate, but it is not the preferred CIQ standard-key family. Keep this warning in method notes until cleaning reconciles source-family choice.
- `IQ_RETAINED_EARNINGS` is available for ASX and SGX/Catalist. SGX/Catalist retained earnings has duplicate selected columns, so cleaning must deduplicate by field key and fiscal year before merge.
- Direct company-master fields for `status_date`, `delisting_date`, `delisting_reason`, bankruptcy date, liquidation date, and suspension date were not detected in the screener field search. Dated distress/delisting evidence must come from the audited Key Developments event workbook.
- The broader Australia/Singapore public-company status universe has 3,005 unique IDs and includes non-operating statuses: Acquired, Out of Business, Liquidating, and Reorganizing. This is the raw boundary file for survivorship-bias discussion and former/inactive checks.

## Completion Percentage

Raw download plus base audit layer: 100%.

Downstream work still not complete:

- unified cleaning;
- source-family reconciliation;
- year/date mapping;
- duplicate-column removal;
- event-label construction;
- v2 panel merge;
- final model reruns;
- manuscript rewrite.

## Next Required Stage

Proceed to a single cleaning and merge pipeline. Do not hand-merge workbooks. The next stage must generate one audited v2 panel and one leakage/timing report before any manuscript claim is upgraded.
