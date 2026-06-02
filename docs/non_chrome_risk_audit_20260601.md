# Non-Chrome Risk Audit

Date: 2026-06-01
Scope: risks other than the unresolved authenticated-browser download path.

## Verification Run

- `data_quality_check.py` now runs against the current APAC firm-year panel and returns: `YELLOW: adequate for conservative coverage framing; expand only if cheap`.
- `scripts/check_submission_ladder_master.py` passes with the bundled Codex Python runtime.
- The master check reruns all four package checks and validates zip integrity, manuscript markers, no author leakage in the APJFS double-blind manuscript, and the current no-70-80 probability boundary.
- The AEL supporting CSV table was cleaned so it no longer carries literal `<br>` markers, and `submission_package/ael_20260601_submission_package.zip` was rebuilt.

## Main Remaining Risks

1. Exact single-journal target is still unresolved.
   No scope-fitting regular SCIE/SSCI/JCR Q3 finance/economics/business journal with credible current 70-80% single-journal acceptance evidence has been verified. Do not describe APJFS, Economic Record, Applied Economics, or AEL as a 70-80% single-journal route.

2. Data licensing is a hard upload constraint.
   Raw S&P Capital IQ exports and firm-level Capital IQ-derived panels must not be uploaded. Only aggregate tables, manuscript outputs, and code that excludes licensed observations should be shared unless the institutional license explicitly permits more.

3. Analyst coverage depth is adequate but not high.
   The broad data audit is yellow on coverage depth. The modelled sample has 5,271 analyst-covered rows out of 19,402 labelled rows, about 27.2%. This is usable for the conservative coverage framing, but do not claim dense analyst coverage or a strong prediction-performance contribution.

4. Stress-label construction remains the most likely reviewer attack.
   The label is broad and accounting-based. Current-stress controls, onset-sample exclusion, conservative label-component controls, strict-label robustness, COVID exclusion, propensity checks, and firm/year fixed-effects LPM reduce this risk but do not remove it.

5. Causal language remains unsafe.
   The manuscript should say analyst coverage is associated with lower future stress probability and is consistent with an information-environment interpretation. It should not say analyst coverage reduces stress.

6. External validity is limited.
   The evidence is Singapore and Australia. Use "two Asia-Pacific markets" or "Singapore and Australia"; do not claim comprehensive APAC evidence.

7. Current market-cap fields are still excluded.
   Existing Capital IQ market-cap fields are current/no-date, transaction-context, or only a three-company dated schema proof with `NA` values. They should not be merged as historical predictors unless a full-sample, date-labelled, non-missing export is obtained.

8. Tooling/runtime can mislead if the wrong Python is used.
   System `python3` lacks `python-docx`, so individual package checks fail there. Use `/Users/guohuiwen/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` or the master script path.

## Decision

Apart from Chrome/Safari download access, the package is structurally sound and the core submission ladder checks pass. The non-technical blockers are unchanged: exact 70-80% single-journal evidence, final data-license confirmation, and strict claim discipline.
