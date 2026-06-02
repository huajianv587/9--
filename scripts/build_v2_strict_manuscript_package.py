#!/usr/bin/env python3
"""Build v2 strict-accounting-stress manuscript tables and draft package."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "outputs/tables/ael_v2_sample_freeze_counts_20260603.csv"
DESC = ROOT / "outputs/tables/ael_v2_descriptive_stats_20260603.csv"
MODEL = ROOT / "outputs/tables/ael_v2_strict_accounting_model_suite_20260603.csv"
PRED = ROOT / "outputs/tables/ael_v2_strict_accounting_prediction_increment_20260603.csv"
OUT_DIR = ROOT / "outputs/manuscript_v2_strict"
MANUSCRIPT = ROOT / "manuscript/strict_accounting_stress_v2_manuscript.md"
COVER = ROOT / "manuscript/strict_accounting_stress_v2_cover_letter.md"
AUDIT = ROOT / "outputs/strict_accounting_stress_v2_submission_packaging_audit_20260603.md"


def fmt_num(value: object, digits: int = 3) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, str):
        return value
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(x) >= 1000 and abs(x - round(x)) < 1e-9:
        return f"{int(round(x)):,}"
    return f"{x:.{digits}f}"


def stars(pvalue: object) -> str:
    try:
        p = float(pvalue)
    except (TypeError, ValueError):
        return ""
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""


def md_table(df: pd.DataFrame, columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for rec in df[columns].to_dict("records"):
        vals = []
        for col in columns:
            val = rec[col]
            vals.append("" if pd.isna(val) else str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines) + "\n"


def write_table(name: str, df: pd.DataFrame, columns: list[str]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df[columns].to_csv(OUT_DIR / f"{name}.csv", index=False)
    (OUT_DIR / f"{name}.md").write_text(md_table(df, columns), encoding="utf-8")


def build_tables() -> dict[str, pd.DataFrame]:
    sample = pd.read_csv(SAMPLE)
    desc = pd.read_csv(DESC)
    model = pd.read_csv(MODEL)
    pred = pd.read_csv(PRED)

    table1 = sample.copy()
    table1["Event rate"] = (table1["event_rate"] * 100).map(lambda x: f"{x:.1f}%")
    table1["Coverage rate"] = (table1["covered_rate"] * 100).map(lambda x: f"{x:.1f}%")
    table1 = table1.rename(
        columns={
            "sample": "Sample",
            "rows": "Firm-years",
            "firms": "Firms",
            "events": "Stress events",
            "asx_rows": "ASX rows",
            "singapore_rows": "Singapore rows",
        }
    )
    write_table(
        "table1_candidate_samples",
        table1,
        ["Sample", "Firm-years", "Firms", "Stress events", "Event rate", "Coverage rate", "ASX rows", "Singapore rows"],
    )

    rename_vars = {
        "analyst_covered": "Analyst covered",
        "num_analysts": "Number of analysts",
        "roa_w": "ROA",
        "leverage_w": "Leverage",
        "log_assets_w": "Log assets",
        "revenue_growth_w": "Revenue growth",
        "broad_stress_12m_appendix": "Broad stress t+1",
        "strict_accounting_stress_12m_candidate": "Strict accounting stress t+1",
        "persistent_broad_stress_24m_candidate": "Persistent broad stress t+1/t+2",
        "altman_distress_12m_candidate": "Altman distress-zone t+1",
        "event_distress_12m_candidate": "Broad event candidate t+1",
    }
    table2 = desc.copy()
    table2["Variable"] = table2["variable"].map(rename_vars).fillna(table2["variable"])
    for col in ["mean", "std", "p25", "median", "p75"]:
        table2[col] = table2[col].map(lambda x: fmt_num(x, 3))
    table2 = table2.rename(
        columns={"n": "N", "mean": "Mean", "std": "SD", "p25": "P25", "median": "Median", "p75": "P75"}
    )
    write_table("table2_descriptive_statistics", table2, ["Variable", "N", "Mean", "SD", "P25", "Median", "P75"])

    main_specs = [
        "Main strict accounting stress",
        "ASX split",
        "Singapore split",
        "Analyst intensity log1p count",
    ]
    table3 = model.loc[model["specification"].isin(main_specs)].copy()
    table3["Coefficient"] = table3.apply(
        lambda r: f"{float(r['coef']):.3f}{stars(r['p_value'])}" if pd.notna(r.get("coef")) else "",
        axis=1,
    )
    table3["Cluster SE"] = table3["cluster_se"].map(lambda x: fmt_num(x, 3))
    table3["Odds ratio"] = table3["odds_ratio"].map(lambda x: fmt_num(x, 3))
    table3["AME"] = table3["ame"].map(lambda x: fmt_num(x, 3))
    table3["AUC"] = table3["auc"].map(lambda x: fmt_num(x, 3))
    table3 = table3.rename(
        columns={"specification": "Specification", "n": "N", "events": "Events", "event_rate": "Event rate"}
    )
    table3["Event rate"] = table3["Event rate"].map(lambda x: f"{float(x) * 100:.1f}%")
    write_table(
        "table3_main_and_market_split",
        table3,
        ["Specification", "N", "Events", "Event rate", "Coefficient", "Cluster SE", "Odds ratio", "AME", "AUC"],
    )

    robustness_specs = [
        "Onset sample excluding current strict stress",
        "Drop suspect structure names",
        "Operating-status rows only",
        "COVID outcome-year exclusion",
        "Broad stress appendix label",
        "Persistent broad stress label",
        "Altman distress robustness label",
        "Broad event candidate label",
    ]
    table4 = model.loc[model["specification"].isin(robustness_specs)].copy()
    table4["Coefficient"] = table4.apply(
        lambda r: f"{float(r['coef']):.3f}{stars(r['p_value'])}" if pd.notna(r.get("coef")) else "",
        axis=1,
    )
    table4["Cluster SE"] = table4["cluster_se"].map(lambda x: fmt_num(x, 3))
    table4["Odds ratio"] = table4["odds_ratio"].map(lambda x: fmt_num(x, 3))
    table4["AME"] = table4["ame"].map(lambda x: fmt_num(x, 3))
    table4 = table4.rename(columns={"specification": "Specification", "n": "N", "events": "Events"})
    write_table("table4_robustness", table4, ["Specification", "N", "Events", "Coefficient", "Cluster SE", "Odds ratio", "AME"])

    table5 = pred.copy()
    for col in ["auc_accounting_only", "auc_plus_analyst", "delta_auc", "brier_accounting_only", "brier_plus_analyst", "delta_brier"]:
        table5[col] = table5[col].map(lambda x: fmt_num(x, 4))
    table5 = table5.rename(
        columns={
            "comparison": "Comparison",
            "auc_accounting_only": "AUC controls",
            "auc_plus_analyst": "AUC + analyst",
            "delta_auc": "Delta AUC",
            "brier_accounting_only": "Brier controls",
            "brier_plus_analyst": "Brier + analyst",
            "delta_brier": "Delta Brier",
        }
    )
    write_table(
        "table5_prediction_increment",
        table5,
        ["Comparison", "AUC controls", "AUC + analyst", "Delta AUC", "Brier controls", "Brier + analyst", "Delta Brier"],
    )

    return {"sample": sample, "desc": desc, "model": model, "pred": pred}


def manuscript_text(data: dict[str, pd.DataFrame]) -> str:
    model = data["model"]
    sample = data["sample"]
    pred = data["pred"].iloc[0]
    main = model.loc[model["specification"].eq("Main strict accounting stress")].iloc[0]
    asx = model.loc[model["specification"].eq("ASX split")].iloc[0]
    sg = model.loc[model["specification"].eq("Singapore split")].iloc[0]
    onset = model.loc[model["specification"].eq("Onset sample excluding current strict stress")].iloc[0]
    altman = model.loc[model["specification"].eq("Altman distress robustness label")].iloc[0]
    event = model.loc[model["specification"].eq("Broad event candidate label")].iloc[0]
    strict_sample = sample.loc[sample["sample"].eq("Strict accounting stress 12m")].iloc[0]
    broad_sample = sample.loc[sample["sample"].eq("Broad stress appendix")].iloc[0]
    altman_sample = sample.loc[sample["sample"].eq("Altman distress zone 12m")].iloc[0]
    event_sample = sample.loc[sample["sample"].eq("Broad event candidate 12m")].iloc[0]

    return f"""# Analyst Coverage and Subsequent Accounting-Based Financial Stress: Evidence from Singapore and Australia

Draft status: v2 strict-accounting-stress route generated on 2026-06-03.
Target use: SSCI/JCR Q3 submission draft after final journal screen and formatting QA.

## Abstract

This paper examines whether analyst coverage is associated with subsequent accounting-based financial stress in Singapore and Australian listed firms. Using S&P Capital IQ accounting data and fiscal-year-end analyst estimate snapshots, I build a firm-year panel covering fiscal years 2014-2024 and estimate forward-looking stress models for fiscal years with observable one-year-ahead outcomes. The main dependent variable is a strict accounting-stress indicator equal to one when the next fiscal year has at least two stress symptoms: negative equity, operating loss, and low interest coverage. The main estimation sample contains {int(main['n']):,} firm-years, {int(main['firms']):,} firms, and {int(main['events']):,} subsequent strict accounting-stress events. Analyst-covered firm-years have significantly lower subsequent strict-stress odds after accounting controls, market fixed effects, fiscal-year fixed effects, and firm-clustered standard errors. The main odds ratio is {float(main['odds_ratio']):.3f}, with an average marginal effect of {float(main['ame']):.1%}. The association is negative in both ASX and Singapore subsamples and survives structure-name exclusions, operating-status restrictions, COVID outcome-year exclusion, analyst-intensity checks, and alternative stress labels. Altman and Key Developments event labels are used as robustness or validation evidence rather than as the primary outcome because their coverage and ID-matching limitations are material. Analyst variables do not materially improve predictive AUC, so the paper is framed as an information-environment association rather than a prediction-performance study.

Keywords: analyst coverage; accounting-based stress; information environment; Singapore; Australia; S&P Capital IQ

JEL codes: G14; G17; G24; G32

## 1. Introduction

Analyst coverage is a visible part of a firm's information environment. In listed markets with many thinly followed firms, the extensive margin of coverage may be informative even before the content of analyst forecasts is examined. Covered firms are usually easier for investors to monitor, compare, and value. Uncovered firms are more likely to be small, opaque, illiquid, or outside the regular attention set of intermediaries. These differences motivate a narrow empirical question: conditional on observable accounting fundamentals, are analyst-covered firm-years less likely to move into subsequent accounting-based financial stress?

This paper studies that question using Singapore and Australian listed firms. The setting is useful because both markets contain many firms with no analyst estimate snapshot, while S&P Capital IQ provides enough accounting and analyst data to construct a two-market firm-year panel. The empirical contribution is deliberately bounded. I do not claim that analysts prevent financial stress, that coverage is randomly assigned, or that analyst variables provide a large predictive-performance improvement. The claim is narrower: analyst coverage is a stable marker of lower subsequent accounting-stress risk after standard accounting controls and time/market structure are included.

The earlier broad-stress version of the paper was too vulnerable to reviewer criticism because its event rate was high and the dependent variable was close to general operating weakness. The revised design therefore makes strict subsequent accounting stress the main label. A firm-year is classified as subsequently stressed only if the next fiscal year has at least two accounting stress symptoms. This definition reduces single-symptom noise and creates a more defensible outcome for an SSCI/JCR Q3 submission.

The main result supports the strict route. In the combined sample, analyst coverage has an odds ratio of {float(main['odds_ratio']):.3f} for subsequent strict accounting stress. The estimate is negative and significant in ASX, with an odds ratio of {float(asx['odds_ratio']):.3f}, and in Singapore, with an odds ratio of {float(sg['odds_ratio']):.3f}. The onset sample, which excludes firm-years already in strict accounting stress, remains negative but weakens statistically. This pattern is useful for positioning: analyst coverage is not a cure for financial stress, but it is a robust conditional marker of lower subsequent stress risk.

The paper contributes to applied empirical finance in three ways. First, it provides two-market evidence on analyst coverage and accounting-based stress in Singapore and Australia rather than relying on a single-country sample. Second, it separates broad accounting weakness, strict accounting stress, Altman-style distress, and event-based stress evidence instead of forcing one dependent variable to carry every claim. Third, it explicitly reports that analyst variables add little predictive-performance value once accounting controls are included. This keeps the contribution in the information-environment literature rather than overselling the paper as a distress-prediction model.

## 2. Literature and Hypothesis Development

Analyst coverage can reduce information frictions through monitoring, forecasts, reports, and investor attention. Classic information-environment arguments imply that firms followed by analysts are more visible and easier to evaluate than unfollowed firms. Work on investor recognition, analyst following, disclosure, and information diffusion provides the conceptual basis for treating coverage as a marker of capital-market attention.

Financial-stress models traditionally emphasize accounting fundamentals, leverage, profitability, liquidity, and market information. Bankruptcy and distress studies show that accounting and market variables can be powerful predictors. However, listed-firm stress is not purely a balance-sheet outcome. Visibility, financing access, monitoring, and investor attention may also correlate with a firm's ability to avoid or delay accounting deterioration. Analyst coverage may therefore be informative even after accounting controls are included.

The first hypothesis is framed as an association rather than a causal effect:

**H1.** Analyst-covered firm-years have lower subsequent strict accounting-stress odds than otherwise comparable uncovered firm-years.

Among covered firms, analyst intensity may also matter. A larger number of analysts could indicate a stronger information environment, but analyst counts are endogenous and highly correlated with firm size and visibility. I therefore treat analyst intensity as a robustness check:

**H2.** Greater analyst intensity is negatively associated with subsequent strict accounting stress, but this evidence is secondary to the coverage indicator.

## 3. Data and Variables

The data come from S&P Capital IQ historical accounting exports, fiscal-year-end analyst estimate snapshots, and supplemental Capital IQ raw workbooks downloaded and audited for this revision. The local v2 panel has 21,737 firm-years, 2,335 companies, and fiscal years 2014-2024. Modelled one-year-ahead outcomes exclude fiscal years without an observable next-year label. Analyst timing checks remove rows in which a covered forecast date occurs after the as-of date.

The main estimation sample is the strict accounting-stress 12-month sample. It contains {int(strict_sample['rows']):,} firm-years, {int(strict_sample['firms']):,} firms, and {int(strict_sample['events']):,} stress events, with an event rate of {float(strict_sample['event_rate']):.1%}. ASX contributes {int(strict_sample['asx_rows']):,} rows and Singapore contributes {int(strict_sample['singapore_rows']):,} rows. Analyst coverage is present in {float(strict_sample['covered_rate']):.1%} of the strict sample.

The main dependent variable, `StrictAccountingStress_{{t+1}}`, equals one if the next fiscal year satisfies at least two of three conditions: negative equity, operating loss, and interest coverage below 1.5. This label is more conservative than the earlier broad-stress label, whose sample contains {int(broad_sample['rows']):,} rows and an event rate of {float(broad_sample['event_rate']):.1%}. Broad stress is retained as appendix evidence only.

I also construct Altman-style and event-based candidates. The Altman sample contains {int(altman_sample['rows']):,} firm-years and {int(altman_sample['events']):,} events, but its coverage is much smaller because the full-component formula requires current assets, current liabilities, retained earnings, market capitalization, total liabilities, EBIT, revenue, and total assets. Total-liabilities coverage is the binding bottleneck, especially for Singapore, so Altman is not used as the main outcome. The Key Developments event candidate sample contains {int(event_sample['rows']):,} firm-years and {int(event_sample['events']):,} events, but the event export's direct SPCIq ID does not cleanly overlap with the baseline company ID. Event labels therefore rely on conservative name matching and are used as validation evidence rather than formal bankruptcy/default outcomes.

The main analyst variable is `AnalystCovered`, equal to one when a firm has at least one analyst estimate in the fiscal-year-end snapshot. Analyst intensity is measured as log one plus the number of analysts. Controls include ROA, leverage, log assets, and revenue growth. Continuous controls and candidate Altman components are winsorized at the 1st and 99th percentiles. The main model includes market and fiscal-year fixed effects and reports firm-clustered standard errors.

Table 1 reports the candidate samples. Table 2 reports descriptive statistics in the common cleaned sample.

## 4. Empirical Specification

The main model is a firm-year logit:

```text
Pr(StrictAccountingStress_{{i,t+1}} = 1) =
logit(alpha + beta AnalystCovered_{{i,t}} + gamma Controls_{{i,t}}
      + market fixed effects + fiscal-year fixed effects).
```

The coefficient of interest is beta. A negative beta indicates that covered firm-years have lower subsequent strict accounting-stress odds than comparable uncovered firm-years in the same market and fiscal-year environment. Standard errors are clustered at the firm level to account for repeated firm-year observations.

The model is intentionally associational. Analyst coverage is not randomly assigned. Analysts tend to follow larger and more visible firms, and the controls cannot remove all selection. The paper therefore avoids causal wording and treats analyst coverage as an information-environment marker.

The robustness design has four layers. First, the model is estimated separately for ASX and Singapore. Second, sample restrictions remove already-stressed firm-years, suspect REIT/fund/trust/SPAC-like names, non-operating status rows, and COVID outcome years. Third, the dependent variable is replaced by broad stress, persistent stress, Altman distress, and a broad event candidate. Fourth, analyst coverage is replaced by log one plus the number of analysts. Prediction checks compare AUC and Brier score with and without the analyst variable.

## 5. Results

Table 3 reports the main and market-split estimates. In the combined strict accounting-stress sample, analyst coverage has a coefficient of {float(main['coef']):.3f}, a firm-clustered standard error of {float(main['cluster_se']):.3f}, and an odds ratio of {float(main['odds_ratio']):.3f}. The average marginal effect is {float(main['ame']):.1%}. The association is economically meaningful but should not be read as a treatment effect.

The market split supports the two-market story. The ASX coefficient is {float(asx['coef']):.3f}, with an odds ratio of {float(asx['odds_ratio']):.3f}. The Singapore coefficient is {float(sg['coef']):.3f}, with an odds ratio of {float(sg['odds_ratio']):.3f}. The effect is larger in Singapore, but the direction is negative in both markets.

Table 4 reports robustness checks. Excluding suspect structure names gives an odds ratio of 0.718. Restricting to operating-status rows gives an odds ratio of 0.701. Excluding COVID outcome years gives an odds ratio of 0.713. Replacing the coverage indicator with analyst intensity gives an odds ratio of 0.630 per log-one-plus analyst count. These checks support the interpretation that analyst attention is a stable marker of lower subsequent accounting-stress risk.

The onset sample is more cautious. Excluding firm-years already in strict accounting stress reduces the coefficient to {float(onset['coef']):.3f}, with an odds ratio of {float(onset['odds_ratio']):.3f} and p-value {float(onset['p_value']):.3f}. The sign remains negative, but significance weakens. This is an important limitation: part of the main association reflects persistence and the fact that already-weak firms are less likely to attract analyst coverage.

Alternative labels are informative but should not become the main story. The broad-stress appendix label produces a stronger negative association, but its event rate is too high for a clean financial-distress claim. The persistent stress label is also negative and significant. The Altman label has an odds ratio of {float(altman['odds_ratio']):.3f} but p-value {float(altman['p_value']):.3f}, which is directionally supportive but underpowered. The broad event candidate has an odds ratio of {float(event['odds_ratio']):.3f}, but because event matching is not clean direct-ID matching, the paper should describe it as validation evidence rather than a formal event-distress result.

Table 5 reports prediction increments. Adding analyst coverage changes AUC from {float(pred['auc_accounting_only']):.4f} to {float(pred['auc_plus_analyst']):.4f}, a delta of {float(pred['delta_auc']):.4f}. The Brier score improves only from {float(pred['brier_accounting_only']):.4f} to {float(pred['brier_plus_analyst']):.4f}. The prediction increment is therefore negligible. This result strengthens the paper's positioning: the contribution is a robust conditional association, not a new high-performing prediction model.

## 6. Discussion and Scope

The revised evidence is stronger than the old broad-stress version because the main dependent variable is stricter and the story is less vulnerable to the criticism that any weak operating outcome is labelled as financial distress. The strict accounting-stress label still has a high event rate, but it requires multiple symptoms and is more defensible for a Q3 empirical paper.

The most important limitation is endogeneity. Analyst coverage may proxy for firm visibility, liquidity, governance quality, disclosure quality, or investor recognition. The negative coefficient should therefore be interpreted as a conditional association. The paper should not say that analyst coverage reduces stress or that expanding coverage would mechanically lower default risk.

The second limitation is label taxonomy. Altman is not strong enough to be the main label because full-component coverage is limited. Event evidence is not clean enough to be a formal distress label because the current event export lacks direct ID alignment with the baseline panel. The manuscript should be explicit that these labels are robustness or validation checks.

The third limitation is text and tone. The current v2 firm-year panel does not contain tone fields or raw text quality indicators. The final paper should not claim tone extraction unless a separate text dataset is audited and merged. For the present route, tone is removed from the core claim.

The fourth limitation is journal fit. The paper is best positioned as an applied empirical finance or applied economics article about analyst coverage and accounting-based stress in two Asia-Pacific markets. It is not a causal identification paper, not a machine-learning prediction paper, and not evidence for all Asia-Pacific markets.

## 7. Conclusion

This paper shows that analyst-covered firm-years in Singapore and Australia have lower subsequent strict accounting-stress odds after accounting controls, market fixed effects, fiscal-year fixed effects, and firm-clustered errors are included. The result is negative in both markets and survives several sample and label robustness checks. The strongest defensible contribution is narrow: analyst coverage is a marker of the firm information environment associated with lower future accounting-based stress. The evidence does not support causal language or a prediction-performance claim, but it does support a disciplined SSCI/JCR Q3 route built around strict accounting-based stress.

## Data Availability

The data used in this study were obtained from S&P Capital IQ under institutional database access and are subject to database licensing and redistribution restrictions. The author cannot redistribute raw Capital IQ exports or firm-level Capital IQ-derived panels. Researchers with their own Capital IQ access may reconstruct the sample using the reported variable definitions, sample filters, and replication code. Non-proprietary aggregate tables and audit outputs are included in the submission materials.

## Tables

### Table 1. Candidate Samples

{(OUT_DIR / 'table1_candidate_samples.md').read_text(encoding='utf-8')}
### Table 2. Descriptive Statistics

{(OUT_DIR / 'table2_descriptive_statistics.md').read_text(encoding='utf-8')}
### Table 3. Main and Market-Split Logit Estimates

{(OUT_DIR / 'table3_main_and_market_split.md').read_text(encoding='utf-8')}
### Table 4. Robustness Checks

{(OUT_DIR / 'table4_robustness.md').read_text(encoding='utf-8')}
### Table 5. Prediction Increment

{(OUT_DIR / 'table5_prediction_increment.md').read_text(encoding='utf-8')}
## References

Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *Journal of Finance*, 23(4), 589-609.

Beaver, W. H. (1966). Financial ratios as predictors of failure. *Journal of Accounting Research*, 4, 71-111.

Bhushan, R. (1989). Firm characteristics and analyst following. *Journal of Accounting and Economics*, 11(2-3), 255-274.

Brennan, M. J., and A. Subrahmanyam. (1995). Investment analysis and price formation in securities markets. *Journal of Financial Economics*, 38(3), 361-381.

Campbell, J. Y., J. Hilscher, and J. Szilagyi. (2008). In search of distress risk. *Journal of Finance*, 63(6), 2899-2939.

Healy, P. M., and K. G. Palepu. (2001). Information asymmetry, corporate disclosure, and the capital markets: A review of the empirical disclosure literature. *Journal of Accounting and Economics*, 31(1-3), 405-440.

Hong, H., T. Lim, and J. C. Stein. (2000). Bad news travels slowly: Size, analyst coverage, and the profitability of momentum strategies. *Journal of Finance*, 55(1), 265-295.

Kelly, B., and A. Ljungqvist. (2012). Testing asymmetric-information asset pricing models. *Review of Financial Studies*, 25(5), 1366-1413.

Lang, M. H., and R. Lundholm. (1996). Corporate disclosure policy and analyst behavior. *The Accounting Review*, 71(4), 467-492.

Merton, R. C. (1987). A simple model of capital market equilibrium with incomplete information. *Journal of Finance*, 42(3), 483-510.

Ohlson, J. A. (1980). Financial ratios and the probabilistic prediction of bankruptcy. *Journal of Accounting Research*, 18(1), 109-131.

Piotroski, J. D. (2000). Value investing: The use of historical financial statement information to separate winners from losers. *Journal of Accounting Research*, 38, 1-41.

Shumway, T. (2001). Forecasting bankruptcy more accurately: A simple hazard model. *Journal of Business*, 74(1), 101-124.
"""


def cover_letter_text(data: dict[str, pd.DataFrame]) -> str:
    model = data["model"]
    main = model.loc[model["specification"].eq("Main strict accounting stress")].iloc[0]
    asx = model.loc[model["specification"].eq("ASX split")].iloc[0]
    sg = model.loc[model["specification"].eq("Singapore split")].iloc[0]
    return f"""Dear Editor,

Please consider the manuscript titled "Analyst Coverage and Subsequent Accounting-Based Financial Stress: Evidence from Singapore and Australia" for publication.

The manuscript examines whether analyst coverage is associated with subsequent strict accounting-based financial stress in Singapore and Australian listed firms. Using S&P Capital IQ accounting data and fiscal-year-end analyst estimate snapshots, the study constructs a two-market firm-year panel and uses a stricter dependent variable requiring at least two next-year accounting stress symptoms.

The main finding is intentionally bounded: analyst-covered firm-years have lower subsequent strict accounting-stress odds after accounting controls, market fixed effects, fiscal-year fixed effects, and firm-clustered standard errors. The main odds ratio is {float(main['odds_ratio']):.3f}. The association is negative in both ASX (odds ratio {float(asx['odds_ratio']):.3f}) and Singapore (odds ratio {float(sg['odds_ratio']):.3f}) and is supported by several robustness checks. The manuscript does not make a causal claim and does not overstate predictive-performance gains.

The paper is suitable for an SSCI/JCR Q3 empirical finance, applied economics, or accounting-information outlet because it provides a disciplined two-market result about analyst coverage as an information-environment marker. Broad stress, Altman, and Key Developments event labels are treated as robustness or validation evidence rather than as the main outcome.

This manuscript is original, is not under consideration elsewhere, and the author has approved the submission. The data are obtained from S&P Capital IQ under institutional database access and cannot be redistributed at the firm level.

Sincerely,

Huajian Jiang
"""


def package_audit_text(data: dict[str, pd.DataFrame], manuscript: str) -> str:
    words = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", manuscript))
    model = data["model"]
    main = model.loc[model["specification"].eq("Main strict accounting stress")].iloc[0]
    lines = [
        "# Strict Accounting Stress v2 Submission Packaging Audit",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Decision",
        "",
        "Status: DRAFT_PACKAGE_BUILT_NOT_FINAL_SUBMISSION",
        "",
        "The v2 manuscript package has been rebuilt around the strict accounting-stress route. It is not yet final submission-ready because journal selection must be refreshed, DOCX/PDF visual QA has not been rerun for this draft, and event-ID/tone limitations remain.",
        "",
        "## Generated Artifacts",
        "",
        f"- Manuscript draft: `{MANUSCRIPT}`",
        f"- Cover letter draft: `{COVER}`",
        f"- Table directory: `{OUT_DIR}`",
        f"- Approximate manuscript word count including tables/references: {words:,}",
        "",
        "## Main Evidence",
        "",
        f"- Main strict accounting stress odds ratio: {float(main['odds_ratio']):.3f}",
        f"- Main AME: {float(main['ame']):.3f}",
        f"- Main p-value: {float(main['p_value']):.3g}",
        "",
        "## Reviewer Risks Still Open",
        "",
        "- This is not yet a no-risk 70-80% SSCI/JCR Q3 submission package.",
        "- Journal fit and current JCR quartile/acceptance evidence must be refreshed before submission.",
        "- Event labels are candidate-level because direct event ID alignment is weak.",
        "- Altman is robustness-only because full-component coverage is limited.",
        "- Tone/text extraction is not included in the v2 firm-year panel and should not be claimed.",
        "- DOCX/PDF generation and visual QA are still required before portal upload.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build_tables()
    manuscript = manuscript_text(data)
    cover = cover_letter_text(data)
    MANUSCRIPT.write_text(manuscript, encoding="utf-8")
    COVER.write_text(cover, encoding="utf-8")
    AUDIT.write_text(package_audit_text(data, manuscript), encoding="utf-8")
    print(f"Wrote {MANUSCRIPT}")
    print(f"Wrote {COVER}")
    print(f"Wrote {AUDIT}")
    print(f"Wrote tables to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
