# How to Add New AI Services

This guide explains how to add new AI-powered features to your application using the existing `llm_service.py`.

## Quick Start

### Option 1: Use Pre-configured Services (Easiest)

The `llm_service.py` already has pre-configured services ready to use:

```python
from llm_service import chat_service, professional_chat_service

# In your endpoint:
response = await chat_service.generate_response(message, conversation_history)
# OR
response = await professional_chat_service.generate_response(message, conversation_history)
```

### Option 2: Create Custom Service Instance

For new AI features, create a new service instance in `llm_service.py`:

```python
# Add to llm_service.py at the bottom:

# Creative writing assistant
creative_chat_service = ChatService(
    system_message="You are a creative writing assistant. Help users write stories, poems, and creative content with vivid descriptions and engaging narratives."
)

# Technical support bot
tech_support_service = ChatService(
    system_message="You are a technical support specialist. Provide clear, step-by-step solutions to technical problems."
)

# Language tutor
language_tutor_service = ChatService(
    system_message="You are a friendly language tutor. Help users learn new languages through conversation, corrections, and explanations."
)
```

### Option 3: Dynamic Service Creation

For runtime configuration, create instances on the fly:

```python
from llm_service import ChatService

# Create a custom service with specific behavior
custom_service = ChatService(
    system_message="Your custom personality here",
    model="gemini-2.5-flash",  # or "gpt-5.2", "claude-sonnet-4-5-20250929"
    provider="gemini"  # or "openai", "anthropic"
)

response = await custom_service.generate_response(message, history)
```

## Complete Example: Adding a Professional Chatbot Button

### Step 1: Service is Already Created
The `professional_chat_service` is already defined in `llm_service.py`

### Step 2: Add API Endpoint (Already Done)
```python
# In server.py
from llm_service import professional_chat_service

@app.post("/api/chat/professional")
async def professional_chat(request: ChatRequest):
    response = await professional_chat_service.generate_response(
        message=request.message,
        conversation_history=request.conversation_history
    )
    return ChatResponse(response=response)
```

### Step 3: Add Frontend Button (Your Next Step)
```jsx
// In App.jsx - add a button to toggle professional mode
const [isProfessionalMode, setIsProfessionalMode] = useState(false);

// Update the API call
const endpoint = isProfessionalMode ? '/api/chat/professional' : '/api/chat';
const response = await axios.post(endpoint, {
    message: input,
    conversation_history: messages
});

// Add toggle button in your UI
<button onClick={() => setIsProfessionalMode(!isProfessionalMode)}>
  {isProfessionalMode ? 'Professional Mode' : 'Casual Mode'}
</button>
```

## Available Models

You can use different models for different services:

### Gemini (Google)
- `gemini-2.5-flash` (default, fastest)
- `gemini-2.5-pro` (more powerful)
- `gemini-3-flash-preview`
- `gemini-3-pro-preview`

### OpenAI
- `gpt-5.2` (latest)
- `gpt-5.1` (recommended)
- `gpt-5-mini` (faster, cheaper)

### Anthropic
- `claude-sonnet-4-5-20250929`
- `claude-4-sonnet-20250514` (recommended)
- `claude-opus-4-5-20251101` (most powerful)

## Example Use Cases

### Code Assistant
```python
code_assistant_service = ChatService(
    system_message="You are an expert programmer. Provide clean, well-documented code with explanations.",
    model="gpt-5.2",
    provider="openai"
)
```

### Medical Info Bot (Disclaimer: Not for diagnosis)
```python
health_info_service = ChatService(
    system_message="You are a health information assistant. Provide general health information but always remind users to consult healthcare professionals for medical advice.",
    model="claude-sonnet-4-5-20250929",
    provider="anthropic"
)
```

### Customer Service Bot
```python
customer_service = ChatService(
    system_message="You are a friendly customer service representative. Be empathetic, helpful, and professional. Always aim to resolve issues quickly."
)
```

## Tips

1. **System Message is Key**: The system message defines the AI's personality and behavior
2. **Reuse the Same Key**: All services use the same `EMERGENT_LLM_KEY` automatically
3. **Different Models for Different Tasks**: Use faster models (gemini-flash) for simple tasks, powerful models (gpt-5.2, claude-opus) for complex reasoning
4. **Conversation History**: Always pass conversation history for context-aware responses
5. **Error Handling**: The service includes built-in error handling and logging

## Testing Your New Service

Test via curl:
```bash
# Test regular chat
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": []}'

# Test professional chat
curl -X POST http://localhost:8001/api/chat/professional \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze this business strategy", "conversation_history": []}'
```
