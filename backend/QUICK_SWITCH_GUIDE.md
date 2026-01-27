# 🔄 Quick Switch Guide: Gemini AI ↔️ Emergent LLM

## Current Status: ✅ GEMINI AI ACTIVE

---

## How to Switch (3 Simple Steps)

### 🔵 To Use Gemini AI Direct (Currently Active)

**File:** `/app/backend/llm_service.py`

1. **Lines 17-94**: Keep UNCOMMENTED ✅
   ```python
   from google import genai
   from google.genai import types
   
   class ChatService:
       # Gemini implementation
   ```

2. **Lines 98-180**: Keep COMMENTED OUT ✅
   ```python
   # from emergentintegrations.llm.chat import LlmChat, UserMessage
   # 
   # class ChatService:
   #     # Emergent LLM implementation
   ```

3. **Restart:** `sudo supervisorctl restart backend`

---

### 🟢 To Use Emergent LLM

**File:** `/app/backend/llm_service.py`

1. **Lines 17-94**: COMMENT OUT (add `#` to each line)
   ```python
   # from google import genai
   # from google.genai import types
   # 
   # class ChatService:
   #     # Gemini implementation
   ```

2. **Lines 98-180**: UNCOMMENT (remove `#` from each line)
   ```python
   from emergentintegrations.llm.chat import LlmChat, UserMessage
   
   class ChatService:
       # Emergent LLM implementation
   ```

3. **Restart:** `sudo supervisorctl restart backend`

---

## 📝 Summary

**What needs to change:**
- ✏️ Only 1 file: `/app/backend/llm_service.py`
- 🔄 Comment one implementation, uncomment the other
- 🔁 Restart backend

**What stays the same:**
- ✅ server.py (no changes)
- ✅ Frontend code (no changes)
- ✅ API endpoints (no changes)
- ✅ .env file (both keys already there)

---

## 🔑 API Keys Location

File: `/app/backend/.env`
```
GEMINI_API_KEY=AIzaSyAJ8n7uo_L-a05UxCMQ8s7k2J9883ZIUWA
EMERGENT_LLM_KEY=sk-emergent-51f67AaD7E6967d742
```

---

## ✅ Verify Switch Worked

```bash
# Check logs
tail -n 30 /var/log/supervisor/backend.out.log

# Test API
curl http://localhost:8001/api/health
```

Look for log messages showing which provider is being used:
- Gemini: `[Gemini/gemini-2.0-flash-exp]`
- Emergent: `[gemini/gemini-2.5-flash]`
