#!/bin/bash

# Alzheimer's Risk Prediction - Linux/Mac Launcher
# This script starts the web application

echo "============================================================"
echo "ALZHEIMER'S RISK PREDICTION - WEB APPLICATION"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.9 or higher"
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Dependencies not installed"
    echo "   Installing requirements..."
    pip3 install -r requirements.txt
    echo ""
fi

# Check if models exist
if [ ! -f "models/tuned_gradient_boosting.pkl" ]; then
    echo "⚠️  Model files not found"
    echo "   Generating models (this may take a minute)..."
    python3 scripts/regenerate_models.py
    echo ""
fi

# Start the server
echo "============================================================"
echo "🚀 Starting web application..."
echo "============================================================"
echo ""
echo "🌐 Web App: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "❤️  Health: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python3 api/start_api.py --reload
