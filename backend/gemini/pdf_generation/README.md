# 📄 PDF Report Generation Module

## Overview

The PDF Report Generation module provides AI-powered comprehensive PDF reports for student dropout risk assessments. It uses **Google Gemini AI** to generate detailed analysis and **ReportLab** to create professionally formatted PDF documents.

## Features

✅ **AI-Powered Content Generation**
- Executive summary with key insights
- Root cause analysis
- Detailed intervention plans (immediate, short-term, medium-term, long-term)
- Resource requirements assessment
- Success metrics and monitoring guidelines
- Predicted outcomes with and without intervention

✅ **Professional PDF Formatting**
- Clean, structured layout with proper sections
- Color-coded risk indicators
- Data tables for student information
- Visual charts for risk factor breakdown
- Confidentiality notices
- Page numbering and metadata

✅ **Comprehensive Report Sections**
1. Executive Summary
2. Student Information
3. Academic Performance
4. Engagement Metrics
5. Risk Assessment with visual charts
6. Root Cause Analysis
7. Detailed Intervention Plan
8. Resource Requirements
9. Success Metrics & Monitoring
10. Predicted Outcomes
11. Appendix with methodology

## Installation

### Required Packages

```bash
pip install reportlab matplotlib pillow jinja2 requests python-dotenv
```

All dependencies are listed in `backend/requirements.txt`.

### Environment Setup

Ensure your `.env` file contains:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### 1. Import the Service

```python
from gemini.pdf_generation import PDFReportService

# Initialize service
pdf_service = PDFReportService()
```

### 2. Prepare Data

```python
# Student data
student_data = {
    "name": "Rahul Sharma",
    "rollNo": "2023CS101",
    "course": "B.Tech Computer Science",
    "year": "2nd Year",
    "familyIncome": "₹3,00,000/year",
    "parentEducation": "High School",
    "attendance": 58,
    "currentCGPA": 4.8,
    "previousCGPA": 6.2,
    # ... more fields
}

# Prediction data
prediction_data = {
    "riskLevel": "HIGH",
    "riskPercentage": 82,
    "riskFactors": [
        {
            "name": "Academic Decline",
            "contribution": 35,
            "description": "Significant drop in CGPA"
        },
        # ... more factors
    ]
}
```

### 3. Generate PDF

```python
# Generate PDF report
pdf_bytes = pdf_service.generate_report(student_data, prediction_data)

# Save to file
with open('report.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

## API Endpoints

### Generate PDF Report

**Endpoint:** `POST /api/pdf/generate/<roll_no>`

**Request Body:**
```json
{
  "student_data": {
    "name": "Student Name",
    "rollNo": "2023CS101",
    "course": "B.Tech Computer Science",
    "year": "2nd Year",
    "attendance": 58,
    "currentCGPA": 4.8,
    "previousCGPA": 6.2,
    "familyIncome": "₹3,00,000/year",
    "parentEducation": "High School",
    "distanceFromCollege": "45 km",
    "accommodation": "Day Scholar",
    "assignmentsSubmitted": "4 out of 10",
    "libraryVisits": "0 visits in 2 months",
    "feeStatus": "2 months delayed",
    "counselorVisits": "Visited 2 times for stress",
    "extracurricular": "No participation",
    "lastLMSLogin": "15 days ago"
  },
  "prediction_data": {
    "riskLevel": "HIGH",
    "riskPercentage": 82,
    "riskFactors": [
      {
        "name": "Academic Decline",
        "contribution": 35,
        "description": "Significant drop in CGPA from 6.2 to 4.8"
      },
      {
        "name": "Low Attendance",
        "contribution": 25,
        "description": "Attendance at 58%, below minimum requirement"
      }
    ]
  }
}
```

**Response:**
- Content-Type: `application/pdf`
- File download with name: `Risk_Report_{roll_no}_{student_name}.pdf`

**Example cURL:**
```bash
curl -X POST http://localhost:8001/api/pdf/generate/2023CS101 \
  -H "Content-Type: application/json" \
  -d @request_data.json \
  --output report.pdf
```

### Health Check

**Endpoint:** `GET /api/pdf/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "PDF Report Generation",
  "gemini_available": true
}
```

## Testing

### Run Test Script

```bash
cd backend
python gemini/pdf_generation/test_pdf.py
```

This will:
1. Initialize the PDF service
2. Generate a test report with sample data
3. Save the PDF as `test_report.pdf`
4. Verify all components are working

### Expected Output

```
============================================================
🧪 Testing PDF Report Generation
============================================================

1️⃣  Initializing PDF Report Service...
   ✅ Service initialized (Gemini available: True)

2️⃣  Generating PDF report...
   ✅ PDF generated successfully (62819 bytes)

3️⃣  Saving PDF to test_report.pdf...
   ✅ PDF saved successfully

============================================================
✅ ALL TESTS PASSED!
============================================================

📄 Test report saved as: test_report.pdf
```

## Architecture

### Components

1. **pdf_service.py** - Core PDF generation service
   - AI content generation using Gemini
   - Chart generation using Matplotlib
   - PDF creation using ReportLab
   - Fallback content when AI is unavailable

2. **pdf_routes.py** - Flask API routes
   - `/api/pdf/generate/<roll_no>` - Generate and download PDF
   - `/api/pdf/health` - Service health check

3. **test_pdf.py** - Test script
   - Validates PDF generation functionality
   - Creates sample report for verification

### Data Flow

```
User Request
    ↓
Flask Route (pdf_routes.py)
    ↓
PDFReportService.generate_report()
    ↓
├─→ _generate_ai_content() → Gemini API
├─→ _generate_risk_chart() → Matplotlib
└─→ _create_pdf() → ReportLab
    ↓
PDF Bytes
    ↓
Download Response
```

## AI Content Generation

### Gemini Prompt Structure

The service sends a comprehensive prompt to Gemini AI requesting:

1. **Executive Summary**
   - 3-4 sentence overview
   - Key concern identification
   - Immediate action recommendation

2. **Root Cause Analysis**
   - Primary causes (3-4 items)
   - Interconnections between factors
   - Unique student concerns

3. **Intervention Plan**
   - Immediate actions (48 hours)
   - Short-term actions (2 weeks)
   - Medium-term actions (1 month)
   - Long-term strategies (ongoing)

4. **Resource Requirements**
   - Personnel needed
   - Time investment
   - Financial support
   - Academic resources

5. **Success Metrics**
   - KPIs to track
   - Milestone checkpoints
   - Warning signs
   - Re-evaluation timeline

6. **Predicted Outcomes**
   - Without intervention
   - With intervention
   - Success probability

### Fallback Mechanism

If Gemini AI is unavailable or fails, the service automatically uses pre-defined fallback content to ensure reports can still be generated.

## PDF Styling

### Color Scheme

- **Headers:** Dark blue (#2c3e50)
- **HIGH Risk:** Red (#dc3545)
- **MEDIUM Risk:** Yellow (#ffc107)
- **LOW Risk:** Green (#28a745)
- **Info Boxes:** Light gray (#ecf0f1)
- **Intervention Boxes:** Light green (#e8f5e9)

### Typography

- **Title:** Helvetica-Bold, 20pt
- **Headings:** Helvetica-Bold, 14pt, white on dark blue
- **Subheadings:** Helvetica-Bold, 12pt
- **Body:** Helvetica, 10pt

### Layout

- **Page Size:** Letter (8.5" x 11")
- **Margins:** 0.75" all sides
- **Tables:** Bordered with alternating row colors
- **Spacing:** Consistent spacing between sections

## Error Handling

The service includes comprehensive error handling:

1. **Gemini API Failures:** Falls back to static content
2. **Chart Generation Errors:** Continues without chart
3. **Missing Data:** Uses default values or skips optional sections
4. **PDF Creation Errors:** Provides detailed error messages

## Performance

- **Average Generation Time:** 3-5 seconds (with Gemini AI)
- **PDF File Size:** 50-100 KB (depending on content)
- **Chart Generation:** ~0.5 seconds
- **AI Content Generation:** 2-4 seconds

## Security Considerations

1. **Confidentiality Notice:** Included in every report
2. **Data Privacy:** No data is stored; reports generated on-demand
3. **API Key Security:** Gemini API key stored in environment variables
4. **Input Validation:** All input data is validated before processing

## Troubleshooting

### Issue: Gemini API not working

**Solution:**
- Check if `GEMINI_API_KEY` is set in `.env`
- Verify API key is valid
- Service will use fallback content automatically

### Issue: Chart not appearing in PDF

**Solution:**
- Ensure matplotlib is installed
- Check if risk_factors data is provided
- Service continues without chart if generation fails

### Issue: PDF generation fails

**Solution:**
- Check all required packages are installed
- Verify student_data and prediction_data are properly formatted
- Check error logs for specific issues

## Future Enhancements

- [ ] Multi-language support
- [ ] Custom branding/logo support
- [ ] Email delivery integration
- [ ] Batch report generation
- [ ] Report templates customization
- [ ] Historical comparison charts
- [ ] Digital signatures

## Dependencies

```
reportlab>=4.0.0      # PDF generation
matplotlib>=3.8.0     # Chart generation
pillow>=10.0.0        # Image processing
jinja2>=3.1.2         # Template rendering (future use)
requests>=2.31.0      # API calls
python-dotenv>=1.0.0  # Environment variables
```

## License

This module is part of the Student Dropout Risk Prediction System.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review test script output
3. Check server logs for detailed error messages
4. Verify all dependencies are installed

## Version History

### v1.0.0 (Current)
- Initial release
- AI-powered content generation
- Professional PDF formatting
- Comprehensive report sections
- Chart visualization
- Fallback mechanism
