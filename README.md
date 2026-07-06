# Proteomics Clinical Index Engine

An end-to-end **clinical AI / applied ML** starter project for Olink-style proteomic data. It demonstrates how to convert high-dimensional NPX protein profiles and clinical metadata into validated machine-learning baselines, leakage-safe evaluation workflows, and the foundation for index-level clinical scores.

This repo is designed as a portfolio project for roles such as **Head of Applied ML and Clinical AI**, **Clinical AI Scientist**, **Translational AI Systems Lead**, or **AI-SaMD / Clinical Decision Support ML Lead**.

## What this first version contains

### Notebook 01 — Olink-style NPX QC
`notebooks/01_olink_npx_qc.ipynb`

Shows how to:
- generate/load synthetic Olink-style long-format NPX data
- inspect core NPX fields: `SampleID`, `OlinkID`, `UniProt`, `Assay`, `Panel`, `LOD`, `NPX`, `QC_Warning`, `SampleQC`, `MissingFreq`
- run sample-level and protein-level QC
- evaluate missingness and below-LOD behaviour
- convert long-format proteomics data into a wide ML-ready matrix
- save ML-ready `X`, `y`, and metadata tables

### Notebook 02 — High-dimensional ML baselines
`notebooks/02_high_dimensional_ml_baselines.ipynb`

Shows how to:
- handle the high-dimensional small-sample setting common in proteomics (`p > n`)
- build leakage-safe scikit-learn pipelines
- perform feature selection inside cross-validation
- compare baseline models
- report AUROC, AUPRC, Brier score, sensitivity, specificity, and selected protein signatures

## Why this matters clinically

Proteomics products do not just need a classifier. They need a **clinical index engine**: QC, cohort-aware preprocessing, signal-to-score logic, confidence logic, validation, reproducibility, auditability, and clinician-facing interpretation.

This first version focuses on the first two layers:

1. **NPX data readiness and quality control**
2. **Leakage-safe high-dimensional ML baselines**

The next versions should add:
- calibrated 0–100 index scores
- confidence bands and indeterminate-zone logic
- biomarker explanations
- clinician-facing report generation
- validation protocol and model card
- FastAPI/Streamlit demo

## Data

The repo includes a small **synthetic Olink-style NPX dataset** under `data/sample/`. It is not real patient data and is safe for public GitHub use.

Files:
- `data/sample/olink_synthetic_npx.csv`
- `data/sample/sample_metadata.csv`

## Python setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

## Optional Python alternative to OlinkAnalyze

OlinkAnalyze is the official R ecosystem package. For Python-only workflows, this repo uses pandas/scikit-learn and defines minimal Olink-style QC utilities in `src/proteomics_index/`. You can also explore `pyprideap`, a Python package that supports Olink Explore/Explore HT/Target/Reveal and SomaScan files, QC reports, LOD handling, preprocessing, normalization, and statistical analysis.

## Clinical-use disclaimer

This project is for education, portfolio demonstration, and engineering design only. It is not a medical device, diagnostic system, or clinical decision-support tool.
