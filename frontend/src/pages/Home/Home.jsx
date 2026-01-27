import { Link } from 'react-router-dom'
import './Home.css'

function Home() {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1>Welcome to Your Hackathon Template</h1>
        <p>A full-stack template with React, FastAPI, and Gemini AI integration</p>
        <div className="cta-buttons">
          <Link to="/chat" className="btn btn-primary">Try Chat</Link>
          <Link to="/about" className="btn btn-secondary">Learn More</Link>
        </div>
      </div>
      
      <div className="features">
        <div className="feature-card">
          <h3>⚡ Fast Setup</h3>
          <p>Pre-configured backend and frontend ready to customize</p>
        </div>
        <div className="feature-card">
          <h3>🤖 AI Powered</h3>
          <p>Integrated with Google Gemini for intelligent responses</p>
        </div>
        <div className="feature-card">
          <h3>🗄️ Database Ready</h3>
          <p>SQLAlchemy setup for easy data persistence</p>
        </div>
        <div className="feature-card">
          <h3>🎨 Modern UI</h3>
          <p>Beautiful, responsive design with React Router</p>
        </div>
      </div>
    </div>
  )
}

export default Home
