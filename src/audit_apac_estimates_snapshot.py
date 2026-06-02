#!/usr/bin/env python3
"""Audit APAC Capital IQ estimates snapshot coverage by exchange."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_quality_check import read_xlsx_stdlib


RAW = Path("data/raw/capital_iq/capital_iq_estimates_snapshot_apac_public_exchange_notna_20260531.xlsx")
OUT_CSV = Path("outputs/tables/apac_estimates_snapshot_by_exchange.csv")
OUT_MD = Path("outputs/apac_estimates_snapshot_coverage.md")


def main() -> int:
    df = read_xlsx_stdlib(RAW).iloc[1:].copy()
    numeric = [
        "SP_EPS_EST_NUM_ANALYSTS_MONTH",
        "SP_EPS_HIGH_EST",
        "SP_EPS_EST",
        "SP_EPS_LOW_EST",
        "SP_EPS_STDDEV_EST",
        "SP_EPS_NUM_EST",
    ]
    for col in numeric:
        df[col] = pd.to_numeric(df[col].replace({"NA": np.nan, "": np.nan}), errors="coerce")
    df["covered"] = df[numeric].notna().any(axis=1)
    df["dispersion_nonmissing"] = df["SP_EPS_STDDEV_EST"].notna()
    agg = (
        df.groupby("SP_EXCHANGE", dropna=False)
        .agg(
            firms=("SP_ENTITY_ID", "nunique"),
            covered=("covered", "sum"),
            dispersion_nonmissing=("dispersion_nonmissing", "sum"),
        )
        .reset_index()
    )
    agg["coverage_pct"] = agg["covered"] / agg["firms"] * 100
    agg["dispersion_pct"] = agg["dispersion_nonmissing"] / agg["firms"] * 100
    agg = agg.sort_values(["covered", "coverage_pct"], ascending=False)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    agg.to_csv(OUT_CSV, index=False)

    top = agg.head(20).copy()
    lines = [
        "# APAC Estimates Snapshot Coverage",
        "",
        "Source file: `data/raw/capital_iq/capital_iq_estimates_snapshot_apac_public_exchange_notna_20260531.xlsx`.",
        "",
        "This is a point-in-time APAC coverage audit. It is not a leakage-safe historical panel, but it is useful for deciding which markets to export next if the Singapore-only AEL route is underpowered.",
        "",
        "## Top Exchanges by Analyst Coverage",
        "",
        top.to_markdown(index=False, floatfmt=".2f"),
        "",
        "## Execution Implication",
        "",
        "- Singapore mainboard has workable snapshot coverage, but the first historical export produced only 135 covered firm-years and 34 covered stress events.",
        "- If historical Singapore coverage remains near this level, the AEL submission should expand to ASX, SEHK, TSE, SZSE/SHSE, NSEI, KLSE, SET or KOSE rather than stay Singapore-only.",
        "- The AEL claim must remain APAC/Singapore evidence only after historical as-of exports confirm adequate analyst-covered stress events.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved: {OUT_CSV}")
    print(f"Saved: {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
