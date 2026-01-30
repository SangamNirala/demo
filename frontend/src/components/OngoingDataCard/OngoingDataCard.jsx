import './OngoingDataCard.css';

const OngoingDataCard = ({ data }) => {
  const getStatusLevel = (value, thresholds) => {
    if (value <= thresholds.danger) return 'danger';
    if (value <= thresholds.warning) return 'warning';
    return 'good';
  };

  const getStatusText = (value, thresholds) => {
    if (value <= thresholds.danger) return 'Critical';
    if (value <= thresholds.warning) return 'Low';
    return 'Good';
  };

  const cgpaTrend = data.currentCGPA - data.previousCGPA;
  const cgpaTrendDirection = cgpaTrend > 0 ? 'up' : cgpaTrend < 0 ? 'down' : 'stable';

  const parseAssignments = (str) => {
    const match = str.match(/(\d+)\s*out of\s*(\d+)/i);
    if (match) {
      return { submitted: parseInt(match[1]), total: parseInt(match[2]) };
    }
    return { submitted: 0, total: 10 };
  };

  const assignments = parseAssignments(data.assignmentsSubmitted);
  const assignmentPercentage = (assignments.submitted / assignments.total) * 100;

  const calculateDaysSince = (dateStr) => {
    if (dateStr.includes('days ago')) {
      return parseInt(dateStr);
    }
    return null;
  };

  const daysSinceLogin = calculateDaysSince(data.lastLMSLogin);

  return (
    <div className="ongoing-card">
      {/* Decorative Background Pattern */}
      <div className="card-pattern"></div>
      
      {/* Header */}
      <div className="card-header">
        <div className="header-glow"></div>
        <div className="header-content">
          <div className="header-icon-container">
            <div className="header-icon-ring"></div>
            <div className="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 3v18h18"/>
                <path d="M18 17V9"/>
                <path d="M13 17V5"/>
                <path d="M8 17v-3"/>
              </svg>
            </div>
          </div>
          <div className="header-text">
            <span className="header-eyebrow">Analytics Dashboard</span>
            <h2>Ongoing Performance Data</h2>
            <p>Real-time academic and engagement metrics</p>
          </div>
        </div>
        <div className="header-badge">
          <span className="live-indicator"></span>
          <span className="live-ring"></span>
          Live Data
        </div>
      </div>

      <div className="card-content">
        {/* Academic Performance Section */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper academic">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                <path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/>
              </svg>
            </div>
            <h3>Academic Performance</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="metrics-grid">
            {/* Attendance */}
            <div className="metric-card">
              <div className="metric-header">
                <div className="metric-icon-wrapper attendance">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                </div>
                <div className="metric-info">
                  <span className="metric-label">Attendance Rate</span>
                  <div className={`status-badge ${getStatusLevel(data.attendance, { danger: 50, warning: 75 })}`}>
                    {getStatusText(data.attendance, { danger: 50, warning: 75 })}
                  </div>
                </div>
              </div>
              <div className="metric-body">
                <div className={`metric-value ${getStatusLevel(data.attendance, { danger: 50, warning: 75 })}`}>
                  {data.attendance}<span className="metric-unit">%</span>
                </div>
                <div className="progress-bar-container">
                  <div className="progress-bar-bg"></div>
                  <div 
                    className={`progress-bar ${getStatusLevel(data.attendance, { danger: 50, warning: 75 })}`}
                    style={{ width: `${data.attendance}%` }}
                  >
                    <div className="progress-bar-shine"></div>
                  </div>
                </div>
                <span className="metric-subtext">Last 30 days</span>
              </div>
            </div>

            {/* CGPA */}
            <div className="metric-card">
              <div className="metric-header">
                <div className="metric-icon-wrapper cgpa">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                    <polyline points="17 6 23 6 23 12"/>
                  </svg>
                </div>
                <div className="metric-info">
                  <span className="metric-label">Current CGPA</span>
                  <div className={`trend-indicator ${cgpaTrendDirection}`}>
                    <span className="trend-arrow">
                      {cgpaTrendDirection === 'up' && '↗'}
                      {cgpaTrendDirection === 'down' && '↘'}
                      {cgpaTrendDirection === 'stable' && '→'}
                    </span>
                    <span className="trend-value">
                      {cgpaTrend > 0 ? '+' : ''}{cgpaTrend.toFixed(1)}
                    </span>
                  </div>
                </div>
              </div>
              <div className="metric-body">
                <div className={`metric-value large ${getStatusLevel(data.currentCGPA, { danger: 5, warning: 6.5 })}`}>
                  {data.currentCGPA}
                </div>
                <div className="cgpa-details">
                  <span className="comparison-text">Previous: {data.previousCGPA}</span>
                  <span className="scale-text">Scale: 10.0</span>
                </div>
              </div>
            </div>

            {/* Assignments */}
            <div className="metric-card">
              <div className="metric-header">
                <div className="metric-icon-wrapper assignments">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                  </svg>
                </div>
                <div className="metric-info">
                  <span className="metric-label">Assignments</span>
                  <div className={`completion-badge ${getStatusLevel(assignmentPercentage, { danger: 40, warning: 70 })}`}>
                    {Math.round(assignmentPercentage)}% Complete
                  </div>
                </div>
              </div>
              <div className="metric-body">
                <div className={`metric-value fraction ${getStatusLevel(assignmentPercentage, { danger: 40, warning: 70 })}`}>
                  <span className="numerator">{assignments.submitted}</span>
                  <span className="separator">/</span>
                  <span className="denominator">{assignments.total}</span>
                </div>
                <div className="progress-bar-container">
                  <div className="progress-bar-bg"></div>
                  <div 
                    className={`progress-bar ${getStatusLevel(assignmentPercentage, { danger: 40, warning: 70 })}`}
                    style={{ width: `${assignmentPercentage}%` }}
                  >
                    <div className="progress-bar-shine"></div>
                  </div>
                </div>
                <span className="metric-subtext">This semester</span>
              </div>
            </div>
          </div>
        </div>

        <div className="section-divider">
          <span className="divider-accent"></span>
        </div>

        {/* Engagement & Activity Section */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper engagement">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                <line x1="9" y1="9" x2="9.01" y2="9"/>
                <line x1="15" y1="9" x2="15.01" y2="9"/>
              </svg>
            </div>
            <h3>Engagement & Activity</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="engagement-grid">
            {/* Library Visits */}
            <div className="engagement-card">
              <div className="engagement-header">
                <div className="engagement-icon-wrapper library">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                  </svg>
                </div>
                <div className="engagement-status">
                  <span className={`status-dot ${data.libraryVisits === '0 visits in 2 months' || data.libraryVisits === 0 || data.libraryVisits === '0' ? 'warning' : 'good'}`}></span>
                </div>
              </div>
              <div className="engagement-body">
                <span className="engagement-label">Library Visits</span>
                <span className={`engagement-value ${data.libraryVisits === '0 visits in 2 months' || data.libraryVisits === 0 || data.libraryVisits === '0' ? 'warning' : 'good'}`}>
                  {data.libraryVisits}
                </span>
                <span className="engagement-subtext">Recent activity</span>
              </div>
            </div>

            {/* LMS Login */}
            <div className="engagement-card">
              <div className="engagement-header">
                <div className={`engagement-icon-wrapper lms ${daysSinceLogin > 7 ? 'inactive' : 'active'}`}>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                    <line x1="8" y1="21" x2="16" y2="21"/>
                    <line x1="12" y1="17" x2="12" y2="21"/>
                  </svg>
                </div>
                <div className="engagement-status">
                  <span className={`status-dot ${daysSinceLogin > 7 ? 'warning' : 'good'}`}></span>
                </div>
              </div>
              <div className="engagement-body">
                <span className="engagement-label">Last LMS Login</span>
                <span className={`engagement-value ${daysSinceLogin > 7 ? 'warning' : 'good'}`}>
                  {data.lastLMSLogin}
                </span>
                <span className="engagement-subtext">
                  {daysSinceLogin > 7 ? 'Recently active' : 'Recently active'}
                </span>
              </div>
            </div>

            {/* Extracurricular */}
            <div className="engagement-card">
              <div className="engagement-header">
                <div className={`engagement-icon-wrapper extra ${data.extracurricular === 'No participation' || data.extracurricular === 'None' ? 'inactive' : 'active'}`}>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="8" r="6"/>
                    <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>
                  </svg>
                </div>
                <div className="engagement-status">
                  <span className={`status-dot ${data.extracurricular === 'No participation' || data.extracurricular === 'None' ? 'warning' : 'good'}`}></span>
                </div>
              </div>
              <div className="engagement-body">
                <span className="engagement-label">Extracurricular</span>
                <span className={`engagement-value ${data.extracurricular === 'No participation' || data.extracurricular === 'None' ? 'warning' : 'good'}`}>
                  {data.extracurricular}
                </span>
                <span className="engagement-subtext">
                  {data.extracurricular === 'No participation' || data.extracurricular === 'None' ? 'Active participation' : 'Active participation'}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="section-divider">
          <span className="divider-accent"></span>
        </div>

        {/* Financial & Wellbeing Section */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper financial">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <h3>Financial & Wellbeing</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="status-cards">
            {/* Fee Status */}
            <div className={`status-card ${data.feeStatus === 'Paid' ? 'status-good' : 'status-warning'}`}>
              <div className="status-card-accent"></div>
              <div className="status-icon-wrapper">
                {data.feeStatus === 'Paid' ? (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                  </svg>
                ) : (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                )}
              </div>
              <div className="status-content">
                <span className="status-label">Fee Payment Status</span>
                <span className="status-value">{data.feeStatus}</span>
              </div>
              {data.feeStatus !== 'Paid' && (
                <div className="status-badge urgent">
                  Action Required
                </div>
              )}
            </div>

            {/* Counselor Visits */}
            <div className={`status-card ${data.counselorVisits && data.counselorVisits !== '0' ? 'status-attention' : 'status-neutral'}`}>
              <div className="status-card-accent"></div>
              <div className="status-icon-wrapper">
                {data.counselorVisits && data.counselorVisits !== '0' ? (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                  </svg>
                ) : (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                    <line x1="9" y1="9" x2="9.01" y2="9"/>
                    <line x1="15" y1="9" x2="15.01" y2="9"/>
                  </svg>
                )}
              </div>
              <div className="status-content">
                <span className="status-label">Counselor Visits</span>
                <span className="status-value">{data.counselorVisits}</span>
              </div>
              {data.counselorVisits && data.counselorVisits !== '0' && (
                <div className="status-badge monitor">
                  Monitor
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Summary Footer */}
        <div className="card-footer">
          <div className="footer-title">Performance Overview</div>
          <div className="summary-items">
            <div className="summary-item danger">
              <span className="summary-dot"></span>
              <span className="summary-count">1</span>
              <span className="summary-text">Critical</span>
            </div>
            <div className="summary-item warning">
              <span className="summary-dot"></span>
              <span className="summary-count">2</span>
              <span className="summary-text">Attention</span>
            </div>
            <div className="summary-item good">
              <span className="summary-dot"></span>
              <span className="summary-count">6</span>
              <span className="summary-text">On Track</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Accent */}
      <div className="card-footer-accent"></div>
    </div>
  );
};

export default OngoingDataCard;