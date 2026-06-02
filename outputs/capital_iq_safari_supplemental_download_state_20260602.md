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
