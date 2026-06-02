# Capital IQ Total Liabilities Candidate Audit

Date: 2026-06-02T23:59:43
Workbook: `data/raw/capital_iq/capital_iq_sgx_catalist_total_liabilities_candidate_snl_2014_2024_20260602.xlsx`

## Universe

- Data rows with Entity ID: 544
- Unique Entity IDs: 544
- Duplicate Entity-ID rows: 0
- Exchange counts: {'SGX': 354, 'Catalist': 190}
- Company-type counts: {'Public Company': 544}

## Field Source And Parameter Coverage

- Total-liabilities field keys detected: ['SNL_TOTAL_LIAB']
- Preferred CIQ total-liabilities key detected: False
- Target FY years present: [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
- Missing target FY years: []
- Leakage/current columns to exclude in cleaning: {'SNL_TOTAL_LIAB:Latest Fiscal Year': [5], 'SNL_TOTAL_LIAB:Latest Fiscal Quarter': [6], 'SNL_TOTAL_LIAB:Year-to-Date': [7], 'SNL_TOTAL_LIAB:Last Twelve Months': [8], 'SNL_TOTAL_LIAB:Latest Half-Year': [9], 'SNL_TOTAL_LIAB:FY2025': [10]}
- Out-of-window FY parameters to exclude in cleaning: ['FY1990', 'FY1991', 'FY1992', 'FY1993', 'FY1994', 'FY1995', 'FY1996', 'FY1997', 'FY1998', 'FY1999', 'FY2000', 'FY2001', 'FY2002', 'FY2003', 'FY2004', 'FY2005', 'FY2006', 'FY2007', 'FY2008', 'FY2009', 'FY2010', 'FY2011', 'FY2012', 'FY2013', 'FY2025']

## Target-Year Numeric Coverage

| Field key | Parameter | Columns | Duplicate count | Max non-missing | Max numeric | Numeric by column |
|---|---|---:|---:|---:|---:|---|
| `SNL_TOTAL_LIAB` | `FY2014` | [21] | 1 | 47 | 47 | [47] |
| `SNL_TOTAL_LIAB` | `FY2015` | [20] | 1 | 48 | 48 | [48] |
| `SNL_TOTAL_LIAB` | `FY2016` | [19] | 1 | 51 | 51 | [51] |
| `SNL_TOTAL_LIAB` | `FY2017` | [18] | 1 | 52 | 52 | [52] |
| `SNL_TOTAL_LIAB` | `FY2018` | [17] | 1 | 55 | 55 | [55] |
| `SNL_TOTAL_LIAB` | `FY2019` | [16] | 1 | 59 | 59 | [59] |
| `SNL_TOTAL_LIAB` | `FY2020` | [15] | 1 | 62 | 62 | [62] |
| `SNL_TOTAL_LIAB` | `FY2021` | [14] | 1 | 62 | 62 | [62] |
| `SNL_TOTAL_LIAB` | `FY2022` | [13] | 1 | 63 | 63 | [63] |
| `SNL_TOTAL_LIAB` | `FY2023` | [12] | 1 | 62 | 62 | [62] |
| `SNL_TOTAL_LIAB` | `FY2024` | [11] | 1 | 62 | 62 | [62] |

## Audit Decision

Status: PASS_WITH_NOTES
- Target-year total-liabilities columns are present and have auditable numeric coverage.
- `SNL_TOTAL_LIAB` is a usable raw candidate but not yet a preferred CIQ standard key; retain this warning until methodology reconciles the source-family choice.
- Latest/current/FY2025 columns are present and must be excluded before modeling.
- FY parameters outside 2014-2024 are present and must be excluded before modeling.
