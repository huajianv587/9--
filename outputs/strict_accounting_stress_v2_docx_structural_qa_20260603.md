# Strict Accounting Stress v2 DOCX Structural QA

Date: 2026-06-03

## Decision

Status: STRUCTURAL_QA_PASS_RENDER_QA_BLOCKED

The DOCX manuscript was generated and passed structural checks, but the required visual render QA could not be completed because the local LibreOffice headless runtime is missing `liblcms2.2.dylib`.

## DOCX Artifact

- `manuscript/strict_accounting_stress_v2_submission_manuscript.docx`
- Size: approximately 46 KB.

## Render Attempt

Command attempted:

`render_docx.py manuscript/strict_accounting_stress_v2_submission_manuscript.docx --output_dir outputs/rendered/strict_accounting_stress_v2_docx --emit_pdf`

Failure:

- `dyld: Library not loaded: /opt/homebrew/opt/little-cms2/lib/liblcms2.2.dylib`
- Both direct DOCX-to-PDF and DOCX-to-ODT fallback failed.

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

Before upload, render QA must be rerun on a machine with a working LibreOffice/Word/PDF conversion path. This DOCX should be treated as a structurally valid draft, not as a visually verified final submission file.

