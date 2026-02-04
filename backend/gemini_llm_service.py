"""
Gemini AI LLM Service Module
Direct integration with Google's Gemini AI API
"""

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()


class ChatService:
    """Service class for handling chat interactions with Gemini AI directly"""
    
    def __init__(self, system_message: str = "You are a helpful AI assistant.", 
                 model: str = "gemini-2.5-flash"):
        """
        Initialize the chat service with Gemini API key
        
        Args:
            system_message: The personality/behavior instruction for the AI
            model: The Gemini model to use (default: gemini-2.5-flash)
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)
        
        self.system_message = system_message
        self.model = model
    
    async def generate_response(self, message: str, conversation_history: list = None) -> str:
        """
        Generate AI response using Gemini AI
        
        Args:
            message: User's current message
            conversation_history: List of previous messages in format 
                                [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            AI generated response as string
        """
        try:
            # Build conversation history for Gemini
            contents = []
            
            # Add system instruction as first user message (workaround for system instruction)
            if self.system_message and (not conversation_history or len(conversation_history) == 0):
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part(text=f"System instruction: {self.system_message}\n\nUser: {message}")]
                ))
            else:
                # Add conversation history
                if conversation_history:
                    for msg in conversation_history:
                        role = "user" if msg["role"] == "user" else "model"
                        contents.append(types.Content(
                            role=role,
                            parts=[types.Part(text=msg["content"])]
                        ))
                
                # Add current message
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part(text=message)]
                ))
            
            print(f"[Gemini AI/{self.model}] Sending request: {message[:100]}...")
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            
            response_text = response.text
            print(f"[Gemini AI/{self.model}] Received response: {response_text[:100]}...")
            
            return response_text
            
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
