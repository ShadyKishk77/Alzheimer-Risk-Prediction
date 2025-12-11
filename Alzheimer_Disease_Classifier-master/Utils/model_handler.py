# model_handler.py - Model loading and prediction logic

import joblib
import pandas as pd
from config import MODEL_FILE


class ModelHandler:
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.encoders = {}
        self._load_model()

    def _load_model(self):
        """Load the trained model and associated data."""
        try:
            data = joblib.load(MODEL_FILE)
            self.model = data['model']
            self.feature_names = data.get('features', [])
            self.encoders = data.get('encoders', {})
            print("✓ Model loaded successfully.")
        except FileNotFoundError:
            print(f"✗ Model file '{MODEL_FILE}' not found.")
        except Exception as e:
            print(f"✗ Error loading model: {e}")

    def is_loaded(self):
        """Check if model is loaded."""
        return self.model is not None

    def prepare_input(self, values, ids):
        """Prepare input data from form values."""
        input_data = {}

        for val, id_obj in zip(values, ids):
            feature_name = id_obj['index']

            if feature_name in self.encoders:
                try:
                    val_str = str(val)
                    encoded_val = self.encoders[feature_name].transform([val_str])[0]
                    input_data[feature_name] = encoded_val
                except Exception as e:
                    raise ValueError(f"Error encoding {feature_name}: {e}")
            else:
                input_data[feature_name] = val

        return input_data

    def predict(self, input_data):
        """Make prediction and return models_results_plots."""
        if not self.is_loaded():
            raise RuntimeError("Model not loaded")

        df = pd.DataFrame([input_data])
        df = df.reindex(columns=self.feature_names, fill_value=0)

        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0][1]

        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'is_positive': prediction == 1
        }


# Singleton instance
model_handler = ModelHandler()