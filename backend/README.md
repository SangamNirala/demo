# Backend - Student Dropout Risk Prediction System

## Overview
Flask-based REST API backend for the Student Dropout Risk Prediction System. Provides endpoints for student data retrieval and dropout risk prediction.

## Features
- 🔍 Student data lookup by roll number
- 🎯 Risk prediction with ML-based scoring
- 📊 Risk factor analysis
- 💡 Automated intervention recommendations
- 📁 JSON-based data storage (easily replaceable with database)

## Tech Stack
- Python 3.8+
- Flask (Web framework)
- Flask-CORS (Cross-origin support)

## Setup

### Prerequisites
- Python 3.8 or higher
- pip or virtualenv

### Installation

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
copy .env.example .env
```

### Running the Server

Start the development server:
```bash
python server.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
```
GET /api/health
```
Returns server status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Server is running"
}
```

### 2. Get Student Data
```
GET /api/student/<roll_no>
```
Retrieves student information by roll number.

**Example:**
```
GET /api/student/12345
```

**Response:**
```json
{
  "name": "Rahul Sharma",
  "rollNo": "12345",
  "course": "B.Tech Computer Science",
  "year": "2nd Year",
  "attendance": 58,
  "currentCGPA": 4.8,
  ...
}
```

### 3. Predict Dropout Risk
```
POST /api/predict/<roll_no>
```
Generates dropout risk prediction for a student.

**Example:**
```
POST /api/predict/12345
```

**Response:**
```json
{
  "riskLevel": "HIGH",
  "riskPercentage": 82,
  "riskFactors": [
    {
      "name": "Academic Decline",
      "contribution": 35
    },
    ...
  ],
  "recommendations": [
    {
      "icon": "📞",
      "text": "Schedule a meeting with academic advisor"
    },
    ...
  ]
}
```

## Sample Student Roll Numbers

Test the system with these roll numbers:
- `12345` - High risk student (Rahul Sharma)
- `2023CS101` - Low risk student (Priya Patel)
- `2023ME205` - Medium risk student (Amit Kumar)
- `2023EC150` - Low risk student (Sneha Reddy)
- `2023CV078` - High risk student (Vikram Singh)

## Risk Calculation Logic

The system calculates risk based on multiple factors:

1. **Attendance** (up to 35 points)
   - < 60%: High risk
   - 60-75%: Medium risk

2. **CGPA Decline** (25 points)
   - Current CGPA < Previous CGPA

3. **Financial Stress** (20 points)
   - Fee payment delays

4. **Mental Health** (15 points)
   - Counselor visits for stress/anxiety

5. **Low Engagement** (5 points)
   - No extracurricular participation

**Risk Levels:**
- HIGH: Score ≥ 70
- MEDIUM: Score 40-69
- LOW: Score < 40

## Database Structure

Currently uses JSON file (`database/students_data.json`). Can be easily replaced with:
- PostgreSQL
- MySQL
- MongoDB
- SQLite

## Future Enhancements

- [ ] Integrate actual ML model (scikit-learn, XGBoost)
- [ ] Add database support (PostgreSQL/MySQL)
- [ ] Implement authentication & authorization
- [ ] Add bulk student upload
- [ ] Create admin dashboard endpoints
- [ ] Add intervention tracking
- [ ] Email/SMS notification system
- [ ] Historical trend analysis

## Development

### Adding New Students

Edit `database/students_data.json`:
```json
{
  "NEW_ROLL_NO": {
    "name": "Student Name",
    "rollNo": "NEW_ROLL_NO",
    ...
  }
}
```

### Customizing Risk Logic

Modify the `calculate_risk()` function in `server.py` to adjust:
- Risk factor weights
- Threshold values
- Recommendation rules

## Troubleshooting

**Port already in use:**
```bash
# Change port in server.py
app.run(host='0.0.0.0', port=8001, debug=True)
```

**CORS errors:**
- Ensure Flask-CORS is installed
- Check frontend API_URL in `.env`

**Student not found:**
- Verify roll number exists in `students_data.json`
- Check for exact match (case-sensitive)
