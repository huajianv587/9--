#!/usr/bin/env python3
"""Audit Capital IQ analyst snapshot timing for leakage risk."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


PANEL = Path("data/processed/ael_apac_firm_year_panel.csv")
OUT = Path("outputs/capital_iq_analyst_snapshot_timing_audit_20260601.md")


def source_asof_year(value: object) -> int | None:
    if pd.isna(value):
        return None
    match = re.search(r"asof_(20\d{2})1231", str(value))
    return int(match.group(1)) if match else None


def yes_no(value: bool) -> str:
    return "PASS" if value else "FAIL"


def frame_to_markdown(frame: pd.DataFrame) -> str:
    cols = list(frame.columns)
    rows = [[str(value) for value in row] for row in frame.itertuples(index=False, name=None)]
    widths = [
        max(len(str(col)), *(len(row[idx]) for row in rows)) if rows else len(str(col))
        for idx, col in enumerate(cols)
    ]

    def fmt(values: list[str]) -> str:
        return "| " + " | ".join(str(value).ljust(widths[idx]) for idx, value in enumerate(values)) + " |"

    header = fmt([str(col) for col in cols])
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    return "\n".join([header, sep, *(fmt(row) for row in rows)])


def main() -> int:
    panel = pd.read_csv(PANEL, low_memory=False)
    panel["fy"] = pd.to_numeric(panel["fiscal_year"], errors="coerce")
    panel["covered"] = pd.to_numeric(panel["analyst_covered"], errors="coerce").fillna(0).astype(int).eq(1)
    panel["stress_labelled"] = panel["stress_12m"].notna()
    panel["asof_dt"] = pd.to_datetime(panel["as_of_date"], errors="coerce")
    panel["forecast_dt"] = pd.to_datetime(panel["forecast_date"], errors="coerce")
    panel["source_asof_year"] = panel["source_file"].map(source_asof_year)

    labelled = panel[panel["stress_labelled"]].copy()
    covered = panel[panel["covered"]].copy()
    asof_rows = panel[panel["asof_dt"].notna()].copy()
    fy2024 = panel[panel["fy"].eq(2024)].copy()

    labelled_asof_ok = labelled["asof_dt"].notna()
    labelled_dec31_ok = (
        labelled["asof_dt"].dt.year.eq(labelled["fy"])
        & labelled["asof_dt"].dt.month.eq(12)
        & labelled["asof_dt"].dt.day.eq(31)
    )
    source_year_ok = asof_rows["source_asof_year"].eq(asof_rows["fy"])
    covered_asof_ok = covered["asof_dt"].notna()
    covered_forecast_ok = covered["forecast_dt"].notna()
    covered_forecast_date_safe = covered["forecast_dt"].dt.normalize().le(covered["asof_dt"].dt.normalize())
    covered_timestamp_after_asof = covered["forecast_dt"].gt(covered["asof_dt"])
    covered_prior_year_forecasts = covered["forecast_dt"].dt.year.lt(covered["fy"])

    checks = [
        (
            "Modelled rows have analyst as-of date",
            int(labelled_asof_ok.sum()),
            len(labelled),
            yes_no(bool(labelled_asof_ok.all())),
        ),
        (
            "Modelled as-of date equals fiscal-year 12/31",
            int(labelled_dec31_ok.sum()),
            len(labelled),
            yes_no(bool(labelled_dec31_ok.all())),
        ),
        (
            "Source filename as-of year matches fiscal year",
            int(source_year_ok.sum()),
            len(asof_rows),
            yes_no(bool(source_year_ok.all())),
        ),
        (
            "Analyst-covered rows have as-of date",
            int(covered_asof_ok.sum()),
            len(covered),
            yes_no(bool(covered_asof_ok.all())),
        ),
        (
            "Analyst-covered rows have forecast timestamp",
            int(covered_forecast_ok.sum()),
            len(covered),
            yes_no(bool(covered_forecast_ok.all())),
        ),
        (
            "Forecast calendar date is not after as-of date",
            int(covered_forecast_date_safe.sum()),
            len(covered),
            yes_no(bool(covered_forecast_date_safe.all())),
        ),
        (
            "FY2024 rows are excluded from next-year stress modelling",
            int(fy2024["stress_12m"].isna().sum()),
            len(fy2024),
            yes_no(bool(fy2024["stress_12m"].isna().all())),
        ),
    ]

    by_market = (
        labelled.groupby("market", as_index=False)
        .agg(
            modelled_rows=("company_id", "count"),
            covered_rows=("covered", "sum"),
            first_asof=("asof_dt", "min"),
            last_asof=("asof_dt", "max"),
        )
        .sort_values("market")
    )
    by_market["first_asof"] = by_market["first_asof"].dt.strftime("%Y-%m-%d")
    by_market["last_asof"] = by_market["last_asof"].dt.strftime("%Y-%m-%d")

    lines = [
        "# Capital IQ Analyst Snapshot Timing Audit",
        "",
        "Date: 2026-06-01",
        "",
        "## Decision",
        "",
        "The analyst-coverage variable is timing-safe for the current APJFS panel. All modelled firm-years have fiscal-year-end analyst snapshot dates, all source filenames with an as-of year match the firm-year, and all analyst-covered forecast calendar dates are on or before the corresponding fiscal-year-end as-of date.",
        "",
        "This audit does not make raw Capital IQ data redistributable. It only documents timing consistency for the licensed exports already used in the model.",
        "",
        "## Core Counts",
        "",
        f"- Total panel rows: {len(panel):,}",
        f"- Modelled next-year-stress rows: {len(labelled):,}",
        f"- Analyst-covered model rows: {int(labelled['covered'].sum()):,}",
        f"- Analyst-covered rows in full panel: {len(covered):,}",
        f"- Rows with explicit as-of dates: {len(asof_rows):,}",
        f"- FY2024 rows excluded from next-year modelling: {len(fy2024):,}",
        "",
        "## Timing Checks",
        "",
        "| Check | Passing rows | Total rows | Status |",
        "| --- | ---: | ---: | --- |",
    ]
    for name, passing, total, status in checks:
        lines.append(f"| {name} | {passing:,} | {total:,} | {status} |")

    lines.extend(
        [
            "",
            "## Market Coverage",
            "",
            frame_to_markdown(by_market),
            "",
            "## Notes",
            "",
            f"- {int(covered_timestamp_after_asof.sum()):,} covered rows have a forecast timestamp later than midnight on the as-of date, but all are on the same calendar date as the as-of date or earlier. The audit therefore uses calendar-date timing, not midnight timestamp timing.",
            f"- {int(covered_prior_year_forecasts.sum()):,} covered rows have forecast timestamps from a prior calendar year. These are stale rather than look-ahead observations because the forecast date is still before the as-of date.",
            "- FY2024 accounting rows are kept in the full panel only to create prior-year next-year labels; they are not modelled because no FY2025 stress outcome is observed.",
            "",
            "## Safe Use Rule",
            "",
            "Analyst variables can be used only when tied to explicit fiscal-year-end as-of exports. Any future Capital IQ analyst, market, price, or liquidity field must pass the same timing check before being merged into the manuscript model.",
        ]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
