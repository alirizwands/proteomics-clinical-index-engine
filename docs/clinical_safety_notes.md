# Clinical Safety Notes

This project demonstrates clinical AI engineering discipline, not clinical deployment readiness.

## Safety principles

1. **Decision support only** - outputs are not autonomous diagnoses.
2. **Clinician review** - red and low-confidence outputs are routed to clinician review.
3. **Traceability** - outputs include model version, input hash, and generated audit record.
4. **Transparency** - confidence logic is rule-based and inspectable.
5. **Validation separation** - discrimination, calibration, confidence, and report completeness are evaluated separately.
6. **Privacy by design** - synthetic data are used; no PHI is included.

## Production hardening still required

- prospective clinical validation
- predefined operating points
- bias/fairness assessment
- assay/site/batch robustness assessment
- drift monitoring
- locked model versioning
- regulatory quality-management processes
- human factors evaluation
