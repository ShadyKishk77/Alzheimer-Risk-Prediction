// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Feature order (must match model expectations)
const FEATURE_NAMES = [
    'Age', 'Gender', 'Ethnicity', 'EducationLevel', 'BMI', 'Smoking',
    'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality',
    'FamilyHistoryAlzheimers', 'CardiovascularDisease', 'Diabetes', 'Depression',
    'HeadInjury', 'Hypertension', 'SystolicBP', 'DiastolicBP',
    'CholesterolTotal', 'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides',
    'MMSE', 'FunctionalAssessment', 'MemoryComplaints', 'BehavioralProblems',
    'ADL', 'Confusion', 'Disorientation', 'PersonalityChanges',
    'DifficultyCompletingTasks', 'Forgetfulness'
];

// Initialize app
document.addEventListener('DOMContentLoaded', function () {
    checkAPIHealth();
    setupFormHandlers();
    loadSampleData(); // Optional: for testing
});

// Check API health status
async function checkAPIHealth() {
    const statusDiv = document.getElementById('apiStatus');

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (data.status === 'healthy' && data.model_loaded) {
            statusDiv.className = 'api-status healthy';
            statusDiv.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <span>API Connected | Model v${data.model_version} | Ready for predictions</span>
            `;
        } else {
            throw new Error('Model not loaded');
        }
    } catch (error) {
        statusDiv.className = 'api-status unhealthy';
        statusDiv.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <span>API Unavailable: ${error.message}. Please start the API server.</span>
        `;
    }
}

// Setup form event handlers
function setupFormHandlers() {
    const form = document.getElementById('predictionForm');
    form.addEventListener('submit', handleFormSubmit);

    // Add real-time validation
    const inputs = form.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function () {
            validateInput(this);
        });
    });
}

// Validate individual input
function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);

    if (input.value && (value < min || value > max)) {
        input.style.borderColor = 'var(--danger-color)';
        return false;
    } else {
        input.style.borderColor = 'var(--border-color)';
        return true;
    }
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();

    // Validate all inputs
    const form = event.target;
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    // Collect form data
    const formData = collectFormData(form);

    // Show loading overlay
    showLoading(true);

    try {
        // Make prediction request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Prediction failed');
        }

        const result = await response.json();

        // Display results
        displayResults(result);

        // Scroll to results
        document.getElementById('resultsCard').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// Collect form data in correct order
function collectFormData(form) {
    const features = [];

    // Map form field names to values in correct order
    const fieldMap = {
        'age': 'Age',
        'gender': 'Gender',
        'ethnicity': 'Ethnicity',
        'educationLevel': 'EducationLevel',
        'bmi': 'BMI',
        'smoking': 'Smoking',
        'alcoholConsumption': 'AlcoholConsumption',
        'physicalActivity': 'PhysicalActivity',
        'dietQuality': 'DietQuality',
        'sleepQuality': 'SleepQuality',
        'familyHistoryAlzheimers': 'FamilyHistoryAlzheimers',
        'cardiovascularDisease': 'CardiovascularDisease',
        'diabetes': 'Diabetes',
        'depression': 'Depression',
        'headInjury': 'HeadInjury',
        'hypertension': 'Hypertension',
        'systolicBP': 'SystolicBP',
        'diastolicBP': 'DiastolicBP',
        'cholesterolTotal': 'CholesterolTotal',
        'cholesterolLDL': 'CholesterolLDL',
        'cholesterolHDL': 'CholesterolHDL',
        'cholesterolTriglycerides': 'CholesterolTriglycerides',
        'mmse': 'MMSE',
        'functionalAssessment': 'FunctionalAssessment',
        'memoryComplaints': 'MemoryComplaints',
        'behavioralProblems': 'BehavioralProblems',
        'adl': 'ADL',
        'confusion': 'Confusion',
        'disorientation': 'Disorientation',
        'personalityChanges': 'PersonalityChanges',
        'difficultyCompletingTasks': 'DifficultyCompletingTasks',
        'forgetfulness': 'Forgetfulness'
    };

    // Collect features in the correct order
    for (const featureName of FEATURE_NAMES) {
        const fieldName = Object.keys(fieldMap).find(key => fieldMap[key] === featureName);
        const element = form.elements[fieldName];

        if (element) {
            features.push(parseFloat(element.value));
        }
    }

    // Build request payload
    const payload = {
        features: features
    };

    // Add patient ID if provided
    const patientId = form.elements['patientId'].value.trim();
    if (patientId) {
        payload.patient_id = patientId;
    }

    return payload;
}

// Display prediction results
function displayResults(result) {
    const resultsCard = document.getElementById('resultsCard');
    const riskBadge = document.getElementById('riskBadge');
    const riskLevel = document.getElementById('riskLevel');
    const probabilityValue = document.getElementById('probabilityValue');
    const probabilityPercent = document.getElementById('probabilityPercent');
    const confidence = document.getElementById('confidence');
    const modelVersion = document.getElementById('modelVersion');
    const resultPatientId = document.getElementById('resultPatientId');
    const gaugeFill = document.getElementById('gaugeFill');

    // Set risk level
    riskLevel.textContent = result.risk_level;
    riskBadge.className = `risk-badge ${result.risk_level.toLowerCase()}`;

    // Set icon based on risk level
    const iconMap = {
        'Low': 'fa-check-circle',
        'Moderate': 'fa-exclamation-circle',
        'High': 'fa-exclamation-triangle',
        'Critical': 'fa-skull-crossbones'
    };
    riskBadge.querySelector('i').className = `fas ${iconMap[result.risk_level] || 'fa-exclamation-triangle'}`;

    // Set probability
    const percentage = (result.probability * 100).toFixed(1);
    probabilityValue.textContent = `${percentage}%`;
    probabilityPercent.textContent = `${percentage}%`;

    // Animate gauge
    setTimeout(() => {
        gaugeFill.style.width = `${percentage}%`;
    }, 100);

    // Set other metrics
    confidence.textContent = result.confidence;
    modelVersion.textContent = `v${result.model_version}`;
    resultPatientId.textContent = result.patient_id || 'N/A';

    // Generate recommendations
    generateRecommendations(result);

    // Show results card
    resultsCard.style.display = 'block';
}

// Generate clinical recommendations based on risk level
function generateRecommendations(result) {
    const recommendationsList = document.getElementById('recommendationsList');

    const recommendations = {
        'Low': [
            'Continue routine health maintenance and monitoring',
            'Maintain healthy lifestyle habits (diet, exercise, sleep)',
            'Annual cognitive screening recommended',
            'Keep cardiovascular risk factors controlled',
            'Stay mentally and socially active'
        ],
        'Moderate': [
            'Schedule enhanced monitoring with 6-month follow-ups',
            'Consider comprehensive cognitive assessment',
            'Optimize management of cardiovascular risk factors',
            'Increase physical and cognitive activities',
            'Discuss preventive strategies with healthcare provider',
            'Consider family education and support resources'
        ],
        'High': [
            ' Specialist referral to neurologist or geriatrician advised',
            'Comprehensive neuropsychological evaluation recommended',
            'Brain imaging (MRI/CT) may be indicated',
            'Aggressive management of modifiable risk factors',
            'Consider cognitive training programs',
            'Evaluate for clinical trial eligibility',
            'Establish advance care planning discussions'
        ],
        'Critical': [
            ' URGENT: Immediate specialist consultation required',
            'Comprehensive diagnostic workup including imaging and biomarkers',
            'Consider specialized memory clinic evaluation',
            'Intensive management of all risk factors',
            'Evaluate for appropriate interventions',
            'Family counseling and caregiver support essential',
            'Discuss clinical trial opportunities',
            'Establish care coordination and support network'
        ]
    };

    const riskRecommendations = recommendations[result.risk_level] || [];

    let html = '<ul>';
    riskRecommendations.forEach(rec => {
        html += `<li><i class="fas fa-chevron-right"></i><span>${rec}</span></li>`;
    });
    html += '</ul>';

    recommendationsList.innerHTML = html;
}

// Show/hide loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.className = show ? 'loading-overlay active' : 'loading-overlay';
}

// Show error message
function showError(message) {
    alert(`Error: ${message}\n\nPlease check:\n1. API server is running\n2. All form fields are valid\n3. Network connection is active`);
}

// Reset form
function resetForm() {
    const form = document.getElementById('predictionForm');
    form.reset();

    // Hide results
    const resultsCard = document.getElementById('resultsCard');
    resultsCard.style.display = 'none';

    // Reset gauge
    const gaugeFill = document.getElementById('gaugeFill');
    gaugeFill.style.width = '0%';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Print results
function printResults() {
    window.print();
}

// New prediction
function newPrediction() {
    resetForm();
}

// Load sample data for testing (optional)
function loadSampleData() {
    // You can uncomment this to pre-fill form with sample data for testing
    /*
    const sampleData = {
        age: 75,
        gender: 1,
        ethnicity: 2,
        educationLevel: 12,
        bmi: 28.5,
        smoking: 0,
        alcoholConsumption: 3,
        physicalActivity: 2.5,
        dietQuality: 6,
        sleepQuality: 5,
        familyHistoryAlzheimers: 1,
        cardiovascularDisease: 0,
        diabetes: 1,
        depression: 0,
        headInjury: 0,
        hypertension: 1,
        systolicBP: 145,
        diastolicBP: 88,
        cholesterolTotal: 220,
        cholesterolLDL: 140,
        cholesterolHDL: 50,
        cholesterolTriglycerides: 180,
        mmse: 22,
        functionalAssessment: 6.5,
        memoryComplaints: 1,
        behavioralProblems: 0,
        adl: 7,
        confusion: 1,
        disorientation: 0,
        personalityChanges: 0,
        difficultyCompletingTasks: 1,
        forgetfulness: 1
    };
    
    const form = document.getElementById('predictionForm');
    Object.keys(sampleData).forEach(key => {
        const element = form.elements[key];
        if (element) {
            element.value = sampleData[key];
        }
    });
    */
}

// Export functions for use in HTML
window.resetForm = resetForm;
window.printResults = printResults;
window.newPrediction = newPrediction;
