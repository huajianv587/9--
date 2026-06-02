# Strict Data Readiness Status

Date: 2026-06-03
Project: Analyst Coverage and Accounting-Based Financial Stress

## Reviewer-Level Decision

If "all required data" means local raw downloads plus base field audits, the Capital IQ supplemental raw layer is complete.

If "all required data" means an auditable dataset that can directly support sample freezing, unified cleaning, final labels, regressions, robustness tests, and a defensible SSCI/JCR Q3 manuscript, the project is not complete yet.

Current strict estimate:

| Scope | Readiness | Reason |
|---|---:|---|
| Raw Capital IQ supplemental downloads | 100% | The current raw completion audit lists all required Altman/liquidity/market-cap, liabilities, retained-earnings, event/status, and broad status-universe workbooks as downloaded and base-audited. |
| Raw workbook base audit layer | 100% | Each required supplemental workbook has a base audit and field/event audit, but most decisions remain `PASS_WITH_NOTES`, not clean unconditional pass. |
| Download checklist at reviewer-data-package level | 95-100% | For the current strict-accounting-stress claim boundary, the required raw downloads are present and base-audited. Additional downloads would only be needed if the paper expands into direct-ID event outcomes, tone/text measures, or industry-based exclusion claims. |
| Unified cleaned v2 panel | 90-92% | The Capital IQ v2 panel has been built from the baseline firm-year panel plus supplemental raw workbooks, with 21,737 rows, 2,335 companies, FY2014-FY2024, and zero duplicate company-year rows. It has moved beyond provisional construction, but final journal-facing exclusions still depend on the selected claim boundary. |
| Sample freeze and exclusion audit | 90-92% | The sample-freeze script defines duplicate, market, analyst-timing, structure-name, event-window, and label-specific sample flags. Remaining exclusions are not blockers for the strict route unless industry classifications or tone/text-quality exclusions are explicitly claimed. |
| Label construction readiness | 88-90% | Broad, strict accounting, persistent, Altman, and event candidate labels exist and have sample counts plus firm-clustered logit checks. Strict accounting stress is main-ready; Altman and event labels remain robustness/validation evidence rather than primary outcomes. |
| Overall data readiness for final model rerun | 90-92% | The v2 merge, sample freeze, winsorization, missingness rules, firm-clustered logit checks, market split, label robustness, onset sample, COVID exclusion, prediction-increment checks, manuscript tables, and draft package are now in place. Remaining data risks are event-ID reconciliation and absent tone/text fields, both outside the current strict main claim. |
| Full paper-to-submission readiness | 68-72% | Results support a conditional strict-accounting-stress route, v2 manuscript tables and draft text have been rebuilt, the full v2 DOCX draft has passed structural plus direct visual render QA, and an Applied Economics Letters strict v2 short draft now exists with render QA and automated package checks. Remaining blockers are live JCR/Web of Science verification, final author/declaration files, strict-route cover letter/portal fields, Capital IQ license wording confirmation, and final upload checks. |

## Evidence Inspected

- `data/raw/capital_iq/` currently contains 48 local `.xlsx` raw Capital IQ workbooks.
- `data/processed/` currently contains 11 `.csv` processed files, including the local v2 and frozen-candidate panels.
- Existing baseline panel: `data/processed/ael_apac_firm_year_panel.csv`, 21,737 firm-years and 2,335 unique companies over FY2014-FY2024.
- Existing processed market/Altman supplements:
  - `data/processed/capital_iq_asx_altman_market_supplement_20260602.csv`
  - `data/processed/capital_iq_catalist_altman_market_pilot_20260602.csv`
- Provisional v2 panel: `data/processed/ael_apac_firm_year_panel_v2_capital_iq_20260603.csv`.
- Provisional v2 audit: `outputs/ael_apac_firm_year_panel_v2_capital_iq_audit_20260603.md`.
- Local frozen candidate panel: `data/processed/ael_apac_firm_year_panel_v2_frozen_candidate_20260603.csv`.
- Sample-freeze audit: `outputs/ael_apac_v2_sample_freeze_cleaning_audit_20260603.md`.
- Strict accounting route Go/No-Go audit: `outputs/ael_v2_strict_accounting_go_no_go_20260603.md`.
- v2 strict-route manuscript draft: `manuscript/strict_accounting_stress_v2_manuscript.md`.
- v2 strict-route cover letter draft: `manuscript/strict_accounting_stress_v2_cover_letter.md`.
- v2 strict-route DOCX draft: `manuscript/strict_accounting_stress_v2_submission_manuscript.docx`.
- v2 DOCX structural QA: `outputs/strict_accounting_stress_v2_docx_structural_qa_20260603.md`.
- v2 DOCX direct render QA: 11 rendered PNG pages from the system-LibreOffice PDF conversion, with pages 1, 5, and 7-11 visually inspected.
- Current raw completion audit: `outputs/capital_iq_raw_data_completion_audit_20260603.md`.
- Current SSCI/JCR Q3-and-above target-route refresh: `outputs/ssci_jcr_q3_target_route_refresh_20260603.md`.
- Applied Economics Letters strict v2 short-route audit: `outputs/ael_strict_v2_submission_audit_20260603.md`.
- Applied Economics Letters strict v2 draft: `manuscript/ael_strict_accounting_stress_v2_letter.md`.
- Applied Economics Letters strict v2 DOCX draft: `manuscript/ael_strict_accounting_stress_v2_submission.docx`.

## Why This Is Not Yet 100% Data Readiness

The raw-data layer is complete, but a Q3 reviewer will not evaluate raw downloads. They will evaluate the final empirical panel and whether the paper can defend:

1. which company-years enter the sample;
2. which observations are excluded and why;
3. whether market cap is historical and date-labelled;
4. whether analyst variables are observable before the outcome window;
5. whether Altman/event labels are outcome variables, not leaked predictors;
6. whether missingness is quantified by field, year, market, and status;
7. whether inactive/delisted/former-listed companies are handled transparently.

Those checks require a unified v2 cleaning/merge pipeline. They cannot be proven by raw-workbook inventory alone.

## 2026-06-03 v2 Panel Update

The first unified v2 panel has now been generated and audited.

Key structural results:

- Rows: 21,737.
- Unique companies: 2,335.
- Fiscal years: 2014-2024.
- Duplicate company-year rows: 0.
- Altman candidate rows with all required components: 4,102.
- Altman distress-zone candidate positives: 1,820.
- Broad distress-event 12m candidate positives: 4,029.
- Broad distress-event 24m candidate positives: 5,341.
- Forecast-date rows after as-of date: 58.

Binding caveats:

- The event workbook's direct `SPCIQ ID` does not overlap with baseline `company_id`; event labels currently use conservative normalized-name matching and must be treated as candidate labels.
- Total liabilities coverage is still the binding Altman bottleneck, especially for Singapore rows.
- The frozen candidate panel has applied provisional sample exclusions and winsorization, but final journal-facing exclusion rules and label selection are not yet locked.

## 2026-06-03 Sample-Freeze Update

The first sample-freeze and unified-cleaning pass has now been generated.

Key freeze results:

- Broad stress appendix sample: 19,344 rows, event rate 63.5%.
- Strict accounting stress 12m sample: 19,322 rows, event rate 40.8%.
- Persistent broad stress 24m sample: 16,984 rows, event rate 57.5%.
- Altman distress-zone 12m sample: 3,459 rows, event rate 41.0%.
- Broad event candidate 12m sample: 19,353 rows, event rate 20.8%.
- Analyst timing violations excluded from model samples: 58 rows.
- Suspect REIT/fund/trust/SPAC-like structure proxy: 653 rows / 72 companies.

Preliminary firm-clustered logit checks:

- Strict accounting stress 12m: analyst-covered odds ratio 0.711, AME -7.2 percentage points, p < 0.001.
- Altman distress-zone 12m: odds ratio 0.710, p about 0.09, direction consistent but underpowered.
- Broad event candidate 12m: odds ratio 0.472, p < 0.001, but event-ID mapping remains candidate-level.

Current reviewer-level reading:

- The strict accounting-stress route is now the strongest candidate for the main story.
- Altman should be robustness or supporting evidence unless total-liabilities coverage is improved.
- Event evidence is useful validation but should not be called formal bankruptcy/default evidence without a direct-ID event export or stronger event taxonomy.
- Tone/text extraction and low-quality-text exclusion remain unverified because the v2 panel has no tone or raw-text fields.

## 2026-06-03 Strict-Route Go/No-Go Update

Status: `CONDITIONAL_GO_FOR_STRICT_ACCOUNTING_STRESS_ROUTE`.

Model-suite results:

- Main strict accounting stress: odds ratio 0.711, AME -7.2 percentage points, p < 0.001.
- ASX split: odds ratio 0.778, p = 0.003.
- Singapore split: odds ratio 0.492, p < 0.001.
- Onset sample excluding current strict stress: odds ratio 0.856, p = 0.077; direction survives but significance weakens.
- COVID outcome-year exclusion: odds ratio 0.713, p < 0.001.
- Analyst intensity: odds ratio 0.630 per log1p analyst count, p < 0.001.
- Altman robustness: odds ratio 0.710, p = 0.090; direction only.
- Broad event candidate: odds ratio 0.472, p < 0.001; candidate-level because event-ID mapping is not clean direct ID.
- Prediction increment: delta AUC -0.0001, delta Brier -0.0005.

Reviewer-facing implication:

- The manuscript should be positioned as an association/information-environment paper, not a prediction-performance paper.
- The main dependent variable should be strict subsequent accounting-based stress.
- Broad stress stays appendix; Altman and event labels are robustness/validation, not the primary claim.

## 2026-06-03 Draft Manuscript Package Update

Generated artifacts:

- v2 strict-route manuscript Markdown draft.
- v2 strict-route cover letter draft.
- five v2 manuscript tables under `outputs/manuscript_v2_strict/`.
- DOCX manuscript draft with portrait text section and landscape table section.
- DOCX structural QA report.
- Applied Economics Letters strict v2 short draft with three main tables.
- Applied Economics Letters strict v2 DOCX rendered to a 6-page PDF and PNG pages.

DOCX QA status:

- Structural QA passed: archive integrity OK, 70 paragraphs, 5 tables, 2 sections, v2 title present, old `19,402` broad-stress sample size absent.
- Direct visual render QA passed using the system LibreOffice application and Poppler rendering path.
- Visual QA inspected the full contact sheet plus pages 1, 5, and 7-11.
- The bundled `render_docx.py` route remains blocked by a local LibreOffice headless dependency error: missing `liblcms2.2.dylib`, but the direct system-LibreOffice route produced a usable PDF and 11 PNG pages.
- The DOCX is therefore a visually verified draft manuscript, not yet the exact final upload file.

Packaging implication:

- The paper is now a coherent v2 draft package with visual DOCX QA and a target-journal short-route AEL draft, but not a final portal-ready submission.

## Binding Next Step

The raw-download phase is complete for the current strict-accounting-stress manuscript route. Do not continue blind downloading merely to make the raw folder larger. The current primary route is Applied Economics Letters strict v2. The next highest-value steps are journal-route verification and final package hardening:

1. verify Applied Economics Letters in live JCR or institutional Web of Science before submission;
2. regenerate strict-route title page, declarations, cover letter, and portal paste fields;
3. lock blinded/non-blinded package requirements;
4. rerender the exact final DOCX/PDF after author/declaration formatting;
5. keep event labels as candidate validation unless a direct-ID Key Developments export is obtained;
6. keep tone/text out of the claim unless a separate text/tone dataset is downloaded, audited, and merged.

Specific data decisions:

- Altman should not be the main label given limited full-component coverage.
- Key Developments should be treated as broad event-candidate evidence rather than strict bankruptcy/default evidence unless a baseline-compatible Entity ID export is obtained.
- FY2024 should remain excluded from one-year-ahead outcome samples, and FY2023 should remain excluded from 24-month forward labels where appropriate.
- The 58 analyst timing violations should remain excluded from model samples unless repaired with leakage-safe forecast-date evidence.
