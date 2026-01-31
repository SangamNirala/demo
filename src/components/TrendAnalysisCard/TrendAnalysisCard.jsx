import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import './TrendAnalysisCard.css';

const TrendAnalysisCard = ({ rollNo }) => {
  const [historyData, setHistoryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('risk');

  useEffect(() => {
    if (rollNo) {
      fetchHistory();
    }
  }, [rollNo]);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8001/api/student/${rollNo}/history`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }

      const data = await response.json();
      setHistoryData(data);
    } catch (err) {
      console.error('Error fetching history:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="trend-analysis-card">
        <div className="trend-header">
          <h2>📈 Historical Trend Analysis</h2>
        </div>
        <div className="trend-loading">
          <div className="spinner"></div>
          <p>Loading historical data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="trend-analysis-card">
        <div className="trend-header">
          <h2>📈 Historical Trend Analysis</h2>
        </div>
        <div className="trend-error">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!historyData) {
    return null;
  }

  const { risk_scores, attendance, cgpa, interventions, comparison } = historyData;

  // Custom tooltip for charts
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="label">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {entry.name}: {entry.value}
              {entry.name.includes('Risk') && '%'}
              {entry.name.includes('Attendance') && '%'}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="trend-analysis-card">
      <div className="trend-header">
        <h2>📈 Historical Trend Analysis</h2>
        <p className="trend-subtitle">Track progress over time</p>
      </div>

      {/* Comparison Summary */}
      <div className="comparison-summary">
        <div className="comparison-item">
          <div className="comparison-label">Risk Score</div>
          <div className="comparison-values">
            <span className="initial-value">{comparison.risk.initial}%</span>
            <span className={`arrow ${comparison.risk.trend}`}>
              {comparison.risk.trend === 'improving' ? '↓' : '↑'}
            </span>
            <span className="current-value">{comparison.risk.current}%</span>
          </div>
          <div className={`comparison-change ${comparison.risk.trend}`}>
            {comparison.risk.change > 0 ? '+' : ''}{comparison.risk.change}% 
            ({comparison.risk.trend})
          </div>
        </div>

        <div className="comparison-item">
          <div className="comparison-label">Attendance</div>
          <div className="comparison-values">
            <span className="initial-value">{comparison.attendance.initial}%</span>
            <span className={`arrow ${comparison.attendance.trend}`}>
              {comparison.attendance.trend === 'improving' ? '↑' : '↓'}
            </span>
            <span className="current-value">{comparison.attendance.current}%</span>
          </div>
          <div className={`comparison-change ${comparison.attendance.trend}`}>
            {comparison.attendance.change > 0 ? '+' : ''}{comparison.attendance.change}% 
            ({comparison.attendance.trend})
          </div>
        </div>

        <div className="comparison-item">
          <div className="comparison-label">CGPA</div>
          <div className="comparison-values">
            <span className="initial-value">{comparison.cgpa.initial}</span>
            <span className={`arrow ${comparison.cgpa.trend}`}>
              {comparison.cgpa.trend === 'improving' ? '↑' : '↓'}
            </span>
            <span className="current-value">{comparison.cgpa.current}</span>
          </div>
          <div className={`comparison-change ${comparison.cgpa.trend}`}>
            {comparison.cgpa.change > 0 ? '+' : ''}{comparison.cgpa.change} 
            ({comparison.cgpa.trend})
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="trend-tabs">
        <button
          className={`tab-button ${activeTab === 'risk' ? 'active' : ''}`}
          onClick={() => setActiveTab('risk')}
        >
          🎯 Risk Score
        </button>
        <button
          className={`tab-button ${activeTab === 'attendance' ? 'active' : ''}`}
          onClick={() => setActiveTab('attendance')}
        >
          📅 Attendance
        </button>
        <button
          className={`tab-button ${activeTab === 'cgpa' ? 'active' : ''}`}
          onClick={() => setActiveTab('cgpa')}
        >
          📚 CGPA
        </button>
        <button
          className={`tab-button ${activeTab === 'interventions' ? 'active' : ''}`}
          onClick={() => setActiveTab('interventions')}
        >
          💡 Interventions
        </button>
      </div>

      {/* Chart Content */}
      <div className="trend-content">
        {activeTab === 'risk' && (
          <div className="chart-container">
            <h3>Risk Score Timeline (Last 6 Months)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={risk_scores}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="risk_percentage"
                  name="Risk Score"
                  stroke="#ef4444"
                  strokeWidth={3}
                  dot={{ fill: '#ef4444', r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
            <div className="chart-insight">
              <span className="insight-icon">💡</span>
              <p>
                {comparison.risk.trend === 'improving'
                  ? `Risk has decreased by ${Math.abs(comparison.risk.change)}% over the past 6 months. Keep up the interventions!`
                  : `Risk has increased by ${Math.abs(comparison.risk.change)}% over the past 6 months. Immediate action needed.`}
              </p>
            </div>
          </div>
        )}

        {activeTab === 'attendance' && (
          <div className="chart-container">
            <h3>Attendance Trend (Last 6 Months)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={attendance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="attendance_percentage"
                  name="Attendance"
                  stroke="#3b82f6"
                  strokeWidth={3}
                  dot={{ fill: '#3b82f6', r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
            <div className="chart-insight">
              <span className="insight-icon">💡</span>
              <p>
                {comparison.attendance.trend === 'improving'
                  ? `Attendance has improved by ${Math.abs(comparison.attendance.change)}%. Great progress!`
                  : `Attendance has declined by ${Math.abs(comparison.attendance.change)}%. Consider attendance interventions.`}
              </p>
            </div>
          </div>
        )}

        {activeTab === 'cgpa' && (
          <div className="chart-container">
            <h3>CGPA Progression (Last 4 Semesters)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={cgpa}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="semester" />
                <YAxis domain={[0, 10]} />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Bar
                  dataKey="cgpa"
                  name="CGPA"
                  fill="#10b981"
                  radius={[8, 8, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
            <div className="chart-insight">
              <span className="insight-icon">💡</span>
              <p>
                {comparison.cgpa.trend === 'improving'
                  ? `CGPA has improved by ${Math.abs(comparison.cgpa.change)} points. Academic performance is on track!`
                  : `CGPA has declined by ${Math.abs(comparison.cgpa.change)} points. Academic support recommended.`}
              </p>
            </div>
          </div>
        )}

        {activeTab === 'interventions' && (
          <div className="interventions-container">
            <h3>Intervention Timeline</h3>
            {interventions.length > 0 ? (
              <div className="interventions-timeline">
                {interventions.map((intervention, index) => (
                  <div key={index} className="intervention-item">
                    <div className="intervention-date">
                      {new Date(intervention.date).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </div>
                    <div className="intervention-content">
                      <div className="intervention-header">
                        <span className="intervention-icon">{intervention.icon}</span>
                        <span className="intervention-type">{intervention.type}</span>
                        <span className={`intervention-status status-${intervention.status}`}>
                          {intervention.status.replace('_', ' ')}
                        </span>
                      </div>
                      <div className="intervention-description">
                        {intervention.description}
                      </div>
                      {intervention.outcome && (
                        <div className={`intervention-outcome outcome-${intervention.outcome}`}>
                          Outcome: {intervention.outcome}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-interventions">
                <p>No interventions recorded yet.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TrendAnalysisCard;
