#!/usr/bin/env bash
# Render build script for Alzheimer's Risk Prediction Platform

set -o errexit

echo "======================================"
echo "Building Alzheimer's Risk Prediction"
echo "======================================"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Generate models if not present (for first deploy)
echo "Checking model files..."
if [ ! -f "models/tuned_gradient_boosting.pkl" ]; then
    echo "Model files not found. Generating models..."
    python scripts/regenerate_models.py
else
    echo "Model files already exist. Skipping generation."
fi

echo "======================================"
echo "Build completed successfully!"
echo "======================================"
