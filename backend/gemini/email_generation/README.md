# Email Generation Feature

## Overview

The Email Generation feature uses Gemini AI to create personalized, context-aware emails for student outreach. This feature helps faculty and administrators communicate effectively with students and parents about academic support needs.

## Features

### 3 Email Types

1. **Email to Student**
   - Tone: Warm, supportive, encouraging, non-judgmental
   - Does NOT mention risk percentages or "flagged" status
   - Invites student for a friendly chat
   - Expresses that support is available

2. **Email to Parents**
   - Tone: Formal, sensitive, professional
   - Does NOT use alarming words like "dropout risk"
   - Frames concerns as "areas where support is needed"
   - Requests a meeting or phone call
   - Emphasizes partnership between institution and parents

3. **Meeting Invitation**
   - Tone: Friendly, casual, non-threatening
   - Frames as a regular check-in, not a serious concern
   - Includes date, time, and location fields
   - Provides option to reschedule

## API Endpoint

### POST `/api/email/generate`

Generate a personalized email using Gemini AI.

**Request Body:**
```json
{
  "emailType": "student" | "parent" | "meeting",
  "studentData": {
    "name": "John Doe",
    "rollNo": "2023BT001",
    "course": "B.Tech Computer Science",
    "year": "2nd Year"
  },
  "predictionData": {
    "riskLevel": "MEDIUM",
    "riskPercentage": 45,
    "riskFactors": [
      {
        "name": "Low Attendance",
        "contribution": 35
      }
    ]
  },
  "additionalNotes": "Student has been struggling with time management",
  "meetingDetails": {
    "date": "2024-02-15",
    "time": "10:00 AM",
    "location": "Room 301, Admin Block"
  }
}
```

**Response:**
```json
{
  "success": true,
  "email": {
    "subject": "Let's Connect - Academic Support Available",
    "body": "Dear John,\n\nI hope this message finds you well..."
  }
}
```

## Usage Example

```python
from gemini.email_generation import email_service

# Generate email to student
email = email_service.generate_email(
    email_type='student',
    student_data={
        'name': 'John Doe',
        'rollNo': '2023BT001',
        'course': 'B.Tech CS',
        'year': '2nd Year'
    },
    prediction_data={
        'riskLevel': 'MEDIUM',
        'riskPercentage': 45,
        'riskFactors': [...]
    },
    additional_notes='Student needs time management support'
)

print(email['subject'])
print(email['body'])
```

## Frontend Component

The `EmailGeneratorCard` component provides a user-friendly interface for:
- Selecting email type (radio buttons)
- Adding optional custom notes
- Entering meeting details (for meeting invitations)
- Generating AI-powered emails
- Editing generated content
- Copying to clipboard
- Opening in default mail app
- Regenerating emails

## Configuration

Ensure `GEMINI_API_KEY` is set in your `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Error Handling

The service includes comprehensive error handling:
- Missing API key detection
- Invalid email type validation
- Meeting details validation
- JSON parsing error recovery
- Network error handling

## Best Practices

1. **Always review generated emails** before sending
2. **Customize as needed** - AI provides a starting point
3. **Add personal touches** to make emails more authentic
4. **Use additional notes** to provide context for better AI generation
5. **Test different email types** to find the best approach for each situation

## Security & Privacy

- Risk percentages and internal assessments are NOT included in student/parent emails
- Sensitive information is handled according to institutional privacy policies
- All communications should comply with data protection regulations

## Future Enhancements

- Email templates library
- Multi-language support
- Email scheduling
- Bulk email generation
- Email tracking and analytics
