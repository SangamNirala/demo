import React from 'react';
import './RecommendationsCard.css';

const RecommendationsCard = ({ recommendations }) => {
  // Debug: Log recommendations to console
  React.useEffect(() => {
    console.log('📋 Recommendations received:', recommendations);
    if (recommendations && recommendations.length > 0) {
      console.log('📝 First recommendation description:', recommendations[0].description);
    }
  }, [recommendations]);

  // Function to format description with bullet points and bold text
  const formatDescription = (description) => {
    if (!description) return null;
    
    console.log('🔍 Formatting description:', description);
    
    // Split by pipe character or newline
    const lines = description.split(/\s*\|\s*|\n/).filter(line => line.trim());
    
    console.log('📊 Split into lines:', lines);
    
    return (
      <ul className="recommendation-bullets">
        {lines.map((line, idx) => {
          // Remove bullet character if present
          let text = line.replace(/^[•·\-*]\s*/, '').trim();
          
          // Convert **bold** to <strong> tags
          const parts = [];
          let lastIndex = 0;
          const boldRegex = /\*\*([^*]+)\*\*/g;
          let match;
          
          while ((match = boldRegex.exec(text)) !== null) {
            // Add text before bold
            if (match.index > lastIndex) {
              parts.push(text.substring(lastIndex, match.index));
            }
            // Add bold text
            parts.push(<strong key={`bold-${idx}-${match.index}`}>{match[1]}</strong>);
            lastIndex = match.index + match[0].length;
          }
          
          // Add remaining text
          if (lastIndex < text.length) {
            parts.push(text.substring(lastIndex));
          }
          
          return parts.length > 0 ? (
            <li key={idx}>{parts}</li>
          ) : null;
        })}
      </ul>
    );
  };

  return (
    <div className="recommendations-card">
      <div className="recommendations-header">
        <div className="header-icon-wrapper">
          <span className="header-icon">💡</span>
        </div>
        <h2>RECOMMENDED INTERVENTIONS</h2>
      </div>
      <div className="recommendations-content">
        {recommendations && recommendations.length > 0 ? (
          <>
            {recommendations.map((rec, index) => (
              <div key={index} className="recommendation-item" data-testid={`recommendation-item-${index}`}>
                <div className="recommendation-icon">{rec.icon}</div>
                <div className="recommendation-text">
                  <div className="recommendation-title">{rec.title}</div>
                  <div className="recommendation-description">
                    {formatDescription(rec.description)}
                  </div>
                  {rec.priority && (
                    <span className={`priority-badge priority-${rec.priority}`}>
                      {rec.priority.toUpperCase()}
                    </span>
                  )}
                </div>
              </div>
            ))}
            <div className="action-buttons">
              <button className="action-btn" data-testid="mark-contacted-btn">
                <span>✅</span> Mark as Contacted
              </button>
              <button className="action-btn" data-testid="schedule-meeting-btn">
                <span>📅</span> Schedule Meeting
              </button>
              <button className="action-btn" data-testid="assign-mentor-btn">
                <span>👨‍🏫</span> Assign Mentor
              </button>
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
