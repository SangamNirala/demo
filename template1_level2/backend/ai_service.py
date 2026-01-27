from google import genai
from config import get_settings

settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

class AIService:
    @staticmethod
    def generate_response(prompt: str, model: str = "gemini-2.0-flash-exp") -> str:
        """Generate AI response using Gemini"""
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")
    
    @staticmethod
    def generate_with_context(message: str, conversation_history: list) -> str:
        """Generate response with conversation context"""
        conversation_context = ""
        for msg in conversation_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation_context += f"{role}: {msg['content']}\n"
        
        full_prompt = conversation_context + f"User: {message}\nAssistant:"
        return AIService.generate_response(full_prompt)
