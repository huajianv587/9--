# Strict Accounting Stress v2 DOCX Structural QA

Date: 2026-06-03

## Decision

Status: STRUCTURAL_AND_DIRECT_RENDER_QA_PASS

The DOCX manuscript was generated, passed structural checks, and passed direct visual render QA using the system LibreOffice application. The bundled `render_docx.py` path still fails in this local environment because its headless LibreOffice runtime cannot find `liblcms2.2.dylib`; that is now recorded as an environment-specific tooling issue rather than a manuscript-blocking issue.

## DOCX Artifact

- `manuscript/strict_accounting_stress_v2_submission_manuscript.docx`
- Size: approximately 46 KB.

## Bundled Render Attempt

Command attempted:

`render_docx.py manuscript/strict_accounting_stress_v2_submission_manuscript.docx --output_dir outputs/rendered/strict_accounting_stress_v2_docx --emit_pdf`

Failure:

- `dyld: Library not loaded: /opt/homebrew/opt/little-cms2/lib/liblcms2.2.dylib`
- Both direct DOCX-to-PDF and DOCX-to-ODT fallback failed.

## Direct Render QA Passed

System LibreOffice was available and rendered the DOCX successfully:

`/Applications/LibreOffice.app/Contents/MacOS/soffice --version`

Observed version:

- LibreOffice 26.2.3.2.

Direct conversion command:

`/Applications/LibreOffice.app/Contents/MacOS/soffice -env:UserInstallation=file:///tmp/lo_profile_strict_v2 --headless --norestore --convert-to pdf --outdir outputs/rendered/strict_accounting_stress_v2_docx_direct manuscript/strict_accounting_stress_v2_submission_manuscript.docx`

PDF render command:

`pdftoppm -png -r 130 outputs/rendered/strict_accounting_stress_v2_docx_direct/strict_accounting_stress_v2_submission_manuscript.pdf outputs/rendered/strict_accounting_stress_v2_docx_direct/page`

Rendered output:

- PDF: `outputs/rendered/strict_accounting_stress_v2_docx_direct/strict_accounting_stress_v2_submission_manuscript.pdf`.
- PNG pages: 11.
- Pages 1-6: portrait text pages.
- Pages 7-11: landscape table pages.

Visual QA inspected:

- Contact sheet of all 11 rendered pages.
- Page 1: title, abstract, keywords, JEL codes, and introduction start.
- Page 5: limitations, conclusion, data availability, and references start.
- Page 7: Table 1.
- Page 8: Table 2.
- Page 9: Table 3.
- Page 10: Table 4.
- Page 11: Table 5.

Visual QA result:

- No blank pages observed.
- No title, paragraph, or table clipping observed.
- Landscape table section renders correctly.
- Table text is readable.
- Table pages have conservative whitespace but no submission-blocking layout defect.

## Structural Checks Passed

- DOCX archive integrity: no compressed-data errors.
- Paragraphs: 70.
- Tables: 5.
- Sections: 2.
- Section 1: portrait.
- Section 2: landscape.
- First paragraph is the v2 strict-route title.
- Main odds ratio `0.711` is present.
- Old broad-stress sample size `19,402` is absent.
- Table 1: 7 rows, 8 columns.
- Table 2: 12 rows, 7 columns.
- Table 3: 5 rows, 9 columns.
- Table 4: 9 rows, 7 columns.
- Table 5: 2 rows, 7 columns.

## Remaining Gate

Before journal upload, rerender the exact final DOCX/PDF after journal-specific formatting, author metadata, acknowledgements, and blinded/non-blinded requirements are locked. The current DOCX is visually verified as a draft submission manuscript, not as a portal-submitted final file.
