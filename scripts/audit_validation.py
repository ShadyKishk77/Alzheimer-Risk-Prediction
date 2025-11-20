import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.exceptions import NotFittedError
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    GroupKFold,
    LeaveOneGroupOut,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingClassifier


# -------------------------------
# Config & constants
# -------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_CANDIDATES = [
    REPO_ROOT / "data" / "raw_alzheimers_data.csv",
    REPO_ROOT / "data" / "processed_alzheimers_data.csv",
]
REPORTS_DIR = REPO_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
N_OUTER = 5
N_INNER = 3

TARGET_PREFERRED = ["Diagnosis", "diagnosis"]
TARGET_CANDIDATE_HINTS = ["diagnosis", "label", "target", "alz", "outcome"]

COGNITIVE_TOKENS = [
    "mmse",
    "functional",
    "adl",
    "memory",
    "behavior",
    "behaviour",
    "confusion",
    "disorientation",
    "personality",
]

SITE_TOKENS = ["site", "hospital", "center", "centre", "clinic", "location"]
DATE_TOKENS = ["date", "year"]

ID_TOKENS = ["patientid", "id", "identifier", "doctorincharge"]


# -------------------------------
# Utilities
# -------------------------------

def load_dataset() -> pd.DataFrame:
    for p in DATA_CANDIDATES:
        if p.exists():
            return pd.read_csv(p)
    raise FileNotFoundError("Could not find raw or processed dataset in data/.")


def detect_target(df: pd.DataFrame) -> str:
    # Prefer explicit names
    for name in TARGET_PREFERRED:
        if name in df.columns:
            return name
    # Fuzzy match hints
    lower_cols = {c.lower(): c for c in df.columns}
    for hint in TARGET_CANDIDATE_HINTS:
        if hint in lower_cols:
            return lower_cols[hint]
    # Fallback: any binary column
    binary_candidates = []
    for c in df.columns:
        vals = df[c].dropna().unique()
        if len(vals) <= 3 and set(np.unique(vals)).issubset({0, 1}):
            binary_candidates.append(c)
    if len(binary_candidates) == 1:
        return binary_candidates[0]
    msg = (
        "Unable to uniquely determine target column. Candidates: "
        + ", ".join(binary_candidates)
        + ". Please rename your target to 'Diagnosis' or pass explicitly."
    )
    raise ValueError(msg)


def find_columns_by_tokens(df: pd.DataFrame, tokens: List[str]) -> List[str]:
    cols = []
    for c in df.columns:
        cl = c.lower()
        for t in tokens:
            if t in cl:
                cols.append(c)
                break
    return sorted(list(dict.fromkeys(cols)))


def get_id_like_columns(df: pd.DataFrame) -> List[str]:
    return find_columns_by_tokens(df, ID_TOKENS)


def get_cognitive_columns(df: pd.DataFrame) -> List[str]:
    return find_columns_by_tokens(df, COGNITIVE_TOKENS)


def get_site_column(df: pd.DataFrame) -> Optional[str]:
    candidates = find_columns_by_tokens(df, SITE_TOKENS)
    return candidates[0] if candidates else None


def get_date_column(df: pd.DataFrame) -> Optional[str]:
    candidates = find_columns_by_tokens(df, DATE_TOKENS)
    # Prefer columns with datetime-like or year-like values
    for c in candidates:
        s = df[c]
        try:
            pd.to_datetime(s, errors="raise")
            return c
        except Exception:
            # maybe year as int
            if pd.api.types.is_integer_dtype(s):
                return c
    return candidates[0] if candidates else None


def split_features(df: pd.DataFrame, target: str, drop_cognitive: bool) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    y = df[target].astype(int)
    id_cols = [c for c in get_id_like_columns(df) if c != target]
    cognitive = get_cognitive_columns(df) if drop_cognitive else []
    X = df.drop(columns=[target] + id_cols + cognitive, errors="ignore").copy()
    used_cols = list(X.columns)
    return X, y, used_cols


def build_pipeline(X: pd.DataFrame, model) -> Pipeline:
    numeric_cols = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
        ]
    )
    pipe = Pipeline(steps=[("pre", pre), ("clf", model)])
    return pipe


# -------------------------------
# Leakage audit
# -------------------------------

def single_feature_auc(df: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
    aucs = {}
    for c in df.columns:
        try:
            x = df[c]
            if pd.api.types.is_numeric_dtype(x):
                # numeric directly
                score = roc_auc_score(y, x)
            else:
                # one-hot encode simple categorical for AUC proxy via probability of class 1
                xs = pd.get_dummies(x, dummy_na=True)
                # average across columns as proxy score
                prob = xs.mean(axis=1)
                score = roc_auc_score(y, prob)
            aucs[c] = float(max(score, 1 - score))  # symmetry
        except Exception:
            continue
    return aucs


def mutual_info_scores(X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
    X_enc = X.copy()
    # quick encoding for MI: one-hot categoricals
    for c in X_enc.columns:
        if not pd.api.types.is_numeric_dtype(X_enc[c]):
            dummies = pd.get_dummies(X_enc[c], prefix=c, dummy_na=True)
            X_enc = X_enc.drop(columns=[c])
            X_enc = pd.concat([X_enc, dummies], axis=1)
    mi = mutual_info_classif(X_enc.fillna(0), y.values, random_state=RANDOM_STATE)
    return {col: float(mi[i]) for i, col in enumerate(X_enc.columns)}


# -------------------------------
# Evaluation helpers
# -------------------------------

def eval_split(pipe: Pipeline, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )
    pipe.fit(Xtr, ytr)
    proba = pipe.predict_proba(Xte)[:, 1]
    preds = (proba >= 0.5).astype(int)
    acc = accuracy_score(yte, preds)
    prec, rec, f1, _ = precision_recall_fscore_support(yte, preds, average="binary", zero_division=0)
    auc = roc_auc_score(yte, proba)
    brier = brier_score_loss(yte, proba)
    return {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1": float(f1),
        "roc_auc": float(auc),
        "brier": float(brier),
    }


def nested_cv_scores(model, param_grid, X: pd.DataFrame, y: pd.Series) -> Dict:
    outer = StratifiedKFold(n_splits=N_OUTER, shuffle=True, random_state=RANDOM_STATE)
    outer_scores: List[float] = []
    fold_details = []

    for fold_idx, (tr_idx, te_idx) in enumerate(outer.split(X, y), start=1):
        Xtr, Xte = X.iloc[tr_idx], X.iloc[te_idx]
        ytr, yte = y.iloc[tr_idx], y.iloc[te_idx]

        pipe = build_pipeline(Xtr, model)
        inner = StratifiedKFold(n_splits=N_INNER, shuffle=True, random_state=RANDOM_STATE)
        search = GridSearchCV(
            estimator=pipe,
            param_grid={f"clf__{k}": v for k, v in param_grid.items()},
            scoring="roc_auc",
            cv=inner,
            n_jobs=-1,
        )
        search.fit(Xtr, ytr)
        best = search.best_estimator_
        proba = best.predict_proba(Xte)[:, 1]
        auc = roc_auc_score(yte, proba)
        outer_scores.append(auc)
        fold_details.append({
            "fold": fold_idx,
            "best_params": search.best_params_,
            "val_score": float(search.best_score_),
            "test_auc": float(auc),
        })

    return {
        "outer_scores": [float(s) for s in outer_scores],
        "mean_auc": float(np.mean(outer_scores)),
        "std_auc": float(np.std(outer_scores)),
        "folds": fold_details,
    }


def temporal_site_validation(df: pd.DataFrame, target: str) -> Dict:
    results = {"temporal": None, "site": None}

    # Temporal
    date_col = get_date_column(df)
    if date_col:
        s = df[[date_col, target]].dropna().copy()
        try:
            s[date_col] = pd.to_datetime(s[date_col], errors="coerce")
        except Exception:
            # year integer
            pass
        df_sorted = df.sort_values(by=date_col)
        n = len(df_sorted)
        tr_end = int(0.7 * n)
        val_end = int(0.85 * n)
        splits = {
            "train": (0, tr_end),
            "val": (tr_end, val_end),
            "test": (val_end, n),
        }
        results["temporal"] = {
            "date_column": date_col,
            "sizes": {k: v[1] - v[0] for k, v in splits.items()}
        }
    else:
        results["temporal"] = {"message": "No date/year column detected; temporal split skipped."}

    # Site
    site_col = get_site_column(df)
    if site_col:
        groups = df[site_col].astype(str)
        logo = LeaveOneGroupOut()
        results["site"] = {
            "site_column": site_col,
            "n_groups": int(groups.nunique()),
        }
    else:
        results["site"] = {"message": "No site/hospital column detected; site validation suggestion recorded."}

    return results


# -------------------------------
# Main routine
# -------------------------------

def main():
    df = load_dataset()
    target = detect_target(df)

    # Model with all features (diagnostic support)
    X_all, y, used_all = split_features(df, target, drop_cognitive=False)
    # Model without cognitive (pre-screen)
    X_nocog, y2, used_nocog = split_features(df, target, drop_cognitive=True)
    assert y.equals(y2)

    # Print detected columns
    cognitive_cols = get_cognitive_columns(df)
    print(f"Target: {target}")
    print(f"Detected cognitive features: {cognitive_cols}")

    # Leakage audit
    aucs = single_feature_auc(df.drop(columns=[target], errors="ignore"), y)
    mi = mutual_info_scores(df.drop(columns=[target], errors="ignore"), y)
    suspicious = sorted(
        (
            (c, aucs.get(c, np.nan), mi.get(c, np.nan))
            for c in df.columns if c != target
        ),
        key=lambda t: (not math.isnan(t[1]) and -t[1], not math.isnan(t[2]) and -t[2])
    )
    top_suspicious = [
        {"feature": c, "single_feature_auc": float(a) if not math.isnan(a) else None, "mutual_info": float(m) if not math.isnan(m) else None}
        for c, a, m in suspicious[:30]
    ]
    leakage_report = {
        "target": target,
        "cognitive_features_detected": cognitive_cols,
        "top_suspicious_by_auc_mi": top_suspicious,
        "proxy_flags": [
            f for f, a in aucs.items() if a is not None and a >= 0.98
        ],
    }
    (REPORTS_DIR / "leakage_audit_report.json").write_text(json.dumps(leakage_report, indent=2))

    # Pipelines & baseline eval
    gb = GradientBoostingClassifier(random_state=RANDOM_STATE)
    lr = LogisticRegression(max_iter=1000, solver="liblinear", random_state=RANDOM_STATE)

    pipe_gb_all = build_pipeline(X_all, gb)
    pipe_gb_nocog = build_pipeline(X_nocog, gb)

    metrics_all = eval_split(pipe_gb_all, X_all, y)
    metrics_nocog = eval_split(pipe_gb_nocog, X_nocog, y)

    with_without = {
        "with_cognitive": {"features": used_all, "metrics": metrics_all},
        "without_cognitive": {"features": used_nocog, "metrics": metrics_nocog},
    }
    (REPORTS_DIR / "with_without_cognitive_metrics.json").write_text(json.dumps(with_without, indent=2))

    # Temporal / site validation feasibility summary
    temp_site = temporal_site_validation(df, target)
    (REPORTS_DIR / "temporal_site_validation.json").write_text(json.dumps(temp_site, indent=2))

    # Nested CV for LR and GB
    nested = {
        "logistic_regression": nested_cv_scores(
            lr,
            {"C": [0.1, 1.0, 10.0], "penalty": ["l1", "l2"], "solver": ["liblinear"]},
            X_all,
            y,
        ),
        "gradient_boosting": nested_cv_scores(
            gb,
            {"n_estimators": [100, 200], "learning_rate": [0.05, 0.1], "max_depth": [2, 3, 5]},
            X_all,
            y,
        ),
    }
    (REPORTS_DIR / "nested_cv_summary.json").write_text(json.dumps(nested, indent=2))

    print("\nAudit complete. Reports saved to 'reports/'.")
    print("- leakage_audit_report.json")
    print("- with_without_cognitive_metrics.json")
    print("- temporal_site_validation.json")
    print("- nested_cv_summary.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
