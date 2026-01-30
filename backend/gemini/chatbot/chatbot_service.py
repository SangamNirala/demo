"""
Chatbot Service Module
======================

This module provides an AI-powered chatbot for faculty/admin to ask questions
about students, get insights, and receive guidance.
Uses Emergent LLM key via emergentintegrations library.
"""

import os
import json
from typing import Dict, List, Optional
import asyncio
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Load environment variables from backend/.env
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)


class ChatbotService:
    """Service for AI-powered faculty/admin chatbot using Emergent LLM key"""
    
    def __init__(self):
        """Initialize chatbot service with emergentintegrations"""
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.model_name = "gemini-2.5-flash"
        self.provider = "gemini"
        self.is_available = bool(self.api_key)
        
        # Conversation history (in-memory, can be moved to database)
        self.conversation_history = {}
        
        if not self.is_available:
            print("⚠️  Warning: EMERGENT_LLM_KEY not found for chatbot")
        else:
            print(f"✅ Chatbot service initialized with emergentintegrations using {self.model_name}")
            print(f"   Using Emergent LLM key for chatbot")
    
    def chat(
        self,
        user_message: str,
        student_data: Dict,
        prediction_data: Dict,
        session_id: str = "default"
    ) -> Dict:
        """
        Process a chat message from faculty/admin
        
        Args:
            user_message: The question or message from faculty
            student_data: Current student's data
            prediction_data: Prediction results including risk factors and recommendations
            session_id: Session identifier for conversation history
            
        Returns:
            Dictionary with chatbot response
        """
        if not self.is_available:
            return {
                'error': True,
                'message': 'Chatbot service is not available. Please check API key configuration.'
            }
        
        try:
            # Build context with student information
            context = self._build_context(student_data, prediction_data)
            
            # Get conversation history for this session
            history = self.conversation_history.get(session_id, [])
            
            # Build the system message with context
            system_message = self._build_system_message(context)
            
            # Call emergentintegrations API
            response_text = self._call_llm_api(user_message, system_message, session_id)
            
            # Update conversation history
            history.append({
                'role': 'user',
                'message': user_message
            })
            history.append({
                'role': 'assistant',
                'message': response_text
            })
            
            # Keep only last 10 exchanges (20 messages)
            if len(history) > 20:
                history = history[-20:]
            
            self.conversation_history[session_id] = history
            
            return {
                'error': False,
                'response': response_text,
                'session_id': session_id
            }
            
        except Exception as e:
            print(f"❌ Error in chatbot: {e}")
            import traceback
            traceback.print_exc()
            return {
                'error': True,
                'message': f'Chatbot error: {str(e)}'
            }
    
    def clear_history(self, session_id: str = "default"):
        """Clear conversation history for a session"""
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]
    
    def _build_context(self, student_data: Dict, prediction_data: Dict) -> str:
        """Build context string with student information"""
        
        # Extract student info
        name = student_data.get('name', 'Unknown')
        roll_no = student_data.get('roll_no', 'N/A')
        course = student_data.get('course', 'N/A')
        year = student_data.get('year_string', student_data.get('year', 'N/A'))
        
        # Extract prediction info
        risk_level = prediction_data.get('risk_level', 'UNKNOWN')
        risk_percentage = prediction_data.get('risk_percentage', 0)
        risk_factors = prediction_data.get('risk_factors', [])
        recommendations = prediction_data.get('recommendations', [])
        
        # Build context
        context = f"""STUDENT PROFILE:
- Name: {name}
- Roll Number: {roll_no}
- Course: {course}
- Year: {year}

RISK ASSESSMENT:
- Risk Level: {risk_level}
- Risk Percentage: {risk_percentage}%

TOP RISK FACTORS:
"""
        
        for rf in risk_factors[:5]:
            context += f"- {rf.get('name', 'Unknown')} ({rf.get('contribution', 0)}%): {rf.get('description', '')}\n"
        
        context += "\nSTUDENT METRICS:\n"
        
        # Add relevant metrics
        metrics = [
            ('Attendance', student_data.get('attendance_percentage')),
            ('CGPA Current', student_data.get('cgpa_current', student_data.get('cgpa_semester2'))),
            ('CGPA Previous', student_data.get('cgpa_previous', student_data.get('cgpa_semester1'))),
            ('Assignment Submission Rate', student_data.get('assignment_submission_rate')),
            ('Library Visits (monthly)', student_data.get('library_visits_monthly')),
            ('LMS Last Login (days ago)', student_data.get('lms_last_login_days')),
            ('Fee Payment Delay (months)', student_data.get('fee_payment_delay_months')),
            ('Counselor Visits', student_data.get('counselor_visits')),
            ('Family Income', student_data.get('family_income')),
        ]
        
        for metric_name, value in metrics:
            if value is not None:
                context += f"- {metric_name}: {value}\n"
        
        context += "\nRECOMMENDED INTERVENTIONS:\n"
        for idx, rec in enumerate(recommendations[:5], 1):
            context += f"{idx}. {rec.get('title', 'Unknown')} (Priority: {rec.get('priority', 'medium')})\n"
        
        return context
    
    def _build_system_message(self, context: str) -> str:
        """Build the system message for emergentintegrations"""
        
        system_prompt = f"""You are an expert educational counselor and student success advisor AI assistant. You help faculty and administrators understand student risk factors, provide actionable guidance, and answer questions about student performance and interventions.

GUIDELINES:
1. Be professional, empathetic, and solution-focused
2. Provide specific, actionable advice based on the student data
3. Reference specific metrics and risk factors when explaining
4. Suggest concrete next steps when asked for guidance
5. Be concise but thorough (2-4 paragraphs maximum)
6. Use bullet points for lists and action items
7. Maintain student privacy and confidentiality
8. If asked to compare, use the data provided to make meaningful comparisons

RESPONSE FORMAT:
- Use clear paragraphs for explanations
- Use bullet points (•) for lists
- Use **bold** for important terms and actions
- Keep responses focused and actionable

CURRENT STUDENT CONTEXT:
{context}
"""
        return system_prompt
    
    def _call_llm_api(self, user_message: str, system_message: str, session_id: str) -> str:
        """Call emergentintegrations LLM API"""
        
        try:
            # Create LlmChat instance with system message
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_message
            )
            
            # Configure to use Gemini model
            chat.with_model(self.provider, self.model_name)
            
            # Create user message
            message = UserMessage(text=user_message)
            
            # Send message and get response (sync wrapper for async)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(chat.send_message(message))
                return response
            finally:
                loop.close()
                
        except Exception as e:
            print(f"❌ Error calling emergentintegrations API: {e}")
            import traceback
            traceback.print_exc()
            raise


# Singleton instance
chatbot_service = ChatbotService()
