# Healthcare Predictive Analytics: Alzheimer's Disease Risk Prediction

## Project Overview

This project presents a comprehensive machine learning framework for predicting Alzheimer's disease risk using patient health metrics and demographic data. The analysis includes exploratory data analysis, statistical hypothesis testing, interactive visualizations, and optimized predictive models.

## Project Structure

```
├── data/                           # Dataset storage
│   ├── raw_alzheimers_data.csv    # Original patient dataset
│   └── processed_alzheimers_data.csv  # Preprocessed and standardized data
├── notebooks/                      # Jupyter notebooks
│   └── alzheimers_analysis.ipynb  # Main analysis and modeling notebook
├── reports/                        # Visualizations and analysis outputs
│   ├── age_distribution.png
│   ├── bmi_distribution.png
│   ├── boxplots_comparisons.png
│   ├── cognitive_assessments.png
│   ├── cognitive_pairplot.png
│   ├── confusion_matrices.png
│   ├── correlation_matrix.png
│   ├── diagnosis_distribution.png
│   ├── enhanced_correlation_heatmap.png
│   ├── feature_importance.png
│   ├── gender_distribution.png
│   ├── model_performance_comparison.png
│   ├── pca_visualization.png
│   ├── roc_curves.png
│   ├── scatter_plots_relationships.png
│   └── tuned_model_comparison.png
├── models/                         # Trained machine learning models
│   ├── tuned_random_forest.pkl
│   ├── tuned_gradient_boosting.pkl
│   ├── tuned_logistic_regression.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
└── docs/                          # Project documentation
    ├── README.md                  # This file
    ├── requirements.txt           # Python dependencies
    └── environment.yml            # Conda environment specification
```

## Objectives

1. Conduct thorough exploratory data analysis to understand patient characteristics
2. Perform statistical hypothesis testing to identify significant health metric associations
3. Develop interactive visualizations for insight communication
4. Build and optimize machine learning models for accurate risk prediction
5. Deploy production-ready models for clinical decision support

## Methodology

### Data Analysis
- Comprehensive data quality assessment
- Missing value analysis and outlier detection
- Correlation analysis between features and outcomes
- Statistical hypothesis testing (t-tests, chi-square, ANOVA)

### Visualization
- Static visualizations using Matplotlib and Seaborn
- Interactive dashboards using Plotly
- Multi-dimensional data exploration tools
- Feature relationship analysis plots

### Machine Learning
- Four baseline models: Logistic Regression, Random Forest, Gradient Boosting, Neural Network
- Five-fold cross-validation for robust evaluation
- Hyperparameter optimization using GridSearchCV and RandomizedSearchCV
- Comprehensive performance metrics: accuracy, precision, recall, F1-score, ROC-AUC

## Key Results

- Successfully trained and optimized four machine learning models
- Identified key predictive features for Alzheimer's diagnosis
- Achieved strong model performance with validated generalization capability
- Generated 16 comprehensive visualizations for data insights
- Created production-ready models with deployment artifacts

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Required packages listed in `requirements.txt`

### Installation

1. Clone or download the project repository

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r docs/requirements.txt
```

Alternatively, using Conda:
```bash
conda env create -f docs/environment.yml
conda activate alzheimers-prediction
```

## Usage

### Running the Analysis

1. Navigate to the project directory
2. Launch Jupyter Notebook:
```bash
jupyter notebook
```
3. Open `notebooks/alzheimers_analysis.ipynb`
4. Run cells sequentially to reproduce the analysis

### Using Saved Models

```python
import joblib
import pandas as pd
import numpy as np

# Load the model and preprocessing artifacts
model = joblib.load('models/tuned_random_forest.pkl')
scaler = joblib.load('models/scaler.pkl')
feature_names = joblib.load('models/feature_names.pkl')

# Prepare new patient data (ensure same feature order)
new_patient_data = pd.DataFrame([patient_features], columns=feature_names)

# Scale features
scaled_data = scaler.transform(new_patient_data)

# Make prediction
prediction = model.predict(scaled_data)
probability = model.predict_proba(scaled_data)

print(f"Prediction: {prediction[0]}")  # 0 = No Alzheimer's, 1 = Alzheimer's
print(f"Probability: {probability[0]}")
```

## Model Performance

All models were evaluated using:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

The optimized models show strong predictive performance with validated generalization through cross-validation.

## Features

The analysis uses the following patient features:
- Demographics: Age, Gender, Ethnicity, Education Level
- Lifestyle factors: BMI, Smoking, Alcohol Consumption, Physical Activity, Diet Quality, Sleep Quality
- Medical history: Family History, Cardiovascular Disease, Diabetes, Depression, Head Injury, Hypertension
- Clinical measurements: Systolic BP, Diastolic BP, Cholesterol levels
- Cognitive assessments: MMSE, Functional Assessment, Memory Complaints, ADL

## Clinical Implications

The developed predictive models provide:
- Reliable risk assessment tools for early Alzheimer's detection
- Feature importance analysis for actionable clinical insights
- Evidence-based decision support for healthcare providers
- Framework for patient stratification and intervention planning

## Future Work

- Prospective validation with new patient cohorts
- Integration with electronic health record systems
- Development of web-based prediction interface
- Regular model retraining with updated data
- Extension to other neurodegenerative diseases

## Contributors

DEPI Graduate Project Team

## License

This project is intended for educational and research purposes.

## Contact

For questions or collaboration opportunities, please contact the project team.

## Acknowledgments

- Healthcare data providers
- DEPI program coordinators
- Clinical advisors and domain experts

---

**Note**: This project follows best practices for reproducible research and clinical ML model development.
