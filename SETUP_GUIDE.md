# 🚀 Quick Setup Guide

## Step-by-Step Installation

### 1️⃣ Backend Setup (5 minutes)

Open a terminal/command prompt:

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py
```

✅ You should see: `Running on http://0.0.0.0:8000`

**Keep this terminal open!**

---

### 2️⃣ Frontend Setup (5 minutes)

Open a **NEW** terminal/command prompt:

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
yarn install
# OR if you don't have yarn:
npm install

# Start development server
yarn dev
# OR:
npm run dev
```

✅ You should see: `Local: http://localhost:5173`

**Keep this terminal open too!**

---

### 3️⃣ Test the Application

1. Open your browser and go to: **http://localhost:5173**

2. You should see the Student Dropout Risk Prediction System

3. Try entering roll number: **12345**

4. Click **"🔍 Analyze Student"**

5. You'll see student data appear

6. Click **"🔮 Generate Risk Prediction"**

7. You'll see the risk assessment with recommendations!

---

## 🎯 Quick Test Roll Numbers

| Roll Number | Expected Result |
|------------|-----------------|
| `12345` | HIGH RISK (82%) - Multiple issues |
| `2023CS101` | LOW RISK - Good student |
| `2023CV078` | HIGH RISK (95%) - Critical case |

---

## ⚡ Using the Batch Files (Windows Only)

Even easier! Just double-click:

1. **START_BACKEND.bat** - Starts backend server
2. **START_FRONTEND.bat** - Starts frontend server

---

## 🐛 Common Issues

### Issue: "python not found"
**Solution**: Install Python 3.8+ from python.org

### Issue: "yarn not found"
**Solution**: Use `npm` instead, or install yarn: `npm install -g yarn`

### Issue: Port 8000 already in use
**Solution**: 
- Close other applications using port 8000
- OR change port in `backend/server.py` line 145:
  ```python
  app.run(host='0.0.0.0', port=8001, debug=True)
  ```
  And update `frontend/.env`:
  ```
  VITE_API_URL=http://localhost:8001
  ```

### Issue: "Student not found"
**Solution**: Make sure you're using one of these roll numbers:
- 12345
- 2023CS101
- 2023ME205
- 2023EC150
- 2023CV078

### Issue: Frontend shows error connecting to backend
**Solution**: 
1. Make sure backend is running (check terminal)
2. Check `frontend/.env` has: `VITE_API_URL=http://localhost:8000`
3. Restart frontend server

---

## 📱 What You Should See

### 1. Search Page
- Clean purple gradient background
- Search input box
- "Analyze Student" button

### 2. Student Data View
- Two cards side by side:
  - Student Profile (name, course, etc.)
  - Ongoing Data (attendance, grades, etc.)
- "Generate Risk Prediction" button

### 3. Risk Prediction View
- Risk Alert Card (RED for high risk)
- Risk Factors with progress bars
- Recommendations with action buttons

---

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Smooth Animations**: Cards fade in nicely
- **Color-Coded Risks**: 
  - 🔴 Red = High Risk
  - 🟡 Yellow = Medium Risk
  - 🟢 Green = Low Risk
- **Interactive Buttons**: Hover effects and animations

---

## 📊 Understanding the Results

### Risk Factors Explained

1. **Academic Decline (35%)**: Low attendance or poor performance
2. **Grade Decline (25%)**: CGPA dropping
3. **Financial Stress (20%)**: Fee payment delays
4. **Mental Health Concern (15%)**: Counselor visits
5. **Low Engagement (5%)**: No extracurricular activities

### Recommendations

The system automatically suggests:
- 📞 Academic advisor meetings
- 💰 Financial aid connections
- 🧠 Mental health support
- 📚 Peer mentoring
- 👨‍👩‍👦 Parent communication

---

## 🔄 Making Changes

### Add New Students

Edit `backend/database/students_data.json`:

```json
{
  "YOUR_ROLL_NO": {
    "name": "Your Name",
    "rollNo": "YOUR_ROLL_NO",
    "course": "B.Tech Computer Science",
    "year": "2nd Year",
    "familyIncome": "₹5,00,000/year",
    "parentEducation": "Graduate",
    "distanceFromCollege": "20 km",
    "accommodation": "Hostel",
    "attendance": 85,
    "currentCGPA": 7.5,
    "previousCGPA": 7.0,
    "assignmentsSubmitted": "8 out of 10 submitted",
    "libraryVisits": "10 visits in 2 months",
    "feeStatus": "Paid",
    "counselorVisits": "No visits",
    "extracurricular": "Active in sports",
    "lastLMSLogin": "Today"
  }
}
```

Restart backend server to see changes!

### Change Colors

Edit `frontend/src/styles/global.css`:

```css
:root {
  --primary-color: #667eea;  /* Change this */
  --danger-color: #ef4444;   /* And this */
}
```

Save and see changes instantly!

---

## ✅ Checklist

Before testing, make sure:

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed (or Yarn)
- [ ] Backend terminal shows "Running on http://0.0.0.0:8000"
- [ ] Frontend terminal shows "Local: http://localhost:5173"
- [ ] Browser opened to http://localhost:5173
- [ ] No firewall blocking ports 8000 or 5173

---

## 🎉 Success!

If you can:
1. ✅ Enter roll number 12345
2. ✅ See student data
3. ✅ Click prediction button
4. ✅ See risk assessment

**Congratulations! Your system is working perfectly!** 🎊

---

## 📞 Need Help?

If something isn't working:
1. Check both terminals for error messages
2. Review the "Common Issues" section above
3. Make sure both servers are running
4. Try restarting both servers

---

**Happy Predicting! 🎓**
