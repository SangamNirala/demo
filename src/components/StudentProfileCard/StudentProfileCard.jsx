import './StudentProfileCard.css';

const StudentProfileCard = ({ data }) => {
  const getInitials = (name) => {
    if (!name) return 'ST';
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="profile-card">
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
              <div className="avatar-badge">
                {getInitials(data.name)}
              </div>
            </div>
          </div>
          <div className="header-text">
            <span className="header-eyebrow">Student Profile</span>
            <h2>{data.name}</h2>
            <p>{data.course} • Year {data.year}</p>
          </div>
        </div>
        <div className="header-badge">
          <span className="status-indicator"></span>
          <span className="status-ring"></span>
          Active
        </div>
      </div>

      <div className="card-content">
        {/* Academic Information */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper academic">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                <path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/>
              </svg>
            </div>
            <h3>Academic Details</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="info-grid">
            <div className="info-card">
              <div className="info-card-glow"></div>
              <div className="info-header">
                <div className="info-icon-wrapper name">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </div>
                <span className="info-label">Full Name</span>
              </div>
              <div className="info-body">
                <div className="info-value">{data.name}</div>
              </div>
            </div>

            <div className="info-card">
              <div className="info-card-glow"></div>
              <div className="info-header">
                <div className="info-icon-wrapper roll">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                  </svg>
                </div>
                <span className="info-label">Roll Number</span>
              </div>
              <div className="info-body">
                <div className="info-value">{data.rollNo}</div>
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
                <span className="info-label">Course</span>
              </div>
              <div className="info-body">
                <div className="info-value">{data.course}</div>
              </div>
            </div>

            <div className="info-card">
              <div className="info-card-glow"></div>
              <div className="info-header">
                <div className="info-icon-wrapper year">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                </div>
                <span className="info-label">Academic Year</span>
              </div>
              <div className="info-body">
                <div className="info-value">Year {data.year}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="section-divider">
          <span className="divider-accent"></span>
        </div>

        {/* Family Background */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper family">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <h3>Family Background</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="family-grid">
            <div className="family-item">
              <div className="family-icon-wrapper income">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="1" x2="12" y2="23"/>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                </svg>
              </div>
              <div className="family-details">
                <span className="family-label">Family Income</span>
                <span className="family-value">{data.familyIncome}</span>
              </div>
              <div className="family-indicator">
                <span className="indicator-dot good"></span>
              </div>
            </div>

            <div className="family-item">
              <div className="family-icon-wrapper education">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                  <path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/>
                </svg>
              </div>
              <div className="family-details">
                <span className="family-label">Parent Education</span>
                <span className="family-value">{data.parentEducation}</span>
              </div>
              <div className="family-indicator">
                <span className="indicator-dot good"></span>
              </div>
            </div>
          </div>
        </div>

        <div className="section-divider">
          <span className="divider-accent"></span>
        </div>

        {/* Location & Accommodation */}
        <div className="data-section">
          <div className="section-header">
            <div className="section-icon-wrapper location">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </div>
            <h3>Location & Accommodation</h3>
            <div className="section-line"></div>
          </div>
          
          <div className="location-cards">
            <div className="location-card">
              <div className="location-card-accent"></div>
              <div className="location-icon-wrapper">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M9 11a3 3 0 1 0 6 0a3 3 0 0 0-6 0"/>
                  <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 0 1-2.827 0l-4.244-4.243a8 8 0 1 1 11.314 0z"/>
                </svg>
              </div>
              <div className="location-content">
                <span className="location-label">Distance from College</span>
                <span className="location-value">{data.distanceFromCollege}</span>
              </div>
            </div>

            <div className="location-card">
              <div className="location-card-accent"></div>
              <div className="location-icon-wrapper">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M3 21h18"/>
                  <path d="M5 21V7l8-4v18"/>
                  <path d="M19 21V11l-6-4"/>
                </svg>
              </div>
              <div className="location-content">
                <span className="location-label">Accommodation Type</span>
                <span className="location-value">{data.accommodation}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Summary Footer */}
        <div className="card-footer">
          <div className="footer-title">Profile Summary</div>
          <div className="summary-items">
            <div className="summary-item good">
              <span className="summary-dot">
                <span className="dot-ring"></span>
              </span>
              <span className="summary-count">6</span>
              <span className="summary-text">Complete</span>
            </div>
            <div className="summary-item neutral">
              <span className="summary-dot">
                <span className="dot-ring"></span>
              </span>
              <span className="summary-count">0</span>
              <span className="summary-text">Pending</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Accent */}
      <div className="card-footer-accent"></div>
    </div>
  );
};

export default StudentProfileCard;