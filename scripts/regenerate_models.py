"""
Regenerate model files compatible with current environment.
This script retrains the models and saves them in a format compatible with your NumPy version.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

print("="*60)
print("MODEL REGENERATION SCRIPT")
print("="*60)
print(f"Python environment:")
print(f"  NumPy: {np.__version__}")
print(f"  scikit-learn: {joblib.__version__}")
print("="*60)

# Define paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

print(f"\nBase directory: {BASE_DIR}")
print(f"Models directory: {MODELS_DIR}")

# Find the preprocessed data file
data_files = list(DATA_DIR.glob("processed*.csv"))
if not data_files:
    data_files = list(DATA_DIR.glob("*preprocessed*.csv"))
if not data_files:
    data_files = list(DATA_DIR.glob("alzheimers*.csv"))
if not data_files:
    data_files = list(DATA_DIR.glob("*.csv"))

if not data_files:
    print("\nERROR: No data file found in data/ directory")
    print("Available files:")
    for f in DATA_DIR.glob("*.csv"):
        print(f"  - {f.name}")
    print("\nPlease ensure you have the dataset CSV file.")
    exit(1)

data_file = data_files[0]
print(f"\nLoading data from: {data_file.name}")

# Load data
df = pd.read_csv(data_file)
print(f"Data loaded: {len(df)} rows, {len(df.columns)} columns")

# Identify target column
target_candidates = ['Diagnosis', 'diagnosis', 'target', 'Target']
target_col = None
for col in target_candidates:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    print("\nERROR: Could not find target column")
    print(f"Available columns: {list(df.columns)}")
    exit(1)

print(f"Target column: {target_col}")

# Prepare data
X = df.drop(columns=[target_col])
y = df[target_col]

# Remove non-numeric columns if any
numeric_cols = X.select_dtypes(include=[np.number]).columns
if len(numeric_cols) < len(X.columns):
    print(f"Warning: Removing {len(X.columns) - len(numeric_cols)} non-numeric columns")
    X = X[numeric_cols]

print(f"Features: {len(X.columns)} columns")
print(f"   First few: {list(X.columns[:5])}")

# Save feature names
feature_names = list(X.columns)
feature_names_path = MODELS_DIR / "feature_names.pkl"
joblib.dump(feature_names, feature_names_path)
print(f"Saved feature names to: {feature_names_path.name}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain/test split: {len(X_train)} train, {len(X_test)} test")

# Fit and save scaler
print("\nFitting StandardScaler...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

scaler_path = MODELS_DIR / "scaler.pkl"
joblib.dump(scaler, scaler_path)
print(f"Saved scaler to: {scaler_path.name}")

# Train Gradient Boosting (best model)
print("\nTraining Gradient Boosting Classifier...")
gb_model = GradientBoostingClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    random_state=42,
    verbose=0
)
gb_model.fit(X_train_scaled, y_train)
gb_score = gb_model.score(X_test_scaled, y_test)
print(f"Gradient Boosting trained - Test accuracy: {gb_score:.4f}")

gb_path = MODELS_DIR / "tuned_gradient_boosting.pkl"
joblib.dump(gb_model, gb_path)
print(f"Saved Gradient Boosting to: {gb_path.name}")

# Train Random Forest
print("\nTraining Random Forest Classifier...")
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    n_jobs=-1,
    verbose=0
)
rf_model.fit(X_train_scaled, y_train)
rf_score = rf_model.score(X_test_scaled, y_test)
print(f"Random Forest trained - Test accuracy: {rf_score:.4f}")

rf_path = MODELS_DIR / "tuned_random_forest.pkl"
joblib.dump(rf_model, rf_path)
print(f"Saved Random Forest to: {rf_path.name}")

# Train Logistic Regression
print("\nTraining Logistic Regression...")
lr_model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    verbose=0
)
lr_model.fit(X_train_scaled, y_train)
lr_score = lr_model.score(X_test_scaled, y_test)
print(f"Logistic Regression trained - Test accuracy: {lr_score:.4f}")

lr_path = MODELS_DIR / "tuned_logistic_regression.pkl"
joblib.dump(lr_model, lr_path)
print(f"Saved Logistic Regression to: {lr_path.name}")

# Summary
print("\n" + "="*60)
print("MODEL REGENERATION COMPLETE!")
print("="*60)
print(f"Models saved to: {MODELS_DIR}")
print(f"\nModel Performance:")
print(f"  Gradient Boosting: {gb_score:.4f}")
print(f"  Random Forest:     {rf_score:.4f}")
print(f"  Logistic Regression: {lr_score:.4f}")
print(f"\nFiles created:")
print(f"  - {feature_names_path.name}")
print(f"  - {scaler_path.name}")
print(f"  - {gb_path.name}")
print(f"  - {rf_path.name}")
print(f"  - {lr_path.name}")
print("\nYou can now start the API server:")
print("   python api\\start_api.py --reload")
print("="*60)
