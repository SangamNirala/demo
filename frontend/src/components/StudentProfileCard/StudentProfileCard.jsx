import React from 'react';
import './StudentProfileCard.css';

const StudentProfileCard = ({ data }) => {
  // Helper function to get initials from name
  const getInitials = (name) => {
    if (!name) return 'ST';
    const names = name.split(' ');
    if (names.length >= 2) {
      return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };

  // Helper function to get year badge color
  const getYearBadgeClass = (year) => {
    if (!year) return 'year-1';
    const yearNum = parseInt(year);
    if (yearNum === 1 || year.includes('1st')) return 'year-1';
    if (yearNum === 2 || year.includes('2nd')) return 'year-2';
    if (yearNum === 3 || year.includes('3rd')) return 'year-3';
    if (yearNum === 4 || year.includes('4th')) return 'year-4';
    return 'year-1';
  };

  // Helper function to parse distance and determine commute level
  const getCommuteLevel = (distance) => {
    if (!distance) return { level: 'unknown', label: 'Unknown' };
    const km = parseInt(distance);
    if (km <= 10) return { level: 'near', label: 'Near Campus' };
    if (km <= 25) return { level: 'moderate', label: 'Moderate Distance' };
    return { level: 'far', label: 'Long Commute' };
  };

  // Helper function to get income level
  const getIncomeLevel = (income) => {
    if (!income) return { level: 'unknown', icon: '💰' };
    const amount = parseInt(income.replace(/[^0-9]/g, ''));
    if (amount <= 200000) return { level: 'low', icon: '📉', label: 'Lower Income' };
    if (amount <= 500000) return { level: 'medium', icon: '📊', label: 'Middle Income' };
    return { level: 'high', icon: '📈', label: 'Higher Income' };
  };

  // Helper function to get accommodation icon and style
  const getAccommodationInfo = (accommodation) => {
    if (!accommodation) return { icon: '🏠', type: 'unknown' };
    const lower = accommodation.toLowerCase();
    if (lower.includes('hostel')) {
      return { icon: '🏢', type: 'hostel', label: 'Campus Resident' };
    }
    return { icon: '🏠', type: 'day-scholar', label: 'Day Scholar' };
  };

  const commuteInfo = getCommuteLevel(data.distanceFromCollege);
  const incomeInfo = getIncomeLevel(data.familyIncome);
  const accommodationInfo = getAccommodationInfo(data.accommodation);

  return (
    <div className="profile-card">
      {/* Profile Header with Avatar */}
      <div className="profile-header">
        <div className="header-background">
          <div className="header-pattern"></div>
        </div>
        
        <div className="profile-avatar-section">
          <div className="avatar-container">
            <div className="avatar">
              <span className="avatar-initials">{getInitials(data.name)}</span>
            </div>
            <div className={`status-indicator ${data.accommodation?.toLowerCase().includes('hostel') ? 'hostel' : 'day-scholar'}`}></div>
          </div>
          
          <div className="profile-title-section">
            <h2 className="student-name">{data.name}</h2>
            <div className="student-id-badge">
              <span className="id-icon">🎓</span>
              <span className="id-text">{data.rollNo}</span>
            </div>
          </div>
        </div>

        <div className="quick-badges">
          <span className={`badge year-badge ${getYearBadgeClass(data.year)}`}>
            {data.year}
          </span>
          <span className={`badge accommodation-badge ${accommodationInfo.type}`}>
            {accommodationInfo.icon} {data.accommodation}
          </span>
        </div>
      </div>

      {/* Card Content */}
      <div className="profile-content">
        
        {/* Academic Information Section */}
        <div className="info-section">
          <div className="section-header">
            <span className="section-icon">📚</span>
            <h3 className="section-title">Academic Information</h3>
          </div>
          
          <div className="info-cards-grid">
            <div className="info-card academic">
              <div className="info-card-icon">
                <span>🎯</span>
              </div>
              <div className="info-card-content">
                <span className="info-card-label">Course / Program</span>
                <span className="info-card-value">{data.course}</span>
              </div>
            </div>
            
            <div className="info-card academic">
              <div className="info-card-icon">
                <span>📅</span>
              </div>
              <div className="info-card-content">
                <span className="info-card-label">Current Year</span>
                <span className="info-card-value">{data.year}</span>
                <div className="year-progress">
                  <div className="year-progress-bar">
                    {[1, 2, 3, 4].map((year) => (
                      <div 
                        key={year}
                        className={`year-dot ${parseInt(data.year) >= year || data.year?.includes(`${year}`) ? 'completed' : ''}`}
                      >
                        {year}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Socio-Economic Information Section */}
        <div className="info-section">
          <div className="section-header">
            <span className="section-icon">👨‍👩‍👧‍👦</span>
            <h3 className="section-title">Socio-Economic Background</h3>
          </div>
          
          <div className="info-cards-grid">
            {/* Family Income Card */}
            <div className={`info-card income ${incomeInfo.level}`}>
              <div className="info-card-icon">
                <span>{incomeInfo.icon}</span>
              </div>
              <div className="info-card-content">
                <span className="info-card-label">Family Income (Annual)</span>
                <span className="info-card-value highlight">{data.familyIncome}</span>
                <span className={`income-indicator ${incomeInfo.level}`}>
                  {incomeInfo.label}
                </span>
              </div>
            </div>

            {/* Parent Education Card */}
            <div className="info-card education">
              <div className="info-card-icon">
                <span>🎓</span>
              </div>
              <div className="info-card-content">
                <span className="info-card-label">Parent Education Level</span>
                <span className="info-card-value">{data.parentEducation}</span>
                <div className="education-level-bar">
                  <div className={`education-fill ${getEducationLevel(data.parentEducation)}`}></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Location & Accommodation Section */}
        <div className="info-section">
          <div className="section-header">
            <span className="section-icon">📍</span>
            <h3 className="section-title">Location & Accommodation</h3>
          </div>
          
          <div className="location-accommodation-grid">
            {/* Distance Card */}
            <div className={`location-card ${commuteInfo.level}`}>
              <div className="location-visual">
                <div className="distance-circle">
                  <span className="distance-value">{parseInt(data.distanceFromCollege) || '?'}</span>
                  <span className="distance-unit">km</span>
                </div>
                <div className={`commute-indicator ${commuteInfo.level}`}>
                  {commuteInfo.level === 'near' && '🚶'}
                  {commuteInfo.level === 'moderate' && '🚌'}
                  {commuteInfo.level === 'far' && '🚗'}
                </div>
              </div>
              <div className="location-details">
                <span className="location-label">Distance from College</span>
                <span className="location-value">{data.distanceFromCollege}</span>
                <span className={`commute-badge ${commuteInfo.level}`}>
                  {commuteInfo.label}
                </span>
              </div>
            </div>

            {/* Accommodation Card */}
            <div className={`accommodation-card ${accommodationInfo.type}`}>
              <div className="accommodation-visual">
                <div className="accommodation-icon-large">
                  {accommodationInfo.icon}
                </div>
              </div>
              <div className="accommodation-details">
                <span className="accommodation-label">Accommodation Type</span>
                <span className="accommodation-value">{data.accommodation}</span>
                <span className={`accommodation-status ${accommodationInfo.type}`}>
                  {accommodationInfo.label}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Profile Summary Footer */}
        <div className="profile-footer">
          <div className="footer-title">
            <span>📋</span>
            Quick Profile Summary
          </div>
          <div className="summary-tags">
            <span className="summary-tag course">{data.course?.split(' ')[0] || 'Student'}</span>
            <span className="summary-tag year">{data.year}</span>
            <span className={`summary-tag accommodation ${accommodationInfo.type}`}>
              {data.accommodation}
            </span>
            <span className={`summary-tag commute ${commuteInfo.level}`}>
              {data.distanceFromCollege}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper function for education level (outside component for reusability)
const getEducationLevel = (education) => {
  if (!education) return 'unknown';
  const lower = education.toLowerCase();
  if (lower.includes('phd') || lower.includes('doctorate')) return 'doctorate';
  if (lower.includes('master') || lower.includes('post')) return 'masters';
  if (lower.includes('bachelor') || lower.includes('graduate') || lower.includes('degree')) return 'bachelors';
  if (lower.includes('diploma') || lower.includes('12') || lower.includes('higher secondary')) return 'diploma';
  if (lower.includes('high school') || lower.includes('10') || lower.includes('secondary')) return 'high-school';
  if (lower.includes('middle') || lower.includes('8')) return 'middle-school';
  if (lower.includes('primary') || lower.includes('elementary')) return 'primary';
  return 'high-school';
};

export default StudentProfileCard;