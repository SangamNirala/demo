import './About.css'

function About() {
  return (
    <div className="about-container">
      <h1>About This Template</h1>
      <div className="about-content">
        <section>
          <h2>🎯 Purpose</h2>
          <p>
            This template is designed for hackathons where you need to quickly build
            and deploy a full-stack application with AI capabilities.
          </p>
        </section>
        
        <section>
          <h2>🛠️ Tech Stack</h2>
          <ul>
            <li><strong>Frontend:</strong> React + Vite + React Router</li>
            <li><strong>Backend:</strong> FastAPI + SQLAlchemy</li>
            <li><strong>AI:</strong> Google Gemini API</li>
            <li><strong>Database:</strong> SQLite (easily switchable)</li>
          </ul>
        </section>
        
        <section>
          <h2>🚀 Quick Start</h2>
          <ol>
            <li>Clone the template</li>
            <li>Add your API keys to <code>.env</code></li>
            <li>Install dependencies</li>
            <li>Start building your solution!</li>
          </ol>
        </section>
        
        <section>
          <h2>📝 Customization Tips</h2>
          <ul>
            <li>Modify <code>ai_service.py</code> to change AI behavior</li>
            <li>Add new routes in <code>backend/routes/</code></li>
            <li>Create new pages in <code>frontend/src/pages/</code></li>
            <li>Update models in <code>models.py</code> for your data</li>
          </ul>
        </section>
      </div>
    </div>
  )
}

export default About
