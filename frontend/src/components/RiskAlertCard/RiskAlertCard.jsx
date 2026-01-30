import './RiskAlertCard.css';

const RiskAlertCard = ({ data, studentData }) => {
  const getRiskLevel = (level) => {
    if (level === 'HIGH') return 'danger';
    if (level === 'MEDIUM') return 'warning';
    return 'good';
  };

  const getRiskText = (level) => {
    if (level === 'HIGH') return 'High Risk';
    if (level === 'MEDIUM') return 'Medium Risk';
    return 'Low Risk';
  };

  const getRiskDescription = (level) => {
    if (level === 'HIGH') return 'Immediate intervention required';
    if (level === 'MEDIUM') return 'Monitor closely and provide support';
    return 'Student performing well';
  };

  const riskLevelClass = getRiskLevel(data.riskLevel);
  const riskPercentage = parseFloat(data.riskPercentage) || 0;

  return (
    <div className="risk-alert-card">
      {/* Decorative Background Pattern */}
      <div className="card-pattern"></div>
      
      {/* Header */}
      <div className="card-header">
        <div className="header-glow"></div>
        <div className="header-glow-secondary"></div>
        <div className="header-content">
          <div className="header-icon-container">
            <div className="header-icon-ring"></div>
            <div className="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
          </div>
          <div className="header-text">
            <span className="header-eyebrow">Risk Assessment</span>
            <h2>Student Dropout Risk Alert</h2>
            <p>AI-powered risk analysis and recommendations</p>
          </div>
        </div>
        <div className={`header-badge ${riskLevelClass}`}>
          <span className="risk-indicator"></span>
          <span className="risk-ring"></span>
          Alert Active
        </div>
      </div>

      <div className="card-content">
        {/* Student Information Section */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper student">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <h3>Student Information</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="student-info-grid">
            <div className="info-card">
              <div className="info-card-glow"></div>
              <div className="info-header">
                <div className="info-icon-wrapper name">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </div>
                <span className="info-label">Student Name</span>
              </div>
              <div className="info-body">
                <div className="info-value">{studentData.name}</div>
                <div className="info-subtext">Roll No: {studentData.rollNo}</div>
              </div>
            </div>

            <div className="info-card">
              <div className="info-card-glow"></div>
              <div className="info-header">
                <div className="info-icon-wrapper course">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                  </svg>
                </div>
                <span className="info-label">Academic Program</span>
              </div>
              <div className="info-body">
                <div className="info-value">{studentData.course}</div>
                <div className="info-subtext">Year {studentData.year}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="section-divider">
          <span className="divider-accent"></span>
        </div>

        {/* Risk Assessment Section */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper risk">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <h3>Risk Assessment</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="risk-assessment-container">
            <div className={`risk-level-card ${riskLevelClass}`}>
              <div className="risk-card-glow"></div>
              <div className="risk-header">
                <div className={`risk-icon-wrapper ${riskLevelClass}`}>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </div>
                <div className="risk-info">
                  <span className="risk-label">Dropout Risk Level</span>
                  <div className={`risk-status-badge ${riskLevelClass}`}>
                    {getRiskText(data.riskLevel)}
                  </div>
                </div>
              </div>
              
              <div className="risk-body">
                <div className="risk-percentage-container">
                  <div className={`risk-percentage ${riskLevelClass}`}>
                    {riskPercentage}<span className="percentage-unit">%</span>
                  </div>
                  <div className="risk-description">
                    {getRiskDescription(data.riskLevel)}
                  </div>
                </div>
                
                <div className="risk-progress-container">
                  <div className="risk-progress-bar-container">
                    <div className="risk-progress-bar-bg"></div>
                    <div 
                      className={`risk-progress-bar ${riskLevelClass}`}
                      style={{ width: `${riskPercentage}%` }}
                    >
                      <div className="risk-progress-bar-shine"></div>
                    </div>
                  </div>
                  <div className="risk-progress-labels">
                    <span className="progress-label-start">Low Risk</span>
                    <span className="progress-label-end">High Risk</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="section-divider">
          <span className="divider-accent"></span>
        </div>

        {/* Action Required Section */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper action">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <h3>Recommended Actions</h3>
            <div className="section-line"></div>
          </div>
          
          <div className={`action-card ${riskLevelClass}`}>
            <div className="action-card-accent"></div>
            <div className="action-icon-wrapper">
              {data.riskLevel === 'HIGH' ? (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
              ) : data.riskLevel === 'MEDIUM' ? (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              ) : (
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
              )}
            </div>
            <div className="action-content">
              <span className="action-label">Priority Level</span>
              <span className="action-value">
                {data.riskLevel === 'HIGH' ? 'Immediate Action Required' : 
                 data.riskLevel === 'MEDIUM' ? 'Monitor and Support' : 
                 'Continue Current Support'}
              </span>
            </div>
            {data.riskLevel !== 'LOW' && (
              <div className={`action-badge ${riskLevelClass}`}>
                {data.riskLevel === 'HIGH' ? 'Urgent' : 'Monitor'}
              </div>
            )}
          </div>
        </div>

        {/* Summary Footer */}
        <div className="card-footer">
          <div className="footer-title">Risk Assessment Summary</div>
          <div className="summary-items">
            <div className={`summary-item ${riskLevelClass}`}>
              <span className="summary-dot">
                <span className="dot-ring"></span>
              </span>
              <span className="summary-count">{Math.round(riskPercentage)}%</span>
              <span className="summary-text">Risk Score</span>
            </div>
            <div className="summary-item neutral">
              <span className="summary-dot">
                <span className="dot-ring"></span>
              </span>
              <span className="summary-count">AI</span>
              <span className="summary-text">Powered</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Accent */}
      <div className="card-footer-accent"></div>
    </div>
  );
};

export default RiskAlertCard;