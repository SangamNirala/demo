import React from 'react';
import './OngoingDataCard.css';

const OngoingDataCard = ({ data }) => {
  // Helper function to determine status level
  const getStatusLevel = (value, thresholds) => {
    if (value <= thresholds.danger) return 'danger';
    if (value <= thresholds.warning) return 'warning';
    return 'good';
  };

  // Calculate CGPA trend
  const cgpaTrend = data.currentCGPA - data.previousCGPA;
  const cgpaTrendDirection = cgpaTrend > 0 ? 'up' : cgpaTrend < 0 ? 'down' : 'stable';

  // Parse assignments (e.g., "4 out of 10")
  const parseAssignments = (str) => {
    const match = str.match(/(\d+)\s*out of\s*(\d+)/i);
    if (match) {
      return { submitted: parseInt(match[1]), total: parseInt(match[2]) };
    }
    return { submitted: 0, total: 10 };
  };

  const assignments = parseAssignments(data.assignmentsSubmitted);
  const assignmentPercentage = (assignments.submitted / assignments.total) * 100;

  // Calculate days since last login
  const calculateDaysSince = (dateStr) => {
    if (dateStr.includes('days ago')) {
      const days = parseInt(dateStr);
      return days;
    }
    return null;
  };

  const daysSinceLogin = calculateDaysSince(data.lastLMSLogin);

  return (
    <div className="ongoing-card">
      {/* Header */}
      <div className="card-header">
        <div className="header-content">
          <div className="header-icon">📊</div>
          <div className="header-text">
            <h2>Ongoing Performance Data</h2>
            <p>Real-time academic and engagement metrics</p>
          </div>
        </div>
        <div className="header-badge">
          <span className="live-indicator"></span>
          Live Data
        </div>
      </div>

      <div className="card-content">
        {/* Academic Performance Section */}
        <div className="data-section">
          <div className="section-header">
            <span className="section-icon">🎓</span>
            <h3>Academic Performance</h3>
          </div>
          
          <div className="metrics-grid">
            {/* Attendance */}
            <div className="metric-card">
              <div className="metric-header">
                <span className="metric-icon">📅</span>
                <span className="metric-label">Attendance</span>
              </div>
              <div className="metric-body">
                <div className={`metric-value ${getStatusLevel(data.attendance, { danger: 50, warning: 75 })}`}>
                  {data.attendance}%
                </div>
                <div className="progress-bar-container">
                  <div 
                    className={`progress-bar ${getStatusLevel(data.attendance, { danger: 50, warning: 75 })}`}
                    style={{ width: `${data.attendance}%` }}
                  ></div>
                </div>
                <span className="metric-subtext">Last 30 days</span>
              </div>
            </div>

            {/* CGPA */}
            <div className="metric-card">
              <div className="metric-header">
                <span className="metric-icon">📈</span>
                <span className="metric-label">Current CGPA</span>
              </div>
              <div className="metric-body">
                <div className="cgpa-display">
                  <span className={`metric-value ${getStatusLevel(data.currentCGPA, { danger: 5, warning: 6.5 })}`}>
                    {data.currentCGPA}
                  </span>
                  <span className={`trend-indicator ${cgpaTrendDirection}`}>
                    {cgpaTrendDirection === 'up' && '↑'}
                    {cgpaTrendDirection === 'down' && '↓'}
                    {cgpaTrendDirection === 'stable' && '→'}
                    <span className="trend-value">
                      {cgpaTrend > 0 ? '+' : ''}{cgpaTrend.toFixed(1)}
                    </span>
                  </span>
                </div>
                <div className="cgpa-comparison">
                  <span className="previous-label">Previous:</span>
                  <span className="previous-value">{data.previousCGPA}</span>
                </div>
              </div>
            </div>

            {/* Assignments */}
            <div className="metric-card">
              <div className="metric-header">
                <span className="metric-icon">📝</span>
                <span className="metric-label">Assignments</span>
              </div>
              <div className="metric-body">
                <div className={`metric-value ${getStatusLevel(assignmentPercentage, { danger: 40, warning: 70 })}`}>
                  {assignments.submitted}/{assignments.total}
                </div>
                <div className="progress-bar-container">
                  <div 
                    className={`progress-bar ${getStatusLevel(assignmentPercentage, { danger: 40, warning: 70 })}`}
                    style={{ width: `${assignmentPercentage}%` }}
                  ></div>
                </div>
                <span className="metric-subtext">Submitted this semester</span>
              </div>
            </div>
          </div>
        </div>

        {/* Engagement Section */}
        <div className="data-section">
          <div className="section-header">
            <span className="section-icon">💡</span>
            <h3>Engagement & Activity</h3>
          </div>
          
          <div className="engagement-grid">
            {/* Library Visits */}
            <div className="engagement-item">
              <div className="engagement-icon-wrapper library">
                <span>📚</span>
              </div>
              <div className="engagement-details">
                <span className="engagement-label">Library Visits</span>
                <span className={`engagement-value ${data.libraryVisits === '0 visits in 2 months' || data.libraryVisits === 0 ? 'warning' : ''}`}>
                  {data.libraryVisits}
                </span>
              </div>
            </div>

            {/* LMS Login */}
            <div className="engagement-item">
              <div className={`engagement-icon-wrapper lms ${daysSinceLogin > 7 ? 'inactive' : ''}`}>
                <span>💻</span>
              </div>
              <div className="engagement-details">
                <span className="engagement-label">Last LMS Login</span>
                <span className={`engagement-value ${daysSinceLogin > 7 ? 'warning' : ''}`}>
                  {data.lastLMSLogin}
                </span>
              </div>
            </div>

            {/* Extracurricular */}
            <div className="engagement-item">
              <div className={`engagement-icon-wrapper extra ${data.extracurricular === 'No participation' ? 'inactive' : ''}`}>
                <span>🏆</span>
              </div>
              <div className="engagement-details">
                <span className="engagement-label">Extracurricular</span>
                <span className={`engagement-value ${data.extracurricular === 'No participation' ? 'warning' : ''}`}>
                  {data.extracurricular}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Financial & Wellbeing Section */}
        <div className="data-section">
          <div className="section-header">
            <span className="section-icon">🛡️</span>
            <h3>Financial & Wellbeing</h3>
          </div>
          
          <div className="status-cards">
            {/* Fee Status */}
            <div className={`status-card ${data.feeStatus === 'Paid' ? 'status-good' : 'status-warning'}`}>
              <div className="status-icon">
                {data.feeStatus === 'Paid' ? '✅' : '⚠️'}
              </div>
              <div className="status-content">
                <span className="status-label">Fee Payment Status</span>
                <span className="status-value">{data.feeStatus}</span>
              </div>
              {data.feeStatus !== 'Paid' && (
                <div className="status-badge urgent">Action Required</div>
              )}
            </div>

            {/* Counselor Visits */}
            <div className={`status-card ${data.counselorVisits && data.counselorVisits !== '0' ? 'status-attention' : 'status-neutral'}`}>
              <div className="status-icon">
                {data.counselorVisits && data.counselorVisits !== '0' ? '🧠' : '😊'}
              </div>
              <div className="status-content">
                <span className="status-label">Counselor Visits</span>
                <span className="status-value">{data.counselorVisits}</span>
              </div>
              {data.counselorVisits && data.counselorVisits !== '0' && (
                <div className="status-badge monitor">Monitor</div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Summary Footer */}
        <div className="card-footer">
          <div className="summary-item">
            <span className="summary-dot danger"></span>
            <span>Critical Areas: 3</span>
          </div>
          <div className="summary-item">
            <span className="summary-dot warning"></span>
            <span>Needs Attention: 2</span>
          </div>
          <div className="summary-item">
            <span className="summary-dot good"></span>
            <span>On Track: 4</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OngoingDataCard;