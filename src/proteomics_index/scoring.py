"""Clinical index scoring utilities for proteomics ML outputs.

The functions in this module intentionally separate model probability from clinical
presentation. A classifier probability is not, by itself, a clinical product. A
clinical index needs score mapping, risk bands, confidence logic, explanation,
review gates, and auditability.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable, List, Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ClinicalIndexResult:
    """Clinician-facing index result for a single sample."""

    sample_id: str
    probability: float
    index_score: int
    risk_band: str
    confidence_label: str
    confidence_score: float
    decision_gate: str
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)


def probability_to_index(probability: float) -> int:
    """Map a calibrated probability to a 0-100 clinical index score."""
    if probability is None or np.isnan(probability):
        return 0
    return int(np.round(np.clip(probability, 0, 1) * 100))


def assign_risk_band(index_score: int, green_threshold: int = 35, red_threshold: int = 65) -> str:
    """Assign red/amber/green status from a 0-100 index score."""
    if index_score < green_threshold:
        return "Green"
    if index_score < red_threshold:
        return "Amber"
    return "Red"


def decision_gate(risk_band: str, confidence_label: str) -> str:
    """Clinical review routing rule.

    This avoids autonomous diagnosis. High-risk or low-confidence outputs are
    escalated for clinician review instead of being auto-actioned.
    """
    if confidence_label == "Low":
        return "Clinician review required: low confidence"
    if risk_band == "Red":
        return "Clinician review required: elevated index"
    if risk_band == "Amber":
        return "Clinician review recommended"
    return "Routine clinician review"


def compute_index_table(
    sample_ids: Iterable[str],
    probabilities: Iterable[float],
    confidence_labels: Iterable[str],
    confidence_scores: Iterable[float],
    ci_lower: Optional[Iterable[float]] = None,
    ci_upper: Optional[Iterable[float]] = None,
) -> pd.DataFrame:
    """Build a tabular set of ClinicalIndexResult rows."""
    rows = []
    sample_ids = list(sample_ids)
    probabilities = list(probabilities)
    confidence_labels = list(confidence_labels)
    confidence_scores = list(confidence_scores)
    ci_lower_values = list(ci_lower) if ci_lower is not None else [None] * len(sample_ids)
    ci_upper_values = list(ci_upper) if ci_upper is not None else [None] * len(sample_ids)

    for sid, prob, label, conf_score, low, high in zip(
        sample_ids,
        probabilities,
        confidence_labels,
        confidence_scores,
        ci_lower_values,
        ci_upper_values,
    ):
        score = probability_to_index(float(prob))
        band = assign_risk_band(score)
        result = ClinicalIndexResult(
            sample_id=str(sid),
            probability=float(prob),
            index_score=score,
            risk_band=band,
            confidence_label=str(label),
            confidence_score=float(conf_score),
            decision_gate=decision_gate(band, str(label)),
            ci_lower=None if low is None or pd.isna(low) else float(low),
            ci_upper=None if high is None or pd.isna(high) else float(high),
        )
        rows.append(result.to_dict())
    return pd.DataFrame(rows)


def linear_model_feature_contributions(
    fitted_pipeline,
    sample: pd.Series,
    feature_names: List[str],
    top_n: int = 8,
) -> pd.DataFrame:
    """Approximate per-sample feature contributions for a fitted linear pipeline.

    This supports pipelines with: imputer -> scaler -> select -> model. It returns
    selected protein features ranked by absolute coefficient*z contribution.
    """
    steps = fitted_pipeline.named_steps
    imputer = steps.get("imputer")
    scaler = steps.get("scaler")
    selector = steps.get("select")
    model = steps.get("model")

    if model is None or not hasattr(model, "coef_"):
        return pd.DataFrame(columns=["feature", "direction", "contribution", "coefficient"])

    x = pd.DataFrame([sample[feature_names].values], columns=feature_names)
    arr = x.values
    if imputer is not None:
        arr = imputer.transform(arr)
    if scaler is not None:
        arr = scaler.transform(arr)

    selected_feature_names = list(feature_names)
    if selector is not None:
        support = selector.get_support(indices=True)
        arr = selector.transform(arr)
        selected_feature_names = [feature_names[i] for i in support]

    coefficients = model.coef_.ravel()
    contributions = arr.ravel() * coefficients
    table = pd.DataFrame(
        {
            "feature": selected_feature_names,
            "coefficient": coefficients,
            "contribution": contributions,
        }
    )
    table["direction"] = np.where(table["contribution"] >= 0, "increases index", "decreases index")
    table["absolute_contribution"] = table["contribution"].abs()
    return table.sort_values("absolute_contribution", ascending=False).head(top_n).reset_index(drop=True)
