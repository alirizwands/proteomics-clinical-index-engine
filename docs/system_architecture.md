# System Architecture — Proteomics Clinical Index Engine

## Architecture overview

```text
Synthetic or real Olink-style NPX file
   ↓
Schema validation and QC
   ↓
Sample/protein filtering, missingness and LOD handling
   ↓
Long-to-wide ML matrix creation
   ↓
Leakage-safe ML pipeline
   - imputation
   - scaling
   - feature selection inside CV
   - sparse/high-dimensional model
   ↓
Model evaluation
   - AUROC/AUPRC
   - Brier score
   - calibration curve
   - bootstrap intervals
   ↓
Clinical index scoring
   - probability → 0–100 score
   - green/amber/red band
   ↓
Confidence logic
   - margin
   - entropy
   - missingness
   - interval width
   ↓
Clinician review gate
   - routine review
   - review recommended
   - review required
   ↓
Clinician-facing report
   - index result
   - top protein drivers
   - validation snapshot
   - limitations and disclaimer
   ↓
Audit trail
   - timestamp
   - model version
   - input hash
   - output snapshot
```

## Key design choices

### 1. Separation of model and clinical score

The model produces probability. The clinical scoring layer converts probability into an index score, risk band, and decision-support summary.

### 2. Confidence is explicit

Confidence is not hidden inside a model. It is computed from transparent signals including entropy, missingness, prediction margin, and bootstrap interval width.

### 3. No autonomous diagnosis

The report and API output are explicitly framed as decision support. Red or low-confidence results require clinician review.

### 4. Auditability by design

The governance layer generates model version, input hash, output snapshot, and review requirement.

## Production upgrades

A production-grade implementation would add:

- external validation cohort
- locked preprocessing recipe
- model registry
- drift monitoring
- batch/site/assay robustness testing
- protected health data controls
- regulatory quality-management system
- clinician user-interface validation
