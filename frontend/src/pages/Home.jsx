import React, { useState } from 'react';
import SearchSection from '../components/SearchSection';
import StudentProfileCard from '../components/StudentProfileCard';
import OngoingDataCard from '../components/OngoingDataCard';
import PredictionButton from '../components/PredictionButton';
import RiskAlertCard from '../components/RiskAlertCard';
import RiskFactorsCard from '../components/RiskFactorsCard';
import RecommendationsCard from '../components/RecommendationsCard';
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
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    padding: '2rem',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
  header: {
    textAlign: 'center',
    marginBottom: '3rem',
    color: 'white',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 'bold',
    marginBottom: '0.5rem',
    textShadow: '2px 2px 4px rgba(0,0,0,0.2)',
  },
  subtitle: {
    fontSize: '1.1rem',
    opacity: 0.9,
  },
  errorBox: {
    maxWidth: '800px',
    margin: '2rem auto',
    padding: '1rem 1.5rem',
    background: '#fee2e2',
    color: '#991b1b',
    borderRadius: '8px',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    fontSize: '1rem',
  },
  errorIcon: {
    fontSize: '1.5rem',
  },
  dataSection: {
    maxWidth: '1200px',
    margin: '0 auto',
  },
  cardsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
    gap: '2rem',
    marginBottom: '2rem',
  },
  predictionSection: {
    maxWidth: '1000px',
    margin: '0 auto',
  },
};

export default Home;
