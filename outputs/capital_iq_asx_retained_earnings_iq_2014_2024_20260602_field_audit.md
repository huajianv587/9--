# Capital IQ Retained Earnings Candidate Audit

Date: 2026-06-03T00:19:17
Workbook: `data/raw/capital_iq/capital_iq_asx_retained_earnings_iq_2014_2024_20260602.xlsx`

## Universe

- Data rows with Entity ID: 1696
- Unique Entity IDs: 1696
- Duplicate Entity-ID rows: 0
- Exchange counts: {'ASX': 1696}
- Company-type counts: {'Public Company': 1696}

## Field Source And Parameter Coverage

- Retained-earnings field keys detected: ['IQ_RETAINED_EARNINGS']
- Preferred CIQ retained-earnings key detected: True
- Target FY years present: [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
- Missing target FY years: []
- Duplicate target-year retained-earnings parameters: None
- Leakage/current columns to exclude in cleaning: {'IQ_RETAINED_EARNINGS:Latest Fiscal Year': [46], 'IQ_RETAINED_EARNINGS:Latest Fiscal Quarter': [47], 'IQ_RETAINED_EARNINGS:Year-to-Date': [48], 'IQ_RETAINED_EARNINGS:Last Twelve Months': [49], 'IQ_RETAINED_EARNINGS:Latest Half-Year': [50], 'IQ_RETAINED_EARNINGS:FY2025': [51]}
- Out-of-window FY parameters to exclude in cleaning: ['FY1973', 'FY1974', 'FY1975', 'FY1976', 'FY1977', 'FY1978', 'FY1979', 'FY1980', 'FY1981', 'FY1982', 'FY1983', 'FY1984', 'FY1985', 'FY1986', 'FY1987', 'FY1988', 'FY1989', 'FY1990', 'FY1991', 'FY1992', 'FY1993', 'FY1994', 'FY1995', 'FY1996', 'FY1997', 'FY1998', 'FY1999', 'FY2000', 'FY2001', 'FY2002', 'FY2003', 'FY2004', 'FY2005', 'FY2006', 'FY2007', 'FY2008', 'FY2009', 'FY2010', 'FY2011', 'FY2012', 'FY2013', 'FY2025']

## Target-Year Numeric Coverage

| Field key | Parameter | Columns | Duplicate count | Max non-missing | Max numeric | Numeric by column |
|---|---|---:|---:|---:|---:|---|
| `IQ_RETAINED_EARNINGS` | `FY2014` | [62] | 1 | 1076 | 1076 | [1076] |
| `IQ_RETAINED_EARNINGS` | `FY2015` | [61] | 1 | 1130 | 1130 | [1130] |
| `IQ_RETAINED_EARNINGS` | `FY2016` | [60] | 1 | 1192 | 1192 | [1192] |
| `IQ_RETAINED_EARNINGS` | `FY2017` | [59] | 1 | 1270 | 1270 | [1270] |
| `IQ_RETAINED_EARNINGS` | `FY2018` | [58] | 1 | 1353 | 1353 | [1353] |
| `IQ_RETAINED_EARNINGS` | `FY2019` | [57] | 1 | 1426 | 1426 | [1426] |
| `IQ_RETAINED_EARNINGS` | `FY2020` | [56] | 1 | 1478 | 1478 | [1478] |
| `IQ_RETAINED_EARNINGS` | `FY2021` | [55] | 1 | 1571 | 1571 | [1571] |
| `IQ_RETAINED_EARNINGS` | `FY2022` | [54] | 1 | 1631 | 1631 | [1631] |
| `IQ_RETAINED_EARNINGS` | `FY2023` | [53] | 1 | 1665 | 1665 | [1665] |
| `IQ_RETAINED_EARNINGS` | `FY2024` | [52] | 1 | 1675 | 1675 | [1675] |

## Audit Decision

Status: PASS_WITH_NOTES
- Target-year retained-earnings columns are present and have auditable numeric coverage.
- Latest/current/FY2025 columns are present and must be excluded before modeling.
- FY parameters outside 2014-2024 are present and must be excluded before modeling.
