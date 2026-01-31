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
      {/* Header */}
      <div className="card-header-simple">
        <div className="header-icon-simple">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <h3>Risk Assessment</h3>
      </div>

      {/* Risk Assessment Content */}
      <div className="risk-content">
        <div className={`risk-level-card ${riskLevelClass}`}>
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
  );
};

export default RiskAlertCard;
