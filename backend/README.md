# Student Dropout Risk Prediction System - Backend

This is the backend server for the Student Dropout Risk Prediction System. It provides REST APIs for student data retrieval and dropout risk prediction using machine learning.

## Features

- **Student Data Management**: Retrieve student information by roll number
- **ML-Based Predictions**: Predict dropout risk using trained machine learning models
- **Risk Factor Analysis**: Identify key factors contributing to dropout risk
- **Intervention Recommendations**: Generate actionable recommendations for at-risk students
- **RESTful API**: Clean and well-documented API endpoints

## Tech Stack

- **Framework**: Flask 3.0.0
- **ML Libraries**: scikit-learn, pandas, numpy
- **CORS**: Flask-CORS for cross-origin requests
- **Data Format**: JSON

## Project Structure

```
backend/
├── server.py                 # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── database/
│   └── students_data.json   # Student database
├── ml/
│   ├── predict.py           # ML prediction module
│   ├── train.py             # Model training script
│   ├── saved_models/        # Trained model files
│   │   ├── dropout_model.pkl
│   │   ├── scaler.pkl
│   │   ├── feature_names.pkl
│   │   ├── label_encoders.pkl
│   │   └── training_metadata.pkl
│   └── data/
│       └── training_data.csv
├── routes/                   # API route definitions
├── services/                 # Business logic layer
├── schemas/                  # Data validation schemas
└── utils/                    # Helper utilities
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy example env file
   copy .env.example .env
   
   # Edit .env file with your settings (optional)
   ```

5. **Verify model files exist**:
   Ensure the following files are present in `ml/saved_models/`:
   - dropout_model.pkl
   - scaler.pkl
   - feature_names.pkl
   - label_encoders.pkl

## Running the Server

### Development Mode

```bash
python server.py
```

The server will start on `http://localhost:8000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 server:app
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns server status and model loading status.

**Response**:
```json
{
  "status": "healthy",
  "message": "Server is running",
  "model_loaded": true
}
```

### Get Student Data
```
GET /api/student/<roll_no>
```
Retrieve student information by roll number.

**Example**: `GET /api/student/2023CS101`

**Response**:
```json
{
  "student_id": "2023CS101",
  "name": "Rahul Sharma",
  "roll_no": "2023CS101",
  "course": "B.Tech Computer Science",
  "year": 2,
  "attendance_percentage": 58,
  "cgpa_current": 4.8,
  "cgpa_previous": 6.2,
  ...
}
```

### Predict Dropout Risk
```
POST /api/predict/<roll_no>
```
Get dropout risk prediction for a student.

**Example**: `POST /api/predict/2023CS101`

**Response**:
```json
{
  "error": false,
  "student_info": {
    "name": "Rahul Sharma",
    "roll_no": "2023CS101",
    "course": "B.Tech Computer Science",
    "year": "2nd Year"
  },
  "risk_level": "HIGH",
  "risk_percentage": 82.5,
  "risk_factors": [
    {
      "name": "Academic Decline",
      "icon": "📚",
      "contribution": 35.0,
      "description": "Declining grades and poor academic performance"
    },
    ...
  ],
  "recommendations": [
    {
      "id": 1,
      "priority": "high",
      "icon": "📚",
      "title": "Assign Academic Mentor",
      "description": "Pair student with a peer mentor for academic support",
      "action": "assign_mentor"
    },
    ...
  ]
}
```

### List All Students
```
GET /api/students
```
Get a list of all students (for debugging/admin purposes).

## ML Model

The system uses a trained machine learning model to predict dropout risk based on various factors:

### Input Features
- Academic performance (CGPA, grades, units approved)
- Attendance metrics
- Engagement indicators (library visits, LMS activity)
- Financial factors (fee delays, family income)
- Support indicators (counselor visits)
- Demographics (age, gender, distance from college)

### Output
- Dropout probability (0-100%)
- Risk level (LOW, MEDIUM, HIGH)
- Contributing risk factors with weights
- Personalized intervention recommendations

## Configuration

Edit `config.py` or `.env` file to customize:

- Server host and port
- CORS origins
- Database path
- Model file paths
- Risk thresholds

## Troubleshooting

### Model Not Loading
If you see "Model not loaded" errors:
1. Check that all `.pkl` files exist in `ml/saved_models/`
2. Verify file permissions
3. Check Python version compatibility (3.8+)

### CORS Errors
If frontend can't connect:
1. Verify CORS_ORIGINS in config includes your frontend URL
2. Check that Flask-CORS is installed
3. Ensure server is running on correct port

### Student Not Found
If API returns 404:
1. Verify roll number format matches database
2. Check `database/students_data.json` exists and is valid JSON
3. Ensure roll number exists in the database

## Development

### Adding New Endpoints
1. Create route in `routes/` directory
2. Add business logic in `services/`
3. Define schemas in `schemas/`
4. Register blueprint in `server.py`

### Training New Model
```bash
cd ml
python train.py
```

This will retrain the model using data in `ml/data/training_data.csv`

## Testing

Test the API using curl or Postman:

```bash
# Health check
curl http://localhost:8000/api/health

# Get student
curl http://localhost:8000/api/student/2023CS101

# Get prediction
curl -X POST http://localhost:8000/api/predict/2023CS101
```

## License

This project is part of an educational system for student retention.

## Support

For issues or questions, please check the main project README or contact the development team. - Student Dropout Risk Prediction System

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
