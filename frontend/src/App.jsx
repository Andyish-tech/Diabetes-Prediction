import React from 'react';
import PredictionForm from './components/PredictionForm';
import './index.css'; // Make sure styles are loaded

function App() {
  return (
    <>
      {/* Background elements */}
      <div className="glow-orb orb-1"></div>
      <div className="glow-orb orb-2"></div>

      <div className="app-container">
        <header className="header">
          <h1>Medical A.I. Diagnostics</h1>
          <p>Advanced Diabetes Prediction System</p>
        </header>

        <main className="dashboard-grid">
          <PredictionForm />
        </main>
      </div>
    </>
  );
}

export default App;
