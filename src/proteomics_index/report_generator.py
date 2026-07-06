"""Clinician-facing report generation for proteomics index outputs.

This module deliberately uses deterministic templating, not autonomous diagnosis.
It demonstrates how an LLM/RAG layer could be wrapped by structured model outputs,
knowledge cards, disclaimers, and clinician-review gates.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Optional

import pandas as pd


DEFAULT_PROTEIN_KNOWLEDGE: Dict[str, str] = {
    "Protein_000": "Synthetic inflammation-linked marker used for demonstration.",
    "Protein_001": "Synthetic immune activation marker used for demonstration.",
    "Protein_002": "Synthetic cardiometabolic stress marker used for demonstration.",
    "Protein_003": "Synthetic protective or inverse-signal marker used for demonstration.",
    "Protein_004": "Synthetic acute-phase marker used for demonstration.",
    "Protein_005": "Synthetic endothelial or vascular stress marker used for demonstration.",
    "Protein_006": "Synthetic metabolic regulation marker used for demonstration.",
    "Protein_007": "Synthetic immune-metabolic cross-talk marker used for demonstration.",
}


def make_clinician_report(
    index_row: pd.Series,
    metadata_row: pd.Series,
    contributions: pd.DataFrame,
    model_summary: Optional[dict] = None,
    protein_knowledge: Optional[Dict[str, str]] = None,
) -> str:
    """Create a structured clinician-facing Markdown report."""
    protein_knowledge = protein_knowledge or DEFAULT_PROTEIN_KNOWLEDGE
    model_summary = model_summary or {}
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    contribution_lines = []
    for _, row in contributions.iterrows():
        feature = row["feature"]
        knowledge = protein_knowledge.get(feature, "No curated knowledge card available in this demo.")
        contribution_lines.append(
            f"- **{feature}**: {row['direction']} "
            f"(relative contribution={row['contribution']:.3f}). {knowledge}"
        )

    contribution_text = "\n".join(contribution_lines) if contribution_lines else "- No model contribution table available."

    ci_text = ""
    if pd.notna(index_row.get("ci_lower")) and pd.notna(index_row.get("ci_upper")):
        ci_text = f"\n- Approximate probability interval: {index_row['ci_lower']:.2f}–{index_row['ci_upper']:.2f}"

    report = f"""# Proteomic Severity Index — Clinician Decision-Support Report

**Generated:** {generated_at}  
**Sample ID:** {index_row.get('sample_id', getattr(index_row, 'name', 'unknown'))}  
**Intended use:** Research/portfolio demonstration of clinical AI architecture. Not for diagnosis or treatment.

## 1. Index Result

- Index score: **{int(index_row['index_score'])}/100**
- Risk band: **{index_row['risk_band']}**
- Model probability: **{index_row['probability']:.2f}**{ci_text}
- Confidence: **{index_row['confidence_label']}** ({index_row['confidence_score']:.2f})
- Review gate: **{index_row['decision_gate']}**

## 2. Sample Context

- Age: {metadata_row.get('Age', 'not available')}
- Sex: {metadata_row.get('Sex', 'not available')}
- BMI: {metadata_row.get('BMI', 'not available')}
- Collection day: {metadata_row.get('CollectionDay', 'not available')}
- Plate ID: {metadata_row.get('PlateID', 'not available')}

## 3. Top Model Drivers

{contribution_text}

## 4. Interpretation Guardrails

This output is a **decision-support summary**, not an autonomous diagnosis. It should be reviewed alongside clinical history, standard laboratory results, assay QC information, and clinician judgement. Red or low-confidence outputs require clinician review before any action is considered.

## 5. Validation Snapshot

- AUROC: {model_summary.get('AUROC', 'not reported')}
- AUPRC: {model_summary.get('AUPRC', 'not reported')}
- Brier score: {model_summary.get('Brier', model_summary.get('brier_score', 'not reported'))}
- Expected calibration error: {model_summary.get('expected_calibration_error', 'not reported')}

## 6. Limitations

- Demonstration uses synthetic Olink-style NPX data, not a clinical validation cohort.
- Protein knowledge cards are illustrative and must be replaced with curated biological evidence before real use.
- Confidence logic is transparent and auditable, but it is not clinically validated.
- This report should not be used for patient management.
"""
    return report
