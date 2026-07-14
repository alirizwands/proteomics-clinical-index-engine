# Example Proteomics Clinical Index Report

**Generated:** 2026-07-06 19:45 UTC  
**Sample ID:** S048  
**Intended use:** Synthetic public reference implementation for demonstrating clinical-AI architecture. Not for diagnosis, treatment or patient management.

## 1. Index Result

- Index score: **96/100**
- Risk band: **Red**
- Model probability: **0.96**
- Confidence: **High** (0.88)
- Review gate: **Clinician review required: elevated index**

## 2. Sample Context

- Age: 75
- Sex: Male
- BMI: 35.3
- Collection day: 19
- Plate ID: Plate_B

## 3. Top Model Drivers

- **Protein_012**: increases index (relative contribution=0.922). No curated knowledge card available in this demo.
- **Protein_013**: increases index (relative contribution=0.779). No curated knowledge card available in this demo.
- **Protein_001**: increases index (relative contribution=0.697). Synthetic immune activation marker used for demonstration.
- **Protein_018**: increases index (relative contribution=0.455). No curated knowledge card available in this demo.
- **Protein_011**: increases index (relative contribution=0.450). No curated knowledge card available in this demo.
- **Protein_009**: increases index (relative contribution=0.376). No curated knowledge card available in this demo.
- **Protein_017**: increases index (relative contribution=0.357). No curated knowledge card available in this demo.
- **Protein_002**: increases index (relative contribution=0.286). Synthetic cardiometabolic stress marker used for demonstration.

## 4. Interpretation Guardrails

This output is a **decision-support summary**, not an autonomous diagnosis. It should be reviewed alongside clinical history, standard laboratory results, assay QC information, and clinician judgement. Red or low-confidence outputs require clinician review before any action is considered.

## 5. Synthetic Demonstration Metrics

These values were generated using synthetic demonstration data and must not be interpreted as evidence of clinical performance.

- AUROC: 1.0
- AUPRC: 1.0
- Brier score: 0.03420854832637001
- Expected calibration error: 0.08688098023558807

## 6. Limitations

- Demonstration uses synthetic Olink-style NPX data, not a clinical validation cohort.
- Protein knowledge cards are illustrative and must be replaced with curated biological evidence before real use.
- Confidence logic is transparent and auditable, but it is not clinically validated.
- This report should not be used for patient management.
