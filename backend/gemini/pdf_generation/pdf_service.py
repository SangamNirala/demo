"""
PDF Report Service
==================

This module generates comprehensive PDF reports for student dropout risk assessments
using Gemini AI for enhanced content generation and ReportLab for PDF creation.
"""

import os
import json
import io
from datetime import datetime
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

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
        """Initialize PDF report service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = "gemini-2.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
        self.is_available = bool(self.api_key)
        
        if not self.is_available:
            print("⚠️  Warning: GEMINI_API_KEY not found - PDF reports will use basic content")
        else:
            print(f"✅ PDF Report Service initialized with {self.model_name}")

    
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
        """Parse Gemini's JSON response"""
        
        response_text = response_text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        elif response_text.startswith('```'):
            response_text = response_text[3:]
        
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        return json.loads(response_text)

    
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
        """Create PDF using ReportLab"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Container for PDF elements
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.white,
            backColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            leftIndent=10,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY
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
        
        # Title
        story.append(Paragraph("🎓 STUDENT DROPOUT RISK ASSESSMENT REPORT", title_style))
        story.append(Paragraph(f"<i>Generated on {timestamp}</i>", ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)))
        story.append(Spacer(1, 0.3*inch))
        
        # Confidentiality notice
        conf_data = [[Paragraph("⚠️ <b>CONFIDENTIAL:</b> This report contains sensitive student information and should be handled according to institutional privacy policies.", body_style)]]
        conf_table = Table(conf_data, colWidths=[6.5*inch])
        conf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
            ('BORDER', (0, 0), (-1, -1), 2, colors.HexColor('#ffc107')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(conf_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        story.append(Paragraph("📋 EXECUTIVE SUMMARY", heading_style))
        story.append(Paragraph(f"<b>{ai_content['executive_summary']['overview']}</b>", body_style))
        story.append(Paragraph(f"<b>Key Concern:</b> {ai_content['executive_summary']['key_concern']}", body_style))
        story.append(Paragraph(f"<b>Immediate Action Required:</b> {ai_content['executive_summary']['immediate_action']}", body_style))
        story.append(Spacer(1, 0.2*inch))

        
        # Student Information
        story.append(Paragraph("👤 STUDENT INFORMATION", heading_style))
        student_info_data = [
            ['Name', name],
            ['Roll Number', roll_no],
            ['Course', course],
            ['Year', year],
        ]
        
        if 'familyIncome' in student_data:
            student_info_data.append(['Family Income', student_data['familyIncome']])
        if 'parentEducation' in student_data:
            student_info_data.append(['Parent Education', student_data['parentEducation']])
        if 'accommodation' in student_data:
            student_info_data.append(['Accommodation', student_data['accommodation']])
        
        student_table = Table(student_info_data, colWidths=[2*inch, 4.5*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(student_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Academic Performance
        story.append(Paragraph("📚 ACADEMIC PERFORMANCE", heading_style))
        academic_data = []
        
        if 'currentCGPA' in student_data:
            academic_data.append(['Current CGPA', str(student_data['currentCGPA'])])
        if 'previousCGPA' in student_data:
            academic_data.append(['Previous CGPA', str(student_data['previousCGPA'])])
        if 'attendance' in student_data:
            academic_data.append(['Attendance', f"{student_data['attendance']}%"])
        if 'assignmentsSubmitted' in student_data:
            academic_data.append(['Assignments Submitted', student_data['assignmentsSubmitted']])
        
        if academic_data:
            academic_table = Table(academic_data, colWidths=[2*inch, 4.5*inch])
            academic_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(academic_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Engagement Metrics
        story.append(Paragraph("📊 ENGAGEMENT METRICS", heading_style))
        engagement_data = []
        
        if 'libraryVisits' in student_data:
            engagement_data.append(['Library Visits', student_data['libraryVisits']])
        if 'lastLMSLogin' in student_data:
            engagement_data.append(['Last LMS Login', student_data['lastLMSLogin']])
        if 'extracurricular' in student_data:
            engagement_data.append(['Extracurricular Activities', student_data['extracurricular']])
        if 'counselorVisits' in student_data:
            engagement_data.append(['Counselor Visits', student_data['counselorVisits']])
        if 'feeStatus' in student_data:
            engagement_data.append(['Fee Status', student_data['feeStatus']])
        
        if engagement_data:
            engagement_table = Table(engagement_data, colWidths=[2*inch, 4.5*inch])
            engagement_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(engagement_table)
        story.append(Spacer(1, 0.2*inch))

        
        # Risk Assessment
        story.append(Paragraph("⚠️ RISK ASSESSMENT", heading_style))
        
        # Risk badge
        risk_colors_map = {
            'HIGH': '#dc3545',
            'MEDIUM': '#ffc107',
            'LOW': '#28a745'
        }
        risk_color = risk_colors_map.get(risk_level, '#6c757d')
        
        risk_badge_data = [[Paragraph(f"<b>{risk_level} RISK - {risk_percentage}%</b>", 
                                      ParagraphStyle('risk', parent=styles['Normal'], fontSize=16, 
                                                    textColor=colors.white, alignment=TA_CENTER))]]
        risk_badge_table = Table(risk_badge_data, colWidths=[6.5*inch])
        risk_badge_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(risk_color)),
            ('PADDING', (0, 0), (-1, -1), 15),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(risk_badge_table)
        story.append(Spacer(1, 0.15*inch))
        
        # Risk factors breakdown
        story.append(Paragraph("<b>Risk Factor Breakdown:</b>", subheading_style))
        for factor in risk_factors:
            factor_name = factor.get('name', factor.get('factor', 'Unknown'))
            contribution = factor.get('contribution', 0)
            description = factor.get('description', '')
            
            factor_text = f"<b>{factor_name}</b> - {contribution}%"
            if description:
                factor_text += f"<br/><i>{description}</i>"
            
            factor_data = [[Paragraph(factor_text, body_style)]]
            factor_table = Table(factor_data, colWidths=[6.5*inch])
            factor_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LINEABOVE', (0, 0), (-1, 0), 4, colors.HexColor('#3498db')),
            ]))
            story.append(factor_table)
            story.append(Spacer(1, 0.08*inch))
        
        # Add chart if available
        if risk_chart_path and os.path.exists(risk_chart_path):
            try:
                img = Image(risk_chart_path, width=6*inch, height=3*inch)
                story.append(Spacer(1, 0.1*inch))
                story.append(img)
            except Exception as e:
                print(f"Warning: Could not add chart to PDF: {e}")
        
        story.append(Spacer(1, 0.2*inch))
        
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

        
        # Intervention Plan
        story.append(Paragraph("🎯 DETAILED INTERVENTION PLAN", heading_style))
        
        intervention_sections = [
            ("🚨 Immediate Actions (Within 48 Hours)", ai_content['intervention_plan']['immediate']),
            ("📅 Short-Term Actions (Within 2 Weeks)", ai_content['intervention_plan']['short_term']),
            ("📆 Medium-Term Actions (Within 1 Month)", ai_content['intervention_plan']['medium_term']),
            ("🔄 Long-Term Strategies (Ongoing)", ai_content['intervention_plan']['long_term'])
        ]
        
        for section_title, actions in intervention_sections:
            story.append(Paragraph(f"<b>{section_title}</b>", subheading_style))
            
            for action in actions:
                action_text = f"<b>{action['action']}</b><br/>"
                action_text += f"<b>Responsible:</b> {action['responsible']}<br/>"
                action_text += f"<b>Expected Outcome:</b> {action['expected_outcome']}"
                
                action_data = [[Paragraph(action_text, body_style)]]
                action_table = Table(action_data, colWidths=[6.5*inch])
                action_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('LINEABOVE', (0, 0), (-1, 0), 4, colors.HexColor('#28a745')),
                ]))
                story.append(action_table)
                story.append(Spacer(1, 0.08*inch))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Resource Requirements
        story.append(Paragraph("💼 RESOURCE REQUIREMENTS", heading_style))
        
        story.append(Paragraph("<b>Personnel Needed:</b>", subheading_style))
        for person in ai_content['resource_requirements']['personnel']:
            story.append(Paragraph(f"• {person}", body_style))
        
        story.append(Paragraph(f"<b>Time Investment:</b> {ai_content['resource_requirements']['time_investment']}", body_style))
        story.append(Paragraph(f"<b>Financial Support:</b> {ai_content['resource_requirements']['financial_support']}", body_style))
        
        story.append(Paragraph("<b>Academic Resources:</b>", subheading_style))
        for resource in ai_content['resource_requirements']['academic_resources']:
            story.append(Paragraph(f"• {resource}", body_style))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Success Metrics
        story.append(Paragraph("📈 SUCCESS METRICS & MONITORING", heading_style))
        
        story.append(Paragraph("<b>Key Performance Indicators (KPIs):</b>", subheading_style))
        for kpi in ai_content['success_metrics']['kpis']:
            story.append(Paragraph(f"• {kpi}", body_style))
        
        story.append(Paragraph("<b>Milestone Checkpoints:</b>", subheading_style))
        for milestone in ai_content['success_metrics']['milestones']:
            story.append(Paragraph(f"• {milestone}", body_style))
        
        story.append(Paragraph("<b>Warning Signs to Watch:</b>", subheading_style))
        for warning in ai_content['success_metrics']['warning_signs']:
            story.append(Paragraph(f"• {warning}", body_style))
        
        story.append(Paragraph(f"<b>Re-evaluation Timeline:</b> {ai_content['success_metrics']['reevaluation_timeline']}", body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Predicted Outcome
        story.append(Paragraph("🔮 PREDICTED OUTCOME", heading_style))
        
        outcome_data = [
            [Paragraph("<b>Without Intervention:</b>", body_style), 
             Paragraph(ai_content['predicted_outcome']['without_intervention'], body_style)],
            [Paragraph("<b>With Intervention:</b>", body_style), 
             Paragraph(ai_content['predicted_outcome']['with_intervention'], body_style)],
            [Paragraph("<b>Success Probability:</b>", body_style), 
             Paragraph(f"<b>{ai_content['predicted_outcome']['success_probability']}</b>", body_style)]
        ]
        
        outcome_table = Table(outcome_data, colWidths=[1.5*inch, 5*inch])
        outcome_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(outcome_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Appendix
        story.append(Paragraph("📎 APPENDIX", heading_style))
        story.append(Paragraph("<b>Risk Calculation Methodology:</b>", subheading_style))
        story.append(Paragraph("This assessment uses a machine learning model trained on historical student data. The model analyzes multiple factors including academic performance, attendance, engagement metrics, and socio-economic indicators to predict dropout risk.", body_style))
        
        story.append(Paragraph("<b>Glossary of Terms:</b>", subheading_style))
        glossary_items = [
            "<b>Risk Level:</b> Overall categorization (HIGH/MEDIUM/LOW) based on dropout probability",
            "<b>Risk Percentage:</b> Numerical probability (0-100%) of student dropout",
            "<b>Risk Factors:</b> Specific areas contributing to overall risk assessment",
            "<b>Intervention:</b> Targeted action to address identified risk factors",
            "<b>KPI:</b> Key Performance Indicator - measurable metric for tracking progress"
        ]
        for item in glossary_items:
            story.append(Paragraph(f"• {item}", body_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Footer note
        footer_text = f"<i>This report was generated using AI-powered analysis and should be used as a guide for intervention planning.<br/>" \
                     f"For questions or concerns, please contact the Student Support Services office.<br/>" \
                     f"<b>Report ID:</b> {roll_no}-{timestamp}</i>"
        story.append(Paragraph(footer_text, ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, 
                                                           textColor=colors.grey, alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
