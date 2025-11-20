#  Alzheimer's Disease Risk Prediction Platform

**Complete web application with machine learning model for early Alzheimer's detection**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Model](https://img.shields.io/badge/ROC--AUC-97.89%25-brightgreen.svg)]()

---

##  Project Overview

This project provides a **production-ready web application** for predicting Alzheimer's disease risk using machine learning. It includes:

-  **Interactive Web Interface** - User-friendly form for patient data entry
-  **REST API** - FastAPI backend for programmatic access
-  **ML Model** - Gradient Boosting classifier (97.89% ROC-AUC)
-  **Validation Framework** - Leakage prevention and nested cross-validation
-  **Risk Visualization** - Color-coded risk levels and recommendations

---

##  Quick Start (3 Steps)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Generate Models (First Time Only)
```powershell
python scripts/regenerate_models.py
```

### 3. Start the Application
```powershell
python api/start_api.py --reload
```

### 4. Open in Browser
Navigate to: **http://localhost:8000**

 **That's it! The web application is now running.**

---

##  Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions for any computer
- **[QUICK_START.md](QUICK_START.md)** - Quick reference guide
- **[WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)** - How to use the web interface
- **[API Docs](http://localhost:8000/docs)** - Interactive API documentation (when server running)

---

##  For New Users / Different Computers

**First-time setup on a new machine:**

1. Make sure Python 3.9+ is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Generate models: `python scripts/regenerate_models.py`
4. Start server: `python api/start_api.py`
5. Open browser: http://localhost:8000

**Subsequent runs:**
- Just run: `python api/start_api.py` or double-click `start_web_app.bat`

 **See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions**

---

##  What You Get

### Web Application Features:
-  **32-field patient assessment form** organized by category
-  **Real-time input validation** with helpful tooltips
-  **4-level risk stratification** (Low, Moderate, High, Critical)
-  **Visual probability gauge** with color-coded risk display
-  **Clinical recommendations** tailored to risk level
-  **Printable reports** for patient records
-  **Mobile-responsive design** works on all devices

### API Features:
-  **RESTful endpoints** (`/predict`, `/health`, `/features`)
-  **Auto-generated documentation** at `/docs`
-  **Input validation** with Pydantic schemas
-  **Batch processing** support for multiple patients
-  **~10-20ms prediction latency**

---

##  Model Performance

| Metric | Value |
|--------|-------|
| **ROC-AUC** | 97.89% |
| **Accuracy** | 94.75% |
| **Recall** | 94.25% |
| **Precision** | 95.24% |
| **F1-Score** | 94.74% |
| **Dataset** | 2,149 patients, 35 features |

---

##  Project Structure

```
 web/                         #  Web Application
    index.html               # Main interface
    static/
        css/style.css        # Styling
        js/app.js            # Application logic

 api/                         #  REST API
    main.py                  # FastAPI application
    config.py                # Configuration
    models.py                # Pydantic schemas
    requirements.txt         # Dependencies
    test_api.py              # Test suite
    README.md                # API documentation

 models/                      #  ML Models
    tuned_gradient_boosting.pkl
    scaler.pkl
    feature_names.pkl

 notebooks/                   #  Jupyter Notebooks
    alzheimers_analysis.ipynb

 scripts/                     #  Utilities
    audit_validation.py      # Validation checks

 docs/                        #  Documentation
    README.md                # Detailed project docs
    requirements.txt
    presentations/

 reports/                     #  Outputs
    *.png                    # Visualizations
    *.json                   # Metrics

 WEB_APP_GUIDE.md            #  Web app documentation
 DEPLOYMENT_COMPLETE.md       #  API deployment guide
```

---

##  Web Application Guide

### Accessing the Application

1. **Start server**: `python api/start_api.py --reload`
2. **Open browser**: http://localhost:8000
3. **Fill patient data**: Complete all 32 fields
4. **Get prediction**: Click "Predict Risk"
5. **View results**: Risk level, probability, recommendations

### Patient Data Required (32 Fields)

**Demographics (4)**
- Age, Gender, Ethnicity, Education Level

**Lifestyle (6)**
- BMI, Smoking, Alcohol, Physical Activity, Diet Quality, Sleep Quality

**Medical History (6)**
- Family History, Cardiovascular Disease, Diabetes, Depression, Head Injury, Hypertension

**Vitals & Labs (6)**
- Systolic BP, Diastolic BP, Total Cholesterol, LDL, HDL, Triglycerides

**Cognitive Tests (3)**
- MMSE, Functional Assessment, ADL Score

**Symptoms (7)**
- Memory Complaints, Behavioral Problems, Confusion, Disorientation, Personality Changes, Task Difficulty, Forgetfulness

### Risk Interpretation

| Probability | Risk Level | Recommendation |
|------------|-----------|----------------|
| < 40% | **Low** 🟢 | Routine monitoring |
| 40-65% | **Moderate** 🟡 | Enhanced monitoring |
| 65-80% | **High** 🟠 | Specialist referral |
| > 80% | **Critical**  | Urgent evaluation |

 **Full guide**: See `WEB_APP_GUIDE.md`

---

##  API Usage

### Endpoints

```http
GET  /              # Web application homepage
GET  /health        # API health check
GET  /features      # Feature list & descriptions
POST /predict       # Risk prediction
GET  /docs          # Interactive API documentation
```

### Example: Make a Prediction

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "features": [
            75.0, 1, 2, 12.0, 28.5, 0, 3.0, 2.5, 6.0, 5.0,
            1, 0, 1, 0, 0, 1, 145.0, 88.0, 220.0, 140.0,
            50.0, 180.0, 22.0, 6.5, 1, 0, 7.0, 1, 0, 0, 1, 1
        ],
        "patient_id": "PATIENT-123"
    }
)

result = response.json()
print(f"Risk: {result['risk_level']} ({result['probability']:.2%})")
# Output: Risk: High (73.4%)
```

### Testing the API

```powershell
# Run automated test suite
python api/test_api.py

# Check health
curl http://localhost:8000/health

# Interactive docs
start http://localhost:8000/docs
```

 **Full guide**: See `api/README.md`

---

##  Validation & Quality

The project includes comprehensive validation:

-  **Leakage Audit** - Detects label proxies (MMSE, cognitive features)
-  **Dual-Model Strategy** - With/without cognitive assessments
-  **Nested Cross-Validation** - 5 outer × 3 inner folds
-  **Temporal/Site Validation** - Readiness for external validation

Run validation checks:
```powershell
python scripts/audit_validation.py
```

Results saved to `reports/`:
- `leakage_audit_report.json`
- `with_without_cognitive_metrics.json`
- `nested_cv_summary.json`

---

##  Deployment Options

### Local Development
```powershell
python api/start_api.py --reload
```

### Production (Multi-worker)
```powershell
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY models/ api/ web/ ./
RUN pip install -r api/requirements.txt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```powershell
docker build -t alzheimer-app .
docker run -p 8000:8000 alzheimer-app
```

### Cloud Platforms
- **Azure**: App Service, Container Instances
- **AWS**: Elastic Beanstalk, ECS, Lambda
- **GCP**: Cloud Run, App Engine

---

##  Documentation

| Document | Description |
|----------|-------------|
| `WEB_APP_GUIDE.md` | Complete web application guide |
| `DEPLOYMENT_COMPLETE.md` | API deployment documentation |
| `api/README.md` | API endpoints and usage |
| `api/QUICK_START.md` | API quick reference |
| `docs/README.md` | Detailed project documentation |
| `docs/LEAKAGE_AND_VALIDATION.md` | Validation methodology |

---

##  Configuration

### Environment Variables

Create `api/.env`:
```env
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info
CORS_ORIGINS=["*"]
```

### Model Paths

Models are automatically loaded from `models/`:
- `tuned_gradient_boosting.pkl` - Main classifier
- `scaler.pkl` - Feature scaling
- `feature_names.pkl` - Feature order

---

##  Troubleshooting

### "API Unavailable" in Web App

```powershell
# Check if server is running
netstat -ano | findstr :8000

# Start the server
python api/start_api.py --reload
```

### Import Errors

```powershell
# Install dependencies
pip install -r api/requirements.txt
```

### Model Not Found

```powershell
# Check models exist
ls models\

# Run notebook to generate models
jupyter notebook notebooks/alzheimers_analysis.ipynb
```

### Port Already in Use

```powershell
# Use different port
python api/start_api.py --port 8001

# Or kill process
taskkill /PID <PID> /F
```

---

##  Use Cases

### Clinical Settings
-  **Memory Clinics** - Screening tool for at-risk patients
- ‍ **Primary Care** - Early detection in routine check-ups
-  **Neurology** - Risk stratification for referrals

### Research
-  **Population Studies** - Large-scale risk assessment
-  **Clinical Trials** - Patient recruitment and stratification
-  **Epidemiology** - Risk factor analysis

### Healthcare Systems
-  **EHR Integration** - Automated risk calculation
-  **Mobile Apps** - Patient-facing risk tools
-  **Dashboards** - Population health monitoring

---

##  Contributing

This is an educational project (DEPI Graduation Project 2025). For improvements:

1. Test changes thoroughly
2. Update documentation
3. Follow existing code style
4. Ensure all tests pass

---

##  License & Disclaimer

**Educational & Research Use Only**

 **Medical Disclaimer**: This tool provides decision support only and is not intended as a substitute for professional medical advice, diagnosis, or treatment. All predictions must be reviewed by qualified healthcare professionals.

---

##  Authors

**DEPI Graduation Project Team** - 2025

---

##  Getting Started Summary

**For End Users (Clinicians):**
```powershell
pip install -r api/requirements.txt
python api/start_api.py --reload
# Open http://localhost:8000
```

**For Developers:**
```powershell
# API testing
python api/test_api.py

# Validation checks
python scripts/audit_validation.py

# Jupyter notebook
jupyter notebook notebooks/alzheimers_analysis.ipynb
```

**For Deployment:**
```powershell
# Production server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

##  Support

-  **Documentation**: See guides in root and `api/` directories
-  **Health Check**: http://localhost:8000/health
-  **API Docs**: http://localhost:8000/docs
-  **Tests**: `python api/test_api.py`

---

** Complete system ready for deployment!**

**Start now**: `python api/start_api.py --reload`

**Access at**: http://localhost:8000
