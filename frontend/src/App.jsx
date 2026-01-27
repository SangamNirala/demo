import { Routes, Route } from 'react-router-dom'
import ErrorBoundary from './components/ErrorBoundary'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Chat from './pages/Chat'
import About from './pages/About'
import Components from './pages/Components'
import TestIntegration from './pages/TestIntegration'
import './App.css'

function App() {
  return (
    <ErrorBoundary>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/about" element={<About />} />
          <Route path="/components" element={<Components />} />
          <Route path="/test" element={<TestIntegration />} />
        </Routes>
      </div>
    </ErrorBoundary>
  )
}

export default App
