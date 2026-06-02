# Submission Ladder Master Status

Date: 2026-06-01

Last updated: 2026-06-02 12:37 +08

## Objective Boundary

User target: regular SSCI/SCIE-level journal, JCR Q3 where possible, not CAS-based, normal SSCI-level reputation, and a stable 70-80% acceptance expectation.

Current evidence does **not** prove a single-journal 70-80% route. The correct operating interpretation is a project-level ladder: submit a strengthened paper to the best-fitting regular journal first, then use prebuilt transfer packages if the paper is rejected without a fatal data objection.

Do not describe any single journal in this package as a guaranteed 70-80% acceptance route.

## Current Submission Ladder

| Order | Package | Role | Current status | Probability boundary |
|---:|---|---|---|---|
| 1 | `submission_package/apjfs_20260601_submission_package.zip` | Primary regular SSCI/JCR Q3 finance-journal route | Ready for user review and final portal preparation | No verified single-journal 70-80% evidence |
| 2 | `submission_package/economic_record_20260601_transfer_package.zip` | Regular SSCI/JCR Q3 economics transfer route | Complete transfer package with DOCX, title page, cover letter, portal fields, and audit | 37% visible acceptance-rate signal, not 70-80% |
| 3 | `submission_package/applied_economics_20260601_transfer_package.zip` | Broader applied-economics transfer route | Complete transfer package | 40% displayed acceptance rate, but not strict Q3 in the current visible best-quartile screen |
| 4 | `submission_package/ael_20260601_submission_package.zip` | Compressed empirical-letter fallback | Complete package | 35% displayed acceptance rate, not 70-80% |

## Manuscript Strengthening Completed

- Full APJFS-style finance manuscript generated and rendered.
- APJFS DOCX/PDF visual QA refreshed on 2026-06-02 after the sample-boundary edits; the main manuscript renders to 19 pages, the title/declarations file renders to 1 page, and the table pages show no visible overlap or clipping. Latest visual QA audit: `outputs/apjfs_docx_pdf_visual_qa_20260602.md`.
- Transfer package DOCX/PDF visual QA refreshed on 2026-06-02 after the same sample-boundary edits; Economic Record renders to 12 pages, Applied Economics renders to 11 pages, the AEL anonymous manuscript renders to 5 pages, and the AEL with-author template renders to 6 pages without visible overlap or table clipping. Latest transfer visual QA audit: `outputs/submission_ladder_transfer_visual_qa_20260602.md`.
- Economic Record full-paper transfer manuscript generated and rendered.
- Applied Economics full-paper transfer manuscript generated and rendered.
- AEL short-letter package retained as compressed fallback.
- Economic Record, Applied Economics, and AEL text paths were synchronized on 2026-06-02 with the Chrome data boundary, conservative Capital IQ data/code wording, and the exchange-consistent ASX/SGX/Catalist robustness result.
- Round 16 and Round 17 current-source journal rechecks added on 2026-06-02; they confirm current SSCI/JCR Q3-compatible signals for several outlets but still do not verify a scope-fitting 70-80% single-journal route.
- Main empirical result remains robust across:
  - firm-clustered logit standard errors;
  - stricter next-year stress label;
  - COVID outcome-year exclusion;
  - trimmed propensity-score common support;
  - inverse-probability weighting;
  - market-year size-decile fixed effects;
  - current-stress control;
  - onset-sample exclusion;
  - analyst-intensity specification;
  - exchange-consistent ASX/SGX/Catalist sample restriction;
  - firm and year fixed-effects LPM.

## Data Status

The Capital IQ / Safari data task is partially advanced but not a new model input.

Current Safari status:

- Computer Use repeatedly returned `cgWindowNotFound`, and `list_apps` timed out in the earlier GUI-bridge tests.
- AppleScript originally saw Safari tabs titled `Office Screener | Application`; after the Chrome export flow, the latest Safari status reports `CIQ Pro: Document Intelligence` at a Capital IQ documents URL.
- Safari DOM extraction is still blocked because `Allow JavaScript from Apple Events` is not enabled.
- System Events now reports two Safari windows, but Safari is still not frontmost and the reported window positions/sizes are abnormal; this has not produced usable Safari DOM control.
- A terminal attempt to set `AllowJavaScriptFromAppleEvents` failed because macOS refused writes to Safari's container preference domain.
- Downloads scans after the earlier Chrome ASX 200 proof export found no additional Safari-triggered Capital IQ/SPGlobal Excel or CSV export. Chrome later produced a stronger ASX/SGX/Catalist public-company export at 22:48:26 +08, an even cleaner ASX/SGX/Catalist operating-public-company export at 00:38:33 +08 on 2026-06-02, a FY2023 S&P Capital IQ Fundamentals financial-field export with explicit `12/31/2023` as-of labels at 00:57:55 +08, a wider FY2021-FY2023 S&P Capital IQ Fundamentals export at 01:21:00 +08, a FY2020-FY2023 S&P Capital IQ Fundamentals export at 01:48:48 +08, a current-operating FY2014-FY2023 S&P Capital IQ Fundamentals export at 02:25:51 +08, and the stronger-coverage current-public-company FY2014-FY2023 export at 02:37:20 +08.
- Latest machine-readable status: `outputs/capital_iq_safari_status_latest.json`.

Current Chrome status:

- The user authorized Chrome control after Safari remained inaccessible.
- The Codex Chrome extension successfully controlled a logged-in Capital IQ tab and navigated to Office Screener.
- `Open Saved Criteria & Fields (Project)` showed no saved project rows; `Open Saved Screen Criteria` showed generic index screens only.
- A generic `S&P ASX 200` saved screen was opened, run, and exported from Chrome as the first browser-control proof.
- A new screen was then constructed directly in Capital IQ with `Exchange [Current] In ASX;Catalist;SGX` and `Company Type In Public Company`, run with 2,240 results, and exported from Chrome.
- A stricter current-universe screen added `Company Status In Operating`, returned 2,050 results, and was exported from Chrome.
- The same Chrome-controlled field selector then added S&P Capital IQ Fundamentals fields with `Period = FY2023` and `As Of Date = 12/31/2023`: total assets, total revenue, EBIT, interest expense, net income, total debt, total equity, and cash from operations.
- Chrome then extended the Capital IQ Fundamentals export to FY2022, FY2021, FY2020, and finally through FY2014 using the same eight `IQ_*` fields.
- Chrome then removed `Company Status In Operating`, reran the full-span display fields on the current public-company universe, and exported 2,240 rows.
- Strongest current Chrome-triggered download proof and coverage proof: `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_9a7f1287-0096-45e1-abba-62c17000cad1.xlsx`, 2026-06-02 02:37:20 +08, 1,902,072 bytes, 2,240 data rows, 84 columns, with `FY2023` / `12/31/2023`, `FY2022` / `12/31/2022`, FY2021 fiscal-year labels with blank as-of rows, and explicit year-end as-of labels for FY2020 through FY2014 including `12/31/2020` and `12/31/2014`.
- Latest Chrome export audit: `outputs/capital_iq_chrome_asx_sgx_catalist_public_company_audit_20260601.md`.
- Latest stricter Chrome export audit: `outputs/capital_iq_chrome_asx_sgx_catalist_operating_public_company_audit_20260602.md`.
- Latest FY2023 as-of financials Chrome audit: `outputs/capital_iq_chrome_fy2023_asof_financials_audit_20260602.md`.
- Latest FY2020-FY2023 financials Chrome audit: `outputs/capital_iq_chrome_fy2020_fy2023_financials_audit_20260602.md`.
- Latest FY2014-FY2023 financials Chrome audit: `outputs/capital_iq_chrome_fy2014_fy2023_financials_audit_20260602.md`.
- Latest public-company FY2014-FY2023 financials Chrome audit: `outputs/capital_iq_chrome_public_company_fy2014_fy2023_financials_audit_20260602.md`.
- Latest missing-ID sample-boundary audit: `outputs/capital_iq_public_company_missing_model_ids_20260602.md`.
- Latest manuscript-facing exchange-consistent robustness audit: `outputs/apjfs_exchange_consistent_sample_robustness_20260602.md`; the restricted ASX/SGX/Catalist sample keeps 18,411 labelled observations, 11,786 stress events, and preserves the analyst-coverage result with odds ratio 0.557.
- Latest targeted Entity-ID export audit: `outputs/capital_iq_entity_id_targeted_export_attempt_20260602.md`. Chrome confirmed precise single-ID export with `Entity ID = 4980397`, returning `Jadestone Energy plc (AIM:JSE)` and downloading `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_c81d7ff7-14df-41fb-8247-f2372e639c40.xlsx` at 09:52:39 +08. The same audit shows that the visible Office Screener UI did not provide a safe one-step 173-ID batch export path: `Includes` can create substring false positives, while semicolon-delimited `Equal` parsed only the first ID.
- Latest Entity-ID repeatability export pilot: `outputs/capital_iq_entity_id_repeatability_export_pilot_20260602.md`. Chrome confirmed repeatable precise single-ID exports with `Entity ID = 19880578`, returning `BYT Holdings Ltd. (CNSX:BYT)` and downloading `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_ff27168e-1e3e-42ca-b577-3e394f8cb789.xlsx` at 10:27:34 +08, and `Entity ID = 142839977`, returning `SWI Capital Holding Ltd. (ENXTAM:SWICH)` and downloading `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_43650838-3af1-4ac4-b4a3-998230a97876.xlsx` at 10:29:54 +08. Both workbooks have `Sheet1`, 7 rows, and 82 columns. A comma-separated equality test returned 0 rows, the `Add Companies` dialog did not expose a confirmed batch Entity-ID import path, and a small per-ID automation pilot became unsafe after page-focus drift.
- Latest stable single-ID export batch audit: `outputs/capital_iq_entity_id_stable_single_export_batch_20260602.md`. Chrome confirmed a more stable per-ID workflow by expanding `CRITERIA`, editing the visible summary row through the real `value_text` input, running the screen, verifying `Results (1)`, and exporting values. Five additional missing IDs exported successfully: `4988333`, `12934451`, `7719008`, `4993272`, and `4991260`. Across targeted attempts, eight unique missing model-panel IDs now have precise single-ID export proof.
- Latest NASDAQCM single-ID export batch audit: `outputs/capital_iq_entity_id_nasdaqcm_single_export_batch_20260602.md`. Chrome used the same stable per-ID workflow on `106505136`, `8325732`, `15051608`, `116717034`, and `115811006`; all five workbooks were verified from Downloads with exact `Entity ID = ...` screening criteria. Across targeted attempts, thirteen unique missing model-panel IDs had precise single-ID export proof at that checkpoint.
- Latest continued NASDAQCM single-ID export batch audit: `outputs/capital_iq_entity_id_nasdaqcm_continued_single_export_batch_20260602.md`. Chrome continued the same workflow on `10822760`, `101570773`, `107528004`, `117362762`, and `116262036`; all five workbooks were verified from Downloads with exact `Entity ID = ...` screening criteria. Across targeted attempts, eighteen unique missing model-panel IDs had precise single-ID export proof at that checkpoint.
- Latest third NASDAQCM single-ID export batch audit: `outputs/capital_iq_entity_id_nasdaqcm_third_single_export_batch_20260602.md`. Chrome continued the same workflow on `19564608`, `118275627`, `105955434`, `108543834`, `119962186`, `7128277`, `120103494`, `19932796`, `114661067`, and `105925327`; all ten workbooks were verified from Downloads with exact `Entity ID = ...` screening criteria. Across targeted attempts, twenty-eight unique missing model-panel IDs had precise single-ID export proof at that checkpoint.
- Latest fourth NASDAQCM single-ID export batch audit: `outputs/capital_iq_entity_id_nasdaqcm_fourth_single_export_batch_20260602.md`. Chrome continued the same workflow on `124102911`, `13425610`, `108602009`, `15315205`, `112234389`, `105706368`, `27833777`, `19932970`, `134561054`, `29742218`, `106610076`, and `118289694`; all twelve workbooks were verified from Downloads with exact `Entity ID = ...` screening criteria. Across targeted attempts, forty unique missing model-panel IDs now have precise single-ID export proof.
- Latest fifth partial NASDAQCM single-ID export batch audit: `outputs/capital_iq_entity_id_nasdaqcm_fifth_single_export_batch_20260602.md`. Chrome continued the same 82-column workflow on `108043631`, `111474686`, `119162267`, `134705526`, `117673507`, and `105894570`; all six counted workbooks were verified from Downloads with exact `Entity ID = ...` screening criteria. A fresh Chrome tab later reproduced `114626074` / `Rectitude Holdings Ltd (NASDAQCM:RECT)` with `Results (1)`, but only on a two-column default grid and without a verified 82-column workbook, so it is not counted. Across targeted attempts, forty-six unique missing model-panel IDs now have precise single-ID export proof.
- Latest identifier-only NASDAQCM recovery batch audit: `outputs/capital_iq_entity_id_nasdaqcm_identifier_only_recovery_batch_20260602.md`. After both existing Screener tabs became unstable for screenshot/DOM work, Chrome opened a clean Office Screener tab and exported exact default-grid workbooks for `114626074`, `106271074`, `100365343`, `115816935`, `110388492`, and `19411859`; each workbook has `Sheet1`, 3 rows, 2 columns, and exact `Entity ID = ...` screening criteria. This raises total exact single-ID workbook export evidence to fifty-two unique missing IDs, but the 82-column financial-field proof count remains forty-six.
- Latest Basic Financial Details NASDAQCM recovery batch audit: `outputs/capital_iq_entity_id_nasdaqcm_basic_financial_details_recovery_batch_20260602.md`. Chrome restored `Basic Financial Details Template` on the clean Office Screener tab and exported exact 12-column LTM financial-details workbooks for `115021631`, `105763599`, `28813776`, `8367240`, `17323870`, and `114081155`; each workbook has `Sheet1`, 7 rows, 12 columns, exact `Entity ID = ...` screening criteria, and fields including `SP_TOTAL_REV`, `SP_EBITDA`, `SP_NET_INC`, `SP_TOTAL_ASSETS`, `SP_TOTAL_DEBT`, `SP_TOTAL_EQUITY`, and `SP_PERIOD_END`. This raises total exact single-ID workbook export evidence to fifty-eight unique missing IDs and direct single-ID financial-field workbook evidence to fifty-two if LTM Basic Financial Details are counted separately, but the 82-column FY2014-FY2023 financial-field proof count remains forty-six.
- Latest final NASDAQCM Basic Financial Details batch audit: `outputs/capital_iq_entity_id_nasdaqcm_final_basic_financial_details_batch_20260602.md`. Chrome kept `Basic Financial Details Template` and exported exact 12-column LTM financial-details workbooks for `108767989`, `118388356`, `108002922`, `114658415`, and `114297536`; this completes exact workbook evidence for the first fifty-five `NASDAQCM` missing rows. Total exact single-ID workbook export evidence is now sixty-three unique missing IDs, direct single-ID financial-field workbook evidence is fifty-seven if LTM Basic Financial Details are counted separately, and the 82-column FY2014-FY2023 financial-field proof count remains forty-six.
- Latest machine-readable Chrome download status: `outputs/capital_iq_chrome_download_status_latest.json`.

Data rule:

- Do not add the visible three-company peer-comparison screener as a model input.
- Do not add current/no-date market-cap fields as historical predictors.
- Do not add the generic `S&P ASX 200` Chrome export as a model input; it is a browser-control/download proof only.
- Do not add the ASX/SGX/Catalist public-company Chrome export as a model input; it is a current exchange-universe/provenance export, not a historical firm-year predictor panel.
- Do not add the ASX/SGX/Catalist operating-public-company Chrome export as a model input; its stricter `Operating` status is useful for current-universe provenance but excludes historical firms that can legitimately appear in the 2014-2023 model panel.
- Do not add the FY2014-FY2023 Chrome financials exports as manuscript model inputs yet; they prove Chrome can download fiscal-year-labelled Capital IQ fundamentals across the full manuscript fiscal-year span, and the public-company version improves model-ID overlap from 1,997 to 2,162, but it is still a current exchange screen, misses 173 historical model-panel companies, has blank FY2021 as-of rows, and has not been reconciled into the model pipeline.
- Do not add the targeted single-ID Chrome export as a manuscript model input. It proves precise identifier retrieval but is not a full 173-ID reconciliation and has not passed model-pipeline integration.
- Do not add the repeatability-pilot single-ID Chrome exports as manuscript model inputs. They prove precise identifier retrieval is repeatable, but they are not a safe 173-ID batch reconciliation and did not pass model-pipeline integration.
- Do not add the stable single-ID Chrome export batches as manuscript model inputs. They prove the per-ID reconciliation route is usable, but the 82-column financial-field proof covers only 46 of 173 missing model-panel IDs and has not passed full field-year/as-of audit or model-pipeline integration.
- Do not add the identifier-only Chrome recovery batch as a manuscript model input. It proves exact Entity-ID retrievability for six additional missing IDs and raises total exact workbook evidence to 52 unique missing IDs, but it has only `Entity Name` and `Entity ID` columns and no financial-field schema.
- Do not add the Basic Financial Details Chrome recovery batch as a manuscript model input. It proves six additional exact IDs have LTM financial fields in Capital IQ, but it is not the 82-column FY2014-FY2023 historical schema, does not solve FY2021 as-of blanks, and does not pass historical-universe/model-pipeline reconciliation.
- Do not add the final NASDAQCM Basic Financial Details Chrome batch as a manuscript model input. It completes the visible `NASDAQCM` exact-ID segment and proves LTM field availability for five more IDs, but it is still not the historical FY2014-FY2023 model panel.
- Use the exchange-consistent ASX/SGX/Catalist robustness check as the manuscript-facing response to the current geography-versus-exchange sample-boundary risk; it is computed from the existing model panel and does not require merging the raw Chrome export.
- Do not upload raw S&P Capital IQ exports or firm-level Capital IQ-derived panels.

## Current Verification Commands

Run all of these before any actual upload:

```bash
/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_apjfs_submission_package.py
/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_economic_record_transfer_package.py
/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_applied_economics_transfer_package.py
/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_ael_submission_package.py
/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_submission_ladder_master.py
/usr/bin/python3 scripts/audit_capital_iq_public_company_missing_ids.py
/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_capital_iq_safari_status.py --after '2026-06-01 22:24:42' --out-json outputs/capital_iq_safari_status_latest.json
/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_capital_iq_chrome_download_status.py --after '2026-06-02 02:36:00' --expect-name 'SPGlobal_Export_6-1-2026_9a7f1287-0096-45e1-abba-62c17000cad1.xlsx' --out-json outputs/capital_iq_chrome_download_status_latest.json
```

## Final Gate

The project is not finished under the original objective until either:

1. a scope-fitting regular SSCI/SCIE Q3 journal with credible 70-80% single-journal acceptance evidence is verified; or
2. the user explicitly accepts the current project-level ladder interpretation instead of a single-journal 70-80% requirement.

Until then, the current state is: **strong multi-package submission ladder, not complete proof of the requested 70-80% single-journal target.**

## Blocked Audit

The active-goal blocker is documented in `docs/active_goal_blocked_audit_20260601.md`.

Current blocking conditions:

- no verified scope-fitting regular SCIE/SSCI/JCR Q3 single journal with credible 70-80% acceptance evidence;
- Safari/Capital IQ still cannot be controlled from the current Safari state because Computer Use cannot obtain Safari windows, AppleScript DOM execution is blocked, and terminal preference writes are denied by macOS.
- Chrome can control Capital IQ, construct relevant ASX/SGX/Catalist public-company and operating-public-company screens, set S&P Capital IQ Fundamentals fields across `FY2014`-`FY2023`, remove criteria, rerun screens, and trigger downloads. The latest public-company full-span export reduces the model-ID gap from 338 to 173; the 173 missing IDs are now audited as a sample-boundary issue rather than random field-export failure. The exchange-consistent ASX/SGX/Catalist robustness check passes, but the Chrome export still requires historical-universe and FY2021 as-of reconciliation before it can replace or extend the model panel.
- Direct targeted, repeatability, stable 82-column single-ID tests, the identifier-only recovery batch, and the two Basic Financial Details recovery batches confirm that 63 individual missing IDs can be exported precisely, including the first fifty-five `NASDAQCM` missing rows. Only 46 of those IDs have the 82-column FY2014-FY2023 financial-field schema; eleven additional IDs now have 12-column LTM Basic Financial Details workbooks. The current Office Screener UI still has not exposed a safe one-step batch route for all 173 IDs. This reinforces the decision to keep the Chrome exports as provenance audits and use the exchange-consistent robustness check for manuscript-facing sample-boundary defense until a complete targeted reconciliation is finished.
