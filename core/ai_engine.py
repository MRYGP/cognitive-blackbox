# cognitive-blackbox/core/ai_engine.py (Fixed Version by Hoshino)
"""
Cognitive Black Box - Enhanced AI Engine (Refactored & Fixed)
This version simplifies the async call to ensure API invocation in Streamlit.
"""

import streamlit as st
import os
import time
import json
import logging
from typing import Dict, Any, Tuple, List

# AI API imports with error handling
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# --- Simplified Configuration ---
MAX_RESPONSE_TIME = 15.0  # Increased timeout for debugging
CACHE_TTL = 3600

class EnhancedAIEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gemini_client = None
        self._initialize_clients()
        # Using a simple dict as an in-memory cache
        self.response_cache = {}

    def _initialize_clients(self):
        if not GENAI_AVAILABLE:
            self.logger.warning("google-generativeai library not installed. AI Engine will not work.")
            return
        
        try:
            gemini_api_key = st.secrets.get('GEMINI_API_KEY')
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                # Model name might need to be adjusted based on availability
                self.gemini_client = genai.GenerativeModel('gemini-1.5-flash')
                self.logger.info("Gemini client initialized successfully.")
            else:
                self.logger.warning("GEMINI_API_KEY not found in Streamlit Secrets.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini client: {str(e)}")

    def generate_response(self, role_id: str, user_input: str, context: Dict[str, Any]) -> Tuple[str, bool]:
        """
        Synchronous, direct AI response generation for simplicity and robustness in Streamlit.
        """
        start_time = time.time()
        
        # 1. Check if AI client is available
        if not self.gemini_client:
            self.logger.error("AI client not available. Returning fallback.")
            return self._get_fallback_response(role_id, context), False

        # 2. Build the full prompt (This part is crucial)
        # Assuming prompts are loaded elsewhere and passed in context or loaded here
        # For now, using a simple prompt structure
        system_prompt = f"You are a helpful assistant acting as a {role_id}." # Placeholder
        full_prompt = f"{system_prompt}\n\nContext: {json.dumps(context)}\n\nUser asks: {user_input}\n\nYour response:"

        # 3. Direct API Call (Synchronous)
        try:
            self.logger.info(f"Calling Gemini API for role: {role_id}...")
            
            # The actual API call
            response = self.gemini_client.generate_content(full_prompt)
            
            # Check for valid response
            if response and hasattr(response, 'text') and response.text:
                ai_text = response.text.strip()
                self.logger.info(f"Successfully received response from Gemini. Time: {time.time() - start_time:.2f}s")
                return ai_text, True
            else:
                # Handle cases where the API returns an empty or invalid response
                self.logger.warning("Received an empty or invalid response from API.")
                return self._get_fallback_response(role_id, context), False

        except Exception as e:
            # Handle all other exceptions during the API call
            self.logger.error(f"Error during Gemini API call for role '{role_id}': {str(e)}", exc_info=True)
            return self._get_fallback_response(role_id, context), False

    def _get_fallback_response(self, role_id: str, context: Dict[str, Any]) -> str:
        """Provides a static, predefined fallback response."""
        # This can be expanded with more sophisticated logic from your JSON files
        fallback_responses = {
            'investor': "经过深入分析，您的决策中存在几个值得探讨的关键风险点。",
            'assistant': "正在为您生成一份专业的决策工具模板。"
        }
        return fallback_responses.get(role_id, "服务暂时出现问题，请稍后再试。")

# Global instance
ai_engine = EnhancedAIEngine()
