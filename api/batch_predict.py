"""
Batch prediction script for processing multiple patients through the API.

Usage:
    python api/batch_predict.py --input patients.csv --output predictions.csv

CSV format:
- Each row is a patient
- First 32 columns are features (in correct order)
- Optional 33rd column: patient_id
"""

import argparse
import pandas as pd
import requests
import json
from pathlib import Path
import sys
from typing import List, Dict
import time


API_URL = "http://localhost:8000"


def load_patients(input_file: Path) -> pd.DataFrame:
    """Load patient data from CSV."""
    try:
        df = pd.read_csv(input_file)
        print(f" Loaded {len(df)} patients from {input_file}")
        return df
    except Exception as e:
        print(f" Error loading file: {e}")
        sys.exit(1)


def check_api_health() -> bool:
    """Check if API is available."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f" API is healthy (model: {data.get('model_version', 'unknown')})")
            return True
        else:
            print(f" API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f" Cannot connect to API at {API_URL}")
        print("   Make sure the API is running: uvicorn api.main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f" Health check failed: {e}")
        return False


def get_feature_names() -> List[str]:
    """Get feature names from API."""
    try:
        response = requests.get(f"{API_URL}/features")
        if response.status_code == 200:
            data = response.json()
            return data["features"]
        else:
            print(f" Could not fetch feature names, using column order")
            return None
    except Exception as e:
        print(f" Error fetching features: {e}")
        return None


def predict_batch(df: pd.DataFrame, patient_id_col: str = None) -> List[Dict]:
    """Make predictions for all patients."""
    results = []
    feature_count = 32
    
    # Determine feature columns
    if patient_id_col and patient_id_col in df.columns:
        feature_cols = [col for col in df.columns if col != patient_id_col][:feature_count]
    else:
        feature_cols = df.columns[:feature_count]
    
    print(f"\n Processing {len(df)} patients...")
    print(f"   Using columns: {', '.join(feature_cols[:3])}... ({len(feature_cols)} features)")
    
    success_count = 0
    error_count = 0
    
    start_time = time.time()
    
    for idx, row in df.iterrows():
        try:
            # Extract features
            features = row[feature_cols].tolist()
            
            # Validate feature count
            if len(features) != feature_count:
                print(f"  Row {idx}: Expected {feature_count} features, got {len(features)}")
                results.append({
                    "row_index": idx,
                    "patient_id": row.get(patient_id_col, f"ROW-{idx}") if patient_id_col else f"ROW-{idx}",
                    "error": f"Invalid feature count: {len(features)}",
                    "prediction": None,
                    "probability": None,
                    "risk_level": None
                })
                error_count += 1
                continue
            
            # Prepare request
            request_data = {"features": features}
            if patient_id_col and patient_id_col in row:
                request_data["patient_id"] = str(row[patient_id_col])
            
            # Make prediction
            response = requests.post(
                f"{API_URL}/predict",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "row_index": idx,
                    "patient_id": result.get("patient_id", f"ROW-{idx}"),
                    "prediction": result["prediction"],
                    "probability": result["probability"],
                    "risk_level": result["risk_level"],
                    "confidence": result["confidence"],
                    "model_version": result["model_version"],
                    "error": None
                })
                success_count += 1
                
                # Progress indicator
                if (idx + 1) % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = (idx + 1) / elapsed
                    print(f"   Progress: {idx + 1}/{len(df)} ({rate:.1f} predictions/sec)")
            else:
                error_detail = response.json().get("detail", "Unknown error")
                print(f" Row {idx}: API error - {error_detail}")
                results.append({
                    "row_index": idx,
                    "patient_id": row.get(patient_id_col, f"ROW-{idx}") if patient_id_col else f"ROW-{idx}",
                    "error": error_detail,
                    "prediction": None,
                    "probability": None,
                    "risk_level": None
                })
                error_count += 1
                
        except Exception as e:
            print(f" Row {idx}: {str(e)}")
            results.append({
                "row_index": idx,
                "patient_id": row.get(patient_id_col, f"ROW-{idx}") if patient_id_col else f"ROW-{idx}",
                "error": str(e),
                "prediction": None,
                "probability": None,
                "risk_level": None
            })
            error_count += 1
    
    elapsed = time.time() - start_time
    print(f"\n Batch processing complete!")
    print(f"   Total time: {elapsed:.2f} seconds")
    print(f"   Success: {success_count}/{len(df)}")
    print(f"   Errors: {error_count}/{len(df)}")
    print(f"   Average: {len(df)/elapsed:.1f} predictions/sec")
    
    return results


def save_results(results: List[Dict], output_file: Path):
    """Save results to CSV."""
    try:
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        print(f"\n Results saved to {output_file}")
        
        # Summary statistics
        if "risk_level" in df.columns:
            print("\n Risk Level Distribution:")
            risk_counts = df["risk_level"].value_counts()
            for level, count in risk_counts.items():
                if pd.notna(level):
                    percentage = (count / len(df)) * 100
                    print(f"   {level}: {count} ({percentage:.1f}%)")
        
        if "error" in df.columns:
            error_count = df["error"].notna().sum()
            if error_count > 0:
                print(f"\n  {error_count} predictions had errors (see 'error' column)")
                
    except Exception as e:
        print(f" Error saving results: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Batch prediction for Alzheimer's risk using API"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Input CSV file with patient data"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Output CSV file for predictions"
    )
    parser.add_argument(
        "--patient-id-col",
        "-p",
        type=str,
        default=None,
        help="Column name for patient IDs (optional)"
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Update global API URL
    global API_URL
    API_URL = args.api_url
    
    print("="*60)
    print("ALZHEIMER'S RISK PREDICTION - BATCH PROCESSOR")
    print("="*60)
    print(f"API: {API_URL}")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    if args.patient_id_col:
        print(f"Patient ID column: {args.patient_id_col}")
    print("="*60)
    
    # Check input file exists
    if not args.input.exists():
        print(f" Input file not found: {args.input}")
        sys.exit(1)
    
    # Check API health
    if not check_api_health():
        sys.exit(1)
    
    # Get feature names (optional, for validation)
    feature_names = get_feature_names()
    
    # Load patients
    df = load_patients(args.input)
    
    # Validate minimum columns
    min_cols = 33 if args.patient_id_col else 32
    if len(df.columns) < 32:
        print(f" Input file must have at least 32 feature columns (found {len(df.columns)})")
        sys.exit(1)
    
    # Make predictions
    results = predict_batch(df, patient_id_col=args.patient_id_col)
    
    # Save results
    save_results(results, args.output)
    
    print("\n" + "="*60)
    print(" Batch processing complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
