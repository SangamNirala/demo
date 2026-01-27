import axios from 'axios'

const API_BASE_URL = '/api'

export const chatAPI = {
  sendMessage: async (message, conversationHistory = []) => {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
      message,
      conversation_history: conversationHistory
    })
    return response.data
  },
  
  getChatHistory: async (sessionId) => {
    const response = await axios.get(`${API_BASE_URL}/chat/history/${sessionId}`)
    return response.data
  }
}

export const userAPI = {
  createUser: async (username, email) => {
    const response = await axios.post(`${API_BASE_URL}/users`, {
      username,
      email
    })
    return response.data
  },
  
  getUser: async (userId) => {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}`)
    return response.data
  }
}

export const healthCheck = async () => {
  const response = await axios.get(`${API_BASE_URL}/health`)
  return response.data
}
