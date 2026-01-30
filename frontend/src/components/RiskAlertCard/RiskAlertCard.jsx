import React from 'react';
import './RiskAlertCard.css';

const RiskAlertCard = ({ data, studentData }) => {
  const getRiskColor = (level) => {
    if (level === 'HIGH') return '#ef4444';
    if (level === 'MEDIUM') return '#f59e0b';
    return '#10b981';
  };

  const getRiskEmoji = (level) => {
    if (level === 'HIGH') return '🔴';
    if (level === 'MEDIUM') return '🟡';
    return '🟢';
  };

  return (
    <div className="risk-alert-card">
      <div className="alert-header">
        <h2>🚨 STUDENT DROPOUT RISK ALERT</h2>
      </div>
      <div className="alert-content">
        <div className="student-info">
          <p><strong>Student:</strong> {studentData.name} ({studentData.rollNo})</p>
          <p><strong>Course:</strong> {studentData.course} - {studentData.year}</p>
        </div>
        
        <div 
          className="risk-level-box"
          style={{ 
            borderColor: getRiskColor(data.riskLevel),
            background: `${getRiskColor(data.riskLevel)}15`
          }}
        >
          <div className="risk-label">RISK LEVEL</div>
          <div className="risk-value" style={{ color: getRiskColor(data.riskLevel) }}>
            {getRiskEmoji(data.riskLevel)} {data.riskLevel} ({data.riskPercentage}%)
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskAlertCard;
