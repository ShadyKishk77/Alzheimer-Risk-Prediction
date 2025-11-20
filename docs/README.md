# Alzheimer's Disease Risk Prediction Platform

End-to-end healthcare analytics project that combines exploratory analysis, statistical testing, interactive dashboards, high-performing machine learning models, and rigorous leakage/validation safeguards to support early Alzheimer's detection.

---

##  Snapshot

| Item | Details |
| --- | --- |
| Dataset | 2,149 patients · 35 features (demographics, lifestyle, medical history, cognitive tests) |
| Best model | Tuned Gradient Boosting · **ROC-AUC 97.89% · Accuracy 94.75% · Recall 94.25% · Precision 95.24%** |
| Notebook | `notebooks/alzheimers_analysis.ipynb` (EDA → stats → ML → deployment) |
| Validation | Leakage audit, dual-model comparison, temporal/site readiness, nested CV (5× outer · 3× inner) |
| Deliverables | Reports/plots, saved models, inference artifacts, presentation scripts, validation plan |

---

##  Quick Links

- Notebook: `notebooks/alzheimers_analysis.ipynb`
- Saved models: `models/`
- Validation script: `scripts/audit_validation.py`
- Documentation & presentations: `docs/`
- Visual outputs & JSON reports: `reports/`

---

##  Quick Start

### 1. Set up the environment (PowerShell example)

```powershell
# (optional) create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r docs/requirements.txt
```

Or, with Conda:

```powershell
conda env create -f docs/environment.yml
conda activate alzheimers-prediction
```

### 2. Reproduce the analysis notebook

```powershell
jupyter notebook notebooks/alzheimers_analysis.ipynb
```
Run cells top-to-bottom to regenerate EDA, statistics, ML training, tuning, and export artifacts to `models/` and `reports/`.

### 3. Run automated leakage + validation checks

```powershell
python scripts/audit_validation.py
```

Outputs saved to `reports/`:
- `leakage_audit_report.json` – single-feature AUC & mutual information flags
- `with_without_cognitive_metrics.json` – pre-screen vs diagnostic model comparison
- `temporal_site_validation.json` – time/site split readiness summary
- `nested_cv_summary.json` – unbiased outer-fold AUC scores

### 4. Use a saved model for inference

```python
import joblib
import pandas as pd

model = joblib.load("models/tuned_gradient_boosting.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_names = joblib.load("models/feature_names.pkl")

patient = pd.DataFrame([patient_features], columns=feature_names)
prob = model.predict_proba(scaler.transform(patient))[0]
print({"prediction": int(prob[1] >= 0.5), "probabilities": prob.tolist()})
```

---

##  Repository Map

```
 data/                        # Raw & processed CSVs (keep out of VCS if sensitive)
 notebooks/
    alzheimers_analysis.ipynb# Main analysis notebook (79 cells)
    models/                  # Notebook-generated copies of models (historical)
 models/                      # Canonical production artifacts (use these!)
    tuned_gradient_boosting.pkl
    tuned_random_forest.pkl
    tuned_logistic_regression.pkl
    scaler.pkl
    feature_names.pkl
 api/                         # Production REST API (FastAPI)
    main.py                  # API application with endpoints
    config.py                # Configuration management
    models.py                # Pydantic request/response schemas
    requirements.txt         # API dependencies
    test_api.py              # Test suite with sample patients
    README.md                # API documentation & deployment guide
 scripts/
    audit_validation.py      # Leakage audit + nested CV runner
 reports/                     # Static plots + JSON metrics
    *.png                    # EDA & performance charts
    leakage_audit_report.json
    with_without_cognitive_metrics.json
    temporal_site_validation.json
    nested_cv_summary.json
 docs/
    README.md (this file)
    requirements.txt
    environment.yml
    SECTION_3_PRESENTATION_SCRIPT.md
    PRESENTATION_OUTLINE.md
    FOCUSED_PRESENTATION.md
    LEAKAGE_AND_VALIDATION.md
 .gitignore, .gitattributes
```

> **Note:** `notebooks/models/` keeps legacy copies so the Jupyter notebook can run offline. For deployment/inference, always consume artifacts from `models/` at the repo root to avoid divergence.

---

##  Data → Insight → Model Workflow

1. **Exploratory Data Analysis** – distribution plots, pairplots, demographic/lifestyle summaries, PCA visualizations.
2. **Statistical Testing** – Pearson/Spearman correlations, t-tests, chi-square, ANOVA with effect sizes and interactive Plotly dashboards.
3. **Machine Learning** – 32 engineered features, StandardScaler, stratified 80/20 split, four algorithms (LR, RF, GB, MLP), 5-fold CV, hyperparameter tuning, persistence to disk.
4. **Validation & Deployment Prep** – confusion matrices, ROC curves, feature importance, leakage checks, nested CV, model saving, inference demo cell.

---

##  Validation & Leakage Controls

| Check | What it does | Artifact |
| --- | --- | --- |
| Leakage audit | Single-feature ROC-AUC & mutual information to flag label proxies (e.g., MMSE) | `reports/leakage_audit_report.json` |
| Two-model strategy | Compare models with vs without cognitive assessments (pre-screen vs diagnostic) | `reports/with_without_cognitive_metrics.json` |
| Temporal/site readiness | Detect date/site columns and outline chronological or leave-one-site-out splits | `reports/temporal_site_validation.json` |
| Nested cross-validation | 5× outer / 3× inner CV for LR & GB with per-fold AUC stats | `reports/nested_cv_summary.json` |

All checks run through `python scripts/audit_validation.py`.

---

##  Models & Inference Guidance

- Canonical artifacts stored in `models/`
- `models/feature_names.pkl` encodes the training feature order (use it to align new patient rows)
- `models/scaler.pkl` must be applied before scoring
- Decision threshold default is 0.5; adjust using probability outputs to meet clinical recall/precision targets
- Log each prediction with model version + timestamp when integrating into an API or dashboard

---

##  Key Metrics & Insights

- Tuned Gradient Boosting = **97.89% ROC-AUC**, only 21 errors on 400-patient test set
- Top features: MMSE (18.4%), FunctionalAssessment (12.6%), MemoryComplaints (9.9%) – aligns with clinical expectations
- Probability outputs enable risk-tiering (e.g., <0.4 low, 0.4–0.65 moderate, etc.)
- Feature importance confirms the model learns clinically meaningful patterns rather than spurious correlations

---

##  Production API Deployment

A production-ready FastAPI REST API is available for real-time predictions:

```powershell
# Install API dependencies
pip install -r api/requirements.txt

# Start the API server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Key Features:**
-  Real-time predictions with <20ms latency
-  Automatic input validation (Pydantic schemas)
-  Risk stratification (Low, Moderate, High, Critical)
-  Interactive API docs at `/docs`
-  Health monitoring at `/health`
-  CORS-enabled for web/mobile integration

**Quick Test:**
```powershell
# Check API health
curl http://localhost:8000/health

# Run comprehensive test suite
python api/test_api.py
```

 **Full documentation:** See `api/README.md` for endpoints, examples, deployment options (Docker, multi-worker), and security configuration.

---

##  Future Enhancements

- External prospective validation across hospitals and demographic segments
- Probability calibration (isotonic/Platt) and threshold tuning per clinical policy
- SHAP/ICE explainability dashboards for clinicians
- Data drift monitoring + scheduled retraining
- Batch prediction API endpoint for population screening

---

##  Contact & License

- Project team: DEPI Graduation Project (2025)
- License: Educational & research use; please cite the authors when reusing materials
- Questions / collaborations: open an issue or reach out via the DEPI coordinators

---

**Reminder:** Keep `models/` as the single source of truth for deployment artifacts. Remove or regenerate `notebooks/models/` copies if you need to slim the repo or refresh the notebook outputs.
