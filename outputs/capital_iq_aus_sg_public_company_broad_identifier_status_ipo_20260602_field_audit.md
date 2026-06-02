# Capital IQ Identifier/Status Schema Audit

Date: 2026-06-03T00:39:50
Workbook: `data/raw/capital_iq/capital_iq_aus_sg_public_company_broad_identifier_status_ipo_20260602.xlsx`

## Universe

- Data rows with Entity ID: 3005
- Unique Entity IDs: 3005
- Duplicate Entity-ID rows: 0
- Exchange counts: {'ASX': 2100, 'Catalist': 184, 'NYSEAM': 15, 'NASDAQGM': 18, 'OTCPK': 35, 'NASDAQCM': 74, 'SGX': 365, 'OTCEM': 16, 'TSXV': 11, 'SEHK': 56, 'NZSE': 6, 'LSE': 6, 'NYSE': 8, 'AIM': 13, 'NASDAQGS': 9, 'NSX': 22, 'OB': 4, 'PSGM': 3, 'CNSX': 4, 'JSE': 1, 'OTCBB': 2, 'TSX': 4, 'TASE': 1, 'OTCQB': 2, 'KLSE': 1, 'DB': 2, 'TSE': 2, 'TWSE': 1, 'KOSE': 1, 'OFEX': 2, 'ENXTAM': 1}
- Company-type counts: {'Public Company': 3005}

## Identifier And Status Keys

- Required identifier keys detected: ['SP_COMPANY_TYPE', 'SP_ENTITY_ID', 'SP_ENTITY_NAME', 'SP_EXCHANGE']
- Missing required identifier keys: []
- Company-status coverage: {'SP_COMPANY_STATUS': {'column_number': 103, 'nonmissing': 3005, 'top_values': [('Operating', 2168), ('Acquired', 600), ('Operating Subsidiary', 210), ('Out of Business', 22), ('Liquidating', 3), ('Reorganizing', 2)]}}
- IPO-date coverage: {'SP_IPO_DATE': {'column_number': 104, 'nonmissing': 1633, 'top_values': [('2007-10-19 00:00:00', 5), ('2010-12-09 00:00:00', 5), ('2007-12-18 00:00:00', 4), ('2015-12-09 00:00:00', 4), ('2020-12-17 00:00:00', 4), ('2007-12-10 00:00:00', 4), ('2021-10-18 00:00:00', 3), ('2020-12-11 00:00:00', 3), ('2019-12-09 00:00:00', 3), ('2019-09-30 00:00:00', 3), ('2021-09-28 00:00:00', 3), ('2024-12-12 00:00:00', 3), ('2021-06-25 00:00:00', 3), ('2021-12-03 00:00:00', 3), ('2011-06-24 00:00:00', 3), ('2022-01-25 00:00:00', 3), ('2007-04-24 00:00:00', 3), ('2021-07-05 00:00:00', 3), ('2006-05-02 00:00:00', 3), ('2007-10-01 00:00:00', 3)]}}
- Geography coverage: {'SP_GEOGRAPHY': {'column_number': 105, 'nonmissing': 3005, 'top_values': [('Asia-Pacific', 3005)]}}

## Direct Event/Boundary Field Search

- status_date: Not detected
- delisting_date: Not detected
- delisting_reason: Not detected
- bankruptcy_date: Not detected
- liquidation_date: Not detected
- suspension_date: Not detected

## Header Tail

| Column | Header | Key |
|---:|---|---|
| 103 | `Company Status` | `SP_COMPANY_STATUS` |
| 104 | `IPO Date
MM/dd/yyyy` | `SP_IPO_DATE` |
| 105 | `Geography` | `SP_GEOGRAPHY` |

## Audit Decision

Status: PASS_WITH_NOTES
- Company identifier/status schema is present and auditable.
- Direct status/date/reason fields not found for: ['status_date', 'delisting_date', 'delisting_reason', 'bankruptcy_date', 'liquidation_date', 'suspension_date']. Use audited Key Developments raw events for dated distress/delisting evidence.
