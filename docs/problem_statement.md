# Problem Statement: Proteomics Clinical Index Engine

## Clinical AI problem

High-dimensional proteomics platforms can measure hundreds to thousands of circulating proteins from a small blood sample, but raw protein measurements are not directly usable by clinicians. The clinical AI challenge is to convert Olink-style NPX protein profiles plus sample metadata into a structured, validated, confidence-aware output that can support clinician review.

This repository demonstrates an end-to-end applied ML workflow for a **Proteomic Severity Index**: a 0-100 clinical index derived from NPX-style protein measurements and clinical metadata.

## Intended use

The demo system is designed as **clinical decision support** for research and portfolio demonstration. It is intended to show how a clinical AI team could build the ML scoring, confidence, validation, reporting, and audit layers behind proteomics-driven health indices.

The system is **not** intended for autonomous diagnosis, treatment selection, patient triage, or real clinical use without prospective validation, regulatory review, locked model governance, and clinician oversight.

## Target users

- Applied ML / clinical AI team building biomarker-index products.
- Bioinformatics team preparing Olink-style NPX datasets for ML.
- Clinical/product stakeholders reviewing index output and report usability.
- Regulatory/governance stakeholders assessing traceability, validation, and safety logic.

## Inputs

- Long-format Olink-style NPX table: sample, assay/protein, panel, NPX, LOD, QC flags, and missingness information.
- Sample/clinical metadata: age, sex, BMI, disease/status labels, severity/outcome labels, collection timing, plate/batch IDs, and sample QC status.

## Outputs

- QC summaries at sample and protein level.
- ML-ready wide protein matrix.
- Baseline high-dimensional ML models.
- Candidate protein drivers/signatures.
- 0-100 proteomic index score.
- Green/amber/red risk band.
- Confidence label and review gate.
- Clinician-facing report.
- Audit trail with model/output metadata.

## Success criteria for the portfolio project

1. Data ingestion and QC are explicit, reproducible, and auditable.
2. Modelling avoids leakage by keeping preprocessing and feature selection inside ML pipelines.
3. Model outputs are translated into clinically readable index-level scores.
4. Confidence logic is separated from raw probability.
5. Low-confidence or high-risk outputs trigger clinician review.
6. The system includes documentation expected in regulated clinical AI: model card, data card, validation protocol, safety notes, and audit record.

## Demonstration limitation

The included data is synthetic/Olink-style demo data. It is useful for showing engineering, workflow design, and clinical AI system thinking, but it cannot support biological claims, diagnostic claims, or clinical performance claims.
