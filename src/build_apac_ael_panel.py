#!/usr/bin/env python3
"""Build a combined APAC AEL firm-year panel from market panels."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs")
DEFAULT_PANELS = [
    PROCESSED_DIR / "ael_singapore_firm_year_panel.csv",
    PROCESSED_DIR / "ael_asx_firm_year_panel.csv",
]
PANEL_OUT = PROCESSED_DIR / "ael_apac_firm_year_panel.csv"


def infer_market(path: Path, frame: pd.DataFrame) -> str:
    if "market" in frame.columns and frame["market"].notna().any():
        return str(frame["market"].dropna().iloc[0]).upper()
    name = path.name.lower()
    if "singapore" in name:
        return "SINGAPORE"
    if "asx" in name:
        return "ASX"
    return path.stem.upper()


def read_market_panel(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["company_id"] = frame["company_id"].astype(str).str.strip()
    frame["fiscal_year"] = pd.to_numeric(frame["fiscal_year"], errors="coerce").astype("Int64")
    frame["market"] = infer_market(path, frame)
    if "country" not in frame.columns:
        frame["country"] = frame["market"]
    if "exchange" not in frame.columns:
        frame["exchange"] = frame["market"]
    frame["source_panel"] = path.name
    return frame


def build_panel(paths: list[Path]) -> pd.DataFrame:
    frames = [read_market_panel(path) for path in paths if path.exists()]
    if not frames:
        return pd.DataFrame()
    panel = pd.concat(frames, ignore_index=True, sort=False)
    panel = panel.dropna(subset=["company_id", "fiscal_year"])
    panel = panel.sort_values(["market", "company_id", "fiscal_year"]).reset_index(drop=True)
    panel = panel.drop_duplicates(["company_id", "fiscal_year"], keep="first")
    return panel


def write_summary(panel: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "ael_apac_firm_year_panel_summary.md"
    lines = [
        "# APAC AEL Firm-Year Panel Summary",
        "",
        "This panel stacks completed market-level AEL panels for cross-market modelling and deduplicates repeated company-years across markets.",
        "",
    ]
    if panel.empty:
        lines.append("No market panels were available.")
    else:
        labelled = panel["stress_12m"].notna() if "stress_12m" in panel.columns else pd.Series(False, index=panel.index)
        covered = (
            pd.to_numeric(panel["analyst_covered"], errors="coerce").fillna(0).astype(bool)
            if "analyst_covered" in panel.columns
            else pd.Series(False, index=panel.index)
        )
        lines.extend(
            [
                "## Combined Coverage",
                "",
                f"- Markets: {panel['market'].nunique()}",
                f"- Firms: {panel['company_id'].nunique()}",
                f"- Firm-years: {len(panel)}",
                f"- Years: {int(panel['fiscal_year'].min())}-{int(panel['fiscal_year'].max())}",
                f"- Labelled next-year stress observations: {int(labelled.sum())}",
                f"- Next-year stress events: {int(pd.to_numeric(panel.loc[labelled, 'stress_12m'], errors='coerce').fillna(0).sum())}",
                f"- Analyst-covered firm-years: {int(covered.sum())}",
                f"- Analyst-covered stress events: {int((covered & pd.to_numeric(panel['stress_12m'], errors='coerce').fillna(0).astype(bool)).sum()) if 'stress_12m' in panel.columns else 0}",
                "",
                "## Market Coverage",
                "",
            ]
        )
        by_market = (
            panel.assign(
                labelled=labelled,
                covered=covered,
                stress_numeric=pd.to_numeric(panel.get("stress_12m", 0), errors="coerce").fillna(0),
            )
            .groupby("market", as_index=False)
            .agg(
                firms=("company_id", "nunique"),
                firm_years=("company_id", "count"),
                labelled=("labelled", "sum"),
                stress_events=("stress_numeric", "sum"),
                analyst_covered=("covered", "sum"),
            )
            .sort_values("market")
        )
        lines.append(by_market.to_markdown(index=False, floatfmt=".0f"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build combined APAC AEL firm-year panel.")
    parser.add_argument("--panels", nargs="*", default=[str(path) for path in DEFAULT_PANELS])
    parser.add_argument("--panel-out", default=str(PANEL_OUT))
    parser.add_argument("--summary-out-dir", default=str(OUTPUT_DIR))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [Path(path) for path in args.panels]
    panel = build_panel(paths)
    out = Path(args.panel_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out, index=False)
    summary = write_summary(panel, Path(args.summary_out_dir))
    print(f"Saved: {out}")
    print(f"Saved: {summary}")
    if not panel.empty:
        labelled = panel["stress_12m"].notna()
        print(
            f"markets={panel['market'].nunique()} firms={panel['company_id'].nunique()} "
            f"firm_years={len(panel)} labelled={int(labelled.sum())}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
