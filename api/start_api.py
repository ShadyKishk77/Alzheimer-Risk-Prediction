"""
Quick start script for the Alzheimer's Risk Prediction API.

This script checks dependencies and starts the FastAPI server.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    required = ["fastapi", "uvicorn", "pydantic", "joblib", "sklearn"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("ERROR: Missing required packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstall with: pip install -r api/requirements.txt")
        return False
    
    print("All dependencies installed")
    return True


def check_models():
    """Check if model files exist."""
    project_root = Path(__file__).resolve().parents[1]
    models_dir = project_root / "models"
    
    required_files = [
        "tuned_gradient_boosting.pkl",
        "scaler.pkl",
        "feature_names.pkl"
    ]
    
    missing = []
    for filename in required_files:
        if not (models_dir / filename).exists():
            missing.append(filename)
    
    if missing:
        print("ERROR: Missing model files in models/:")
        for file in missing:
            print(f"  - {file}")
        print("\nRun the notebook to generate models: notebooks/alzheimers_analysis.ipynb")
        return False
    
    print("All model files present")
    return True


def start_server(reload=False, port=8000):
    """Start the FastAPI server."""
    print("\n" + "="*60)
    print("STARTING ALZHEIMER'S RISK PREDICTION API")
    print("="*60)
    
    cmd = [
        "uvicorn",
        "api.main:app",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]
    
    if reload:
        cmd.append("--reload")
        print(f"Development mode (auto-reload enabled)")
    
    print(f"Server starting on http://localhost:{port}")
    print(f"API docs: http://localhost:{port}/docs")
    print(f"Health check: http://localhost:{port}/health")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\nServer stopped successfully")
    except FileNotFoundError:
        print("\nERROR: 'uvicorn' not found. Install with: pip install uvicorn")
        sys.exit(1)


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("ALZHEIMER'S RISK PREDICTION API - STARTUP CHECK")
    print("="*60 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model files
    if not check_models():
        sys.exit(1)
    
    # All checks passed, start server
    # Use reload=True for development, False for production
    reload = "--reload" in sys.argv or "-r" in sys.argv
    
    # Get custom port if specified
    port = 8000
    if "--port" in sys.argv:
        try:
            port_idx = sys.argv.index("--port")
            port = int(sys.argv[port_idx + 1])
        except (IndexError, ValueError):
            print("  Invalid port specified, using default 8000")
    
    start_server(reload=reload, port=port)


if __name__ == "__main__":
    main()
