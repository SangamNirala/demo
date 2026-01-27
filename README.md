# AI Chatbot

A simple chatbot application with React frontend and FastAPI backend.

## Setup Instructions

### Backend Setup
1. Navigate to backend folder and install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Create a `.env` file from `.env.example` and add your OpenAI API key:
   ```bash
   copy .env.example .env
   ```
   Then edit `.env` and add your API key.

3. Run the backend server:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

### Frontend Setup
1. Navigate to frontend folder and install dependencies:
   ```bash
   cd frontend
   yarn install
   ```

2. Run the frontend:
   ```bash
   yarn run
   ```

The frontend will be available at http://localhost:3000
The backend API will be available at http://localhost:8001
