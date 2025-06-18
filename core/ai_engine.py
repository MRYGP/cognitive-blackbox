# cognitive-blackbox/core/ai_engine.py (Final Refactored Version)
import streamlit as st
import logging
import time
import json
from pathlib import Path
from typing import Dict, Any, Tuple

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class AIEngine:
    def __init__(self, prompts_dir: str = "config/prompts"):
        self.logger = logging.getLogger(__name__)
        self.prompts_dir = Path(prompts_dir)
        self.roles_prompts = {}
        self.gemini_client = None
        
        self._load_all_prompts()
        self._initialize_clients()

    def _initialize_clients(self):
        if not GENAI_AVAILABLE:
            self.logger.warning("google-genai library not found. AI Engine is disabled.")
            return
        try:
            gemini_api_key = st.secrets.get('GEMINI_API_KEY')
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                # Using a stable and recent model
                self.gemini_client = genai.GenerativeModel('gemini-1.5-flash-latest')
                self.logger.info("Gemini client initialized successfully.")
            else:
                self.logger.warning("GEMINI_API_KEY not found in Streamlit Secrets. AI will not function.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini client: {str(e)}")

    def _load_all_prompts(self):
        """Loads all role prompts from the specified directory."""
        if not self.prompts_dir.is_dir():
            self.logger.error(f"Prompts directory not found: {self.prompts_dir}")
            return
        for file_path in self.prompts_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    role_data = json.load(f)
                    role_id = role_data.get('role_id')
                    if role_id:
                        self.roles_prompts[role_id] = role_data
                        self.logger.info(f"Loaded prompt for role: {role_id}")
            except Exception as e:
                self.logger.error(f"Failed to load prompt from {file_path}: {e}")
    
    def _build_prompt(self, role_id: str, user_input: str, context: Dict[str, Any]) -> str:
        """Builds a high-quality, structured prompt based on the loaded JSON configuration."""
        role_config = self.roles_prompts.get(role_id)
        if not role_config:
            self.logger.warning(f"No prompt config found for role '{role_id}'. Using a generic prompt.")
            return f"Act as a {role_id}. The user input is: {user_input}. The context is: {json.dumps(context)}"
            
        system_prompt = role_config.get('system_prompt', f"You are an expert {role_id}.")
        
        # Dynamically create context string from what's available
        context_str_parts = []
        if 'case_name' in context:
            context_str_parts.append(f"- Case: {context['case_name']}")
        if 'current_step' in context:
            context_str_parts.append(f"- Current Step: {context['current_step']}")
        if 'user_decisions' in context:
            decisions = json.dumps(context['user_decisions'], ensure_ascii=False, indent=2)
            context_str_parts.append(f"- User's Previous Decisions:\n{decisions}")

        context_str = "\n".join(context_str_parts)

        # Use personalization templates if they exist
        personalization_key = context.get('user_decisions', {}).get('dp_final_decision')
        personalization_template = role_config.get('personalization_templates', {}).get(personalization_key)
        
        if personalization_template:
            final_user_input = personalization_template
        else:
            final_user_input = user_input

        full_prompt = f"""
        {system_prompt}

        ---
        **CONTEXT:**
        {context_str}
        ---
        **USER'S TASK / LATEST INPUT:**
        {final_user_input}
        ---

        Please provide your expert response now.
        """
        return full_prompt

    def generate_response(self, role_id: str, user_input: str, context: Dict[str, Any]) -> Tuple[str, bool]:
        """Generates a response using the configured Gemini client."""
        if not self.gemini_client:
            self.logger.error("AI client not available. Returning fallback.")
            return self._get_fallback_response(role_id, context), False

        full_prompt = self._build_prompt(role_id, user_input, context)
        self.logger.info(f"Generated prompt for '{role_id}':\n{full_prompt[:500]}...") # Log first 500 chars

        try:
            self.logger.info(f"Calling Gemini API for role: {role_id}...")
            start_time = time.time()
            
            response = self.gemini_client.generate_content(full_prompt)
            
            if response and hasattr(response, 'text') and response.text:
                ai_text = response.text.strip()
                self.logger.info(f"Successfully received response. Time: {time.time() - start_time:.2f}s")
                return ai_text, True
            else:
                self.logger.warning("Received an empty or invalid response from API.")
                return self._get_fallback_response(role_id, context), False

        except Exception as e:
            self.logger.error(f"Error during Gemini API call: {str(e)}", exc_info=True)
            return self._get_fallback_response(role_id, context), False

    def _get_fallback_response(self, role_id: str, context: Dict[str, Any]) -> str:
        """Provides a static, predefined fallback response from config if available."""
        role_config = self.roles_prompts.get(role_id, {})
        fallback_responses = role_config.get('fallback_responses', {})
        # Choose a context-aware fallback if possible
        return fallback_responses.get('technical_issue', "AI服务暂时繁忙，为您提供专业的标准分析。")

# Global instance
ai_engine = AIEngine()
