# Capital IQ Identifier/Status Schema Audit

Date: 2026-06-03T00:42:40
Workbook: `data/raw/capital_iq/capital_iq_asx_identifier_status_ipo_schema_proof_20260602.xlsx`

## Universe

- Data rows with Entity ID: 1696
- Unique Entity IDs: 1696
- Duplicate Entity-ID rows: 0
- Exchange counts: {'ASX': 1696}
- Company-type counts: {'Public Company': 1696}

## Identifier And Status Keys

- Required identifier keys detected: ['SP_COMPANY_TYPE', 'SP_ENTITY_ID', 'SP_ENTITY_NAME', 'SP_EXCHANGE']
- Missing required identifier keys: []
- Company-status coverage: {'SP_COMPANY_STATUS': {'column_number': 104, 'nonmissing': 1696, 'top_values': [('Operating', 1641), ('Operating Subsidiary', 54), ('Acquired', 1)]}}
- IPO-date coverage: {'SP_IPO_DATE': {'column_number': 105, 'nonmissing': 1078, 'top_values': [('2007-10-19 00:00:00', 4), ('2021-10-18 00:00:00', 3), ('2007-12-18 00:00:00', 3), ('2019-12-09 00:00:00', 3), ('2021-09-28 00:00:00', 3), ('2021-06-25 00:00:00', 3), ('2020-12-17 00:00:00', 3), ('2022-01-25 00:00:00', 3), ('2021-07-05 00:00:00', 3), ('2022-01-20 00:00:00', 3), ('2024-11-21 00:00:00', 3), ('2020-12-16 00:00:00', 3), ('2020-12-03 00:00:00', 3), ('2022-04-06 00:00:00', 3), ('2007-12-07 00:00:00', 3), ('2007-06-01 00:00:00', 3), ('2007-12-19 00:00:00', 3), ('2021-11-15 00:00:00', 3), ('2010-12-09 00:00:00', 3), ('2021-07-02 00:00:00', 2)]}}
- Geography coverage: None

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
| 104 | `Company Status` | `SP_COMPANY_STATUS` |
| 105 | `IPO Date
MM/dd/yyyy` | `SP_IPO_DATE` |

## Audit Decision

Status: PASS_WITH_NOTES
- Company identifier/status schema is present and auditable.
- Direct status/date/reason fields not found for: ['status_date', 'delisting_date', 'delisting_reason', 'bankruptcy_date', 'liquidation_date', 'suspension_date']. Use audited Key Developments raw events for dated distress/delisting evidence.
