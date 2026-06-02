#!/usr/bin/env python3
"""Build a market-level Capital IQ estimates panel from as-of-date exports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_singapore_ael_panel import RAW_DIR, read_estimates_file


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs")


def estimate_files(market: str, raw_dir: Path) -> list[Path]:
    return sorted(raw_dir.glob(f"capital_iq_estimates_{market}_fyplus1_asof_*_*.xlsx"))


def build_estimates_panel(market: str, raw_dir: Path) -> pd.DataFrame:
    frames = [read_estimates_file(path) for path in estimate_files(market, raw_dir)]
    frames = [df for df in frames if not df.empty]
    if not frames:
        return pd.DataFrame()
    estimates = pd.concat(frames, ignore_index=True)
    estimates.insert(0, "market", market.upper())
    return estimates


def write_summary(market: str, estimates: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{market}_estimates_firm_year_summary.md"
    title_market = market.upper()
    lines = [
        f"# {title_market} Estimates Firm-Year Summary",
        "",
        "This file audits leakage-safe Capital IQ FY+1 EPS estimate exports by explicit 12/31/YYYY as-of date.",
        "",
    ]
    if estimates.empty:
        lines.append("No estimates files were parsed.")
    else:
        cov = (
            estimates.groupby("fiscal_year", as_index=False)
            .agg(
                firms=("company_id", "nunique"),
                analyst_covered=("analyst_covered", "sum"),
                eps_est_nonmissing=("eps_est", lambda s: int(s.notna().sum())),
                eps_stddev_nonmissing=("eps_stddev", lambda s: int(s.notna().sum())),
                num_analysts_nonmissing=("num_analysts", lambda s: int(s.notna().sum())),
                source_files=("source_file", "nunique"),
            )
            .sort_values("fiscal_year")
        )
        cov["coverage_pct"] = cov["analyst_covered"] / cov["firms"] * 100
        lines.extend(
            [
                "## Coverage By As-Of Year",
                "",
                cov.to_markdown(index=False, floatfmt=".2f"),
                "",
                "## Parsed Files",
                "",
            ]
        )
        file_audit = (
            estimates.groupby(["source_file", "source_sheet", "fiscal_year"], as_index=False)
            .agg(rows=("company_id", "count"), analyst_covered=("analyst_covered", "sum"))
            .sort_values(["fiscal_year", "source_file"])
        )
        lines.append(file_audit.to_markdown(index=False))
        lines.extend(
            [
                "",
                "## Merge Status",
                "",
                f"- {title_market} estimates are parsed and ready.",
                f"- {title_market} historical accounting/stress financials are still required before this market can be merged into the AEL firm-year panel.",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a market-level Capital IQ estimates firm-year panel.")
    parser.add_argument("--market", required=True, help="Market token used in raw filenames, e.g. asx or singapore.")
    parser.add_argument("--raw-dir", default=str(RAW_DIR))
    parser.add_argument("--estimates-out")
    parser.add_argument("--summary-out-dir", default=str(OUTPUT_DIR))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    market = args.market.lower()
    raw_dir = Path(args.raw_dir)
    estimates = build_estimates_panel(market, raw_dir)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.estimates_out) if args.estimates_out else PROCESSED_DIR / f"{market}_estimates_firm_year.csv"
    estimates.to_csv(out_path, index=False)
    summary_path = write_summary(market, estimates, Path(args.summary_out_dir))

    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
    if not estimates.empty:
        print(
            f"market={market.upper()} rows={len(estimates)} "
            f"years={int(estimates['fiscal_year'].min())}-{int(estimates['fiscal_year'].max())} "
            f"covered={int(estimates['analyst_covered'].sum())}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
