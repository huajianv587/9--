#!/usr/bin/env python3
"""Run the Applied Economics Letters modeling pipeline.

Input: a leakage-safe firm-quarter panel with a stress label and analyst variables.
Output: the three core AEL tables:

- outputs/tables/table1_sample_distribution.csv
- outputs/tables/table2_logit_results.csv
- outputs/tables/table3_prediction_robustness.csv

The script deliberately uses scikit-learn rather than requiring statsmodels or
xgboost. If xgboost is installed later, the sklearn fallback can be replaced, but
the AEL paper should still treat ML as secondary evidence.
"""

from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DEFAULT_PANEL = Path("data/processed/ael_firm_quarter_panel.parquet")
OUT_DIR = Path("outputs/tables")


ANALYST_FEATURES = [
    "analyst_covered",
    "analyst_dispersion",
    "eps_stddev",
    "forecast_high_low_spread",
    "num_analysts",
    "revision_30d",
    "revision_90d",
    "coverage_change",
]

ACCOUNTING_FEATURES = [
    "roa",
    "roe",
    "leverage",
    "current_ratio",
    "interest_coverage",
    "operating_margin",
    "revenue_growth",
    "cash_flow_to_assets",
    "log_assets",
]

MARKET_FEATURES = [
    "market_cap",
    "log_market_cap",
    "return_3m",
    "return_12m",
    "return_volatility",
    "market_to_book",
    "turnover",
]

CATEGORICAL_FEATURES = ["country", "sector", "exchange"]


def load_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Panel not found: {path}")
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path, low_memory=False)


def existing(cols: list[str], df: pd.DataFrame) -> list[str]:
    return [c for c in cols if c in df.columns]


def infer_time_col(df: pd.DataFrame) -> str | None:
    for c in ["fiscal_quarter", "fiscal_period_end", "period", "date", "year_quarter"]:
        if c in df.columns:
            return c
    return None


def make_table1(df: pd.DataFrame, target: str) -> pd.DataFrame:
    group_col = "country" if "country" in df.columns else "exchange" if "exchange" in df.columns else None
    if "analyst_covered" in df.columns:
        analyst_available = pd.to_numeric(df["analyst_covered"], errors="coerce").fillna(0).astype(bool)
    else:
        analyst_cols = existing([c for c in ANALYST_FEATURES if c != "analyst_covered"], df)
        analyst_available = df[analyst_cols].notna().any(axis=1) if analyst_cols else pd.Series(False, index=df.index)
    if group_col:
        rows = []
        for market, g in df.groupby(group_col, dropna=False):
            idx = g.index
            rows.append(
                {
                    "market": market,
                    "firms": g["company_id"].nunique() if "company_id" in g.columns else np.nan,
                    "firm_periods": len(g),
                    "stress_events": int(pd.to_numeric(g[target], errors="coerce").fillna(0).sum()),
                    "analyst_covered_periods": int(analyst_available.loc[idx].sum()),
                    "stress_events_with_analyst": int(
                        (pd.to_numeric(g[target], errors="coerce").fillna(0).astype(bool) & analyst_available.loc[idx]).sum()
                    ),
                }
            )
        return pd.DataFrame(rows)
    return pd.DataFrame(
        [
            {
                "market": "All",
                "firms": df["company_id"].nunique() if "company_id" in df.columns else np.nan,
                "firm_periods": len(df),
                "stress_events": int(pd.to_numeric(df[target], errors="coerce").fillna(0).sum()),
                "analyst_covered_periods": int(analyst_available.sum()),
                "stress_events_with_analyst": int(
                    (pd.to_numeric(df[target], errors="coerce").fillna(0).astype(bool) & analyst_available).sum()
                ),
            }
        ]
    )


def preprocessor(df: pd.DataFrame, features: list[str]) -> ColumnTransformer:
    numeric_features = [c for c in features if c not in CATEGORICAL_FEATURES]
    cat_features = [c for c in features if c in CATEGORICAL_FEATURES]
    return ColumnTransformer(
        transformers=[
            ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric_features),
            ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), cat_features),
        ],
        remainder="drop",
    )


def model_frame(df: pd.DataFrame, target: str, features: list[str]) -> pd.DataFrame:
    use = df[[target] + features].copy()
    numeric_cols = [c for c in features if c not in CATEGORICAL_FEATURES]
    for col in numeric_cols:
        use[col] = pd.to_numeric(use[col], errors="coerce")
    use = use.replace([np.inf, -np.inf], np.nan)
    for col in numeric_cols:
        nonmissing = use[col].dropna()
        if col != "analyst_covered" and len(nonmissing) >= 20:
            lo, hi = nonmissing.quantile([0.01, 0.99])
            if pd.notna(lo) and pd.notna(hi) and lo < hi:
                use[col] = use[col].clip(lower=lo, upper=hi)
    return use


def fit_logit(df: pd.DataFrame, target: str, features: list[str], label: str) -> dict[str, object]:
    use = model_frame(df, target, features)
    y = pd.to_numeric(use[target], errors="coerce").fillna(0).astype(int)
    if y.nunique() < 2:
        return {"model": label, "error": "target has one class"}
    clf = Pipeline(
        [
            ("prep", preprocessor(df, features)),
            ("model", LogisticRegression(max_iter=2000, class_weight="balanced", solver="liblinear")),
        ]
    )
    clf.fit(use[features], y)
    pred = clf.predict_proba(use[features])[:, 1]
    return metrics_row(label, y, pred)


def metrics_row(label: str, y: pd.Series, pred: np.ndarray) -> dict[str, object]:
    hard = (pred >= 0.5).astype(int)
    return {
        "model": label,
        "n": int(len(y)),
        "events": int(y.sum()),
        "roc_auc": roc_auc_score(y, pred) if y.nunique() == 2 else np.nan,
        "pr_auc": average_precision_score(y, pred) if y.nunique() == 2 else np.nan,
        "brier": brier_score_loss(y, pred),
        "balanced_accuracy": balanced_accuracy_score(y, hard),
        "stress_f1": f1_score(y, hard, zero_division=0),
    }


def train_test_metrics(df: pd.DataFrame, target: str, features: list[str], label: str) -> dict[str, object]:
    use = model_frame(df, target, features)
    y = pd.to_numeric(use[target], errors="coerce").fillna(0).astype(int)
    if y.nunique() < 2 or y.sum() < 5:
        return {"model": label, "error": "not enough target variation"}
    strat = y if y.value_counts().min() >= 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        use[features], y, test_size=0.25, random_state=42, stratify=strat
    )
    clf = Pipeline(
        [
            ("prep", preprocessor(df, features)),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    max_depth=6,
                    min_samples_leaf=20,
                    class_weight="balanced_subsample",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    clf.fit(x_train, y_train)
    pred = clf.predict_proba(x_test)[:, 1]
    row = metrics_row(label, y_test, pred)
    row["train_n"] = int(len(y_train))
    row["test_n"] = int(len(y_test))
    return row


def build_tables(panel: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if target not in panel.columns:
        raise ValueError(f"Target column not found: {target}")
    panel = panel.copy()
    target_numeric = pd.to_numeric(panel[target], errors="coerce")
    panel = panel[target_numeric.notna()].copy()
    panel[target] = target_numeric[target_numeric.notna()].astype(int)

    table1 = make_table1(panel, target)

    accounting_market = existing(ACCOUNTING_FEATURES + MARKET_FEATURES + CATEGORICAL_FEATURES, panel)
    analyst = existing(ANALYST_FEATURES, panel)
    full = accounting_market + analyst

    rows2 = []
    if accounting_market:
        rows2.append(fit_logit(panel, target, accounting_market, "Logit: accounting + market"))
    if full and analyst:
        rows2.append(fit_logit(panel, target, full, "Logit: accounting + market + analyst"))
    table2 = pd.DataFrame(rows2)

    rows3 = []
    if accounting_market:
        rows3.append(train_test_metrics(panel, target, accounting_market, "RF: accounting + market"))
    if full and analyst:
        rows3.append(train_test_metrics(panel, target, full, "RF: accounting + market + analyst"))
    if "strict_distress_12m" in panel.columns and "strict_distress_12m" != target and full:
        rows3.append(train_test_metrics(panel, "strict_distress_12m", full, "Robustness: strict distress"))
    if "num_analysts" in panel.columns and full:
        n = pd.to_numeric(panel["num_analysts"], errors="coerce")
        rows3.append(train_test_metrics(panel[n >= 2], target, full, "Robustness: analyst coverage >=2"))
        rows3.append(train_test_metrics(panel[n >= 3], target, full, "Robustness: analyst coverage >=3"))
    table3 = pd.DataFrame(rows3)

    return table1, table2, table3


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run AEL modeling tables.")
    p.add_argument("--panel", default=str(DEFAULT_PANEL))
    p.add_argument("--target", default="stress_12m")
    p.add_argument("--output-dir", default=str(OUT_DIR))
    return p.parse_args()


def main() -> int:
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="sklearn.utils.extmath")
    args = parse_args()
    panel_path = Path(args.panel)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_panel(panel_path)
    table1, table2, table3 = build_tables(df, args.target)
    table1.to_csv(output_dir / "table1_sample_distribution.csv", index=False)
    table2.to_csv(output_dir / "table2_logit_results.csv", index=False)
    table3.to_csv(output_dir / "table3_prediction_robustness.csv", index=False)

    print(f"Saved: {output_dir / 'table1_sample_distribution.csv'}")
    print(f"Saved: {output_dir / 'table2_logit_results.csv'}")
    print(f"Saved: {output_dir / 'table3_prediction_robustness.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
