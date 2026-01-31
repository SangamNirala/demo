# AI Chatbot for Faculty/Admin

An intelligent conversational interface that helps faculty and administrators understand student risk factors, get insights, and receive guidance on interventions.

## Features

✅ **Context-Aware Conversations**: Understands student data, risk factors, and recommendations
✅ **Natural Language Queries**: Ask questions in plain English
✅ **Actionable Insights**: Provides specific, data-driven guidance
✅ **Conversation History**: Maintains context across multiple questions
✅ **Suggested Questions**: Quick-start prompts for common queries
✅ **Real-time Responses**: Powered by Gemini 2.5 Flash

## Example Questions

Faculty can ask questions like:

- "Why is this student at high risk?"
- "What should I do first for this student?"
- "How can we improve their attendance?"
- "What are the main concerns for this student?"
- "What financial support options are available?"
- "How is their academic performance trending?"
- "What interventions have the highest priority?"
- "How can we address their engagement issues?"

## Architecture

### Backend Components

1. **chatbot_service.py**: Core chatbot logic and Gemini API integration
2. **chatbot_routes.py**: Flask API endpoints for chat functionality
3. **test_chatbot.py**: Test script for chatbot service

### Frontend Components

1. **ChatbotCard.jsx**: React component for chat interface
2. **ChatbotCard.css**: Styling for chat UI

## API Endpoints

### POST /api/chatbot/chat

Send a message to the chatbot.

**Request:**
```json
{
  "message": "Why is this student at high risk?",
  "student_data": { ... },
  "prediction_data": { ... },
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "error": false,
  "response": "Based on the data, this student is at high risk primarily due to...",
  "session_id": "session_123"
}
```

### POST /api/chatbot/clear-history

Clear conversation history for a session.

**Request:**
```json
{
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Conversation history cleared"
}
```

### GET /api/chatbot/suggestions

Get suggested questions for faculty.

**Response:**
```json
{
  "suggestions": [
    "Why is this student at high risk?",
    "What should I do first for this student?",
    ...
  ]
}
```

## How It Works

1. **Context Building**: When a question is asked, the chatbot receives:
   - Student profile (name, course, year, etc.)
   - Risk assessment (level, percentage, factors)
   - Student metrics (attendance, CGPA, etc.)
   - Recommended interventions

2. **AI Processing**: Gemini 2.5 Flash analyzes the context and generates a response that:
   - References specific data points
   - Provides actionable guidance
   - Maintains professional, empathetic tone
   - Considers conversation history

3. **Response Formatting**: The response includes:
   - Clear paragraphs for explanations
   - Bullet points for lists
   - Bold text for important terms
   - Specific next steps

## Testing

Test the chatbot service:

```bash
cd backend
python gemini/chatbot/test_chatbot.py
```

## Configuration

The chatbot uses the same `GEMINI_API_KEY` from `backend/.env`:

```
GEMINI_API_KEY=your_api_key_here
```

## Conversation History

- Stored in-memory (can be moved to database for persistence)
- Maintains last 10 exchanges (20 messages) per session
- Session ID can be provided or auto-generated
- Can be cleared via API or UI

## UI Features

### Welcome Screen
- Friendly greeting
- Suggested questions to get started
- Clean, inviting interface

### Chat Interface
- User messages (right-aligned, purple gradient)
- Assistant messages (left-aligned, gray background)
- Typing indicator during processing
- Auto-scroll to latest message
- Clear conversation button

### Message Formatting
- Paragraphs for explanations
- Bullet points for lists
- Bold text for emphasis
- Responsive design

## Security & Privacy

- Student data is only sent with each request (not stored by chatbot)
- Conversation history is session-specific
- No persistent storage of sensitive information
- API key is server-side only

## Future Enhancements

- [ ] Database-backed conversation history
- [ ] Multi-user session management
- [ ] Export conversation transcripts
- [ ] Voice input/output
- [ ] Suggested follow-up questions
- [ ] Integration with student management system
- [ ] Analytics on common questions
- [ ] Multilingual support

## Troubleshooting

**Chatbot not responding:**
- Check GEMINI_API_KEY is set in backend/.env
- Verify backend server is running
- Check browser console for errors
- Ensure student and prediction data are available

**Slow responses:**
- Gemini API may take 2-5 seconds
- Check internet connection
- Verify API quota/limits

**Error messages:**
- Check backend logs for detailed error information
- Verify API key is valid
- Ensure request format is correct
