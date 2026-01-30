# 🎓 Student Dropout Risk Prediction System

An intelligent system for early identification of at-risk students and proactive intervention recommendations.

## 🌟 Features

- **Student Search**: Quick lookup by roll number
- **Comprehensive Analysis**: View static profile and dynamic performance data
- **Risk Prediction**: ML-based dropout risk assessment
- **Risk Factors**: Visual breakdown of contributing factors
- **Smart Recommendations**: Automated intervention suggestions
- **Action Tracking**: Mark contacted, schedule meetings, assign mentors

## 🏗️ Architecture

```
├── Frontend (React + Vite)
│   ├── Search Interface
│   ├── Student Profile Display
│   ├── Risk Dashboard
│   └── Recommendations Panel
│
└── Backend (Flask REST API)
    ├── Student Data Management
    ├── Risk Calculation Engine
    └── JSON Database
```

## 🚀 Quick Start

### Prerequisites

- **Frontend**: Node.js 16+ or Yarn
- **Backend**: Python 3.8+

### Installation & Setup

#### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

Backend will run on `http://localhost:8000`

#### 2. Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
yarn install

# Run development server
yarn dev
```

Frontend will run on `http://localhost:5173`

## 🧪 Testing the System

### Sample Student Roll Numbers

Try these roll numbers to see different risk levels:

| Roll Number | Student Name | Risk Level | Description |
|------------|--------------|------------|-------------|
| `12345` | Rahul Sharma | 🔴 HIGH | Low attendance, declining grades, financial stress |
| `2023CS101` | Priya Patel | 🟢 LOW | Good performance, active engagement |
| `2023ME205` | Amit Kumar | 🟡 MEDIUM | Moderate attendance, some concerns |
| `2023EC150` | Sneha Reddy | 🟢 LOW | Excellent student, no risk factors |
| `2023CV078` | Vikram Singh | 🔴 HIGH | Multiple risk factors, urgent intervention needed |

### Usage Flow

1. **Enter Roll Number**: Type `12345` in the search box
2. **Click "Analyze Student"**: View student profile and performance data
3. **Click "Generate Risk Prediction"**: See risk assessment
4. **Review Results**: 
   - Risk level and percentage
   - Contributing factors with weights
   - Recommended interventions
5. **Take Action**: Use action buttons to track interventions

## 📊 Risk Calculation

The system evaluates multiple factors:

- **Attendance** (35% weight): < 60% triggers high risk
- **Academic Performance** (25% weight): Declining CGPA
- **Financial Status** (20% weight): Fee payment delays
- **Mental Health** (15% weight): Counselor visits
- **Engagement** (5% weight): Extracurricular participation

**Risk Levels:**
- 🔴 **HIGH**: Score ≥ 70 (Immediate intervention required)
- 🟡 **MEDIUM**: Score 40-69 (Monitor closely)
- 🟢 **LOW**: Score < 40 (Minimal risk)

## 📁 Project Structure

```
student-dropout-prediction/
├── frontend/
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── pages/           # Main pages
│   │   ├── services/        # API integration
│   │   └── styles/          # Global styles
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── database/
│   │   └── students_data.json  # Student records
│   ├── routes/              # API routes (future)
│   ├── services/            # Business logic (future)
│   ├── ml/                  # ML models (future)
│   ├── server.py            # Main server
│   └── requirements.txt
│
└── README.md
```

## 🔌 API Endpoints

### Get Student Data
```http
GET /api/student/<roll_no>
```

### Predict Dropout Risk
```http
POST /api/predict/<roll_no>
```

### Health Check
```http
GET /api/health
```

## 🎨 UI Components

- **SearchSection**: Student roll number input
- **StudentProfileCard**: Static student information
- **OngoingDataCard**: Dynamic performance metrics
- **PredictionButton**: Trigger risk analysis
- **RiskAlertCard**: Risk level display
- **RiskFactorsCard**: Factor breakdown with progress bars
- **RecommendationsCard**: Intervention suggestions
- **Loader**: Loading spinner

## 🔮 Future Enhancements

### Phase 1 (Current)
- ✅ Basic UI with all components
- ✅ Mock data and risk calculation
- ✅ REST API endpoints

### Phase 2 (Next)
- [ ] Real ML model integration (scikit-learn/XGBoost)
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] User authentication
- [ ] Admin dashboard

### Phase 3 (Advanced)
- [ ] Historical trend analysis
- [ ] Bulk student upload
- [ ] Email/SMS notifications
- [ ] Intervention tracking system
- [ ] Parent portal
- [ ] Mobile app

## 🛠️ Development

### Adding New Students

Edit `backend/database/students_data.json`:

```json
{
  "NEW_ROLL_NO": {
    "name": "Student Name",
    "rollNo": "NEW_ROLL_NO",
    "course": "B.Tech Course Name",
    "year": "Year",
    "attendance": 75,
    "currentCGPA": 7.0,
    ...
  }
}
```

### Customizing Risk Logic

Modify `calculate_risk()` in `backend/server.py` to adjust:
- Factor weights
- Threshold values
- Recommendation rules

### Styling

Edit CSS variables in `frontend/src/styles/global.css`:

```css
:root {
  --primary-color: #667eea;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --success-color: #10b981;
}
```

## 🐛 Troubleshooting

**Backend not starting:**
- Check if port 8000 is available
- Verify Python version (3.8+)
- Ensure all dependencies are installed

**Frontend not connecting:**
- Verify backend is running on port 8000
- Check `.env` file has correct `VITE_API_URL`
- Clear browser cache

**Student not found:**
- Verify roll number exists in `students_data.json`
- Check for exact match (case-sensitive)

**CORS errors:**
- Ensure Flask-CORS is installed
- Backend should allow all origins in development

## 📝 License

This project is for educational purposes.

## 👥 Contributing

Contributions welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ for better student outcomes**
