import { Link } from 'react-router-dom'
import './Navbar.css'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/">🚀 Hackathon Template</Link>
      </div>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/chat">Chat</Link>
        <Link to="/components">Components</Link>
        <Link to="/about">About</Link>
      </div>
    </nav>
  )
}

export default Navbar
