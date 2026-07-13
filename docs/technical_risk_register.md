# Technical Risk Register for a Proteomics-Driven Fertility AI System

> **Public demo notice**  
> This document is an independent educational and technical-review artifact for a public GitHub repository. It does not disclose, reproduce, or claim to represent any confidential client, employer, partner, or proprietary implementation. The concerns are framed generically for proteomics-driven fertility prediction and clinical decision-support systems.

## Purpose

This register identifies the main technical, clinical-AI, data, regulatory, and operational risks that should be addressed before a proteomics-driven fertility prediction system is treated as clinically reliable or deployment-ready.

The assumed end-to-end system boundary is:

```text
Sample collection
    -> Laboratory assay
    -> Bioinformatics and normalization
    -> Feature engineering
    -> ML scoring
    -> Confidence and abstention logic
    -> RAG/LLM-assisted reporting
    -> Clinician review and decision
```

A failure at any stage can invalidate the final output, even when the predictive model appears accurate in development.

## Technical Risk Register

| # | Area | Core concern | What could go wrong |
|---:|---|---|---|
| 1 | Intended clinical claim | “Probability of conception” is not precisely defined | The system may be trained on positive pregnancy tests but presented as predicting clinical pregnancy or live birth. |
| 2 | Prediction denominator | Probability per what: menstrual cycle, IVF stimulation, egg retrieval, embryo transfer, or complete treatment episode? | The same patient can receive materially different probabilities depending on the denominator. |
| 3 | Target population | Natural conception, IVF, IUI, donor cycles, fresh transfer, and frozen transfer are fundamentally different populations | Combining them without explicit modelling can create a misleading average model. |
| 4 | Unit of analysis | Is one row a person, couple, sample, menstrual cycle, retrieval, transfer, or treatment episode? | Incorrect unit definitions can produce leakage, invalid confidence intervals, and misleading event counts. |
| 5 | Couple-level biology | Fertility depends on both partners | Female-only molecular data may be presented as a couple-level conception probability. |
| 6 | Meaning of the candidate signature set | The proposed feature set may represent measured proteins, derived signatures, pathway scores, or mixed biological features | The dimensionality, analytical validation, interpretability, versioning, and model-development burden change substantially. |
| 7 | Biological plausibility | Blood proteins may not directly represent ovarian, endometrial, sperm, embryo, or placental biology | The model may learn general health, age, obesity, or inflammation rather than fertility-specific biology. |
| 8 | Proteomics limitations | Steroid hormones, vitamins, minerals, lipids, and many metabolites are not proteins | A “comprehensive” fertility assessment cannot be delivered through proteomics alone. |
| 9 | Sample matrix | Dried capillary whole blood differs from venous plasma or serum | A panel discovered in venous samples may not transfer reliably to dried blood. |
| 10 | Collection timing | Protein levels can change with cycle day, stimulation drugs, fasting, exercise, infection, and acute illness | Timing effects may be mistaken for fertility signals. |
| 11 | Dry-to-venous bridging | Correlation does not prove interchangeability | A protein may correlate strongly across matrices while still showing clinically unacceptable systematic bias. |
| 12 | Sample stability | Drying, temperature, humidity, transport time, and handling can alter proteins | Shipping variation may become a hidden model feature. |
| 13 | Laboratory reproducibility | Plate, reagent lot, operator, site, and instrument effects can influence measurements | The model may learn laboratory batches instead of biology. |
| 14 | Biobank integrity | Freeze-thaw history, storage duration, and storage conditions affect samples | Future testing may not be comparable with original testing. |
| 15 | Data provenance | It may be unclear how samples, labels, and clinical variables were generated | Untraceable data cannot support a credible regulated claim. |
| 16 | Consent and data rights | Research consent may not permit commercial algorithm development, future testing, or cross-border processing | Technically valuable data may be unusable for product development. |
| 17 | Retrospective-data bias | Historical clinic data are often incomplete and selectively collected | The training population may not represent future commercial users. |
| 18 | Outcome-label quality | Pregnancy and birth outcomes may be missing, delayed, or inconsistently defined | Label noise can materially limit achievable performance. |
| 19 | Outcome-event count | Successful outcomes, not only total records, constrain model complexity | Thousands of records may still contain too few live-birth events for reliable modelling. |
| 20 | Repeated cycles | Multiple cycles from one couple are correlated | Random row splitting can create severe information leakage. |
| 21 | Treatment confounding | Medication, stimulation protocol, clinic policy, and clinician decisions affect outcomes | The model may predict treatment selection rather than underlying fertility. |
| 22 | Embryo-related confounding | Implantation and live birth depend strongly on embryo quality and transfer-related variables | A blood model may receive credit for information actually explained by embryo factors. |
| 23 | Missing data | Clinical history, partner data, cycle timing, and laboratory results will often be incomplete | Imputation may create artificial patterns or unjustified confidence. |
| 24 | Feature-selection leakage | Selecting proteins before validation contaminates the evaluation | Reported accuracy may be materially overstated. |
| 25 | High dimensionality | Predictors may exceed the number of independent patients or positive outcomes | Flexible models can memorize the development cohort. |
| 26 | Baseline comparison | Proteomics may not improve on age, AMH, semen analysis, diagnosis, and treatment history | The product may be scientifically interesting but clinically unnecessary. |
| 27 | Model choice | Complex AI may be selected for branding rather than evidence | Deep learning may perform less reliably than regularized regression on small clinical datasets. |
| 28 | Calibration | A model can rank patients well while producing incorrect probabilities | A reported 40% probability may correspond to only 20% observed pregnancy. |
| 29 | External validation | Internal cross-validation is insufficient | Performance may collapse in a different clinic, laboratory, geography, or calendar period. |
| 30 | Distribution shift | Future patients may differ by age, ethnicity, diagnosis, clinic, assay lot, or treatment type | The system may confidently score unsupported cases. |
| 31 | Confidence logic | “Confidence” may be a qualitative label without a defined mathematical basis | Low-quality or out-of-distribution samples may still receive precise-looking predictions. |
| 32 | Subgroup safety | Average results can conceal poor performance in important subgroups | Older patients, minority populations, or specific infertility diagnoses may receive systematically misleading scores. |
| 33 | Longitudinal interpretation | Changes across cycles may reflect technical noise rather than biological improvement | The report may incorrectly attribute change to an intervention. |
| 34 | Causality and actionability | Predictive associations are not necessarily modifiable causes | SHAP values or feature importance may be translated into unsupported treatment advice. |
| 35 | LLM calculations | An LLM should not interpret raw NPX values or calculate clinical scores | The same patient could receive inconsistent outputs across repeated runs. |
| 36 | RAG quality | Retrieved evidence may be outdated, contradictory, poorly matched, or irrelevant | The report may cite evidence that does not support the patient-specific conclusion. |
| 37 | Hallucination and omission | The LLM may add unsupported advice or omit critical warnings | Clinician review alone may not reliably detect every error. |
| 38 | Report reproducibility | Models, prompts, retrieval sources, and report templates may change | A historical report may become impossible to reproduce. |
| 39 | Human factors | Clinicians may over-trust red-amber-green outputs or precise probabilities | A decision-support report may function as an implicit diagnosis. |
| 40 | Privacy architecture | Removing direct identifiers does not fully anonymize molecular and clinical data | Patients may remain re-identifiable through linked attributes. |
| 41 | Cybersecurity | Clinic, laboratory, cloud, model, and LLM interfaces expand the attack surface | Samples, identities, results, or reports may be mismatched, altered, or exposed. |
| 42 | MLOps and change control | Updating proteins, preprocessing, calibration, thresholds, prompts, or knowledge sources changes the system | Uncontrolled updates can invalidate previous validation. |
| 43 | Clinical utility | Better prediction does not automatically improve patient outcomes | The system may add cost without improving decisions, treatment efficiency, or live-birth outcomes. |
| 44 | Regulatory product boundary | It may be unclear which organization is responsible for the assay, scoring software, report generator, and final clinical output | Accountability for validation, release, vigilance, and post-market safety may be fragmented. |
| 45 | Quality-management maturity | Development may be occurring outside a controlled quality-management system | Evidence required for regulatory review may need to be recreated. |
| 46 | Operational scalability | Small-volume collection, repeated sampling, advanced assays, and clinician reporting may not scale reliably | High failure rates, long turnaround times, or poor margins can make the product clinically unusable. |

## Recommended Review Order

The risks should not be addressed only after model development. A practical review sequence is:

1. **Define the intended clinical claim and denominator.**
2. **Define the target population and unit of analysis.**
3. **Clarify whether candidate inputs are measured proteins, derived signatures, pathway scores, or mixed features.**
4. **Complete the dataset and outcome-event inventory.**
5. **Establish analytical validity for the intended sample matrix and workflow.**
6. **Build and evaluate a clinical-only baseline.**
7. **Develop leakage-controlled proteomics and combined models.**
8. **Validate calibration, confidence, abstention, and subgroup performance.**
9. **Constrain the LLM to structured, traceable, approved interpretation.**
10. **Implement quality management, change control, external validation, and post-deployment monitoring.**

## Suggested Repository Use

This document can support:

- architecture reviews;
- model-readiness assessments;
- data and validation planning;
- clinical-AI safety reviews;
- MLOps and change-control design;
- regulatory and quality-management discussions;
- risk-register expansion into formal FMEA or ISO 14971-aligned workflows.

It should be treated as an expert technical checklist, not as evidence that any particular clinical product has failed or passed validation.
