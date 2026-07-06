# Validation Notes

This first version uses cross-validated baselines on synthetic data. It is not clinically valid.

A clinical-grade version would require:

- predefined target definition
- pre-registered analysis plan
- train/validation/test separation by cohort/site/time where possible
- feature selection inside cross-validation only
- external validation cohort
- calibration curves and calibration slope/intercept
- bootstrap confidence intervals
- missingness and out-of-distribution checks
- subgroup performance analysis
- model card and data card
- audit trail for model version, data version, and report version
