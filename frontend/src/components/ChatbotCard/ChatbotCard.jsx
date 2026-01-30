import React, { useState, useRef, useEffect } from 'react';
import './ChatbotCard.css';

const ChatbotCard = ({ studentData, predictionData }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(`session_${Date.now()}`);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Suggested questions
  const suggestions = [
    "Why is this student at high risk?",
    "What should I do first?",
    "How can we improve their attendance?",
    "What are the main concerns?"
  ];

  const sendMessage = async (message) => {
    if (!message.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8001/api/chatbot/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          student_data: studentData,
          prediction_data: predictionData,
          session_id: sessionId
        }),
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.message || 'Failed to get response');
      }

      console.log('📨 Chatbot response received:', data.response);
      console.log('📏 Response length:', data.response?.length);

      // Add assistant message to chat
      const assistantMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  const clearChat = () => {
    setMessages([]);
    // Optionally call API to clear server-side history
    fetch('http://localhost:8001/api/chatbot/clear-history', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ session_id: sessionId }),
    }).catch(err => console.error('Error clearing history:', err));
  };

  // Format message content with bullet points and bold text
  const formatMessage = (content) => {
    if (!content) return null;

    // Split by newlines and filter empty lines
    const lines = content.split('\n').filter(line => line.trim());

    return (
      <div className="message-formatted">
        {lines.map((line, idx) => {
          // Check if line is a bullet point
          const isBullet = line.trim().startsWith('•') || line.trim().startsWith('-') || line.trim().startsWith('*');
          
          // Remove bullet character
          let text = line.replace(/^[•\-*]\s*/, '').trim();

          // Convert **bold** to <strong> tags
          const parts = [];
          let lastIndex = 0;
          const boldRegex = /\*\*([^*]+)\*\*/g;
          let match;

          while ((match = boldRegex.exec(text)) !== null) {
            if (match.index > lastIndex) {
              parts.push(text.substring(lastIndex, match.index));
            }
            parts.push(<strong key={`bold-${idx}-${match.index}`}>{match[1]}</strong>);
            lastIndex = match.index + match[0].length;
          }

          if (lastIndex < text.length) {
            parts.push(text.substring(lastIndex));
          }

          if (isBullet) {
            return (
              <li key={idx} className="chat-bullet">
                {parts.length > 0 ? parts : text}
              </li>
            );
          } else {
            return (
              <p key={idx} className="chat-paragraph">
                {parts.length > 0 ? parts : text}
              </p>
            );
          }
        })}
      </div>
    );
  };

  return (
    <div className="chatbot-card">
      <div className="chatbot-header">
        <div className="chatbot-title">
          <span className="chatbot-icon">🤖</span>
          <h2>AI Assistant for Faculty</h2>
        </div>
        {messages.length > 0 && (
          <button className="clear-chat-btn" onClick={clearChat} title="Clear conversation">
            🗑️
          </button>
        )}
      </div>

      <div className="chatbot-content">
        {messages.length === 0 ? (
          <div className="chatbot-welcome">
            <div className="welcome-icon">👋</div>
            <h3>Hello! I'm your AI assistant 🤖</h3>
            <p>💡 Ask me anything about this student's risk factors, performance, or recommended interventions.</p>
            
            <div className="suggestions-container">
              <p className="suggestions-label">💭 Try asking:</p>
              <div className="suggestions-grid">
                {suggestions.map((suggestion, idx) => (
                  <button
                    key={idx}
                    className="suggestion-btn"
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="messages-container">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`message ${msg.role} ${msg.isError ? 'error' : ''}`}
              >
                <div className="message-avatar">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  {formatMessage(msg.content)}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant loading">
                <div className="message-avatar">💭</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="chatbot-input-container">
        <form onSubmit={handleSubmit} className="chatbot-form">
          <input
            type="text"
            className="chatbot-input"
            placeholder="Ask a question about this student..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            className="chatbot-send-btn"
            disabled={!inputMessage.trim() || isLoading}
          >
            {isLoading ? '⏳' : '🚀'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatbotCard;
