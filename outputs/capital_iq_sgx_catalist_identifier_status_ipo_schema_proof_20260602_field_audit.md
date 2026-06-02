# Capital IQ Identifier/Status Schema Audit

Date: 2026-06-03T00:42:39
Workbook: `data/raw/capital_iq/capital_iq_sgx_catalist_identifier_status_ipo_schema_proof_20260602.xlsx`

## Universe

- Data rows with Entity ID: 544
- Unique Entity IDs: 544
- Duplicate Entity-ID rows: 0
- Exchange counts: {'SGX': 354, 'Catalist': 190}
- Company-type counts: {'Public Company': 544}

## Identifier And Status Keys

- Required identifier keys detected: ['SP_COMPANY_TYPE', 'SP_ENTITY_ID', 'SP_ENTITY_NAME', 'SP_EXCHANGE']
- Missing required identifier keys: []
- Company-status coverage: {'SP_COMPANY_STATUS': {'column_number': 104, 'nonmissing': 544, 'top_values': [('Operating', 408), ('Operating Subsidiary', 136)]}}
- IPO-date coverage: {'SP_IPO_DATE': {'column_number': 105, 'nonmissing': 280, 'top_values': [('2007-04-17 00:00:00', 2), ('2007-03-26 00:00:00', 2), ('2014-07-18 00:00:00', 2), ('2014-06-27 00:00:00', 2), ('2014-12-08 00:00:00', 2), ('2014-12-10 00:00:00', 2), ('2015-11-25 00:00:00', 2), ('2005-02-01 00:00:00', 1), ('2016-04-15 00:00:00', 1), ('2019-05-09 00:00:00', 1), ('2004-09-22 00:00:00', 1), ('2016-07-08 00:00:00', 1), ('2020-12-11 00:00:00', 1), ('2019-05-30 00:00:00', 1), ('2010-11-24 00:00:00', 1), ('2010-07-01 00:00:00', 1), ('2013-06-05 00:00:00', 1), ('2012-10-24 00:00:00', 1), ('2006-03-31 00:00:00', 1), ('2010-10-22 00:00:00', 1)]}}
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
