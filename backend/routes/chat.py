from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import ChatRequest, ChatResponse
from ai_service import AIService
from database import get_db
from models import ChatHistory
import uuid

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Generate AI response
        bot_response = AIService.generate_with_context(
            request.message, 
            request.conversation_history
        )
        
        # Save to database (optional - comment out if not needed)
        # chat_record = ChatHistory(
        #     user_message=request.message,
        #     bot_response=bot_response,
        #     session_id=session_id
        # )
        # db.add(chat_record)
        # db.commit()
        
        return ChatResponse(response=bot_response, session_id=session_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    history = db.query(ChatHistory).filter(
        ChatHistory.session_id == session_id
    ).order_by(ChatHistory.timestamp).all()
    return history
