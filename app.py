import os
import pickle
import pandas as pd
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load the pre-trained loan prediction model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'loan_model.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Training data statistics for imputing missing values
IMPUTATION_DEFAULTS = {
    'Gender': 1,              # Mode: Male
    'Married': 1,             # Mode: Yes
    'Dependents': 0,          # Mode: 0
    'Education': 0,           # Mode: Graduate
    'Self_Employed': 0,       # Mode: No
    'ApplicantIncome': 5403,  # Approximate Mean
    'CoapplicantIncome': 1621, # Approximate Mean
    'LoanAmount': 146.412162, # Mean
    'Loan_Amount_Term': 360.0, # Mode
    'Credit_History': 1.0,     # Mode
    'Property_Area': 1         # Mode: Semiurban (1)
}

# String value level mapping to integer representation
CATEGORICAL_MAPPINGS = {
    'Gender': {'Female': 0, 'Male': 1},
    'Married': {'No': 0, 'Yes': 1},
    'Dependents': {'0': 0, '1': 1, '2': 2, '3+': 3},
    'Education': {'Graduate': 0, 'Not Graduate': 1},
    'Self_Employed': {'No': 0, 'Yes': 1},
    'Property_Area': {'Rural': 0, 'Semiurban': 1, 'Urban': 2}
}

def predict(features_df):
    """
    Predicts the loan approval status using the loaded XGBoost model.
    Returns "Loan Approved" or "Loan Rejected".
    """
    if model is None:
        raise ValueError("Model is not loaded properly.")
    
    # Predict status
    prediction = model.predict(features_df)[0]
    
    # XGBoost output: 1 for Yes (Approved), 0 for No (Rejected)
    if prediction == 1:
        return "Loan Approved"
    else:
        return "Loan Rejected"

@app.route('/')
def home():
    """Renders the Home Page."""
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_route():
    """Handles loan eligibility prediction form rendering and submission."""
    if request.method == 'POST':
        # Retrieve form data and process it
        try:
            # Helper function to get float or fallback to default
            def get_float(field_name):
                val = request.form.get(field_name, '').strip()
                return float(val) if val else IMPUTATION_DEFAULTS[field_name]

            # Categorical Mapping helper
            def get_encoded(field_name):
                val = request.form.get(field_name, '').strip()
                if not val or val not in CATEGORICAL_MAPPINGS[field_name]:
                    return IMPUTATION_DEFAULTS[field_name]
                return CATEGORICAL_MAPPINGS[field_name][val]

            # Build feature dictionary aligned with training feature names
            features = {
                'Gender': get_encoded('Gender'),
                'Married': get_encoded('Married'),
                'Dependents': get_encoded('Dependents'),
                'Education': get_encoded('Education'),
                'Self_Employed': get_encoded('Self_Employed'),
                'ApplicantIncome': get_float('ApplicantIncome'),
                'CoapplicantIncome': get_float('CoapplicantIncome'),
                'LoanAmount': get_float('LoanAmount'),
                'Loan_Amount_Term': get_float('Loan_Amount_Term'),
                'Credit_History': get_float('Credit_History'),
                'Property_Area': get_encoded('Property_Area')
            }

            # Convert features to a 2D Pandas DataFrame (matching training column names and ordering)
            columns = [
                'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 
                'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 
                'Credit_History', 'Property_Area'
            ]
            features_df = pd.DataFrame([features], columns=columns)

            # Perform prediction
            status = predict(features_df)
            
            # Pass input parameters back to render the result
            return render_template('result.html', 
                                   status=status, 
                                   raw_inputs=request.form)

        except Exception as e:
            return render_template('predict.html', error=f"Prediction error: {str(e)}")

    return render_template('predict.html')

@app.route('/health')
def health():
    """Health check endpoint for cloud hosting / load balancers."""
    model_status = "loaded" if model is not None else "failed"
    return {"status": "ok", "model": model_status}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1', 't')
    app.run(debug=debug, host='0.0.0.0', port=port)
