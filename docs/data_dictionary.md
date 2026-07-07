# Data Dictionary

This file documents the schema used in the demo proteomics clinical AI pipeline. The project uses synthetic Olink-style NPX data to demonstrate data handling, QC, ML modelling, index scoring, reporting, and governance.

## `data/sample/olink_synthetic_npx.csv`

Long-format NPX-style proteomics file. Each row represents one protein assay measurement for one sample.

| Column | Type | Description | Notes |
|---|---|---|---|
| `SampleID` | string | Unique sample identifier | Join key to sample metadata |
| `OlinkID` | string | Olink-style assay identifier | Synthetic demo identifier |
| `UniProt` | string | UniProt-style protein identifier | Synthetic demo identifier |
| `Assay` | string | Protein/assay feature name | Used as ML feature after pivoting |
| `Panel` | string | Proteomics panel/category | Useful for panel-level QC |
| `NPX` | float | Normalized protein expression value | Olink-style log-scale value; may be missing |
| `LOD` | float | Limit of detection threshold | Used to flag weak/low measurements |
| `QC_Warning` | string | Per-measurement QC flag | Expected values include `Pass` or warning labels |
| `PlateID` | string | Assay plate/batch identifier | Used for batch/plate summaries |
| `SampleQC` | string | Sample-level QC flag copied into long table | Join/consistency check with metadata |
| `BelowLOD` | boolean | Whether NPX is below LOD | Used in QC summaries/confidence logic |
| `MissingFreq` | float | Assay-level missing frequency | Used for feature reliability review |

## `data/sample/sample_metadata.csv`

Sample-level metadata table. Each row represents one sample/patient record in the demo dataset.

| Column | Type | Description | Notes |
|---|---|---|---|
| `SampleID` | string | Unique sample identifier | Primary join key |
| `SubjectID` | string | Subject/patient identifier | Synthetic demo identifier |
| `Age` | integer | Age in years | Clinical covariate |
| `Sex` | string | Biological sex category in demo data | Clinical covariate |
| `BMI` | float | Body mass index | Clinical covariate |
| `DiseaseStatus` | string | Demo disease/status group | Used for stratification/exploration |
| `WHO_Severity` | integer | Ordinal severity score | Demo severity target/covariate |
| `SevereOutcome` | integer | Binary severe outcome label | Main classification target in baseline notebooks |
| `CollectionDay` | integer | Day of sample collection relative to baseline | Temporal/context field |
| `PlateID` | string | Assay plate/batch identifier | Batch/plate summary field |
| `SampleQC` | string | Sample-level quality control status | Used for sample filtering/review |

## `data/processed/X_proteomics.csv`

ML-ready wide matrix produced from the long NPX table.

| Column type | Description |
|---|---|
| `SampleID` or index | Sample identifier |
| Protein feature columns | One column per protein assay after long-to-wide pivot |

## `data/processed/y_severe_outcome.csv`

Binary target file for the demo model.

| Column | Description |
|---|---|
| `SampleID` | Sample identifier |
| `SevereOutcome` | Binary label used for demonstration modelling |

## `data/processed/metadata_model.csv`

Sample metadata aligned to the processed ML matrix.

## Reports generated from QC and modelling

| File | Purpose |
|---|---|
| `reports/qc_summary.csv` | Global dataset and QC summary |
| `reports/protein_missingness.csv` | Protein-level missingness, below-LOD, and QC-warning rates |
| `reports/sample_qc_summary.csv` | Sample-level missingness, below-LOD, metadata, and QC status |
| `reports/baseline_model_results.csv` | Baseline ML performance metrics |
| `reports/candidate_protein_signature.csv` | Candidate protein features ranked in baseline modelling |
| `reports/top_protein_drivers.csv` | Interpretable top protein drivers for reporting/demo purposes |

## Privacy and governance note

The dataset in this repository is synthetic/demo data. In a real clinical dataset, `SubjectID`, timestamps, linkage keys, sample metadata, and clinical labels may be sensitive or identifiable. Raw clinical data should not be committed to GitHub. Use `data/raw/` locally only and document access controls separately.
