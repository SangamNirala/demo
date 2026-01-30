import React from 'react';
import './RecommendationsCard.css';

const RecommendationsCard = ({ recommendations }) => {
  return (
    <div className="recommendations-card">
      <div className="recommendations-header">
        <h2>💡 RECOMMENDED INTERVENTIONS</h2>
      </div>
      <div className="recommendations-content">
        {recommendations && recommendations.length > 0 ? (
          <>
            {recommendations.map((rec, index) => (
              <div key={index} className="recommendation-item" data-testid={`recommendation-item-${index}`}>
                <div className="recommendation-icon">{rec.icon}</div>
                <div className="recommendation-text">
                  <div className="recommendation-title">{rec.title}</div>
                  <div className="recommendation-description">{rec.description}</div>
                  {rec.priority && (
                    <span className={`priority-badge priority-${rec.priority}`}>
                      {rec.priority.toUpperCase()}
                    </span>
                  )}
                </div>
              </div>
            ))}
            <div className="action-buttons">
              <button className="action-btn" data-testid="mark-contacted-btn">Mark as Contacted</button>
              <button className="action-btn" data-testid="schedule-meeting-btn">Schedule Meeting</button>
              <button className="action-btn" data-testid="assign-mentor-btn">Assign Mentor</button>
            </div>
          </>
        ) : (
          <div className="no-recommendations">
            <p>No recommendations available at this time.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationsCard;
