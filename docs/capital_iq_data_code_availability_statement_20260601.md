# Capital IQ Data and Code Availability Statement

Date: 2026-06-01
Use: AEL submission package and transfer-journal submissions

## Conservative Statement for Submission Portal

### Data Availability

The data used in this study were obtained from S&P Capital IQ under institutional database access and are subject to database licensing and redistribution restrictions. The author cannot redistribute the raw Capital IQ exports or firm-level Capital IQ-derived research panels. Researchers with their own S&P Capital IQ access may reconstruct the sample using the variable definitions, sample filters, and replication code. The non-proprietary aggregate tables reported in the article are included in the submission materials.

### Code Availability

Replication code for parsing licensed exports, constructing the firm-year panels, estimating the models, and producing the manuscript tables can be made available on reasonable request. The code release would exclude raw Capital IQ exports and firm-level Capital IQ-derived data. Reuse of the code requires users to obtain any necessary data access independently.

### Submission-Safe Clarification

The Chrome-controlled Capital IQ exports generated during pre-submission checks are audit and provenance materials only. They should not be uploaded to a journal portal, public repository, or supplementary file set. The manuscript-facing evidence remains the aggregate tables, the model-output tables, and the exchange-consistent robustness result. Any supplemental code should describe how licensed users can reconstruct the sample, but it must not include raw S&P Capital IQ workbooks or firm-level Capital IQ-derived values.

## If the Portal Requires a Data Repository

Use this response:

> The underlying firm-level data are licensed from S&P Capital IQ and cannot be redistributed through a public repository. The manuscript reports aggregate result tables, and replication code can be shared without the licensed raw data. Researchers with appropriate Capital IQ access can reconstruct the dataset using the documented variable definitions and scripts.

## Risk Boundary

- Do not upload raw Capital IQ exports.
- Do not upload the processed firm-year panel if it contains Capital IQ-derived company-level fields.
- Do not promise public access to raw, cleaned, or firm-level Capital IQ-derived data.
- It is acceptable to share article-level aggregate tables, model outputs, and scripts that do not contain proprietary observations.
- The final wording should still be checked against the applicable institutional S&P Capital IQ license before pressing final submit.

## Market-Data Boundary

The 2026-06-01 Capital IQ market-field audit found `SP_MARKETCAP` fields in existing exports. Safari/Capital IQ can display a `12/31/2023` market-cap as-of-date field, but the exported proof-of-schema file covers only three peer-comparison companies and returns `NA` market-cap values. Earlier raw exports also contain current/no-date market-cap fields or transaction-context target market-cap fields. None of these market-cap fields are used in the APJFS panel because they do not provide a non-missing, full-sample, historical predictor-date series for the 2014-2023 firm-year panel.

Safe rule: market capitalization, price, return, volume, or liquidity controls can be added only if exported with explicit historical fiscal-year, predictor-date, or as-of-date labels, non-missing values, and the same company universe needed for the stress outcome window.
