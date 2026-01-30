# 🚀 Quick Start Guide - PDF Report Feature

## ⚡ 5-Minute Setup

### 1. Install Dependencies

```bash
cd backend
pip install reportlab matplotlib pillow jinja2
```

### 2. Verify Installation

```bash
python gemini/pdf_generation/test_pdf.py
```

Expected output:
```
✅ Service initialized (Gemini available: True)
✅ PDF generated successfully
✅ PDF saved successfully
```

### 3. Start Backend Server

```bash
python server.py
```

You should see:
```
✅ PDF Report Service initialized with gemini-2.5-flash
🌐 Server starting on http://localhost:8001
  POST /api/pdf/generate/<roll_no>    - Generate PDF report
```

### 4. Start Frontend

```bash
cd frontend
npm run dev
```

### 5. Test the Feature

1. Open http://localhost:5173
2. Enter roll number: `2023CS101`
3. Click "Analyze"
4. Click "Generate Risk Prediction"
5. Click "📄 Download Detailed Report"
6. PDF downloads automatically!

---

## 📋 API Quick Reference

### Generate PDF Report

```bash
POST http://localhost:8001/api/pdf/generate/{roll_no}
Content-Type: application/json

{
  "student_data": { ... },
  "prediction_data": { ... }
}
```

### Health Check

```bash
GET http://localhost:8001/api/pdf/health
```

---

## 🎯 What You Get

✅ **10+ Page Comprehensive Report**
- Executive Summary (AI-generated)
- Student Profile & Academic Data
- Risk Assessment with Charts
- Root Cause Analysis (AI-generated)
- Detailed Intervention Plans
- Resource Requirements
- Success Metrics
- Predicted Outcomes

✅ **Professional Formatting**
- Color-coded risk indicators
- Tables and charts
- Structured sections
- Confidentiality notices

✅ **AI-Powered Insights**
- Personalized analysis
- Specific recommendations
- Timeline-based action plans

---

## 🔧 Troubleshooting

### PDF not generating?
```bash
# Check if service is running
curl http://localhost:8001/api/pdf/health

# Test with sample data
cd backend
python gemini/pdf_generation/test_pdf.py
```

### Missing dependencies?
```bash
pip install -r requirements.txt
```

### Gemini API not working?
- Check `.env` file has `GEMINI_API_KEY`
- Service will use fallback content automatically

---

## 📁 Key Files

```
backend/
├── gemini/pdf_generation/
│   ├── pdf_service.py          # Main service
│   ├── pdf_routes.py           # API endpoints
│   ├── test_pdf.py             # Test script
│   └── README.md               # Full documentation

frontend/
└── src/components/DownloadReportButton/
    ├── DownloadReportButton.jsx
    ├── DownloadReportButton.css
    └── index.js
```

---

## 🎉 That's It!

Your PDF Report Generation feature is ready to use!

For detailed documentation, see:
- `backend/gemini/pdf_generation/README.md`
- `PDF_REPORT_FEATURE_COMPLETE.md`
