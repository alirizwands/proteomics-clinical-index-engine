# Proteomics Foundations for Clinical AI

## What is proteomics?

Proteomics is the large-scale measurement of proteins. For clinical AI, proteins are useful because they are closer to current biological function than DNA sequence alone. A proteomic profile can capture inflammation, organ stress, immune activation, metabolic dysfunction, ageing biology, and disease progression.

## What is NPX?

NPX stands for Normalized Protein Expression. It is commonly used in Olink-style workflows as a normalized, relative, usually log-scale abundance value. Higher NPX means higher measured protein expression relative to the platform normalization approach.

## Why Olink-style data is different from ordinary tabular ML

Proteomics ML often has:

- many protein features and fewer samples
- missing values due to limit-of-detection and assay behaviour
- batch, plate, and panel effects
- correlated proteins and biological pathways
- high risk of leakage during feature selection
- need for calibration and confidence logic before clinical interpretation

## Clinical AI objective

The goal is not merely to classify disease. A clinically useful proteomics system should translate high-dimensional protein signals into:

- an index-level score
- confidence and uncertainty
- explainable protein/pathway contributors
- traceable validation evidence
- a clinician-facing report

This repository starts with QC and ML baselines, then can be extended into scoring, calibration, report generation, and governance.
