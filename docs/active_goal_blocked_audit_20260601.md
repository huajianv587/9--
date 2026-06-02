# Active Goal Blocked Audit

Date: 2026-06-01

## Original Goal

按照用户要求：正规 SSCI 同级别、不按中科院，将整篇论文完善到三区、稳 70-80% 接收率；数据方面直接控制 Safari 下载。

## Current Completed Work

- APJFS primary package is complete and passes checks.
- Economic Record regular SSCI/JCR Q3 economics transfer package is complete and passes checks.
- Applied Economics transfer package is complete and passes checks.
- AEL fallback package is complete and passes checks.
- Master submission ladder check passes.
- Manuscript evidence has been strengthened with firm-clustered standard errors, stricter stress labels, COVID exclusion, propensity-score trimming, IPTW, size-decile fixed effects, an exchange-consistent ASX/SGX/Catalist sample restriction, current-stress controls, onset-sample exclusion, analyst-intensity checks, and firm/year fixed-effects LPM.
- After user authorization, Chrome control of Capital IQ succeeded, first producing a generic ASX 200 Excel download proof, then a stronger ASX/SGX/Catalist public-company Excel export, then a stricter ASX/SGX/Catalist operating-public-company Excel export, then FY2023, FY2021-FY2023, FY2020-FY2023, current-operating FY2014-FY2023, and current-public-company FY2014-FY2023 S&P Capital IQ Fundamentals financial-field exports. None of these files is part of the manuscript model data yet.
- The missing-ID audit now shows that the remaining 173 model-panel IDs are Singapore-side records with non-SGX/Catalist ticker suffixes such as NASDAQCM and SEHK. A manuscript-facing exchange-consistent ASX/SGX/Catalist robustness check keeps 18,411 labelled observations and preserves the main result with odds ratio 0.557. Targeted Chrome tests now prove repeatable precise 82-column single-ID exports for forty-six unique missing IDs, identifier-only exact workbook exports for six more, and 12-column LTM Basic Financial Details exports for eleven more, but not a safe 173-ID batch route or model-ready reconciliation.

## Blocking Condition 1: Exact Single-Journal 70-80%

After repeated regular SCIE/SSCI/JCR screens, no scope-fitting normal-reputation SCIE/SSCI Q3 finance/economics/business journal with credible single-journal 70-80% acceptance evidence has been verified.

Current best defensible route is a project-level ladder:

1. APJFS primary route: regular SSCI/JCR Q3 finance fit, but no verified 70-80% acceptance signal.
2. Economic Record transfer: regular SSCI/JCR Q3 economics backup, 37% visible acceptance-rate signal.
3. Applied Economics transfer: 40% displayed acceptance rate, but not strict Q3 in the current visible best-quartile screen.
4. AEL fallback: 35% displayed acceptance rate.

This does not prove the user's original single-journal 70-80% condition.

## Blocking Condition 2: Direct Browser / Capital IQ Research Export

The Safari-specific Capital IQ task still cannot be completed from the current agent state. A Chrome workaround now proves authenticated Capital IQ browser control, custom screen construction, display-field configuration, fiscal-year/as-of financial-field export, and download capability. It still did not provide a full-sample 2014-2023 historical research export.

Evidence:

- Computer Use repeatedly returns `cgWindowNotFound` for Safari.
- Computer Use `list_apps` also timed out, indicating broader GUI bridge failure rather than only a webpage problem.
- AppleScript can see Safari tabs titled `Office Screener | Application` at the Capital IQ Office Screener URL.
- After the Chrome export flow, the latest Safari script sees `CIQ Pro: Document Intelligence` at a Capital IQ documents URL rather than the earlier Office Screener tab.
- AppleScript DOM extraction fails because Safari has not enabled `Allow JavaScript from Apple Events`.
- Apple documents that this setting is required to allow JavaScript to be executed on webpages via AppleScript.
- A terminal attempt to set `AllowJavaScriptFromAppleEvents` failed because macOS refused writes to Safari's container preference domain.
- Creating a new Safari document at the Capital IQ URL increased Safari's AppleScript window count. Earlier System Events checks reported zero accessible Safari windows; after the Chrome export flow, System Events reports two Safari windows with abnormal off-screen positions/sizes, but this still has not produced usable Safari DOM control.
- Chrome extension control successfully claimed a logged-in Capital IQ tab, opened Office Screener, ran the generic `S&P ASX 200` saved screen, and downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_e1df1ce4-ae1a-4fed-be7d-bc2d439b52ed.xlsx`.
- Chrome then constructed a new screen with `Exchange [Current] In ASX;Catalist;SGX` and `Company Type In Public Company`, ran 2,240 results, and downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_05b00b5f-f6bb-4535-8c71-4ada625fec66.xlsx`.
- Chrome then added `Company Status In Operating`, ran 2,050 results, and downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_35315e47-5458-44d2-9b0e-dce3d696b52b.xlsx`.
- Chrome then used the Capital IQ `DISPLAY COLUMNS` field selector to add S&P Capital IQ Fundamentals fields with `Period = FY2023` and `As Of Date = 12/31/2023`, then downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_58dce7cb-583f-4d1a-8d5d-0db1151bfc77.xlsx`.
- The FY2023 as-of financials export has 2,050 data rows, 13 columns, and explicit `FY2023` / `12/31/2023` labels for `IQ_TOTAL_ASSETS`, `IQ_TOTAL_REV`, `IQ_EBIT`, `IQ_INTEREST_EXP`, `IQ_NET_INC_PARENT`, `IQ_TOTAL_DEBT`, `IQ_TOTAL_EQUITY`, and `IQ_CASH_OPER`.
- Chrome then extended the same S&P Capital IQ Fundamentals fields to `FY2022`, `FY2021`, and `FY2020`, then downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_3b97feaa-a0d3-4ab4-92b0-203a0c6a9e98.xlsx`.
- The FY2020-FY2023 financials export has 2,050 data rows, 37 columns, explicit `FY2023` / `12/31/2023`, `FY2022` / `12/31/2022`, and `FY2020` / `12/31/2020` labels, plus `FY2021` labels with blank as-of rows for the same eight `IQ_*` fields.
- Chrome then extended the same S&P Capital IQ Fundamentals fields through `FY2014`, repaired a duplicate FY2014 cash-from-operations selected field, verified one copy of all 80 field-year combinations, and downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_71bcb677-981d-4f92-b8c1-d782d88c07f8.xlsx`.
- The FY2014-FY2023 financials export has 2,050 data rows, 85 columns, explicit year-end as-of labels for every year except FY2021 including `12/31/2014`, and the same eight `IQ_*` fields for the full manuscript fiscal-year span.
- Chrome then removed `Company Status In Operating`, reran the full FY2014-FY2023 display fields on the current public-company universe, verified one copy of all 80 field-year combinations, and downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_9a7f1287-0096-45e1-abba-62c17000cad1.xlsx`.
- The current-public-company FY2014-FY2023 financials export has 2,240 data rows, 84 columns, explicit year-end as-of labels for every year except FY2021, and the same eight `IQ_*` fields for the full manuscript fiscal-year span.
- The public-company full-span Chrome export overlaps 2,162 of the 2,335 existing model-panel company IDs and reduces missing model-panel IDs from 338 to 173. It is the strongest historical-schema and coverage bridge so far, but it is still a current exchange-universe export rather than a validated replacement for the historical research panel.
- A direct targeted test with `Entity ID = 4980397` returned `Jadestone Energy plc (AIM:JSE)` and downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_c81d7ff7-14df-41fb-8247-f2372e639c40.xlsx`; subsequent repeatability tests with `Entity ID = 19880578` and `Entity ID = 142839977` returned `BYT Holdings Ltd. (CNSX:BYT)` and `SWI Capital Holding Ltd. (ENXTAM:SWICH)` and downloaded `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_ff27168e-1e3e-42ca-b577-3e394f8cb789.xlsx` and `/Users/guohuiwen/Downloads/SPGlobal_Export_6-1-2026_43650838-3af1-4ac4-b4a3-998230a97876.xlsx`.
- A more stable per-ID workflow then exported five additional missing IDs: `4988333` / `MClean Technologies Berhad (KLSE:MCLEAN)`, `12934451` / `Prestige BioPharma Limited (KOSE:A950210)`, `7719008` / `Asia Strategic Holdings Limited (LSE:ASIA)`, `4993272` / `Avation PLC (LSE:AVAP)`, and `4991260` / `XP Power Limited (LSE:XPP)`.
- The same per-ID workflow then exported five first `NASDAQCM` missing-ID rows: `106505136` / `ARB IOT Group Limited (NASDAQCM:ARBB)`, `8325732` / `Aeries Technology, Inc (NASDAQCM:AERT)`, `15051608` / `BTC Digital Ltd. (NASDAQCM:BTCT)`, `116717034` / `Basel Medical Group Ltd (NASDAQCM:BMGL)`, and `115811006` / `BeLive Holdings (NASDAQCM:BLIV)`.
- The continued per-ID workflow then exported five more `NASDAQCM` missing-ID rows: `10822760` / `Bit Origin Ltd (NASDAQCM:BTOG)`, `101570773` / `BitFuFu Inc. (NASDAQCM:FUFU)`, `107528004` / `Bitdeer Technologies Group (NASDAQCM:BTDR)`, `117362762` / `Concorde International Group Ltd. (NASDAQCM:YOOV)`, and `116262036` / `Cuprina Holdings (Cayman) Limited (NASDAQCM:CUPR)`.
- The third per-ID workflow then exported ten more `NASDAQCM` missing-ID rows: `19564608` / `CytoMed Therapeutics Limited (NASDAQCM:GDTC)`, `118275627` / `Delixy Holdings Limited (NASDAQCM:DLXY)`, `105955434` / `EUDA Health Holdings Limited (NASDAQCM:EUDA)`, `108543834` / `FBS Global Limited (NASDAQCM:FBGL)`, `119962186` / `Fast Track Group (NASDAQCM:FTRK)`, `7128277` / `FingerMotion, Inc. (NASDAQCM:FNGR)`, `120103494` / `Fitness Champs Holdings Limited (NASDAQCM:FCHL)`, `19932796` / `Guardforce AI Co., Limited (NASDAQCM:GFAI)`, `114661067` / `Helport AI Limited (NASDAQCM:HPAI)`, and `105925327` / `High-Trend International Group (NASDAQCM:HTCO)`.
- The fourth per-ID workflow then exported twelve more `NASDAQCM` missing-ID rows: `124102911` / `HomesToLife Ltd. (NASDAQCM:HTLM)`, `13425610` / `Horizon Quantum Holdings Ltd. (NASDAQCM:HQ)`, `108602009` / `Hotel101 Global Holdings Corp. (NASDAQCM:HBNB)`, `15315205` / `INNEOVA Holdings Limited (NASDAQCM:INEO)`, `112234389` / `JBDI Holdings Limited (NASDAQCM:JBDI)`, `105706368` / `JE Cleantech Holdings Limited (NASDAQCM:JCSE)`, `27833777` / `Karooooo Ltd. (NASDAQCM:KARO)`, `19932970` / `Lion Group Holding Ltd. (NASDAQCM:LGHL)`, `134561054` / `Magnitude International Ltd (NASDAQCM:MAGH)`, `29742218` / `Mobile-health Network Solutions (NASDAQCM:MNDR)`, `106610076` / `NetClass Technology Inc (NASDAQCM:NTCL)`, and `118289694` / `OMS Energy Technologies Inc. (NASDAQCM:OMSE)`.
- The fifth partial per-ID workflow then exported six more 82-column `NASDAQCM` missing-ID rows: `108043631` / `Ohmyhome Limited (NASDAQCM:OMH)`, `111474686` / `Orangekloud Technology Inc. (NASDAQCM:ORKT)`, `119162267` / `PTL Limited (NASDAQCM:PTLE)`, `134705526` / `Platinum Analytics Cayman Limited (NASDAQCM:PLTS)`, `117673507` / `Premium Catering (Holdings) Limited (NASDAQCM:PC)`, and `105894570` / `Primech Holdings Ltd. (NASDAQCM:PMEC)`. A fresh Chrome tab reproduced `114626074` / `Rectitude Holdings Ltd (NASDAQCM:RECT)` with `Results (1)`, but it did not preserve the 82-column export schema or produce a verified workbook, so it is not counted.
- The identifier-only recovery workflow then opened a clean Chrome Screener tab and exported exact two-column default-grid workbooks for `114626074` / `Rectitude Holdings Ltd (NASDAQCM:RECT)`, `106271074` / `Republic Power Group Limited (NASDAQCM:RPGL)`, `100365343` / `SAIHEAT Limited (NASDAQCM:SAIH)`, `115816935` / `SKK Holdings Limited (NASDAQCM:SKK)`, `110388492` / `Simpple Ltd. (NASDAQCM:SPPL)`, and `19411859` / `Sound Group Inc. (NASDAQCM:SOGP)`. These are exact workbook exports but not financial-field exports.
- The Basic Financial Details recovery workflow then restored `Basic Financial Details Template` on the clean Chrome Screener tab and exported exact 12-column LTM financial-details workbooks for `115021631` / `Springview Holdings Ltd (NASDAQCM:SPHL)`, `105763599` / `SuperX AI Technology Limited (NASDAQCM:SUPX)`, `28813776` / `TOP Financial Group Limited (NASDAQCM:TOP)`, `8367240` / `Ten-League International Holdings Limited (NASDAQCM:TLIH)`, `17323870` / `The Growhub Limited (NASDAQCM:TGHL)`, and `114081155` / `Trident Digital Tech Holdings Ltd (NASDAQCM:TDTH)`. These prove exact retrievability and LTM financial-field availability for six more missing IDs, but they are not FY2014-FY2023 historical-schema workbooks.
- The final NASDAQCM Basic Financial Details workflow then exported exact 12-column LTM financial-details workbooks for `108767989` / `Tungray Technologies Inc. (NASDAQCM:TRSG)`, `118388356` / `Uni-Fuels Holdings Limited (NASDAQCM:UFG)`, `108002922` / `Webuy Global Ltd (NASDAQCM:WBUY)`, `114658415` / `YY Group Holding Limited (NASDAQCM:YYGH)`, and `114297536` / `iOThree Limited (NASDAQCM:IOTR)`. This completes exact workbook evidence for the first fifty-five `NASDAQCM` missing rows, but it remains outside the historical model panel.
- The visible Office Screener UI still did not expose a safe one-step batch route: comma-separated `Equal` returned 0 rows, semicolon-delimited `Equal` previously parsed only the first ID, `Includes` can create substring false positives, and a small unattended per-ID pilot became unsafe after page-focus drift.

## What Is Needed To Unblock

At least one external-state change is required:

1. User enables Safari's `Allow JavaScript from Apple Events` in Safari's Developer settings and makes the Capital IQ Safari window visible in the current desktop session, if Safari itself must be used; or
2. User identifies or manually opens a full-sample historical Capital IQ saved project/export, or approves reconciling the Chrome public-company FY2014-FY2023 export against the remaining 173 missing model-panel IDs and the FY2021 as-of-label gap; or
3. User explicitly accepts the current project-level submission ladder instead of requiring a verified single-journal 70-80% route.

Until then, the original goal is not achievable as stated. The browser-control blocker is materially reduced by Chrome, including verified current-operating and current-public-company FY2014-FY2023 financials downloads, repeatable precise 82-column single-ID exports for forty-six missing IDs, exact identifier-only workbook exports for six more IDs, and exact 12-column LTM Basic Financial Details workbook exports for eleven more IDs, but the remaining 110 IDs without any single-ID workbook, the remaining 116 IDs without any direct single-ID financial-field workbook, the remaining 127 IDs without 82-column FY2014-FY2023 financial-field proof, the historical-universe/model-reconciliation blocker, and the single-journal 70-80% condition remain unproved.
