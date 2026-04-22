import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

def check_and_impute(df, col_name):
    # Impute missing values with group median based on 'Outcome'
    df[col_name] = df[col_name].fillna(df.groupby('Outcome')[col_name].transform('median'))
    return df

def train_model():
    print("Loading data...")
    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'diabetes.csv')
    df = pd.read_csv(data_path)

    print("Preprocessing...")
    # Replace valid 0 values with NaN for specific columns
    cols_with_invalid_zeros = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    df[cols_with_invalid_zeros] = df[cols_with_invalid_zeros].replace(0, np.nan)

    # Impute missing values
    for col in cols_with_invalid_zeros:
        df = check_and_impute(df, col)
        
    # Extra fallback if 'Outcome' grouping caused NaN (should not happen in this dataset)
    df.fillna(df.median(), inplace=True)

    print("Feature Engineering...")
    # Feature engineering: BMI x Age, Glucose x BMI
    df['BMI_Age'] = df['BMI'] * df['Age']
    df['Glucose_BMI'] = df['Glucose'] * df['BMI']

    # Splitting features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    print("Splitting and Scaling...")
    # Train-test split (80/20, Stratified)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale variables
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training Model...")
    # Train Gradient Boosting Classifier
    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train_scaled, y_train)

    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model Accuracy: {accuracy:.4f}")

    print("Saving Models...")
    # Save Model and Scaler
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

if __name__ == '__main__':
    train_model()
