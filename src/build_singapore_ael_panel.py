#!/usr/bin/env python3
"""Build the Singapore AEL firm-year panel with historical analyst estimates.

Capital IQ exports may place the estimates report on different worksheets. This
script scans each workbook for the Capital IQ alias row, reads the estimates
sheet from files named with an as-of date, then merges those leakage-safe
analyst variables into the existing accounting panel.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_quality_check import read_xlsx_stdlib


RAW_DIR = Path("data/raw/capital_iq")
PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs")
ACCOUNTING_PANEL = PROCESSED_DIR / "singapore_financials_firm_year_pilot.csv"
PANEL_OUT = PROCESSED_DIR / "ael_singapore_firm_year_panel.csv"
ESTIMATES_OUT = PROCESSED_DIR / "singapore_estimates_firm_year.csv"

FIELD_ALIASES = {
    "SP_ENTITY_NAME": "company_name",
    "SP_ENTITY_ID": "company_id",
    "SP_EPS_STDDEV_EST": "eps_stddev",
    "SP_EPS_HIGH_EST": "eps_high",
    "SP_EPS_LOW_EST": "eps_low",
    "SP_EPS_NUM_EST": "num_analysts",
    "SP_EPS_EST": "eps_est",
    "SP_EPS_DATE_OF_EST": "forecast_date",
}


def parse_number(value: object) -> float:
    text = str(value).strip()
    if not text or text.upper() in {"NA", "NM", "N/A", "NONE", "NULL"}:
        return np.nan
    text = text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return np.nan


def parse_excel_date(value: object) -> pd.Timestamp:
    number = parse_number(value)
    if pd.notna(number):
        return pd.to_datetime(number, unit="D", origin="1899-12-30", errors="coerce")
    return pd.to_datetime(value, errors="coerce")


def asof_year_from_name(path: Path) -> int | None:
    match = re.search(r"asof_(20\d{2})1231", path.name)
    return int(match.group(1)) if match else None


def estimate_files() -> list[Path]:
    return sorted(RAW_DIR.glob("capital_iq_estimates_singapore_fyplus1_asof_*_*.xlsx"))


def worksheet_numbers(path: Path) -> list[int]:
    """Return actual worksheet numbers instead of relying on reader fallback."""
    with zipfile.ZipFile(path) as zf:
        numbers = []
        for name in zf.namelist():
            match = re.fullmatch(r"xl/worksheets/sheet(\d+)\.xml", name)
            if match:
                numbers.append(int(match.group(1)))
    return sorted(numbers)


def has_estimates_aliases(raw: pd.DataFrame) -> bool:
    if raw.empty or raw.shape[0] < 4:
        return False
    aliases = set(raw.iloc[0].astype(str).str.strip())
    return "SP_ENTITY_ID" in aliases and bool(
        aliases
        & {
            "SP_EPS_STDDEV_EST",
            "SP_EPS_HIGH_EST",
            "SP_EPS_LOW_EST",
            "SP_EPS_NUM_EST",
            "SP_EPS_EST",
            "SP_EPS_DATE_OF_EST",
        }
    )


def read_estimates_file(path: Path) -> pd.DataFrame:
    asof_year = asof_year_from_name(path)
    if asof_year is None:
        return pd.DataFrame()

    raw = pd.DataFrame()
    sheet_no = None
    for candidate in worksheet_numbers(path):
        candidate_raw = read_xlsx_stdlib(path, sheet_no=candidate)
        if has_estimates_aliases(candidate_raw):
            raw = candidate_raw
            sheet_no = candidate
            break
    if raw.empty:
        return pd.DataFrame()

    alias_row = raw.iloc[0].astype(str).str.strip()
    data = raw.iloc[3:].copy()
    data.columns = [FIELD_ALIASES.get(alias, alias) for alias in alias_row]
    keep = [c for c in FIELD_ALIASES.values() if c in data.columns]
    out = data[keep].copy()
    if "company_id" not in out.columns:
        return pd.DataFrame()

    out["company_id"] = out["company_id"].astype(str).str.strip()
    out = out[out["company_id"].ne("")]
    out["fiscal_year"] = asof_year
    out["as_of_date"] = f"{asof_year}-12-31"
    for col in ["eps_stddev", "eps_high", "eps_low", "num_analysts", "eps_est"]:
        if col in out.columns:
            out[col] = out[col].map(parse_number)
        else:
            out[col] = np.nan
    if "forecast_date" in out.columns:
        out["forecast_date"] = out["forecast_date"].map(parse_excel_date)
    else:
        out["forecast_date"] = pd.NaT

    denominator = out["eps_est"].abs().replace(0, np.nan)
    out["analyst_dispersion"] = out["eps_stddev"] / denominator
    out["forecast_high_low_spread"] = (out["eps_high"] - out["eps_low"]) / denominator
    out["analyst_covered"] = (
        out[["eps_stddev", "eps_high", "eps_low", "num_analysts", "eps_est"]].notna().any(axis=1)
    ).astype(int)
    out["source_file"] = path.name
    out["source_sheet"] = sheet_no
    return out.drop_duplicates(["company_id", "fiscal_year"], keep="first")


def build_estimates_panel() -> pd.DataFrame:
    frames = [read_estimates_file(path) for path in estimate_files()]
    frames = [df for df in frames if not df.empty]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def write_summary(estimates: pd.DataFrame, panel: pd.DataFrame) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "singapore_ael_panel_summary.md"
    lines = [
        "# Singapore AEL Panel Build Summary",
        "",
        "This panel merges historical accounting stress labels with Capital IQ analyst estimates. Analyst variables are only valid for years with explicit as-of-date exports.",
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
                eps_stddev_nonmissing=("eps_stddev", lambda s: int(s.notna().sum())),
                num_analysts_nonmissing=("num_analysts", lambda s: int(s.notna().sum())),
            )
            .sort_values("fiscal_year")
        )
        cov["coverage_pct"] = cov["analyst_covered"] / cov["firms"] * 100
        lines.extend(["## Analyst Export Coverage", ""])
        lines.append(cov.to_markdown(index=False, floatfmt=".2f"))
    if not panel.empty:
        labelled = panel["stress_12m"].notna() if "stress_12m" in panel.columns else pd.Series(False)
        covered = panel["analyst_covered"].fillna(0).astype(bool) if "analyst_covered" in panel.columns else pd.Series(False)
        lines.extend(
            [
                "",
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
    parser = argparse.ArgumentParser(description="Build Singapore AEL analyst-accounting firm-year panel.")
    parser.add_argument("--accounting-panel", default=str(ACCOUNTING_PANEL))
    parser.add_argument("--panel-out", default=str(PANEL_OUT))
    parser.add_argument("--estimates-out", default=str(ESTIMATES_OUT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    accounting_path = Path(args.accounting_panel)
    if not accounting_path.exists():
        raise FileNotFoundError(f"Accounting panel not found: {accounting_path}")

    accounting = pd.read_csv(accounting_path)
    accounting["company_id"] = accounting["company_id"].astype(str).str.strip()
    accounting["fiscal_year"] = pd.to_numeric(accounting["fiscal_year"], errors="coerce").astype("Int64")

    estimates = build_estimates_panel()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    estimates.to_csv(args.estimates_out, index=False)

    if estimates.empty:
        panel = accounting.copy()
        for col in [
            "eps_stddev",
            "eps_high",
            "eps_low",
            "num_analysts",
            "eps_est",
            "analyst_dispersion",
            "forecast_high_low_spread",
            "analyst_covered",
        ]:
            panel[col] = np.nan
    else:
        panel = accounting.merge(
            estimates.drop(columns=["company_name"], errors="ignore"),
            on=["company_id", "fiscal_year"],
            how="left",
            validate="many_to_one",
        )
        panel["analyst_covered"] = panel["analyst_covered"].fillna(0).astype(int)

    panel.to_csv(args.panel_out, index=False)
    summary_path = write_summary(estimates, panel)
    print(f"Saved: {args.estimates_out}")
    print(f"Saved: {args.panel_out}")
    print(f"Saved: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
