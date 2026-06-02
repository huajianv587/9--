#!/usr/bin/env python3
"""Extended robustness checks for the APJFS-style manuscript."""

from __future__ import annotations

from pathlib import Path
import math
import re

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit

from ael_logit_inference import ACCOUNTING_BASE, estimate, load_panel, logit_fit, prepare_matrix


PANEL = Path("data/processed/ael_apac_firm_year_panel.csv")
OUT = Path("outputs/tables/apjfs_extended_robustness.csv")


def normal_two_sided_pvalue(stat: float) -> float:
    return math.erfc(abs(float(stat)) / math.sqrt(2))


def focus_row(table: pd.DataFrame, label: str, variable: str = "analyst_covered") -> dict[str, object]:
    match = table[table["variable"].eq(variable)]
    if match.empty:
        raise ValueError(f"{variable} missing in {label}")
    row = match.iloc[0]
    return {
        "specification": label,
        "reported_variable": variable,
        "coef": row["coef"],
        "robust_se": row["robust_se"],
        "p_value": row["p_value"],
        "odds_ratio": row["odds_ratio"],
        "n": int(row["n"]),
        "events": int(row["events"]),
        "fixed_effects": row["fixed_effects"],
    }


def exchange_suffix(name: object) -> str:
    match = re.search(r"\(([^():]+):[^()]+\)\s*$", str(name))
    return match.group(1) if match else "NO_TICKER_SUFFIX"


def exchange_consistent_sample_logit(panel: pd.DataFrame) -> dict[str, object]:
    suffix = panel["company_name"].map(exchange_suffix)
    market = panel["market"].astype(str).str.upper()
    keep = (market.eq("ASX") & suffix.eq("ASX")) | (
        market.eq("SINGAPORE") & suffix.isin(["SGX", "Catalist"])
    )
    exchange_consistent = panel[keep].copy()
    features = [c for c in [*ACCOUNTING_BASE, "analyst_covered"] if c in exchange_consistent.columns]
    table = estimate(
        exchange_consistent,
        "stress_12m",
        features,
        "Exchange-consistent ASX/SGX/Catalist sample",
        ["market", "fiscal_year"],
    )
    row = focus_row(table, "Exchange-consistent ASX/SGX/Catalist sample")
    row["model_family"] = "logit"
    row["cluster"] = np.nan
    row["within_firm_coverage_changers"] = np.nan
    row["excluded_labelled_rows"] = int(
        panel[pd.to_numeric(panel["stress_12m"], errors="coerce").notna()].shape[0] - row["n"]
    )
    row["exchange_consistent_firms"] = int(exchange_consistent["company_id"].nunique())
    return row


def prepare_lpm_matrix(
    panel: pd.DataFrame,
    target: str,
    features: list[str],
) -> tuple[pd.DataFrame, np.ndarray, np.ndarray, list[str]]:
    use_cols = [target, "company_id", "fiscal_year"] + features
    use = panel[use_cols].copy()
    target_numeric = pd.to_numeric(use[target], errors="coerce")
    use = use[target_numeric.notna()].copy()
    y = target_numeric[target_numeric.notna()].astype(float).to_numpy()

    cols: list[np.ndarray] = []
    names: list[str] = []
    for col in features:
        x = pd.to_numeric(use[col], errors="coerce").replace([np.inf, -np.inf], np.nan)
        if col == "analyst_covered":
            x = x.fillna(0)
        else:
            nonmissing = x.dropna()
            if len(nonmissing) >= 20:
                qlo, qhi = nonmissing.quantile([0.01, 0.99])
                if pd.notna(qlo) and pd.notna(qhi) and qlo < qhi:
                    x = x.clip(qlo, qhi)
            x = x.fillna(x.median())
            sd = x.std(ddof=0)
            if pd.notna(sd) and sd > 0:
                x = (x - x.mean()) / sd
        if x.nunique(dropna=True) <= 1:
            continue
        cols.append(x.to_numpy(dtype=float))
        names.append(col)

    return use, y, np.column_stack(cols), names


def residualize_two_way(values: np.ndarray, first: np.ndarray, second: np.ndarray) -> np.ndarray:
    residual = values.astype(float).copy()
    for _ in range(100):
        old = residual.copy()
        tmp = pd.DataFrame(residual)
        tmp["group"] = first
        residual = residual - tmp.groupby("group").transform("mean").iloc[:, : residual.shape[1]].to_numpy()
        tmp = pd.DataFrame(residual)
        tmp["group"] = second
        residual = residual - tmp.groupby("group").transform("mean").iloc[:, : residual.shape[1]].to_numpy()
        if np.max(np.abs(residual - old)) < 1e-10:
            break
    return residual


def firm_year_fe_lpm(panel: pd.DataFrame) -> dict[str, object]:
    features = [c for c in ["analyst_covered", *ACCOUNTING_BASE] if c in panel.columns]
    use, y, x, names = prepare_lpm_matrix(panel, "stress_12m", features)
    firms = use["company_id"].astype(str).to_numpy()
    years = use["fiscal_year"].astype(str).to_numpy()
    residualized = residualize_two_way(np.column_stack([y, x]), firms, years)
    y_resid = residualized[:, 0]
    x_resid = residualized[:, 1:]

    keep = np.sqrt((x_resid**2).sum(axis=0)) > 1e-8
    x_resid = x_resid[:, keep]
    kept_names = [name for name, keep_col in zip(names, keep) if keep_col]
    if "analyst_covered" not in kept_names:
        raise ValueError("analyst_covered has no within-firm identifying variation")

    xtx = np.einsum("ni,nj->ij", x_resid, x_resid)
    inv = np.linalg.pinv(xtx)
    beta = np.einsum("ij,j->i", inv, np.einsum("ni,n->i", x_resid, y_resid))
    resid = y_resid - np.einsum("ij,j->i", x_resid, beta)

    # Cluster by firm because the identifying variation is within firm over time.
    unique_firms = np.unique(firms)
    meat = np.zeros((len(beta), len(beta)))
    for firm in unique_firms:
        idx = firms == firm
        score = np.einsum("ni,n->i", x_resid[idx], resid[idx])
        meat += np.outer(score, score)
    cov = np.einsum("ij,jk,kl->il", inv, meat, inv)
    n = len(y_resid)
    k = len(beta)
    g = len(unique_firms)
    if g > 1 and n > k:
        cov *= (g / (g - 1)) * ((n - 1) / (n - k))
    se = np.sqrt(np.maximum(np.diag(cov), 0))

    analyst_idx = kept_names.index("analyst_covered")
    coef = float(beta[analyst_idx])
    robust_se = float(se[analyst_idx])
    z = coef / robust_se
    return {
        "specification": "Firm and year fixed-effects LPM",
        "reported_variable": "analyst_covered",
        "coef": coef,
        "robust_se": robust_se,
        "p_value": normal_two_sided_pvalue(z),
        "odds_ratio": np.nan,
        "n": int(n),
        "events": int(y.sum()),
        "fixed_effects": "company_id, fiscal_year",
        "model_family": "linear probability",
        "cluster": "company_id",
        "within_firm_coverage_changers": int(
            pd.DataFrame({"firm": firms, "coverage": x[:, names.index("analyst_covered")]})
            .groupby("firm")["coverage"]
            .nunique()
            .gt(1)
            .sum()
        ),
    }


def firm_clustered_logit(panel: pd.DataFrame) -> dict[str, object]:
    features = [c for c in [*ACCOUNTING_BASE, "analyst_covered"] if c in panel.columns]
    fixed_effects = ["market", "fiscal_year"]
    x, y, names = prepare_matrix(panel, "stress_12m", features, fixed_effects)
    beta, fitted = logit_fit(x, y)

    use_cols = ["stress_12m", "company_id"] + features + fixed_effects
    use = panel[use_cols].copy()
    target_numeric = pd.to_numeric(use["stress_12m"], errors="coerce")
    use = use[target_numeric.notna()].copy()
    clusters = use["company_id"].astype(str).to_numpy()

    weights = fitted * (1 - fitted)
    hessian = np.einsum("ni,nj,n->ij", x, x, weights)
    inv_hessian = np.linalg.pinv(np.nan_to_num(hessian, nan=0.0, posinf=0.0, neginf=0.0), rcond=1e-10)
    residual = y - fitted

    meat = np.zeros((x.shape[1], x.shape[1]))
    for firm in np.unique(clusters):
        idx = clusters == firm
        score = np.einsum("ni,n->i", x[idx], residual[idx])
        meat += np.outer(score, score)

    cov = np.einsum("ij,jk,kl->il", inv_hessian, meat, inv_hessian)
    n, k = x.shape
    g = len(np.unique(clusters))
    if g > 1 and n > k:
        cov *= (g / (g - 1)) * ((n - 1) / (n - k))
    se = np.sqrt(np.maximum(np.diag(cov), 0))

    analyst_idx = names.index("analyst_covered")
    coef = float(beta[analyst_idx])
    robust_se = float(se[analyst_idx])
    z = coef / robust_se
    return {
        "specification": "Firm-clustered logit standard errors",
        "reported_variable": "analyst_covered",
        "coef": coef,
        "robust_se": robust_se,
        "p_value": normal_two_sided_pvalue(z),
        "odds_ratio": float(np.exp(coef)),
        "n": int(n),
        "events": int(y.sum()),
        "fixed_effects": "market, fiscal_year",
        "model_family": "logit",
        "cluster": "company_id",
        "within_firm_coverage_changers": np.nan,
    }


def weighted_logit_fit(
    x: np.ndarray,
    y: np.ndarray,
    weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    def linear_predictor(beta: np.ndarray) -> np.ndarray:
        beta = np.clip(np.nan_to_num(beta, nan=0.0, posinf=20.0, neginf=-20.0), -20, 20)
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            xb = x @ beta
        return np.nan_to_num(np.clip(xb, -35, 35), nan=0.0, posinf=35.0, neginf=-35.0)

    def objective(beta: np.ndarray) -> float:
        xb = linear_predictor(beta)
        return float(np.sum(weights * (np.logaddexp(0, xb) - y * xb)))

    def gradient(beta: np.ndarray) -> np.ndarray:
        p = expit(linear_predictor(beta))
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            grad = x.T @ (weights * (p - y))
        return np.nan_to_num(grad, nan=0.0, posinf=0.0, neginf=0.0)

    result = minimize(
        objective,
        np.zeros(x.shape[1]),
        jac=gradient,
        method="L-BFGS-B",
        bounds=[(-20, 20)] * x.shape[1],
        options={"maxiter": 2000},
    )
    beta = np.clip(np.nan_to_num(result.x, nan=0.0, posinf=20.0, neginf=-20.0), -20, 20)
    fitted = np.clip(expit(linear_predictor(beta)), 1e-8, 1 - 1e-8)
    return beta, fitted


def iptw_weighted_logit(panel: pd.DataFrame) -> dict[str, object]:
    features = [c for c in ACCOUNTING_BASE if c in panel.columns]
    fixed_effects = ["market", "fiscal_year"]
    model_panel = panel[pd.to_numeric(panel["stress_12m"], errors="coerce").notna()].copy()

    x_ps, treatment, _ = prepare_matrix(model_panel, "analyst_covered", features, fixed_effects)
    _, propensity = logit_fit(x_ps, treatment)
    propensity = np.clip(propensity, 1e-3, 1 - 1e-3)
    treatment_rate = float(treatment.mean())
    weights = np.where(treatment == 1, treatment_rate / propensity, (1 - treatment_rate) / (1 - propensity))
    lower, upper = np.quantile(weights, [0.01, 0.99])
    weights = np.clip(weights, lower, upper)
    weights = weights / weights.mean()

    x, y, names = prepare_matrix(model_panel, "stress_12m", features + ["analyst_covered"], fixed_effects)
    if len(weights) != len(y):
        raise ValueError("IPTW weight length does not match outcome matrix")
    beta, fitted = weighted_logit_fit(x, y, weights)

    hessian = np.einsum("ni,nj,n->ij", x, x, weights * fitted * (1 - fitted))
    inv_hessian = np.linalg.pinv(np.nan_to_num(hessian, nan=0.0, posinf=0.0, neginf=0.0), rcond=1e-10)
    residual = y - fitted
    meat = np.einsum("ni,nj,n->ij", x, x, (weights * residual) ** 2)
    cov = np.einsum("ij,jk,kl->il", inv_hessian, meat, inv_hessian)
    n, k = x.shape
    if n > k:
        cov *= n / (n - k)
    se = np.sqrt(np.maximum(np.diag(cov), 0))

    analyst_idx = names.index("analyst_covered")
    coef = float(beta[analyst_idx])
    robust_se = float(se[analyst_idx])
    z = coef / robust_se
    return {
        "specification": "IPTW propensity-score weighted logit",
        "reported_variable": "analyst_covered",
        "coef": coef,
        "robust_se": robust_se,
        "p_value": normal_two_sided_pvalue(z),
        "odds_ratio": float(np.exp(coef)),
        "n": int(n),
        "events": int(y.sum()),
        "fixed_effects": "market, fiscal_year",
        "model_family": "weighted logit",
        "cluster": np.nan,
        "within_firm_coverage_changers": np.nan,
        "propensity_lower": np.nan,
        "propensity_upper": np.nan,
        "covered_rows": int(treatment.sum()),
        "weight_lower": float(lower),
        "weight_upper": float(upper),
    }


def trimmed_propensity_common_support(panel: pd.DataFrame) -> dict[str, object]:
    features = [c for c in ACCOUNTING_BASE if c in panel.columns]
    fixed_effects = ["market", "fiscal_year"]
    model_panel = panel[pd.to_numeric(panel["stress_12m"], errors="coerce").notna()].copy()

    x_ps, covered, _ = prepare_matrix(model_panel, "analyst_covered", features, fixed_effects)
    _, propensity = logit_fit(x_ps, covered)
    use_cols = ["analyst_covered", *features, *fixed_effects]
    use = model_panel[use_cols].copy()
    coverage_numeric = pd.to_numeric(use["analyst_covered"], errors="coerce")
    use = use[coverage_numeric.notna()].copy()

    covered_propensity = propensity[covered == 1]
    uncovered_propensity = propensity[covered == 0]
    lower = max(
        float(covered_propensity.min()),
        float(uncovered_propensity.min()),
        float(np.quantile(covered_propensity, 0.05)),
        float(np.quantile(uncovered_propensity, 0.05)),
    )
    upper = min(
        float(covered_propensity.max()),
        float(uncovered_propensity.max()),
        float(np.quantile(covered_propensity, 0.95)),
        float(np.quantile(uncovered_propensity, 0.95)),
    )
    if not lower < upper:
        raise ValueError("propensity common-support bounds are invalid")

    model_panel["coverage_propensity"] = np.nan
    model_panel.loc[use.index, "coverage_propensity"] = propensity
    common = model_panel[
        model_panel["coverage_propensity"].ge(lower)
        & model_panel["coverage_propensity"].le(upper)
    ].copy()
    table = estimate(
        common,
        "stress_12m",
        features + ["analyst_covered"],
        "Trimmed propensity-score common support",
        fixed_effects,
    )
    row = focus_row(table, "Trimmed propensity-score common support")
    row["model_family"] = "logit"
    row["cluster"] = np.nan
    row["within_firm_coverage_changers"] = np.nan
    row["propensity_lower"] = lower
    row["propensity_upper"] = upper
    row["covered_rows"] = int(pd.to_numeric(common["analyst_covered"], errors="coerce").fillna(0).sum())
    return row


def add_market_year_size_decile(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy()
    out["market_year"] = out["market"].astype(str) + "|" + out["fiscal_year"].astype(str)
    out["size_decile"] = np.nan
    size = pd.to_numeric(out["log_assets"], errors="coerce")
    for group_key, idx in out.groupby("market_year", dropna=False).groups.items():
        group_size = size.loc[idx]
        nonmissing = group_size.dropna()
        if len(nonmissing) < 10 or nonmissing.nunique() < 3:
            continue
        bins = min(10, int(nonmissing.nunique()))
        ranked = nonmissing.rank(method="first")
        deciles = pd.qcut(ranked, q=bins, labels=False, duplicates="drop") + 1
        out.loc[deciles.index, "size_decile"] = deciles.astype(int)
    out["market_year_size_decile"] = (
        out["market"].astype(str)
        + "|"
        + out["fiscal_year"].astype(str)
        + "|S"
        + out["size_decile"].fillna(0).astype(int).astype(str)
    )
    return out


def add_strict_component_label(panel: pd.DataFrame) -> pd.DataFrame:
    components = [
        "negative_equity",
        "operating_loss",
        "interest_coverage_below_1_5",
    ]
    missing = [col for col in components if col not in panel.columns]
    if missing:
        raise ValueError(f"missing strict-label components: {missing}")

    out = panel.copy()
    for col in components:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype(int)
    out["stress_component_count_current"] = out[components].sum(axis=1)
    out["strict_component_stress_current"] = out["stress_component_count_current"].ge(2).astype(int)
    sorted_out = out.sort_values(["company_id", "fiscal_year"])
    shifted = sorted_out.groupby("company_id")["strict_component_stress_current"].shift(-1)
    out["strict_component_stress_12m"] = shifted.reindex(sorted_out.index).reindex(out.index)
    return out


def main() -> int:
    panel = load_panel(PANEL)
    panel = add_market_year_size_decile(panel)
    panel = add_strict_component_label(panel)
    rows: list[dict[str, object]] = []

    accounting = [c for c in ACCOUNTING_BASE if c in panel.columns]
    fixed_effects = ["market", "fiscal_year"]

    baseline = estimate(
        panel,
        "stress_12m",
        accounting + ["analyst_covered"],
        "Baseline with market-year FE",
        fixed_effects,
    )
    rows.append(focus_row(baseline, "Baseline with market-year FE"))
    rows.append(exchange_consistent_sample_logit(panel))
    rows.append(firm_clustered_logit(panel))

    strict_label = estimate(
        panel,
        "strict_component_stress_12m",
        accounting + ["analyst_covered"],
        "Strict next-year stress: >=2 components",
        fixed_effects,
    )
    rows.append(focus_row(strict_label, "Strict next-year stress: >=2 components"))

    fiscal_year = pd.to_numeric(panel["fiscal_year"], errors="coerce")
    covid_outcome = panel[~fiscal_year.add(1).isin([2020, 2021])].copy()
    covid_outcome_model = estimate(
        covid_outcome,
        "stress_12m",
        accounting + ["analyst_covered"],
        "Excludes COVID outcome years 2020-2021",
        fixed_effects,
    )
    rows.append(focus_row(covid_outcome_model, "Excludes COVID outcome years 2020-2021"))
    rows.append(trimmed_propensity_common_support(panel))
    rows.append(iptw_weighted_logit(panel))

    size_decile_accounting = [c for c in accounting if c != "log_assets"]
    size_decile_fe = estimate(
        panel,
        "stress_12m",
        size_decile_accounting + ["analyst_covered"],
        "Market-year size-decile fixed effects",
        ["market_year_size_decile"],
    )
    rows.append(focus_row(size_decile_fe, "Market-year size-decile fixed effects"))

    if "financial_stress_current" in panel.columns:
        controls = accounting + ["financial_stress_current", "analyst_covered"]
        current_control = estimate(
            panel,
            "stress_12m",
            controls,
            "Adds current stress indicator",
            fixed_effects,
        )
        rows.append(focus_row(current_control, "Adds current stress indicator"))

        onset = panel[pd.to_numeric(panel["financial_stress_current"], errors="coerce").fillna(0).eq(0)].copy()
        onset_model = estimate(
            onset,
            "stress_12m",
            accounting + ["analyst_covered"],
            "Excludes currently stressed firm-years",
            fixed_effects,
        )
        rows.append(focus_row(onset_model, "Excludes currently stressed firm-years"))

    if "num_analysts" in panel.columns:
        panel["log1p_num_analysts"] = np.log1p(
            pd.to_numeric(panel["num_analysts"], errors="coerce").fillna(0)
        )
        intensity = estimate(
            panel,
            "stress_12m",
            accounting + ["log1p_num_analysts"],
            "Analyst intensity: log(1 + analysts)",
            fixed_effects,
        )
        rows.append(
            focus_row(
                intensity,
                "Analyst intensity: log(1 + analysts)",
                variable="log1p_num_analysts",
            )
        )

    rows.append(firm_year_fe_lpm(panel))

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"Saved: {OUT}")
    print(out.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
