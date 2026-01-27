from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Initialize LlmChat with Emergent LLM key and configure for Gemini
        chat = LlmChat(
            api_key=os.getenv("EMERGENT_LLM_KEY"),
            session_id=f"chat-session",
            system_message="You are a helpful AI assistant."
        ).with_model("gemini", "gemini-2.5-flash")
        
        # Build conversation context from history
        conversation_context = ""
        for msg in request.conversation_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation_context += f"{role}: {msg['content']}\n"
        
        # Combine context with current message
        full_message = conversation_context + request.message if conversation_context else request.message
        
        print(f"Sending request to Gemini with message: {full_message[:100]}...")
        
        # Create user message and send
        user_message = UserMessage(text=full_message)
        response = await chat.send_message(user_message)
        
        print(f"Received response: {response[:100]}...")
        
        return ChatResponse(response=response)
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
