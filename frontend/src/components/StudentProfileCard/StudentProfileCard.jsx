import React from 'react';
import './StudentProfileCard.css';

const StudentProfileCard = ({ data }) => {
  return (
    <div className="profile-card">
      <div className="card-header">
        <h2>👤 Student Profile</h2>
      </div>
      <div className="card-content">
        <div className="info-row">
          <span className="label">Name:</span>
          <span className="value">{data.name}</span>
        </div>
        <div className="info-row">
          <span className="label">Roll No:</span>
          <span className="value">{data.rollNo}</span>
        </div>
        <div className="info-row">
          <span className="label">Course:</span>
          <span className="value">{data.course}</span>
        </div>
        <div className="info-row">
          <span className="label">Year:</span>
          <span className="value">{data.year}</span>
        </div>
        <div className="info-row">
          <span className="label">Family Income:</span>
          <span className="value">{data.familyIncome}</span>
        </div>
        <div className="info-row">
          <span className="label">Parent Education:</span>
          <span className="value">{data.parentEducation}</span>
        </div>
        <div className="info-row">
          <span className="label">Distance:</span>
          <span className="value">{data.distanceFromCollege}</span>
        </div>
        <div className="info-row">
          <span className="label">Accommodation:</span>
          <span className="value">{data.accommodation}</span>
        </div>
      </div>
    </div>
  );
};

export default StudentProfileCard;
