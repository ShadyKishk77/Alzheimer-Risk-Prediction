"""
Pydantic models for request/response validation.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class PatientInput(BaseModel):
    """Input schema for patient feature data."""
    
    features: List[float] = Field(
        ...,
        min_length=32,
        max_length=32,
        description="List of 32 patient features in the correct order as specified by feature_names.pkl"
    )
    
    patient_id: Optional[str] = Field(
        None,
        description="Optional patient identifier for tracking (not used in prediction)"
    )
    
    @field_validator('features')
    @classmethod
    def validate_features(cls, v):
        """Ensure all features are valid numbers."""
        if any(not isinstance(x, (int, float)) for x in v):
            raise ValueError("All features must be numeric")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [
                    70.5, 1.0, 0.0, 2.0, 28.3, 0.0, 1.0, 5.5, 7.2, 6.8,
                    1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 130.0, 82.0, 220.5,
                    24.0, 6.5, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0,
                    1.0, 0.0, 1.0, 0.0
                ],
                "patient_id": "PT-12345"
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for prediction results."""
    
    prediction: int = Field(
        ...,
        ge=0,
        le=1,
        description="Binary prediction: 0 = No Alzheimer's, 1 = Alzheimer's"
    )
    
    probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of Alzheimer's disease (0.0 to 1.0)"
    )
    
    risk_level: str = Field(
        ...,
        description="Categorical risk level: Low, Moderate, High, or Critical"
    )
    
    confidence: str = Field(
        ...,
        description="Confidence indicator based on probability distance from threshold"
    )
    
    model_version: str = Field(
        ...,
        description="Version of the model used for prediction"
    )
    
    patient_id: Optional[str] = Field(
        None,
        description="Patient identifier if provided in request"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction": 1,
                "probability": 0.873,
                "risk_level": "High",
                "confidence": "High confidence",
                "model_version": "1.0.0",
                "patient_id": "PT-12345"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="API status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    model_version: str = Field(..., description="Current model version")
    api_version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    status_code: int = Field(..., description="HTTP status code")


class FeatureNamesResponse(BaseModel):
    """Feature names and metadata."""
    
    features: List[str] = Field(..., description="List of feature names in order")
    count: int = Field(..., description="Total number of features")
    description: Dict[str, str] = Field(..., description="Feature descriptions")
