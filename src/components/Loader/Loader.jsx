import React from 'react';
import './Loader.css';

const Loader = () => {
  return (
    <div className="loader-container">
      <div className="loader-wrapper">
        <div className="loader-spinner">
          <div className="spinner-inner"></div>
          <div className="spinner-glow"></div>
        </div>
        <div className="loader-icon">🤖</div>
      </div>
      <div className="loader-text-wrapper">
        <p className="loader-text">AI Analysing</p>
        <div className="loader-dots">
          <span className="dot"></span>
          <span className="dot"></span>
          <span className="dot"></span>
        </div>
      </div>
      <p className="loader-subtitle">✨ Processing student data with advanced algorithms</p>
    </div>
  );
};

export default Loader;
