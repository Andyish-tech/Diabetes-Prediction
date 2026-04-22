import sys
import json
import pandas as pd
import joblib
import os

def predict(input_data_json):
    try:
        # Load data
        data = json.loads(input_data_json)
        
        # Make a DataFrame
        # The input data should be a dictionary with keys matching the original CSV minus Outcome
        # Order: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
        df = pd.DataFrame([data])
        
        # Feature Engineering
        if 'BMI' in df.columns and 'Age' in df.columns:
            df['BMI_Age'] = df['BMI'] * df['Age']
        if 'Glucose' in df.columns and 'BMI' in df.columns:
            df['Glucose_BMI'] = df['Glucose'] * df['BMI']
        
        # Ensure correct column order
        cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 
                'BMI', 'DiabetesPedigreeFunction', 'Age', 'BMI_Age', 'Glucose_BMI']
        df = df[cols]
        
        # Load model and scaler
        ml_dir = os.path.dirname(__file__)
        model = joblib.load(os.path.join(ml_dir, 'model.pkl'))
        scaler = joblib.load(os.path.join(ml_dir, 'scaler.pkl'))
        
        # Scale
        scaled_data = scaler.transform(df)
        
        # Predict
        prediction = model.predict(scaled_data)[0]
        status = "Diabetic" if prediction == 1 else "Not Diabetic"
        
        # Return as JSON
        result = {
            "prediction": int(prediction),
            "status": status,
            "success": True
        }
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_result))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        predict(sys.argv[1])
    else:
        print(json.dumps({"success": False, "error": "No input data provided"}))
