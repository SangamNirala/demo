"""
PDF Report Service
==================

This module generates comprehensive PDF reports for student dropout risk assessments
using Gemini AI via Emergent LLM integration for enhanced content generation and ReportLab for PDF creation.
"""

import os
import json
import io
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

# ReportLab imports
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas

# Matplotlib for charts
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()


class PDFReportService:
    """Service for generating AI-powered PDF reports"""
    
    def __init__(self):
        """Initialize PDF report service with Emergent LLM key"""
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.model_name = "gemini-2.5-flash"
        self.provider = "gemini"
        self.is_available = bool(self.api_key)
        
        if not self.is_available:
            print("⚠️  Warning: EMERGENT_LLM_KEY not found - PDF reports will use basic content")
        else:
            print(f"✅ PDF Report Service initialized with {self.model_name} via Emergent LLM")

    
    def generate_report(
        self,
        student_data: Dict,
        prediction_data: Dict
    ) -> bytes:
        """
        Generate comprehensive PDF report
        
        Args:
            student_data: Student information
            prediction_data: Prediction results with risk factors and recommendations
            
        Returns:
            PDF file as bytes
        """
        try:
            # Generate AI-enhanced content
            ai_content = self._generate_ai_content(student_data, prediction_data)
            
            # Generate chart
            risk_chart_path = self._generate_risk_chart(prediction_data.get('risk_factors', []))
            
            # Generate PDF
            pdf_bytes = self._create_pdf(student_data, prediction_data, ai_content, risk_chart_path)
            
            # Clean up chart file
            if risk_chart_path and os.path.exists(risk_chart_path):
                try:
                    os.remove(risk_chart_path)
                except:
                    pass
            
            return pdf_bytes
            
        except Exception as e:
            print(f"❌ Error generating PDF report: {e}")
            import traceback
            traceback.print_exc()
            raise

    
    def _generate_ai_content(self, student_data: Dict, prediction_data: Dict) -> Dict:
        """Generate AI-enhanced report content using Gemini"""
        
        if not self.is_available:
            return self._get_fallback_content(student_data, prediction_data)
        
        try:
            prompt = self._build_report_prompt(student_data, prediction_data)
            response = self._call_gemini_api(prompt)
            content = self._parse_ai_response(response)
            return content
            
        except Exception as e:
            print(f"❌ Error generating AI content: {e}")
            print("⚠️  Using fallback content instead")
            return self._get_fallback_content(student_data, prediction_data)
    
    def _build_report_prompt(self, student_data: Dict, prediction_data: Dict) -> str:
        """Build comprehensive prompt for Gemini AI"""
        
        # Extract key information
        name = student_data.get('name', 'Student')
        roll_no = student_data.get('rollNo', student_data.get('roll_no', 'N/A'))
        course = student_data.get('course', 'N/A')
        year = student_data.get('year', 'N/A')
        
        risk_level = prediction_data.get('riskLevel', prediction_data.get('risk_level', 'UNKNOWN'))
        risk_percentage = prediction_data.get('riskPercentage', prediction_data.get('risk_percentage', 0))
        
        # Format risk factors
        risk_factors = prediction_data.get('riskFactors', prediction_data.get('risk_factors', []))
        risk_factors_text = "\n".join([
            f"- {rf.get('name', rf.get('factor', 'Unknown'))}: {rf.get('contribution', 0)}%"
            for rf in risk_factors[:5]
        ])
        
        # Format student details
        student_details = []
        
        if 'attendance' in student_data:
            student_details.append(f"Attendance: {student_data['attendance']}%")
        if 'currentCGPA' in student_data:
            student_details.append(f"Current CGPA: {student_data['currentCGPA']}")
        if 'previousCGPA' in student_data:
            student_details.append(f"Previous CGPA: {student_data['previousCGPA']}")
        if 'familyIncome' in student_data:
            student_details.append(f"Family Income: {student_data['familyIncome']}")
        if 'feeStatus' in student_data:
            student_details.append(f"Fee Status: {student_data['feeStatus']}")
        if 'libraryVisits' in student_data:
            student_details.append(f"Library Visits: {student_data['libraryVisits']}")
        if 'lastLMSLogin' in student_data:
            student_details.append(f"Last LMS Login: {student_data['lastLMSLogin']}")
        if 'counselorVisits' in student_data:
            student_details.append(f"Counselor Visits: {student_data['counselorVisits']}")
        
        student_context = "\n".join(student_details)
        
        prompt = f"""Generate a comprehensive, professional Student Dropout Risk Assessment Report in JSON format.

STUDENT PROFILE:
- Name: {name}
- Roll Number: {roll_no}
- Course: {course}
- Year: {year}
- Risk Level: {risk_level} ({risk_percentage}%)

RISK FACTORS:
{risk_factors_text}

STUDENT CONTEXT:
{student_context}

Generate a detailed report with the following sections. Return ONLY valid JSON with this exact structure:

{{
  "executive_summary": {{
    "overview": "3-4 sentence comprehensive overview of the student's situation",
    "key_concern": "The single most critical risk factor requiring immediate attention",
    "immediate_action": "Specific action that must be taken within 48 hours"
  }},
  "root_cause_analysis": {{
    "primary_causes": ["List of 3-4 root causes behind the risk factors"],
    "interconnections": "Explanation of how different risk factors are connected",
    "unique_concerns": "Specific concerns unique to this student's situation"
  }},
  "intervention_plan": {{
    "immediate": [
      {{"action": "Specific action", "responsible": "Who", "expected_outcome": "Result", "timeline": "within 48 hours"}}
    ],
    "short_term": [
      {{"action": "Specific action", "responsible": "Who", "expected_outcome": "Result", "timeline": "within 2 weeks"}}
    ],
    "medium_term": [
      {{"action": "Specific action", "responsible": "Who", "expected_outcome": "Result", "timeline": "within 1 month"}}
    ],
    "long_term": [
      {{"action": "Specific action", "responsible": "Who", "expected_outcome": "Result", "timeline": "ongoing"}}
    ]
  }},
  "resource_requirements": {{
    "personnel": ["List of staff needed"],
    "time_investment": "Estimated hours per week",
    "financial_support": "Estimated cost or 'None required'",
    "academic_resources": ["List of resources needed"]
  }},
  "success_metrics": {{
    "kpis": ["List of 4-5 KPIs to track"],
    "milestones": ["List of 3-4 milestones with timeframes"],
    "warning_signs": ["List of 3-4 warning signs"],
    "reevaluation_timeline": "When to reassess"
  }},
  "predicted_outcome": {{
    "without_intervention": "What will likely happen without action",
    "with_intervention": "Expected positive outcome with intervention",
    "success_probability": "Estimated percentage"
  }}
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""

        return prompt

    
    def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API"""
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 4000,
                "response_mime_type": "application/json"
            }
        }
        
        url = f"{self.api_url}?key={self.api_key}"
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if len(parts) > 0 and 'text' in parts[0]:
                    return parts[0]['text']
        
        raise Exception("Invalid response format from Gemini API")
    
    def _parse_ai_response(self, response_text: str) -> Dict:
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
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error at position {e.pos}: {e.msg}")
            print(f"Response text (first 500 chars): {response_text[:500]}")
            print(f"Response text (around error): {response_text[max(0, e.pos-100):min(len(response_text), e.pos+100)]}")
            raise Exception(f"Unterminated string starting at: line {e.lineno} column {e.colno} (char {e.pos})")

    
    def _get_fallback_content(self, student_data: Dict, prediction_data: Dict) -> Dict:
        """Generate fallback content when AI is unavailable"""
        
        risk_level = prediction_data.get('riskLevel', prediction_data.get('risk_level', 'UNKNOWN'))
        
        return {
            "executive_summary": {
                "overview": f"This student has been identified as {risk_level} risk for dropout. Multiple factors contribute to this assessment, requiring coordinated intervention.",
                "key_concern": "Academic performance and engagement levels",
                "immediate_action": "Schedule meeting with academic advisor and student support team"
            },
            "root_cause_analysis": {
                "primary_causes": [
                    "Academic performance challenges",
                    "Attendance and engagement issues",
                    "Potential financial or personal stressors"
                ],
                "interconnections": "Multiple risk factors are likely interconnected, with academic struggles potentially stemming from external stressors.",
                "unique_concerns": "Individual assessment required to identify specific underlying causes."
            },
            "intervention_plan": {
                "immediate": [
                    {
                        "action": "Contact student for urgent meeting",
                        "responsible": "Academic Advisor",
                        "expected_outcome": "Understand immediate concerns",
                        "timeline": "within 48 hours"
                    }
                ],
                "short_term": [
                    {
                        "action": "Develop personalized support plan",
                        "responsible": "Student Support Team",
                        "expected_outcome": "Structured intervention strategy",
                        "timeline": "within 2 weeks"
                    }
                ],
                "medium_term": [
                    {
                        "action": "Monitor progress and adjust interventions",
                        "responsible": "Assigned Mentor",
                        "expected_outcome": "Measurable improvement in key metrics",
                        "timeline": "within 1 month"
                    }
                ],
                "long_term": [
                    {
                        "action": "Ongoing mentorship and support",
                        "responsible": "Academic Advisor & Mentor",
                        "expected_outcome": "Sustained academic success",
                        "timeline": "ongoing"
                    }
                ]
            },
            "resource_requirements": {
                "personnel": ["Academic Advisor", "Peer Mentor", "Counselor"],
                "time_investment": "3-5 hours per week",
                "financial_support": "Assess need for financial aid",
                "academic_resources": ["Tutoring services", "Study groups", "Library resources"]
            },
            "success_metrics": {
                "kpis": [
                    "Attendance rate improvement",
                    "CGPA increase",
                    "Assignment submission rate",
                    "Engagement metrics"
                ],
                "milestones": [
                    "Week 2: Initial improvement in attendance",
                    "Week 4: Academic performance stabilization",
                    "Week 8: Sustained positive trajectory"
                ],
                "warning_signs": [
                    "Continued absence from classes",
                    "Declining grades",
                    "Withdrawal from support services"
                ],
                "reevaluation_timeline": "4 weeks from intervention start"
            },
            "predicted_outcome": {
                "without_intervention": "High likelihood of continued decline and potential dropout",
                "with_intervention": "Strong potential for academic recovery and retention",
                "success_probability": "70-80% with proper intervention"
            }
        }

    
    def _generate_risk_chart(self, risk_factors: List[Dict]) -> Optional[str]:
        """Generate risk factors bar chart and save to temp file"""
        
        try:
            if not risk_factors:
                return None
            
            # Extract data
            factors = [rf.get('name', rf.get('factor', 'Unknown'))[:20] for rf in risk_factors[:5]]
            contributions = [rf.get('contribution', 0) for rf in risk_factors[:5]]
            
            # Create figure
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Create bar chart
            colors_list = ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#17a2b8']
            bars = ax.barh(factors, contributions, color=colors_list[:len(factors)])
            
            # Customize chart
            ax.set_xlabel('Contribution (%)', fontsize=11, fontweight='bold')
            ax.set_title('Risk Factor Contributions', fontsize=13, fontweight='bold', pad=15)
            ax.set_xlim(0, max(contributions) * 1.2)
            
            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, contributions)):
                ax.text(value + 1, i, f'{value}%', va='center', fontsize=9, fontweight='bold')
            
            # Style
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            plt.tight_layout()
            
            # Save to temp file
            chart_path = 'temp_risk_chart.png'
            plt.savefig(chart_path, format='png', dpi=150, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            print(f"❌ Error generating chart: {e}")
            return None

    
    def _create_pdf(
        self,
        student_data: Dict,
        prediction_data: Dict,
        ai_content: Dict,
        risk_chart_path: Optional[str]
    ) -> bytes:
        """Create beautiful PDF using ReportLab with enhanced styling"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            topMargin=0.5*inch, 
            bottomMargin=0.6*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        
        # Container for PDF elements
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Enhanced custom styles with better typography
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=8,
            spaceBefore=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=28
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#5c6bc0'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique',
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.white,
            backColor=colors.HexColor('#3f51b5'),
            spaceAfter=14,
            spaceBefore=16,
            leftIndent=12,
            rightIndent=12,
            fontName='Helvetica-Bold',
            borderPadding=10
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#3f51b5'),
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            leftIndent=5
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#424242'),
            leading=14
        )
        
        bold_body_style = ParagraphStyle(
            'BoldBody',
            parent=body_style,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1a237e')
        )
        
        # Extract data
        name = student_data.get('name', 'Student')
        roll_no = student_data.get('rollNo', student_data.get('roll_no', 'N/A'))
        course = student_data.get('course', 'N/A')
        year = student_data.get('year', 'N/A')
        risk_level = prediction_data.get('riskLevel', prediction_data.get('risk_level', 'UNKNOWN'))
        risk_percentage = prediction_data.get('riskPercentage', prediction_data.get('risk_percentage', 0))
        risk_factors = prediction_data.get('riskFactors', prediction_data.get('risk_factors', []))
        
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # ============================================================
        # COVER PAGE WITH GRADIENT EFFECT
        # ============================================================
        
        # Decorative top border
        top_border_data = [['']]
        top_border = Table(top_border_data, colWidths=[7*inch], rowHeights=[0.3*inch])
        top_border.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#3f51b5')),
            ('LINEBELOW', (0, 0), (-1, -1), 4, colors.HexColor('#1a237e')),
        ]))
        story.append(top_border)
        story.append(Spacer(1, 0.3*inch))
        
        # Main title with icon
        story.append(Paragraph("🎓", ParagraphStyle('icon', parent=title_style, fontSize=36, spaceAfter=10)))
        story.append(Paragraph("STUDENT DROPOUT RISK", title_style))
        story.append(Paragraph("ASSESSMENT REPORT", title_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Subtitle with timestamp
        story.append(Paragraph(f"<i>Generated on {timestamp}</i>", subtitle_style))
        
        # Student info box on cover
        cover_info_data = [
            [Paragraph(f"<b>Student:</b> {name}", body_style)],
            [Paragraph(f"<b>Roll Number:</b> {roll_no}", body_style)],
            [Paragraph(f"<b>Course:</b> {course} | {year}", body_style)]
        ]
        cover_info_table = Table(cover_info_data, colWidths=[5*inch])
        cover_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8eaf6')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3f51b5')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(Spacer(1, 0.3*inch))
        story.append(cover_info_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Confidentiality notice with icon
        conf_text = "🔒 <b>CONFIDENTIAL:</b> This report contains sensitive student information and must be handled according to institutional privacy policies and data protection regulations."
        conf_data = [[Paragraph(conf_text, body_style)]]
        conf_table = Table(conf_data, colWidths=[6.5*inch])
        conf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff9c4')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#f57f17')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(conf_table)
        story.append(Spacer(1, 0.5*inch))
        
        # ============================================================
        # EXECUTIVE SUMMARY - Enhanced with highlight box
        # ============================================================
        story.append(Paragraph("📋 EXECUTIVE SUMMARY", heading_style))
        
        # Overview in highlighted box
        overview_data = [[Paragraph(f"<b>{ai_content['executive_summary']['overview']}</b>", body_style)]]
        overview_table = Table(overview_data, colWidths=[6.5*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e3f2fd')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#2196f3')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 0.12*inch))
        
        # Key points in colored boxes
        key_points = [
            ("🎯 Key Concern", ai_content['executive_summary']['key_concern'], '#ffebee', '#c62828'),
            ("⚡ Immediate Action", ai_content['executive_summary']['immediate_action'], '#e8f5e9', '#2e7d32')
        ]
        
        for icon_title, content, bg_color, border_color in key_points:
            point_data = [[
                Paragraph(f"<b>{icon_title}</b>", subheading_style),
                Paragraph(content, body_style)
            ]]
            point_table = Table(point_data, colWidths=[1.8*inch, 4.7*inch])
            point_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_color)),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor(border_color)),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEAFTER', (0, 0), (0, -1), 1, colors.HexColor(border_color)),
            ]))
            story.append(point_table)
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.15*inch))

        
        # ============================================================
        # STUDENT INFORMATION - Enhanced table design
        # ============================================================
        story.append(Paragraph("👤 STUDENT INFORMATION", heading_style))
        
        student_info_data = [
            [Paragraph('<b>Name</b>', bold_body_style), Paragraph(str(name), body_style)],
            [Paragraph('<b>Roll Number</b>', bold_body_style), Paragraph(str(roll_no), body_style)],
            [Paragraph('<b>Course</b>', bold_body_style), Paragraph(str(course), body_style)],
            [Paragraph('<b>Year</b>', bold_body_style), Paragraph(str(year), body_style)],
        ]
        
        if 'familyIncome' in student_data:
            student_info_data.append([Paragraph('<b>Family Income</b>', bold_body_style), Paragraph(str(student_data['familyIncome']), body_style)])
        if 'parentEducation' in student_data:
            student_info_data.append([Paragraph('<b>Parent Education</b>', bold_body_style), Paragraph(str(student_data['parentEducation']), body_style)])
        if 'accommodation' in student_data:
            student_info_data.append([Paragraph('<b>Accommodation</b>', bold_body_style), Paragraph(str(student_data['accommodation']), body_style)])
        if 'distanceFromCollege' in student_data:
            student_info_data.append([Paragraph('<b>Distance from College</b>', bold_body_style), Paragraph(str(student_data['distanceFromCollege']), body_style)])
        
        student_table = Table(student_info_data, colWidths=[2.2*inch, 4.3*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#424242')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#c5cae9')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3f51b5')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#fafafa')]),
        ]))
        story.append(student_table)
        story.append(Spacer(1, 0.2*inch))
        
        # ============================================================
        # ACADEMIC PERFORMANCE - Enhanced with icons
        # ============================================================
        story.append(Paragraph("📚 ACADEMIC PERFORMANCE", heading_style))
        academic_data = []
        
        if 'currentCGPA' in student_data:
            academic_data.append([Paragraph('<b>📊 Current CGPA</b>', bold_body_style), Paragraph(str(student_data['currentCGPA']), body_style)])
        if 'previousCGPA' in student_data:
            academic_data.append([Paragraph('<b>📈 Previous CGPA</b>', bold_body_style), Paragraph(str(student_data['previousCGPA']), body_style)])
        if 'attendance' in student_data:
            academic_data.append([Paragraph('<b>✅ Attendance</b>', bold_body_style), Paragraph(f"{student_data['attendance']}%", body_style)])
        if 'assignmentsSubmitted' in student_data:
            academic_data.append([Paragraph('<b>📝 Assignments Submitted</b>', bold_body_style), Paragraph(str(student_data['assignmentsSubmitted']), body_style)])
        
        if academic_data:
            academic_table = Table(academic_data, colWidths=[2.2*inch, 4.3*inch])
            academic_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e1f5fe')),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#424242')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#b3e5fc')),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#0288d1')),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#fafafa')]),
            ]))
            story.append(academic_table)
        story.append(Spacer(1, 0.2*inch))
        
        # ============================================================
        # ENGAGEMENT METRICS - Enhanced with icons
        # ============================================================
        story.append(Paragraph("📊 ENGAGEMENT METRICS", heading_style))
        engagement_data = []
        
        if 'libraryVisits' in student_data:
            engagement_data.append([Paragraph('<b>📚 Library Visits</b>', bold_body_style), Paragraph(str(student_data['libraryVisits']), body_style)])
        if 'lastLMSLogin' in student_data:
            engagement_data.append([Paragraph('<b>💻 Last LMS Login</b>', bold_body_style), Paragraph(str(student_data['lastLMSLogin']), body_style)])
        if 'extracurricular' in student_data:
            engagement_data.append([Paragraph('<b>🎯 Extracurricular</b>', bold_body_style), Paragraph(str(student_data['extracurricular']), body_style)])
        if 'counselorVisits' in student_data:
            engagement_data.append([Paragraph('<b>🧠 Counselor Visits</b>', bold_body_style), Paragraph(str(student_data['counselorVisits']), body_style)])
        if 'feeStatus' in student_data:
            engagement_data.append([Paragraph('<b>💰 Fee Status</b>', bold_body_style), Paragraph(str(student_data['feeStatus']), body_style)])
        
        if engagement_data:
            engagement_table = Table(engagement_data, colWidths=[2.2*inch, 4.3*inch])
            engagement_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3e5f5')),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#424242')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e1bee7')),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#8e24aa')),
                ('PADDING', (0, 0), (-1, -1), 10),
                ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#fafafa')]),
            ]))
            story.append(engagement_table)
        story.append(Spacer(1, 0.25*inch))

        
        # ============================================================
        # RISK ASSESSMENT - Enhanced with gradient-style badge
        # ============================================================
        story.append(Paragraph("⚠️ RISK ASSESSMENT", heading_style))
        
        # Risk badge with enhanced styling
        risk_colors_map = {
            'HIGH': ('#d32f2f', '#ffebee'),
            'MEDIUM': ('#f57c00', '#fff3e0'),
            'LOW': ('#388e3c', '#e8f5e9')
        }
        risk_color, risk_bg = risk_colors_map.get(risk_level, ('#757575', '#f5f5f5'))
        
        # Large risk indicator
        risk_badge_data = [[
            Paragraph(f"<b>RISK LEVEL</b>", ParagraphStyle('risk_label', parent=body_style, fontSize=11, textColor=colors.HexColor(risk_color), alignment=TA_CENTER)),
            Paragraph(f"<b>{risk_level}</b>", ParagraphStyle('risk_value', parent=title_style, fontSize=28, textColor=colors.HexColor(risk_color), alignment=TA_CENTER, spaceAfter=0)),
            Paragraph(f"<b>{risk_percentage}%</b>", ParagraphStyle('risk_percent', parent=title_style, fontSize=24, textColor=colors.HexColor(risk_color), alignment=TA_CENTER, spaceAfter=0))
        ]]
        risk_badge_table = Table(risk_badge_data, colWidths=[2*inch, 2.5*inch, 2*inch])
        risk_badge_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(risk_bg)),
            ('BOX', (0, 0), (-1, -1), 3, colors.HexColor(risk_color)),
            ('LINEAFTER', (0, 0), (1, -1), 1, colors.HexColor(risk_color)),
            ('PADDING', (0, 0), (-1, -1), 15),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(risk_badge_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Risk factors breakdown with enhanced styling
        story.append(Paragraph("<b>Risk Factor Breakdown:</b>", subheading_style))
        story.append(Spacer(1, 0.08*inch))
        
        for idx, factor in enumerate(risk_factors):
            factor_name = factor.get('name', factor.get('factor', 'Unknown'))
            contribution = factor.get('contribution', 0)
            description = factor.get('description', '')
            
            # Color coding based on contribution
            if contribution >= 30:
                factor_color = '#d32f2f'
                factor_bg = '#ffebee'
            elif contribution >= 20:
                factor_color = '#f57c00'
                factor_bg = '#fff3e0'
            elif contribution >= 10:
                factor_color = '#fbc02d'
                factor_bg = '#fffde7'
            else:
                factor_color = '#388e3c'
                factor_bg = '#e8f5e9'
            
            factor_text = f"<b>{factor_name}</b> - {contribution}%"
            if description:
                factor_text += f"<br/><font size=9><i>{description}</i></font>"
            
            factor_data = [[Paragraph(factor_text, body_style)]]
            factor_table = Table(factor_data, colWidths=[6.5*inch])
            factor_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(factor_bg)),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LINEABOVE', (0, 0), (-1, 0), 4, colors.HexColor(factor_color)),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(factor_color)),
            ]))
            story.append(factor_table)
            story.append(Spacer(1, 0.08*inch))
        
        # Add chart if available
        if risk_chart_path and os.path.exists(risk_chart_path):
            try:
                story.append(Spacer(1, 0.1*inch))
                img = Image(risk_chart_path, width=6.5*inch, height=3.2*inch)
                story.append(img)
            except Exception as e:
                print(f"Warning: Could not add chart to PDF: {e}")
        
        story.append(Spacer(1, 0.25*inch))
        
        # Root Cause Analysis
        story.append(Paragraph("🔍 ROOT CAUSE ANALYSIS", heading_style))
        story.append(Paragraph("<b>Primary Causes:</b>", subheading_style))
        for cause in ai_content['root_cause_analysis']['primary_causes']:
            story.append(Paragraph(f"• {cause}", body_style))
        
        story.append(Paragraph("<b>Interconnections:</b>", subheading_style))
        story.append(Paragraph(ai_content['root_cause_analysis']['interconnections'], body_style))
        
        story.append(Paragraph("<b>Unique Concerns:</b>", subheading_style))
        story.append(Paragraph(ai_content['root_cause_analysis']['unique_concerns'], body_style))
        story.append(Spacer(1, 0.2*inch))

        
        # ============================================================
        # INTERVENTION PLAN - Enhanced with timeline styling
        # ============================================================
        story.append(Paragraph("🎯 DETAILED INTERVENTION PLAN", heading_style))
        
        intervention_sections = [
            ("🚨 Immediate Actions", "within 48 hours", ai_content['intervention_plan']['immediate'], '#ffebee', '#c62828'),
            ("📅 Short-Term Actions", "within 2 weeks", ai_content['intervention_plan']['short_term'], '#fff3e0', '#e65100'),
            ("📆 Medium-Term Actions", "within 1 month", ai_content['intervention_plan']['medium_term'], '#e3f2fd', '#1565c0'),
            ("🔄 Long-Term Strategies", "ongoing", ai_content['intervention_plan']['long_term'], '#e8f5e9', '#2e7d32')
        ]
        
        for section_icon_title, timeline, actions, bg_color, border_color in intervention_sections:
            # Section header with timeline
            section_header = [[
                Paragraph(f"<b>{section_icon_title}</b>", subheading_style),
                Paragraph(f"<i>{timeline}</i>", ParagraphStyle('timeline', parent=body_style, fontSize=9, textColor=colors.HexColor(border_color), alignment=TA_RIGHT))
            ]]
            header_table = Table(section_header, colWidths=[4.5*inch, 2*inch])
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.08*inch))
            
            for idx, action in enumerate(actions):
                action_text = f"<b>{idx + 1}. {action['action']}</b><br/>"
                action_text += f"<font size=9>👤 <b>Responsible:</b> {action['responsible']}<br/></font>"
                action_text += f"<font size=9>🎯 <b>Expected Outcome:</b> {action['expected_outcome']}</font>"
                
                action_data = [[Paragraph(action_text, body_style)]]
                action_table = Table(action_data, colWidths=[6.5*inch])
                action_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_color)),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor(border_color)),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(border_color)),
                ]))
                story.append(action_table)
                story.append(Spacer(1, 0.08*inch))
            
            story.append(Spacer(1, 0.12*inch))
        
        story.append(Spacer(1, 0.15*inch))
        
        # ============================================================
        # RESOURCE REQUIREMENTS - Enhanced with icon boxes
        # ============================================================
        story.append(Paragraph("💼 RESOURCE REQUIREMENTS", heading_style))
        
        # Personnel in styled box
        personnel_text = "<b>👥 Personnel Needed:</b><br/>"
        for person in ai_content['resource_requirements']['personnel']:
            personnel_text += f"• {person}<br/>"
        
        personnel_data = [[Paragraph(personnel_text, body_style)]]
        personnel_table = Table(personnel_data, colWidths=[6.5*inch])
        personnel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8eaf6')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3f51b5')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(personnel_table)
        story.append(Spacer(1, 0.1*inch))
        
        # Time, Financial, Academic in grid
        resource_grid = [
            [
                Paragraph(f"<b>⏰ Time Investment</b><br/>{ai_content['resource_requirements']['time_investment']}", body_style),
                Paragraph(f"<b>💰 Financial Support</b><br/>{ai_content['resource_requirements']['financial_support']}", body_style)
            ]
        ]
        resource_table = Table(resource_grid, colWidths=[3.25*inch, 3.25*inch])
        resource_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3e0')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#f57c00')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ffb74d')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(resource_table)
        story.append(Spacer(1, 0.1*inch))
        
        # Academic resources
        academic_text = "<b>📚 Academic Resources:</b><br/>"
        for resource in ai_content['resource_requirements']['academic_resources']:
            academic_text += f"• {resource}<br/>"
        
        academic_data = [[Paragraph(academic_text, body_style)]]
        academic_table = Table(academic_data, colWidths=[6.5*inch])
        academic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#388e3c')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(academic_table)
        story.append(Spacer(1, 0.2*inch))
        
        # ============================================================
        # SUCCESS METRICS - Enhanced with visual indicators
        # ============================================================
        story.append(Paragraph("📈 SUCCESS METRICS & MONITORING", heading_style))
        
        # KPIs in styled list
        kpi_text = "<b>🎯 Key Performance Indicators (KPIs):</b><br/>"
        for kpi in ai_content['success_metrics']['kpis']:
            kpi_text += f"✓ {kpi}<br/>"
        
        kpi_data = [[Paragraph(kpi_text, body_style)]]
        kpi_table = Table(kpi_data, colWidths=[6.5*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e3f2fd')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#1976d2')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 0.1*inch))
        
        # Milestones
        milestone_text = "<b>🏁 Milestone Checkpoints:</b><br/>"
        for milestone in ai_content['success_metrics']['milestones']:
            milestone_text += f"▶ {milestone}<br/>"
        
        milestone_data = [[Paragraph(milestone_text, body_style)]]
        milestone_table = Table(milestone_data, colWidths=[6.5*inch])
        milestone_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3e5f5')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#7b1fa2')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(milestone_table)
        story.append(Spacer(1, 0.1*inch))
        
        # Warning signs
        warning_text = "<b>⚠️ Warning Signs to Watch:</b><br/>"
        for warning in ai_content['success_metrics']['warning_signs']:
            warning_text += f"⚡ {warning}<br/>"
        
        warning_data = [[Paragraph(warning_text, body_style)]]
        warning_table = Table(warning_data, colWidths=[6.5*inch])
        warning_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3e0')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#f57c00')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(warning_table)
        story.append(Spacer(1, 0.1*inch))
        
        # Re-evaluation timeline
        timeline_data = [[Paragraph(f"<b>🔄 Re-evaluation Timeline:</b> {ai_content['success_metrics']['reevaluation_timeline']}", body_style)]]
        timeline_table = Table(timeline_data, colWidths=[6.5*inch])
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#388e3c')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(timeline_table)
        story.append(Spacer(1, 0.2*inch))
        
        # ============================================================
        # PREDICTED OUTCOME - Enhanced comparison boxes
        # ============================================================
        story.append(Paragraph("🔮 PREDICTED OUTCOME", heading_style))
        
        outcome_data = [
            [
                Paragraph("<b>❌ Without Intervention</b>", ParagraphStyle('outcome_header', parent=subheading_style, textColor=colors.HexColor('#c62828'))),
                Paragraph(ai_content['predicted_outcome']['without_intervention'], body_style)
            ],
            [
                Paragraph("<b>✅ With Intervention</b>", ParagraphStyle('outcome_header', parent=subheading_style, textColor=colors.HexColor('#2e7d32'))),
                Paragraph(ai_content['predicted_outcome']['with_intervention'], body_style)
            ],
            [
                Paragraph("<b>📊 Success Probability</b>", ParagraphStyle('outcome_header', parent=subheading_style, textColor=colors.HexColor('#1565c0'))),
                Paragraph(f"<b>{ai_content['predicted_outcome']['success_probability']}</b>", bold_body_style)
            ]
        ]
        
        outcome_table = Table(outcome_data, colWidths=[2*inch, 4.5*inch])
        outcome_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#ffebee')),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#ffebee')),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#e8f5e9')),
            ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#e8f5e9')),
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#e3f2fd')),
            ('BACKGROUND', (1, 2), (1, 2), colors.HexColor('#e3f2fd')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3f51b5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#9fa8da')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEAFTER', (0, 0), (0, -1), 2, colors.HexColor('#9fa8da')),
        ]))
        story.append(outcome_table)
        story.append(Spacer(1, 0.25*inch))
        
        # ============================================================
        # APPENDIX - Enhanced with better formatting
        # ============================================================
        story.append(Paragraph("📎 APPENDIX", heading_style))
        
        story.append(Paragraph("<b>Risk Calculation Methodology:</b>", subheading_style))
        methodology_text = "This assessment uses a machine learning model trained on historical student data. The model analyzes multiple factors including academic performance, attendance, engagement metrics, and socio-economic indicators to predict dropout risk with high accuracy."
        methodology_data = [[Paragraph(methodology_text, body_style)]]
        methodology_table = Table(methodology_data, colWidths=[6.5*inch])
        methodology_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafafa')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bdbdbd')),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(methodology_table)
        story.append(Spacer(1, 0.12*inch))
        
        story.append(Paragraph("<b>Glossary of Terms:</b>", subheading_style))
        glossary_items = [
            ("<b>Risk Level:</b>", "Overall categorization (HIGH/MEDIUM/LOW) based on dropout probability"),
            ("<b>Risk Percentage:</b>", "Numerical probability (0-100%) of student dropout"),
            ("<b>Risk Factors:</b>", "Specific areas contributing to overall risk assessment"),
            ("<b>Intervention:</b>", "Targeted action to address identified risk factors"),
            ("<b>KPI:</b>", "Key Performance Indicator - measurable metric for tracking progress")
        ]
        
        glossary_data = [[Paragraph(f"{term} {definition}", body_style)] for term, definition in glossary_items]
        glossary_table = Table(glossary_data, colWidths=[6.5*inch])
        glossary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafafa')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bdbdbd')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(glossary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # ============================================================
        # FOOTER - Enhanced with better styling
        # ============================================================
        footer_text = f"<i>This report was generated using AI-powered analysis and should be used as a guide for intervention planning. " \
                     f"The predictions are based on statistical models and should be combined with professional judgment.<br/><br/>" \
                     f"For questions or concerns, please contact the Student Support Services office.<br/>" \
                     f"<b>Report ID:</b> {roll_no}-{datetime.now().strftime('%Y%m%d-%H%M%S')}</i>"
        
        footer_data = [[Paragraph(footer_text, ParagraphStyle('footer', parent=body_style, fontSize=8, 
                                                           textColor=colors.HexColor('#757575'), alignment=TA_CENTER))]]
        footer_table = Table(footer_data, colWidths=[6.5*inch])
        footer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bdbdbd')),
            ('PADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(footer_table)
        
        # Decorative bottom border
        bottom_border_data = [['']]
        bottom_border = Table(bottom_border_data, colWidths=[7*inch], rowHeights=[0.2*inch])
        bottom_border.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#3f51b5')),
        ]))
        story.append(Spacer(1, 0.2*inch))
        story.append(bottom_border)
        
        # Build PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
