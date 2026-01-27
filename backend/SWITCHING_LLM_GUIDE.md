# How to Switch Between Emergent LLM and Gemini AI

This chatbot supports two LLM integration options that you can easily switch between.

## Current Configuration
**Currently Active: GEMINI AI (Direct Integration)**

## Switching Instructions

### Option 1: Use Gemini AI (Direct) - CURRENTLY ACTIVE ✅

**What to do:**
1. Keep the Gemini AI section in `/app/backend/llm_service.py` UNCOMMENTED (lines 17-83)
2. Keep the Emergent LLM section COMMENTED OUT (lines 86-168)
3. Ensure `GEMINI_API_KEY` is set in `/app/backend/.env`
4. Restart backend: `sudo supervisorctl restart backend`

**Features:**
- Direct access to Google's Gemini API
- Uses google-generativeai SDK
- More control over Gemini-specific features
- Supports conversation history
- Default model: gemini-2.0-flash-exp

---

### Option 2: Use Emergent LLM (Universal Key)

**What to do:**
1. Open `/app/backend/llm_service.py`
2. **Comment out the GEMINI AI section** (lines 17-83):
   - Add `#` at the beginning of every line in that section
   - OR wrap it in `'''` multiline comments
3. **Uncomment the EMERGENT LLM section** (lines 86-168):
   - Remove `#` from the beginning of every line
   - OR remove the `'''` multiline comment markers
4. Ensure `EMERGENT_LLM_KEY` is set in `/app/backend/.env`
5. Restart backend: `sudo supervisorctl restart backend`

**Features:**
- Universal key works across multiple LLM providers (OpenAI, Anthropic, Gemini)
- Uses emergentintegrations library
- Simplified billing and API key management
- Supports conversation history
- Default model: gemini-2.5-flash

---

## Quick Reference: What to Comment/Uncomment

### File: `/app/backend/llm_service.py`

**For Gemini AI Direct (Current Setup):**
```python
# Lines 17-83: UNCOMMENTED ✅
import google.generativeai as genai

class ChatService:
    # ... Gemini implementation
```

```python
# Lines 86-168: COMMENTED OUT ✅
# from emergentintegrations.llm.chat import LlmChat, UserMessage
# 
# class ChatService:
#     # ... Emergent LLM implementation
```

**For Emergent LLM:**
```python
# Lines 17-83: COMMENTED OUT
# import google.generativeai as genai
#
# class ChatService:
#     # ... Gemini implementation
```

```python
# Lines 86-168: UNCOMMENTED
from emergentintegrations.llm.chat import LlmChat, UserMessage

class ChatService:
    # ... Emergent LLM implementation
```

---

## Environment Variables

Both API keys are stored in `/app/backend/.env`:

```bash
# Gemini AI Direct Integration
GEMINI_API_KEY=AIzaSyAJ8n7uo_L-a05UxCMQ8s7k2J9883ZIUWA

# Emergent LLM Universal Key
EMERGENT_LLM_KEY=sk-emergent-51f67AaD7E6967d742
```

**Note:** Only the key for the active integration needs to be set, but having both doesn't hurt.

---

## After Switching

1. **Always restart the backend server:**
   ```bash
   sudo supervisorctl restart backend
   ```

2. **Verify the switch worked:**
   - Check logs: `tail -n 50 /var/log/supervisor/backend.out.log`
   - Test the chatbot in the frontend
   - Look for the correct provider name in console logs

---

## Important Notes

- Both implementations have the **same interface** (same methods and parameters)
- No changes needed in `server.py` or frontend code
- The `chat_service` and `professional_chat_service` instances work with both
- Switching only requires commenting/uncommenting in **one file**: `llm_service.py`
- Always test after switching to ensure the integration works correctly

---

## Troubleshooting

**If chatbot doesn't work after switching:**

1. Check if the correct API key is in `.env`
2. Verify you commented/uncommented the right sections
3. Ensure you restarted the backend: `sudo supervisorctl restart backend`
4. Check logs for errors: `tail -n 100 /var/log/supervisor/backend.err.log`
5. Verify the required libraries are installed:
   - For Gemini: `google-generativeai`
   - For Emergent: `emergentintegrations`

**Common mistakes:**
- Forgetting to uncomment the import statement at the top of the section
- Not restarting the backend after making changes
- Having both sections uncommented (will cause a duplicate class definition error)
- Having both sections commented (will cause no ChatService class found error)
