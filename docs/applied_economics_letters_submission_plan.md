<!-- SUPERSEDED 2026-06-01: Current route is analyst coverage / information environment. See docs/SUPERSEDED_BY_COVERAGE_ROUTE_20260601.md and docs/SSCI_Q3_transfer_ladder_coverage_route_20260601.md. -->

# Applied Economics Letters Targeted Submission Plan

Date: 2026-05-31

## Target Journal

**Applied Economics Letters**

Verified fit:

- 2024 JCR: SSCI.
- 2024 JCR category: Economics.
- 2024 JIF quartile: Q3.
- 2024 JIF: 1.3.
- Taylor & Francis official acceptance rate: 35%.
- Scope: short research and discussion letters in applied economic analysis, including financial economics.

Planning constraint:

- Treat the manuscript as a short empirical letter.
- Conservative working limit: **<= 2,000 words all-in** for the main manuscript. A recent Applied Economics Letters article explicitly refers to a strict 2,000-word manuscript limit; verify the current submission portal before final upload.
- Use online supplementary material for extended robustness, definitions, and extra tables.

## AEL-Specific Framing

Do not write this as:

> A machine-learning bankruptcy prediction system for Asia-Pacific firms.

Write it as:

> Analyst disagreement predicts future financial stress among Asia-Pacific listed firms, even after controlling for accounting and market indicators.

The contribution must be one clean empirical result:

1. Analyst forecast dispersion/revisions have early-warning content.
2. The result holds in Asia-Pacific listed firms where analyst coverage and information environments vary.
3. Capital IQ Estimates allow a cleaner analyst-signal test than public-only datasets.

## Working Title

Preferred title:

**Analyst Disagreement and Financial Stress in Asia-Pacific Listed Firms**

Alternative if strict distress events are strong:

**Analyst Forecast Dispersion and Corporate Distress in Asia-Pacific Markets**

Avoid:

- "XGBoost"
- "AI"
- "machine learning"
- "multimodal"
- "prediction framework"

These can appear in the method/robustness section only if needed.

## Research Question

Does analyst forecast disagreement predict future financial stress or distress in Asia-Pacific listed firms beyond standard accounting and market indicators?

## Main Hypothesis Set

Keep only two hypotheses in the main manuscript:

- H1: Higher analyst forecast dispersion is associated with higher future financial stress/distress risk.
- H2: Analyst variables add incremental information beyond accounting and market predictors.

Move revisions, coverage decline, and cross-market heterogeneity to robustness or supplement unless they are the strongest empirical result.

## Main Model for AEL

Primary model:

```text
Pr(Stress_{i,t+h}=1) =
logit(alpha + beta*AnalystDispersion_{i,t}
      + gamma*Accounting_{i,t}
      + delta*Market_{i,t}
      + country FE + sector FE + time FE)
```

Preferred horizon:

- h = 4 quarters / 12 months.

Why:

- It is transparent to applied economics reviewers.
- It fits a short letter better than an ML-heavy model.
- It makes coefficient direction and economic meaning easy to state.

Secondary model:

- XGBoost only for incremental prediction evidence.
- SHAP only as compact explanation or supplementary material.
- LightGBM only if XGBoost is unstable; do not make it a separate contribution.

## Data Design

Initial sample:

- SGX, HKEx, ASX listed firms.
- 2014-2024 preferred; 2016-2024 minimum.
- Firm-quarter panel if feasible.

Minimum viable paper:

- At least 300 broader financial-stress events, or 150 clean strict-distress events.
- Analyst variables for at least 30% of firm-periods.
- Analyst-covered sample includes enough stress/distress events to estimate the main model.

Preferred dependent variable for AEL:

- **Financial stress within the next 12 months** as the main label, if strict distress is too sparse.

Strict distress should be used as robustness:

- bankruptcy;
- debt default;
- restructuring / receivership / liquidation;
- distress-related delisting;
- severe credit downgrade if coverage is sufficient.

Why this is AEL-friendly:

- AEL needs one clean result, not a complex event taxonomy.
- Broader financial stress improves statistical power.
- Strict distress robustness protects against label looseness.

## Main Manuscript Structure

Target: 1,800-2,000 words.

| Section | Target words | Job |
|---|---:|---|
| Abstract | 100-120 | State data, method, one result, implication. |
| 1. Introduction | 350-450 | One paragraph problem, one paragraph contribution, one paragraph result. |
| 2. Data and variables | 350-450 | Sample, stress label, analyst disagreement, controls. |
| 3. Method | 200-250 | Logit specification and prediction comparison. |
| 4. Results | 500-650 | Main coefficient, marginal effect, incremental prediction, robustness summary. |
| 5. Conclusion | 150-200 | One implication and one limitation. |

No full literature review. Use only essential citations.

## Main Tables and Figures

Main text:

1. **Table 1: Sample and financial stress distribution**
   - firms, firm-quarters, stress events, analyst-covered observations by market.

2. **Table 2: Main logit results**
   - accounting + market baseline;
   - baseline + analyst dispersion;
   - baseline + dispersion + revisions/coverage if space allows.

3. **Table 3: Incremental prediction and robustness**
   - ROC-AUC;
   - PR-AUC;
   - Brier score;
   - strict distress robustness;
   - analyst coverage >= 2 / >= 3.

Optional one figure only:

- coefficient/marginal-effect plot for analyst dispersion.

Supplement:

- variable definitions;
- sample construction;
- detailed robustness tables;
- SHAP plot if XGBoost is included;
- market-specific estimates;
- microcap exclusion;
- 6/24-month horizons.

## Results Needed to Submit

Green-light result:

- analyst dispersion coefficient positive and statistically meaningful; and
- analyst block improves PR-AUC, ROC-AUC, or calibration; and
- effect survives at least one strict robustness check.

Yellow-light result:

- coefficient positive but weak; prediction improvement appears only in analyst-covered or high-coverage subsample.
- Submit only if framed as "limited but economically relevant early-warning information."

Red-light result:

- analyst variables are directionally unstable or become irrelevant after accounting/market controls.
- Do not submit to AEL in the current framing. Reframe to accounting/market stress prediction or return to earnings-surprise backup.

## Cover Letter Angle

Core pitch:

> This letter provides new Asia-Pacific evidence that analyst forecast disagreement contains early-warning information about corporate financial stress. Using S&P Capital IQ Estimates matched to firm-quarter accounting and market data, the paper shows that analyst dispersion improves stress prediction beyond conventional financial ratios and market signals.

Avoid mentioning:

- GPU training;
- LLM fine-tuning;
- broad AI framework;
- 70-80% target probability.

## Execution Changes From the Generic Plan

- Main paper becomes a short empirical economics letter, not a full finance/AI article.
- Logit / marginal effects become the main result.
- XGBoost becomes secondary evidence.
- SHAP moves to supplement unless it is very compact.
- Literature review is cut to only essential distress and analyst-disagreement citations.
- All nonessential heterogeneity tests move to supplement.
