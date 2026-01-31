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
        <div style={styles.titleWrapper}>
          <div style={{...styles.decorativeCorner, ...styles.cornerTopLeft}}></div>
          <div style={{...styles.decorativeCorner, ...styles.cornerBottomRight}}></div>
          <h1 style={styles.title}>
            <span style={styles.titleIcon}>🎯</span>
            <span style={styles.titleText}>Student Dropout Risk Prediction System</span>
          </h1>
        </div>
        <p style={styles.subtitle}>
          <span style={styles.subtitleIcon}>✨</span>
          Early intervention for better student outcomes
        </p>
        <div style={styles.badge}>
          <span style={styles.badgeIcon}>🤖</span>
          Powered by AI & Machine Learning
        </div>
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
    marginBottom: '4rem',
    color: 'white',
    animation: 'fadeInDown 0.8s ease-out',
    position: 'relative',
  },
  titleWrapper: {
    position: 'relative',
    display: 'inline-block',
    padding: '2rem 3rem',
    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
    backdropFilter: 'blur(20px)',
    WebkitBackdropFilter: 'blur(20px)',
    borderRadius: '24px',
    border: '2px solid rgba(255, 255, 255, 0.2)',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.3)',
    marginBottom: '1.5rem',
  },
  title: {
    fontSize: 'clamp(1.75rem, 4.5vw, 3.2rem)',
    fontWeight: '900',
    margin: 0,
    textShadow: '0 4px 20px rgba(0,0,0,0.5), 0 2px 8px rgba(0,0,0,0.4), 0 0 40px rgba(102, 126, 234, 0.4)',
    letterSpacing: '0.5px',
    color: '#ffffff',
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
  },
  titleIcon: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 'clamp(2.5rem, 5.5vw, 4rem)',
    width: 'clamp(3.5rem, 7vw, 5rem)',
    height: 'clamp(3.5rem, 7vw, 5rem)',
    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%)',
    borderRadius: '20px',
    border: '2px solid rgba(255, 255, 255, 0.3)',
    boxShadow: '0 8px 32px rgba(102, 126, 234, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.4)',
    filter: 'drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3))',
    animation: 'iconFloat 3s ease-in-out infinite, iconGlow 2s ease-in-out infinite',
    flexShrink: 0,
  },
  titleText: {
    display: 'inline-block',
  },
  decorativeCorner: {
    position: 'absolute',
    width: '60px',
    height: '60px',
    border: '3px solid rgba(255, 255, 255, 0.2)',
    borderRadius: '12px',
  },
  cornerTopLeft: {
    top: '-15px',
    left: '-15px',
    borderRight: 'none',
    borderBottom: 'none',
    animation: 'cornerPulse 3s ease-in-out infinite',
  },
  cornerBottomRight: {
    bottom: '-15px',
    right: '-15px',
    borderLeft: 'none',
    borderTop: 'none',
    animation: 'cornerPulse 3s ease-in-out infinite 1.5s',
  },
  subtitle: {
    fontSize: 'clamp(1.05rem, 2.5vw, 1.35rem)',
    fontWeight: '500',
    textShadow: '0 2px 12px rgba(0,0,0,0.4), 0 4px 20px rgba(0,0,0,0.2)',
    letterSpacing: '0.8px',
    marginTop: '0',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    animation: 'subtitleFade 2s ease-in-out infinite',
  },
  subtitleIcon: {
    fontSize: '1.5rem',
    filter: 'drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3))',
    animation: 'sparkle 2s ease-in-out infinite',
  },
  badge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.5rem 1.25rem',
    background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%)',
    backdropFilter: 'blur(10px)',
    WebkitBackdropFilter: 'blur(10px)',
    border: '1px solid rgba(16, 185, 129, 0.3)',
    borderRadius: '50px',
    fontSize: '0.9rem',
    fontWeight: '600',
    color: '#86efac',
    textShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
    boxShadow: '0 4px 16px rgba(16, 185, 129, 0.2)',
    marginTop: '1rem',
    animation: 'badgePulse 2s ease-in-out infinite',
  },
  badgeIcon: {
    fontSize: '1.1rem',
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
