# 🧠 Neuro ML: Alzheimer's Risk Assessment

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Dash](https://img.shields.io/badge/Framework-Dash-orange)
![Machine Learning](https://img.shields.io/badge/Model-Random%20Forest-green)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-purple)

**Neuro ML** is an advanced web application designed to assess the risk of Alzheimer's Disease using Machine Learning. It provides an intuitive interface for patients and healthcare professionals to input clinical data, receive immediate risk predictions, and interact with an integrated LLM-powered medical assistant.

---
## 🌐 Check Live Website : [Neuro ML](https://alzheimer-disease-prediction-gp2t.onrender.com/)

---


## ✨ Key Features

### 1. 🤖 AI-Powered Risk Analysis
* Utilizes a trained **Random Forest Classifier** to predict the likelihood of Alzheimer's based on demographic, lifestyle, and clinical data.

### 2. 📝 PDF Report Generation
* Instantly generate and download a professional PDF summary of the assessment, including patient details and risk probability, suitable for medical record-keeping.

### 3. 💬 NeuroBot Assistant (Gemini Powered)
* A floating, intelligent chatbot powered by **Google Gemini**.
* Capable of explaining complex medical terms, offering health tips, and analyzing the specific data entered by the user in real-time.

### 4. 🛡️ Robust UI/UX
* **Dark/Light Mode:** Seamless theme toggling.
* **Smart Validation:** Prevents submission of erroneous data (e.g., impossible blood pressure values).
* **Responsive Design:** Works on desktop and mobile devices.
* **Interactive Health Tips:** Dedicated section for brain-healthy lifestyle recommendations.

---

## 🛠️ Tech Stack

* **Frontend:** [Dash](https://dash.plotly.com/), Dash Bootstrap Components (DBC), Custom CSS.
* **Backend:** Python.
* **Machine Learning:** Scikit-Learn, Joblib.
* **PDF Generation:** FPDF.
* **LLM Integration:** Google Generative AI (Gemini API).

---

## 📂 Project Structure

```text
NeuroPredict-AI/
│
├── assets/
│   ├── style.css           # Custom styling for Dark Mode & Animations
│   └── favicon.ico         # App Icon
│
├── models/
│   └── alzheimers_model_data.pkl  # Pre-trained ML Model & Encoders
│
├── Utils/
│   ├── components.py       # UI Component Definitions
│   ├── chatbot_service.py  # Google Gemini API Connection
│   ├── model_handler.py    # ML Prediction Logic
│   ├── pages.py            # Page Layouts (Home, Assessment, Tips)
│   └── report_generator.py # PDF Report Creation Logic
│
├── app.py                  # Main Application Entry Point
├── callbacks.py            # Logic Controller (Interactivity & Events)
├── config.py               # Feature Ranges & Form Configuration
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
````

-----

## 🚀 Installation & Setup

### 1\. Clone the Repository

```bash
git clone [https://github.com/Amr2054/Alzheimer_Disease_Classifier]
cd neuropredict-ai
```

### 2\. Create a Virtual Environment

It is recommended to run this project in an isolated environment.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Configure API Key

To use the **NeuroBot Assistant**, you need a Google Gemini API Key.

1.  Get a key from [Google AI Studio](https://aistudio.google.com/).
2.  Set it as an environment variable (Recommended):

**Windows (Powershell):**

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

**Mac/Linux (Terminal):**

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 5\. Run the Application

```bash
python app.py
```

Open your browser and navigate to: `http://127.0.0.1:8050/`

-----

## 🖥️ Usage Guide

1.  **Input Data:** Fill in the demographic and clinical fields manually.
2.  **Analyze:** Click **"Analyze Risk Profile"**.
      * The app will validate inputs and run the Random Forest model.
3.  **View Results:**
      * See the risk probability score and risk level (Low vs Elevated).
4.  **Download:** Click **"Download PDF Report"** to save the results.
5.  **Ask AI:** Click the **Brain Icon** (bottom-left) to open NeuroBot. Ask questions like *"What does my MMSE score mean?"* or *"How can I lower my cholesterol?"*.

-----

## ⚠️ Medical Disclaimer

**IMPORTANT:** This application is a prototype developed for educational and screening assistance purposes only.

  * It is **not** a substitute for professional medical diagnosis or treatment.
  * The predictions are based on statistical patterns and may produce false positives or false negatives.
  * Always consult a qualified neurologist or healthcare provider for medical advice.

-----

## 📜 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
