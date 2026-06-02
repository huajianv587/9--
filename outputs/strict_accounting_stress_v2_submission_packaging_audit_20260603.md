# Strict Accounting Stress v2 Submission Packaging Audit

Date: 2026-06-03T04:29:41

## Decision

Status: DRAFT_PACKAGE_BUILT_NOT_FINAL_SUBMISSION

The v2 manuscript package has been rebuilt around the strict accounting-stress route. It now has a visually checked DOCX draft via direct system-LibreOffice rendering, but it is not yet final submission-ready because journal selection must be refreshed and event-ID/tone limitations remain.

## Generated Artifacts

- Manuscript draft: `/Users/guohuiwen/华健 论文/9- 金融/manuscript/strict_accounting_stress_v2_manuscript.md`
- Cover letter draft: `/Users/guohuiwen/华健 论文/9- 金融/manuscript/strict_accounting_stress_v2_cover_letter.md`
- DOCX manuscript draft: `/Users/guohuiwen/华健 论文/9- 金融/manuscript/strict_accounting_stress_v2_submission_manuscript.docx`
- Table directory: `/Users/guohuiwen/华健 论文/9- 金融/outputs/manuscript_v2_strict`
- Approximate manuscript word count including tables/references: 3,140

## Main Evidence

- Main strict accounting stress odds ratio: 0.711
- Main AME: -0.072
- Main p-value: 2.8e-06

## Reviewer Risks Still Open

- This is not yet a no-risk 70-80% SSCI/JCR Q3 submission package.
- Journal fit and current JCR quartile/acceptance evidence must be refreshed before submission.
- Event labels are candidate-level because direct event ID alignment is weak.
- Altman is robustness-only because full-component coverage is limited.
- Tone/text extraction is not included in the v2 firm-year panel and should not be claimed.
- DOCX generation is complete, structural QA passed, and direct visual render QA passed using `/Applications/LibreOffice.app`. The bundled `render_docx.py` path remains blocked by a local `liblcms2.2.dylib` dependency issue, so the exact final upload file should still be rerendered after journal-specific formatting.
