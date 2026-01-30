import React from 'react';
import './RecommendationsCard.css';

const RecommendationsCard = ({ recommendations }) => {
  return (
    <div className="recommendations-card">
      <div className="recommendations-header">
        <h2>💡 RECOMMENDED INTERVENTIONS</h2>
      </div>
      <div className="recommendations-content">
        {recommendations.map((rec, index) => (
          <div key={index} className="recommendation-item">
            <div className="recommendation-icon">{rec.icon}</div>
            <div className="recommendation-text">{rec.text}</div>
          </div>
        ))}
        <div className="action-buttons">
          <button className="action-btn">Mark as Contacted</button>
          <button className="action-btn">Schedule Meeting</button>
          <button className="action-btn">Assign Mentor</button>
        </div>
      </div>
    </div>
  );
};

export default RecommendationsCard;
