#!/usr/bin/env python3
"""Audit Capital IQ market fields before using them as panel predictors."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_quality_check import read_xlsx_stdlib


RAW_DIR = Path("data/raw/capital_iq")
DOWNLOADS = Path.home() / "Downloads"
OUT = Path("outputs/capital_iq_market_field_leakage_audit_20260601.md")
ALIASES = {"SP_MARKETCAP", "SPTR_TARGET_MARKETCAP"}


def markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for _, row in frame.iterrows():
        values = [str(row[col]).replace("\n", " ") if pd.notna(row[col]) else "" for col in columns]
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def worksheet_numbers(path: Path) -> list[int]:
    with zipfile.ZipFile(path) as zf:
        numbers = []
        for name in zf.namelist():
            match = re.fullmatch(r"xl/worksheets/sheet(\d+)\.xml", name)
            if match:
                numbers.append(int(match.group(1)))
    return sorted(numbers)


def classify_context(row1: object, row2: object) -> str:
    context = " ".join(str(x) for x in [row1, row2] if pd.notna(x)).strip()
    if re.search(r"\bFY\s*(19|20)\d{2}\b", context, flags=re.I):
        return "fiscal-year-labelled"
    if re.search(r"\b(19|20)\d{2}[-/]\d{1,2}[-/]\d{1,2}\b", context):
        return "date-labelled"
    if re.search(r"\b\d{1,2}[-/]\d{1,2}[-/](19|20)\d{2}\b", context):
        return "date-labelled"
    if context:
        return "non-panel-context"
    return "no-date-or-period-label"


def audit_file(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sheet_no in worksheet_numbers(path):
        raw = read_xlsx_stdlib(path, sheet_no=sheet_no)
        if raw.empty:
            continue
        candidate_rows = [[str(c).strip() for c in raw.columns]]
        for idx in range(min(3, len(raw))):
            candidate_rows.append(raw.iloc[idx].astype(str).str.strip().tolist())
        for aliases in candidate_rows:
            for col_idx, alias in enumerate(aliases):
                if alias not in ALIASES:
                    continue
                label = raw.columns[col_idx] if col_idx < len(raw.columns) else ""
                row1 = raw.iloc[0, col_idx] if len(raw) > 0 else ""
                row2 = raw.iloc[1, col_idx] if len(raw) > 1 else ""
                rows.append(
                    {
                        "file": path.name,
                        "location": "raw" if RAW_DIR in path.parents else "downloads",
                        "sheet": sheet_no,
                        "column_index": col_idx,
                        "alias": alias,
                        "label_or_row0": str(label),
                        "row1": str(row1),
                        "row2": str(row2),
                        "context_class": classify_context(row1, row2),
                    }
                )
    return rows


def main() -> int:
    paths = sorted(RAW_DIR.glob("*.xlsx"))
    paths.extend(sorted(DOWNLOADS.glob("SPGlobal*.xlsx"), key=lambda p: p.stat().st_mtime, reverse=True)[:12])
    records: list[dict[str, object]] = []
    for path in paths:
        try:
            records.extend(audit_file(path))
        except Exception as exc:  # noqa: BLE001
            records.append(
                {
                    "file": path.name,
                    "location": "raw" if RAW_DIR in path.parents else "downloads",
                    "sheet": "",
                    "column_index": "",
                    "alias": "READ_ERROR",
                    "label_or_row0": type(exc).__name__,
                    "row1": str(exc),
                    "row2": "",
                    "context_class": "read-error",
                }
            )

    frame = pd.DataFrame(records).drop_duplicates()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Capital IQ Market Field Leakage Audit",
        "",
        "Date: 2026-06-01",
        "",
        "## Decision",
        "",
        "Do not add the currently available `SP_MARKETCAP` fields to the APJFS predictive panel. Safari/Capital IQ can display an explicit `12/31/2023` market-cap as-of-date field, but the exported proof-of-schema file covers only three peer-comparison companies and the market-cap values are `NA`. It is therefore not usable as a 2014-2023 panel control.",
        "",
        "## Rationale",
        "",
        "- A current, no-date market capitalization field would introduce post-outcome information if merged into historical firm-years.",
        "- Transaction target market-cap fields belong to deal screens, not the listed-firm accounting/analyst panel.",
        "- The new `capital_iq_peer_marketcap_asof_20231231_20260601.xlsx` export proves that a dated market-cap field exists in the interface, but it is only a three-company peer-comparison export and does not contain usable market-cap values.",
        "- The existing APJFS results therefore remain based on accounting fundamentals, analyst estimates, market fixed effects, and fiscal-year fixed effects.",
        "",
        "## Field Hits",
        "",
    ]
    if frame.empty:
        lines.append("No market-cap field aliases were found in the audited files.")
    else:
        display = frame[
            ["location", "file", "sheet", "column_index", "alias", "row1", "row2", "context_class"]
        ].sort_values(["location", "file", "sheet", "column_index"])
        lines.append(markdown_table(display))
    lines.append("")
    lines.append("## Safe Use Rule")
    lines.append("")
    lines.append("Only use market-cap, price, return, or liquidity controls if the export contains explicit predictor-date or fiscal-year/as-of-date labels, non-missing values, and the same company universe needed for the APJFS panel.")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved: {OUT}")
    if not frame.empty:
        print(frame["context_class"].value_counts().to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
