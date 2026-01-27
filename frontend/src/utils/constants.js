// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// App Configuration
export const APP_NAME = 'Hackathon Template'
export const APP_VERSION = '1.0.0'

// Pagination
export const DEFAULT_PAGE_SIZE = 10
export const MAX_PAGE_SIZE = 100

// Status Constants
export const STATUS = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error'
}

// Local Storage Keys
export const STORAGE_KEYS = {
  USER: 'user',
  TOKEN: 'auth_token',
  THEME: 'theme',
  LANGUAGE: 'language'
}

// Routes
export const ROUTES = {
  HOME: '/',
  CHAT: '/chat',
  ABOUT: '/about',
  COMPONENTS: '/components'
}
