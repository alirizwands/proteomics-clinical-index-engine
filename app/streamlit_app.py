"""Interactive public demonstration for the Proteomics Clinical Index Engine.

Run locally with:
    streamlit run app/streamlit_app.py

The application demonstrates the score-presentation and clinician-review layer.
The complete synthetic NPX-to-model workflow remains documented in the notebooks.
"""

from __future__ import annotations

from pathlib import Path
import json
import sys

try:
    import streamlit as st
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "Streamlit is required to run this demonstration. "
        "Install the project dependencies with: pip install -r requirements.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from proteomics_index.scoring import (  # noqa: E402
    assign_risk_band,
    decision_gate,
    probability_to_index,
)


st.set_page_config(
    page_title="Proteomics Clinical Index Engine",
    page_icon="🧬",
    layout="wide",
)

st.title("Proteomics Clinical Index Engine")
st.caption(
    "Interactive public reference implementation demonstrating how an "
    "upstream proteomics model output can be translated into a 0–100 index, "
    "illustrative risk band, confidence assessment, clinician-review decision "
    "and auditable output."
)

st.info(
    "This application uses synthetic/example inputs and illustrative thresholds. "
    "It is not a medical device, diagnostic system, clinical recommendation, "
    "or substitute for professional judgement."
)
with st.expander("How to use this demonstration", expanded=True):
    st.markdown(
        """
1. Adjust the **simulated model probability** in the sidebar.
2. Select an illustrative **confidence level**.
3. Observe how the index, risk band and clinician-review decision change.

This screen demonstrates the **interpretation, reporting and governance layer**.
It does not upload proteomic samples, train a model or generate a clinical diagnosis.
"""
    )


with st.sidebar:
    st.header("Demonstration inputs")

    probability = st.slider(
        "Simulated model probability",
        min_value=0.0,
        max_value=1.0,
        value=0.72,
        step=0.01,
        help=(
             "Represents the calibrated output of an upstream proteomics model. "
             "Raw NPX data are not processed directly on this screen. The repository "
             "notebooks demonstrate how this type of probability can be generated "
             "from synthetic Olink-style NPX data."
        ),
    )

    confidence = st.selectbox(
        "Confidence label",
        options=["High", "Moderate", "Low"],
        index=1,
        help=(
            "Illustrative confidence category combining signals such as prediction "
            "margin, entropy, missingness and bootstrap uncertainty."
        ),
    )

    with st.expander("Illustrative score thresholds"):
        green_threshold = st.number_input(
            "Green-to-amber threshold",
            min_value=1,
            max_value=98,
            value=35,
            step=1,
        )
        red_threshold = st.number_input(
            "Amber-to-red threshold",
            min_value=2,
            max_value=99,
            value=65,
            step=1,
        )

    st.caption(
        "Thresholds are configuration examples for demonstrating system behaviour; "
        "they are not validated clinical cut-offs."
    )

if green_threshold >= red_threshold:
    st.error(
        "The green-to-amber threshold must be lower than the amber-to-red threshold."
    )
    st.stop()

score = probability_to_index(probability)
band = assign_risk_band(
    score,
    green_threshold=int(green_threshold),
    red_threshold=int(red_threshold),
)
gate = decision_gate(band, confidence)

st.subheader("Interactive result")

metric_score, metric_band, metric_confidence = st.columns(3)
metric_score.metric("Clinical index", f"{score}/100")
metric_band.metric("Illustrative risk band", band)
metric_confidence.metric("Confidence", confidence)

st.progress(score, text=f"Index score: {score}/100")

st.markdown("### Clinician-review routing")
st.write(gate)

if confidence == "Low":
    st.warning(
        "Low-confidence outputs are escalated regardless of the risk band. "
        "The objective is to prevent uncertain model outputs from being treated "
        "as autonomous clinical decisions."
    )
elif band == "Red":
    st.warning(
        "The elevated illustrative index triggers clinician review. "
        "No diagnosis or treatment action is generated automatically."
    )
elif band == "Amber":
    st.info(
        "The intermediate illustrative index is routed for clinician review "
        "rather than interpreted as a standalone conclusion."
    )
else:
    st.success(
        "The lower illustrative index remains subject to routine clinician review "
        "and must be interpreted alongside the wider clinical context."
    )

with st.expander("How this screen connects to the complete pipeline"):
    st.code(
        "Olink-style NPX data\n"
        "  → quality control and ML-ready transformation\n"
        "  → leakage-safe high-dimensional modelling\n"
        "  → calibrated probability\n"
        "  → 0–100 index and illustrative risk band\n"
        "  → confidence logic and clinician-review gate\n"
        "  → report and audit record",
        language="text",
    )
st.markdown("### Static example outputs")

st.info(
    "The report and audit record below were generated from a separate "
    "synthetic demonstration sample. They do not update when the interactive "
    "controls above are changed."
)
report_path = ROOT / "reports" / "example_clinician_report.md"
audit_path = ROOT / "reports" / "example_audit_record.json"


report_tab, audit_tab = st.tabs(
    ["Clinician-facing report", "Technical audit record"]
)

with report_tab:
    st.markdown("### Static example clinician-facing report")
    if report_path.exists():
        report_text = report_path.read_text(encoding="utf-8")
        with st.expander("Open example report", expanded=True):
            st.markdown(report_text)

        st.download_button(
            "Download example report",
            data=report_text,
            file_name="example_clinician_report.md",
            mime="text/markdown",
        )
    else:
        st.info(
            "The example report has not been generated. "
            "Run notebook 05 to create it."
        )

with audit_tab:
    st.markdown("### Static example audit record")
    if audit_path.exists():
        try:
            audit_record = json.loads(
                audit_path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            st.error("The example audit record is not valid JSON.")
        else:
            st.json(audit_record)
    else:
        st.info(
            "The example audit record has not been generated. "
            "Run notebook 05 to create it."
        )



st.markdown("### Scope and limitations")
st.markdown(
    """
- The probability control represents a simulated upstream model output; the
  deployed screen does not directly process uploaded proteomics data.
- The interactive controls demonstrate the **score presentation, confidence and
  human-review layer**.
- The five notebooks demonstrate the wider synthetic
  **NPX → QC → modelling → calibration → reporting** workflow.
- The repository contains no real patient data, proprietary clinical panel,
  commercial algorithm or confidential client implementation.
- Outputs, thresholds and labels are illustrative and require formal analytical,
  clinical, usability and regulatory validation before any real-world use.
"""
)
