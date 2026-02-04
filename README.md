# AI Chatbot Application

A full-stack chatbot application with React frontend and FastAPI backend, supporting multiple LLM providers (Google Gemini and Emergent AI).

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn server:app --reload --port 8001
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
# Set VITE_API_URL=http://localhost:8001/api in .env
npm run dev
```

## 📦 Deployment

This project is configured for easy deployment:
- **Frontend**: Vercel
- **Backend**: Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🛠️ Tech Stack

**Frontend:**
- React 18
- Vite
- Axios

**Backend:**
- FastAPI
- Python 3.11
- Google Gemini AI
- Emergent AI

## 📁 Project Structure

```
.
├── frontend/           # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── backend/            # FastAPI backend
│   ├── server.py
│   ├── llm_service.py
│   └── requirements.txt
├── vercel.json         # Vercel configuration
├── render.yaml         # Render configuration
└── DEPLOYMENT.md       # Deployment guide
```

## 🔑 Environment Variables

**Backend (.env):**
- `GEMINI_API_KEY` - Your Google Gemini API key
- `EMERGENT_API_KEY` - Your Emergent API key (optional)

**Frontend (.env):**
- `VITE_API_URL` - Backend API URL

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [How to Add New AI Service](backend/HOW_TO_ADD_NEW_AI_SERVICE.md)
- [Quick Reference](backend/QUICK_REFERENCE.md)
- [Switching LLM Guide](backend/SWITCHING_LLM_GUIDE.md)

## 🤝 Contributing

Feel free to submit issues and pull requests.

## 📄 License

MIT
