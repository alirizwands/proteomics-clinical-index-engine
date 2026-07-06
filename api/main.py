"""Minimal FastAPI scaffold for the Proteomics Clinical Index Engine.

Run after installing optional FastAPI dependencies:
    pip install fastapi uvicorn
    uvicorn api.main:app --reload
"""

from __future__ import annotations

from typing import Dict, List

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except Exception:  # pragma: no cover
    FastAPI = None
    BaseModel = object

from src.proteomics_index.scoring import probability_to_index, assign_risk_band, decision_gate


if FastAPI is not None:
    app = FastAPI(title="Proteomics Clinical Index Engine", version="0.2.0-demo")
else:  # pragma: no cover
    app = None


class ScoreRequest(BaseModel):
    sample_id: str
    probability: float
    confidence_label: str = "Moderate"
    confidence_score: float = 0.5
    top_proteins: List[str] = []


if app is not None:
    @app.post("/score")
    def score_index(request: ScoreRequest) -> Dict[str, object]:
        index_score = probability_to_index(request.probability)
        band = assign_risk_band(index_score)
        return {
            "sample_id": request.sample_id,
            "index_score": index_score,
            "risk_band": band,
            "confidence_label": request.confidence_label,
            "confidence_score": request.confidence_score,
            "decision_gate": decision_gate(band, request.confidence_label),
            "top_proteins": request.top_proteins,
            "clinical_use_status": "research_demo_not_for_clinical_use",
        }
