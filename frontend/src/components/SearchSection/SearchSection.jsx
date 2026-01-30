import { useState, useEffect, useRef } from 'react';
import './SearchSection.css';

const SearchSection = ({ onSearch, isLoading = false }) => {
  const [rollNo, setRollNo] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [error, setError] = useState('');
  const [riskCategories, setRiskCategories] = useState({
    high: [],
    medium: [],
    low: []
  });
  const [showDropdown, setShowDropdown] = useState(null); // 'high', 'medium', 'low', or null
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);
  const dropdownRef = useRef(null);

  // Fetch risk categories on mount
  useEffect(() => {
    fetchRiskCategories();
  }, []);

  const fetchRiskCategories = async () => {
    try {
      // Fetch all students
      const response = await fetch('http://localhost:8001/api/students');
      const data = await response.json();
      
      if (data.students) {
        // Categorize by risk level
        const high = [];
        const medium = [];
        const low = [];
        
        data.students.forEach(student => {
          const riskPercentage = student.risk_percentage || 0;
          
          if (riskPercentage > 60) {
            high.push(student);
          } else if (riskPercentage >= 40) {
            medium.push(student);
          } else {
            low.push(student);
          }
        });
        
        setRiskCategories({ high, medium, low });
      }
    } catch (err) {
      console.error('Error fetching risk categories:', err);
    }
  };

  // Filter suggestions based on input
  const filteredSuggestions = rollNo.length > 0
    ? [...riskCategories.high, ...riskCategories.medium, ...riskCategories.low].filter(
        s => s.roll_no?.toLowerCase().includes(rollNo.toLowerCase()) ||
             s.name?.toLowerCase().includes(rollNo.toLowerCase())
      ).slice(0, 10)
    : [];

  // Handle form submit
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!rollNo.trim()) {
      setError('Please enter a roll number');
      inputRef.current?.focus();
      return;
    }
    setError('');
    setShowSuggestions(false);
    onSearch(rollNo.trim().toUpperCase());
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion) => {
    setRollNo(suggestion.roll_no);
    setShowSuggestions(false);
    setError('');
    onSearch(suggestion.roll_no);
  };

  // Handle quick access click
  const handleQuickAccess = (roll) => {
    setRollNo(roll);
    setError('');
    setShowDropdown(null);
    onSearch(roll);
  };

  // Toggle dropdown
  const toggleDropdown = (category) => {
    setShowDropdown(showDropdown === category ? null : category);
  };

  // Handle input change
  const handleInputChange = (e) => {
    const value = e.target.value.toUpperCase();
    setRollNo(value);
    setError('');
    setShowSuggestions(value.length > 0);
  };

  // Handle clear input
  const handleClear = () => {
    setRollNo('');
    setError('');
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  // Close suggestions and dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (suggestionsRef.current && !suggestionsRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
      if (e.key === 'Escape') {
        handleClear();
        setShowDropdown(null);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="search-section">
      {/* Main Search Container */}
      <div className={`search-container ${isFocused ? 'focused' : ''} ${error ? 'has-error' : ''}`}>
        
        {/* Search Icon */}
        <div className="search-icon-wrapper">
          <svg 
            className="search-icon" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
        </div>

        {/* Input Field */}
        <form onSubmit={handleSubmit} className="search-form">
          <input
            ref={inputRef}
            type="text"
            placeholder="Enter Roll Number or Student Name..."
            value={rollNo}
            onChange={handleInputChange}
            onFocus={() => {
              setIsFocused(true);
              if (rollNo.length > 0) setShowSuggestions(true);
            }}
            onBlur={() => setIsFocused(false)}
            className="search-input"
            autoComplete="off"
            spellCheck="false"
          />

          {/* Clear Button */}
          {rollNo && (
            <button 
              type="button" 
              className="clear-button"
              onClick={handleClear}
              title="Clear (Esc)"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          )}

          {/* Keyboard Shortcut Hint */}
          {!rollNo && !isFocused && (
            <div className="keyboard-hint">
              <kbd>Ctrl</kbd>
              <span>+</span>
              <kbd>K</kbd>
            </div>
          )}

          {/* Submit Button */}
          <button 
            type="submit" 
            className={`search-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
                <span>Analyze Student</span>
              </>
            )}
          </button>
        </form>

        {/* Suggestions Dropdown */}
        {showSuggestions && filteredSuggestions.length > 0 && (
          <div className="suggestions-dropdown" ref={suggestionsRef}>
            <div className="suggestions-header">
              <span className="suggestions-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
                Suggestions
              </span>
              <span className="suggestions-count">{filteredSuggestions.length} found</span>
            </div>
            <ul className="suggestions-list">
              {filteredSuggestions.map((suggestion, index) => (
                <li 
                  key={suggestion.roll_no}
                  className="suggestion-item"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  <div className="suggestion-avatar">
                    {suggestion.name.charAt(0)}
                  </div>
                  <div className="suggestion-info">
                    <span className="suggestion-name">{suggestion.name}</span>
                    <span className="suggestion-details">
                      {suggestion.roll_no} • {suggestion.course}
                    </span>
                  </div>
                  <div className="suggestion-arrow">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M9 18l6-6-6-6" />
                    </svg>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Quick Access Section with Counts */}
      <div className="quick-access-section">
        <div className="quick-access-header">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
          </svg>
          <span>Quick Access</span>
        </div>
        <div className="quick-access-grid">
          {/* High Risk Card */}
          <div className="quick-access-card-wrapper" ref={showDropdown === 'high' ? dropdownRef : null}>
            <button
              className="quick-access-card high-risk"
              onClick={() => toggleDropdown('high')}
            >
              <div className="risk-icon high-risk">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L2 22h20L12 2zm0 4l7 14H5l7-14zm-1 5v4h2v-4h-2zm0 6v2h2v-2h-2z"/>
                </svg>
              </div>
              <div className="card-content">
                <span className="risk-badge high-risk">HIGH RISK</span>
                <span className="roll-number">({riskCategories.high.length})</span>
              </div>
              <svg className={`dropdown-arrow ${showDropdown === 'high' ? 'open' : ''}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M6 9l6 6 6-6"/>
              </svg>
            </button>
            
            {/* Dropdown for High Risk */}
            {showDropdown === 'high' && riskCategories.high.length > 0 && (
              <div className="risk-dropdown">
                <div className="dropdown-header">
                  <span>High Risk Students ({riskCategories.high.length})</span>
                </div>
                <ul className="dropdown-list">
                  {riskCategories.high.map((student) => (
                    <li 
                      key={student.roll_no}
                      className="dropdown-item"
                      onClick={() => handleQuickAccess(student.roll_no)}
                    >
                      <div className="student-avatar high-risk">
                        {student.name?.charAt(0) || 'S'}
                      </div>
                      <div className="student-info">
                        <span className="student-name">{student.name}</span>
                        <span className="student-details">
                          {student.roll_no} • {student.risk_percentage?.toFixed(1)}%
                        </span>
                      </div>
                      <div className="arrow-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M9 18l6-6-6-6" />
                        </svg>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Medium Risk Card */}
          <div className="quick-access-card-wrapper" ref={showDropdown === 'medium' ? dropdownRef : null}>
            <button
              className="quick-access-card medium-risk"
              onClick={() => toggleDropdown('medium')}
            >
              <div className="risk-icon medium-risk">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2" stroke="white" strokeWidth="2" fill="none"/>
                </svg>
              </div>
              <div className="card-content">
                <span className="risk-badge medium-risk">MEDIUM RISK</span>
                <span className="roll-number">({riskCategories.medium.length})</span>
              </div>
              <svg className={`dropdown-arrow ${showDropdown === 'medium' ? 'open' : ''}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M6 9l6 6 6-6"/>
              </svg>
            </button>
            
            {/* Dropdown for Medium Risk */}
            {showDropdown === 'medium' && riskCategories.medium.length > 0 && (
              <div className="risk-dropdown">
                <div className="dropdown-header">
                  <span>Medium Risk Students ({riskCategories.medium.length})</span>
                </div>
                <ul className="dropdown-list">
                  {riskCategories.medium.map((student) => (
                    <li 
                      key={student.roll_no}
                      className="dropdown-item"
                      onClick={() => handleQuickAccess(student.roll_no)}
                    >
                      <div className="student-avatar medium-risk">
                        {student.name?.charAt(0) || 'S'}
                      </div>
                      <div className="student-info">
                        <span className="student-name">{student.name}</span>
                        <span className="student-details">
                          {student.roll_no} • {student.risk_percentage?.toFixed(1)}%
                        </span>
                      </div>
                      <div className="arrow-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M9 18l6-6-6-6" />
                        </svg>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Low Risk Card */}
          <div className="quick-access-card-wrapper" ref={showDropdown === 'low' ? dropdownRef : null}>
            <button
              className="quick-access-card low-risk"
              onClick={() => toggleDropdown('low')}
            >
              <div className="risk-icon low-risk">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <div className="card-content">
                <span className="risk-badge low-risk">LOW RISK</span>
                <span className="roll-number">({riskCategories.low.length})</span>
              </div>
              <svg className={`dropdown-arrow ${showDropdown === 'low' ? 'open' : ''}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M6 9l6 6 6-6"/>
              </svg>
            </button>
            
            {/* Dropdown for Low Risk */}
            {showDropdown === 'low' && riskCategories.low.length > 0 && (
              <div className="risk-dropdown">
                <div className="dropdown-header">
                  <span>Low Risk Students ({riskCategories.low.length})</span>
                </div>
                <ul className="dropdown-list">
                  {riskCategories.low.map((student) => (
                    <li 
                      key={student.roll_no}
                      className="dropdown-item"
                      onClick={() => handleQuickAccess(student.roll_no)}
                    >
                      <div className="student-avatar low-risk">
                        {student.name?.charAt(0) || 'S'}
                      </div>
                      <div className="student-info">
                        <span className="student-name">{student.name}</span>
                        <span className="student-details">
                          {student.roll_no} • {student.risk_percentage?.toFixed(1)}%
                        </span>
                      </div>
                      <div className="arrow-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M9 18l6-6-6-6" />
                        </svg>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Info Footer */}
      <div className="search-footer">
        <div className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 16v-4" />
            <path d="M12 8h.01" />
          </svg>
          <span>Enter a valid roll number to analyze dropout risk</span>
        </div>
        <div className="footer-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          <span>Data is secure and confidential</span>
        </div>
      </div>
    </div>
  );
};

export default SearchSection;