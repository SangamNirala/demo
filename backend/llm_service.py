"""
LLM Service Module
Handles all interactions with Emergent LLM API for chat functionality
"""

from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
import os

load_dotenv()


class ChatService:
    """Service class for handling chat interactions with Gemini via Emergent LLM"""
    
    def __init__(self):
        """Initialize the chat service with Emergent LLM key"""
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    async def generate_response(self, message: str, conversation_history: list = None) -> str:
        """
        Generate AI response using Gemini model via Emergent LLM
        
        Args:
            message: User's current message
            conversation_history: List of previous messages in format 
                                [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            AI generated response as string
        """
        try:
            # Initialize LlmChat with Emergent LLM key and configure for Gemini
            chat = LlmChat(
                api_key=self.api_key,
                session_id="chat-session",
                system_message="You are a helpful AI assistant."
            ).with_model("gemini", "gemini-2.5-flash")
            
            # Build conversation context from history
            conversation_context = ""
            if conversation_history:
                for msg in conversation_history:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation_context += f"{role}: {msg['content']}\n"
            
            # Combine context with current message
            full_message = conversation_context + message if conversation_context else message
            
            print(f"Sending request to Gemini: {full_message[:100]}...")
            
            # Create user message and send
            user_message = UserMessage(text=full_message)
            response = await chat.send_message(user_message)
            
            print(f"Received response: {response[:100]}...")
            
            return response
            
        except Exception as e:
            print(f"Error in ChatService.generate_response: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


# Create a singleton instance
chat_service = ChatService()
