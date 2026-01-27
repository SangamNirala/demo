from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from models import User
from utils.validators import validate_password
from utils.helpers import hash_password, verify_password
from middleware.auth import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["authentication"])

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == request.email) | (User.username == request.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Validate password
    is_valid, error = validate_password(request.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Create user (Note: In production, use proper password hashing like bcrypt)
    # new_user = User(
    #     username=request.username,
    #     email=request.email,
    #     password_hash=hash_password(request.password)
    # )
    # db.add(new_user)
    # db.commit()
    
    # Create token
    access_token = create_access_token(
        data={"user_id": 1, "email": request.email},
        expires_delta=timedelta(days=7)
    )
    
    return TokenResponse(access_token=access_token)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    # Find user
    # user = db.query(User).filter(User.email == request.email).first()
    # if not user or not verify_password(request.password, user.password_hash):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    access_token = create_access_token(
        data={"user_id": 1, "email": request.email},
        expires_delta=timedelta(days=7)
    )
    
    return TokenResponse(access_token=access_token)
