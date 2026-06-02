# Capital IQ Supplemental Workbook Audit

Date: 2026-06-02T22:38:47
Workbook: `/Users/guohuiwen/华健 论文/9- 金融/data/raw/capital_iq/capital_iq_key_developments_distress_events_aus_sg_2010_2024_20260602.xlsx`
Size bytes: 10,136,943
Modified: 2026-06-02T22:38:33
SHA-256: `8b2b560221947c7a39578ec1a1110b60d6a9afab27c0c57dbfd22af6ddb57545`

## Workbook Summary

| Sheet | Rows | Columns | Header row | Data rows | ID column | Unique IDs | Model overlap | Missing model IDs | Extra IDs |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| Sheet1 | 44688 | 9 | 13 | 44675 |  |  |  |  |  |
| Screening Criteria | 7 | 4 |  |  |  |  |  |  |  |

## Sheet: Sheet1

### Date-like columns

- None detected

### Critical-like columns

- `Delisting`
- `The Board of Directors (Board) of Suntar Eco-City Limited announced that the Singapore Exchange Securities Trading Limited (Exchange) had notified the Company that it would be placed on the watch-list due to the MTP Entry Criteria (Watch-list) with effect from 5 June 2017. The Company must take active steps to meet the requirements of Listing Rule 1314(2) within 36 months from 5 June 2017, failing which the Exchange would delist the Company or suspend trading in the Company’s shares with a view to delisting the Company. Listing Rule 1314(2) states that the Company will be assessed by the Exchange for removal from the Watch-list if it records volume-weighted average price of at least SGD 0.20 and an average daily market capitalisation of SGD 40 million or more over the last 6 months.`
- `Delisting.1`

### First rows preview

| Row | First non-empty cells |
|---:|---|
| 1 |  |
| 2 |  |
| 3 | Key Development Date / MM/dd/yyyy; Key Development OID; Key Development Type & Category; Key Development Headline; Key Development Description; Company Name; Country / Region Name; Key Development Type & Category; SPCIQ ID |
| 4 | SPKD_ANNOUNCED_EVENT_DATE; SPKD_KEYDEVELOPMENT_ID; SPKD_TYPE_CATEGORY; SPKD_HEADLINE; SPKD_ABSTRACT; SPKD_COMPANY_NAME; SPKD_TYPE_CATEGORY |
| 5 |  |
| 6 |  |
| 7 | 2020-05-25 04:00:00; 29450193; Index Constituent: Drop; Stanmore Coal Limited(ASX:SMR) dropped from S&P/ASX All Ordinaries Index; Stanmore Coal Limited(ASX:SMR) dropped from S&P/ASX All Ordinaries Index; Stanmore Resources Limited; Australia [Stanmore Resources Limited]; Index Constituent: Drop; IQ81596125 [Stanmore Resources Limited] |
| 8 | 2023-09-18 04:00:00; 35532090; Index Constituent: Drop; Fenix Resources Limited(ASX:FEX) dropped from S&P Global BMI Index; Fenix Resources Limited(ASX:FEX) dropped from S&P Global BMI Index; Fenix Resources Limited; Australia [Fenix Resources Limited]; Index Constituent: Drop; IQ39144434 [Fenix Resources Limited] |

### Top non-missing columns

| Column | Non-missing |
|---|---:|
| `2017-06-05 04:00:00` | 44,675 |
| `10985315` | 44,675 |
| `Delisting` | 44,675 |
| `Suntar Eco-City Limited Announces Inclusion On The Watch-List Due To The Minimum Trading Price Entry Criteria With Effect From 5 June 2017` | 44,675 |
| `The Board of Directors (Board) of Suntar Eco-City Limited announced that the Singapore Exchange Securities Trading Limited (Exchange) had notified the Company that it would be placed on the watch-list due to the MTP Entry Criteria (Watch-list) with effect from 5 June 2017. The Company must take active steps to meet the requirements of Listing Rule 1314(2) within 36 months from 5 June 2017, failing which the Exchange would delist the Company or suspend trading in the Company’s shares with a view to delisting the Company. Listing Rule 1314(2) states that the Company will be assessed by the Exchange for removal from the Watch-list if it records volume-weighted average price of at least SGD 0.20 and an average daily market capitalisation of SGD 40 million or more over the last 6 months.` | 44,675 |
| `Suntar Eco-City Limited` | 44,675 |
| `Singapore [Suntar Eco-City Limited]` | 44,675 |
| `Delisting.1` | 44,675 |
| `IQ35415174 [Suntar Eco-City Limited]` | 44,675 |

## Sheet: Screening Criteria

### Date-like columns

- None detected

### Critical-like columns

- None detected

### First rows preview

| Row | First non-empty cells |
|---:|---|
| 1 |  |
| 2 |  |
| 3 | Key Developments: New Screen |
| 4 | Screening Criteria: |
| 5 | 1                 Key Development Date (mm/dd/yyyy) Between 01/01/2010 - 12/31/2024 |
| 6 | 2    And     Country / Region Name In [Australia;Singapore] |
| 7 | 3    And     Key Development Type & Category [01/01/2010-12/31/2024] In Bankruptcy Updates;Listing or Trading;Potential Red Flags or Distress Indicators |

### Top non-missing columns

| Column | Non-missing |
|---|---:|

## Merge Decision Checklist

- Do not merge if market-cap/date fields are current or undated.
- Do not merge if the workbook only covers a current operating-company universe.
- Do not merge if critical fiscal-year labels are missing or inconsistent.
- Do not merge if model-ID overlap is materially below the expected research universe without a targeted reconciliation plan.
- Use this report as intake evidence only; model-panel changes require a separate merge script and leakage audit.
