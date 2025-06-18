# cognitive-blackbox/core/ai_engine.py (Final Fixed Version for new SDK)
import streamlit as st
import logging
import time
from typing import Dict, Any, Tuple

try:
    # Import the new, recommended SDK
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class EnhancedAIEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.gemini_client = None
        self._initialize_clients()

    def _initialize_clients(self):
        if not GENAI_AVAILABLE:
            self.logger.warning("google-genai library not found. AI Engine is disabled.")
            return
        
        try:
            gemini_api_key = st.secrets.get('GEMINI_API_KEY')
            if gemini_api_key:
                # The initialization method for the new SDK
                genai.configure(api_key=gemini_api_key)
                # Model name might need to be adjusted, 'gemini-1.5-flash' is current
                self.gemini_client = genai.GenerativeModel('gemini-1.5-flash')
                self.logger.info("Gemini client initialized successfully with new SDK.")
            else:
                self.logger.warning("GEMINI_API_KEY not found in Streamlit Secrets.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini client: {str(e)}")

    def generate_response(self, role_id: str, user_input: str, context: Dict[str, Any]) -> Tuple[str, bool]:
        """
        Generates a response using the configured Gemini client.
        """
        if not self.gemini_client:
            self.logger.error("AI client not available. Returning fallback.")
            return self._get_fallback_response(role_id, context), False

        # Assume prompt building logic exists here
        # For simplicity, we create a direct prompt. In production, this would use a template.
        full_prompt = f"Act as a {role_id}. The user says: '{user_input}'. The context is: {context}. Please respond."

        try:
            self.logger.info(f"Calling Gemini API for role: {role_id}...")
            start_time = time.time()
            
            # API call using the new SDK's method
            response = self.gemini_client.generate_content(full_prompt)
            
            if response and hasattr(response, 'text') and response.text:
                ai_text = response.text.strip()
                self.logger.info(f"Successfully received response. Time: {time.time() - start_time:.2f}s")
                return ai_text, True
            else:
                self.logger.warning("Received an empty response from API.")
                return self._get_fallback_response(role_id, context), False

        except Exception as e:
            self.logger.error(f"Error during Gemini API call: {str(e)}", exc_info=True)
            return self._get_fallback_response(role_id, context), False

    def _get_fallback_response(self, role_id: str, context: Dict[str, Any]) -> str:
        """Provides a static, predefined fallback response."""
        return f"AI服务暂时繁忙，为您提供专业的标准分析。（角色：{role_id}）"

# Global instance
ai_engine = EnhancedAIEngine()
