#!/usr/bin/env python3
"""Run strict-accounting-stress v2 model and robustness checks."""

from __future__ import annotations

import argparse
from datetime import datetime
from math import erfc, sqrt
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "data/processed/ael_apac_firm_year_panel_v2_frozen_candidate_20260603.csv"
OUT_MODEL = ROOT / "outputs/tables/ael_v2_strict_accounting_model_suite_20260603.csv"
OUT_PRED = ROOT / "outputs/tables/ael_v2_strict_accounting_prediction_increment_20260603.csv"
OUT_AUDIT = ROOT / "outputs/ael_v2_strict_accounting_go_no_go_20260603.md"

BASE_CONTROLS = ["roa_w", "leverage_w", "log_assets_w", "revenue_growth_w"]


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)


def sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def fit_logit(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta = np.zeros(X.shape[1])
    ridge = np.eye(X.shape[1]) * 1e-6
    ridge[0, 0] = 0.0
    for _ in range(220):
        pred = np.clip(sigmoid(X @ beta), 1e-8, 1 - 1e-8)
        w = pred * (1 - pred)
        grad = X.T @ (pred - y) + ridge @ beta
        hessian = X.T @ (X * w[:, None]) + ridge
        step = np.linalg.pinv(np.nan_to_num(hessian), rcond=1e-10) @ np.nan_to_num(grad)
        beta = np.clip(beta - step, -20, 20)
        if float(np.max(np.abs(step))) < 1e-7:
            break
    return beta, np.clip(sigmoid(X @ beta), 1e-8, 1 - 1e-8)


def cluster_se(X: np.ndarray, y: np.ndarray, p: np.ndarray, clusters: np.ndarray) -> np.ndarray:
    n, k = X.shape
    w = p * (1 - p)
    hessian = X.T @ (X * w[:, None])
    bread = np.linalg.pinv(np.nan_to_num(hessian), rcond=1e-10)
    scores = X * (y - p)[:, None]
    meat = np.zeros((k, k))
    for cluster in np.unique(clusters):
        summed = scores[clusters == cluster].sum(axis=0).reshape(-1, 1)
        meat += summed @ summed.T
    cov = bread @ meat @ bread
    g = len(np.unique(clusters))
    if g > 1 and n > k:
        cov *= (g / (g - 1)) * ((n - 1) / (n - k))
    return np.sqrt(np.maximum(np.diag(cov), 0))


def auc_score(y: np.ndarray, pred: np.ndarray) -> float:
    y = np.asarray(y)
    pred = np.asarray(pred)
    n_pos = int(y.sum())
    n_neg = int(len(y) - n_pos)
    if n_pos == 0 or n_neg == 0:
        return np.nan
    ranks = pd.Series(pred).rank(method="average").to_numpy()
    return float((ranks[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def brier_score(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean((pred - y) ** 2))


def prepare_matrix(
    df: pd.DataFrame,
    target: str,
    controls: list[str],
    fixed_effects: list[str],
    analyst_var: str | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str], pd.DataFrame]:
    use_cols = [target, "company_id"] + controls + fixed_effects
    if analyst_var:
        use_cols.append(analyst_var)
    use = df[list(dict.fromkeys(use_cols))].copy()
    y = numeric(use[target])
    use = use.loc[y.notna()].copy()
    y = numeric(use[target]).astype(int)
    if y.nunique() < 2:
        raise ValueError("target has one class")

    columns = [np.ones(len(use))]
    names = ["Intercept"]
    if analyst_var:
        x = numeric(use[analyst_var]).fillna(0)
        columns.append(x.to_numpy(dtype=float))
        names.append(analyst_var)

    for col in controls:
        x = numeric(use[col])
        x = x.fillna(x.median())
        sd = x.std(ddof=0)
        if pd.notna(sd) and sd > 0:
            x = (x - x.mean()) / sd
        if x.nunique(dropna=True) > 1:
            columns.append(x.to_numpy(dtype=float))
            names.append(col)

    for col in fixed_effects:
        labels = use[col].astype(str).replace({"": "Missing", "nan": "Missing", "NaN": "Missing"})
        dummies = pd.get_dummies(labels, prefix=f"FE:{col}", drop_first=True, dtype=float)
        for dummy_col in dummies:
            x = dummies[dummy_col]
            if x.nunique(dropna=True) > 1:
                columns.append(x.to_numpy(dtype=float))
                names.append(dummy_col)
    return np.column_stack(columns), y.to_numpy(dtype=int), use["company_id"].to_numpy(dtype=int), names, use


def estimate_spec(
    df: pd.DataFrame,
    name: str,
    target: str,
    analyst_var: str | None = "analyst_covered",
    fixed_effects: list[str] | None = None,
) -> dict[str, object]:
    fixed_effects = fixed_effects or ["market", "fiscal_year"]
    controls = [col for col in BASE_CONTROLS if col in df.columns]
    X, y, clusters, names, _use = prepare_matrix(df, target, controls, fixed_effects, analyst_var)
    beta, pred = fit_logit(X, y)
    se = cluster_se(X, y, pred, clusters)
    row: dict[str, object] = {
        "specification": name,
        "target": target,
        "analyst_var": analyst_var or "none",
        "n": int(len(y)),
        "firms": int(len(np.unique(clusters))),
        "events": int(y.sum()),
        "event_rate": float(y.mean()),
        "auc": auc_score(y, pred),
        "brier": brier_score(y, pred),
        "fixed_effects": ", ".join(fixed_effects),
        "controls": ", ".join(controls),
        "error": "",
    }
    if analyst_var:
        idx = names.index(analyst_var)
        coef = beta[idx]
        stderr = se[idx]
        z = coef / stderr if stderr > 0 else np.nan
        pvalue = erfc(abs(z) / sqrt(2)) if pd.notna(z) else np.nan
        x0 = X.copy()
        x1 = X.copy()
        x0[:, idx] = 0
        x1[:, idx] = 1 if analyst_var == "analyst_covered" else x1[:, idx] + 1
        ame = float((sigmoid(x1 @ beta) - sigmoid(x0 @ beta)).mean())
        row.update(
            {
                "coef": float(coef),
                "cluster_se": float(stderr),
                "z": float(z),
                "p_value": float(pvalue),
                "odds_ratio": float(np.exp(coef)),
                "ame": ame,
            }
        )
    return row


def model_suite(panel: pd.DataFrame) -> pd.DataFrame:
    panel = panel.copy()
    panel["log1p_num_analysts"] = np.log1p(numeric(panel["num_analysts"]).fillna(0))
    strict = panel.loc[panel["strict_accounting_sample_flag"]].copy()
    specs: list[tuple[str, pd.DataFrame, str, str | None, list[str]]] = [
        ("Main strict accounting stress", strict, "strict_accounting_stress_12m_candidate", "analyst_covered", ["market", "fiscal_year"]),
        ("Main without analyst", strict, "strict_accounting_stress_12m_candidate", None, ["market", "fiscal_year"]),
        ("ASX split", strict.loc[strict["market"].eq("ASX")], "strict_accounting_stress_12m_candidate", "analyst_covered", ["fiscal_year"]),
        ("Singapore split", strict.loc[strict["market"].eq("SINGAPORE")], "strict_accounting_stress_12m_candidate", "analyst_covered", ["fiscal_year"]),
        ("Onset sample excluding current strict stress", strict.loc[~strict["strict_accounting_stress_current"].eq(1)], "strict_accounting_stress_12m_candidate", "analyst_covered", ["market", "fiscal_year"]),
        ("Drop suspect structure names", strict.loc[~strict["suspect_structure_name_flag"]], "strict_accounting_stress_12m_candidate", "analyst_covered", ["market", "fiscal_year"]),
        ("Operating-status rows only", strict.loc[~strict["status_nonoperating_flag"]], "strict_accounting_stress_12m_candidate", "analyst_covered", ["market", "fiscal_year"]),
        ("COVID outcome-year exclusion", strict.loc[~strict["fiscal_year"].isin([2019, 2020])], "strict_accounting_stress_12m_candidate", "analyst_covered", ["market", "fiscal_year"]),
        ("Analyst intensity log1p count", strict, "strict_accounting_stress_12m_candidate", "log1p_num_analysts", ["market", "fiscal_year"]),
        ("Broad stress appendix label", panel.loc[panel["broad_baseline_sample_flag"]], "broad_stress_12m_appendix", "analyst_covered", ["market", "fiscal_year"]),
        ("Persistent broad stress label", panel.loc[panel["persistent_sample_flag"]], "persistent_broad_stress_24m_candidate", "analyst_covered", ["market", "fiscal_year"]),
        ("Altman distress robustness label", panel.loc[panel["altman_sample_flag"]], "altman_distress_12m_candidate", "analyst_covered", ["market", "fiscal_year"]),
        ("Broad event candidate label", panel.loc[panel["event12_sample_flag"]], "event_distress_12m_candidate", "analyst_covered", ["market", "fiscal_year"]),
    ]
    rows = []
    for name, frame, target, analyst_var, fixed_effects in specs:
        try:
            if len(frame) < 200:
                raise ValueError("sample too small")
            rows.append(estimate_spec(frame, name, target, analyst_var, fixed_effects))
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "specification": name,
                    "target": target,
                    "analyst_var": analyst_var or "none",
                    "n": int(len(frame)),
                    "error": repr(exc),
                }
            )
    return pd.DataFrame(rows)


def prediction_increment(model_df: pd.DataFrame) -> pd.DataFrame:
    base = model_df.loc[model_df["specification"].eq("Main without analyst")].iloc[0]
    full = model_df.loc[model_df["specification"].eq("Main strict accounting stress")].iloc[0]
    return pd.DataFrame(
        [
            {
                "comparison": "strict_label_accounting_plus_analyst_minus_accounting_only",
                "n": int(full["n"]),
                "events": int(full["events"]),
                "auc_accounting_only": float(base["auc"]),
                "auc_plus_analyst": float(full["auc"]),
                "delta_auc": float(full["auc"] - base["auc"]),
                "brier_accounting_only": float(base["brier"]),
                "brier_plus_analyst": float(full["brier"]),
                "delta_brier": float(full["brier"] - base["brier"]),
            }
        ]
    )


def markdown_table(df: pd.DataFrame, cols: list[str]) -> list[str]:
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for record in df[cols].to_dict("records"):
        vals = []
        for col in cols:
            value = record.get(col, "")
            if pd.isna(value):
                vals.append("")
            elif isinstance(value, float):
                vals.append(f"{value:.4f}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def render_audit(model_df: pd.DataFrame, pred_df: pd.DataFrame) -> str:
    main = model_df.loc[model_df["specification"].eq("Main strict accounting stress")].iloc[0]
    asx = model_df.loc[model_df["specification"].eq("ASX split")].iloc[0]
    sg = model_df.loc[model_df["specification"].eq("Singapore split")].iloc[0]
    altman = model_df.loc[model_df["specification"].eq("Altman distress robustness label")].iloc[0]
    event = model_df.loc[model_df["specification"].eq("Broad event candidate label")].iloc[0]
    pred = pred_df.iloc[0]
    if (
        float(main["coef"]) < 0
        and float(main["p_value"]) < 0.01
        and float(asx["coef"]) < 0
        and float(sg["coef"]) < 0
        and float(event["coef"]) < 0
    ):
        decision = "CONDITIONAL_GO_FOR_STRICT_ACCOUNTING_STRESS_ROUTE"
    else:
        decision = "NO_GO_FOR_CURRENT_Q3_ROUTE"

    lines = [
        "# AEL v2 Strict Accounting Stress Go/No-Go Audit",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        f"Input frozen candidate panel: `{PANEL}`",
        "",
        "## Decision",
        "",
        f"Status: {decision}",
        "",
        "The current v2 result pattern supports a stricter accounting-stress manuscript route, but not a no-risk submission package. The claim should be framed as an association between analyst coverage and subsequent accounting-based stress, not as causal prevention or formal bankruptcy prediction.",
        "",
        "## Model Suite",
        "",
    ]
    lines.extend(
        markdown_table(
            model_df,
            [
                "specification",
                "n",
                "events",
                "event_rate",
                "coef",
                "cluster_se",
                "p_value",
                "odds_ratio",
                "ame",
                "auc",
                "brier",
                "error",
            ],
        )
    )
    lines.extend(["", "## Prediction Increment", ""])
    lines.extend(
        markdown_table(
            pred_df,
            [
                "comparison",
                "auc_accounting_only",
                "auc_plus_analyst",
                "delta_auc",
                "brier_accounting_only",
                "brier_plus_analyst",
                "delta_brier",
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Reviewer-Level Reading",
            "",
            f"- Main strict-accounting OR: {float(main['odds_ratio']):.3f}; AME: {float(main['ame']):.3f}; p-value: {float(main['p_value']):.3g}.",
            f"- Market split directions: ASX coef {float(asx['coef']):.3f}; Singapore coef {float(sg['coef']):.3f}.",
            f"- Altman robustness is directionally consistent but weaker: p-value {float(altman['p_value']):.3g}; this supports robustness-only treatment.",
            f"- Event candidate is directionally strong, but still candidate-level because event matching is not clean direct Entity ID matching.",
            f"- Prediction increment is small: delta AUC {float(pred['delta_auc']):.4f}, delta Brier {float(pred['delta_brier']):.4f}. Do not sell this as a prediction-performance paper.",
            "",
            "## Route Decision",
            "",
            "- Main route: strict accounting-based stress, market/year FE, firm-clustered standard errors.",
            "- Robustness: broad stress appendix, persistent stress, event candidate, Altman candidate, market split, onset sample, COVID exclusion, analyst intensity.",
            "- Do not use Altman as the main dependent variable unless total-liabilities coverage is improved.",
            "- Do not call event evidence bankruptcy/default distress without direct-ID event data or a stricter event taxonomy.",
            "- The result pattern is promising for SSCI/JCR Q3, but the package still needs final table rebuild, manuscript rewrite, journal fit screen, and submission QA.",
            "",
        ]
    )
    return "\n".join(lines)


def build(panel_path: Path) -> None:
    panel = pd.read_csv(panel_path, low_memory=False)
    model_df = model_suite(panel)
    pred_df = prediction_increment(model_df)
    OUT_MODEL.parent.mkdir(parents=True, exist_ok=True)
    model_df.to_csv(OUT_MODEL, index=False)
    pred_df.to_csv(OUT_PRED, index=False)
    OUT_AUDIT.write_text(render_audit(model_df, pred_df), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", type=Path, default=PANEL)
    args = parser.parse_args()
    build(args.panel)
    print(f"Wrote {OUT_MODEL}")
    print(f"Wrote {OUT_PRED}")
    print(f"Wrote {OUT_AUDIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
