# Analyst Coverage and Financial Stress Project

Date locked: 2026-06-01

## Locked Direction

Primary route:

**Analyst coverage, analyst information environment, and future financial stress in thinly covered APAC markets.**

The empirical base is now a deduplicated Singapore+ASX firm-year panel built from S&P Capital IQ accounting data and explicit FY+1 estimate snapshots.

This replaces the earlier "analyst disagreement predicts financial distress" route. Disagreement variables may appear as secondary tests only; they are not the paper's main claim.

## Journal Strategy

Strict user target:

**SCIE/SSCI indexed, Q3 level, stable 70-80% acceptance likelihood.**

Current status: the manuscript is submission-ready for a serious SCIE/SSCI empirical outlet and is compatible with a Q3-style applied-economics route. The exact strict target is **not yet achieved** because the verified lead outlet does not have a 70-80% acceptance signal. See `outputs/strict_scie_ssci_q3_70_80_feasibility_audit_20260601.md`.

Lead outlet under the user's regular Q3 constraint:

1. **Asia-Pacific Journal of Financial Studies**
   - Regular SSCI JCR Q3 Business, Finance outlet based on the current public JCR screen.
   - Official English-language journal of the Korean Securities Association.
   - Better fit than AEL for the user's "regular SSCI-level reputation" requirement.
   - Does not provide a 70-80% single-journal acceptance signal.

Transfer and fallback outlets:

2. **Economic Record**
   - Regular SSCI/JCR Q3 economics backup.
   - Best used after APJFS rejection without a fatal data objection, with the paper reframed around market information, Australia, and Asia-Pacific applied economics.
   - Visible acceptance-rate signal is 37%, not 70-80%.

3. **Applied Economics**
   - Probability-first full-article transfer option if Q2-or-better is acceptable.
   - Displayed acceptance signal is 40%, but it is not the strict Q3 substitute.

4. **Applied Economics Letters**
   - Short empirical-letter fallback.
   - Best suited to one clean result if the full-paper route fails or is abandoned.
   - Do not claim an AEL single-journal 70-80% acceptance probability.

Project-level SSCI Q3 strategy:

1. Use APJFS as the primary regular-Q3 finance version.
2. Use Economic Record as the clearest current regular SSCI/JCR Q3 economics transfer package.
3. Keep Applied Economics ready as a probability-first full-article backup if Q2-or-better is acceptable; do not present it as the strict Q3 solution.
4. Use AEL only as a compressed empirical-letter fallback if the full-paper route fails or is abandoned.
5. Treat APJAE as a lower-probability accounting/economics name to re-check later, not as the current packaged transfer route.
6. The 70-80% target is project-level after a sequential ladder, not a promise for one journal.

## Core Research Question

Does analyst coverage provide incremental information about one-year-ahead financial stress beyond accounting indicators in thinly covered APAC listed markets?

Secondary question:

Conditional on analyst coverage, do forecast-disagreement measures add robust incremental information?

## Claim Boundary

The paper may claim:

- analyst-covered firms have lower future financial-stress odds after accounting controls;
- this association is robust in Singapore, ASX, and the combined APAC panel;
- the result is consistent with analyst coverage proxying for the firm information environment;
- forecast disagreement has mixed and limited incremental evidence.

The paper must not claim:

- analyst disagreement alone robustly predicts distress;
- analyst coverage causally reduces financial stress;
- analyst variables deliver large prediction-performance gains;
- a trading strategy, AI system, LLM/RL method, or multimodal contribution;
- AEL alone provides 70-80% acceptance odds.
- the current package already proves the strict SCIE/SSCI Q3 70-80% target.

## Current Evidence Gate

Gate status: **PASSED for coverage framing; failed for disagreement framing.**

APAC combined sample:

- Markets: 2
- Firms: 2,335
- Firm-years: 21,737
- Labelled next-year stress observations: 19,402
- Stress events: 12,303
- Analyst-covered firm-years: 5,271
- Analyst-covered stress events: 1,816

Main APAC results:

- Logit accounting + market ROC AUC: 0.8851
- Logit accounting + market + analyst ROC AUC: 0.8913
- RF accounting + market ROC AUC: 0.9306
- RF accounting + market + analyst ROC AUC: 0.9299
- Fixed-effect logit with market and fiscal-year controls: `analyst_covered` coef = -0.5650, p < 0.001, odds ratio = 0.5684
- Fixed-effect conservative robustness excluding direct or near-direct label components: `analyst_covered` odds ratio = 0.5642, p < 0.001

Market split:

- Singapore: `analyst_covered` odds ratio = 0.5395, p = 8.23e-10.
- ASX: `analyst_covered` odds ratio = 0.6645, p = 4.50e-13.

## Manuscript Constraint

AEL version:

- Target main text: about 2,000 words.
- One main dependent variable: one-year-ahead broad financial stress.
- Main model: logit with accounting controls and market/country handling.
- Secondary checks: market-split robustness and random forest prediction.
- Disagreement variables discussed as conditional, mixed evidence.

Transfer version:

- Can include fuller tables, more robustness, and journal-specific framing.
- Can keep APAC two-market external-validity argument.
- Current Economic Record transfer package: `submission_package/economic_record_20260601/`.
- Current Applied Economics transfer package: `submission_package/applied_economics_20260601/`.

## Next Work

Do not expand to more markets now. The next work is upload discipline and transfer control:

1. Keep APJFS as the active upload package unless the user explicitly changes venue.
2. Keep Economic Record, Applied Economics, and AEL as sequential transfer/fallback packages only.
3. Re-run the master check before any portal upload.
4. Do not expand markets unless a reviewer or target journal explicitly requires it.
