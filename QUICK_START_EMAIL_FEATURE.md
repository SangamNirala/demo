# Quick Start: Email Generation Feature

## 🚀 5-Minute Setup

### Step 1: Verify Configuration

Ensure your `.env` file has the Gemini API key:

```bash
# backend/.env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 2: Start Backend

```bash
cd backend
python server.py
```

You should see:
```
✅ Email Generation Service initialized with gemini-2.5-flash
```

### Step 3: Start Frontend

```bash
cd frontend
npm run dev
```

### Step 4: Test the Feature

1. Open `http://localhost:5173`
2. Search for student: `2023BT2086`
3. Click **"Predict Risk"**
4. Scroll down to **"📧 Generate Personalized Email"** card
5. Select an email type
6. Click **"Generate Email"**

## 📧 Email Types Quick Reference

### 1. To Student
- **When to use**: Direct student outreach
- **Tone**: Warm, supportive
- **What it includes**: Friendly invitation for chat
- **What it excludes**: Risk percentages, alarming language

### 2. To Parents
- **When to use**: Parent communication
- **Tone**: Professional, reassuring
- **What it includes**: Support partnership request
- **What it excludes**: "Dropout risk", alarming terms

### 3. Meeting Invitation
- **When to use**: Scheduling check-ins
- **Tone**: Casual, friendly
- **Required fields**: Date, Time, Location
- **What it includes**: Meeting details, reschedule option

## 🎯 Quick Tips

### For Best Results

1. **Add Context**: Use "Additional Notes" field
   ```
   Example: "Student mentioned family issues in last meeting"
   ```

2. **Review Before Sending**: Always edit generated content

3. **Personalize**: Add specific details about the student

4. **Test Different Types**: Try all three to see what works best

### Common Workflows

**Workflow 1: Student Outreach**
```
Search → Predict → Select "To Student" → Add notes → Generate → Edit → Copy
```

**Workflow 2: Parent Meeting**
```
Search → Predict → Select "To Parents" → Generate → Review → Open in Mail
```

**Workflow 3: Schedule Check-in**
```
Search → Predict → Select "Meeting" → Fill details → Generate → Send
```

## 🔧 Troubleshooting

### Issue: Button doesn't work
- **Check**: Backend server is running
- **Check**: Console for errors (F12)

### Issue: Generic emails
- **Solution**: Add more context in "Additional Notes"

### Issue: API error
- **Check**: GEMINI_API_KEY is valid
- **Check**: Internet connection

## 📱 Action Buttons

After generating an email:

- **📋 Copy to Clipboard**: Copy entire email
- **🔄 Regenerate**: Generate new version
- **📬 Open in Mail App**: Open default email client

## 🎨 UI Overview

```
┌─────────────────────────────────────┐
│  📧 Generate Personalized Email     │
├─────────────────────────────────────┤
│  Email Type: [Student] [Parent] [Meeting] │
│  Additional Notes: [textarea]       │
│  [Meeting Details if selected]      │
│  [✨ Generate Email]                │
└─────────────────────────────────────┘
```

## 📊 Example Output

### Student Email Example
```
Subject: Let's Connect - Support Available

Dear John,

I hope you're doing well! I wanted to reach out 
to see how things are going this semester...
```

### Parent Email Example
```
Subject: Partnership in Supporting John's Academic Journey

Dear Mr. and Mrs. Doe,

I hope this message finds you well. I am reaching 
out to discuss some areas where additional support...
```

### Meeting Invitation Example
```
Subject: Quick Check-in Meeting

Hi John,

I'd love to catch up and see how everything is 
going! I've scheduled a brief meeting for...
```

## ✅ Success Checklist

- [ ] Backend server running
- [ ] Frontend accessible
- [ ] GEMINI_API_KEY configured
- [ ] Student data loaded
- [ ] Prediction completed
- [ ] Email generated successfully
- [ ] Email reviewed and customized
- [ ] Email sent/copied

## 🎓 Next Steps

1. **Explore all email types**
2. **Customize generated content**
3. **Track which emails work best**
4. **Share feedback with team**
5. **Document your workflows**

## 📚 Additional Resources

- Full documentation: `EMAIL_GENERATION_FEATURE.md`
- API details: `backend/gemini/email_generation/README.md`
- Test suite: `backend/gemini/email_generation/test_email.py`

---

**Ready to generate your first email?** Follow Step 4 above! 🚀
