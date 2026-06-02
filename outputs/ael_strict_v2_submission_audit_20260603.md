# Applied Economics Letters Strict v2 Submission Audit

Date: 2026-06-03

## Decision

Status: AEL_STRICT_V2_DRAFT_PACKAGE_RENDER_QA_PASS_NOT_FINAL_UPLOAD

The current Applied Economics Letters route has been rebuilt around the v2 strict-accounting-stress evidence. This supersedes the older 2026-06-01 AEL package that used the broad-stress `19,402 / 0.568` route.

## Current Artifacts

- Markdown draft: `manuscript/ael_strict_accounting_stress_v2_letter.md`.
- DOCX draft: `manuscript/ael_strict_accounting_stress_v2_submission.docx`.
- DOCX builder: `scripts/build_ael_strict_v2_submission_docx.py`.
- Package checker: `scripts/check_ael_strict_v2_package.py`.
- Rendered PDF: `outputs/rendered/ael_strict_v2/ael_strict_accounting_stress_v2_submission.pdf`.
- Rendered PNG pages: `outputs/rendered/ael_strict_v2/page-1.png` through `page-6.png`.

## Scope

This is an Applied Economics Letters short-article draft. It keeps three main tables:

1. Candidate samples.
2. Main and market-split logit estimates.
3. Robustness checks.

Descriptive statistics and prediction-increment evidence are not main tables in the AEL short route. Prediction increment is summarized in text to avoid overstating the contribution.

## Main Evidence

- Main strict accounting-stress sample: 19,322 firm-years.
- Strict-stress events: 7,874.
- Main analyst-coverage odds ratio: 0.711.
- Main average marginal effect: -7.2 percentage points.
- ASX odds ratio: 0.778.
- Singapore odds ratio: 0.492.
- Onset sample odds ratio: 0.856, p = 0.077.
- Altman robustness odds ratio: 0.710, p = 0.090.
- Event-candidate odds ratio: 0.472, retained as validation evidence because direct event-ID matching is not clean.
- Prediction increment: AUC changes from 0.7101 to 0.7100; no prediction-performance claim is made.

## Automated Checks

Command:

`/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_ael_strict_v2_package.py`

Result:

- `AEL strict v2 package checks passed.`

Checked conditions:

- Required markdown, DOCX, PDF, and 6 rendered PNG pages exist.
- Markdown word count is below the short-letter guardrail.
- DOCX archive integrity passes.
- DOCX has 3 tables and 2 sections.
- DOCX table shapes are 7x8, 5x9, and 9x7.
- Required strict-route markers are present: `19,322`, `7,874`, `0.711`, and `-7.2 percentage points`.
- Stale broad-route markers are absent: `19,402`, `0.568`, and old broad-stress wording.
- PDF has 6 pages and contains the strict-route table markers.

## Render QA

Direct render path:

`/Applications/LibreOffice.app/Contents/MacOS/soffice -env:UserInstallation=file:///tmp/lo_profile_ael_strict_v2 --headless --norestore --convert-to pdf --outdir outputs/rendered/ael_strict_v2 manuscript/ael_strict_accounting_stress_v2_submission.docx`

PNG render path:

`pdftoppm -png -r 130 outputs/rendered/ael_strict_v2/ael_strict_accounting_stress_v2_submission.pdf outputs/rendered/ael_strict_v2/page`

Visual inspection:

- Page 1: title, abstract, keywords, JEL codes, and introduction start are readable and not clipped.
- Page 3: conclusion, data availability, and references are readable and not clipped.
- Page 4: Table 1 is readable and not clipped.
- Page 5: Table 2 is readable and not clipped.
- Page 6: Table 3 is readable and not clipped.

Visual QA result:

- No blank pages observed.
- No paragraph or table clipping observed.
- Landscape table pages render correctly.
- Table pages have conservative whitespace but no submission-blocking layout defect.

## Remaining Non-Data Gates

This package is not final portal-ready until:

1. Applied Economics Letters is verified in live JCR/Web of Science immediately before submission.
2. Final author details, title page, declarations, and blinded/non-blinded requirements are locked.
3. Cover letter and portal fields are regenerated for the strict v2 route.
4. The exact final upload files are rerendered after author/declaration formatting.
5. The user confirms the Capital IQ data-availability wording is acceptable under the relevant institutional license.

## Reviewer-Risk Reading

This is now the strongest local JCR Q3 short-route package. It still cannot honestly be called a guaranteed 70-80% route because Applied Economics Letters publicly displays a 35% acceptance rate. The internal 70-80% target can only be treated as a polishing goal, not as an official journal probability.
