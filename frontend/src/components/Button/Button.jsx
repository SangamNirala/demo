import './Button.css'

function Button({ children, variant = 'primary', onClick, disabled, type = 'button' }) {
  return (
    <button 
      className={`custom-btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled}
      type={type}
    >
      {children}
    </button>
  )
}

export default Button
