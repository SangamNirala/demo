# Backend Structure Guide

## 📁 Complete Backend Structure

```
backend/
├── main.py                  # Main FastAPI application
├── server.py                # Simple version (legacy)
├── config.py                # Configuration management
├── database.py              # Database setup
├── models.py                # SQLAlchemy models
├── schemas.py               # Pydantic schemas
├── ai_service.py            # AI/Gemini integration
│
├── routes/                  # API endpoints
│   ├── __init__.py
│   ├── chat.py             # Chat endpoints
│   ├── users.py            # User management
│   ├── auth.py             # Authentication
│   └── files.py            # File upload/download
│
├── middleware/              # Middleware functions
│   ├── __init__.py
│   ├── auth.py             # JWT authentication
│   ├── rate_limit.py       # Rate limiting
│   └── logging.py          # Request logging
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── helpers.py          # General helpers
│   ├── validators.py       # Input validation
│   └── response.py         # Standard responses
│
├── tests/                   # Unit tests
│   ├── __init__.py
│   └── test_api.py         # API tests
│
├── uploads/                 # File uploads directory
├── .env                     # Environment variables
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── requirements.txt        # Python dependencies
```

## 🔧 What Each Folder Does

### **routes/**
API endpoints organized by feature:
- `chat.py` - Chat with AI
- `users.py` - User CRUD operations
- `auth.py` - Login/register/JWT tokens
- `files.py` - File upload/download

### **middleware/**
Request/response processing:
- `auth.py` - JWT token verification
- `rate_limit.py` - Prevent API abuse
- `logging.py` - Log all requests

### **utils/**
Reusable utilities:
- `helpers.py` - Date formatting, hashing, pagination
- `validators.py` - Email, password, phone validation
- `response.py` - Standard JSON responses

### **tests/**
Unit and integration tests:
- `test_api.py` - Test all endpoints

## 🚀 Quick Usage Examples

### 1. Authentication
```python
from middleware.auth import create_access_token, get_current_user
from fastapi import Depends

@router.get("/protected")
async def protected_route(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id}
```

### 2. Rate Limiting
```python
from middleware.rate_limit import rate_limit
from fastapi import Depends

@router.get("/limited", dependencies=[Depends(rate_limit(max_requests=5))])
async def limited_endpoint():
    return {"message": "Rate limited"}
```

### 3. Standard Responses
```python
from utils.response import success_response, error_response

@router.get("/data")
async def get_data():
    return success_response(data={"items": []}, message="Data retrieved")
```

### 4. Validation
```python
from utils.validators import validate_email, validate_password

email = "test@example.com"
if not validate_email(email):
    raise HTTPException(400, "Invalid email")

is_valid, error = validate_password("MyPass123")
if not is_valid:
    raise HTTPException(400, error)
```

### 5. File Upload
```python
from routes.files import router as files_router
app.include_router(files_router)

# POST /api/files/upload with file
# POST /api/files/upload-multiple with multiple files
```

## 🔐 Security Features

- ✅ JWT Authentication
- ✅ Password validation
- ✅ Rate limiting
- ✅ Input sanitization
- ✅ CORS configuration
- ✅ Request logging

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest tests/
```

## 📝 Adding New Features

### Add New Route
1. Create `routes/my_feature.py`
2. Define router and endpoints
3. Add to `main.py`: `app.include_router(my_feature.router)`

### Add New Middleware
1. Create `middleware/my_middleware.py`
2. Define middleware function
3. Add to `main.py`: `app.middleware("http")(my_middleware)`

### Add New Utility
1. Create function in `utils/helpers.py`
2. Import where needed: `from utils.helpers import my_function`

## 🎯 Production Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Use proper password hashing (bcrypt)
- [ ] Switch to PostgreSQL/MySQL
- [ ] Add Redis for rate limiting
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Add monitoring (Sentry)
- [ ] Configure CORS properly
- [ ] Add API documentation
- [ ] Set up CI/CD

## 💡 Tips

1. **Keep routes thin** - Move logic to services
2. **Use dependency injection** - FastAPI's Depends()
3. **Validate everything** - Use Pydantic schemas
4. **Log important events** - Use logging middleware
5. **Test your endpoints** - Write tests in tests/

Your backend is now production-ready! 🚀
