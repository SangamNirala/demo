# Deployment Guide

This guide will help you deploy the chatbot application with the frontend on Vercel and the backend on Render.

## Prerequisites

- GitHub account
- Vercel account (sign up at https://vercel.com)
- Render account (sign up at https://render.com)
- Your API keys (GEMINI_API_KEY or EMERGENT_API_KEY)

## Backend Deployment (Render)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com/dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Add environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `EMERGENT_API_KEY`: Your Emergent API key (if using Emergent)
6. Click "Create Web Service"
7. Wait for deployment to complete
8. Copy your backend URL (e.g., `https://chatbot-backend-xxxx.onrender.com`)

### Important Notes for Render:
- The free tier may spin down after inactivity (cold starts)
- First request after inactivity may take 30-60 seconds
- Consider upgrading to a paid plan for production use

## Frontend Deployment (Vercel)

### Step 1: Deploy on Vercel

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. Add environment variable:
   - Name: `VITE_API_URL`
   - Value: `https://your-backend-url.onrender.com/api` (use your actual Render URL)
6. Click "Deploy"
7. Wait for deployment to complete

### Step 2: Update CORS (if needed)

If you encounter CORS errors, update `backend/server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vercel-app.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy the backend on Render.

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
# Create .env file with your API keys
uvicorn server:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
# Create .env file with VITE_API_URL=http://localhost:8001/api
npm run dev
```

## Environment Variables Summary

### Backend (Render)
- `GEMINI_API_KEY`: Your Google Gemini API key
- `EMERGENT_API_KEY`: Your Emergent API key (optional)
- `PYTHON_VERSION`: 3.11.0 (auto-configured)

### Frontend (Vercel)
- `VITE_API_URL`: Your backend API URL (e.g., `https://chatbot-backend-xxxx.onrender.com/api`)

## Troubleshooting

### Frontend can't connect to backend
- Check that `VITE_API_URL` is set correctly in Vercel
- Verify CORS settings in backend
- Check browser console for errors

### Backend errors on Render
- Check Render logs for error messages
- Verify environment variables are set
- Ensure API keys are valid

### Cold start delays
- First request after inactivity may be slow on Render free tier
- Consider upgrading to paid tier or implementing a keep-alive ping

## Updating Your Deployment

### Backend Updates
```bash
git add .
git commit -m "Update backend"
git push
```
Render will automatically redeploy.

### Frontend Updates
```bash
git add .
git commit -m "Update frontend"
git push
```
Vercel will automatically redeploy.

## Custom Domains (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### Render
1. Go to Service Settings → Custom Domain
2. Add your custom domain
3. Follow DNS configuration instructions
