# Data Card — Synthetic Olink-style NPX Dataset

## Dataset type

Synthetic Olink-style proteomics dataset for public GitHub demonstration.

## Why synthetic data?

The repository is designed to be publicly shareable without patient data, proprietary data, or protected health information. The synthetic data mimic common NPX workflow structure but do not represent real patients.

## Files

- `data/sample/olink_synthetic_npx.csv`
- `data/sample/sample_metadata.csv`
- `data/processed/X_proteomics.csv`
- `data/processed/y_severe_outcome.csv`
- `data/processed/metadata_model.csv`

## NPX-style fields

- SampleID
- OlinkID
- UniProt
- Assay
- Panel
- NPX
- LOD
- QC_Warning
- SampleQC
- BelowLOD
- MissingFreq

## Limitations

- No clinical claims can be made.
- Synthetic effect sizes are intentionally constructed.
- Protein names are placeholders.
- Biology knowledge cards are illustrative.

## Recommended next dataset upgrade

Add a public Olink NPX dataset and reproduce the same workflow with real cohort data, while keeping patient privacy and licensing constraints explicit.
