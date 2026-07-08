# Model Card: Proteomic Severity Index Demo

## Model name

ElasticNet_LogReg_ProteomicSeverityIndex

## Version

0.2.0-demo

## Model type

Sparse logistic regression pipeline with median imputation, standard scaling, univariate feature selection, and elastic-net regularisation.

## Intended use

Portfolio demonstration of a clinical AI scoring layer for Olink-style proteomics data. The model demonstrates how NPX data can be transformed into a calibrated, confidence-aware index output.

## Not intended for

- diagnosis
- treatment decisions
- patient management
- clinical triage
- regulatory submission

## Inputs

- Sample × protein NPX matrix
- Sample metadata, where available
- Missingness indicators used indirectly for confidence logic

## Outputs

- calibrated or uncalibrated probability
- 0–100 proteomic severity index
- green/amber/red risk band
- confidence label
- clinician-review gate
- top protein drivers
- audit record

## Performance reporting

The demo reports AUROC, AUPRC, Brier score, expected calibration error, sensitivity, specificity, and routing summaries. Because the data are synthetic, these values demonstrate workflow capability rather than clinical validity.

## Safety controls

- no autonomous diagnosis
- low-confidence escalation
- red-band escalation
- report disclaimers
- audit trail with input hash and model version
- feature-selection leakage controls
