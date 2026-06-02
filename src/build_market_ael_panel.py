#!/usr/bin/env python3
"""Merge market-level accounting stress panels with historical estimates."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs")


ANALYST_COLUMNS = [
    "eps_stddev",
    "eps_high",
    "eps_low",
    "num_analysts",
    "eps_est",
    "forecast_date",
    "as_of_date",
    "analyst_dispersion",
    "forecast_high_low_spread",
    "analyst_covered",
    "source_file",
    "source_sheet",
]


def merge_panel(accounting_path: Path, estimates_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not accounting_path.exists():
        raise FileNotFoundError(f"Accounting panel not found: {accounting_path}")
    accounting = pd.read_csv(accounting_path)
    accounting["company_id"] = accounting["company_id"].astype(str).str.strip()
    accounting["fiscal_year"] = pd.to_numeric(accounting["fiscal_year"], errors="coerce").astype("Int64")

    if estimates_path.exists():
        estimates = pd.read_csv(estimates_path)
    else:
        estimates = pd.DataFrame()
    if estimates.empty:
        panel = accounting.copy()
        for col in ANALYST_COLUMNS:
            if col not in panel.columns:
                panel[col] = np.nan
        return panel, estimates

    estimates["company_id"] = estimates["company_id"].astype(str).str.strip()
    estimates["fiscal_year"] = pd.to_numeric(estimates["fiscal_year"], errors="coerce").astype("Int64")
    estimates = estimates.drop_duplicates(["company_id", "fiscal_year"], keep="first")
    panel = accounting.merge(
        estimates.drop(columns=["company_name", "market"], errors="ignore"),
        on=["company_id", "fiscal_year"],
        how="left",
        validate="many_to_one",
    )
    panel["analyst_covered"] = panel["analyst_covered"].fillna(0).astype(int)
    return panel, estimates


def write_summary(market: str, estimates: pd.DataFrame, panel: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"ael_{market}_firm_year_panel_summary.md"
    title_market = market.upper()
    lines = [
        f"# {title_market} AEL Firm-Year Panel Summary",
        "",
        "This panel merges historical accounting stress labels with Capital IQ analyst estimates by explicit fiscal year.",
        "",
    ]
    if not estimates.empty:
        cov = (
            estimates.groupby("fiscal_year", as_index=False)
            .agg(
                firms=("company_id", "nunique"),
                analyst_covered=("analyst_covered", "sum"),
                eps_stddev_nonmissing=("eps_stddev", lambda s: int(s.notna().sum())),
                num_analysts_nonmissing=("num_analysts", lambda s: int(s.notna().sum())),
            )
            .sort_values("fiscal_year")
        )
        cov["coverage_pct"] = cov["analyst_covered"] / cov["firms"] * 100
        lines.extend(["## Analyst Export Coverage", "", cov.to_markdown(index=False, floatfmt=".2f"), ""])
    else:
        lines.extend(["No estimates files were parsed or merged.", ""])

    if not panel.empty:
        labelled = panel["stress_12m"].notna() if "stress_12m" in panel.columns else pd.Series(False)
        covered = panel["analyst_covered"].fillna(0).astype(bool) if "analyst_covered" in panel.columns else pd.Series(False)
        lines.extend(
            [
                "## Merged Panel",
                "",
                f"- Firm-years: {len(panel)}",
                f"- Firms: {panel['company_id'].nunique()}",
                f"- Labelled next-year stress observations: {int(labelled.sum())}",
                f"- Analyst-covered firm-years: {int(covered.sum())}",
                f"- Analyst-covered stress events: {int((covered & panel['stress_12m'].fillna(0).astype(bool)).sum()) if 'stress_12m' in panel.columns else 0}",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a market AEL analyst-accounting firm-year panel.")
    parser.add_argument("--market", required=True, help="Market token used in processed filenames, e.g. asx or singapore.")
    parser.add_argument("--accounting-panel")
    parser.add_argument("--estimates-panel")
    parser.add_argument("--panel-out")
    parser.add_argument("--summary-out-dir", default=str(OUTPUT_DIR))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    market = args.market.lower()
    accounting_path = Path(args.accounting_panel) if args.accounting_panel else PROCESSED_DIR / f"{market}_financials_firm_year_pilot.csv"
    estimates_path = Path(args.estimates_panel) if args.estimates_panel else PROCESSED_DIR / f"{market}_estimates_firm_year.csv"
    panel_out = Path(args.panel_out) if args.panel_out else PROCESSED_DIR / f"ael_{market}_firm_year_panel.csv"

    panel, estimates = merge_panel(accounting_path, estimates_path)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(panel_out, index=False)
    summary_path = write_summary(market, estimates, panel, Path(args.summary_out_dir))
    print(f"Saved: {panel_out}")
    print(f"Saved: {summary_path}")
    if not panel.empty:
        covered = int(panel.get("analyst_covered", pd.Series(dtype=float)).fillna(0).sum())
        print(f"market={market.upper()} rows={len(panel)} firms={panel['company_id'].nunique()} covered={covered}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
