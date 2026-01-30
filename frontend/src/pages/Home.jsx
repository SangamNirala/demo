import React, { useState } from 'react';
import SearchSection from '../components/SearchSection';
import StudentProfileCard from '../components/StudentProfileCard';
import OngoingDataCard from '../components/OngoingDataCard';
import PredictionButton from '../components/PredictionButton';
import RiskAlertCard from '../components/RiskAlertCard';
import RiskFactorsCard from '../components/RiskFactorsCard';
import RecommendationsCard from '../components/RecommendationsCard';
import ChatbotCard from '../components/ChatbotCard';
import DownloadReportButton from '../components/DownloadReportButton';
import EmailGeneratorCard from '../components/EmailGeneratorCard';
import Loader from '../components/Loader';
import { getStudentData, getPrediction } from '../services/api';
import '../styles/global.css';

const Home = () => {
  const [studentData, setStudentData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (rollNo) => {
    setLoading(true);
    setError(null);
    setPredictionData(null);
    
    try {
      const data = await getStudentData(rollNo);
      setStudentData(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch student data');
      setStudentData(null);
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async () => {
    if (!studentData) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await getPrediction(studentData.roll_no || studentData.rollNo);
      setPredictionData(data);
    } catch (err) {
      setError(err.message || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🎓 Student Dropout Risk Prediction System</h1>
        <p style={styles.subtitle}>Early intervention for better student outcomes</p>
      </div>

      <SearchSection onSearch={handleSearch} />

      {loading && <Loader />}
      
      {error && (
        <div style={styles.errorBox}>
          <span style={styles.errorIcon}>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {studentData && !predictionData && (
        <div style={styles.dataSection}>
          <div style={styles.cardsRow}>
            <StudentProfileCard data={studentData} />
            <OngoingDataCard data={studentData} />
          </div>
          <PredictionButton onClick={handlePredict} disabled={loading} />
        </div>
      )}

      {predictionData && (
        <div style={styles.predictionSection}>
          <RiskAlertCard data={predictionData} studentData={studentData} />
          <RiskFactorsCard factors={predictionData.riskFactors} />
          <RecommendationsCard recommendations={predictionData.recommendations} />
          <EmailGeneratorCard studentData={studentData} predictionData={predictionData} />
          <DownloadReportButton 
            studentData={studentData} 
            predictionData={predictionData}
            rollNo={studentData.roll_no || studentData.rollNo}
          />
          <ChatbotCard studentData={studentData} predictionData={predictionData} />
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    padding: '2rem 1.5rem',
    position: 'relative',
    zIndex: 1,
  },
  header: {
    textAlign: 'center',
    marginBottom: '3.5rem',
    color: 'white',
    animation: 'fadeInDown 0.8s ease-out',
  },
  title: {
    fontSize: 'clamp(1.8rem, 5vw, 3rem)',
    fontWeight: '800',
    marginBottom: '0.75rem',
    textShadow: '0 4px 12px rgba(0,0,0,0.3), 0 2px 4px rgba(0,0,0,0.2)',
    letterSpacing: '-0.5px',
    background: 'linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  },
  subtitle: {
    fontSize: 'clamp(1rem, 2.5vw, 1.25rem)',
    opacity: 0.95,
    fontWeight: '400',
    textShadow: '0 2px 8px rgba(0,0,0,0.2)',
    letterSpacing: '0.3px',
  },
  errorBox: {
    maxWidth: '800px',
    margin: '2rem auto',
    padding: '1.25rem 1.75rem',
    background: 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)',
    color: '#991b1b',
    borderRadius: '16px',
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    fontSize: '1rem',
    fontWeight: '500',
    boxShadow: '0 10px 25px rgba(239, 68, 68, 0.2)',
    border: '1px solid rgba(239, 68, 68, 0.2)',
    animation: 'slideInUp 0.4s ease-out',
  },
  errorIcon: {
    fontSize: '1.75rem',
    flexShrink: 0,
  },
  dataSection: {
    maxWidth: '1200px',
    margin: '0 auto',
    animation: 'fadeInUp 0.6s ease-out',
  },
  cardsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(min(350px, 100%), 1fr))',
    gap: '2rem',
    marginBottom: '2rem',
  },
  predictionSection: {
    maxWidth: '1000px',
    margin: '0 auto',
    animation: 'fadeInUp 0.6s ease-out 0.2s both',
  },
};

export default Home;
