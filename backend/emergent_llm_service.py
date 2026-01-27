"""
Emergent LLM Service Module
Universal LLM integration using Emergent's Universal Key
Supports OpenAI, Anthropic, and Gemini through a single API key
"""

from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
import os

load_dotenv()


class ChatService:
    """Service class for handling chat interactions with Gemini via Emergent LLM"""
    
    def __init__(self, system_message: str = "You are a helpful AI assistant.", 
                 model: str = "gemini-2.5-flash", 
                 provider: str = "gemini"):
        """
        Initialize the chat service with Emergent LLM key
        
        Args:
            system_message: The personality/behavior instruction for the AI
            model: The model to use (default: gemini-2.5-flash)
            provider: The LLM provider (default: gemini)
        """
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
        
        self.system_message = system_message
        self.model = model
        self.provider = provider
    
    async def generate_response(self, message: str, conversation_history: list = None) -> str:
        """
        Generate AI response using configured model via Emergent LLM
        
        Args:
            message: User's current message
            conversation_history: List of previous messages in format 
                                [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            AI generated response as string
        """
        try:
            # Initialize LlmChat with Emergent LLM key and configure model
            chat = LlmChat(
                api_key=self.api_key,
                session_id="chat-session",
                system_message=self.system_message
            ).with_model(self.provider, self.model)
            
            # Build conversation context from history
            conversation_context = ""
            if conversation_history:
                for msg in conversation_history:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation_context += f"{role}: {msg['content']}\n"
            
            # Combine context with current message
            full_message = conversation_context + message if conversation_context else message
            
            print(f"[Emergent LLM/{self.provider}/{self.model}] Sending request: {full_message[:100]}...")
            
            # Create user message and send
            user_message = UserMessage(text=full_message)
            response = await chat.send_message(user_message)
            
            print(f"[Emergent LLM/{self.provider}/{self.model}] Received response: {response[:100]}...")
            
            return response
            
        except Exception as e:
            print(f"Error in ChatService.generate_response: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


# ============================================
# Pre-configured Service Instances
# ============================================

# Default friendly chatbot
chat_service = ChatService(
    system_message="You are a helpful AI assistant."
)

# Professional chatbot - for business/formal queries
professional_chat_service = ChatService(
    system_message="You are a professional business consultant. Provide detailed, formal, and well-structured responses. Use professional language and industry best practices."
)
