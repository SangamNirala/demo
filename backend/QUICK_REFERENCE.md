# 🎯 SUPER QUICK REFERENCE - How to Switch LLM

## Current Setup: ✅ GEMINI AI ACTIVE

---

## 🔄 TO SWITCH: Edit Just ONE Line!

**File:** `/app/backend/llm_service.py` (Line 20)

### Currently (Gemini AI Active):
```python
from gemini_llm_service import ChatService, chat_service, professional_chat_service  ✅
# from emergent_llm_service import ChatService, chat_service, professional_chat_service  ❌
```

### To Use Emergent LLM:
```python
# from gemini_llm_service import ChatService, chat_service, professional_chat_service  ❌
from emergent_llm_service import ChatService, chat_service, professional_chat_service  ✅
```

**Then run:**
```bash
sudo supervisorctl restart backend
```

---

## 📁 3 Files Created for You:

1. **`gemini_llm_service.py`** → Gemini AI code
2. **`emergent_llm_service.py`** → Emergent LLM code  
3. **`llm_service.py`** → Router (Edit this to switch!)

---

## 🔑 API Keys (Already in .env):

```
GEMINI_API_KEY=AIzaSyAJ8n7uo_L-a05UxCMQ8s7k2J9883ZIUWA
EMERGENT_LLM_KEY=sk-emergent-51f67AaD7E6967d742
```

---

## ✅ That's It!

Just change **ONE import line** → Restart backend → Done!

No need to:
- ❌ Comment 100+ lines of code
- ❌ Change server.py
- ❌ Change frontend
- ❌ Modify .env file

---

**See full guide:** `SWITCH_GUIDE_SEPARATE_FILES.md`
