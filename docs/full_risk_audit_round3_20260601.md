# Full Risk Audit Round 3

Date: 2026-06-01

Scope: third strict re-check after the user confirmed that acceptance-probability language must not appear in the manuscript or final upload package.

## New Issues Found And Fixed

1. Stale APJFS preview PNGs.
   The APJFS DOCX/PDF had been regenerated with correct 3 cm margins and top-right page numbers, but `submission_package/apjfs_20260601/rendered_preview/` still contained older PNG previews. This was fixed by syncing all 18 main-manuscript page PNGs and the 1 title-page PNG from the latest rendered output. `scripts/check_apjfs_submission_package.py` now fails if package preview PDFs/PNGs are stale relative to the latest rendered outputs.

2. Working package vs final-upload package risk.
   The internal APJFS working package intentionally contains journal screens, audits, route notes, and 70-80 risk-control language. That package should not be uploaded wholesale to a journal portal. A new clean APJFS portal-upload zip was created:
   `submission_package/apjfs_20260601_portal_upload_clean.zip`.

3. Clean upload package guard added.
   `scripts/check_apjfs_portal_upload_clean_package.py` validates that the clean upload zip contains only five public-facing files and no internal route/probability language.

4. Data timing audit dependency fixed.
   `src/audit_analyst_snapshot_timing.py` no longer depends on optional `tabulate`; it now writes its markdown table through a local formatter. The timing audit runs successfully again.

5. Master check widened.
   `scripts/check_submission_ladder_master.py` now includes the clean APJFS portal-upload package and its checker.

## Verification Commands Passed

- `scripts/check_submission_ladder_master.py`: PASS.
- `scripts/check_apjfs_submission_package.py`: PASS.
- `scripts/check_apjfs_portal_upload_clean_package.py`: PASS.
- `data_quality_check.py`: YELLOW, adequate for conservative coverage framing; expand only if cheap.
- `src/audit_analyst_snapshot_timing.py`: PASS/run completed and report regenerated.
- `src/audit_capital_iq_market_field_leakage.py`: PASS/run completed and report regenerated.

## Clean Upload Package Contents

`submission_package/apjfs_20260601_portal_upload_clean.zip` contains exactly:

- `Manuscript_APJFS_double_blind.docx`
- `Title_page_and_declarations.docx`
- `Cover_letter.txt`
- `Data_and_code_availability_statement.txt`
- `Portal_metadata_for_copy_paste.txt`

It does not contain journal-screen files, readiness audits, transfer-ladder notes, 70-80 language, acceptance-probability language, raw data, firm-level panels, rendered QA images, or internal checklists.

## Current Hashes

| package | sha256 |
| --- | --- |
| `submission_package/apjfs_20260601_portal_upload_clean.zip` | `beccebc7ddceeb5c1bd4b8819d11c269ceac1fe49b8a4bb0a3dc58ada7bf73ee` |
| `submission_package/apjfs_20260601_submission_package.zip` | `5b221f3ce80f46dee371251b0c5aaa3060f32eb53e8200096d4381c6b51857f9` |
| `submission_package/economic_record_20260601_transfer_package.zip` | `7c119c1576835273b67b397a2e09f60342f467a6edc9366ef39e0239ceb1b113` |
| `submission_package/applied_economics_20260601_transfer_package.zip` | `c1c16ed6f581a429b1f434eebafa3aba79cb65536745bc956b93c66950e02714` |
| `submission_package/ael_20260601_submission_package.zip` | `49ce32cde0d3834136483c6475cb58b33f6f3376625c9355910971b0eaa1a7b4` |

## Data And Claim Boundary Check

- Panel rows: 21,737.
- Unique firms: 2,335.
- Duplicate company-year rows: 0.
- Modelled next-year-stress rows: 19,402.
- Stress events: 12,303.
- Analyst-covered model rows: 5,271.
- Modelled analyst coverage rate: 27.17%.
- FY2024 model rows: 0.
- Analyst snapshot timing checks pass: all modelled rows have fiscal-year-end as-of dates, source filename years match fiscal years, and covered forecast calendar dates are not after as-of dates.
- Market-cap fields remain excluded because available fields are current/no-date, transaction-context, or incomplete proof-of-schema exports.

The manuscript claim boundary remains conservative. Hits for causal/comprehensive/predictive language are in negative or limiting sentences, not positive overclaims.

## Remaining Risks

1. Use only the clean APJFS portal-upload zip for actual APJFS portal upload.
   The broader APJFS working package is for internal QA and should not be submitted wholesale.

2. Transfer packages remain working packages, not final clean upload packages.
   If APJFS is rejected and Economic Record, Applied Economics, or AEL becomes active, create a corresponding clean portal-upload package before submission.

3. The exact single-journal 70-80 target remains unverified.
   Do not state it in the manuscript, cover letter, portal fields, response letters, or final upload materials.

4. Data license remains a hard gate.
   Do not upload raw S&P Capital IQ exports or firm-level Capital IQ-derived panels.

5. Scientific framing must remain associational.
   Do not claim causality, comprehensive APAC evidence, or a large prediction-performance contribution.

## Decision

The current APJFS path is safer after this round because there is now a clean upload bundle that excludes internal probability and route language. The correct upload artifact is:

`submission_package/apjfs_20260601_portal_upload_clean.zip`

The internal working package remains useful for auditability but is not a journal-facing deliverable.
