# Proteomics Clinical Index Engine

An end-to-end **clinical AI / applied ML** portfolio project for Olink-style proteomic data. It demonstrates how to convert high-dimensional NPX protein profiles and clinical metadata into **ML-ready data, leakage-safe models, calibrated probabilities, 0–100 clinical index scores, confidence-aware risk bands, biomarker explanations, clinician-facing reports, and audit records**.

## Repository walkthrough

https://github.com/user-attachments/assets/bc44a46d-94d0-4e22-b43c-5c98ec28bf7b

**Translating Protein Data into Confidence-Aware Clinical Scores**

A guided discussion of the complete public demonstration pipeline, covering
proteomic-data QC, high-dimensional modelling, calibration, index scoring,
confidence logic, clinician review, reporting, and auditability.

> This recording explains a synthetic-data educational demonstration. It is
> not a clinically validated diagnostic product, regulated medical device,
> or proprietary client implementation.



## Executive positioning

This is not a generic classifier notebook. It is a **clinical index engine**:

```text
Olink-style NPX data
   → QC + ML-ready transformation
   → high-dimensional proteomics ML
   → calibration + uncertainty
   → 0–100 clinical index
   → confidence + review gate
   → clinician-facing report
   → audit trail + validation docs
```
## Scope 

This repository is an intentionally developed functional demonstration of a clinical proteomics AI pipeline. It has been prepared for education, technical communication, and controlled demonstration purposes, showing how Olink-style NPX data can be handled, quality-checked, transformed into ML-ready datasets, modelled using high-dimensional biomedical ML methods, converted into index-level scores, and presented through confidence-aware, clinician-reviewable outputs.

The repository does not contain any proprietary client code, confidential datasets, production infrastructure, regulatory submissions, commercial algorithms, or implementation details from real-world delivered systems. Actual production or client-facing systems in this domain are substantially more complex and may include additional protected components such as validated clinical datasets, regulated software architecture, security controls, quality-management workflows, audit evidence, monitoring pipelines, regulatory documentation, human-in-the-loop governance, and organisation-specific deployment processes.

This demo is therefore designed to communicate the methodology, architecture, and applied AI thinking behind clinical proteomics decision-support systems without disclosing protected intellectual property, confidential project assets, or NDA-restricted implementation details.

## What the project demonstrates

### Notebook 01: Olink-style NPX QC
`notebooks/01_olink_npx_qc.ipynb`

Shows how to:

- generate/load synthetic Olink-style long-format NPX data
- inspect NPX fields: `SampleID`, `OlinkID`, `UniProt`, `Assay`, `Panel`, `LOD`, `NPX`, `QC_Warning`, `SampleQC`, `MissingFreq`
- run sample-level and protein-level QC
- evaluate missingness and below-LOD behaviour
- convert long-format proteomics data into a wide ML-ready matrix
- save ML-ready `X`, `y`, and metadata tables

### Notebook 02: High-dimensional ML baselines
`notebooks/02_high_dimensional_ml_baselines.ipynb`

Shows how to:

- handle the small-sample/high-dimensional setting common in proteomics (`p > n`)
- build leakage-safe scikit-learn pipelines
- keep imputation, scaling, and feature selection inside CV
- compare baseline models
- report AUROC, AUPRC, Brier score, sensitivity, specificity, and selected protein signatures

### Notebook 03: Proteomic clinical index scoring
`notebooks/03_proteomic_clinical_index_scoring.ipynb`

Shows how to:

- train a sparse elastic-net proteomics model
- convert model probability into a 0–100 clinical index
- map scores to green/amber/red bands
- attach confidence labels
- generate a clinician-review gate
- extract top protein drivers for sample-level interpretation

### Notebook 04: Calibration, confidence, and review gates
`notebooks/04_calibration_confidence_and_review_gates.ipynb`

Shows how to:

- compare base vs calibrated probabilities
- report Brier score and expected calibration error
- plot a calibration curve
- generate bootstrap prediction intervals
- combine margin, entropy, missingness, and uncertainty into confidence logic
- produce routing summaries for clinician review

### Notebook 05: Clinician report and audit trail
`notebooks/05_clinician_report_and_audit_trail.ipynb`

Shows how to:

- generate a structured clinician-facing decision-support report
- include index score, risk band, confidence, review gate, top protein drivers, validation snapshot, limitations, and disclaimers
- generate an audit record with timestamp, model version, input hash, output snapshot, and review requirement
- check report completeness

## Repository structure

```text
proteomics-clinical-index-engine/
├── notebooks/
│   ├── 01_olink_npx_qc.ipynb
│   ├── 02_high_dimensional_ml_baselines.ipynb
│   ├── 03_proteomic_clinical_index_scoring.ipynb
│   ├── 04_calibration_confidence_and_review_gates.ipynb
│   └── 05_clinician_report_and_audit_trail.ipynb
├── src/proteomics_index/
│   ├── synthetic_data.py
│   ├── qc.py
│   ├── modeling.py
│   ├── scoring.py
│   ├── confidence.py
│   ├── report_generator.py
│   └── governance.py
├── docs/
│   ├── proteomics_foundations.md
│   ├── system_architecture.md
│   ├── validation_protocol.md
│   ├── validation_notes.md
│   ├── model_card.md
│   ├── data_card.md
│   ├── clinical_safety_notes.md
│   └── literature_benchmark.md
├── reports/
│   ├── baseline_model_results.csv
│   ├── candidate_protein_signature.csv
│   ├── patient_index_examples.csv
│   ├── calibration_validation_metrics.csv
│   ├── confidence_logic_examples.csv
│   ├── example_clinician_report.md
│   └── example_audit_record.json
├── app/streamlit_app.py
├── api/main.py
└── tests/
```

## Why this matters clinically

Proteomics products do not just need a model. They need a **clinical AI translation layer**: QC, cohort-aware preprocessing, signal-to-score logic, confidence logic, validation, reproducibility, auditability, and clinician-facing interpretation.

This repository demonstrates that translation pathway while using public-safe synthetic data.

## Data

The repo includes a small **synthetic Olink-style NPX dataset** under `data/sample/`. It is not real patient data and is safe for public GitHub use.

Files:

- `data/sample/olink_synthetic_npx.csv`
- `data/sample/sample_metadata.csv`
- `data/processed/X_proteomics.csv`
- `data/processed/y_severe_outcome.csv`
- `data/processed/metadata_model.csv`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Run tests:

```bash
pytest -q
```

Run optional API demo:

```bash
uvicorn api.main:app --reload
```

Run optional Streamlit demo:

```bash
streamlit run app/streamlit_app.py
```

## Python alternative to OlinkAnalyze

OlinkAnalyze is the official R ecosystem package. For Python-only workflows, this repo uses pandas/scikit-learn and defines minimal Olink-style QC utilities in `src/proteomics_index/`. You can also explore `pyprideap`, a Python package that supports Olink Explore/Explore HT/Target/Reveal and SomaScan-style workflows.

## Clinical-use disclaimer

This project is for education, portfolio demonstration, and engineering design only. It is **not** a medical device, diagnostic system, or clinical decision-support tool.
