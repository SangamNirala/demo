import React, { useState, useEffect } from 'react';
import { getTrendData, getTrendAnalysis } from '../../services/api';
import './TrendAnalysisCard.css';

const TrendAnalysisCard = ({ rollNo, currentRisk }) => {
  const [trendData, setTrendData] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('risk');

  useEffect(() => {
    const fetchTrendData = async () => {
      setLoading(true);
      try {
        const [trends, trendAnalysis] = await Promise.all([
          getTrendData(rollNo),
          getTrendAnalysis(rollNo)
        ]);
        
        if (trends.has_data) {
          setTrendData(trends.data);
        }
        if (trendAnalysis) {
          setAnalysis(trendAnalysis.analysis);
        }
      } catch (error) {
        console.error('Error fetching trend data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (rollNo) {
      fetchTrendData();
    }
  }, [rollNo]);

  if (loading) {
    return (
      <div className="trend-card">
        <div className="trend-card-header">
          <h2>📊 Historical Trend Analysis</h2>
        </div>
        <div className="trend-loading">Loading trend data...</div>
      </div>
    );
  }

  if (!trendData) {
    return (
      <div className="trend-card">
        <div className="trend-card-header">
          <h2>📊 Historical Trend Analysis</h2>
        </div>
        <div className="trend-no-data">
          <span className="no-data-icon">📈</span>
          <p>No historical data available for this student yet.</p>
          <p className="no-data-subtitle">Data will be collected over time to show trends.</p>
        </div>
      </div>
    );
  }

  const renderRiskTimeline = () => {
    const riskHistory = trendData.risk_history || [];
    if (riskHistory.length === 0) return <div className="no-chart-data">No risk data available</div>;

    const maxRisk = Math.max(...riskHistory.map(r => r.risk_percentage), 100);
    
    return (
      <div className="chart-container">
        <div className="chart-header">
          <h3>Risk Score Over Time</h3>
          <div className="trend-indicator">
            {analysis?.risk_trend === 'improving' && <span className="trend-up">📈 Improving</span>}
            {analysis?.risk_trend === 'declining' && <span className="trend-down">📉 Declining</span>}
            {analysis?.risk_trend === 'stable' && <span className="trend-stable">➡️ Stable</span>}
          </div>
        </div>
        <div className="line-chart">
          {riskHistory.map((point, index) => {
            const height = (point.risk_percentage / maxRisk) * 100;
            const isLast = index === riskHistory.length - 1;
            
            return (
              <div key={index} className="chart-point-wrapper">
                <div className="chart-bar-container">
                  <div 
                    className={`chart-bar ${point.risk_level.toLowerCase()}-risk`}
                    style={{ height: `${height}%` }}
                  >
                    {isLast && <span className="current-badge">Current</span>}
                  </div>
                  <span className="chart-value">{point.risk_percentage.toFixed(1)}%</span>
                </div>
                <span className="chart-label">{new Date(point.date).toLocaleDateString('en-US', { month: 'short' })}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderAttendanceTrends = () => {
    const attendanceHistory = trendData.attendance_history || [];
    if (attendanceHistory.length === 0) return <div className="no-chart-data">No attendance data available</div>;

    return (
      <div className="chart-container">
        <div className="chart-header">
          <h3>Attendance Trends</h3>
          <div className="trend-indicator">
            {analysis?.attendance_trend === 'improving' && <span className="trend-up">📈 Improving</span>}
            {analysis?.attendance_trend === 'declining' && <span className="trend-down">📉 Declining</span>}
            {analysis?.attendance_trend === 'stable' && <span className="trend-stable">➡️ Stable</span>}
          </div>
        </div>
        <div className="line-chart">
          {attendanceHistory.map((point, index) => {
            const height = point.percentage;
            const isLast = index === attendanceHistory.length - 1;
            
            return (
              <div key={index} className="chart-point-wrapper">
                <div className="chart-bar-container">
                  <div 
                    className={`chart-bar ${point.percentage >= 75 ? 'good' : point.percentage >= 60 ? 'medium' : 'poor'}`}
                    style={{ height: `${height}%` }}
                  >
                    {isLast && <span className="current-badge">Current</span>}
                  </div>
                  <span className="chart-value">{point.percentage.toFixed(1)}%</span>
                </div>
                <span className="chart-label">{new Date(point.date).toLocaleDateString('en-US', { month: 'short' })}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderCGPATrajectory = () => {
    const cgpaHistory = trendData.cgpa_history || [];
    if (cgpaHistory.length === 0) return <div className="no-chart-data">No CGPA data available</div>;

    const maxCGPA = 10;
    
    return (
      <div className="chart-container">
        <div className="chart-header">
          <h3>CGPA Trajectory</h3>
          <div className="trend-indicator">
            {analysis?.cgpa_trend === 'improving' && <span className="trend-up">📈 Improving</span>}
            {analysis?.cgpa_trend === 'declining' && <span className="trend-down">📉 Declining</span>}
            {analysis?.cgpa_trend === 'stable' && <span className="trend-stable">➡️ Stable</span>}
          </div>
        </div>
        <div className="line-chart">
          {cgpaHistory.map((point, index) => {
            const height = (point.cgpa / maxCGPA) * 100;
            const isLast = index === cgpaHistory.length - 1;
            
            return (
              <div key={index} className="chart-point-wrapper">
                <div className="chart-bar-container">
                  <div 
                    className={`chart-bar ${point.cgpa >= 7 ? 'good' : point.cgpa >= 6 ? 'medium' : 'poor'}`}
                    style={{ height: `${height}%` }}
                  >
                    {isLast && <span className="current-badge">Current</span>}
                  </div>
                  <span className="chart-value">{point.cgpa.toFixed(1)}</span>
                </div>
                <span className="chart-label">{point.semester}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderInterventions = () => {
    const interventions = trendData.interventions || [];
    
    if (interventions.length === 0) {
      return (
        <div className="no-interventions">
          <span className="no-data-icon">📋</span>
          <p>No interventions recorded yet</p>
        </div>
      );
    }

    return (
      <div className="interventions-container">
        <h3>Intervention Timeline</h3>
        <div className="interventions-list">
          {interventions.map((intervention, index) => (
            <div key={index} className={`intervention-item ${intervention.impact}`}>
              <div className="intervention-header">
                <span className="intervention-icon">
                  {intervention.impact === 'positive' && '✅'}
                  {intervention.impact === 'neutral' && '⚪'}
                  {intervention.impact === 'negative' && '⚠️'}
                </span>
                <span className="intervention-type">{intervention.type}</span>
                <span className="intervention-date">
                  {new Date(intervention.date).toLocaleDateString()}
                </span>
              </div>
              <p className="intervention-description">{intervention.description}</p>
              <span className={`intervention-impact ${intervention.impact}`}>
                Impact: {intervention.impact}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="trend-card">
      <div className="trend-card-header">
        <h2>📊 Historical Trend Analysis</h2>
        <p className="trend-subtitle">Track student progress over time</p>
      </div>

      <div className="trend-tabs">
        <button 
          className={`trend-tab ${activeTab === 'risk' ? 'active' : ''}`}
          onClick={() => setActiveTab('risk')}
        >
          📉 Risk Score
        </button>
        <button 
          className={`trend-tab ${activeTab === 'attendance' ? 'active' : ''}`}
          onClick={() => setActiveTab('attendance')}
        >
          📅 Attendance
        </button>
        <button 
          className={`trend-tab ${activeTab === 'cgpa' ? 'active' : ''}`}
          onClick={() => setActiveTab('cgpa')}
        >
          📚 CGPA
        </button>
        <button 
          className={`trend-tab ${activeTab === 'interventions' ? 'active' : ''}`}
          onClick={() => setActiveTab('interventions')}
        >
          🎯 Interventions
        </button>
      </div>

      <div className="trend-content">
        {activeTab === 'risk' && renderRiskTimeline()}
        {activeTab === 'attendance' && renderAttendanceTrends()}
        {activeTab === 'cgpa' && renderCGPATrajectory()}
        {activeTab === 'interventions' && renderInterventions()}
      </div>

      {analysis && (
        <div className="trend-summary">
          <h3>Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-label">Risk Trend</span>
              <span className={`summary-value ${analysis.risk_trend}`}>
                {analysis.risk_trend.replace('_', ' ')}
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Attendance Trend</span>
              <span className={`summary-value ${analysis.attendance_trend}`}>
                {analysis.attendance_trend.replace('_', ' ')}
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">CGPA Trend</span>
              <span className={`summary-value ${analysis.cgpa_trend}`}>
                {analysis.cgpa_trend.replace('_', ' ')}
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Total Interventions</span>
              <span className="summary-value">{analysis.intervention_count}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TrendAnalysisCard;
