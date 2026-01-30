# Frontend Testing Guide 🧪

## Quick Start

### Step 1: Start the Backend
```bash
# Open terminal 1
cd backend
python server.py
```

Wait until you see:
```
✅ ML Model loaded successfully!
🌐 Server starting on http://localhost:8000
```

### Step 2: Start the Frontend
```bash
# Open terminal 2
cd frontend
npm run dev
```

Wait until you see:
```
Local: http://localhost:5173/
```

### Step 3: Open Browser
Navigate to: **http://localhost:5173**

---

## Test Cases with Real Student Data

### 🔴 Test Case 1: HIGH RISK Student
**Student**: Rashmi Yadav  
**Roll Number**: `2023BT2086`

**Expected Profile Data**:
- Name: Rashmi Yadav
- Course: B.Tech Biotechnology
- Year: 1st Year
- Family Income: ₹2.0 Lakh/year
- Parent Education: Post Graduate
- Distance: 60.2 km
- Hostel/Day Scholar: Hostel

**Expected Ongoing Data**:
- Attendance: 43.4% (Very Low ⚠️)
- CGPA: Semester 1: 8.3 → Semester 2: 7.5 (Declining)
- Assignments: 4 out of 10 submitted (40%)
- Library Visits: 0 visits in 2 months
- Fee Payment: 1 month delayed
- Counselor Visits: 2 times for Stress
- Extracurricular: Yes
- LMS Login: 11 days ago

**Expected Prediction**:
- Risk Level: 🔴 HIGH (70-90%)
- Top Risk Factors:
  1. Low Attendance (40-50% contribution)
  2. Academic Decline (20-30% contribution)
  3. Mental Health Concern (15-20% contribution)
  4. Financial Stress (10-15% contribution)
  5. Low Engagement (5-10% contribution)

**Expected Recommendations**:
- 📞 Contact Student
- 🧠 Counselor Referral
- 💰 Financial Aid Review
- 📚 Assign Academic Mentor
- 👨‍👩‍👦 Parent Meeting

---

### 🔴 Test Case 2: HIGH RISK Student (Different Profile)
**Student**: Sneha Kumar  
**Roll Number**: `2023CS3944`

**Expected Profile Data**:
- Name: Sneha Kumar
- Course: B.Tech Computer Science
- Year: 1st Year
- Family Income: ₹2.3 Lakh/year
- Parent Education: Below 10th
- Distance: 29.9 km
- Hostel/Day Scholar: Hostel

**Expected Ongoing Data**:
- Attendance: 40.0% (Very Low ⚠️)
- CGPA: Semester 1: 8.9 → Semester 2: 7.8 (Declining)
- Assignments: 3 out of 10 submitted (31.6%)
- Library Visits: 2 visits
- Fee Payment: 2 months delayed
- Counselor Visits: 0
- Extracurricular: No
- LMS Login: 35 days ago (Very inactive!)

**Expected Prediction**:
- Risk Level: 🔴 HIGH (75-95%)
- Major concerns: Attendance, Engagement, Financial issues

---

### 🟡 Test Case 3: MEDIUM RISK Student
**Student**: Ekta Reddy  
**Roll Number**: `2022CS179`

**Expected Profile Data**:
- Name: Ekta Reddy
- Course: B.Tech Computer Science
- Year: 2nd Year
- Family Income: ₹4.2 Lakh/year
- Distance: 100.0 km (Very far!)

**Expected Ongoing Data**:
- Attendance: 53.5% (Below average)
- CGPA: Semester 1: 6.2 → Semester 2: 5.2 (Declining)
- Assignments: 6 out of 10 submitted (55%)
- Library Visits: 0
- Fee Payment: 3 months delayed
- Counselor Visits: 4 times for Personal issues
- LMS Login: 30 days ago

**Expected Prediction**:
- Risk Level: 🟡 MEDIUM (50-70%)
- Concerns: Distance, Financial stress, Personal issues

---

### 🟢 Test Case 4: LOW RISK Student
**Student**: Sneha Tiwari  
**Roll Number**: `2021CS276`

**Expected Profile Data**:
- Name: Sneha Tiwari
- Course: B.Tech Computer Science
- Year: 1st Year
- Family Income: ₹5.8 Lakh/year
- Distance: 15.1 km

**Expected Ongoing Data**:
- Attendance: 68.0% (Good)
- CGPA: Semester 1: 6.8 → Semester 2: 7.7 (Improving! ✅)
- Assignments: 10 out of 10 submitted (100% ⭐)
- Library Visits: 7 visits (Excellent!)
- Fee Payment: Up to date
- Counselor Visits: 1 time for Academic guidance
- Extracurricular: Yes
- LMS Login: Today (0 days ago)

**Expected Prediction**:
- Risk Level: 🟢 LOW (10-30%)
- Student is on track!

---

### 🟢 Test Case 5: LOW RISK Student (Another Example)
**Student**: Tanvi Mishra  
**Roll Number**: `2023CE4184`

**Expected Profile Data**:
- Name: Tanvi Mishra
- Course: B.Tech Civil Engineering
- Year: 2nd Year
- Family Income: ₹3.5 Lakh/year
- Hostel/Day Scholar: Hostel

**Expected Ongoing Data**:
- Attendance: 91.1% (Excellent! ⭐)
- CGPA: Semester 1: 7.4 → Semester 2: 7.0 (Stable)
- Assignments: 8 out of 10 submitted (81.3%)
- Library Visits: 7 visits
- Fee Payment: Up to date
- Counselor Visits: 1 time for Stress
- Extracurricular: Yes
- LMS Login: 2 days ago

**Expected Prediction**:
- Risk Level: 🟢 LOW (15-35%)
- Good overall performance

---

## More Test Roll Numbers

### High Risk Students (Try These):
- `2021CS1078` - Neha Mishra (27.4% attendance)
- `2023EC1688` - Tushar Nair (35.2% attendance, 3 months fee delay)
- `2022CE3113` - Kritika Mishra (39.6% attendance, financial issues)
- `2024CE1527` - Ankit Singh (27.5% attendance)
- `2023CS4261` - Tanvi Kapoor (61.1% attendance, 3 months delay)
- `2021IT3513` - Karan Malhotra (57.8% attendance, declining grades)
- `2022IT1295` - Sachin Shah (64.5% attendance, 3 months delay)
- `2021CS1898` - Divya Mishra (43.7% attendance, financial stress)
- `2023BT1951` - Lakshmi Bansal (49.0% attendance, declining CGPA)
- `2022EC2758` - Varun Khanna (51.3% attendance, 56 days LMS inactive)
- `2024IT2317` - Ravi Bansal (37.2% attendance, 4 months delay)

### Medium Risk Students (Try These):
- `2023EE345` - Ishita Goel (90.4% attendance but low grades)
- `2024BT061` - Divya Bansal (80.9% attendance, stable)
- `2022EC909` - Riya Kapoor (74.9% attendance, low CGPA)
- `2024EE4173` - Kavya Joshi (65.0% attendance)

### Low Risk Students (Try These):
- `2023EC4154` - Anjali Bhatia (74.4% attendance, good grades)
- `2021BT3362` - Neha Chauhan (77.9% attendance, scholarship holder)
- `2023IT1264` - Priya Reddy (94.9% attendance, 8.1 CGPA, scholarship)
- `2023CE3780` - Aarti Agarwal (81.6% attendance, 100% assignments)
- `2021EE406` - Kavya Joshi (65.0% attendance, 8.2 CGPA)

---

## Step-by-Step Testing Process

### 1. Search for Student
1. In the search box, enter a roll number (e.g., `2023BT2086`)
2. Click the **"Search"** or **"Analyze"** button
3. Wait for the loading spinner

### 2. Review Student Data
You should see two cards:

**Card 1: Student Profile**
- Name, Roll No, Course, Year
- Family Income, Parent Education
- Distance from College
- Hostel/Day Scholar status

**Card 2: Ongoing Data**
- Attendance percentage
- CGPA (current and previous)
- Assignment submission rate
- Library visits
- Fee payment status
- Counselor visits
- Extracurricular participation
- LMS last login

### 3. Click "Prediction" Button
1. Click the **"Get Prediction"** or **"Analyze Risk"** button
2. Wait for the ML model to process (should take 1-3 seconds)

### 4. Review Prediction Results
You should see three new cards:

**Card 1: Risk Alert**
- 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW
- Risk percentage (0-100%)
- Student name and course

**Card 2: Risk Factors**
- List of contributing factors
- Each with a percentage contribution
- Icons and descriptions

**Card 3: Recommendations**
- Actionable interventions
- Prioritized by urgency
- Icons and detailed descriptions

---

## What to Look For

### ✅ Success Indicators:
- Student data loads within 1-2 seconds
- All fields are populated correctly
- Prediction completes within 3 seconds
- Risk level matches student's situation
- Risk factors make sense (low attendance → attendance risk)
- Recommendations are relevant

### ❌ Error Scenarios to Test:

#### Test 1: Invalid Roll Number
- Input: `INVALID123`
- Expected: Error message "Student not found"

#### Test 2: Empty Input
- Input: (leave blank)
- Expected: Validation error or prompt to enter roll number

#### Test 3: Backend Not Running
- Stop the backend server
- Try to search
- Expected: Connection error message

#### Test 4: Special Characters
- Input: `2023@#$%`
- Expected: Error message "Student not found"

---

## Visual Checks

### Colors:
- 🔴 High Risk: Red background/border
- 🟡 Medium Risk: Yellow/Orange background/border
- 🟢 Low Risk: Green background/border

### Icons:
- 📚 Academic factors
- 📅 Attendance factors
- 💰 Financial factors
- 🧠 Mental health factors
- 📉 Engagement factors

### Layout:
- Cards should be responsive
- Text should be readable
- No overlapping elements
- Smooth transitions

---

## Performance Testing

### Load Time Expectations:
- Student data fetch: < 2 seconds
- Prediction calculation: < 3 seconds
- Total workflow: < 5 seconds

### Try Multiple Students:
1. Search for `2023BT2086` (High Risk)
2. Search for `2021CS276` (Low Risk)
3. Search for `2022CS179` (Medium Risk)
4. Repeat several times to test caching

---

## Common Issues & Solutions

### Issue 1: "Student not found"
**Solution**: 
- Check if roll number is typed correctly
- Use roll numbers from the list above
- Ensure backend is running

### Issue 2: "Prediction failed"
**Solution**:
- Check if model files exist in `backend/ml/saved_models/`
- Check backend console for error messages
- Restart backend server

### Issue 3: CORS Error
**Solution**:
- Ensure backend is running on port 8000
- Check frontend .env file has correct API URL
- Restart both servers

### Issue 4: Blank/Missing Data
**Solution**:
- Check browser console for errors
- Verify API response in Network tab
- Check if database file is valid JSON

---

## Browser Developer Tools

### Open DevTools:
- Chrome/Edge: Press `F12` or `Ctrl+Shift+I`
- Firefox: Press `F12`

### Check Network Tab:
1. Open DevTools → Network tab
2. Search for a student
3. Look for API calls:
   - `GET /api/student/2023BT2086` (should return 200)
   - `POST /api/predict/2023BT2086` (should return 200)

### Check Console Tab:
- Should have no red errors
- May have info/debug messages (blue/gray)

---

## Sample Test Script

```
Test Session: [Date/Time]

1. High Risk Student
   Roll No: 2023BT2086
   ✅ Data loaded correctly
   ✅ Prediction: HIGH (82%)
   ✅ Risk factors displayed
   ✅ Recommendations shown

2. Low Risk Student
   Roll No: 2021CS276
   ✅ Data loaded correctly
   ✅ Prediction: LOW (25%)
   ✅ Risk factors displayed
   ✅ Recommendations shown

3. Medium Risk Student
   Roll No: 2022CS179
   ✅ Data loaded correctly
   ✅ Prediction: MEDIUM (58%)
   ✅ Risk factors displayed
   ✅ Recommendations shown

4. Error Handling
   Roll No: INVALID123
   ✅ Error message displayed

Overall: ✅ PASS / ❌ FAIL
```

---

## Quick Reference: Best Test Roll Numbers

| Risk Level | Roll Number | Name | Key Issue |
|------------|-------------|------|-----------|
| 🔴 HIGH | 2023BT2086 | Rashmi Yadav | 43% attendance, stress |
| 🔴 HIGH | 2023CS3944 | Sneha Kumar | 40% attendance, 35 days inactive |
| 🔴 HIGH | 2021CS1078 | Neha Mishra | 27% attendance |
| 🟡 MEDIUM | 2022CS179 | Ekta Reddy | 53% attendance, 100km distance |
| 🟡 MEDIUM | 2024BT061 | Divya Bansal | Moderate performance |
| 🟢 LOW | 2021CS276 | Sneha Tiwari | 100% assignments, improving |
| 🟢 LOW | 2023CE4184 | Tanvi Mishra | 91% attendance |
| 🟢 LOW | 2023IT1264 | Priya Reddy | 95% attendance, 8.1 CGPA |

---

## Expected User Flow

1. **Landing Page** → See title and search box
2. **Enter Roll Number** → Type `2023BT2086`
3. **Click Search** → Loading spinner appears
4. **View Student Data** → Two cards with profile and ongoing data
5. **Click Prediction** → Loading spinner appears
6. **View Results** → Three cards with risk alert, factors, and recommendations
7. **Try Another Student** → Search again with different roll number

---

## Success Criteria

Your frontend is working correctly if:
- ✅ All 8 test roll numbers work
- ✅ Risk levels match expectations (High/Medium/Low)
- ✅ Data displays correctly in all cards
- ✅ No console errors
- ✅ Smooth user experience
- ✅ Error handling works for invalid inputs
- ✅ Responsive design (try resizing browser)

---

## Need Help?

If something doesn't work:
1. Check both terminals (backend and frontend) for errors
2. Open browser DevTools and check Console tab
3. Verify backend is running: http://localhost:8000/api/health
4. Check if model files exist in `backend/ml/saved_models/`
5. Restart both servers

Happy Testing! 🚀
