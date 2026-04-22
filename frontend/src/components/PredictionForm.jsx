import React, { useState } from 'react';
import axios from 'axios';

const INITAL_STATE = {
  Pregnancies: '',
  Glucose: '',
  BloodPressure: '',
  SkinThickness: '',
  Insulin: '',
  BMI: '',
  DiabetesPedigreeFunction: '',
  Age: ''
};

export default function PredictionForm() {
  const [formData, setFormData] = useState(INITAL_STATE);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    // Convert strings to floats/ints for the backend
    const payload = {};
    for (const key in formData) {
      if (formData[key] === '') {
        setError(`Please fill out ${key}`);
        setLoading(false);
        return;
      }
      payload[key] = parseFloat(formData[key]);
    }

    try {
      const response = await axios.post('http://localhost:3001/api/predict', payload);
      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || 'Prediction failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Error communicating with server. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel prediction-form-wrapper">
      <form onSubmit={handleSubmit}>
        <div className="input-grid">
          <div className="form-group">
            <label htmlFor="Pregnancies">Pregnancies (0-20)</label>
            <input className="custom-input" type="number" step="1" min="0" name="Pregnancies" value={formData.Pregnancies} onChange={handleChange} placeholder="e.g. 2" required />
          </div>
          
          <div className="form-group">
            <label htmlFor="Glucose">Glucose (mg/dL)</label>
            <input className="custom-input" type="number" step="0.1" name="Glucose" value={formData.Glucose} onChange={handleChange} placeholder="e.g. 120" required />
          </div>

          <div className="form-group">
            <label htmlFor="BloodPressure">Blood Pressure (mm Hg)</label>
            <input className="custom-input" type="number" step="0.1" name="BloodPressure" value={formData.BloodPressure} onChange={handleChange} placeholder="e.g. 70" required />
          </div>

          <div className="form-group">
            <label htmlFor="SkinThickness">Skin Thickness (mm)</label>
            <input className="custom-input" type="number" step="0.1" name="SkinThickness" value={formData.SkinThickness} onChange={handleChange} placeholder="e.g. 20" required />
          </div>

          <div className="form-group">
            <label htmlFor="Insulin">Insulin (mu U/ml)</label>
            <input className="custom-input" type="number" step="0.1" name="Insulin" value={formData.Insulin} onChange={handleChange} placeholder="e.g. 79" required />
          </div>

          <div className="form-group">
            <label htmlFor="BMI">Body Mass Index (BMI)</label>
            <input className="custom-input" type="number" step="0.1" name="BMI" value={formData.BMI} onChange={handleChange} placeholder="e.g. 25.5" required />
          </div>

          <div className="form-group">
            <label htmlFor="DiabetesPedigreeFunction">Pedigree Function (0.01 - 2.5)</label>
            <input className="custom-input" type="number" step="0.001" name="DiabetesPedigreeFunction" value={formData.DiabetesPedigreeFunction} onChange={handleChange} placeholder="e.g. 0.5" required />
          </div>

          <div className="form-group">
            <label htmlFor="Age">Age (Years)</label>
            <input className="custom-input" type="number" step="1" name="Age" value={formData.Age} onChange={handleChange} placeholder="e.g. 35" required />
          </div>
        </div>

        {error && <div style={{ color: '#ff4d4d', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}

        <button className="submit-btn" type="submit" disabled={loading}>
          {loading ? <div className="spinner" /> : 'Run Neural Analysis'}
        </button>
      </form>

      {result && (
        <div className={`result-card ${result.prediction === 1 ? 'positive' : 'negative'}`}>
          <h3>Analysis Result</h3>
          <div className="result-value">
            {result.status}
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '0.5rem' }}>
             Algorithm Confidence: High
          </p>
        </div>
      )}
    </div>
  );
}
