"""
Gemini Service Module
=====================

This module provides AI-powered personalized intervention recommendations
using Google's Gemini API.
"""

import os
import json
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiService:
    """Service for generating personalized recommendations using Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        # Using Gemini 2.5 Flash model
        self.model_name = "gemini-2.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
        self.is_available = bool(self.api_key)
        
        if not self.is_available:
            print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
            print("   Falling back to static recommendations")
        else:
            print(f"✅ Gemini AI service initialized with {self.model_name}")
    
    def generate_personalized_recommendations(
        self,
        student_data: Dict,
        risk_percentage: float,
        risk_factors: List[Dict],
        risk_level: str
    ) -> List[Dict]:
        """
        Generate personalized intervention recommendations using Gemini AI
        
        Args:
            student_data: Student information dictionary
            risk_percentage: Calculated risk percentage
            risk_factors: List of risk factor dictionaries
            risk_level: Risk level (HIGH, MEDIUM, LOW)
            
        Returns:
            List of personalized recommendation dictionaries
        """
        if not self.is_available:
            return self._get_fallback_recommendations(risk_factors, risk_percentage)
        
        try:
            # Build context for Gemini
            prompt = self._build_prompt(student_data, risk_percentage, risk_factors, risk_level)
            
            # Call Gemini API
            response = self._call_gemini_api(prompt)
            
            # Parse and format recommendations
            recommendations = self._parse_gemini_response(response, risk_level)
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Error generating Gemini recommendations: {e}")
            print("   Falling back to static recommendations")
            return self._get_fallback_recommendations(risk_factors, risk_percentage)
    
    def _build_prompt(
        self,
        student_data: Dict,
        risk_percentage: float,
        risk_factors: List[Dict],
        risk_level: str
    ) -> str:
        """Build the prompt for Gemini API"""
        
        # Extract key student information
        name = student_data.get('name', 'Student')
        course = student_data.get('course', 'N/A')
        year = student_data.get('year_string', student_data.get('year', 'N/A'))
        
        # Format risk factors
        risk_factors_text = "\n".join([
            f"- {rf['name']} ({rf['contribution']}%): {rf['description']}"
            for rf in risk_factors[:3]
        ])
        
        # Build detailed context
        context_details = []
        
        # Academic context
        cgpa_current = student_data.get('cgpa_current', student_data.get('cgpa_semester2'))
        cgpa_previous = student_data.get('cgpa_previous', student_data.get('cgpa_semester1'))
        if cgpa_current:
            context_details.append(f"Current CGPA: {cgpa_current}")
        if cgpa_previous:
            context_details.append(f"Previous CGPA: {cgpa_previous}")
        
        # Attendance
        attendance = student_data.get('attendance_percentage')
        if attendance is not None:
            context_details.append(f"Attendance: {attendance}%")
        
        # Financial
        fee_delay = student_data.get('fee_payment_delay_months', 0)
        if fee_delay > 0:
            context_details.append(f"Fee payment delayed by {fee_delay} months")
        
        # Engagement
        library_visits = student_data.get('library_visits_monthly', 0)
        context_details.append(f"Library visits: {library_visits}/month")
        
        lms_days = student_data.get('lms_last_login_days', 0)
        if lms_days > 0:
            context_details.append(f"Last LMS login: {lms_days} days ago")
        
        # Counselor visits
        counselor_visits = student_data.get('counselor_visits', 0)
        if counselor_visits > 0:
            context_details.append(f"Counselor visits: {counselor_visits}")
        
        context_text = "\n".join(context_details)
        
        # Build the prompt
        prompt = f"""You are an expert educational counselor and student success advisor. Analyze the following student's situation and provide 5 personalized, actionable intervention recommendations.

STUDENT PROFILE:
- Name: {name}
- Course: {course}
- Year: {year}
- Dropout Risk Level: {risk_level} ({risk_percentage}%)

TOP RISK FACTORS:
{risk_factors_text}

DETAILED CONTEXT:
{context_text}

TASK:
Generate exactly 5 personalized intervention recommendations. Each recommendation should be:
1. Specific to this student's situation
2. Actionable and practical
3. Prioritized based on urgency
4. Empathetic and supportive in tone

For each recommendation, provide:
- A clear, concise title (max 6 words)
- A description in BULLET POINT format with key terms in **bold** for emphasis
- Priority level: "urgent", "high", "medium", or "low"
- An appropriate emoji icon

DESCRIPTION FORMAT REQUIREMENTS:
- Use 2-4 bullet points separated by " | " (pipe character)
- Keep each bullet point to 1-2 short sentences
- Use **bold** for key actions, important terms, and outcomes
- Make it scannable and easy to read
- Focus on actionable steps

Example description format:
"• **Connect immediately** with the financial aid office to explore payment plans and emergency funds | • **Address the 3-month delay** to reduce stress and allow focus on academics | • This will **alleviate financial burden** and improve overall well-being"

Format your response as a JSON array with this exact structure:
[
  {{
    "title": "Recommendation Title",
    "description": "• **Bold key action** with explanation | • **Another key point** with brief detail | • Expected **outcome** or benefit",
    "priority": "high",
    "icon": "📚"
  }}
]

CRITICAL JSON FORMATTING RULES:
- Use " | " (space-pipe-space) to separate bullet points, NOT newlines
- Ensure all strings are on a single line
- No line breaks within string values
- Valid JSON syntax only

IMPORTANT:
- Make recommendations specific to the student's actual problems
- Consider the interconnection between risk factors
- Prioritize interventions that address multiple issues
- Be empathetic and solution-focused
- Use varied, relevant emojis for each recommendation
- ALWAYS use bullet points (•) and **bold** formatting in descriptions
- Return ONLY the JSON array, no additional text"""

        return prompt
    
    def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API with the prompt"""
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 3000,  # Increased for longer responses
                "response_mime_type": "application/json"  # Request JSON response
            }
        }
        
        url = f"{self.api_url}?key={self.api_key}"
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract text from response
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if len(parts) > 0 and 'text' in parts[0]:
                    return parts[0]['text']
        
        raise Exception("Invalid response format from Gemini API")
    
    def _parse_gemini_response(self, response_text: str, risk_level: str) -> List[Dict]:
        """Parse Gemini's response and format recommendations"""
        
        try:
            # Extract JSON from response (handle markdown code blocks)
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            elif response_text.startswith('```'):
                response_text = response_text[3:]
            
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Try to parse JSON directly first
            try:
                recommendations_raw = json.loads(response_text)
            except json.JSONDecodeError as e:
                # If parsing fails, try to fix common issues
                print(f"⚠️  Initial JSON parse failed, attempting to fix...")
                
                # Try to fix incomplete JSON by completing it
                # Check if it's just missing closing brackets
                if not response_text.endswith(']'):
                    # Count opening and closing brackets
                    open_braces = response_text.count('{')
                    close_braces = response_text.count('}')
                    open_brackets = response_text.count('[')
                    close_brackets = response_text.count(']')
                    
                    # Add missing closing characters
                    if open_braces > close_braces:
                        # Find the last complete object
                        last_complete = response_text.rfind('},')
                        if last_complete > 0:
                            response_text = response_text[:last_complete + 1]
                    
                    # Add missing closing bracket
                    if open_brackets > close_brackets:
                        response_text += ']'
                
                # Try parsing again
                recommendations_raw = json.loads(response_text)
            
            # Format recommendations
            recommendations = []
            for idx, rec in enumerate(recommendations_raw[:5]):  # Limit to 5
                recommendations.append({
                    'id': idx + 1,
                    'title': rec.get('title', 'Intervention Needed'),
                    'description': rec.get('description', 'Please consult with advisor.'),
                    'priority': rec.get('priority', 'medium'),
                    'icon': rec.get('icon', '💡'),
                    'action': f"gemini_recommendation_{idx + 1}"
                })
            
            # Add urgent intervention for high risk if not already present
            if risk_level == 'HIGH' and not any(r['priority'] == 'urgent' for r in recommendations):
                recommendations.insert(0, {
                    'id': 0,
                    'title': 'Immediate Intervention Required',
                    'description': '• **Schedule urgent meeting** with student, advisor, and support team | • **Address critical risk factors** immediately | • This intervention is **time-sensitive** and requires immediate action',
                    'priority': 'urgent',
                    'icon': '🚨',
                    'action': 'urgent_intervention'
                })
                recommendations = recommendations[:5]  # Keep only 5
            
            print(f"✅ Successfully parsed {len(recommendations)} Gemini recommendations")
            return recommendations
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing Gemini response as JSON: {e}")
            print(f"   Response text (first 500 chars): {response_text[:500]}...")
            # Save full response for debugging
            with open('gemini_error_response.txt', 'w', encoding='utf-8') as f:
                f.write(response_text)
            print(f"   Full response saved to gemini_error_response.txt")
            raise
        except Exception as e:
            print(f"❌ Error formatting Gemini recommendations: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _get_fallback_recommendations(
        self,
        risk_factors: List[Dict],
        risk_percentage: float
    ) -> List[Dict]:
        """Get static fallback recommendations when Gemini is unavailable"""
        
        recommendations = []
        top_factors = [rf['category'] for rf in risk_factors[:3]]
        
        # Static recommendation templates
        all_recommendations = {
            'academic_decline': [
                {
                    'id': 1,
                    'priority': 'high',
                    'icon': '📚',
                    'title': 'Assign Academic Mentor',
                    'description': 'Pair student with a peer mentor for academic support and study guidance.',
                    'action': 'assign_mentor'
                },
                {
                    'id': 2,
                    'priority': 'medium',
                    'icon': '📝',
                    'title': 'Academic Counseling Session',
                    'description': 'Schedule a session with academic advisor to discuss study strategies.',
                    'action': 'schedule_academic_counseling'
                }
            ],
            'low_attendance': [
                {
                    'id': 3,
                    'priority': 'high',
                    'icon': '📞',
                    'title': 'Contact Student',
                    'description': 'Reach out to understand reasons for low attendance.',
                    'action': 'contact_student'
                },
                {
                    'id': 4,
                    'priority': 'medium',
                    'icon': '👨‍👩‍👦',
                    'title': 'Parent Meeting',
                    'description': 'Schedule a meeting with parents to discuss attendance concerns.',
                    'action': 'schedule_parent_meeting'
                }
            ],
            'financial_stress': [
                {
                    'id': 5,
                    'priority': 'high',
                    'icon': '💰',
                    'title': 'Financial Aid Review',
                    'description': 'Connect with Financial Aid office for scholarship or fee waiver options.',
                    'action': 'financial_aid_review'
                },
                {
                    'id': 6,
                    'priority': 'medium',
                    'icon': '📋',
                    'title': 'Payment Plan',
                    'description': 'Discuss flexible payment plan options with accounts department.',
                    'action': 'setup_payment_plan'
                }
            ],
            'mental_health': [
                {
                    'id': 7,
                    'priority': 'high',
                    'icon': '🧠',
                    'title': 'Counselor Referral',
                    'description': 'Refer to mental health counselor for follow-up session.',
                    'action': 'counselor_referral'
                },
                {
                    'id': 8,
                    'priority': 'medium',
                    'icon': '🤝',
                    'title': 'Peer Support Group',
                    'description': 'Connect with peer support group or student wellness program.',
                    'action': 'peer_support'
                }
            ],
            'low_engagement': [
                {
                    'id': 9,
                    'priority': 'medium',
                    'icon': '🎯',
                    'title': 'Activity Recommendation',
                    'description': 'Encourage participation in clubs or extracurricular activities.',
                    'action': 'recommend_activities'
                },
                {
                    'id': 10,
                    'priority': 'low',
                    'icon': '📖',
                    'title': 'Library Resources',
                    'description': 'Introduce student to library resources and study groups.',
                    'action': 'library_orientation'
                }
            ]
        }
        
        # Add recommendations based on top risk factors
        for factor in top_factors:
            if factor in all_recommendations:
                recommendations.extend(all_recommendations[factor])
        
        # Add urgent recommendation for high risk
        if risk_percentage >= 60:
            recommendations.insert(0, {
                'id': 0,
                'priority': 'urgent',
                'icon': '🚨',
                'title': 'Immediate Intervention Required',
                'description': 'Schedule urgent meeting with student, advisor, and support team.',
                'action': 'urgent_intervention'
            })
        
        # Remove duplicates and limit to 5
        seen_ids = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['id'] not in seen_ids:
                seen_ids.add(rec['id'])
                unique_recommendations.append(rec)
        
        return unique_recommendations[:5]
