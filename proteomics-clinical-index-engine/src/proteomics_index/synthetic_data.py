"""Synthetic Olink-style NPX data generator.

The generated data is intentionally synthetic and safe for public GitHub use.
It mimics long-format NPX outputs commonly used in Olink-style workflows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticOlinkConfig:
    n_samples: int = 96
    n_proteins: int = 240
    n_panels: int = 4
    disease_prevalence: float = 0.35
    signal_proteins: int = 18
    random_state: int = 42


def generate_synthetic_olink_npx(
    config: SyntheticOlinkConfig = SyntheticOlinkConfig(),
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate synthetic Olink-style long-format NPX data and metadata.

    Returns
    -------
    npx_long:
        Long-format dataframe with Olink-like columns.
    metadata:
        Sample-level clinical metadata.
    """

    rng = np.random.default_rng(config.random_state)

    sample_ids = [f"S{i:03d}" for i in range(1, config.n_samples + 1)]
    subject_ids = [f"P{i:03d}" for i in range(1, config.n_samples + 1)]

    age = rng.integers(24, 82, size=config.n_samples)
    sex = rng.choice(["Female", "Male"], size=config.n_samples, p=[0.55, 0.45])
    bmi = np.round(rng.normal(27, 5, size=config.n_samples).clip(17, 45), 1)

    # Disease/severity is synthetic, but designed so selected proteins carry signal.
    disease = rng.binomial(1, config.disease_prevalence, size=config.n_samples)
    latent_severity = (
        0.035 * (age - 50)
        + 0.08 * (bmi - 27)
        + 1.15 * disease
        + rng.normal(0, 0.85, size=config.n_samples)
    )
    who_severity = np.clip(np.round(3 + latent_severity).astype(int), 1, 8)
    severe_outcome = (who_severity >= 5).astype(int)

    metadata = pd.DataFrame(
        {
            "SampleID": sample_ids,
            "SubjectID": subject_ids,
            "Age": age,
            "Sex": sex,
            "BMI": bmi,
            "DiseaseStatus": np.where(disease == 1, "Case", "Control"),
            "WHO_Severity": who_severity,
            "SevereOutcome": severe_outcome,
            "CollectionDay": rng.integers(0, 28, size=config.n_samples),
            "PlateID": rng.choice(["Plate_A", "Plate_B", "Plate_C", "Plate_D"], size=config.n_samples),
            "SampleQC": rng.choice(["Pass", "Warning"], size=config.n_samples, p=[0.91, 0.09]),
        }
    )

    panels = [
        "Olink Inflammation",
        "Olink Cardiometabolic",
        "Olink Neurology",
        "Olink Oncology",
    ][: config.n_panels]

    proteins = []
    for j in range(config.n_proteins):
        panel = panels[j % len(panels)]
        proteins.append(
            {
                "OlinkID": f"OID{10000 + j}",
                "UniProt": f"P{10000 + j}",
                "Assay": f"Protein_{j:03d}",
                "Panel": panel,
            }
        )
    proteins_df = pd.DataFrame(proteins)

    signal_idx = np.arange(min(config.signal_proteins, config.n_proteins))
    rows = []

    for s_idx, sample in enumerate(sample_ids):
        plate_shift = {"Plate_A": 0.0, "Plate_B": 0.07, "Plate_C": -0.05, "Plate_D": 0.03}[
            metadata.loc[s_idx, "PlateID"]
        ]
        for p_idx, protein in proteins_df.iterrows():
            base = rng.normal(8.5, 0.8)
            age_effect = 0.006 * (metadata.loc[s_idx, "Age"] - 50)
            bmi_effect = 0.01 * (metadata.loc[s_idx, "BMI"] - 27)

            # First proteins have biologically plausible disease/severity signal.
            if p_idx in signal_idx:
                direction = 1 if p_idx % 3 != 0 else -1
                disease_effect = direction * (0.45 + 0.04 * p_idx) * severe_outcome[s_idx]
            else:
                disease_effect = rng.normal(0, 0.04)

            npx = base + age_effect + bmi_effect + plate_shift + disease_effect + rng.normal(0, 0.35)
            lod = base - rng.uniform(1.1, 2.0)

            below_lod = npx < lod or rng.random() < 0.025
            if below_lod:
                npx_value = np.nan if rng.random() < 0.55 else lod - rng.uniform(0.05, 0.35)
            else:
                npx_value = npx

            rows.append(
                {
                    "SampleID": sample,
                    "OlinkID": protein["OlinkID"],
                    "UniProt": protein["UniProt"],
                    "Assay": protein["Assay"],
                    "Panel": protein["Panel"],
                    "NPX": np.round(npx_value, 4) if pd.notna(npx_value) else np.nan,
                    "LOD": np.round(lod, 4),
                    "QC_Warning": "Warning" if rng.random() < 0.035 else "Pass",
                    "PlateID": metadata.loc[s_idx, "PlateID"],
                    "SampleQC": metadata.loc[s_idx, "SampleQC"],
                    "BelowLOD": bool(below_lod),
                }
            )

    npx_long = pd.DataFrame(rows)

    missing_freq = (
        npx_long.assign(is_missing=lambda df: df["NPX"].isna())
        .groupby("OlinkID")["is_missing"]
        .mean()
        .rename("MissingFreq")
        .reset_index()
    )
    npx_long = npx_long.merge(missing_freq, on="OlinkID", how="left")

    return npx_long, metadata


if __name__ == "__main__":
    npx, meta = generate_synthetic_olink_npx()
    npx.to_csv("data/sample/olink_synthetic_npx.csv", index=False)
    meta.to_csv("data/sample/sample_metadata.csv", index=False)
