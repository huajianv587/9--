<!-- SUPERSEDED 2026-06-01: Current route is analyst coverage / information environment. See docs/SUPERSEDED_BY_COVERAGE_ROUTE_20260601.md and docs/SSCI_Q3_transfer_ladder_coverage_route_20260601.md. -->

# Reviewer Assessment of the AEL Strategy

Date: 2026-05-31

## Overall Verdict

The revised strategy is now defensible for a stability-first SSCI Q3 plan:

**Applied Economics Letters first, with an analyst-disagreement and financial-stress letter.**

The route is not defensible if written as a large AI/ML paper. It is defensible if
written as a concise applied-economics result using institutional data.

## What AEL Reviewers Are Likely to Accept

A short paper with:

- one clear applied question;
- one clean dependent variable;
- transparent logit/probit/discrete-time hazard estimates;
- a meaningful coefficient or marginal effect;
- concise robustness checks;
- no excessive theory, no inflated novelty, no method spectacle.

The core manuscript should say:

> Analyst forecast dispersion predicts future financial stress in Asia-Pacific listed firms, beyond accounting and market indicators.

## Main Reviewer Risks

### 1. The paper may look like a machine-learning exercise

Risk:

If XGBoost and SHAP dominate the paper, AEL editors may see it as too technical,
too long, or not a standard applied-economics contribution.

Fix:

- Main result = logit marginal effect.
- XGBoost = one incremental prediction row/table.
- SHAP = supplement unless needed for one compact figure.

### 2. The distress label may be too noisy

Risk:

If "distress" includes ordinary delistings, M&A, privatization, or listing
transfers, the paper can be rejected for label contamination.

Fix:

- Use financial stress as the main label if strict events are sparse.
- Use strict distress as robustness.
- Audit delisting reason manually.

### 3. The analyst sample may be selected

Risk:

Analyst-covered firms are larger and more liquid, so the result may reflect firm
selection rather than analyst information.

Fix:

- Report analyst-covered vs non-covered sample statistics.
- Include size, liquidity, market cap, sector, country, and time controls.
- Run coverage >= 2 and >= 3 robustness.

### 4. The paper may be too broad for 2,000 words

Risk:

Too many markets, hypotheses, models, and robustness checks will make the letter
unreadable.

Fix:

- Keep two hypotheses.
- Keep three main tables.
- Put market heterogeneity, SHAP, and alternative horizons in supplement.

## Required AEL Manuscript Design

### Title

Use:

**Analyst Disagreement and Financial Stress in Asia-Pacific Listed Firms**

Avoid:

- "machine learning";
- "XGBoost";
- "multimodal";
- "framework";
- "AI".

### Main Tables

1. Sample and stress-event distribution.
2. Main logit / marginal-effects estimates.
3. Incremental prediction and robustness.

### Main Tests

- Baseline accounting + market model.
- Baseline + analyst dispersion.
- Baseline + analyst dispersion + revisions/coverage, only if space allows.
- XGBoost incremental prediction, summarized compactly.

## Go / No-Go Standard

Proceed to AEL if:

- analyst dispersion is positive and stable;
- incremental model improves PR-AUC, ROC-AUC, or calibration;
- strict or alternative label robustness does not overturn the result;
- the main story fits within a short letter.

Do not submit to AEL if:

- analyst variables have unstable signs;
- stress labels cannot be audited;
- the only positive result is from a black-box model;
- the paper needs a long methodological defense to make sense.

## Reviewer Recommendation

Proceed with the AEL-specific plan.

The next execution step is not modeling. It is Capital IQ data validation:

1. event/stress count;
2. analyst coverage;
3. leakage audit;
4. delisting reason audit.
