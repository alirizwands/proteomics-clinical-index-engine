"""Governance, auditability, and validation documentation helpers."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict

import pandas as pd


def dataframe_hash(df: pd.DataFrame) -> str:
    """Stable-ish hash for a dataframe snapshot."""
    content = pd.util.hash_pandas_object(df, index=True).values.tobytes()
    return hashlib.sha256(content).hexdigest()


def make_audit_record(
    sample_id: str,
    model_name: str,
    model_version: str,
    input_hash: str,
    output: Dict[str, Any],
    reviewer_required: bool,
) -> Dict[str, Any]:
    """Build an audit record for a single inference."""
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sample_id": sample_id,
        "model_name": model_name,
        "model_version": model_version,
        "input_hash_sha256": input_hash,
        "output": output,
        "reviewer_required": reviewer_required,
        "clinical_use_status": "research_demo_not_for_clinical_use",
    }


def save_json(record: Dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)


def make_validation_protocol_text() -> str:
    return """# Validation Protocol — Proteomic Clinical Index Engine

## Intended Demonstration Scope

This repository demonstrates a clinical AI architecture for transforming Olink-style NPX proteomic data into calibrated index-level outputs. It is not a validated diagnostic or clinical decision-support device.

## Validation Questions

1. Can Olink-style NPX data be transformed into ML-ready matrices with reproducible QC?
2. Can high-dimensional proteomic models be trained without feature-selection leakage?
3. Are probabilities calibrated enough to support index-level score presentation?
4. Does confidence logic identify low-confidence or high-risk cases for clinician review?
5. Are model outputs traceable to input data, model version, and explanation artifacts?

## Controls Against Common Failure Modes

- Feature selection is inside the cross-validation pipeline.
- Calibration is evaluated separately from discrimination.
- Missingness is reflected in confidence logic.
- High-risk and low-confidence cases are routed to clinician review.
- Reports are labelled as decision support, not autonomous diagnosis.
- Audit records include input hash, model version, and output snapshot.

## Metrics

- AUROC and AUPRC for discrimination.
- Brier score and expected calibration error for calibration.
- Sensitivity/specificity at operating thresholds.
- Confidence-band coverage and indeterminate-zone rate.
- Report completeness and auditability checks.
"""
