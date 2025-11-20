"""
FastAPI application for Alzheimer's Disease Risk Prediction.

This API provides real-time predictions using a trained Gradient Boosting model.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from api.config import settings
from api.models import (
    PatientInput,
    PredictionResponse,
    HealthResponse,
    ErrorResponse,
    FeatureNamesResponse
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global model storage
model_artifacts = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML model on startup, cleanup on shutdown."""
    logger.info("Loading ML model artifacts...")
    try:
        model_artifacts["model"] = joblib.load(settings.MODEL_PATH)
        model_artifacts["scaler"] = joblib.load(settings.SCALER_PATH)
        model_artifacts["feature_names"] = joblib.load(settings.FEATURES_PATH)
        logger.info(f"Model loaded successfully: {settings.MODEL_NAME} v{settings.MODEL_VERSION}")
        logger.info(f"Features loaded: {len(model_artifacts['feature_names'])} features")
    except Exception as e:
        logger.error(f"Failed to load model artifacts: {e}")
        raise RuntimeError(f"Model loading failed: {e}")
    
    yield
    
    # Cleanup
    model_artifacts.clear()
    logger.info("Model artifacts unloaded")


# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web application
WEB_DIR = settings.BASE_DIR / "web"
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")
    logger.info(f"Static files mounted from {WEB_DIR / 'static'}")


def calculate_risk_level(probability: float) -> str:
    """Categorize risk based on probability."""
    if probability < 0.40:
        return "Low"
    elif probability < 0.65:
        return "Moderate"
    elif probability < 0.80:
        return "High"
    else:
        return "Critical"


def calculate_confidence(probability: float, threshold: float = 0.5) -> str:
    """Assess prediction confidence based on distance from threshold."""
    distance = abs(probability - threshold)
    if distance >= 0.30:
        return "High confidence"
    elif distance >= 0.15:
        return "Moderate confidence"
    else:
        return "Low confidence (borderline case)"


@app.get("/", tags=["Info"], include_in_schema=False)
async def root():
    """Serve the web application homepage."""
    web_index = WEB_DIR / "index.html"
    if web_index.exists():
        return FileResponse(str(web_index))
    else:
        # Fallback to API info if web app not available
        return {
            "message": "Alzheimer's Disease Risk Prediction API",
            "version": settings.API_VERSION,
            "model": settings.MODEL_NAME,
            "model_version": settings.MODEL_VERSION,
            "docs": "/docs",
            "health": "/health",
            "web_app": "/index.html" if web_index.exists() else "Not available"
        }


@app.get("/api", tags=["Info"])
async def api_info():
    """API endpoint information (for programmatic access)."""
    return {
        "message": "Alzheimer's Disease Risk Prediction API",
        "version": settings.API_VERSION,
        "model": settings.MODEL_NAME,
        "model_version": settings.MODEL_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint"
)
async def health_check():
    """
    Check API and model health status.
    
    Returns information about:
    - API operational status
    - Model loading status
    - Version information
    """
    model_loaded = all(
        key in model_artifacts 
        for key in ["model", "scaler", "feature_names"]
    )
    
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        model_version=settings.MODEL_VERSION,
        api_version=settings.API_VERSION
    )


@app.get(
    "/features",
    response_model=FeatureNamesResponse,
    tags=["Info"],
    summary="Get feature names and metadata"
)
async def get_features():
    """
    Retrieve the list of features required for prediction.
    
    Returns:
    - Feature names in the correct order
    - Feature count
    - Brief descriptions
    """
    if "feature_names" not in model_artifacts:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    feature_names = model_artifacts["feature_names"]
    
    # Feature category descriptions
    descriptions = {
        "Age": "Patient age (60-90 years)",
        "Gender": "0=Female, 1=Male",
        "Ethnicity": "Categorical (0-3)",
        "EducationLevel": "Years of education",
        "BMI": "Body Mass Index",
        "Smoking": "0=No, 1=Yes",
        "AlcoholConsumption": "Weekly units",
        "PhysicalActivity": "Weekly hours",
        "DietQuality": "Score 0-10",
        "SleepQuality": "Score 0-10",
        "FamilyHistoryAlzheimers": "0=No, 1=Yes",
        "CardiovascularDisease": "0=No, 1=Yes",
        "Diabetes": "0=No, 1=Yes",
        "Depression": "0=No, 1=Yes",
        "HeadInjury": "0=No, 1=Yes",
        "Hypertension": "0=No, 1=Yes",
        "SystolicBP": "Systolic blood pressure (mmHg)",
        "DiastolicBP": "Diastolic blood pressure (mmHg)",
        "CholesterolTotal": "Total cholesterol (mg/dL)",
        "CholesterolLDL": "LDL cholesterol (mg/dL)",
        "CholesterolHDL": "HDL cholesterol (mg/dL)",
        "CholesterolTriglycerides": "Triglycerides (mg/dL)",
        "MMSE": "Mini-Mental State Examination score (0-30)",
        "FunctionalAssessment": "Functional ability score (0-10)",
        "MemoryComplaints": "0=No, 1=Yes",
        "BehavioralProblems": "0=No, 1=Yes",
        "ADL": "Activities of Daily Living score (0-10)",
        "Confusion": "0=No, 1=Yes",
        "Disorientation": "0=No, 1=Yes",
        "PersonalityChanges": "0=No, 1=Yes",
        "DifficultyCompletingTasks": "0=No, 1=Yes",
        "Forgetfulness": "0=No, 1=Yes"
    }
    
    return FeatureNamesResponse(
        features=feature_names,
        count=len(feature_names),
        description=descriptions
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
    summary="Predict Alzheimer's disease risk",
    responses={
        200: {"description": "Successful prediction"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        503: {"model": ErrorResponse, "description": "Model not available"}
    }
)
async def predict(patient: PatientInput):
    """
    Predict Alzheimer's disease risk from patient features.
    
    **Input:** 32 patient features in the correct order (see /features endpoint)
    
    **Output:**
    - Binary prediction (0 or 1)
    - Probability score (0.0 to 1.0)
    - Risk level (Low, Moderate, High, Critical)
    - Confidence assessment
    - Model version
    
    **Clinical Interpretation:**
    - Probability < 0.40: Low risk, routine monitoring
    - Probability 0.40-0.65: Moderate risk, enhanced monitoring recommended
    - Probability 0.65-0.80: High risk, specialist referral advised
    - Probability > 0.80: Critical risk, urgent specialist evaluation
    
    **Note:** This tool provides decision support only. Final diagnosis must be made by qualified healthcare professionals.
    """
    # Check model availability
    if not all(key in model_artifacts for key in ["model", "scaler", "feature_names"]):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Please check server logs."
        )
    
    try:
        # Validate feature count
        if len(patient.features) != settings.EXPECTED_FEATURES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected {settings.EXPECTED_FEATURES} features, got {len(patient.features)}"
            )
        
        # Prepare input
        features_array = np.array(patient.features).reshape(1, -1)
        
        # Scale features
        scaled_features = model_artifacts["scaler"].transform(features_array)
        
        # Make prediction
        prediction_proba = model_artifacts["model"].predict_proba(scaled_features)[0]
        probability = float(prediction_proba[1])  # Probability of class 1 (Alzheimer's)
        prediction = int(probability >= 0.5)
        
        # Calculate risk level and confidence
        risk_level = calculate_risk_level(probability)
        confidence = calculate_confidence(probability)
        
        logger.info(
            f"Prediction made - Patient: {patient.patient_id or 'N/A'}, "
            f"Probability: {probability:.3f}, Risk: {risk_level}"
        )
        
        return PredictionResponse(
            prediction=prediction,
            probability=round(probability, 4),
            risk_level=risk_level,
            confidence=confidence,
            model_version=settings.MODEL_VERSION,
            patient_id=patient.patient_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please contact support.",
            "status_code": 500
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL
    )
