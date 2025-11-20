"""
Test script for Alzheimer's Risk Prediction API.

Usage:
    python api/test_api.py

Make sure the API server is running:
    uvicorn api.main:app --reload --port 8000
"""

import requests
import json
from typing import Dict, List


API_BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint."""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Health check failed"
    data = response.json()
    assert data["status"] == "healthy", "API is not healthy"
    assert data["model_loaded"] is True, "Model not loaded"
    print(" Health check passed")


def test_get_features():
    """Test the features metadata endpoint."""
    print("\n" + "="*60)
    print("TEST 2: Get Features Metadata")
    print("="*60)
    
    response = requests.get(f"{API_BASE_URL}/features")
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"Feature Count: {data['count']}")
    print(f"First 5 Features: {data['features'][:5]}")
    print(f"Sample Descriptions:")
    for feature in list(data['description'].keys())[:3]:
        print(f"  - {feature}: {data['description'][feature]}")
    
    assert response.status_code == 200, "Get features failed"
    assert data["count"] == 32, f"Expected 32 features, got {data['count']}"
    print(" Features metadata retrieved successfully")


def test_prediction_low_risk():
    """Test prediction with low-risk patient profile."""
    print("\n" + "="*60)
    print("TEST 3: Low Risk Patient Prediction")
    print("="*60)
    
    # Low-risk profile: Young, healthy, no risk factors, good cognitive scores
    patient_data = {
        "features": [
            62.0,  # Age (younger)
            0,     # Gender (Female)
            1,     # Ethnicity
            16.0,  # EducationLevel (high)
            24.0,  # BMI (healthy)
            0,     # Smoking (no)
            1.0,   # AlcoholConsumption (low)
            5.0,   # PhysicalActivity (high)
            8.0,   # DietQuality (good)
            8.0,   # SleepQuality (good)
            0,     # FamilyHistoryAlzheimers (no)
            0,     # CardiovascularDisease (no)
            0,     # Diabetes (no)
            0,     # Depression (no)
            0,     # HeadInjury (no)
            0,     # Hypertension (no)
            120.0, # SystolicBP (normal)
            80.0,  # DiastolicBP (normal)
            180.0, # CholesterolTotal (normal)
            100.0, # CholesterolLDL (normal)
            60.0,  # CholesterolHDL (good)
            120.0, # CholesterolTriglycerides (normal)
            29.0,  # MMSE (excellent)
            9.5,   # FunctionalAssessment (excellent)
            0,     # MemoryComplaints (no)
            0,     # BehavioralProblems (no)
            9.5,   # ADL (excellent)
            0,     # Confusion (no)
            0,     # Disorientation (no)
            0,     # PersonalityChanges (no)
            0,     # DifficultyCompletingTasks (no)
            0      # Forgetfulness (no)
        ],
        "patient_id": "LOW-RISK-001"
    }
    
    response = requests.post(f"{API_BASE_URL}/predict", json=patient_data)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"\nPrediction Results:")
    print(f"  Patient ID: {data.get('patient_id', 'N/A')}")
    print(f"  Prediction: {data['prediction']} ({'Positive' if data['prediction'] == 1 else 'Negative'})")
    print(f"  Probability: {data['probability']:.4f} ({data['probability']*100:.2f}%)")
    print(f"  Risk Level: {data['risk_level']}")
    print(f"  Confidence: {data['confidence']}")
    print(f"  Model Version: {data['model_version']}")
    
    assert response.status_code == 200, "Prediction failed"
    print(f"\n Low-risk prediction completed (Expected: Low/Moderate risk)")


def test_prediction_high_risk():
    """Test prediction with high-risk patient profile."""
    print("\n" + "="*60)
    print("TEST 4: High Risk Patient Prediction")
    print("="*60)
    
    # High-risk profile: Older, multiple risk factors, poor cognitive scores
    patient_data = {
        "features": [
            85.0,  # Age (elderly)
            1,     # Gender (Male)
            2,     # Ethnicity
            8.0,   # EducationLevel (low)
            32.0,  # BMI (overweight)
            1,     # Smoking (yes)
            6.0,   # AlcoholConsumption (high)
            0.5,   # PhysicalActivity (sedentary)
            3.0,   # DietQuality (poor)
            3.0,   # SleepQuality (poor)
            1,     # FamilyHistoryAlzheimers (yes)
            1,     # CardiovascularDisease (yes)
            1,     # Diabetes (yes)
            1,     # Depression (yes)
            1,     # HeadInjury (yes)
            1,     # Hypertension (yes)
            160.0, # SystolicBP (high)
            95.0,  # DiastolicBP (high)
            260.0, # CholesterolTotal (high)
            170.0, # CholesterolLDL (high)
            35.0,  # CholesterolHDL (low)
            220.0, # CholesterolTriglycerides (high)
            18.0,  # MMSE (impaired)
            3.5,   # FunctionalAssessment (poor)
            1,     # MemoryComplaints (yes)
            1,     # BehavioralProblems (yes)
            3.5,   # ADL (poor)
            1,     # Confusion (yes)
            1,     # Disorientation (yes)
            1,     # PersonalityChanges (yes)
            1,     # DifficultyCompletingTasks (yes)
            1      # Forgetfulness (yes)
        ],
        "patient_id": "HIGH-RISK-001"
    }
    
    response = requests.post(f"{API_BASE_URL}/predict", json=patient_data)
    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    print(f"\nPrediction Results:")
    print(f"  Patient ID: {data.get('patient_id', 'N/A')}")
    print(f"  Prediction: {data['prediction']} ({'Positive' if data['prediction'] == 1 else 'Negative'})")
    print(f"  Probability: {data['probability']:.4f} ({data['probability']*100:.2f}%)")
    print(f"  Risk Level: {data['risk_level']}")
    print(f"  Confidence: {data['confidence']}")
    print(f"  Model Version: {data['model_version']}")
    
    assert response.status_code == 200, "Prediction failed"
    print(f"\n High-risk prediction completed (Expected: High/Critical risk)")


def test_invalid_input():
    """Test API error handling with invalid input."""
    print("\n" + "="*60)
    print("TEST 5: Invalid Input Handling")
    print("="*60)
    
    # Test with wrong number of features
    invalid_data = {
        "features": [75.0, 1, 2],  # Only 3 features instead of 32
        "patient_id": "INVALID-001"
    }
    
    response = requests.post(f"{API_BASE_URL}/predict", json=invalid_data)
    print(f"Status Code: {response.status_code}")
    print(f"Error Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 400, "Should return 400 for invalid input"
    print(" Invalid input properly rejected")


def test_root_endpoint():
    """Test the root endpoint."""
    print("\n" + "="*60)
    print("TEST 6: Root Endpoint")
    print("="*60)
    
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Root endpoint failed"
    print(" Root endpoint working")


def run_all_tests():
    """Run all API tests."""
    print("\n" + "="*60)
    print("ALZHEIMER'S RISK PREDICTION API TEST SUITE")
    print("="*60)
    print(f"Testing API at: {API_BASE_URL}")
    print("Make sure the API server is running!")
    print("Start with: uvicorn api.main:app --reload --port 8000")
    
    try:
        tests = [
            test_root_endpoint,
            test_health_check,
            test_get_features,
            test_prediction_low_risk,
            test_prediction_high_risk,
            test_invalid_input
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                passed += 1
            except Exception as e:
                print(f"\n Test failed: {str(e)}")
                failed += 1
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {passed + failed}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%")
        print("="*60 + "\n")
        
        if failed == 0:
            print(" All tests passed! API is working correctly.")
        else:
            print(" Some tests failed. Please check the errors above.")
            
    except requests.exceptions.ConnectionError:
        print("\n ERROR: Could not connect to API server")
        print("Make sure the API is running:")
        print("  uvicorn api.main:app --reload --port 8000")
        print("\nOr check if the port is correct in API_BASE_URL")


if __name__ == "__main__":
    run_all_tests()
