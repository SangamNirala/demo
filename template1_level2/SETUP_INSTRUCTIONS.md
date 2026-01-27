# 🚀 Setup Instructions

## Current Status
You have TWO versions of the backend:

1. **Simple Version** (Currently Running)
   - File: `backend/server.py`
   - Single file, basic structure
   - Good for quick demos

2. **Hackathon Template** (New - Recommended)
   - File: `backend/main.py`
   - Modular structure with routes, models, services
   - Production-ready, scalable

## 🔄 Switch to Hackathon Template

### Step 1: Stop Current Server
Press `CTRL+C` in your backend terminal

### Step 2: Install New Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Start New Backend
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Step 4: Update Frontend Dependencies
In a new terminal:
```bash
cd frontend
yarn install
yarn dev
```

## ✨ What's New?

### Backend Features
- ✅ Modular route structure (`routes/chat.py`, `routes/users.py`)
- ✅ Database models and schemas
- ✅ Centralized AI service
- ✅ Configuration management
- ✅ Easy to add new endpoints

### Frontend Features
- ✅ Multi-page routing (Home, Chat, About)
- ✅ Navigation bar
- ✅ Reusable components
- ✅ API service layer
- ✅ Professional landing page

## 📝 Quick Customization

### Add a New Feature (5 minutes)

1. **Backend**: Create `backend/routes/my_feature.py`
```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/my-feature", tags=["my-feature"])

@router.get("/")
async def get_data():
    return {"data": "your data"}
```

2. **Register Route**: In `backend/main.py`
```python
from routes import my_feature
app.include_router(my_feature.router)
```

3. **Frontend**: Create folder `frontend/src/pages/MyFeature/`

**MyFeature.jsx:**
```jsx
function MyFeature() {
  return <div>My Feature</div>
}
export default MyFeature
```

**MyFeature.css:**
```css
.my-feature {
  padding: 2rem;
}
```

**index.js:**
```js
export { default } from './MyFeature'
```

4. **Add Route**: In `frontend/src/App.jsx`
```jsx
<Route path="/my-feature" element={<MyFeature />} />
```

## 🎯 For Your Hackathon

### Before the Event
- ✅ Test both versions work
- ✅ Read `HACKATHON_GUIDE.md`
- ✅ Familiarize yourself with the structure
- ✅ Have your API keys ready

### During the Event
1. Listen to problem statement
2. Identify which features you need
3. Modify existing routes/pages
4. Add new endpoints as needed
5. Focus on your unique solution!

### Common Scenarios

**Need user authentication?**
- Modify `backend/routes/users.py`
- Add JWT token logic

**Need file upload?**
- Add to `backend/routes/` with `UploadFile`

**Need real-time updates?**
- Add WebSocket endpoint in `main.py`

**Need different AI model?**
- Modify `backend/ai_service.py`

**Need custom database?**
- Update models in `backend/models.py`
- Change `DATABASE_URL` in `.env`

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Change port in command
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Module not found?**
```bash
pip install -r requirements.txt
```

**Frontend build errors?**
```bash
cd frontend
rm -rf node_modules
yarn install
```

## 📚 Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- React Router: https://reactrouter.com
- Gemini API: https://ai.google.dev/docs

## 🎉 You're Ready!

Your template includes:
- ✅ Working chat with AI
- ✅ Database setup
- ✅ Multi-page frontend
- ✅ API structure
- ✅ Easy customization

**Focus on solving the problem, not building infrastructure!**

Good luck at your hackathon! 🚀
