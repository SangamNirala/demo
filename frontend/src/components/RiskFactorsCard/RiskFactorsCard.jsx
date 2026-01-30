import React from 'react';
import './RiskFactorsCard.css';

const RiskFactorsCard = ({ factors }) => {
  return (
    <div className="risk-factors-card">
      <div className="factors-header">
        <h2>📊 Risk Factors Identified</h2>
      </div>
      <div className="factors-content">
        {factors.map((factor, index) => (
          <div key={index} className="factor-item">
            <div className="factor-info">
              <span className="factor-name">{factor.name}</span>
              <span className="factor-percentage">{factor.contribution}% contribution</span>
            </div>
            <div className="factor-bar-container">
              <div 
                className="factor-bar"
                style={{ width: `${factor.contribution}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RiskFactorsCard;
