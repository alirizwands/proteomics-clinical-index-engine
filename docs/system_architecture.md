# System Architecture

```text
Olink-style NPX file + clinical metadata
        |
        v
Data ingestion and schema validation
        |
        v
QC layer: sample QC, protein QC, missingness, below-LOD, panel distributions
        |
        v
ML-ready matrix: samples x proteins
        |
        v
Leakage-safe ML pipeline: imputation, scaling, feature selection, model
        |
        v
Validation metrics: AUROC, AUPRC, Brier, sensitivity, specificity
        |
        v
Future layer: calibrated clinical index score, confidence logic, report generation
```
