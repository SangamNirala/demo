import React from 'react';
import './PredictionButton.css';

const PredictionButton = ({ onClick, disabled }) => {
  return (
    <div className="prediction-button-container">
      <button 
        className="prediction-button" 
        onClick={onClick}
        disabled={disabled}
      >
        <span className="button-icon">🎯</span>
        Generate Risk Prediction
      </button>
    </div>
  );
};

export default PredictionButton;
