import './Input.css'

function Input({ 
  label, 
  type = 'text', 
  placeholder, 
  value, 
  onChange, 
  error,
  disabled,
  required 
}) {
  return (
    <div className="input-group">
      {label && (
        <label className="input-label">
          {label} {required && <span className="required">*</span>}
        </label>
      )}
      <input
        type={type}
        className={`input-field ${error ? 'input-error' : ''}`}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        disabled={disabled}
        required={required}
      />
      {error && <span className="error-message">{error}</span>}
    </div>
  )
}

export default Input
