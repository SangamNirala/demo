import React, { useState, useEffect } from 'react';
import './InterventionTrackerCard.css';
import {
  createIntervention,
  getStudentInterventions,
  updateIntervention,
  deleteIntervention,
  markAsContacted,
  getInterventionStatistics,
} from '../../services/api';

const InterventionTrackerCard = ({ studentData }) => {
  const [interventions, setInterventions] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [editingNote, setEditingNote] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    type: 'meeting',
    status: 'scheduled',
    assigned_to: '',
    scheduled_date: '',
    notes: '',
  });

  // Quick action state
  const [contactedBy, setContactedBy] = useState('');
  const [contactNotes, setContactNotes] = useState('');

  const studentId = studentData?.rollNo || studentData?.roll_no;

  useEffect(() => {
    if (studentId) {
      loadInterventions();
      loadStatistics();
    }
  }, [studentId]);

  const loadInterventions = async () => {
    try {
      setLoading(true);
      const result = await getStudentInterventions(studentId);
      setInterventions(result.interventions || []);
    } catch (err) {
      console.error('Error loading interventions:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const result = await getInterventionStatistics(studentId);
      if (result?.statistics) {
        setStatistics(result.statistics);
      }
    } catch (err) {
      console.error('Error loading statistics:', err);
    }
  };

  const handleCreateIntervention = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!formData.assigned_to.trim()) {
      setError('Please enter who this intervention is assigned to');
      return;
    }

    try {
      setLoading(true);
      const interventionData = {
        student_id: studentId,
        type: formData.type,
        status: formData.status,
        assigned_to: formData.assigned_to,
        scheduled_date: formData.scheduled_date || null,
        notes: formData.notes,
      };

      await createIntervention(interventionData);
      setSuccessMessage('Intervention created successfully!');
      setShowCreateForm(false);
      setFormData({
        type: 'meeting',
        status: 'scheduled',
        assigned_to: '',
        scheduled_date: '',
        notes: '',
      });
      loadInterventions();
      loadStatistics();

      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(err.message || 'Failed to create intervention');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsContacted = async () => {
    if (!contactedBy.trim()) {
      setError('Please enter your name');
      return;
    }

    setError(null);
    setSuccessMessage(null);

    try {
      setLoading(true);
      await markAsContacted(studentId, contactedBy, contactNotes);
      setSuccessMessage('Student marked as contacted!');
      setContactedBy('');
      setContactNotes('');
      loadInterventions();
      loadStatistics();

      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(err.message || 'Failed to mark as contacted');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (interventionId, newStatus) => {
    try {
      setLoading(true);
      await updateIntervention(interventionId, { status: newStatus });
      setSuccessMessage('Status updated successfully!');
      loadInterventions();
      loadStatistics();
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(err.message || 'Failed to update status');
    } finally {
      setLoading(false);
    }
  };

  const handleOutcomeChange = async (interventionId, newOutcome) => {
    try {
      setLoading(true);
      await updateIntervention(interventionId, { outcome: newOutcome });
      setSuccessMessage('Outcome updated successfully!');
      loadInterventions();
      loadStatistics();
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(err.message || 'Failed to update outcome');
    } finally {
      setLoading(false);
    }
  };

  const handleAddNote = async (interventionId, note) => {
    try {
      setLoading(true);
      await updateIntervention(interventionId, { notes: note });
      setSuccessMessage('Note saved successfully!');
      setEditingNote(null);
      loadInterventions();
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(err.message || 'Failed to save note');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteIntervention = async (interventionId) => {
    if (!window.confirm('Are you sure you want to delete this intervention?')) {
      return;
    }

    try {
      setLoading(true);
      await deleteIntervention(interventionId);
      setSuccessMessage('Intervention deleted successfully!');
      loadInterventions();
      loadStatistics();
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError(err.message || 'Failed to delete intervention');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadgeStyle = (status) => {
    const styles = {
      scheduled: { background: '#dbeafe', color: '#1e40af' },
      in_progress: { background: '#fef3c7', color: '#92400e' },
      completed: { background: '#d1fae5', color: '#065f46' },
      cancelled: { background: '#fee2e2', color: '#991b1b' },
    };
    return styles[status] || styles.scheduled;
  };

  const getOutcomeBadgeStyle = (outcome) => {
    const styles = {
      positive: { background: '#d1fae5', color: '#065f46' },
      neutral: { background: '#e5e7eb', color: '#374151' },
      negative: { background: '#fee2e2', color: '#991b1b' },
      pending: { background: '#dbeafe', color: '#1e40af' },
    };
    return styles[outcome] || styles.pending;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getTypeIcon = (type) => {
    const icons = {
      meeting: '🤝',
      counseling: '💬',
      mentor: '👨‍🏫',
      academic_support: '📚',
      financial_aid: '💰',
      attendance_warning: '⚠️',
      other: '📋',
    };
    return icons[type] || '📋';
  };

  return (
    <div className="intervention-tracker-card" data-testid="intervention-tracker-card">
      <div className="card-header">
        <h2 className="card-title">
          <span className="title-icon">📊</span>
          Intervention Tracking
        </h2>
        <p className="card-subtitle">Track actions taken and their outcomes</p>
      </div>

      {/* Messages */}
      {error && (
        <div className="message-box error-message" data-testid="error-message">
          <span className="message-icon">⚠️</span>
          <span>{error}</span>
          <button onClick={() => setError(null)} className="close-btn">×</button>
        </div>
      )}

      {successMessage && (
        <div className="message-box success-message" data-testid="success-message">
          <span className="message-icon">✅</span>
          <span>{successMessage}</span>
        </div>
      )}

      {/* Statistics */}
      {statistics && statistics.total > 0 && (
        <div className="statistics-section" data-testid="statistics-section">
          <h3 className="section-title">📈 Summary</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-value">{statistics.total}</div>
              <div className="stat-label">Total</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{statistics.by_status?.completed || 0}</div>
              <div className="stat-label">Completed</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{statistics.by_status?.scheduled || 0}</div>
              <div className="stat-label">Scheduled</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{statistics.by_outcome?.positive || 0}</div>
              <div className="stat-label">Positive</div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="quick-actions-section" data-testid="quick-actions-section">
        <h3 className="section-title">⚡ Quick Actions</h3>
        <div className="quick-actions-grid">
          <div className="quick-action-card">
            <h4 className="quick-action-title">✓ Mark as Contacted</h4>
            <input
              type="text"
              placeholder="Your name"
              value={contactedBy}
              onChange={(e) => setContactedBy(e.target.value)}
              className="quick-input"
              data-testid="contacted-by-input"
            />
            <textarea
              placeholder="Optional notes..."
              value={contactNotes}
              onChange={(e) => setContactNotes(e.target.value)}
              className="quick-textarea"
              rows="2"
              data-testid="contact-notes-input"
            />
            <button
              onClick={handleMarkAsContacted}
              disabled={loading || !contactedBy.trim()}
              className="action-btn primary-btn"
              data-testid="mark-contacted-btn"
            >
              {loading ? 'Processing...' : 'Mark as Contacted'}
            </button>
          </div>

          <div className="quick-action-card">
            <h4 className="quick-action-title">📅 Schedule New Intervention</h4>
            <button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="action-btn secondary-btn"
              data-testid="schedule-meeting-btn"
            >
              {showCreateForm ? 'Cancel' : 'Schedule Meeting'}
            </button>
          </div>
        </div>
      </div>

      {/* Create Intervention Form */}
      {showCreateForm && (
        <div className="create-form-section" data-testid="create-form-section">
          <h3 className="section-title">📝 Schedule Intervention</h3>
          <form onSubmit={handleCreateIntervention} className="intervention-form">
            <div className="form-group">
              <label className="form-label">Type</label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="form-select"
                data-testid="intervention-type-select"
              >
                <option value="meeting">🤝 Meeting</option>
                <option value="counseling">💬 Counseling</option>
                <option value="mentor">👨‍🏫 Mentor</option>
                <option value="academic_support">📚 Academic Support</option>
                <option value="financial_aid">💰 Financial Aid</option>
                <option value="attendance_warning">⚠️ Attendance Warning</option>
                <option value="other">📋 Other</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="form-select"
                data-testid="intervention-status-select"
              >
                <option value="scheduled">Scheduled</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Assigned To *</label>
              <input
                type="text"
                value={formData.assigned_to}
                onChange={(e) => setFormData({ ...formData, assigned_to: e.target.value })}
                placeholder="Enter name (e.g., Dr. Smith)"
                className="form-input"
                required
                data-testid="assigned-to-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Scheduled Date & Time</label>
              <input
                type="datetime-local"
                value={formData.scheduled_date}
                onChange={(e) => setFormData({ ...formData, scheduled_date: e.target.value })}
                className="form-input"
                data-testid="scheduled-date-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Notes</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                placeholder="Add any relevant notes..."
                className="form-textarea"
                rows="3"
                data-testid="notes-input"
              />
            </div>

            <div className="form-actions">
              <button
                type="submit"
                disabled={loading}
                className="action-btn primary-btn"
                data-testid="create-intervention-btn"
              >
                {loading ? 'Creating...' : 'Create Intervention'}
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="action-btn cancel-btn"
                data-testid="cancel-form-btn"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Interventions History */}
      <div className="history-section" data-testid="history-section">
        <h3 className="section-title">📜 Intervention History</h3>
        
        {loading && interventions.length === 0 ? (
          <div className="loading-state">Loading interventions...</div>
        ) : interventions.length === 0 ? (
          <div className="empty-state" data-testid="empty-state">
            <span className="empty-icon">📭</span>
            <p>No interventions recorded yet</p>
            <p className="empty-subtitle">Schedule a meeting or mark the student as contacted to get started</p>
          </div>
        ) : (
          <div className="interventions-list">
            {interventions.map((intervention) => (
              <div key={intervention.id} className="intervention-item" data-testid="intervention-item">
                <div className="intervention-header">
                  <div className="intervention-title-row">
                    <span className="intervention-icon">{getTypeIcon(intervention.type)}</span>
                    <span className="intervention-type">{intervention.type.replace('_', ' ')}</span>
                    <span
                      className="status-badge"
                      style={getStatusBadgeStyle(intervention.status)}
                      data-testid="status-badge"
                    >
                      {intervention.status.replace('_', ' ')}
                    </span>
                  </div>
                  <button
                    onClick={() => handleDeleteIntervention(intervention.id)}
                    className="delete-btn"
                    title="Delete intervention"
                    data-testid="delete-intervention-btn"
                  >
                    🗑️
                  </button>
                </div>

                <div className="intervention-details">
                  <div className="detail-row">
                    <span className="detail-label">Assigned to:</span>
                    <span className="detail-value">{intervention.assigned_to}</span>
                  </div>
                  {intervention.scheduled_date && (
                    <div className="detail-row">
                      <span className="detail-label">Scheduled:</span>
                      <span className="detail-value">{formatDate(intervention.scheduled_date)}</span>
                    </div>
                  )}
                  {intervention.completed_date && (
                    <div className="detail-row">
                      <span className="detail-label">Completed:</span>
                      <span className="detail-value">{formatDate(intervention.completed_date)}</span>
                    </div>
                  )}
                </div>

                {/* Status Changer */}
                <div className="status-changer">
                  <label className="status-label">Status:</label>
                  <select
                    value={intervention.status}
                    onChange={(e) => handleStatusChange(intervention.id, e.target.value)}
                    className="status-select"
                    data-testid="status-select"
                  >
                    <option value="scheduled">Scheduled</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>

                {/* Outcome Selector */}
                <div className="outcome-selector">
                  <label className="outcome-label">Outcome:</label>
                  <div className="outcome-buttons">
                    {['positive', 'neutral', 'negative', 'pending'].map((outcome) => (
                      <button
                        key={outcome}
                        onClick={() => handleOutcomeChange(intervention.id, outcome)}
                        className={`outcome-btn ${intervention.outcome === outcome ? 'active' : ''}`}
                        style={intervention.outcome === outcome ? getOutcomeBadgeStyle(outcome) : {}}
                        data-testid={`outcome-${outcome}-btn`}
                      >
                        {outcome.charAt(0).toUpperCase() + outcome.slice(1)}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Notes Section */}
                <div className="notes-section">
                  {editingNote === intervention.id ? (
                    <div className="note-editor">
                      <textarea
                        defaultValue={intervention.notes}
                        className="note-textarea"
                        rows="3"
                        id={`note-${intervention.id}`}
                        data-testid="note-textarea"
                      />
                      <div className="note-actions">
                        <button
                          onClick={() => {
                            const note = document.getElementById(`note-${intervention.id}`).value;
                            handleAddNote(intervention.id, note);
                          }}
                          className="save-note-btn"
                          data-testid="save-note-btn"
                        >
                          Save Note
                        </button>
                        <button
                          onClick={() => setEditingNote(null)}
                          className="cancel-note-btn"
                          data-testid="cancel-note-btn"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="note-display">
                      <div className="note-header">
                        <span className="note-label">📝 Notes:</span>
                        <button
                          onClick={() => setEditingNote(intervention.id)}
                          className="edit-note-btn"
                          data-testid="edit-note-btn"
                        >
                          ✏️ Edit
                        </button>
                      </div>
                      <p className="note-text">
                        {intervention.notes || 'No notes added yet'}
                      </p>
                    </div>
                  )}
                </div>

                <div className="intervention-footer">
                  <span className="timestamp">Created: {formatDate(intervention.created_at)}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default InterventionTrackerCard;