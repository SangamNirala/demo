import React, { useState, useEffect, useRef } from 'react';
import './SearchSection.css';

const SearchSection = ({ onSearch, isLoading = false, recentSearches = [] }) => {
  const [rollNo, setRollNo] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);

  // Sample suggestions - replace with actual data from API
  const sampleSuggestions = [
    { roll_no: '2023CS001', name: 'Rahul Sharma', course: 'B.Tech CSE' },
    { roll_no: '2023ME4422', name: 'Ekta Verma', course: 'B.Tech ME' },
    { roll_no: '2023EC4154', name: 'Anjali Bhatia', course: 'B.Tech ECE' },
    { roll_no: '2022CE3113', name: 'Kritika Mishra', course: 'B.Tech CE' },
    { roll_no: '2023EE345', name: 'Ishita Goel', course: 'B.Tech EE' },
  ];

  // Filter suggestions based on input
  const filteredSuggestions = rollNo.length > 0
    ? sampleSuggestions.filter(
        s => s.roll_no.toLowerCase().includes(rollNo.toLowerCase()) ||
             s.name.toLowerCase().includes(rollNo.toLowerCase())
      )
    : [];

  // Quick access roll numbers
  const quickAccess = [
    { roll_no: '2023ME4422', label: 'High Risk' },
    { roll_no: '2023EC4154', label: 'Medium Risk' },
    { roll_no: '2023EE345', label: 'Low Risk' },
  ];

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
    onSearch(roll);
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

  // Close suggestions on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (suggestionsRef.current && !suggestionsRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl/Cmd + K to focus search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
      // Escape to clear
      if (e.key === 'Escape') {
        handleClear();
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

      {/* Quick Access Section */}
      <div className="quick-access">
        <span className="quick-access-label">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
          </svg>
          Quick Access:
        </span>
        <div className="quick-access-buttons">
          {quickAccess.map((item) => (
            <button
              key={item.roll_no}
              className={`quick-access-btn ${item.label.toLowerCase().replace(' ', '-')}`}
              onClick={() => handleQuickAccess(item.roll_no)}
            >
              <span className="quick-btn-roll">{item.roll_no}</span>
              <span className={`quick-btn-badge ${item.label.toLowerCase().replace(' ', '-')}`}>
                {item.label}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Info Text */}
      <div className="search-info">
        <div className="info-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 16v-4" />
            <path d="M12 8h.01" />
          </svg>
          <span>Enter a valid roll number to analyze dropout risk</span>
        </div>
        <div className="info-item">
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