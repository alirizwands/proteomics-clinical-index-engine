"""Leakage-safe baseline modelling utilities for high-dimensional proteomics."""

from __future__ import annotations

from typing import Dict, Iterable

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def make_baseline_models(k_features: int = 40, random_state: int = 42) -> Dict[str, Pipeline]:
    """Create leakage-safe scikit-learn pipelines.

    Feature selection is inside the pipeline, therefore it is refit within each CV fold.
    """
    return {
        "Dummy": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("model", DummyClassifier(strategy="prior")),
            ]
        ),
        "ElasticNet_LogReg": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("select", SelectKBest(score_func=f_classif, k=k_features)),
                (
                    "model",
                    LogisticRegression(
                        penalty="elasticnet",
                        solver="saga",
                        l1_ratio=0.5,
                        C=0.3,
                        max_iter=5000,
                        class_weight="balanced",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
        "RandomForest": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("select", SelectKBest(score_func=f_classif, k=k_features)),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=4,
                        min_samples_leaf=4,
                        class_weight="balanced_subsample",
                        random_state=random_state,
                    ),
                ),
            ]
        ),
    }


def binary_metrics(y_true: Iterable[int], y_prob: Iterable[float], threshold: float = 0.5) -> dict:
    """Compute clinical-style binary classification metrics."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    y_pred = (y_prob >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else np.nan
    specificity = tn / (tn + fp) if (tn + fp) > 0 else np.nan

    return {
        "AUROC": roc_auc_score(y_true, y_prob),
        "AUPRC": average_precision_score(y_true, y_prob),
        "Brier": brier_score_loss(y_true, y_prob),
        "Sensitivity": sensitivity,
        "Specificity": specificity,
    }


def evaluate_cv_models(
    X: pd.DataFrame,
    y: pd.Series,
    models: Dict[str, Pipeline],
    n_splits: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Evaluate models with out-of-fold predicted probabilities."""
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    rows = []
    for name, model in models.items():
        y_prob = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]
        metrics = binary_metrics(y, y_prob)
        metrics["Model"] = name
        rows.append(metrics)
    return pd.DataFrame(rows).set_index("Model").sort_values("AUROC", ascending=False)


def top_selected_features(
    model: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    top_n: int = 20,
) -> pd.DataFrame:
    """Fit a feature-selection model and return selected features with ANOVA F scores."""
    model.fit(X, y)
    selector = model.named_steps.get("select")
    if selector is None:
        return pd.DataFrame(columns=["feature", "score"])

    selected_idx = selector.get_support(indices=True)
    scores = selector.scores_[selected_idx]
    selected_features = X.columns[selected_idx]
    table = pd.DataFrame({"feature": selected_features, "anova_f_score": scores})
    return table.sort_values("anova_f_score", ascending=False).head(top_n)
