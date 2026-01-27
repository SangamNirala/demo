import { useState } from 'react'
import Card from '../../components/Card'
import Button from '../../components/Button'
import Input from '../../components/Input'
import Loading from '../../components/Loading'
import Modal from '../../components/Modal'
import './Components.css'

function Components() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [inputValue, setInputValue] = useState('')

  return (
    <div className="components-page">
      <h1>Component Library</h1>
      <p className="subtitle">Reusable components ready for your hackathon project</p>

      <div className="components-grid">
        {/* Card Component */}
        <Card title="Card Component">
          <p>This is a reusable card component with header, body, and optional footer.</p>
        </Card>

        {/* Button Component */}
        <Card title="Button Variants">
          <div className="button-demo">
            <Button variant="primary">Primary Button</Button>
            <Button variant="secondary">Secondary Button</Button>
            <Button variant="danger">Danger Button</Button>
            <Button disabled>Disabled Button</Button>
          </div>
        </Card>

        {/* Input Component */}
        <Card title="Input Component">
          <Input
            label="Email Address"
            type="email"
            placeholder="Enter your email"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            required
          />
          <Input
            label="Password"
            type="password"
            placeholder="Enter password"
            error="Password must be at least 8 characters"
          />
        </Card>

        {/* Loading Component */}
        <Card title="Loading Spinner">
          <div className="loading-demo">
            <Loading size="small" text="Small" />
            <Loading size="medium" text="Medium" />
            <Loading size="large" text="Large" />
          </div>
        </Card>

        {/* Modal Component */}
        <Card title="Modal Component">
          <Button onClick={() => setIsModalOpen(true)}>
            Open Modal
          </Button>
          <Modal
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            title="Example Modal"
            footer={
              <>
                <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
                  Cancel
                </Button>
                <Button variant="primary" onClick={() => setIsModalOpen(false)}>
                  Confirm
                </Button>
              </>
            }
          >
            <p>This is a modal dialog. You can put any content here!</p>
          </Modal>
        </Card>
      </div>

      <div className="usage-section">
        <h2>How to Use</h2>
        <Card>
          <pre className="code-block">
{`// Import components
import Card from './components/Card'
import Button from './components/Button'
import Input from './components/Input'
import Loading from './components/Loading'
import Modal from './components/Modal'

// Use in your component
<Card title="My Card">
  <p>Content here</p>
</Card>

<Button variant="primary" onClick={handleClick}>
  Click Me
</Button>

<Input 
  label="Name" 
  value={name} 
  onChange={(e) => setName(e.target.value)} 
/>

<Loading size="medium" text="Loading..." />

<Modal isOpen={isOpen} onClose={handleClose} title="Title">
  Modal content
</Modal>`}
          </pre>
        </Card>
      </div>
    </div>
  )
}

export default Components
