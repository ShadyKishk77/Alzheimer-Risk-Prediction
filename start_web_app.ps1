# Quick start script for Alzheimer's Risk Prediction Web Application
# PowerShell Script

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  ALZHEIMER'S RISK PREDICTION - WEB APPLICATION" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found! Please install Python 3.10 or higher." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
try {
    python -c "import fastapi" 2>&1 | Out-Null
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "[WARNING] Dependencies not installed" -ForegroundColor Yellow
    Write-Host "[INFO] Installing required packages..." -ForegroundColor Cyan
    Write-Host ""
    
    pip install -r api\requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Dependencies installed successfully" -ForegroundColor Green
}

# Check if models exist
if (-not (Test-Path "models\tuned_gradient_boosting.pkl")) {
    Write-Host ""
    Write-Host "[ERROR] Model files not found in models\ directory" -ForegroundColor Red
    Write-Host "[INFO] Please run the Jupyter notebook to generate models:" -ForegroundColor Yellow
    Write-Host "       jupyter notebook notebooks\alzheimers_analysis.ipynb" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Model files found" -ForegroundColor Green

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  STARTING WEB APPLICATION" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[INFO] Server will start at: " -NoNewline -ForegroundColor Cyan
Write-Host "http://localhost:8000" -ForegroundColor Yellow
Write-Host "[INFO] Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Wait a moment for user to read
Start-Sleep -Milliseconds 500

# Start the application
try {
    python api\start_api.py --reload
} catch {
    Write-Host ""
    Write-Host "[ERROR] Failed to start application" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
