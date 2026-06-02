#!/usr/bin/env python3
"""AEL route data audit for Capital IQ exports.

This replaces the older earnings-surprise checker. It is designed for the
Applied Economics Letters route:

    Analyst disagreement -> future financial stress/distress.

The script is intentionally tolerant of Capital IQ export column names. It
produces a Week-1 style audit report from whatever pilot CSV/XLSX files exist in
``data/raw/capital_iq`` and, when available, a processed firm-quarter panel.
"""

from __future__ import annotations

import argparse
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

import numpy as np
import pandas as pd


RAW_DIR = Path("data/raw/capital_iq")
OUTPUT_DIR = Path("outputs")
PROCESSED_PANEL = Path("data/processed/ael_apac_firm_year_panel.csv")


ALIASES = {
    "company_id": [
        "company_id",
        "company id",
        "companyid",
        "sp entity id",
        "iq company id",
        "ciq company id",
        "capital iq company id",
        "gvkey",
    ],
    "company_name": ["company_name", "company name", "name", "entity name", "sp entity name"],
    "ticker": ["ticker", "ticker symbol", "symbol", "sp ticker"],
    "country": ["country", "country/region", "market", "exchange country", "sp geography"],
    "exchange": ["exchange", "primary exchange", "listing exchange", "sp exchange"],
    "sector": ["sector", "gics sector", "industry sector"],
    "period": ["period", "fiscal quarter", "fiscal period", "fiscal_period_end", "report date", "date"],
    "status": ["company status", "status", "listing status", "sp company status"],
    "status_date": ["status date", "inactive date", "company status date"],
    "delisting_date": ["delisting date", "delisted date", "delisting_date"],
    "delisting_reason": ["delisting reason", "reason for delisting", "delisting_reason"],
    "bankruptcy_date": ["bankruptcy filing date", "bankruptcy date", "bankruptcy_filing_date"],
    "default_date": ["default event date", "default date", "debt default date"],
    "restructuring_date": ["restructuring date", "reorganization date"],
    "liquidation_date": ["liquidation date", "receivership date", "winding up date"],
    "rating": ["credit rating", "issuer credit rating", "rating"],
    "rating_date": ["credit rating date", "rating date"],
    "num_analysts": [
        "number of analysts",
        "analyst count",
        "num_analysts",
        "num analysts",
        "sp eps est num analysts month",
        "sp eps num est",
    ],
    "eps_stddev": [
        "eps std dev",
        "forecast dispersion",
        "eps_stddev",
        "std dev",
        "standard deviation",
        "sp eps stddev est",
    ],
    "eps_high": ["eps high", "forecast high", "eps_high", "sp eps high est"],
    "eps_low": ["eps low", "forecast low", "eps_low", "sp eps low est"],
    "revision_30d": ["30-day revision", "estimate revision 30d", "estimate_revision_30d", "revision 30d"],
    "revision_90d": ["90-day revision", "estimate revision 90d", "estimate_revision_90d", "revision 90d"],
    "forecast_date": ["forecast date", "estimate date", "forecast_date", "sp eps date of est"],
    "total_equity": ["total equity", "book equity", "shareholders equity", "total_equity", "sp total equity"],
    "ebit": ["ebit", "operating income", "operating_income", "sp ebit"],
    "interest_expense": ["interest expense", "interest_expense", "sp int exp"],
    "net_income": ["net income", "net_income", "sp net inc"],
    "revenue": ["revenue", "total revenue", "sp total rev"],
    "total_assets": ["total assets", "total_assets", "sp total assets"],
    "total_debt": ["total debt", "total_debt", "sp total debt"],
    "market_cap": ["market cap", "market capitalization", "market_cap", "sp marketcap"],
    "currency": ["currency", "reported currency code", "sp currency financials"],
    "return_3m": ["3 month return", "3-month return", "total_return_3m", "return_3m"],
    "return_12m": ["12 month return", "12-month return", "total_return_12m", "return_12m"],
    "volatility": ["return volatility", "volatility", "return_volatility_12m"],
}


DISTRESS_TERMS = re.compile(
    r"bankrupt|insolven|default|restructur|receivership|liquidat|winding|distress|administration",
    re.I,
)
NON_DISTRESS_DELIST_TERMS = re.compile(
    r"merger|acqui|takeover|privati[sz]ation|voluntary|transfer|administrative|duplicate|name change",
    re.I,
)


def norm_name(name: str) -> str:
    return re.sub(r"\s+", " ", str(name).strip().lower().replace("_", " "))


def find_col(df: pd.DataFrame, key: str) -> str | None:
    normalized = {norm_name(c): c for c in df.columns}
    for alias in ALIASES[key]:
        if norm_name(alias) in normalized:
            return normalized[norm_name(alias)]
    return None


def numeric(s: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    if isinstance(s, pd.DataFrame):
        return s.apply(lambda col: numeric(col))
    return pd.to_numeric(s.astype(str).str.replace(",", "", regex=False), errors="coerce")


def date_series(s: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    if isinstance(s, pd.DataFrame):
        return s.apply(lambda col: date_series(col))
    return pd.to_datetime(s, errors="coerce")


def named_columns(df: pd.DataFrame, col: str) -> pd.DataFrame:
    selected = df.loc[:, df.columns == col]
    if selected.empty:
        value = df[col]
        if isinstance(value, pd.DataFrame):
            return value
        return value.to_frame()
    return selected


def first_named_column(df: pd.DataFrame, col: str) -> pd.Series:
    return named_columns(df, col).iloc[:, 0]


def any_numeric(df: pd.DataFrame, col: str, op: str, threshold: float = 0.0) -> pd.Series:
    values = numeric(named_columns(df, col))
    if op == "gt":
        mask = values > threshold
    elif op == "lt":
        mask = values < threshold
    elif op == "notna":
        mask = values.notna()
    else:
        raise ValueError(f"unsupported numeric op: {op}")
    return mask.any(axis=1)


def any_date_or_term(df: pd.DataFrame, col: str, pattern: re.Pattern[str]) -> pd.Series:
    values = named_columns(df, col)
    dates = date_series(values).notna().any(axis=1)
    terms = values.astype(str).apply(lambda s: s.str.contains(pattern, na=False)).any(axis=1)
    return dates | terms


def any_text_contains(df: pd.DataFrame, col: str, pattern: re.Pattern[str]) -> pd.Series:
    return named_columns(df, col).astype(str).apply(lambda s: s.str.contains(pattern, na=False)).any(axis=1)


def pct(num: float, den: float) -> float:
    return float(num) / float(den) * 100 if den else np.nan


def _xlsx_col_index(cell_ref: str) -> int:
    letters = re.sub(r"[^A-Z]", "", cell_ref.upper())
    out = 0
    for ch in letters:
        out = out * 26 + (ord(ch) - ord("A") + 1)
    return out - 1


def _xlsx_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    shared: list[str] = []
    for item in root.findall("a:si", ns):
        shared.append("".join(t.text or "" for t in item.findall(".//a:t", ns)))
    return shared


def _xlsx_cell_text(cell: ET.Element, shared: list[str], ns: dict[str, str]) -> str:
    cell_type = cell.get("t")
    if cell_type == "s":
        value = cell.find("a:v", ns)
        if value is not None and value.text is not None:
            idx = int(value.text)
            return shared[idx] if 0 <= idx < len(shared) else ""
        return ""
    if cell_type == "inlineStr":
        inline = cell.find("a:is", ns)
        return "" if inline is None else "".join(t.text or "" for t in inline.findall(".//a:t", ns))
    value = cell.find("a:v", ns)
    return "" if value is None or value.text is None else value.text


def _best_header_row(rows: list[list[str]]) -> int:
    keywords = re.compile(
        r"entity|company|ticker|exchange|status|date|analyst|estimate|forecast|eps|"
        r"equity|assets|revenue|income|ebit|market|return|rating|default|delist",
        re.I,
    )
    best_idx = 0
    best_score = -1
    for idx, row in enumerate(rows[:50]):
        nonempty = [str(x).strip() for x in row if str(x).strip()]
        if len(nonempty) < 2:
            continue
        score = sum(bool(keywords.search(x)) for x in nonempty) * 10 + len(nonempty)
        if score > best_score:
            best_idx = idx
            best_score = score
    return best_idx


def read_xlsx_stdlib(path: Path, sheet_no: int = 1) -> pd.DataFrame:
    """Read a simple Capital IQ XLSX export without optional Excel packages."""
    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        sheet_name = f"xl/worksheets/sheet{sheet_no}.xml"
        if sheet_name not in zf.namelist():
            sheet_name = next(name for name in zf.namelist() if name.startswith("xl/worksheets/sheet"))
        shared = _xlsx_shared_strings(zf)
        root = ET.fromstring(zf.read(sheet_name))

    rows: list[list[str]] = []
    for row in root.findall(".//a:sheetData/a:row", ns):
        values: list[str] = []
        for cell in row.findall("a:c", ns):
            idx = _xlsx_col_index(cell.get("r", "A1"))
            while len(values) <= idx:
                values.append("")
            values[idx] = _xlsx_cell_text(cell, shared, ns)
        while values and values[-1] == "":
            values.pop()
        rows.append(values)

    if not rows:
        return pd.DataFrame()
    header_idx = _best_header_row(rows)
    header = [str(x).strip() or f"unnamed_{i}" for i, x in enumerate(rows[header_idx])]
    width = len(header)
    records = []
    for row in rows[header_idx + 1 :]:
        padded = (row + [""] * width)[:width]
        if any(str(x).strip() for x in padded):
            records.append(padded)
    return pd.DataFrame(records, columns=header)


def read_table(path: Path) -> pd.DataFrame | None:
    try:
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() == ".xlsx":
            return read_xlsx_stdlib(path)
        if path.suffix.lower() == ".xls":
            return pd.read_excel(path)
    except Exception as exc:
        print(f"WARNING: failed to read {path}: {exc}")
    return None


@dataclass
class TableInfo:
    path: Path
    rows: int
    cols: int
    role: str
    mapped: dict[str, str | None]


def classify_table(df: pd.DataFrame) -> tuple[str, dict[str, str | None]]:
    mapped = {k: find_col(df, k) for k in ALIASES}
    score_events = sum(mapped[k] is not None for k in ["status", "delisting_reason", "bankruptcy_date", "default_date"])
    score_estimates = sum(mapped[k] is not None for k in ["num_analysts", "eps_stddev", "eps_high", "eps_low", "revision_30d"])
    score_financials = sum(mapped[k] is not None for k in ["total_equity", "ebit", "interest_expense", "net_income", "total_assets"])
    score_market = sum(mapped[k] is not None for k in ["market_cap", "return_3m", "return_12m", "volatility"])
    scores = {
        "events": score_events,
        "estimates": score_estimates,
        "financials": score_financials,
        "market": score_market,
    }
    best = max(scores, key=scores.get)
    return (best if scores[best] > 0 else "unknown"), mapped


def table_inventory(raw_dir: Path) -> tuple[list[TableInfo], dict[Path, pd.DataFrame]]:
    files = sorted(
        p for p in raw_dir.glob("**/*") if p.suffix.lower() in {".csv", ".xlsx", ".xls"}
    )
    infos: list[TableInfo] = []
    data: dict[Path, pd.DataFrame] = {}
    for path in files:
        df = read_table(path)
        if df is None:
            continue
        role, mapped = classify_table(df)
        infos.append(TableInfo(path, len(df), len(df.columns), role, mapped))
        data[path] = df
    return infos, data


def company_count(df: pd.DataFrame, mapped: dict[str, str | None]) -> int:
    col = mapped.get("company_id") or mapped.get("company_name") or mapped.get("ticker")
    return int(first_named_column(df, col).nunique(dropna=True)) if col else 0


def audit_events(tables: list[tuple[pd.DataFrame, dict[str, str | None]]]) -> dict[str, object]:
    rows = []
    potential_strict = 0
    distress_delist = 0
    non_distress_delist = 0
    companies = set()
    for df, m in tables:
        id_col = m.get("company_id") or m.get("company_name") or m.get("ticker")
        if id_col:
            companies.update(first_named_column(df, id_col).dropna().astype(str).unique())
        strict_mask = pd.Series(False, index=df.index)
        for key in ["bankruptcy_date", "default_date", "restructuring_date", "liquidation_date"]:
            col = m.get(key)
            if col:
                strict_mask |= any_date_or_term(df, col, DISTRESS_TERMS)
        status_col = m.get("status")
        if status_col:
            strict_mask |= any_text_contains(df, status_col, DISTRESS_TERMS)
        reason_col = m.get("delisting_reason")
        if reason_col:
            dist_terms = any_text_contains(df, reason_col, DISTRESS_TERMS)
            nondist = any_text_contains(df, reason_col, NON_DISTRESS_DELIST_TERMS)
            dist = dist_terms & ~nondist
            strict_mask |= dist
            distress_delist += int(dist.sum())
            non_distress_delist += int(nondist.sum())
        potential_strict += int(strict_mask.sum())
        if len(df):
            rows.append({"rows": len(df), "potential_strict_rows": int(strict_mask.sum())})
    return {
        "event_tables": len(tables),
        "event_companies": len(companies),
        "potential_strict_rows": potential_strict,
        "distress_delisting_rows": distress_delist,
        "non_distress_delisting_rows": non_distress_delist,
        "table_rows": rows,
    }


def audit_estimates(tables: list[tuple[pd.DataFrame, dict[str, str | None]]]) -> dict[str, object]:
    total_rows = 0
    covered_rows = 0
    dispersion_rows = 0
    companies = set()
    for df, m in tables:
        total_rows += len(df)
        id_col = m.get("company_id") or m.get("company_name") or m.get("ticker")
        if id_col:
            companies.update(first_named_column(df, id_col).dropna().astype(str).unique())
        analyst_col = m.get("num_analysts")
        if analyst_col:
            covered_rows += int(any_numeric(df, analyst_col, "gt", 0).sum())
        dispersion_col = m.get("eps_stddev")
        if dispersion_col:
            dispersion_rows += int(any_numeric(df, dispersion_col, "notna").sum())
        elif m.get("eps_high") and m.get("eps_low"):
            high = numeric(named_columns(df, m["eps_high"]))
            low = numeric(named_columns(df, m["eps_low"]))
            pair_count = min(high.shape[1], low.shape[1])
            if pair_count:
                dispersion_rows += int((high.iloc[:, :pair_count] - low.iloc[:, :pair_count]).notna().any(axis=1).sum())
    return {
        "estimate_tables": len(tables),
        "estimate_companies": len(companies),
        "estimate_rows": total_rows,
        "analyst_covered_rows": covered_rows,
        "analyst_coverage_rate": pct(covered_rows, total_rows),
        "dispersion_available_rows": dispersion_rows,
        "dispersion_available_rate": pct(dispersion_rows, total_rows),
    }


def audit_financial_stress(tables: list[tuple[pd.DataFrame, dict[str, str | None]]]) -> dict[str, object]:
    total_rows = 0
    stress_rows = 0
    components = {
        "negative_equity": 0,
        "interest_coverage_below_1_5": 0,
        "operating_loss": 0,
    }
    companies = set()
    for df, m in tables:
        total_rows += len(df)
        id_col = m.get("company_id") or m.get("company_name") or m.get("ticker")
        if id_col:
            companies.update(first_named_column(df, id_col).dropna().astype(str).unique())
        mask = pd.Series(False, index=df.index)
        if m.get("total_equity"):
            neg = any_numeric(df, m["total_equity"], "lt", 0)
            components["negative_equity"] += int(neg.sum())
            mask |= neg
        if m.get("ebit") and m.get("interest_expense"):
            ebit = numeric(named_columns(df, m["ebit"]))
            interest = numeric(named_columns(df, m["interest_expense"])).abs().replace(0, np.nan)
            pair_count = min(ebit.shape[1], interest.shape[1])
            low_ic = pd.Series(False, index=df.index)
            if pair_count:
                low_ic = ((ebit.iloc[:, :pair_count] / interest.iloc[:, :pair_count]) < 1.5).any(axis=1)
            components["interest_coverage_below_1_5"] += int(low_ic.sum())
            mask |= low_ic
        if m.get("net_income"):
            loss = any_numeric(df, m["net_income"], "lt", 0)
            components["operating_loss"] += int(loss.sum())
            mask |= loss
        stress_rows += int(mask.sum())
    return {
        "financial_tables": len(tables),
        "financial_companies": len(companies),
        "financial_rows": total_rows,
        "observable_stress_rows": stress_rows,
        "observable_stress_rate": pct(stress_rows, total_rows),
        **components,
    }


def audit_panel(panel_path: Path) -> dict[str, object] | None:
    if not panel_path.exists():
        return None
    df = pd.read_parquet(panel_path) if panel_path.suffix == ".parquet" else pd.read_csv(panel_path, low_memory=False)
    out: dict[str, object] = {"panel_path": str(panel_path), "panel_rows": len(df), "panel_cols": len(df.columns)}
    if "company_id" in df.columns:
        out["panel_companies"] = int(df["company_id"].nunique(dropna=True))
    for target in ["stress_12m", "strict_distress_12m"]:
        if target in df.columns:
            out[f"{target}_events"] = int(pd.to_numeric(df[target], errors="coerce").fillna(0).sum())
            out[f"{target}_rate"] = pct(out[f"{target}_events"], len(df))
    if "analyst_covered" in df.columns:
        analyst_available = pd.to_numeric(df["analyst_covered"], errors="coerce").fillna(0).gt(0)
        out["panel_analyst_coverage_rate"] = pct(int(analyst_available.sum()), len(df))
    else:
        analyst_cols = [c for c in ["analyst_dispersion", "eps_stddev", "num_analysts"] if c in df.columns]
        if analyst_cols:
            analyst_available = df[analyst_cols].notna().any(axis=1)
            out["panel_analyst_coverage_rate"] = pct(int(analyst_available.sum()), len(df))
    return out


def gate_status(events: dict[str, object], estimates: dict[str, object], financials: dict[str, object], panel: dict[str, object] | None) -> tuple[str, list[str]]:
    notes: list[str] = []
    stress_count = 0
    strict_count = 0
    if panel:
        stress_count = int(panel.get("stress_12m_events", 0) or 0)
        strict_count = int(panel.get("strict_distress_12m_events", 0) or 0)
        analyst_rate = float(panel.get("panel_analyst_coverage_rate", np.nan))
    else:
        stress_count = int(financials.get("observable_stress_rows", 0) or 0)
        strict_count = int(events.get("potential_strict_rows", 0) or 0)
        analyst_rate = float(estimates.get("analyst_coverage_rate", np.nan))

    if stress_count >= 300 or strict_count >= 150:
        notes.append("GREEN event/stress count gate")
        event_gate = "green"
    elif stress_count >= 200 or strict_count >= 80:
        notes.append("YELLOW event/stress count gate")
        event_gate = "yellow"
    else:
        notes.append("RED event/stress count gate")
        event_gate = "red"

    if analyst_rate >= 30:
        notes.append("GREEN analyst coverage gate")
        analyst_gate = "green"
    elif analyst_rate >= 20:
        notes.append("YELLOW analyst coverage gate")
        analyst_gate = "yellow"
    else:
        notes.append("RED analyst coverage gate")
        analyst_gate = "red"

    if event_gate == "green" and analyst_gate == "green":
        return "GREEN: proceed to panel/modeling", notes
    if event_gate == "red" or analyst_gate == "red":
        return "RED: do not write AEL manuscript yet; expand/export more data", notes
    return "YELLOW: adequate for conservative coverage framing; expand only if cheap", notes


def md_table(rows: Iterable[dict[str, object]]) -> str:
    rows = list(rows)
    if not rows:
        return "_No rows._"
    cols = list(rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(c, "")) for c in cols) + " |")
    return "\n".join(out)


def write_report(
    output_dir: Path,
    infos: list[TableInfo],
    events: dict[str, object],
    estimates: dict[str, object],
    financials: dict[str, object],
    panel: dict[str, object] | None,
    decision: str,
    notes: list[str],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "week1_event_coverage_report.md"
    inventory_rows = [
        {"file": str(i.path), "role": i.role, "rows": i.rows, "cols": i.cols, "companies": company_count(read_table(i.path), i.mapped) if i.path.exists() else ""}
        for i in infos
    ]
    pd.DataFrame(inventory_rows).to_csv(output_dir / "tables" / "raw_export_inventory.csv", index=False)
    lines = [
        "# Week 1 Capital IQ Event and Coverage Audit",
        "",
        "Generated by `data_quality_check.py`.",
        "",
        "## Decision",
        "",
        f"**{decision}**",
        "",
        "## Gate Notes",
        "",
        *[f"- {n}" for n in notes],
        "",
        "## Raw Export Inventory",
        "",
        md_table(inventory_rows),
        "",
        "## Event / Strict Distress Audit",
        "",
        md_table([{k: v for k, v in events.items() if k != "table_rows"}]),
        "",
        "## Analyst Estimates Coverage",
        "",
        md_table([estimates]),
        "",
        "## Financial Stress Proxy Audit",
        "",
        md_table([financials]),
        "",
        "## Processed Panel Audit",
        "",
        md_table([panel] if panel else []),
        "",
        "## Next Actions",
        "",
    ]
    if decision.startswith("GREEN"):
        lines += [
            "- Keep `data/processed/ael_apac_firm_year_panel.csv` as the current firm-year modelling panel.",
            "- Use the dedicated APJFS/AEL check scripts before upload; this Week-1 report is only a broad raw-export sanity audit.",
        ]
    elif decision.startswith("YELLOW"):
        lines += [
            "- Keep analyst coverage as the main information-environment variable; do not make forecast disagreement the title claim.",
            "- Treat the panel as adequate for conservative SCIE/SSCI submission, but do not call the coverage depth high.",
            "- Expand markets or years only if it is cheap and does not delay submission or introduce new data-license risk.",
        ]
    else:
        lines += [
            "- Do not write the AEL manuscript yet.",
            "- Export broader event/status data and analyst coverage data.",
            "- Expand APAC markets once before switching topic.",
        ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit Capital IQ exports for the AEL route.")
    p.add_argument("--raw-dir", default=str(RAW_DIR), help="Directory containing Capital IQ CSV/XLSX exports.")
    p.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for reports and tables.")
    p.add_argument("--panel", default=str(PROCESSED_PANEL), help="Optional processed panel path.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    output_dir = Path(args.output_dir)
    panel_path = Path(args.panel)

    infos, data = table_inventory(raw_dir)
    role_tables: dict[str, list[tuple[pd.DataFrame, dict[str, str | None]]]] = {
        "events": [],
        "estimates": [],
        "financials": [],
        "market": [],
        "unknown": [],
    }
    for info in infos:
        role_tables.setdefault(info.role, []).append((data[info.path], info.mapped))

    events = audit_events(role_tables.get("events", []))
    estimates = audit_estimates(role_tables.get("estimates", []))
    financials = audit_financial_stress(role_tables.get("financials", []))
    panel = audit_panel(panel_path)
    decision, notes = gate_status(events, estimates, financials, panel)
    report_path = write_report(output_dir, infos, events, estimates, financials, panel, decision, notes)

    print("=" * 72)
    print("AEL Capital IQ data audit")
    print("=" * 72)
    print(f"Raw dir: {raw_dir}")
    print(f"Files read: {len(infos)}")
    print(f"Decision: {decision}")
    for note in notes:
        print(f"- {note}")
    print(f"Report: {report_path}")
    return 0 if not decision.startswith("RED") else 1


if __name__ == "__main__":
    raise SystemExit(main())
