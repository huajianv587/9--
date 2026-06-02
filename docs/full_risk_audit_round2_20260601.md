# Full Risk Audit Round 2

Date: 2026-06-01

Scope: strict re-check of the current APJFS-led SCIE/SSCI ladder package, non-Chrome data risks, package leakage, journal-claim boundaries, and residual reviewer risks.

Primary live source checked for APJFS formatting/fee rules: https://apjfs.org/homepage/custom/instruction

## Fresh Verification

- `scripts/check_submission_ladder_master.py`: PASS.
- `scripts/check_apjfs_submission_package.py`: PASS.
- `data_quality_check.py`: YELLOW, adequate for conservative analyst-coverage framing; expand only if cheap.
- Zip integrity: PASS for APJFS, Economic Record, Applied Economics, and AEL packages.
- Zip leakage: no hidden macOS files, no raw Excel/parquet/pickle/statistical-data files, no `data/raw` paths, and no literal `<br>` markers inside the submission zips.
- Double-blind files: APJFS, Economic Record, Applied Economics, and AEL blind manuscripts have no strict author-identity markers. Author identity appears only in expected cover-letter, title-page, portal-field, and author-template files.
- APJFS render QA: LibreOffice generated the PDF previews; Quick Look rendered 18 main-manuscript pages and 1 title-page preview for visual inspection. The table pages and title page were checked for clipping, overlap, page numbering, and margin issues.

## Corrections Made In This Round

1. APJFS formatting risk removed.
   The official APJFS instructions require double spacing, all margins at least 30 mm, and page numbering in the top right. The APJFS generator now uses exact 3 cm margins and adds a top-right PAGE field. The APJFS package check now fails if margins drop below 30 mm or the PAGE field disappears.

2. APJFS package regenerated.
   The APJFS DOCX files, PDF previews, rendered page images, and zip package were rebuilt after the margin/page-number correction.

3. AEL-first wording risk reduced.
   Old AEL-first operational wording was replaced with the current ladder framing: APJFS primary, Economic Record full-paper transfer, Applied Economics only if Q2-or-better is acceptable, and AEL only as a compressed fallback.

4. Affected zips rebuilt.
   APJFS, AEL, and Applied Economics packages were rebuilt after the edits.

## Current Package Hashes

| package | sha256 |
| --- | --- |
| `submission_package/apjfs_20260601_submission_package.zip` | `836e79b60acd6ddd870b24d76b6e01e0e10120674b326badee6f662d6726cddb` |
| `submission_package/economic_record_20260601_transfer_package.zip` | `cb2ef68fe24450e398655565f857650051fac2a862660dbb63a06d01e089437a` |
| `submission_package/applied_economics_20260601_transfer_package.zip` | `d95be2423f2e7489e75578cd120e5dd486483455d71c56a480e6e06baf4c1f83` |
| `submission_package/ael_20260601_submission_package.zip` | `49ce32cde0d3834136483c6475cb58b33f6f3376625c9355910971b0eaa1a7b4` |

## Remaining Hard Risks

1. No verified single-journal 70-80% route.
   The current package is regular-SCIE/SSCI-ladder ready, but no reputable scope-fitting SCIE/SSCI JCR Q3 finance/economics journal has been verified with credible current 70-80% single-journal acceptance evidence.

2. Data license remains a hard upload gate.
   Raw S&P Capital IQ exports and firm-level Capital IQ-derived panels must not be uploaded unless the institutional license explicitly permits it.

3. No simultaneous submission.
   Only one journal route can be active at a time. Transfer packages are for rejection/withdrawal sequences, not parallel submission.

4. Final index/quartile confirmation should be done at upload time.
   Public JCR/WoS screens and publisher pages can drift. Before pressing submit, the active target should be rechecked in the user's institutional JCR/Master Journal List access if available.

## Remaining Scientific Reviewer Risks

1. Analyst coverage depth is adequate but not strong.
   The modelled APAC sample has 5,271 analyst-covered rows out of 19,402 labelled rows. This supports conservative information-environment framing, not a claim of dense analyst coverage.

2. Stress-label construction is the main empirical attack point.
   The broad accounting-based financial-stress label is defensible only because the package includes current-stress controls, onset exclusion, conservative component controls, strict-label robustness, COVID exclusion, propensity checks, and firm/year fixed-effects checks.

3. Causality is unsafe.
   The manuscript should say analyst coverage is associated with lower future stress odds and is consistent with an information-environment interpretation. It should not claim analyst coverage reduces stress.

4. External validity is limited.
   The evidence is Singapore and Australia. Use "two Asia-Pacific markets" or "Singapore and Australia"; do not claim comprehensive APAC evidence.

5. Market-cap fields remain excluded.
   Existing market-cap fields are current/no-date, transaction-context, or incomplete proof-of-schema exports. They should not enter the predictive panel unless a full historical, date-labelled, non-missing export is obtained.

6. Prediction-performance claims must stay secondary.
   Analyst variables add robust association evidence, but the incremental AUC gain is small and random-forest results do not justify a strong prediction-system contribution.

## Decision

The package is now structurally cleaner than before this round: APJFS formatting has been tightened, page numbering is present, package zips pass, and old AEL-first route wording has been reduced. It is acceptable to proceed with APJFS only if the user accepts the project-level ladder interpretation and the conservative Capital IQ data-sharing boundary.

It is still not acceptable to state that this paper has a guaranteed or stable 70-80% single-journal acceptance probability.
