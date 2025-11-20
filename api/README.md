# Alzheimer's Risk Prediction API

Production-ready REST API for real-time Alzheimer's disease risk prediction.

## Features

-  **FastAPI** framework - High performance, automatic OpenAPI docs
-  **Input validation** - Pydantic schemas enforce data integrity
-  **Risk stratification** - 4-level categorization (Low, Moderate, High, Critical)
-  **Health checks** - Monitor API and model status
-  **CORS enabled** - Ready for web/mobile integration
-  **Automatic docs** - Interactive API documentation at `/docs`

---

## Quick Start

### 1. Install Dependencies

```bash
cd api
pip install -r requirements.txt
```

Or from project root:
```bash
pip install -r api/requirements.txt
```

### 2. Start the API Server

**Development mode (auto-reload):**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Verify API is Running

Open your browser: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

###  GET `/` - Root
API information and navigation

**Response:**
```json
{
  "message": "Alzheimer's Disease Risk Prediction API",
  "version": "1.0.0",
  "model": "Gradient Boosting Classifier",
  "model_version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

###  GET `/health` - Health Check
Monitor API and model status

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0",
  "api_version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - All systems operational
- `503 Service Unavailable` - Model loading failed

---

###  GET `/features` - Feature Metadata
List required features and their descriptions

**Response:**
```json
{
  "features": ["Age", "Gender", "Ethnicity", "..."],
  "count": 32,
  "description": {
    "Age": "Patient age (60-90 years)",
    "Gender": "0=Female, 1=Male",
    "MMSE": "Mini-Mental State Examination score (0-30)",
    "..."
  }
}
```

---

###  POST `/predict` - Make Prediction
Predict Alzheimer's risk from patient features

**Request Body:**
```json
{
  "features": [
    75.0,  // Age
    1,     // Gender (0=Female, 1=Male)
    2,     // Ethnicity
    12.0,  // EducationLevel
    28.5,  // BMI
    0,     // Smoking
    3.0,   // AlcoholConsumption
    2.5,   // PhysicalActivity
    6.0,   // DietQuality
    5.0,   // SleepQuality
    1,     // FamilyHistoryAlzheimers
    0,     // CardiovascularDisease
    1,     // Diabetes
    0,     // Depression
    0,     // HeadInjury
    1,     // Hypertension
    145.0, // SystolicBP
    88.0,  // DiastolicBP
    220.0, // CholesterolTotal
    140.0, // CholesterolLDL
    50.0,  // CholesterolHDL
    180.0, // CholesterolTriglycerides
    22.0,  // MMSE
    6.5,   // FunctionalAssessment
    1,     // MemoryComplaints
    0,     // BehavioralProblems
    7.0,   // ADL
    1,     // Confusion
    0,     // Disorientation
    0,     // PersonalityChanges
    1,     // DifficultyCompletingTasks
    1      // Forgetfulness
  ],
  "patient_id": "PATIENT-12345"  // Optional
}
```

**Response:**
```json
{
  "prediction": 1,
  "probability": 0.8234,
  "risk_level": "Critical",
  "confidence": "High confidence",
  "model_version": "1.0.0",
  "patient_id": "PATIENT-12345"
}
```

**Risk Levels:**
| Probability | Risk Level | Interpretation |
|------------|-----------|----------------|
| < 0.40 | **Low** | Routine monitoring sufficient |
| 0.40 - 0.65 | **Moderate** | Enhanced monitoring recommended |
| 0.65 - 0.80 | **High** | Specialist referral advised |
| > 0.80 | **Critical** | Urgent specialist evaluation |

**Status Codes:**
- `200 OK` - Successful prediction
- `400 Bad Request` - Invalid input (wrong feature count/types)
- `503 Service Unavailable` - Model not loaded

---

## Testing Examples

### Using `curl`

**Health Check:**
```bash
curl -X GET http://localhost:8000/health
```

**Get Features:**
```bash
curl -X GET http://localhost:8000/features
```

**Make Prediction:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [75.0, 1, 2, 12.0, 28.5, 0, 3.0, 2.5, 6.0, 5.0, 1, 0, 1, 0, 0, 1, 145.0, 88.0, 220.0, 140.0, 50.0, 180.0, 22.0, 6.5, 1, 0, 7.0, 1, 0, 0, 1, 1],
    "patient_id": "TEST-001"
  }'
```

### Using Python `requests`

```python
import requests

API_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{API_URL}/health")
print(response.json())

# Make prediction
patient_data = {
    "features": [
        75.0, 1, 2, 12.0, 28.5, 0, 3.0, 2.5, 6.0, 5.0,
        1, 0, 1, 0, 0, 1, 145.0, 88.0, 220.0, 140.0,
        50.0, 180.0, 22.0, 6.5, 1, 0, 7.0, 1, 0, 0, 1, 1
    ],
    "patient_id": "PATIENT-123"
}

response = requests.post(f"{API_URL}/predict", json=patient_data)
result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Probability: {result['probability']:.2%}")
print(f"Risk Level: {result['risk_level']}")
print(f"Confidence: {result['confidence']}")
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `api/` directory:

```env
# API Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=false
LOG_LEVEL=info

# Security
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

# Model Paths (optional, defaults provided)
MODEL_PATH=/path/to/custom/model.pkl
SCALER_PATH=/path/to/custom/scaler.pkl
```

### Customizing Settings

Edit `api/config.py` to modify default settings:
- Model paths
- CORS origins
- Request size limits
- Logging levels

---

## Production Deployment

### Option 1: Uvicorn (Recommended)

```bash
# Multi-worker setup for better performance
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

### Option 2: Gunicorn + Uvicorn Workers

```bash
gunicorn api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info
```

### Option 3: Docker

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy model artifacts
COPY models/ /app/models/

# Copy API code
COPY api/ /app/api/

# Install dependencies
RUN pip install --no-cache-dir -r api/requirements.txt

# Expose port
EXPOSE 8000

# Run API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Build and run:**
```bash
docker build -t alzheimer-api .
docker run -p 8000:8000 alzheimer-api
```

---

## Security Considerations

### For Production:

1. **Restrict CORS origins** - Update `CORS_ORIGINS` in `config.py`:
   ```python
   CORS_ORIGINS: List[str] = [
       "https://yourdomain.com",
       "https://app.yourdomain.com"
   ]
   ```

2. **Add authentication** - Implement API key or OAuth2:
   ```python
   from fastapi.security import APIKeyHeader
   api_key_header = APIKeyHeader(name="X-API-Key")
   ```

3. **Enable HTTPS** - Use reverse proxy (Nginx/Apache) with SSL certificates

4. **Rate limiting** - Add rate limiting middleware:
   ```bash
   pip install slowapi
   ```

5. **Input sanitization** - Already handled by Pydantic validation

6. **Logging & monitoring** - Configure production logging and add monitoring tools (Prometheus, Grafana)

---

## API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### OpenAPI Schema
- **JSON**: http://localhost:8000/openapi.json

---

## Troubleshooting

### Model Not Loading
```
RuntimeError: Model loading failed: [Errno 2] No such file or directory
```

**Solution:** Ensure model files exist in `models/` directory:
```bash
ls models/
# Should show: tuned_gradient_boosting.pkl, scaler.pkl, feature_names.pkl
```

### Import Errors
```
Import "fastapi" could not be resolved
```

**Solution:** Install API dependencies:
```bash
pip install -r api/requirements.txt
```

### Port Already in Use
```
ERROR: [Errno 10048] error while attempting to bind on address
```

**Solution:** Change port or kill existing process:
```bash
# Use different port
uvicorn api.main:app --port 8001

# Or kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Prediction Latency** | ~10-20ms |
| **Throughput** | ~200 requests/sec (4 workers) |
| **Model Size** | 89.67 KB |
| **Memory Usage** | ~200-300 MB |

---

## Integration Examples

### Dashboard Integration (JavaScript)

```javascript
async function predictAlzheimerRisk(patientFeatures) {
  try {
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features: patientFeatures })
    });
    
    const result = await response.json();
    
    // Update UI
    document.getElementById('risk-level').textContent = result.risk_level;
    document.getElementById('probability').textContent = 
      `${(result.probability * 100).toFixed(1)}%`;
    
    return result;
  } catch (error) {
    console.error('Prediction failed:', error);
  }
}
```

### Mobile App Integration (React Native)

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://your-server.com:8000';

export const getPrediction = async (features, patientId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/predict`, {
      features,
      patient_id: patientId
    });
    return response.data;
  } catch (error) {
    throw new Error(`Prediction failed: ${error.response?.data?.detail}`);
  }
};
```

---

## License & Disclaimer

 **Medical Disclaimer:** This API is for research and decision support purposes only. It does not constitute medical advice. All predictions must be reviewed by qualified healthcare professionals before clinical use.

---

## Support

For issues or questions:
- Check `/docs` for interactive API testing
- Review logs for error details
- Ensure model files are present in `models/` directory
- Verify Python environment and dependencies

**Model Version:** 1.0.0  
**API Version:** 1.0.0  
**Last Updated:** 2024
