#!/usr/bin/env python3
"""Run logit robustness excluding direct financial-stress label components."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ael_logit_inference import estimate


DEFAULT_PANEL = Path("data/processed/ael_singapore_firm_year_panel.csv")
OUT = Path("outputs/tables/table4_label_component_robustness.csv")

CONSERVATIVE_CONTROLS = [
    "roa",
    "leverage",
    "revenue_growth",
    "log_assets",
]

EXCLUDED_AS_DIRECT_OR_NEAR_DIRECT = [
    "roe",
    "interest_coverage",
    "operating_margin",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate robustness models excluding direct stress-label components."
    )
    parser.add_argument("--panel", default=str(DEFAULT_PANEL))
    parser.add_argument("--target", default="stress_12m")
    parser.add_argument("--output", default=str(OUT))
    parser.add_argument(
        "--fixed-effects",
        nargs="*",
        default=[],
        help="Optional categorical fixed effects passed to the logit estimator.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    panel = pd.read_csv(args.panel, low_memory=False)
    fixed_effects = [c for c in args.fixed_effects if c in panel.columns]
    controls = [c for c in CONSERVATIVE_CONTROLS if c in panel.columns]
    rows = [
        estimate(panel, args.target, controls, "Conservative controls", fixed_effects),
    ]
    if "analyst_covered" in panel.columns:
        rows.append(
            estimate(
                panel,
                args.target,
                controls + ["analyst_covered"],
                "Conservative controls + analyst coverage",
                fixed_effects,
            )
        )
    out = pd.concat(rows, ignore_index=True)
    out["excluded_direct_or_near_direct_controls"] = ", ".join(
        [c for c in EXCLUDED_AS_DIRECT_OR_NEAR_DIRECT if c in panel.columns]
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(f"Saved: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
