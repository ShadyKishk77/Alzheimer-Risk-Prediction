"""
Configuration settings for the Alzheimer's Risk Prediction API.
"""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API configuration settings."""
    
    # API metadata
    API_TITLE: str = "Alzheimer's Disease Risk Prediction API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = """
    Production-ready REST API for predicting Alzheimer's disease risk using machine learning.
    
    ## Features
    - Real-time risk prediction from patient health metrics
    - Input validation and error handling
    - Probability scores with confidence intervals
    - Health monitoring endpoints
    - Versioned API interface
    
    ## Use Cases
    - Clinical decision support systems
    - Hospital EHR integration
    - Mobile health applications
    - Population screening dashboards
    """
    
    # Model paths
    BASE_DIR: Path = Path(__file__).resolve().parents[1]
    MODEL_DIR: Path = BASE_DIR / "models"
    MODEL_PATH: Path = MODEL_DIR / "tuned_gradient_boosting.pkl"
    SCALER_PATH: Path = MODEL_DIR / "scaler.pkl"
    FEATURES_PATH: Path = MODEL_DIR / "feature_names.pkl"
    
    # API configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    
    # Security
    CORS_ORIGINS: List[str] = ["*"]  # Restrict in production
    MAX_REQUEST_SIZE: int = 1024 * 1024  # 1MB
    
    # Model metadata
    MODEL_VERSION: str = "1.0.0"
    MODEL_NAME: str = "Tuned Gradient Boosting"
    EXPECTED_FEATURES: int = 32
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
