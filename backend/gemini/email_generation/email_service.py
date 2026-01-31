"""
Email Generation Service
========================

This module generates personalized emails using Gemini AI via Emergent LLM integration for student outreach.
"""

import os
import json
import asyncio
from typing import Dict, Optional
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()


class EmailGenerationService:
    """Service for generating AI-powered personalized emails"""
    
    def __init__(self):
        """Initialize email generation service with Emergent LLM key"""
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.model_name = "gemini-2.5-flash"
        self.provider = "gemini"
        self.is_available = bool(self.api_key)
        
        if not self.is_available:
            print("⚠️  Warning: EMERGENT_LLM_KEY not found - Email generation unavailable")
        else:
            print(f"✅ Email Generation Service initialized with {self.model_name} via Emergent LLM")

    def generate_email(
        self,
        email_type: str,
        student_data: Dict,
        prediction_data: Dict,
        additional_notes: Optional[str] = None,
        meeting_details: Optional[Dict] = None
    ) -> Dict:
        """
        Generate personalized email using Gemini AI via Emergent LLM
        
        Args:
            email_type: Type of email (student, parent, meeting)
            student_data: Student information
            prediction_data: Prediction results
            additional_notes: Optional custom notes
            meeting_details: Optional meeting details (date, time, location)
            
        Returns:
            Dictionary with subject and body
        """
        
        if not self.is_available:
            raise Exception("Email generation service is not available. Please configure EMERGENT_LLM_KEY.")
        
        try:
            prompt = self._build_email_prompt(
                email_type, 
                student_data, 
                prediction_data, 
                additional_notes, 
                meeting_details
            )
            
            response = self._call_gemini_api(prompt)
            email_content = self._parse_response(response)
            
            return email_content
            
        except Exception as e:
            print(f"❌ Error generating email: {e}")
            raise

    def _build_email_prompt(
        self,
        email_type: str,
        student_data: Dict,
        prediction_data: Dict,
        additional_notes: Optional[str],
        meeting_details: Optional[Dict]
    ) -> str:
        """Build prompt for Gemini AI based on email type"""
        
        # Extract student information
        name = student_data.get('name', 'Student')
        roll_no = student_data.get('rollNo', student_data.get('roll_no', 'N/A'))
        course = student_data.get('course', 'N/A')
        year = student_data.get('year', 'N/A')
        
        # Extract prediction data
        risk_level = prediction_data.get('riskLevel', prediction_data.get('risk_level', 'UNKNOWN'))
        risk_percentage = prediction_data.get('riskPercentage', prediction_data.get('risk_percentage', 0))
        risk_factors = prediction_data.get('riskFactors', prediction_data.get('risk_factors', []))
        
        # Format risk factors
        risk_factors_text = "\n".join([
            f"- {rf.get('name', rf.get('factor', 'Unknown'))}: {rf.get('contribution', 0)}%"
            for rf in risk_factors[:5]
        ])
        
        # Build context
        context = f"""
STUDENT INFORMATION:
- Name: {name}
- Roll Number: {roll_no}
- Course: {course}
- Year: {year}

RISK ASSESSMENT (Internal Use Only - DO NOT mention in email):
- Risk Level: {risk_level}
- Risk Percentage: {risk_percentage}%

KEY AREAS NEEDING SUPPORT:
{risk_factors_text}
"""
        
        if additional_notes:
            context += f"\n\nADDITIONAL CONTEXT:\n{additional_notes}"
        
        if meeting_details:
            context += f"""

MEETING DETAILS:
- Date: {meeting_details.get('date', 'TBD')}
- Time: {meeting_details.get('time', 'TBD')}
- Location: {meeting_details.get('location', 'TBD')}
"""
        
        # Email type specific prompts
        if email_type == 'student':
            return self._build_student_email_prompt(name, context)
        elif email_type == 'parent':
            return self._build_parent_email_prompt(name, context)
        elif email_type == 'meeting':
            return self._build_meeting_email_prompt(name, context, meeting_details)
        else:
            raise ValueError(f"Invalid email type: {email_type}")

    def _build_student_email_prompt(self, name: str, context: str) -> str:
        """Build prompt for student email"""
        
        return f"""{context}

Generate a warm, supportive, and encouraging email to the student.

CRITICAL REQUIREMENTS:
1. DO NOT mention risk percentages, dropout risk, or that they are "flagged"
2. Use a warm, friendly, and non-judgmental tone
3. Frame this as a regular check-in and support opportunity
4. Invite them for a friendly chat
5. Express that support is available
6. Make them feel valued and cared for
7. Keep it brief and positive (150-200 words)

Return ONLY valid JSON with this structure:
{{
  "subject": "Brief, friendly subject line",
  "body": "Complete email body with proper formatting and line breaks"
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""

    def _build_parent_email_prompt(self, name: str, context: str) -> str:
        """Build prompt for parent email"""
        
        return f"""{context}

Generate a formal, sensitive, and professional email to the student's parents.

CRITICAL REQUIREMENTS:
1. DO NOT use alarming words like "dropout risk", "failing", or "danger"
2. Frame concerns as "areas where additional support would be beneficial"
3. Use a respectful, professional, and reassuring tone
4. Request a meeting or phone call to discuss support strategies
5. Emphasize partnership between institution and parents
6. Express confidence in the student's potential
7. Keep it professional yet warm (200-250 words)

Return ONLY valid JSON with this structure:
{{
  "subject": "Professional, non-alarming subject line",
  "body": "Complete email body with proper formatting and line breaks"
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""

    def _build_meeting_email_prompt(self, name: str, context: str, meeting_details: Optional[Dict]) -> str:
        """Build prompt for meeting invitation"""
        
        return f"""{context}

Generate a friendly, casual meeting invitation email.

CRITICAL REQUIREMENTS:
1. Frame as a regular check-in, NOT a serious concern
2. Use a friendly, approachable, and non-threatening tone
3. Include the meeting date, time, and location clearly
4. Provide option to reschedule if needed
5. Make it sound like a normal part of student support
6. Keep it brief and casual (150-180 words)

Return ONLY valid JSON with this structure:
{{
  "subject": "Friendly meeting invitation subject",
  "body": "Complete email body with meeting details and proper formatting"
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""

    def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API using Emergent LLM integration"""
        
        try:
            # Create a unique session ID for this request
            session_id = f"email_{hash(prompt) % 1000000}"
            
            # Initialize LlmChat with Emergent key
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message="You are an expert at writing professional, empathetic emails for educational institutions."
            ).with_model(self.provider, self.model_name)
            
            # Create user message
            user_message = UserMessage(text=prompt)
            
            # Send message and get response (run async in sync context)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(chat.send_message(user_message))
            finally:
                loop.close()
            
            return response
            
        except Exception as e:
            print(f"❌ Error calling Gemini API via Emergent: {e}")
            raise Exception(f"Failed to call Gemini API: {e}")

    def _parse_response(self, response_text: str) -> Dict:
        """Parse Gemini's JSON response with robust error handling"""
        
        response_text = response_text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        elif response_text.startswith('```'):
            response_text = response_text[3:]
        
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        try:
            # Try to parse as-is first
            parsed = json.loads(response_text)
            
            # Validate structure
            if 'subject' not in parsed or 'body' not in parsed:
                raise ValueError("Response missing required fields: subject and body")
            
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing failed, trying regex extraction...")
            
            # Try to extract subject and body using regex as fallback
            try:
                import re
                
                # Extract the entire JSON-like structure
                # Find subject
                subject_match = re.search(r'"subject"\s*:\s*"([^"]+)"', response_text)
                
                # Find body - match everything between "body": " and the closing "
                # This handles newlines and escaped characters
                body_match = re.search(r'"body"\s*:\s*"(.*?)"\s*\}', response_text, re.DOTALL)
                
                if not body_match:
                    # Try alternative pattern
                    body_match = re.search(r'"body"\s*:\s*"(.*?)$', response_text, re.DOTALL)
                
                if subject_match and body_match:
                    subject = subject_match.group(1)
                    body = body_match.group(1)
                    
                    # Decode escape sequences
                    body = body.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
                    subject = subject.replace('\\n', ' ').replace('\\"', '"')
                    
                    print("✅ Successfully extracted email using regex fallback")
                    return {
                        'subject': subject.strip(),
                        'body': body.strip()
                    }
                else:
                    print(f"❌ Could not extract subject or body from response")
                    print(f"Subject found: {bool(subject_match)}, Body found: {bool(body_match)}")
                    if subject_match:
                        print(f"Subject: {subject_match.group(1)[:100]}")
                    
            except Exception as regex_error:
                print(f"❌ Regex extraction failed: {regex_error}")
                import traceback
                traceback.print_exc()
            
            # If all else fails, raise the original error
            raise Exception(f"Failed to parse AI response: {e}")


# Global instance
email_service = EmailGenerationService()
