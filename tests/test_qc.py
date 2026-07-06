from proteomics_index.synthetic_data import SyntheticOlinkConfig, generate_synthetic_olink_npx
from proteomics_index.qc import summarize_npx, filter_npx, long_to_wide


def test_synthetic_qc_and_pivot():
    npx, meta = generate_synthetic_olink_npx(SyntheticOlinkConfig(n_samples=12, n_proteins=20))
    summary = summarize_npx(npx)
    assert summary.loc["samples", "value"] == 12
    assert summary.loc["proteins", "value"] == 20

    filtered = filter_npx(npx)
    wide = long_to_wide(filtered)
    assert "SampleID" in wide.columns
    assert wide.shape[0] <= 12
