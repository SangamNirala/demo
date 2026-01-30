import React, { useState } from 'react';
import './DownloadReportButton.css';

const DownloadReportButton = ({ studentData, predictionData, rollNo }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  const handleDownload = async () => {
    if (!studentData || !predictionData) {
      setError('Missing student or prediction data');
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8001/api/pdf/generate/${rollNo}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_data: studentData,
          prediction_data: predictionData,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate PDF report');
      }

      // Get the PDF blob
      const blob = await response.blob();
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      // Generate filename
      const studentName = studentData.name?.replace(/\s+/g, '_') || 'Student';
      link.download = `Risk_Report_${rollNo}_${studentName}.pdf`;
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (err) {
      console.error('Error generating PDF:', err);
      setError('Failed to generate PDF report. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="download-report-container">
      <button
        className="download-report-button"
        onClick={handleDownload}
        disabled={isGenerating || !studentData || !predictionData}
      >
        {isGenerating ? (
          <>
            <span className="spinner"></span>
            Generating PDF...
          </>
        ) : (
          <>
            <span className="icon">📊</span>
            Download Detailed Report
          </>
        )}
      </button>
      
      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}
      
      {!error && !isGenerating && (
        <p className="download-hint">
          📈 Get a comprehensive AI-powered PDF report with detailed analysis and intervention plans
        </p>
      )}
    </div>
  );
};

export default DownloadReportButton;
