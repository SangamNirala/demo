# 🔄 LLM Integration Switch Guide (Separate Files Architecture)

## 📁 New File Structure

Your chatbot now uses a **clean, modular architecture** with separate files for each LLM integration:

```
/app/backend/
├── gemini_llm_service.py       # Gemini AI Direct Integration
├── emergent_llm_service.py     # Emergent LLM Universal Key Integration
├── llm_service.py              # Import Router (THIS IS WHERE YOU SWITCH)
├── server.py                   # Main API server (no changes needed)
└── .env                        # API keys for both services
```

---

## ✅ Current Status

**Currently Active: GEMINI AI** (using `GEMINI_API_KEY`)

---

## 🎯 How to Switch Between Integrations

### **SUPER SIMPLE: Just Edit ONE LINE in ONE FILE!**

**File to Edit:** `/app/backend/llm_service.py`

---

### 🔵 To Use Gemini AI (Currently Active ✅)

**In `/app/backend/llm_service.py`, line 20:**

```python
# Keep this line UNCOMMENTED:
from gemini_llm_service import ChatService, chat_service, professional_chat_service

# Keep this line COMMENTED:
# from emergent_llm_service import ChatService, chat_service, professional_chat_service
```

**Then restart:**
```bash
sudo supervisorctl restart backend
```

---

### 🟢 To Use Emergent LLM

**In `/app/backend/llm_service.py`, change line 20 to:**

```python
# COMMENT OUT this line:
# from gemini_llm_service import ChatService, chat_service, professional_chat_service

# UNCOMMENT this line:
from emergent_llm_service import ChatService, chat_service, professional_chat_service
```

**Then restart:**
```bash
sudo supervisorctl restart backend
```

---

## 📝 Step-by-Step Visual Guide

### Current State (Gemini Active):

**File: `/app/backend/llm_service.py`**
```python
# ============================================
# ACTIVE INTEGRATION - Change this line to switch
# ============================================

# OPTION 1: Gemini AI Direct Integration (CURRENTLY ACTIVE)
from gemini_llm_service import ChatService, chat_service, professional_chat_service  ✅

# OPTION 2: Emergent LLM Universal Key (COMMENTED OUT)
# Uncomment the line below and comment out the line above to switch to Emergent LLM
# from emergent_llm_service import ChatService, chat_service, professional_chat_service  ❌
```

---

### To Switch to Emergent LLM:

**File: `/app/backend/llm_service.py`**
```python
# ============================================
# ACTIVE INTEGRATION - Change this line to switch
# ============================================

# OPTION 1: Gemini AI Direct Integration (COMMENTED OUT)
# from gemini_llm_service import ChatService, chat_service, professional_chat_service  ❌

# OPTION 2: Emergent LLM Universal Key (CURRENTLY ACTIVE)
from emergent_llm_service import ChatService, chat_service, professional_chat_service  ✅
```

---

## 🔑 API Keys Configuration

**File:** `/app/backend/.env`

Both API keys are already configured:
```bash
# Gemini AI Direct Integration (Currently Active)
GEMINI_API_KEY=AIzaSyAJ8n7uo_L-a05UxCMQ8s7k2J9883ZIUWA

# Emergent LLM Universal Key
EMERGENT_LLM_KEY=sk-emergent-51f67AaD7E6967d742
```

**Note:** You don't need to change the `.env` file when switching. Both keys are always available.

---

## 🎨 What Each File Does

### 1. **`gemini_llm_service.py`**
- Contains Gemini AI direct integration code
- Uses `google.genai` library
- Connects directly to Google's Gemini API
- Model: `gemini-2.0-flash-exp`

### 2. **`emergent_llm_service.py`**
- Contains Emergent LLM integration code
- Uses `emergentintegrations` library
- Universal key supporting OpenAI, Anthropic, Gemini
- Model: `gemini-2.5-flash`

### 3. **`llm_service.py`** (Import Router)
- **This is the ONLY file you need to edit to switch!**
- Simply imports from one of the above files
- Acts as a router between integrations
- No business logic, just one import statement

### 4. **`server.py`**
- Main FastAPI server
- **Never needs to be changed!**
- Imports from `llm_service.py`

---

## ✨ Benefits of This Architecture

✅ **Super Simple Switching** - Change just ONE line instead of commenting 100+ lines  
✅ **Clean Separation** - Each integration has its own file  
✅ **No Code Conflicts** - No risk of accidentally uncommenting wrong sections  
✅ **Easy to Maintain** - Each file is independent and focused  
✅ **Safe** - Can't break one integration while working on another  
✅ **Version Control Friendly** - Easy to see what changed in git diffs  

---

## 🔍 How to Verify Which Integration is Active

### Check the logs:
```bash
tail -n 50 /var/log/supervisor/backend.out.log
```

**Look for:**
- **Gemini AI Active:** `[Gemini AI/gemini-2.0-flash-exp]` in logs
- **Emergent LLM Active:** `[Emergent LLM/gemini/gemini-2.5-flash]` in logs

### Check the backend status:
```bash
curl http://localhost:8001/api/health
```

Should return: `{"status":"healthy"}`

---

## ⚙️ Complete Switching Checklist

1. ✏️ Open `/app/backend/llm_service.py`
2. 🔄 Change the import line (comment one, uncomment the other)
3. 💾 Save the file
4. 🔁 Run: `sudo supervisorctl restart backend`
5. ✅ Verify: `curl http://localhost:8001/api/health`
6. 📊 Check logs: `tail -n 30 /var/log/supervisor/backend.out.log`
7. 🧪 Test the chatbot in frontend

---

## ❗ Important Notes

- **Only edit `llm_service.py`** to switch - nothing else needs to change
- **Both API keys stay in `.env`** - no need to modify them
- **`server.py` never changes** - it always imports from `llm_service.py`
- **Frontend never changes** - same API endpoints regardless of integration
- **Always restart backend** after changing the import

---

## 🐛 Troubleshooting

### Backend won't start after switching:

1. **Check you have only ONE import uncommented** in `llm_service.py`
   - If both are uncommented → Error
   - If both are commented → Error
   
2. **Verify the API key exists** in `.env`:
   - For Gemini: Check `GEMINI_API_KEY=...`
   - For Emergent: Check `EMERGENT_LLM_KEY=...`

3. **Check error logs:**
   ```bash
   tail -n 50 /var/log/supervisor/backend.err.log
   ```

4. **Restart backend manually:**
   ```bash
   sudo supervisorctl restart backend
   ```

---

## 📚 Quick Reference Card

| What You Want | What to Do | File to Edit | Line to Change |
|---------------|-----------|--------------|----------------|
| **Use Gemini AI** | Uncomment Gemini import | `llm_service.py` | Line 20 |
| **Use Emergent LLM** | Uncomment Emergent import | `llm_service.py` | Line 24-25 |
| **After changing** | Restart backend | Terminal | `sudo supervisorctl restart backend` |

---

## 🎓 Example: Complete Switch Process

**Scenario: Want to switch from Gemini to Emergent**

1. Open file:
   ```bash
   nano /app/backend/llm_service.py
   ```

2. Change line 20-21 from:
   ```python
   from gemini_llm_service import ChatService, chat_service, professional_chat_service
   # from emergent_llm_service import ChatService, chat_service, professional_chat_service
   ```
   
   To:
   ```python
   # from gemini_llm_service import ChatService, chat_service, professional_chat_service
   from emergent_llm_service import ChatService, chat_service, professional_chat_service
   ```

3. Save and exit (Ctrl+X, then Y, then Enter)

4. Restart:
   ```bash
   sudo supervisorctl restart backend
   ```

5. Verify:
   ```bash
   curl http://localhost:8001/api/health
   tail -n 30 /var/log/supervisor/backend.out.log
   ```

**Done! ✅ Now using Emergent LLM**

---

This is now the **simplest possible switching mechanism** - just one line change!
