import React, { useState } from 'react';
import './SearchSection.css';

const SearchSection = ({ onSearch }) => {
  const [rollNo, setRollNo] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (rollNo.trim()) {
      onSearch(rollNo.trim());
    }
  };

  return (
    <div className="search-section">
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          placeholder="Enter Student Roll Number (e.g., 2023CS101)"
          value={rollNo}
          onChange={(e) => setRollNo(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button">
          🔍 Analyze Student
        </button>
      </form>
    </div>
  );
};

export default SearchSection;
