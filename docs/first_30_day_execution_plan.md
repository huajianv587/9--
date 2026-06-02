<!-- SUPERSEDED 2026-06-01: Current route is analyst coverage / information environment. See docs/SUPERSEDED_BY_COVERAGE_ROUTE_20260601.md and docs/SSCI_Q3_transfer_ladder_coverage_route_20260601.md. -->

# First 30-Day Execution Plan

Objective: validate and build the SSCI Q3 stability-first paper:

**Analyst Disagreement and Financial Distress in Asia-Pacific Listed Firms.**

Lead journal after verification: **Applied Economics Letters**.

## Week 1: Capital IQ Feasibility Gates

- Build an event-led Capital IQ pilot for SGX, HKEx, and ASX.
- Include active and inactive/delisted firms.
- Export company status, distress events, delisting dates/reasons, defaults, restructuring/liquidation/receivership, and credit-rating history if available.
- Export a small accounting/market/analyst pilot to verify join keys.
- Manually audit at least 20 event cases for timing and distress-related reason.

Exit conditions:

- strict distress events >= 150 after realistic expansion, or broader stress events >= 300;
- analyst variables cover at least 30% of firm-periods and enough event cases;
- delisting reasons can distinguish distress from M&A, privatization, voluntary delisting, transfer, or administrative changes;
- no obvious timestamp leakage.

## Week 2: Firm-Quarter Panel

- Build the firm-quarter panel with accounting, market, analyst, and event tables.
- Create strict distress labels for 6-month, 12-month, and 24-month horizons.
- Create broader financial-stress labels only if strict events are insufficient.
- Validate missingness, duplicate keys, identifier drift, and class imbalance.
- Freeze market expansion if SGX/HKEx/ASX event count is insufficient.

Exit conditions:

- a leakage-safe modeling table exists;
- non-event controls greatly outnumber events without losing comparability;
- event labels and feature timestamps are auditable.

## Week 3: Baselines and Increment Tests

- Train logistic regression with accounting + market variables.
- Train XGBoost with accounting + market variables.
- Add analyst variables and measure incremental value.
- Report ROC-AUC, PR-AUC, balanced accuracy, distress-class F1, Brier score, and false-positive/false-negative rates.
- Use time-based train/test split; add market split if sample size allows.

Exit conditions:

- baseline performance is publishable or interpretable;
- analyst variables provide incremental value, or the null/boundary result is clean enough for a concise empirical letter.

## Week 4: SHAP, Robustness, and Manuscript Framing

- Produce SHAP summary and dependence plots for dispersion, revisions, coverage, leverage, liquidity, and returns.
- Run robustness checks: strict vs broader label, 6/12/24-month horizons, analyst coverage thresholds, excluding microcaps, financial vs non-financial.
- Decide final paper framing:
  - analyst disagreement as incremental early-warning signal; or
  - limited analyst value / accounting-market baseline dominance as a bounded empirical letter.
- Draft the Applied Economics Letters structure: introduction, data, method, main result, robustness, conclusion.

Exit conditions:

- final claim boundary is clear;
- table/figure list is frozen;
- no LLM/RL/neural method is needed for the first submission.
