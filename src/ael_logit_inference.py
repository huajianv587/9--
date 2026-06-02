#!/usr/bin/env python3
"""Estimate compact logit coefficient tables for the AEL paper.

The local Python environment does not include statsmodels. This script uses
scipy directly and reports HC1 robust standard errors. It is intentionally
small because Applied Economics Letters needs a transparent main specification,
not a large predictive modeling system.
"""

from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit
from scipy.stats import norm


DEFAULT_PANEL = Path("data/processed/ael_singapore_firm_year_panel.csv")
OUT = Path("outputs/tables/table2a_logit_inference.csv")

ACCOUNTING_BASE = [
    "roa",
    "roe",
    "leverage",
    "interest_coverage",
    "operating_margin",
    "revenue_growth",
    "log_assets",
]

ANALYST_BASE = [
    "analyst_covered",
    "analyst_dispersion",
    "forecast_high_low_spread",
    "num_analysts",
]


def load_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, low_memory=False)


def winsorize(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce").replace([np.inf, -np.inf], np.nan)
    nonmissing = x.dropna()
    if len(nonmissing) < 20:
        return x
    qlo, qhi = nonmissing.quantile([lo, hi])
    if pd.notna(qlo) and pd.notna(qhi) and qlo < qhi:
        x = x.clip(qlo, qhi)
    return x


def prepare_matrix(
    df: pd.DataFrame,
    target: str,
    features: list[str],
    fixed_effects: list[str] | None = None,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    fixed_effects = fixed_effects or []
    use_cols = [target] + features + [c for c in fixed_effects if c not in features]
    use = df[use_cols].copy()
    target_numeric = pd.to_numeric(use[target], errors="coerce")
    use = use[target_numeric.notna()].copy()
    y = target_numeric[target_numeric.notna()].astype(int).to_numpy()

    cols: list[np.ndarray] = []
    names: list[str] = ["Intercept"]
    for col in features:
        x = winsorize(use[col])
        if col.startswith("analyst_") or col == "num_analysts":
            x = x.fillna(0)
        else:
            x = x.fillna(x.median())
        if col != "analyst_covered":
            sd = x.std(ddof=0)
            if pd.notna(sd) and sd > 0:
                x = (x - x.mean()) / sd
        if x.nunique(dropna=True) <= 1:
            continue
        cols.append(x.to_numpy(dtype=float))
        names.append(col)

    for col in fixed_effects:
        if col not in use.columns:
            continue
        labels = use[col].astype(str).str.strip().replace({"": "Missing", "nan": "Missing", "NaN": "Missing"})
        dummies = pd.get_dummies(labels, prefix=f"FE:{col}", drop_first=True, dtype=float)
        for dummy_col in dummies.columns:
            x = dummies[dummy_col]
            if x.nunique(dropna=True) <= 1:
                continue
            cols.append(x.to_numpy(dtype=float))
            names.append(dummy_col)

    X = np.column_stack([np.ones(len(y)), *cols])
    return X, y, names


def logit_fit(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    def linear_predictor(beta: np.ndarray) -> np.ndarray:
        b = np.nan_to_num(beta, nan=0.0, posinf=20.0, neginf=-20.0)
        b = np.clip(b, -20, 20)
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            xb = X @ b
        return np.nan_to_num(np.clip(xb, -35, 35), nan=0.0, posinf=35.0, neginf=-35.0)

    def objective(beta: np.ndarray) -> float:
        xb = linear_predictor(beta)
        return float(np.sum(np.logaddexp(0, xb) - y * xb))

    def gradient(beta: np.ndarray) -> np.ndarray:
        p = expit(linear_predictor(beta))
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            grad = X.T @ (p - y)
        return np.nan_to_num(grad, nan=0.0, posinf=0.0, neginf=0.0)

    result = minimize(
        objective,
        np.zeros(X.shape[1]),
        jac=gradient,
        method="L-BFGS-B",
        bounds=[(-20, 20)] * X.shape[1],
        options={"maxiter": 2000},
    )
    beta = np.nan_to_num(result.x, nan=0.0, posinf=20.0, neginf=-20.0)
    beta = np.clip(beta, -20, 20)
    p = np.clip(expit(linear_predictor(beta)), 1e-8, 1 - 1e-8)
    return beta, p


def robust_se(X: np.ndarray, y: np.ndarray, p: np.ndarray) -> np.ndarray:
    n, k = X.shape
    w = p * (1 - p)
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        hessian = X.T @ (X * w[:, None])
    hessian = np.nan_to_num(hessian, nan=0.0, posinf=0.0, neginf=0.0)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        bread = np.linalg.pinv(hessian, rcond=1e-10)
    bread = np.nan_to_num(bread, nan=0.0, posinf=0.0, neginf=0.0)
    resid = y - p
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        meat = X.T @ (X * (resid**2)[:, None])
    meat = np.nan_to_num(meat, nan=0.0, posinf=0.0, neginf=0.0)
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        cov = bread @ meat @ bread
    cov = np.nan_to_num(cov, nan=0.0, posinf=0.0, neginf=0.0)
    if n > k:
        cov *= n / (n - k)
    return np.sqrt(np.maximum(np.diag(cov), 0))


def estimate(
    df: pd.DataFrame,
    target: str,
    features: list[str],
    model: str,
    fixed_effects: list[str] | None = None,
) -> pd.DataFrame:
    fixed_effects = fixed_effects or []
    X, y, names = prepare_matrix(df, target, features, fixed_effects)
    if y.sum() < 10 or y.sum() > len(y) - 10:
        raise ValueError(f"Not enough target variation for {model}")
    beta, p = logit_fit(X, y)
    se = robust_se(X, y, p)
    z = beta / se
    pvalue = 2 * (1 - norm.cdf(np.abs(z)))
    return pd.DataFrame(
        {
            "model": model,
            "variable": names,
            "coef": beta,
            "robust_se": se,
            "z": z,
            "p_value": pvalue,
            "odds_ratio": np.exp(beta),
            "n": len(y),
            "events": int(y.sum()),
            "fixed_effects": ", ".join(fixed_effects) if fixed_effects else "none",
        }
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Estimate AEL logit inference tables.")
    parser.add_argument("--panel", default=str(DEFAULT_PANEL))
    parser.add_argument("--target", default="stress_12m")
    parser.add_argument("--output", default=str(OUT))
    parser.add_argument(
        "--fixed-effects",
        nargs="*",
        default=[],
        help="Optional categorical fixed effects, e.g. market fiscal_year.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    panel = load_panel(Path(args.panel))
    if args.target not in panel.columns:
        raise ValueError(f"Target column not found: {args.target}")
    fixed_effects = [c for c in args.fixed_effects if c in panel.columns]

    rows = []
    accounting = [c for c in ACCOUNTING_BASE if c in panel.columns]
    analyst = [c for c in ANALYST_BASE if c in panel.columns]
    rows.append(estimate(panel, args.target, accounting, "Accounting controls", fixed_effects))
    rows.append(estimate(panel, args.target, accounting + ["analyst_covered"], "Add analyst coverage", fixed_effects))

    covered = panel[pd.to_numeric(panel.get("analyst_covered", 0), errors="coerce").fillna(0) == 1].copy()
    covered_target = pd.to_numeric(covered[args.target], errors="coerce")
    if len(covered[covered_target.notna()]) >= 100 and covered_target.dropna().sum() >= 20:
        compact = [c for c in ["roa", "leverage", "log_assets"] if c in covered.columns] + [
            c for c in ["analyst_dispersion", "forecast_high_low_spread", "num_analysts"] if c in covered.columns
        ]
        rows.append(estimate(covered, args.target, compact, "Analyst-covered subsample", fixed_effects))

    out = pd.concat(rows, ignore_index=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(f"Saved: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
