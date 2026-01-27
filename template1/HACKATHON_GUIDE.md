# 🚀 Hackathon Template - Quick Start Guide

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # Main FastAPI app (use this instead of server.py)
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── ai_service.py        # AI/Gemini integration
│   ├── routes/
│   │   ├── chat.py          # Chat endpoints
│   │   └── users.py         # User endpoints
│   └── .env                 # Environment variables
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── Navbar/
    │   │       ├── Navbar.jsx
    │   │       ├── Navbar.css
    │   │       └── index.js
    │   ├── pages/
    │   │   ├── Home/
    │   │   │   ├── Home.jsx
    │   │   │   ├── Home.css
    │   │   │   └── index.js
    │   │   ├── Chat/
    │   │   │   ├── Chat.jsx
    │   │   │   ├── Chat.css
    │   │   │   └── index.js
    │   │   └── About/
    │   │       ├── About.jsx
    │   │       ├── About.css
    │   │       └── index.js
    │   ├── services/
    │   │   └── api.js       # API calls
    │   └── App.jsx          # Main app with routing
    └── package.json
```

## ⚡ Quick Setup (5 minutes)

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd frontend
yarn install
yarn dev
```

## 🎯 Customization for Your Problem Statement

### 1. **Add New API Endpoints**
Create a new file in `backend/routes/your_feature.py`:
```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/your-feature", tags=["your-feature"])

@router.post("/")
async def your_endpoint():
    return {"message": "Your logic here"}
```

Then add to `main.py`:
```python
from routes import your_feature
app.include_router(your_feature.router)
```

### 2. **Add Database Models**
Edit `backend/models.py`:
```python
class YourModel(Base):
    __tablename__ = "your_table"
    id = Column(Integer, primary_key=True)
    # Add your fields
```

### 3. **Create New Frontend Pages**
Create a new folder `frontend/src/pages/YourPage/`:

**YourPage.jsx:**
```jsx
function YourPage() {
  return <div>Your content</div>
}
export default YourPage
```

**YourPage.css:**
```css
.your-page {
  /* Your styles */
}
```

**index.js:**
```js
export { default } from './YourPage'
```

Add route in `App.jsx`:
```jsx
import YourPage from './pages/YourPage'
<Route path="/your-page" element={<YourPage />} />
```

### 4. **Modify AI Behavior**
Edit `backend/ai_service.py` to customize prompts and AI logic.

## 🔧 Common Modifications

### Change Database (PostgreSQL/MySQL)
Update `backend/.env`:
```
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Add Authentication
1. Install: `pip install python-jose passlib`
2. Create `backend/auth.py`
3. Add JWT token generation/validation

### Add File Upload
```python
from fastapi import File, UploadFile

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Process file
```

### Add WebSocket (Real-time)
```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Handle messages
```

## 📦 Deployment Tips

### Backend (Railway/Render)
- Use `requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel/Netlify)
- Build command: `yarn build`
- Output directory: `dist`

## 🎨 UI Customization

Colors are in CSS files - search for `#667eea` and `#764ba2` to change the gradient theme.

## 💡 Pro Tips

1. **Keep it simple** - Don't over-engineer
2. **Test endpoints** - Use http://localhost:8001/docs for API testing
3. **Version control** - Commit frequently
4. **Environment variables** - Never commit `.env` files
5. **Error handling** - Add try-catch blocks everywhere

## 🐛 Troubleshooting

**Backend won't start?**
- Check if port 8001 is free
- Verify `.env` file exists
- Run `pip install -r requirements.txt` again

**Frontend API errors?**
- Check backend is running on port 8001
- Verify CORS settings in `config.py`
- Check browser console for details

**Database errors?**
- Delete `app.db` and restart
- Check SQLAlchemy models syntax

## 🚀 Ready to Hack!

You now have:
- ✅ Working chat interface
- ✅ AI integration (Gemini)
- ✅ Database setup
- ✅ Multi-page routing
- ✅ API structure
- ✅ Reusable components

**Focus on your unique solution, not the boilerplate!**

Good luck! 🎉
