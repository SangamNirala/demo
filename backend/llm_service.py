"""
LLM Service Module
Handles all interactions with LLM API for chat functionality

SWITCHING BETWEEN EMERGENT LLM AND GEMINI AI:
================================================
1. To use GEMINI AI (Direct): Keep the GEMINI AI section uncommented
2. To use EMERGENT LLM: Comment out GEMINI AI section and uncomment EMERGENT LLM section
3. Make sure the corresponding API key is set in .env file
"""

from dotenv import load_dotenv
import os

load_dotenv()


# ============================================
# OPTION 1: GEMINI AI (Direct Integration) - CURRENTLY ACTIVE
# ============================================

from google import genai
from google.genai import types

class ChatService:
    """Service class for handling chat interactions with Gemini AI directly"""
    
    def __init__(self, system_message: str = "You are a helpful AI assistant.", 
                 model: str = "gemini-2.0-flash-exp"):
        """
        Initialize the chat service with Gemini API key
        
        Args:
            system_message: The personality/behavior instruction for the AI
            model: The Gemini model to use (default: gemini-2.0-flash-exp)
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
            
            print(f"[Gemini/{self.model}] Sending request: {message[:100]}...")
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            
            response_text = response.text
            print(f"[Gemini/{self.model}] Received response: {response_text[:100]}...")
            
            return response_text
            
        except Exception as e:
            print(f"Error in ChatService.generate_response: {str(e)}")
            import traceback
            traceback.print_exc()
            raise


# ============================================
# OPTION 2: EMERGENT LLM (Universal Key) - COMMENTED OUT
# ============================================
# To switch to Emergent LLM:
# 1. Comment out the entire GEMINI AI section above (lines 17-83)
# 2. Uncomment this entire section below
# 3. Make sure EMERGENT_LLM_KEY is set in .env file

# from emergentintegrations.llm.chat import LlmChat, UserMessage
# 
# class ChatService:
#     """Service class for handling chat interactions with Gemini via Emergent LLM"""
#     
#     def __init__(self, system_message: str = "You are a helpful AI assistant.", 
#                  model: str = "gemini-2.5-flash", 
#                  provider: str = "gemini"):
#         """
#         Initialize the chat service with Emergent LLM key
#         
#         Args:
#             system_message: The personality/behavior instruction for the AI
#             model: The model to use (default: gemini-2.5-flash)
#             provider: The LLM provider (default: gemini)
#         """
#         self.api_key = os.getenv("EMERGENT_LLM_KEY")
#         if not self.api_key:
#             raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
#         
#         self.system_message = system_message
#         self.model = model
#         self.provider = provider
#     
#     async def generate_response(self, message: str, conversation_history: list = None) -> str:
#         """
#         Generate AI response using configured model via Emergent LLM
#         
#         Args:
#             message: User's current message
#             conversation_history: List of previous messages in format 
#                                 [{"role": "user/assistant", "content": "..."}]
#         
#         Returns:
#             AI generated response as string
#         """
#         try:
#             # Initialize LlmChat with Emergent LLM key and configure model
#             chat = LlmChat(
#                 api_key=self.api_key,
#                 session_id="chat-session",
#                 system_message=self.system_message
#             ).with_model(self.provider, self.model)
#             
#             # Build conversation context from history
#             conversation_context = ""
#             if conversation_history:
#                 for msg in conversation_history:
#                     role = "User" if msg["role"] == "user" else "Assistant"
#                     conversation_context += f"{role}: {msg['content']}\n"
#             
#             # Combine context with current message
#             full_message = conversation_context + message if conversation_context else message
#             
#             print(f"[{self.provider}/{self.model}] Sending request: {full_message[:100]}...")
#             
#             # Create user message and send
#             user_message = UserMessage(text=full_message)
#             response = await chat.send_message(user_message)
#             
#             print(f"[{self.provider}/{self.model}] Received response: {response[:100]}...")
#             
#             return response
#             
#         except Exception as e:
#             print(f"Error in ChatService.generate_response: {str(e)}")
#             import traceback
#             traceback.print_exc()
#             raise


# ============================================
# Pre-configured Service Instances
# ============================================
# These work with both integrations (same interface)

# Default friendly chatbot
chat_service = ChatService(
    system_message="You are a helpful AI assistant."
)

# Professional chatbot - for business/formal queries
professional_chat_service = ChatService(
    system_message="You are a professional business consultant. Provide detailed, formal, and well-structured responses. Use professional language and industry best practices."
)
