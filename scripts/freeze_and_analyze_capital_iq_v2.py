#!/usr/bin/env python3
"""Freeze candidate samples and run preliminary v2 analyses.

The output panel is local/licensed-data-derived and should not be committed.
The Markdown/CSV summaries are aggregate audit artifacts.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from math import erfc, sqrt
from pathlib import Path
import re
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PANEL = ROOT / "data/processed/ael_apac_firm_year_panel_v2_capital_iq_20260603.csv"
OUT_PANEL = ROOT / "data/processed/ael_apac_firm_year_panel_v2_frozen_candidate_20260603.csv"
OUT_AUDIT = ROOT / "outputs/ael_apac_v2_sample_freeze_cleaning_audit_20260603.md"
OUT_SAMPLE_COUNTS = ROOT / "outputs/tables/ael_v2_sample_freeze_counts_20260603.csv"
OUT_MODEL = ROOT / "outputs/tables/ael_v2_preliminary_logit_20260603.csv"
OUT_DESC = ROOT / "outputs/tables/ael_v2_descriptive_stats_20260603.csv"

CONTROLS = ["roa", "leverage", "log_assets", "revenue_growth"]
EXTRA_CONTROLS = ["roe", "interest_coverage", "operating_margin"]
WINSOR_VARS = [
    "roa",
    "roe",
    "leverage",
    "interest_coverage",
    "operating_margin",
    "revenue_growth",
    "log_assets",
    "altman_z_ciq_candidate",
    "altman_x1_working_capital_assets_ciq",
    "altman_x2_retained_earnings_assets_ciq",
    "altman_x3_ebit_assets_ciq",
    "altman_x4_market_value_liabilities_ciq",
    "altman_x5_sales_assets_ciq",
    "market_cap_ciq_usd_m",
]
STRUCTURE_RE = re.compile(
    r"\b(?:REIT|fund|ETF|trust|stapled|SPAC|acquisition corp|investment company|investment trust)\b",
    flags=re.I,
)


def load_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    panel = pd.read_csv(path, low_memory=False)
    panel["company_id"] = pd.to_numeric(panel["company_id"], errors="coerce").astype("Int64")
    panel["fiscal_year"] = pd.to_numeric(panel["fiscal_year"], errors="coerce").astype("Int64")
    panel = panel.loc[panel["company_id"].notna() & panel["fiscal_year"].notna()].copy()
    panel["company_id"] = panel["company_id"].astype(int)
    panel["fiscal_year"] = panel["fiscal_year"].astype(int)
    panel = panel.sort_values(["company_id", "fiscal_year"]).reset_index(drop=True)
    return panel


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)


def add_labels(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.copy()
    components = ["negative_equity", "operating_loss", "interest_coverage_below_1_5"]
    for col in components + ["financial_stress_current", "stress_12m", "altman_distress_zone_ciq_candidate"]:
        if col in panel.columns:
            panel[col] = numeric(panel[col])

    panel["strict_accounting_stress_current"] = (
        panel[components].apply(numeric).fillna(0).sum(axis=1) >= 2
    ).astype(int)

    grouped = panel.groupby("company_id", sort=False)
    panel["strict_accounting_stress_12m_candidate"] = grouped["strict_accounting_stress_current"].shift(-1)
    panel["persistent_broad_stress_24m_candidate"] = (
        (grouped["financial_stress_current"].shift(-1) == 1)
        & (grouped["financial_stress_current"].shift(-2) == 1)
    ).astype(float)
    # Remove rows where the t+1/t+2 years are not actually observed.
    next_year = grouped["fiscal_year"].shift(-1)
    next2_year = grouped["fiscal_year"].shift(-2)
    panel.loc[next_year.ne(panel["fiscal_year"] + 1), "strict_accounting_stress_12m_candidate"] = np.nan
    panel.loc[
        next_year.ne(panel["fiscal_year"] + 1) | next2_year.ne(panel["fiscal_year"] + 2),
        "persistent_broad_stress_24m_candidate",
    ] = np.nan

    panel["altman_distress_12m_candidate"] = grouped["altman_distress_zone_ciq_candidate"].shift(-1)
    panel.loc[next_year.ne(panel["fiscal_year"] + 1), "altman_distress_12m_candidate"] = np.nan

    panel["broad_stress_12m_appendix"] = numeric(panel["stress_12m"])
    panel["event_distress_12m_candidate"] = numeric(panel["distress_event_12m_ciq"])
    panel["event_distress_24m_candidate"] = numeric(panel["distress_event_24m_ciq"])
    return panel


def add_freeze_flags(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.copy()
    panel["duplicate_company_year_flag"] = panel.duplicated(["company_id", "fiscal_year"], keep=False)
    panel["valid_market_flag"] = panel["market"].astype(str).isin(["ASX", "SINGAPORE"])
    panel["analyst_timing_violation_flag"] = numeric(panel["analyst_timing_ok"]).eq(0)
    panel["suspect_structure_name_flag"] = panel["company_name"].astype(str).str.contains(STRUCTURE_RE, na=False)
    panel["status_nonoperating_flag"] = ~panel["ciq_status"].fillna(panel["company_status"]).astype(str).str.contains(
        "Operating", case=False, na=False
    )
    panel["common_base_sample_flag"] = (
        ~panel["duplicate_company_year_flag"]
        & panel["valid_market_flag"]
        & ~panel["analyst_timing_violation_flag"]
    )
    panel["broad_baseline_sample_flag"] = panel["common_base_sample_flag"] & panel["broad_stress_12m_appendix"].notna()
    panel["strict_accounting_sample_flag"] = (
        panel["common_base_sample_flag"] & panel["strict_accounting_stress_12m_candidate"].notna()
    )
    panel["persistent_sample_flag"] = (
        panel["common_base_sample_flag"] & panel["persistent_broad_stress_24m_candidate"].notna()
    )
    panel["altman_sample_flag"] = (
        panel["common_base_sample_flag"]
        & ~panel["suspect_structure_name_flag"]
        & panel["altman_distress_12m_candidate"].notna()
    )
    panel["event12_sample_flag"] = (
        panel["common_base_sample_flag"]
        & numeric(panel["event_window_observable_12m"]).eq(1)
        & panel["event_distress_12m_candidate"].notna()
    )
    panel["event24_sample_flag"] = (
        panel["common_base_sample_flag"]
        & numeric(panel["event_window_observable_24m"]).eq(1)
        & panel["event_distress_24m_candidate"].notna()
    )
    return panel


def winsorize_panel(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    panel = panel.copy()
    rows = []
    for col in WINSOR_VARS:
        if col not in panel.columns:
            continue
        x = numeric(panel[col])
        nonmissing = x.dropna()
        if len(nonmissing) < 20:
            panel[f"{col}_w"] = x
            rows.append({"variable": col, "n": int(len(nonmissing)), "p01": np.nan, "p99": np.nan, "rule": "not_winsorized_lt20"})
            continue
        q01, q99 = nonmissing.quantile([0.01, 0.99])
        if pd.notna(q01) and pd.notna(q99) and q01 < q99:
            panel[f"{col}_w"] = x.clip(q01, q99)
            rule = "clip_p01_p99"
        else:
            panel[f"{col}_w"] = x
            rule = "not_winsorized_degenerate"
        rows.append({"variable": col, "n": int(len(nonmissing)), "p01": q01, "p99": q99, "rule": rule})
    return panel, pd.DataFrame(rows)


def sample_counts(panel: pd.DataFrame) -> pd.DataFrame:
    specs = [
        ("Broad stress appendix", "broad_baseline_sample_flag", "broad_stress_12m_appendix"),
        ("Strict accounting stress 12m", "strict_accounting_sample_flag", "strict_accounting_stress_12m_candidate"),
        ("Persistent broad stress 24m", "persistent_sample_flag", "persistent_broad_stress_24m_candidate"),
        ("Altman distress zone 12m", "altman_sample_flag", "altman_distress_12m_candidate"),
        ("Broad event candidate 12m", "event12_sample_flag", "event_distress_12m_candidate"),
        ("Broad event candidate 24m", "event24_sample_flag", "event_distress_24m_candidate"),
    ]
    rows = []
    for label, flag, target in specs:
        use = panel.loc[panel[flag]].copy()
        y = numeric(use[target])
        use = use.loc[y.notna()]
        y = numeric(use[target])
        rows.append(
            {
                "sample": label,
                "flag": flag,
                "target": target,
                "rows": int(len(use)),
                "firms": int(use["company_id"].nunique()),
                "events": int(y.sum()),
                "event_rate": float(y.mean()) if len(y) else np.nan,
                "covered_rows": int(numeric(use["analyst_covered"]).fillna(0).eq(1).sum()),
                "covered_rate": float(numeric(use["analyst_covered"]).fillna(0).mean()) if len(use) else np.nan,
                "asx_rows": int(use["market"].eq("ASX").sum()),
                "singapore_rows": int(use["market"].eq("SINGAPORE").sum()),
            }
        )
    return pd.DataFrame(rows)


def descriptive_stats(panel: pd.DataFrame) -> pd.DataFrame:
    use = panel.loc[panel["common_base_sample_flag"]].copy()
    variables = [
        "analyst_covered",
        "num_analysts",
        "roa_w",
        "leverage_w",
        "log_assets_w",
        "revenue_growth_w",
        "broad_stress_12m_appendix",
        "strict_accounting_stress_12m_candidate",
        "persistent_broad_stress_24m_candidate",
        "altman_distress_12m_candidate",
        "event_distress_12m_candidate",
    ]
    rows = []
    for var in variables:
        if var not in use.columns:
            continue
        x = numeric(use[var])
        rows.append(
            {
                "variable": var,
                "n": int(x.notna().sum()),
                "mean": float(x.mean()) if x.notna().any() else np.nan,
                "std": float(x.std()) if x.notna().sum() > 1 else np.nan,
                "p25": float(x.quantile(0.25)) if x.notna().any() else np.nan,
                "median": float(x.quantile(0.5)) if x.notna().any() else np.nan,
                "p75": float(x.quantile(0.75)) if x.notna().any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def prepare_logit_matrix(
    df: pd.DataFrame,
    target: str,
    controls: list[str],
    fixed_effects: list[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    cols = [target, "company_id", "analyst_covered"] + controls + fixed_effects
    use = df[cols].copy()
    y = numeric(use[target])
    use = use.loc[y.notna()].copy()
    y = numeric(use[target]).astype(int)
    if y.nunique() < 2:
        raise ValueError("target has one class")

    matrix_cols = [np.ones(len(use))]
    names = ["Intercept"]
    analyst = numeric(use["analyst_covered"]).fillna(0)
    matrix_cols.append(analyst.to_numpy(dtype=float))
    names.append("analyst_covered")

    for col in controls:
        x = numeric(use[col])
        x = x.fillna(x.median())
        sd = x.std(ddof=0)
        if pd.notna(sd) and sd > 0:
            x = (x - x.mean()) / sd
        if x.nunique(dropna=True) > 1:
            matrix_cols.append(x.to_numpy(dtype=float))
            names.append(col)

    for col in fixed_effects:
        labels = use[col].astype(str).replace({"nan": "Missing", "NaN": "Missing", "": "Missing"})
        dummies = pd.get_dummies(labels, prefix=f"FE:{col}", drop_first=True, dtype=float)
        for dummy_col in dummies:
            x = dummies[dummy_col]
            if x.nunique(dropna=True) > 1:
                matrix_cols.append(x.to_numpy(dtype=float))
                names.append(dummy_col)
    return np.column_stack(matrix_cols), y.to_numpy(dtype=int), use["company_id"].to_numpy(dtype=int), names


def fit_logit(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    beta = np.zeros(X.shape[1], dtype=float)
    ridge = np.eye(X.shape[1]) * 1e-6
    ridge[0, 0] = 0.0
    last_grad = np.zeros(X.shape[1], dtype=float)
    for _ in range(200):
        z = np.clip(X @ beta, -35, 35)
        p = np.clip(1.0 / (1.0 + np.exp(-z)), 1e-8, 1 - 1e-8)
        w = p * (1 - p)
        grad = X.T @ (p - y) + ridge @ beta
        hessian = X.T @ (X * w[:, None]) + ridge
        step = np.linalg.pinv(np.nan_to_num(hessian), rcond=1e-10) @ np.nan_to_num(grad)
        beta = np.clip(beta - step, -20, 20)
        last_grad = grad
        if float(np.max(np.abs(step))) < 1e-7:
            break
    z = np.clip(X @ beta, -35, 35)
    p = np.clip(1.0 / (1.0 + np.exp(-z)), 1e-8, 1 - 1e-8)
    return beta, p, last_grad


def cluster_se(X: np.ndarray, y: np.ndarray, p: np.ndarray, clusters: np.ndarray) -> np.ndarray:
    n, k = X.shape
    w = p * (1 - p)
    hessian = X.T @ (X * w[:, None])
    bread = np.linalg.pinv(np.nan_to_num(hessian), rcond=1e-10)
    scores = X * (y - p)[:, None]
    meat = np.zeros((k, k))
    for cluster in np.unique(clusters):
        s = scores[clusters == cluster].sum(axis=0).reshape(-1, 1)
        meat += s @ s.T
    cov = bread @ meat @ bread
    g = len(np.unique(clusters))
    if g > 1 and n > k:
        cov *= (g / (g - 1)) * ((n - 1) / (n - k))
    return np.sqrt(np.maximum(np.diag(cov), 0))


def logit_models(panel: pd.DataFrame) -> pd.DataFrame:
    specs = [
        ("Broad stress appendix", "broad_baseline_sample_flag", "broad_stress_12m_appendix"),
        ("Strict accounting stress 12m", "strict_accounting_sample_flag", "strict_accounting_stress_12m_candidate"),
        ("Persistent broad stress 24m", "persistent_sample_flag", "persistent_broad_stress_24m_candidate"),
        ("Altman distress zone 12m", "altman_sample_flag", "altman_distress_12m_candidate"),
        ("Broad event candidate 12m", "event12_sample_flag", "event_distress_12m_candidate"),
    ]
    controls = [f"{col}_w" for col in CONTROLS if f"{col}_w" in panel.columns]
    rows = []
    for label, flag, target in specs:
        use = panel.loc[panel[flag]].copy()
        y0 = numeric(use[target])
        use = use.loc[y0.notna()].copy()
        if len(use) < 200 or numeric(use[target]).nunique() < 2:
            rows.append({"label": label, "target": target, "n": len(use), "error": "insufficient variation"})
            continue
        try:
            X, y, clusters, names = prepare_logit_matrix(use, target, controls, ["market", "fiscal_year"])
            beta, pred, _grad = fit_logit(X, y)
            se = cluster_se(X, y, pred, clusters)
            idx = names.index("analyst_covered")
            coef = beta[idx]
            stderr = se[idx]
            z = coef / stderr if stderr > 0 else np.nan
            pvalue = erfc(abs(z) / sqrt(2)) if pd.notna(z) else np.nan
            # Average marginal effect for binary analyst coverage by toggling the raw column in X.
            x0 = X.copy()
            x1 = X.copy()
            x0[:, idx] = 0
            x1[:, idx] = 1
            p0 = 1.0 / (1.0 + np.exp(-np.clip(x0 @ beta, -35, 35)))
            p1 = 1.0 / (1.0 + np.exp(-np.clip(x1 @ beta, -35, 35)))
            ame = float((p1 - p0).mean())
            rows.append(
                {
                    "label": label,
                    "target": target,
                    "sample_flag": flag,
                    "n": int(len(y)),
                    "firms": int(len(np.unique(clusters))),
                    "events": int(y.sum()),
                    "event_rate": float(y.mean()),
                    "coef": float(coef),
                    "cluster_se": float(stderr),
                    "z": float(z),
                    "p_value": float(pvalue),
                    "odds_ratio": float(np.exp(coef)),
                    "ame": ame,
                    "controls": ", ".join(controls),
                    "fixed_effects": "market, fiscal_year",
                    "error": "",
                }
            )
        except Exception as exc:  # noqa: BLE001
            rows.append({"label": label, "target": target, "n": len(use), "error": repr(exc)})
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame, cols: list[str]) -> list[str]:
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for rec in df[cols].to_dict("records"):
        vals = []
        for col in cols:
            val = rec[col]
            if pd.isna(val):
                vals.append("")
            elif isinstance(val, float):
                vals.append(f"{val:.4f}")
            else:
                vals.append(str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def render_audit(
    panel: pd.DataFrame,
    sample_df: pd.DataFrame,
    winsor_df: pd.DataFrame,
    desc_df: pd.DataFrame,
    model_df: pd.DataFrame,
    out_panel: Path,
) -> str:
    lines = [
        "# AEL APAC v2 Sample Freeze and Cleaning Audit",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        f"Input panel: `{INPUT_PANEL}`",
        f"Local frozen candidate panel: `{out_panel}`",
        "",
        "## Decision",
        "",
        "Status: PROVISIONAL_SAMPLE_FREEZE_NOT_FINAL_SUBMISSION_SAMPLE",
        "",
        "The v2 panel has been converted into auditable candidate samples with explicit exclusion flags, winsorized controls, next-year label candidates, and preliminary logit checks. This is progress toward the data-freeze gate, not a final no-risk submission dataset.",
        "",
        "## Freeze Rules Applied",
        "",
        "- Drop duplicate company-year rows from model samples; current duplicate count is shown below.",
        "- Keep only recognized markets: ASX and SINGAPORE.",
        "- Drop rows where a covered analyst forecast date is after its as-of date; uncovered rows are not penalized for missing forecast/as-of dates.",
        "- Keep FY2024 out of forward 12-month event/broad-stress samples and FY2023-FY2024 out of 24-month forward samples when the event window is not observable.",
        "- Build next-year strict accounting stress from negative equity, operating loss, and low interest coverage.",
        "- Build next-year Altman distress by shifting the full-component Altman distress-zone candidate one fiscal year ahead.",
        "- Exclude name-flagged REIT/fund/trust/SPAC-like firms from the Altman candidate sample only; this is a conservative proxy until industry classifications are available.",
        "- Winsorize continuous controls and candidate Altman components at the 1st/99th percentiles.",
        "",
        "## Exclusion Counts",
        "",
        f"- Total rows: {len(panel):,}",
        f"- Unique companies: {panel['company_id'].nunique():,}",
        f"- Duplicate company-year rows: {int(panel['duplicate_company_year_flag'].sum()):,}",
        f"- Analyst timing violations: {int(panel['analyst_timing_violation_flag'].sum()):,}",
        f"- Suspect structure name rows: {int(panel['suspect_structure_name_flag'].sum()):,}",
        f"- Suspect structure companies: {panel.loc[panel['suspect_structure_name_flag'], 'company_id'].nunique():,}",
        f"- Non-operating status rows: {int(panel['status_nonoperating_flag'].sum()):,}",
        "",
        "## Candidate Sample Counts",
        "",
    ]
    lines.extend(
        markdown_table(
            sample_df,
            ["sample", "rows", "firms", "events", "event_rate", "covered_rate", "asx_rows", "singapore_rows"],
        )
    )
    lines.extend(["", "## Preliminary Logit Checks", ""])
    display_model = model_df.copy()
    for col in ["coef", "cluster_se", "p_value", "odds_ratio", "ame", "event_rate"]:
        if col in display_model:
            display_model[col] = pd.to_numeric(display_model[col], errors="coerce")
    lines.extend(
        markdown_table(
            display_model,
            ["label", "n", "events", "event_rate", "coef", "cluster_se", "p_value", "odds_ratio", "ame", "error"],
        )
    )
    lines.extend(["", "## Winsorization Rules", ""])
    lines.extend(markdown_table(winsor_df, ["variable", "n", "p01", "p99", "rule"]))
    lines.extend(["", "## Descriptive Statistics", ""])
    lines.extend(markdown_table(desc_df, ["variable", "n", "mean", "std", "p25", "median", "p75"]))
    lines.extend(
        [
            "",
            "## Reviewer-Level Interpretation",
            "",
            "- Broad stress remains appendix-only because its event rate is high and was already identified as too broad for the main Q3 claim.",
            "- Strict accounting stress is the most defensible current main-label candidate from the available data because it is forward-looking, uses transparent accounting components, and has full-panel coverage after timing exclusions.",
            "- Altman distress is not yet strong enough as the main label because the full-component sample is much smaller and total-liabilities coverage is the binding bottleneck, especially for Singapore.",
            "- Broad Key Developments event labels are useful as a validation/robustness candidate, but not as formal bankruptcy/default evidence because event matching currently uses conservative company-name matching rather than clean direct Entity ID overlap.",
            "- Tone/text cleaning cannot be marked complete from this panel because no tone or raw text quality fields are present in the v2 firm-year file; this remains a separate data/input gap if the final paper keeps a tone-extraction component.",
            "",
            "## Next Gate",
            "",
            "Use this frozen candidate panel to rerun the full table suite around the strict accounting stress label, then decide whether the result pattern is strong enough for the SSCI/JCR Q3 route. If strict accounting and event/Altman robustness do not align, downgrade the paper story rather than forcing a stronger claim.",
            "",
        ]
    )
    return "\n".join(lines)


def build(input_panel: Path, out_panel: Path, out_audit: Path) -> None:
    panel = load_panel(input_panel)
    panel = add_labels(panel)
    panel = add_freeze_flags(panel)
    panel, winsor_df = winsorize_panel(panel)
    sample_df = sample_counts(panel)
    desc_df = descriptive_stats(panel)
    model_df = logit_models(panel)

    out_panel.parent.mkdir(parents=True, exist_ok=True)
    out_audit.parent.mkdir(parents=True, exist_ok=True)
    OUT_SAMPLE_COUNTS.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out_panel, index=False)
    sample_df.to_csv(OUT_SAMPLE_COUNTS, index=False)
    desc_df.to_csv(OUT_DESC, index=False)
    model_df.to_csv(OUT_MODEL, index=False)
    out_audit.write_text(render_audit(panel, sample_df, winsor_df, desc_df, model_df, out_panel), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-panel", type=Path, default=INPUT_PANEL)
    parser.add_argument("--out-panel", type=Path, default=OUT_PANEL)
    parser.add_argument("--out-audit", type=Path, default=OUT_AUDIT)
    args = parser.parse_args()
    build(args.input_panel, args.out_panel, args.out_audit)
    print(f"Wrote {args.out_panel}")
    print(f"Wrote {args.out_audit}")
    print(f"Wrote {OUT_SAMPLE_COUNTS}")
    print(f"Wrote {OUT_DESC}")
    print(f"Wrote {OUT_MODEL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
