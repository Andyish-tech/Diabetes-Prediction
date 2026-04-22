import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def train_model():
    print("Loading data...")
    # 2. Load dataset
    data_path = os.path.join(os.path.dirname(__file__), '..', 'diabetes.csv')
    data = pd.read_csv(data_path)

    print("Data Cleaning...")
    # 3. Data Cleaning (Improved)
    cols_with_zero_as_missing = [
        'Glucose', 'BloodPressure', 'BMI', 'Insulin', 'SkinThickness'
    ]

    # Replace invalid zeros with NaN
    data[cols_with_zero_as_missing] = data[cols_with_zero_as_missing].replace(0, np.nan)

    # Fill missing values using MEDIAN per class (better medical logic)
    for col in cols_with_zero_as_missing:
        data[col] = data.groupby('Outcome')[col].transform(
            lambda x: x.fillna(x.median())
        )
        
    # Fallback just in case some NaN remain if grouping caused an issue
    data.fillna(data.median(), inplace=True)

    print("Feature Engineering...")
    # 4. Feature Engineering
    data['BMI_Age'] = data['BMI'] * data['Age']
    data['Glucose_BMI'] = data['Glucose'] * data['BMI']

    # 5. Split features & target
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    print("Splitting...")
    # 6. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("Scaling...")
    # 7. Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print("Training Model with GridSearchCV...")
    # 8. Model: Gradient Boosting (BEST CHOICE)
    param_grid = {
        'n_estimators': [200, 300, 400],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [2, 3, 4]
    }

    grid = GridSearchCV(
        GradientBoostingClassifier(),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )

    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_

    print("\n=== MODEL PERFORMANCE ===")
    y_pred = best_model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    print("\nSaving Models...")
    # Save Model and Scaler
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
    
    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

if __name__ == '__main__':
    train_model()
