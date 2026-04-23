CREATE DATABASE IF NOT EXISTS diabetes_predictions;
USE diabetes_predictions;
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregnancies FLOAT,
    glucose FLOAT,
    blood_pressure FLOAT,
    skin_thickness FLOAT,
    insulin FLOAT,
    bmi FLOAT,
    pedigree_function FLOAT,
    age FLOAT,
    prediction_result INT,
    prediction_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
