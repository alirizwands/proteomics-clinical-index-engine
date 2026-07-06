"""Calibration, uncertainty, and confidence logic for clinical proteomics models."""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, log_loss
from sklearn.utils import resample


def entropy_binary(probability: Iterable[float]) -> np.ndarray:
    """Binary prediction entropy in [0, 1], where 1 is maximally uncertain."""
    p = np.clip(np.asarray(probability, dtype=float), 1e-6, 1 - 1e-6)
    entropy = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return entropy


def missingness_penalty(X: pd.DataFrame) -> np.ndarray:
    """A simple patient-level penalty based on proportion of missing features."""
    return X.isna().mean(axis=1).to_numpy()


def confidence_score_from_signals(
    probabilities: Iterable[float],
    missingness: Iterable[float],
    ci_width: Iterable[float] | None = None,
) -> np.ndarray:
    """Combine margin, entropy, missingness, and CI width into a 0-1 confidence score.

    This is a transparent engineering heuristic for portfolio demonstration. A real
    clinical system would tune and validate this gate prospectively.
    """
    p = np.asarray(probabilities, dtype=float)
    miss = np.asarray(missingness, dtype=float)
    entropy = entropy_binary(p)
    margin = np.abs(p - 0.5) * 2
    score = 0.45 * margin + 0.35 * (1 - entropy) + 0.20 * (1 - np.clip(miss / 0.35, 0, 1))
    if ci_width is not None:
        width = np.asarray(ci_width, dtype=float)
        score = 0.80 * score + 0.20 * (1 - np.clip(width / 0.60, 0, 1))
    return np.clip(score, 0, 1)


def confidence_label(scores: Iterable[float]) -> np.ndarray:
    """Map confidence score to High / Moderate / Low."""
    scores = np.asarray(scores, dtype=float)
    labels = np.full(scores.shape, "Low", dtype=object)
    labels[scores >= 0.45] = "Moderate"
    labels[scores >= 0.70] = "High"
    return labels


def bootstrap_prediction_intervals(
    estimator,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_eval: pd.DataFrame,
    n_bootstraps: int = 80,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Bootstrap model fits to approximate prediction uncertainty.

    For speed and reproducibility this defaults to 80 bootstraps. Increase for a
    real validation study.
    """
    rng = np.random.default_rng(random_state)
    preds = []
    for _ in range(n_bootstraps):
        seed = int(rng.integers(0, 1_000_000))
        X_bs, y_bs = resample(X_train, y_train, replace=True, stratify=y_train, random_state=seed)
        est = clone(estimator)
        est.fit(X_bs, y_bs)
        preds.append(est.predict_proba(X_eval)[:, 1])
    pred_matrix = np.vstack(preds)
    return (
        np.mean(pred_matrix, axis=0),
        np.quantile(pred_matrix, 0.025, axis=0),
        np.quantile(pred_matrix, 0.975, axis=0),
    )


def calibration_summary(y_true: Iterable[int], y_prob: Iterable[float], n_bins: int = 5) -> dict:
    """Return compact calibration metrics."""
    y_true = np.asarray(y_true)
    y_prob = np.clip(np.asarray(y_prob, dtype=float), 1e-6, 1 - 1e-6)
    frac_pos, mean_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy="quantile")
    ece = np.mean(np.abs(frac_pos - mean_pred))
    return {
        "brier_score": float(brier_score_loss(y_true, y_prob)),
        "log_loss": float(log_loss(y_true, y_prob)),
        "expected_calibration_error": float(ece),
        "calibration_bins": pd.DataFrame(
            {"mean_predicted_probability": mean_pred, "observed_event_rate": frac_pos}
        ),
    }
