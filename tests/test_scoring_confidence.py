import numpy as np
import pandas as pd

from proteomics_index.scoring import probability_to_index, assign_risk_band, compute_index_table
from proteomics_index.confidence import entropy_binary, confidence_label


def test_probability_to_index_bounds():
    assert probability_to_index(0.0) == 0
    assert probability_to_index(1.0) == 100
    assert probability_to_index(0.735) == 74


def test_risk_bands():
    assert assign_risk_band(10) == "Green"
    assert assign_risk_band(50) == "Amber"
    assert assign_risk_band(90) == "Red"


def test_confidence_labels():
    labels = confidence_label(np.array([0.2, 0.5, 0.8]))
    assert list(labels) == ["Low", "Moderate", "High"]


def test_compute_index_table():
    table = compute_index_table(["S001"], [0.76], ["Moderate"], [0.55])
    assert table.loc[0, "index_score"] == 76
    assert table.loc[0, "risk_band"] == "Red"
    assert "clinician" in table.loc[0, "decision_gate"].lower()
