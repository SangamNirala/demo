"""
LLM Service Module - Import Router
=====================================
This file acts as a simple router to switch between different LLM integrations.

SWITCHING BETWEEN GEMINI AI AND EMERGENT LLM:
==============================================
Simply change the import statement below:

TO USE GEMINI AI (Currently Active):
    from gemini_llm_service import ChatService, chat_service, professional_chat_service

TO USE EMERGENT LLM:
    from emergent_llm_service import ChatService, chat_service, professional_chat_service

That's it! Just change one line and restart the backend.
"""

# ============================================
# ACTIVE INTEGRATION - Change this line to switch
# ============================================

# OPTION 1: Gemini AI Direct Integration (CURRENTLY ACTIVE)
from gemini_llm_service import ChatService, chat_service, professional_chat_service

# OPTION 2: Emergent LLM Universal Key (COMMENTED OUT)
# Uncomment the line below and comment out the line above to switch to Emergent LLM
# from emergent_llm_service import ChatService, chat_service, professional_chat_service


# ============================================
# Export for server.py
# ============================================
__all__ = ['ChatService', 'chat_service', 'professional_chat_service']
