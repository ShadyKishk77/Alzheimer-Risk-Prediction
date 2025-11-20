@echo off
REM Quick start script for Alzheimer's Risk Prediction Web Application
REM Windows Batch Script

echo.
echo ================================================================
echo   ALZHEIMER'S RISK PREDICTION - WEB APPLICATION
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10 or higher.
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Dependencies not installed
    echo [INFO] Installing required packages...
    echo.
    pip install -r api\requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [OK] Dependencies installed

REM Check if models exist
if not exist "models\tuned_gradient_boosting.pkl" (
    echo.
    echo [ERROR] Model files not found in models\ directory
    echo [INFO] Please run the Jupyter notebook to generate models:
    echo        jupyter notebook notebooks\alzheimers_analysis.ipynb
    pause
    exit /b 1
)

echo [OK] Model files found

echo.
echo ================================================================
echo   STARTING WEB APPLICATION
echo ================================================================
echo.
echo [INFO] Server will start at: http://localhost:8000
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ================================================================
echo.

REM Start the application
python api\start_api.py --reload

pause
