"""Streamlit demo scaffold for the Proteomics Clinical Index Engine.

Run after installing streamlit:
    streamlit run app/streamlit_app.py
"""

from pathlib import Path
import sys

import pandas as pd

try:
    import streamlit as st
except Exception as exc:  # pragma: no cover
    raise RuntimeError("Install streamlit to run the demo: pip install streamlit") from exc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from proteomics_index.scoring import assign_risk_band, probability_to_index, decision_gate

st.set_page_config(page_title="Proteomics Clinical Index Engine", layout="wide")
st.title("Proteomics Clinical Index Engine")
st.caption("Portfolio demo: NPX → ML probability → clinical index → confidence-aware report")

prob = st.slider("Model probability", 0.0, 1.0, 0.72, 0.01)
confidence = st.selectbox("Confidence label", ["High", "Moderate", "Low"], index=1)
score = probability_to_index(prob)
band = assign_risk_band(score)

col1, col2, col3 = st.columns(3)
col1.metric("Index score", f"{score}/100")
col2.metric("Risk band", band)
col3.metric("Review gate", decision_gate(band, confidence))

if Path(ROOT / "reports" / "example_clinician_report.md").exists():
    st.markdown("## Example clinician report")
    st.markdown(Path(ROOT / "reports" / "example_clinician_report.md").read_text(encoding="utf-8"))
else:
    st.info("Run notebook 05 to generate the example clinician report.")
