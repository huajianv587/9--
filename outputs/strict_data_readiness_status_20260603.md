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
| Download checklist at reviewer-data-package level | 80-85% | The critical raw blocks are present, but the checklist still requires missing-ID reconciliation, duplicate handling, leakage checks, and market/current-universe boundary decisions after merge. |
| Unified cleaned v2 panel | 70-75% | A provisional Capital IQ v2 panel has now been built from the baseline firm-year panel plus supplemental raw workbooks, with 21,737 rows, 2,335 companies, FY2014-FY2024, and zero duplicate company-year rows. It is not yet sample-frozen. |
| Sample freeze and exclusion audit | 70-75% | A provisional sample-freeze script now defines duplicate, market, analyst-timing, structure-name, event-window, and label-specific sample flags. It is still not final because industry classifications and tone/text-quality exclusions are not available in the v2 firm-year panel. |
| Label construction readiness | 75-80% | Broad, strict accounting, persistent, Altman, and event candidate labels now exist and have sample counts plus preliminary logit checks. Event labels still rely on conservative name matching rather than direct Entity ID matching. |
| Overall data readiness for final model rerun | 85-90% | The v2 merge, provisional sample freeze, winsorization, missingness rules, preliminary firm-clustered logit checks, market split, label robustness, onset sample, COVID exclusion, and prediction-increment checks are now in place. Remaining blockers are final industry/tone exclusions, event-ID reconciliation, and final manuscript-table regeneration. |
| Full paper-to-submission readiness | 45-50% | Results now support a conditional strict-accounting-stress manuscript route, but manuscript rewrite, final tables, target-journal packaging, and submission QA remain incomplete. |

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
- Current raw completion audit: `outputs/capital_iq_raw_data_completion_audit_20260603.md`.

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

## Binding Next Step

Do not continue blind downloading before reviewing the v2 diagnostics. The next highest-value step is sample freeze and unified cleaning based on the v2 panel:

1. sample-freeze table;
2. field/year/market missingness audit;
3. duplicate company-year audit;
4. historical-market-cap date audit;
5. analyst timing/leakage audit;
6. Altman/strict/persistent/event label construction audit;
7. Go/No-Go decision for using Altman as main label versus robustness-only label.

Specific next decisions:

- whether to keep Altman as a main label given only 4,102 full-component candidate rows;
- whether to treat Key Developments as broad going-concern/delisting event evidence rather than strict bankruptcy/default evidence;
- whether to re-download Key Developments with baseline-compatible Entity ID before using event labels in a reviewer-facing main model;
- whether to exclude FY2024 from forward-event labels and FY2023 from 24-month labels;
- whether the 58 analyst timing violations are dropped, repaired, or used only after leakage-safe correction.
