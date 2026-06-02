# Capital IQ Key Developments Event Workbook Audit

Date: 2026-06-02T22:41:19
Workbook: `/Users/guohuiwen/华健 论文/9- 金融/data/raw/capital_iq/capital_iq_key_developments_distress_events_aus_sg_2010_2024_20260602.xlsx`
Size bytes: 10,136,943
Modified: 2026-06-02T22:38:33
SHA-256: `8b2b560221947c7a39578ec1a1110b60d6a9afab27c0c57dbfd22af6ddb57545`
Target date window: 2010-01-01 to 2024-12-31

## Workbook Summary

Skipped metadata sheets: `Screening Criteria`

| Sheet | Rows | Columns | Header row | ID column | Unique IDs | Model overlap | Date column | Parsed dates | In-range dates | Distress-keyword rows |
|---|---:|---:|---:|---|---:|---:|---|---:|---:|---:|
| Sheet1 | 44682 | 9 | 3 | SPCIQ ID | 6620 | 1 | Key Development Date
MM/dd/yyyy | 44682 | 44679 | 14105 |

## Sheet: Sheet1

- Date range parsed: 2010-01-01 to 2025-01-01
- Out-of-range parsed dates: 3
- Extra export IDs outside model panel: 6619
- Missing model IDs relative to current panel: 2334

### Detected columns

- Date columns: ['Key Development Date\nMM/dd/yyyy']
- Type columns: ['Key Development Type & Category', 'Key Development Type & Category.1']
- Category columns: ['Key Development Type & Category', 'Key Development Type & Category.1']
- Text columns: ['Key Development Headline', 'Key Development Description']

### Top event labels

| Label | Count |
|---|---:|
| Auditor Going Concern Doubt | 36356 |
| End of Lock-up Period | 21168 |
| Index Constituent: Add | 18384 |
| Index Constituent: Drop | 18272 |
| Initial Public Offering | 15160 |
| Delisting | 12960 |
| Auditor Change | 7576 |
| Lawsuits & Legal Issues | 7092 |
| Credit Rating: S&P: Credit Watch or Outlook Action | 6772 |
| Announcement of Earnings,Impairments or Write Offs | 6140 |
| Discontinued Operations or Downsizing | 3984 |
| Credit Rating: S&P: Downgrade | 2616 |
| Halt or Resumption of Operations, Unusual Events | 2388 |
| Credit Rating: S&P: Not-Rated Action | 2324 |
| Delayed SEC Filing | 1820 |
| Ticker Change | 1520 |
| Regulatory Authority: Compliance | 1512 |
| Activist Communication | 1492 |
| Impairments or Write Offs | 1120 |
| Bankruptcy: Asset Sale or Liquidation | 1092 |
| Labor-related Announcement | 1052 |
| Bankruptcy: Other | 988 |
| Business Reorganization | 916 |
| Announcement of Earnings,Corporate Guidance: New or Confirmed,Impairments or Write Offs | 612 |
| Regulatory Authority: Enforcement Action | 428 |

### Sheet decision notes

- NOTE: Some parsed dates fall outside the target 2010-2024 window; review before merge.

## Audit Decision

Status: PASS_WITH_NOTES
- Event workbook has company IDs, date fields, event descriptors, and parseable dates.
- Treat this as raw event evidence only; outcome-label construction still needs a separate cleaning script.
