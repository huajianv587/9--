#!/usr/bin/env python3
"""Build a Singapore firm-year financial-stress pilot panel.

This script intentionally builds only the accounting side of the AEL dataset.
It does not merge the latest Capital IQ Estimates snapshot into historical
years, because doing so would create forward-looking analyst variables.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_quality_check import read_xlsx_stdlib


RAW_DIR = Path("data/raw/capital_iq")
OUT_DIR = Path("data/processed")
TABLE_DIR = Path("outputs/tables")

FIELD_MAP = {
    "SP_TOTAL_EQUITY": "total_equity",
    "SP_TOTAL_ASSETS": "total_assets",
    "SP_TOTAL_REV": "revenue",
    "SP_EBIT": "ebit",
    "SP_INT_EXP": "interest_expense",
    "SP_NET_INC": "net_income",
    "SP_TOTAL_DEBT": "total_debt",
}

PRIMARY_FILES = [
    RAW_DIR / "capital_iq_historical_financials_singapore_part1_assets_revenue_ebit_20260531.xlsx",
    RAW_DIR / "capital_iq_historical_financials_singapore_financial_stress_report2_values_20260531.xlsx",
]

STATUS_FILE = RAW_DIR / "capital_iq_company_status_apac_public_exchange_notna_20260531.xlsx"


def parse_number(value: object) -> float:
    text = str(value).strip()
    if not text or text.upper() in {"NA", "NM", "N/A", "NONE", "NULL"}:
        return np.nan
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()").replace(",", "")
    try:
        out = float(text)
    except ValueError:
        return np.nan
    return -out if negative else out


def fy_from_period(period: object) -> int | None:
    match = re.search(r"\bFY\s*(20\d{2}|19\d{2})\b", str(period), flags=re.I)
    if not match:
        return None
    return int(match.group(1))


def source_files() -> list[Path]:
    files = [p for p in PRIMARY_FILES if p.exists()]
    if files:
        return files
    return sorted(RAW_DIR.glob("capital_iq_historical_financials_singapore*.xlsx"))


def read_status_lookup(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["company_id", "country", "exchange", "company_status", "ticker"])
    raw = read_xlsx_stdlib(path)
    if raw.empty:
        return pd.DataFrame(columns=["company_id", "country", "exchange", "company_status", "ticker"])
    alias = raw.iloc[0].astype(str).str.strip()
    data = raw.iloc[1:].copy()
    data.columns = alias
    rename = {
        "SP_ENTITY_ID": "company_id",
        "SP_GEOGRAPHY": "country",
        "SP_EXCHANGE": "exchange",
        "SP_COMPANY_STATUS": "company_status",
        "SP_TICKER": "ticker",
    }
    keep = [c for c in rename if c in data.columns]
    out = data[keep].rename(columns=rename)
    if "company_id" not in out.columns:
        return pd.DataFrame(columns=["company_id", "country", "exchange", "company_status", "ticker"])
    out["company_id"] = out["company_id"].astype(str).str.strip()
    out = out[out["company_id"].ne("")]
    return out.drop_duplicates("company_id")


def extract_long(path: Path, start_year: int, end_year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = read_xlsx_stdlib(path)
    if raw.shape[0] < 2:
        return pd.DataFrame(), pd.DataFrame()

    header_aliases = [str(c).strip() for c in raw.columns]
    row0_aliases = raw.iloc[0].astype(str).str.strip().tolist()
    header_score = sum(alias in FIELD_MAP or alias in {"SP_ENTITY_NAME", "SP_ENTITY_ID"} for alias in header_aliases)
    row0_score = sum(alias in FIELD_MAP or alias in {"SP_ENTITY_NAME", "SP_ENTITY_ID"} for alias in row0_aliases)
    if header_score >= row0_score and header_score > 0:
        aliases = header_aliases
        periods = raw.iloc[0].astype(str).str.strip().tolist()
        data = raw.iloc[1:].copy()
    else:
        if raw.shape[0] < 3:
            return pd.DataFrame(), pd.DataFrame()
        aliases = row0_aliases
        periods = raw.iloc[1].astype(str).str.strip().tolist()
        data = raw.iloc[2:].copy()

    name_idx = aliases.index("SP_ENTITY_NAME") if "SP_ENTITY_NAME" in aliases else 0
    id_idx = aliases.index("SP_ENTITY_ID") if "SP_ENTITY_ID" in aliases else 1

    records: list[dict[str, object]] = []
    audit: list[dict[str, object]] = []
    for idx, alias in enumerate(aliases):
        field = FIELD_MAP.get(alias)
        year = fy_from_period(periods[idx] if idx < len(periods) else "")
        if field is None or year is None or not (start_year <= year <= end_year):
            continue
        values = data.iloc[:, idx].map(parse_number)
        non_missing = int(values.notna().sum())
        audit.append(
            {
                "source_file": path.name,
                "field": field,
                "capital_iq_alias": alias,
                "year": year,
                "non_missing": non_missing,
                "rows": int(len(values)),
            }
        )
        for row_idx, value in values.items():
            if pd.isna(value):
                continue
            records.append(
                {
                    "company_name": str(data.iloc[data.index.get_loc(row_idx), name_idx]).strip(),
                    "company_id": str(data.iloc[data.index.get_loc(row_idx), id_idx]).strip(),
                    "fiscal_year": year,
                    "field": field,
                    "value": float(value),
                    "source_file": path.name,
                }
            )
    return pd.DataFrame(records), pd.DataFrame(audit)


def collapse_values(values: pd.Series) -> float:
    clean = pd.to_numeric(values, errors="coerce").dropna()
    if clean.empty:
        return np.nan
    # Duplicate Capital IQ columns are expected when two templates expose the
    # same item. The median avoids dependence on arbitrary column order.
    return float(clean.median())


def build_panel(start_year: int, end_year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    audits: list[pd.DataFrame] = []
    for path in source_files():
        long, audit = extract_long(path, start_year, end_year)
        if not long.empty:
            frames.append(long)
        if not audit.empty:
            audits.append(audit)

    if not frames:
        return pd.DataFrame(), pd.DataFrame()

    long_all = pd.concat(frames, ignore_index=True)
    audit_all = pd.concat(audits, ignore_index=True) if audits else pd.DataFrame()
    long_all = long_all[long_all["company_id"].ne("")]

    collapsed = (
        long_all.groupby(["company_id", "company_name", "fiscal_year", "field"], as_index=False)["value"]
        .agg(collapse_values)
    )
    panel = collapsed.pivot_table(
        index=["company_id", "company_name", "fiscal_year"],
        columns="field",
        values="value",
        aggfunc="first",
    ).reset_index()
    panel.columns.name = None

    status = read_status_lookup(STATUS_FILE)
    if not status.empty:
        panel = panel.merge(status, on="company_id", how="left")
    if "country" in panel.columns:
        panel["country"] = panel["country"].fillna("Singapore")
    else:
        panel["country"] = "Singapore"

    for col in FIELD_MAP.values():
        if col not in panel.columns:
            panel[col] = np.nan

    panel = panel.sort_values(["company_id", "fiscal_year"]).reset_index(drop=True)
    panel["roa"] = panel["net_income"] / panel["total_assets"].replace(0, np.nan)
    panel["roe"] = panel["net_income"] / panel["total_equity"].replace(0, np.nan)
    panel["leverage"] = panel["total_debt"] / panel["total_assets"].replace(0, np.nan)
    panel["operating_margin"] = panel["ebit"] / panel["revenue"].replace(0, np.nan)
    panel["log_assets"] = np.log(panel["total_assets"].where(panel["total_assets"] > 0))
    panel["interest_coverage"] = panel["ebit"] / panel["interest_expense"].abs().replace(0, np.nan)
    panel["revenue_growth"] = panel.groupby("company_id")["revenue"].pct_change(fill_method=None)

    panel["negative_equity"] = panel["total_equity"] < 0
    panel["operating_loss"] = panel["ebit"] < 0
    panel["interest_coverage_below_1_5"] = panel["interest_coverage"] < 1.5
    panel["financial_stress_current"] = (
        panel["negative_equity"] | panel["operating_loss"] | panel["interest_coverage_below_1_5"]
    ).astype(int)
    panel["stress_12m"] = panel.groupby("company_id")["financial_stress_current"].shift(-1)

    return panel, audit_all


def write_summary(panel: pd.DataFrame, audit: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "singapore_historical_financials_summary.md"
    lines = [
        "# Singapore Historical Financials Pilot Audit",
        "",
        "This is an accounting-only pilot panel. It is not yet the final Applied Economics Letters panel because historical analyst estimates have not been merged.",
        "",
        "## Panel Coverage",
        "",
    ]
    if panel.empty:
        lines.append("No panel rows were built.")
    else:
        labelled = panel["stress_12m"].notna()
        lines.extend(
            [
                f"- Firms: {panel['company_id'].nunique()}",
                f"- Firm-years: {len(panel)}",
                f"- Years: {int(panel['fiscal_year'].min())}-{int(panel['fiscal_year'].max())}",
                f"- Labelled firm-years for next-year stress: {int(labelled.sum())}",
                f"- Next-year stress events: {int(panel.loc[labelled, 'stress_12m'].sum())}",
                "",
                "## Field Non-Missing Counts",
                "",
            ]
        )
        for col in FIELD_MAP.values():
            lines.append(f"- {col}: {int(panel[col].notna().sum())}")
    if not audit.empty:
        field_audit = (
            audit.groupby("field", as_index=False)
            .agg(columns=("year", "count"), years=("year", "nunique"), non_missing=("non_missing", "sum"))
            .sort_values("field")
        )
        lines.extend(["", "## Export Field Audit", ""])
        for row in field_audit.to_dict("records"):
            lines.append(
                f"- {row['field']}: {int(row['columns'])} exported FY columns, {int(row['years'])} years, {int(row['non_missing'])} non-missing cells"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Singapore historical financial-stress pilot panel.")
    parser.add_argument("--start-year", type=int, default=2014)
    parser.add_argument("--end-year", type=int, default=2024)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    panel, audit = build_panel(args.start_year, args.end_year)
    panel_path = OUT_DIR / "singapore_financials_firm_year_pilot.csv"
    audit_path = TABLE_DIR / "singapore_historical_financials_audit.csv"
    panel.to_csv(panel_path, index=False)
    audit.to_csv(audit_path, index=False)
    summary_path = write_summary(panel, audit, Path("outputs"))
    print(f"Saved: {panel_path}")
    print(f"Saved: {audit_path}")
    print(f"Saved: {summary_path}")
    if not panel.empty:
        labelled = panel["stress_12m"].notna()
        print(f"firms={panel['company_id'].nunique()} firm_years={len(panel)} labelled={int(labelled.sum())} events={int(panel.loc[labelled, 'stress_12m'].sum())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
