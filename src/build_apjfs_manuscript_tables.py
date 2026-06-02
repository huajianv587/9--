#!/usr/bin/env python3
"""Build APJFS-style manuscript tables from verified outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import numpy as np


PANEL = Path("data/processed/ael_apac_firm_year_panel.csv")
OUT_DIR = Path("outputs/manuscript_apjfs")

LABELS = {
    "stress_12m": "Future stress",
    "financial_stress_current": "Current stress",
    "roa": "ROA",
    "roe": "ROE",
    "leverage": "Leverage",
    "interest_coverage": "Interest coverage",
    "operating_margin": "Operating margin",
    "revenue_growth": "Revenue growth",
    "log_assets": "Log assets",
    "num_analysts": "Number of analysts",
}


def p_text(value: float) -> str:
    if pd.isna(value):
        return ""
    if value < 0.001:
        return "<0.001"
    return f"{value:.3f}"


def stars(value: float) -> str:
    if pd.isna(value):
        return ""
    if value < 0.01:
        return "***"
    if value < 0.05:
        return "**"
    if value < 0.10:
        return "*"
    return ""


def write_outputs(name: str, table: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_DIR / f"{name}.csv", index=False)
    rows = []
    columns = [str(c) for c in table.columns]
    rows.append("| " + " | ".join(columns) + " |")
    rows.append("| " + " | ".join("---" for _ in columns) + " |")
    for _, row in table.iterrows():
        values = [str(row[c]) if pd.notna(row[c]) else "" for c in table.columns]
        rows.append("| " + " | ".join(values) + " |")
    (OUT_DIR / f"{name}.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def table1(panel: pd.DataFrame) -> pd.DataFrame:
    labelled = panel[panel["stress_12m"].notna()].copy()
    rows = []
    for market, group in labelled.groupby("market", dropna=False):
        covered = pd.to_numeric(group["analyst_covered"], errors="coerce").fillna(0).astype(bool)
        stress = pd.to_numeric(group["stress_12m"], errors="coerce").fillna(0).astype(bool)
        rows.append(
            {
                "Market": "ASX" if str(market).upper() == "ASX" else "Singapore",
                "Firms": f"{group['company_id'].nunique():,}",
                "Firm-years": f"{len(group):,}",
                "Stress events": f"{int(stress.sum()):,}",
                "Analyst-covered firm-years": f"{int(covered.sum()):,}",
                "Coverage rate (%)": f"{covered.mean() * 100:.1f}",
            }
        )
    covered = pd.to_numeric(labelled["analyst_covered"], errors="coerce").fillna(0).astype(bool)
    stress = pd.to_numeric(labelled["stress_12m"], errors="coerce").fillna(0).astype(bool)
    rows.append(
        {
            "Market": "Combined",
            "Firms": f"{labelled['company_id'].nunique():,}",
            "Firm-years": f"{len(labelled):,}",
            "Stress events": f"{int(stress.sum()):,}",
            "Analyst-covered firm-years": f"{int(covered.sum()):,}",
            "Coverage rate (%)": f"{covered.mean() * 100:.1f}",
        }
    )
    return pd.DataFrame(rows)


def table2(panel: pd.DataFrame) -> pd.DataFrame:
    labelled = panel[panel["stress_12m"].notna()].copy()
    labelled["covered_group"] = pd.to_numeric(labelled["analyst_covered"], errors="coerce").fillna(0).astype(int)
    rows = []
    for var in [
        "stress_12m",
        "financial_stress_current",
        "roa",
        "roe",
        "leverage",
        "interest_coverage",
        "operating_margin",
        "revenue_growth",
        "log_assets",
        "num_analysts",
    ]:
        if var not in labelled.columns:
            continue
        x = pd.to_numeric(labelled[var], errors="coerce").replace([np.inf, -np.inf], np.nan)
        if var not in {"stress_12m", "financial_stress_current", "num_analysts"}:
            nonmissing = x.dropna()
            if len(nonmissing) >= 20:
                lo, hi = nonmissing.quantile([0.01, 0.99])
                if pd.notna(lo) and pd.notna(hi) and lo < hi:
                    x = x.clip(lo, hi)
        uncovered = x[labelled["covered_group"].eq(0)].dropna()
        covered = x[labelled["covered_group"].eq(1)].dropna()
        rows.append(
            {
                "Variable": LABELS[var],
                "Uncovered mean": "" if uncovered.empty else f"{uncovered.mean():.3f}",
                "Covered mean": "" if covered.empty else f"{covered.mean():.3f}",
                "Uncovered SD": "" if uncovered.empty else f"{uncovered.std(ddof=1):.3f}",
                "Covered SD": "" if covered.empty else f"{covered.std(ddof=1):.3f}",
            }
        )
    return pd.DataFrame(rows)


def coef_cell(row: pd.Series) -> str:
    return f"{row['coef']:.3f}{stars(row['p_value'])} ({row['robust_se']:.3f})"


def table3() -> pd.DataFrame:
    df = pd.read_csv("outputs/tables/apac_table2a_logit_inference_fe.csv")
    labels = {
        "analyst_covered": "Analyst coverage",
        "roa": "ROA",
        "roe": "ROE",
        "leverage": "Leverage",
        "interest_coverage": "Interest coverage",
        "operating_margin": "Operating margin",
        "revenue_growth": "Revenue growth",
        "log_assets": "Log assets",
    }
    rows = []
    for var, label in labels.items():
        row = {"Variable": label}
        for model in ["Accounting controls", "Add analyst coverage"]:
            match = df[(df["model"].eq(model)) & (df["variable"].eq(var))]
            row[model] = "" if match.empty else coef_cell(match.iloc[0])
        rows.append(row)
    rows.extend(
        [
            {"Variable": "Market fixed effects", "Accounting controls": "Yes", "Add analyst coverage": "Yes"},
            {"Variable": "Year fixed effects", "Accounting controls": "Yes", "Add analyst coverage": "Yes"},
            {"Variable": "Observations", "Accounting controls": "19,402", "Add analyst coverage": "19,402"},
            {"Variable": "Stress events", "Accounting controls": "12,303", "Add analyst coverage": "12,303"},
        ]
    )
    return pd.DataFrame(rows)


def table4() -> pd.DataFrame:
    base = pd.read_csv("outputs/manuscript/table3_robustness.csv")
    ext = pd.read_csv("outputs/tables/apjfs_extended_robustness.csv")
    rows = []
    for _, row in base.iterrows():
        rows.append(
            {
                "Specification": row["Specification"],
                "Coefficient": row["Coefficient"],
                "Robust SE": row["Robust SE"],
                "Odds ratio / metric": row["Odds ratio"],
                "p-value": row["p-value"],
                "Observations": row["Observations"],
                "Stress events": row["Stress events"],
            }
        )
    for _, row in ext.iterrows():
        if row["specification"] == "Baseline with market-year FE":
            continue
        model_family = str(row.get("model_family", "logit"))
        if model_family == "linear probability":
            coefficient = f"{row['coef']:.3f}{stars(row['p_value'])}"
            effect_metric = "LPM"
        else:
            coefficient = f"{row['coef']:.3f}{stars(row['p_value'])}"
            effect_metric = f"{row['odds_ratio']:.3f}"
        rows.append(
            {
                "Specification": row["specification"],
                "Coefficient": coefficient,
                "Robust SE": f"{row['robust_se']:.3f}",
                "Odds ratio / metric": effect_metric,
                "p-value": p_text(row["p_value"]),
                "Observations": f"{int(row['n']):,}",
                "Stress events": f"{int(row['events']):,}",
            }
        )
    return pd.DataFrame(rows)


def main() -> int:
    panel = pd.read_csv(PANEL, low_memory=False)
    write_outputs("table1_sample", table1(panel))
    write_outputs("table2_descriptives", table2(panel))
    write_outputs("table3_logit", table3())
    write_outputs("table4_robustness", table4())
    print(f"Saved APJFS manuscript tables to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
