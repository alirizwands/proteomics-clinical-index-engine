"""QC and data-wrangling utilities for Olink-style NPX data."""

from __future__ import annotations

import pandas as pd


def summarize_npx(npx_long: pd.DataFrame) -> pd.DataFrame:
    """Return a compact QC summary for long-format NPX data."""
    required = {"SampleID", "OlinkID", "Assay", "Panel", "NPX", "LOD", "SampleQC", "QC_Warning"}
    missing = required - set(npx_long.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    summary = {
        "rows": len(npx_long),
        "samples": npx_long["SampleID"].nunique(),
        "proteins": npx_long["OlinkID"].nunique(),
        "panels": npx_long["Panel"].nunique(),
        "missing_npx_rate": npx_long["NPX"].isna().mean(),
        "below_lod_rate": npx_long.get("BelowLOD", pd.Series(index=npx_long.index, dtype=float)).mean(),
        "sample_qc_warning_rate": (npx_long["SampleQC"] != "Pass").mean(),
        "assay_qc_warning_rate": (npx_long["QC_Warning"] != "Pass").mean(),
    }
    return pd.DataFrame([summary]).T.rename(columns={0: "value"})


def sample_qc_table(npx_long: pd.DataFrame) -> pd.DataFrame:
    """Sample-level missingness and QC summary."""
    table = (
        npx_long.groupby("SampleID")
        .agg(
            n_proteins=("OlinkID", "nunique"),
            missing_rate=("NPX", lambda s: s.isna().mean()),
            below_lod_rate=("BelowLOD", "mean"),
            sample_qc=("SampleQC", "first"),
            assay_warning_rate=("QC_Warning", lambda s: (s != "Pass").mean()),
        )
        .reset_index()
        .sort_values("missing_rate", ascending=False)
    )
    return table


def protein_qc_table(npx_long: pd.DataFrame) -> pd.DataFrame:
    """Protein-level missingness and detectability summary."""
    table = (
        npx_long.groupby(["OlinkID", "UniProt", "Assay", "Panel"])
        .agg(
            missing_rate=("NPX", lambda s: s.isna().mean()),
            below_lod_rate=("BelowLOD", "mean"),
            mean_npx=("NPX", "mean"),
            sd_npx=("NPX", "std"),
            assay_warning_rate=("QC_Warning", lambda s: (s != "Pass").mean()),
        )
        .reset_index()
        .sort_values("missing_rate", ascending=False)
    )
    return table


def filter_npx(
    npx_long: pd.DataFrame,
    max_sample_missing: float = 0.35,
    max_protein_missing: float = 0.40,
    keep_sample_qc_warning: bool = True,
) -> pd.DataFrame:
    """Filter poor-quality samples/proteins before ML-ready pivoting."""
    sample_qc = sample_qc_table(npx_long)
    protein_qc = protein_qc_table(npx_long)

    keep_samples = sample_qc.loc[sample_qc["missing_rate"] <= max_sample_missing, "SampleID"]
    keep_proteins = protein_qc.loc[protein_qc["missing_rate"] <= max_protein_missing, "OlinkID"]

    filtered = npx_long[
        npx_long["SampleID"].isin(keep_samples) & npx_long["OlinkID"].isin(keep_proteins)
    ].copy()

    if not keep_sample_qc_warning:
        filtered = filtered[filtered["SampleQC"] == "Pass"].copy()

    return filtered


def long_to_wide(npx_long: pd.DataFrame, feature_col: str = "Assay") -> pd.DataFrame:
    """Pivot long-format NPX data into a sample x protein matrix."""
    if feature_col not in npx_long.columns:
        raise ValueError(f"feature_col {feature_col!r} is not in dataframe")
    wide = npx_long.pivot_table(index="SampleID", columns=feature_col, values="NPX", aggfunc="mean")
    wide.columns.name = None
    return wide.reset_index()
