import React, { useState } from 'react';
import './EmailGeneratorCard.css';

const EmailGeneratorCard = ({ studentData, predictionData }) => {
  const [emailType, setEmailType] = useState('student');
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [meetingDate, setMeetingDate] = useState('');
  const [meetingTime, setMeetingTime] = useState('');
  const [meetingLocation, setMeetingLocation] = useState('');
  const [generatedEmail, setGeneratedEmail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [editableSubject, setEditableSubject] = useState('');
  const [editableBody, setEditableBody] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setGeneratedEmail(null);

    // Validate meeting details if meeting type
    if (emailType === 'meeting') {
      if (!meetingDate || !meetingTime || !meetingLocation) {
        setError('Please fill in all meeting details (date, time, and location)');
        setLoading(false);
        return;
      }
    }

    try {
      const payload = {
        emailType,
        studentData,
        predictionData,
        additionalNotes: additionalNotes.trim() || null,
      };

      if (emailType === 'meeting') {
        payload.meetingDetails = {
          date: meetingDate,
          time: meetingTime,
          location: meetingLocation,
        };
      }

      const response = await fetch('http://localhost:8001/api/email/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate email');
      }

      if (data.success && data.email) {
        setGeneratedEmail(data.email);
        setEditableSubject(data.email.subject);
        setEditableBody(data.email.body);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (err) {
      setError(err.message || 'Failed to generate email');
    } finally {
      setLoading(false);
    }
  };

  const handleCopyToClipboard = () => {
    const emailText = `Subject: ${editableSubject}\n\n${editableBody}`;
    navigator.clipboard.writeText(emailText).then(() => {
      alert('Email copied to clipboard!');
    });
  };

  const handleOpenInMailApp = () => {
    const mailtoLink = `mailto:?subject=${encodeURIComponent(editableSubject)}&body=${encodeURIComponent(editableBody)}`;
    window.location.href = mailtoLink;
  };

  const handleRegenerate = () => {
    setGeneratedEmail(null);
    handleGenerate();
  };

  return (
    <div className="email-generator-card">
      <div className="email-generator-header">
        <div className="header-icon-wrapper">
          <span className="header-icon">✉️</span>
        </div>
        <div className="header-text">
          <h2>Generate Personalized Email</h2>
          <p>✨ Create AI-powered emails for student outreach</p>
        </div>
      </div>

      <div className="email-generator-content">
        {/* Email Type Selection */}
        <div className="form-section">
          <label className="form-label">Email Type</label>
          <div className="email-type-options">
            <label className={`email-type-option ${emailType === 'student' ? 'active' : ''}`}>
              <input
                type="radio"
                name="emailType"
                value="student"
                checked={emailType === 'student'}
                onChange={(e) => setEmailType(e.target.value)}
              />
              <div className="option-content">
                <span className="option-icon">🎓</span>
                <span className="option-label">To Student</span>
                <span className="option-desc">💙 Warm & supportive</span>
              </div>
            </label>

            <label className={`email-type-option ${emailType === 'parent' ? 'active' : ''}`}>
              <input
                type="radio"
                name="emailType"
                value="parent"
                checked={emailType === 'parent'}
                onChange={(e) => setEmailType(e.target.value)}
              />
              <div className="option-content">
                <span className="option-icon">👪</span>
                <span className="option-label">To Parents</span>
                <span className="option-desc">🤝 Formal & professional</span>
              </div>
            </label>

            <label className={`email-type-option ${emailType === 'meeting' ? 'active' : ''}`}>
              <input
                type="radio"
                name="emailType"
                value="meeting"
                checked={emailType === 'meeting'}
                onChange={(e) => setEmailType(e.target.value)}
              />
              <div className="option-content">
                <span className="option-icon">📅</span>
                <span className="option-label">Meeting Invite</span>
                <span className="option-desc">☕ Friendly check-in</span>
              </div>
            </label>
          </div>
        </div>

        {/* Additional Notes */}
        <div className="form-section">
          <label className="form-label" htmlFor="additionalNotes">
            Additional Notes (Optional)
          </label>
          <textarea
            id="additionalNotes"
            className="form-textarea"
            placeholder="Add any specific context or points you'd like to include..."
            value={additionalNotes}
            onChange={(e) => setAdditionalNotes(e.target.value)}
            rows={3}
          />
        </div>

        {/* Meeting Details (only for meeting type) */}
        {emailType === 'meeting' && (
          <div className="form-section meeting-details">
            <label className="form-label">Meeting Details</label>
            <div className="meeting-fields">
              <div className="meeting-field">
                <label htmlFor="meetingDate">Date</label>
                <input
                  type="date"
                  id="meetingDate"
                  className="form-input"
                  value={meetingDate}
                  onChange={(e) => setMeetingDate(e.target.value)}
                />
              </div>
              <div className="meeting-field">
                <label htmlFor="meetingTime">Time</label>
                <input
                  type="time"
                  id="meetingTime"
                  className="form-input"
                  value={meetingTime}
                  onChange={(e) => setMeetingTime(e.target.value)}
                />
              </div>
              <div className="meeting-field full-width">
                <label htmlFor="meetingLocation">Location</label>
                <input
                  type="text"
                  id="meetingLocation"
                  className="form-input"
                  placeholder="e.g., Room 301, Admin Block"
                  value={meetingLocation}
                  onChange={(e) => setMeetingLocation(e.target.value)}
                />
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* Generate Button */}
        {!generatedEmail && (
          <button
            className="generate-button"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Generating Email...
              </>
            ) : (
              <>
                <span>✨</span>
                Generate Email
              </>
            )}
          </button>
        )}

        {/* Generated Email Display */}
        {generatedEmail && (
          <div className="generated-email">
            <div className="email-preview">
              <div className="email-field">
                <label htmlFor="emailSubject">Subject</label>
                <input
                  type="text"
                  id="emailSubject"
                  className="email-subject-input"
                  value={editableSubject}
                  onChange={(e) => setEditableSubject(e.target.value)}
                />
              </div>
              <div className="email-field">
                <label htmlFor="emailBody">Body</label>
                <textarea
                  id="emailBody"
                  className="email-body-textarea"
                  value={editableBody}
                  onChange={(e) => setEditableBody(e.target.value)}
                  rows={12}
                />
              </div>
            </div>

            <div className="email-actions">
              <button className="action-button copy-button" onClick={handleCopyToClipboard}>
                <span>📋</span>
                Copy to Clipboard
              </button>
              <button className="action-button regenerate-button" onClick={handleRegenerate}>
                <span>🔄</span>
                Regenerate
              </button>
              <button className="action-button mail-button" onClick={handleOpenInMailApp}>
                <span>📨</span>
                Open in Mail App
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailGeneratorCard;
