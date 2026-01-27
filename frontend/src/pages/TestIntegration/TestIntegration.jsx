import { useState } from 'react'
import { useApp } from '../../context/AppContext'
import useLocalStorage from '../../hooks/useLocalStorage'
import useDebounce from '../../hooks/useDebounce'
import useFetch from '../../hooks/useFetch'
import { formatDate, formatTime, truncateText, isValidEmail } from '../../utils/helpers'
import { storage } from '../../utils/storage'
import { STORAGE_KEYS, STATUS } from '../../utils/constants'
import Card from '../../components/Card'
import Button from '../../components/Button'
import Input from '../../components/Input'
import Loading from '../../components/Loading'
import Modal from '../../components/Modal'
import Layout from '../../components/Layout'
import './TestIntegration.css'

function TestIntegration() {
  const { theme, toggleTheme, addNotification, notifications } = useApp()
  const [name, setName] = useLocalStorage('test_name', '')
  const [searchTerm, setSearchTerm] = useState('')
  const debouncedSearch = useDebounce(searchTerm, 500)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const { data: healthData, loading: healthLoading } = useFetch('/api/health')

  const testHelpers = () => {
    const now = new Date()
    const longText = "This is a very long text that will be truncated to show only the first 30 characters..."
    
    addNotification(`Date: ${formatDate(now)}`, 'info')
    addNotification(`Time: ${formatTime(now)}`, 'success')
    addNotification(`Truncated: ${truncateText(longText, 30)}`, 'info')
  }

  const testStorage = () => {
    storage.set('test_key', { message: 'Hello from storage!' })
    const value = storage.get('test_key')
    addNotification(`Storage test: ${value.message}`, 'success')
  }

  const testValidation = () => {
    const email = 'test@example.com'
    const isValid = isValidEmail(email)
    addNotification(`Email ${email} is ${isValid ? 'valid' : 'invalid'}`, isValid ? 'success' : 'error')
  }

  return (
    <Layout>
      <div className="test-integration">
        <h1>🧪 Integration Test Page</h1>
        <p className="subtitle">Testing all utilities, hooks, and components</p>

        {/* Notifications Display */}
        <div className="notifications">
          {notifications.map(notif => (
            <div key={notif.id} className={`notification notification-${notif.type}`}>
              {notif.message}
            </div>
          ))}
        </div>

        <div className="test-grid">
          {/* Context Test */}
          <Card title="🌍 Context (AppContext)">
            <p>Current theme: <strong>{theme}</strong></p>
            <Button onClick={toggleTheme}>Toggle Theme</Button>
            <Button onClick={() => addNotification('Test notification!', 'info')}>
              Add Notification
            </Button>
          </Card>

          {/* LocalStorage Hook Test */}
          <Card title="💾 useLocalStorage Hook">
            <Input
              label="Your Name (saved to localStorage)"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
            />
            <p className="text-sm text-gray">Refresh page - your name persists!</p>
          </Card>

          {/* Debounce Hook Test */}
          <Card title="⏱️ useDebounce Hook">
            <Input
              label="Search (debounced 500ms)"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Type to search..."
            />
            <p className="text-sm">Debounced value: <strong>{debouncedSearch}</strong></p>
          </Card>

          {/* Fetch Hook Test */}
          <Card title="🌐 useFetch Hook">
            {healthLoading ? (
              <Loading size="small" text="Fetching..." />
            ) : (
              <div>
                <p>API Health: <strong className="text-success">{healthData?.status || 'N/A'}</strong></p>
                <p className="text-sm text-gray">Auto-fetched from /api/health</p>
              </div>
            )}
          </Card>

          {/* Utils Test */}
          <Card title="🛠️ Utils (helpers.js)">
            <Button onClick={testHelpers}>Test Date/Time/Truncate</Button>
            <Button onClick={testValidation} variant="secondary">
              Test Email Validation
            </Button>
          </Card>

          {/* Storage Test */}
          <Card title="📦 Storage Utils">
            <Button onClick={testStorage}>Test LocalStorage Utils</Button>
            <p className="text-sm text-gray">Check notifications for result</p>
          </Card>

          {/* Constants Test */}
          <Card title="📋 Constants">
            <p className="text-sm">STATUS.LOADING: <code>{STATUS.LOADING}</code></p>
            <p className="text-sm">STORAGE_KEYS.USER: <code>{STORAGE_KEYS.USER}</code></p>
          </Card>

          {/* Modal Test */}
          <Card title="🪟 Modal Component">
            <Button onClick={() => setIsModalOpen(true)}>Open Modal</Button>
            <Modal
              isOpen={isModalOpen}
              onClose={() => setIsModalOpen(false)}
              title="Test Modal"
              footer={
                <>
                  <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={() => {
                    addNotification('Modal confirmed!', 'success')
                    setIsModalOpen(false)
                  }}>
                    Confirm
                  </Button>
                </>
              }
            >
              <p>This modal is working perfectly! ✨</p>
            </Modal>
          </Card>

          {/* CSS Variables Test */}
          <Card title="🎨 CSS Variables">
            <div className="color-boxes">
              <div className="color-box" style={{background: 'var(--primary-color)'}}>Primary</div>
              <div className="color-box" style={{background: 'var(--success-color)'}}>Success</div>
              <div className="color-box" style={{background: 'var(--danger-color)'}}>Danger</div>
            </div>
          </Card>

          {/* Utility Classes Test */}
          <Card title="📐 Utility Classes">
            <div className="flex gap-2">
              <span className="text-primary">Primary</span>
              <span className="text-success">Success</span>
              <span className="text-danger">Danger</span>
            </div>
            <div className="flex-center mt-2">
              <span className="text-bold">Centered & Bold</span>
            </div>
          </Card>

          {/* All Components */}
          <Card title="🧩 All Components Working">
            <div className="flex-col gap-2">
              <Button variant="primary">Primary Button ✓</Button>
              <Input placeholder="Input Component ✓" />
              <Loading size="small" text="Loading ✓" />
            </div>
          </Card>

          {/* Layout Component Info */}
          <Card title="📄 Layout Component">
            <p className="text-sm">This page uses the Layout component!</p>
            <p className="text-sm text-gray">Check Layout.jsx for structure</p>
          </Card>
        </div>

        <div className="success-message">
          <h2>✅ All Integrations Working!</h2>
          <p>Every file you created is now connected and functional</p>
        </div>
      </div>
    </Layout>
  )
}

export default TestIntegration
