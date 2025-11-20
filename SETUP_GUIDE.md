#  Alzheimer's Risk Prediction - Setup Guide

This guide will help you set up and run the Alzheimer's Risk Prediction web application on **any computer**.

---

##  Prerequisites

Before you start, make sure you have:

1. **Python 3.9 or higher** installed
   - Check: `python --version`
   - Download from: https://www.python.org/downloads/

2. **Git** (optional, for cloning the repository)
   - Download from: https://git-scm.com/downloads

---

##  First-Time Setup

### Step 1: Get the Project

**Option A: Clone from GitHub**
```bash
git clone https://github.com/shadykishk7/Alzheimer.git
cd Alzheimer
```

**Option B: Extract from ZIP/RAR**
- Extract the project folder
- Open terminal/PowerShell in the project folder

### Step 2: Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

>  **Note**: If you get an error about execution policy on Windows:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages:
- FastAPI (web framework)
- scikit-learn (machine learning)
- pandas, numpy (data processing)
- uvicorn (server)
- And more...

### Step 4: Generate Model Files (First Time Only)

**If model files don't exist or are incompatible:**
```bash
python scripts/regenerate_models.py
```

This will:
-  Train the machine learning models
-  Save them in the `models/` folder
-  Takes about 30 seconds
-  Shows accuracy scores

---

##  Running the Application

### Quick Start (Easiest Method)

**Windows:**
```powershell
.\start_web_app.ps1
```

or double-click `start_web_app.bat`

**Linux/Mac:**
```bash
chmod +x start_web_app.sh
./start_web_app.sh
```

### Manual Start

```bash
python api/start_api.py --reload
```

---

##  Accessing the Application

Once the server starts, you'll see:

```
 All dependencies installed
 All model files present

 Server starting on http://localhost:8000
 API docs: http://localhost:8000/docs
```

**Open your browser and go to:**
- **Web App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

##  Stopping the Server

Press `Ctrl+C` in the terminal

---

##  Troubleshooting

### Problem: "Module not found" errors

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: "Model loading failed" or pickle errors

**Solution:** Regenerate models with your Python environment
```bash
python scripts/regenerate_models.py
```

### Problem: Port 8000 already in use

**Solution 1:** Stop the other application using port 8000

**Solution 2:** Change the port in `api/config.py`:
```python
PORT: int = 8001  # Change from 8000 to 8001
```

### Problem: "Cannot load model" errors

**Solution:** Check that these files exist:
- `models/tuned_gradient_boosting.pkl`
- `models/scaler.pkl`
- `models/feature_names.pkl`

If missing, run: `python scripts/regenerate_models.py`

### Problem: Browser shows "API Not Connected" (red banner)

**Solution:**
1. Make sure the server is running (check terminal)
2. Refresh the browser page
3. Check http://localhost:8000/health shows "healthy"

---

##  Project Structure

```
Alzheimer/
 api/                    # Backend API
    main.py            # FastAPI application
    config.py          # Configuration
    start_api.py       # Server startup script
 data/                   # Dataset files
 models/                 # Trained ML models (generated)
 scripts/                # Utility scripts
    regenerate_models.py
 web/                    # Frontend web application
    index.html
    static/
        css/
        js/
 requirements.txt        # Python dependencies
 start_web_app.bat      # Windows launcher
 start_web_app.ps1      # PowerShell launcher
```

---

##  Updating the Application

If you pull new changes from Git:

```bash
git pull origin main
pip install -r requirements.txt
python scripts/regenerate_models.py  # If models changed
python api/start_api.py --reload
```

---

##  Sharing with Others

To share this application:

1. **Share the Repository**
   - Push to GitHub
   - Share the repository URL
   - Others clone and follow this setup guide

2. **Share as ZIP**
   - Compress the entire `Alzheimer` folder
   - Exclude `venv/` folder (virtual environment)
   - Exclude `__pycache__/` folders
   - Share the ZIP file
   - Recipient follows "First-Time Setup" steps

3. **Important Files to Include:**
   -  All Python code (`api/`, `scripts/`, etc.)
   -  Web files (`web/`)
   -  Data files (`data/`)
   -  `requirements.txt`
   -  Documentation (README.md, this file)
   -  NOT needed: `venv/`, `models/` (will be regenerated), `__pycache__/`

---

##  System Requirements

- **Operating System**: Windows, Linux, or macOS
- **Python**: 3.9 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB
- **Browser**: Chrome, Firefox, Edge, or Safari (latest version)

---

##  Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Check the terminal output for error messages
3. Verify all prerequisites are installed
4. Try regenerating models: `python scripts/regenerate_models.py`
5. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

##  Model Information

- **Primary Model**: Gradient Boosting Classifier
- **Accuracy**: ~94%
- **Features**: 32 patient attributes
- **Training Data**: 2,149 patient records

The models are automatically trained when you run `regenerate_models.py`.

---

##  Security Notes

 **Important**: This is a development/demo application. For production use:

- Change SECRET_KEY in `api/config.py`
- Enable HTTPS
- Add authentication
- Use a production database
- Follow medical data compliance (HIPAA, etc.)

---

##  Quick Checklist

- [ ] Python 3.9+ installed
- [ ] Project downloaded/cloned
- [ ] Virtual environment created (optional but recommended)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Models generated (`python scripts/regenerate_models.py`)
- [ ] Server started (`python api/start_api.py`)
- [ ] Browser opened to http://localhost:8000
- [ ] Green "API Connected" banner visible

---

** That's it! You're ready to use the Alzheimer's Risk Prediction application!**
