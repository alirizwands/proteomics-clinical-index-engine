# Validation Protocol — Proteomics Clinical Index Engine

## Purpose

This document defines the validation approach for a portfolio-grade clinical AI pipeline that converts Olink-style NPX proteomic profiles and clinical metadata into confidence-aware index-level outputs.

## Intended demonstration

The repository is **not a medical device** and is not intended for clinical use. It demonstrates an architecture for:

1. Olink-style NPX ingestion and QC
2. small-sample, high-dimensional proteomics ML
3. leakage-safe feature selection and model validation
4. calibrated probability estimation
5. confidence-aware 0–100 clinical index scoring
6. clinician-facing report generation
7. traceability, auditability, and clinician-review gates

## Validation design

### Data readiness controls

- Validate required NPX fields: SampleID, OlinkID, UniProt, Assay, Panel, NPX, LOD, SampleQC, QC_Warning.
- Summarise sample-level missingness and assay warning rates.
- Summarise protein-level missingness and below-LOD rates.
- Convert long-format NPX into an ML-ready sample × protein matrix.

### Leakage controls

- All imputation, scaling, and feature selection are inside scikit-learn pipelines.
- Feature selection is refit inside each CV fold.
- Test data are not used for threshold selection or model fitting.

### Model evaluation

Minimum reported metrics:

- AUROC
- AUPRC
- Brier score
- sensitivity and specificity
- expected calibration error
- calibration curve
- bootstrap prediction intervals

### Confidence logic

Confidence is estimated from transparent signals:

- prediction margin from the decision boundary
- binary entropy
- missingness rate
- bootstrap interval width

Outputs are categorised as High, Moderate, or Low confidence.

### Clinical review gates

- Red band → clinician review required
- Amber band → clinician review recommended
- Low confidence → clinician review required
- Green/high-confidence → routine clinician review

No output is framed as an autonomous diagnosis.

## Key limitations

- The included data are synthetic and cannot support clinical claims.
- Protein knowledge cards are illustrative.
- Thresholds are demonstrative and must be validated prospectively.
- Calibration and confidence logic require external validation on real cohorts.
