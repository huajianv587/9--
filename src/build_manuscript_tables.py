#!/usr/bin/env python3
"""Build compact manuscript-facing tables from verified model outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PANEL = Path("data/processed/ael_apac_firm_year_panel.csv")
OUT_DIR = Path("outputs/manuscript")


LABELS = {
    "analyst_covered": "Analyst coverage",
    "roa": "ROA",
    "roe": "ROE",
    "leverage": "Leverage",
    "interest_coverage": "Interest coverage",
    "operating_margin": "Operating margin",
    "revenue_growth": "Revenue growth",
    "log_assets": "Log assets",
    "analyst_dispersion": "Analyst dispersion",
    "forecast_high_low_spread": "Forecast high-low spread",
    "num_analysts": "Number of analysts",
}


def p_text(p_value: float) -> str:
    if pd.isna(p_value):
        return ""
    if p_value < 0.001:
        return "<0.001"
    return f"{p_value:.3f}"


def stars(p_value: float) -> str:
    if pd.isna(p_value):
        return ""
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""


def coef_cell(row: pd.Series) -> str:
    return f"{row['coef']:.3f}{stars(row['p_value'])}<br>({row['robust_se']:.3f})"


def read(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def table1(panel: pd.DataFrame) -> pd.DataFrame:
    labelled = panel[panel["stress_12m"].notna()].copy()
    covered = pd.to_numeric(labelled["analyst_covered"], errors="coerce").fillna(0).astype(bool)
    rows = []
    for market, group in labelled.groupby("market", dropna=False):
        cov = pd.to_numeric(group["analyst_covered"], errors="coerce").fillna(0).astype(bool)
        rows.append(
            {
                "Market": market.title() if str(market).upper() != "ASX" else "ASX",
                "Labelled firms": group["company_id"].nunique(),
                "Labelled firm-years": len(group),
                "Stress events": int(pd.to_numeric(group["stress_12m"], errors="coerce").sum()),
                "Analyst-covered firm-years": int(cov.sum()),
                "Covered event firm-years": int((cov & pd.to_numeric(group["stress_12m"], errors="coerce").astype(bool)).sum()),
                "Coverage rate (%)": cov.mean() * 100,
            }
        )
    rows.append(
        {
            "Market": "Combined",
            "Labelled firms": labelled["company_id"].nunique(),
            "Labelled firm-years": len(labelled),
            "Stress events": int(pd.to_numeric(labelled["stress_12m"], errors="coerce").sum()),
            "Analyst-covered firm-years": int(covered.sum()),
            "Covered event firm-years": int((covered & pd.to_numeric(labelled["stress_12m"], errors="coerce").astype(bool)).sum()),
            "Coverage rate (%)": covered.mean() * 100,
        }
    )
    out = pd.DataFrame(rows)
    out["Coverage rate (%)"] = out["Coverage rate (%)"].map(lambda x: f"{x:.1f}")
    return out


def table2() -> pd.DataFrame:
    df = read("outputs/tables/apac_table2a_logit_inference_fe.csv")
    keep_vars = [
        "analyst_covered",
        "roa",
        "roe",
        "leverage",
        "interest_coverage",
        "operating_margin",
        "revenue_growth",
        "log_assets",
    ]
    models = ["Accounting controls", "Add analyst coverage"]
    rows = []
    for variable in keep_vars:
        row = {"Variable": LABELS[variable]}
        for model in models:
            match = df[(df["model"] == model) & (df["variable"] == variable)]
            row[model] = "" if match.empty else coef_cell(match.iloc[0])
        rows.append(row)
    rows.extend(
        [
            {"Variable": "Market fixed effects", models[0]: "Yes", models[1]: "Yes"},
            {"Variable": "Year fixed effects", models[0]: "Yes", models[1]: "Yes"},
            {"Variable": "Observations", models[0]: "19,402", models[1]: "19,402"},
            {"Variable": "Stress events", models[0]: "12,303", models[1]: "12,303"},
        ]
    )
    return pd.DataFrame(rows)


def focus_row(path: str, variable: str = "analyst_covered") -> pd.Series:
    df = read(path)
    match = df[df["variable"].eq(variable)]
    if match.empty:
        raise ValueError(f"{variable} not found in {path}")
    return match.iloc[0]


def table3() -> pd.DataFrame:
    specs = [
        ("APAC main logit", "outputs/tables/apac_table2a_logit_inference_fe.csv"),
        ("APAC conservative controls", "outputs/tables/apac_table4_label_component_robustness_fe.csv"),
        ("Singapore main logit", "outputs/tables/singapore_table2a_logit_inference_fe.csv"),
        ("Singapore conservative controls", "outputs/tables/singapore_table4_label_component_robustness_fe.csv"),
        ("ASX main logit", "outputs/tables/asx_table2a_logit_inference_fe.csv"),
        ("ASX conservative controls", "outputs/tables/asx_table4_label_component_robustness_fe.csv"),
    ]
    rows = []
    for label, path in specs:
        row = focus_row(path)
        fe = row["fixed_effects"]
        fe = fe.replace("market, fiscal_year", "Market, year").replace("fiscal_year", "Year")
        rows.append(
            {
                "Specification": label,
                "Coefficient": f"{row['coef']:.3f}{stars(row['p_value'])}",
                "Robust SE": f"{row['robust_se']:.3f}",
                "Odds ratio": f"{row['odds_ratio']:.3f}",
                "p-value": p_text(row["p_value"]),
                "Observations": f"{int(row['n']):,}",
                "Stress events": f"{int(row['events']):,}",
                "Fixed effects": fe,
            }
        )
    return pd.DataFrame(rows)


def write_outputs(name: str, table: pd.DataFrame) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_DIR / f"{name}.csv", index=False)
    (OUT_DIR / f"{name}.md").write_text(table.to_markdown(index=False) + "\n", encoding="utf-8")


def main() -> int:
    panel = pd.read_csv(PANEL, low_memory=False)
    write_outputs("table1_sample", table1(panel))
    write_outputs("table2_logit_fixed_effects", table2())
    write_outputs("table3_robustness", table3())
    print(f"Saved manuscript tables to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
