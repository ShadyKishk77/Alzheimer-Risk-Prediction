# config.py - Feature definitions and configuration

MODEL_FILE = 'models/alzheimers_model_data.pkl'

FEATURE_GROUPS = {
    "Patient Demographics": {
        "icon": "fa-user",
        "color": "#6366f1",
        "features": [
            {'name': 'Age', 'label': 'Age', 'unit': 'years', 'type': 'number', 'min': 60, 'max': 90, 'default': 70},
            {'name': 'Gender', 'label': 'Gender', 'type': 'dropdown', 'options': [
                {'label': 'Male', 'value': 0}, {'label': 'Female', 'value': 1}
            ]},
            {'name': 'Ethnicity', 'label': 'Ethnicity', 'type': 'dropdown', 'options': [
                {'label': 'Caucasian', 'value': 0}, {'label': 'African American', 'value': 1},
                {'label': 'Asian', 'value': 2}, {'label': 'Other', 'value': 3}
            ]},
            {'name': 'EducationLevel', 'label': 'Education Level', 'type': 'dropdown', 'options': [
                {'label': 'None', 'value': 0}, {'label': 'High School', 'value': 1},
                {'label': "Bachelor's", 'value': 2}, {'label': 'Higher', 'value': 3}
            ]},
            {'name': 'BMI', 'label': 'BMI', 'unit': 'kg/m²', 'type': 'number', 'min': 15, 'max': 40, 'default': 25.0},
        ]
    },
    "Lifestyle Factors": {
        "icon": "fa-heart-pulse",
        "color": "#ec4899",
        "features": [
            {'name': 'Smoking', 'label': 'Smoker?', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'AlcoholConsumption', 'label': 'Alcohol Consumption', 'unit': 'units/week', 'type': 'number', 'min': 0, 'max': 20, 'default': 5.0},
            {'name': 'PhysicalActivity', 'label': 'Physical Activity', 'unit': 'hrs/week', 'type': 'number', 'min': 0, 'max': 10, 'default': 5.0},
            {'name': 'DietQuality', 'label': 'Diet Quality', 'unit': '0-10', 'type': 'number', 'min': 0, 'max': 10, 'default': 5.0},
            {'name': 'SleepQuality', 'label': 'Sleep Quality', 'unit': '4-10', 'type': 'number', 'min': 4, 'max': 10, 'default': 7.0},
        ]
    },
    "Medical History": {
        "icon": "fa-notes-medical",
        "color": "#f59e0b",
        "features": [
            {'name': 'FamilyHistoryAlzheimers', 'label': "Family History of Alzheimer's", 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'CardiovascularDisease', 'label': 'Cardiovascular Disease', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'Diabetes', 'label': 'Diabetes', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'Depression', 'label': 'Depression', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'HeadInjury', 'label': 'History of Head Injury', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'Hypertension', 'label': 'Hypertension', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
        ]
    },
    "Clinical Measurements": {
        "icon": "fa-stethoscope",
        "color": "#10b981",
        "features": [
            {'name': 'SystolicBP', 'label': 'Systolic BP', 'unit': 'mmHg', 'type': 'number', 'min': 90, 'max': 180, 'default': 120},
            {'name': 'DiastolicBP', 'label': 'Diastolic BP', 'unit': 'mmHg', 'type': 'number', 'min': 60, 'max': 120, 'default': 80},
            {'name': 'CholesterolTotal', 'label': 'Total Cholesterol', 'unit': 'mg/dL', 'type': 'number', 'min': 150, 'max': 300, 'default': 200},
            {'name': 'CholesterolLDL', 'label': 'LDL Cholesterol', 'unit': 'mg/dL', 'type': 'number', 'min': 50, 'max': 200, 'default': 100},
            {'name': 'CholesterolHDL', 'label': 'HDL Cholesterol', 'unit': 'mg/dL', 'type': 'number', 'min': 20, 'max': 100, 'default': 50},
            {'name': 'CholesterolTriglycerides', 'label': 'Triglycerides', 'unit': 'mg/dL', 'type': 'number', 'min': 50, 'max': 400, 'default': 150},
        ]
    },
    "Cognitive & Symptoms": {
        "icon": "fa-brain",
        "color": "#8b5cf6",
        "features": [
            {'name': 'MMSE', 'label': 'MMSE Score', 'unit': '0-30', 'type': 'number', 'min': 0, 'max': 30, 'default': 25},
            {'name': 'FunctionalAssessment', 'label': 'Functional Assessment', 'unit': '0-10', 'type': 'number', 'min': 0, 'max': 10, 'default': 5},
            {'name': 'ADL', 'label': 'ADL Score', 'unit': '0-10', 'type': 'number', 'min': 0, 'max': 10, 'default': 8},
            {'name': 'MemoryComplaints', 'label': 'Memory Complaints', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'BehavioralProblems', 'label': 'Behavioral Problems', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'Confusion', 'label': 'Confusion', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'Disorientation', 'label': 'Disorientation', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'PersonalityChanges', 'label': 'Personality Changes', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'DifficultyCompletingTasks', 'label': 'Difficulty Completing Tasks', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
            {'name': 'Forgetfulness', 'label': 'Forgetfulness', 'type': 'radio',
             'options': [{'label': 'No', 'value': 0}, {'label': 'Yes', 'value': 1}]},
        ]
    }
}