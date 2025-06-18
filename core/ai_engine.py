# cognitive-blackbox/core/ai_engine.py (Final Fixed Version by Hoshino, respecting C's architecture)
"""
Cognitive Black Box - Enhanced AI Engine (Refactored)
This version contains a critical fix for running async code within Streamlit's environment,
while preserving all of C's advanced features like caching, fallbacks, and multi-API support.
"""

import streamlit as st
import asyncio
import os
import time
import json
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from pathlib import Path
import logging

# AI API imports with error handling
try:
    import google.generativeai as genai
    from anthropic import Anthropic
    APIS_AVAILABLE = True
except ImportError:
    APIS_AVAILABLE = False
    # This warning will appear on the Streamlit UI if libraries are missing
    st.warning("AI API libraries (google-generativeai, anthropic) not installed. AI will run in fallback mode.")

class AIEngineConfig:
    """AI Engine configuration, preserved from C's design."""
    def __init__(self):
        self.max_response_time = 15.0  # Increased for initial debugging
        self.cache_ttl = 3600
        self.max_retries = 2
        self.fallback_enabled = True
        self.api_config = {
            'gemini': {'model': 'gemini-1.5-flash-latest', 'temperature': 0.7, 'max_tokens': 2048},
            'claude': {'model': 'claude-3-5-sonnet-20240620', 'temperature': 0.7, 'max_tokens': 2048}
        }

class AIRole:
    """AI Role definition, preserved from C's design."""
    def __init__(self, role_id: str, config: Dict[str, Any]):
        self.role_id = role_id
        self.name = config.get('name', '')
        self.system_prompt = config.get('system_prompt', '')
        self.fallback_responses = config.get('fallback_responses', {})

class EnhancedAIEngine:
    """Enhanced AI Engine, preserving C's architecture with a critical fix."""
    
    def __init__(self, prompts_dir: str = "config/prompts"):
        self.config = AIEngineConfig()
        self.prompts_dir = Path(prompts_dir)
        self._setup_logging()
        self.gemini_client = None
        self.claude_client = None
        self._initialize_clients()
        self.roles: Dict[str, AIRole] = {}
        self._load_roles()
        self.response_cache = {}
        self.performance_metrics = {'total_calls': 0, 'successful_calls': 0, 'cache_hits': 0, 'timeouts': 0, 'errors': 0}

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def _initialize_clients(self):
        if not APIS_AVAILABLE:
            return
        try:
            gemini_api_key = st.secrets.get('GEMINI_API_KEY')
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                self.gemini_client = genai.GenerativeModel(self.config.api_config['gemini']['model'])
                self.logger.info("Gemini client initialized successfully.")
            else:
                self.logger.warning("GEMINI_API_KEY not found in Streamlit Secrets.")
            # Claude client initialization preserved
            claude_api_key = st.secrets.get('ANTHROPIC_API_KEY')
            if claude_api_key:
                self.claude_client = Anthropic(api_key=claude_api_key)
                self.logger.info("Claude client initialized successfully.")
        except Exception as e:
            self.logger.error(f"API client initialization failed: {str(e)}")

    def _load_roles(self):
        if not self.prompts_dir.is_dir():
            self.logger.error(f"Prompts directory not found: {self.prompts_dir}")
            return
        for role_id in ['host', 'investor', 'mentor', 'assistant']:
            try:
                role_file = self.prompts_dir / f"{role_id}.json"
                if role_file.exists():
                    with open(role_file, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                        self.roles[role_id] = AIRole(role_id, config_data)
                        self.logger.info(f"Successfully loaded prompt for role: {role_id}")
                else:
                    self.logger.warning(f"Prompt file not found for role: {role_id}. AI may not function for this role.")
            except Exception as e:
                self.logger.error(f"Failed to load role '{role_id}': {str(e)}")

    # =================================================================================
    # === CRITICAL FIX by Hoshino (S): Replaced the synchronous wrapper function ===
    # =================================================================================
    def generate_response(self, role_id: str, user_input: str, context: Dict[str, Any], api_preference: str = 'gemini') -> Tuple[str, bool]:
        """
        A robust synchronous wrapper for the async response generation.
        This is the key fix to resolve the event loop conflict with Streamlit.
        """
        try:
            # This is a more reliable way to run an async function from a sync context
            # without conflicting with Streamlit's own event loop management.
            return asyncio.run(self.generate_response_async(role_id, user_input, context, api_preference))
        except Exception as e:
            self.logger.error(f"Error in sync wrapper for generate_response: {str(e)}", exc_info=True)
            return self._get_fallback_response(role_id, context), False
    # =================================================================================
    # === END OF CRITICAL FIX ===
    # =================================================================================

    async def generate_response_async(self, role_id: str, user_input: str, context: Dict[str, Any], api_preference: str = 'gemini') -> Tuple[str, bool]:
        """Async generation logic, preserved from C's design."""
        self.performance_metrics['total_calls'] += 1
        
        # Cache logic preserved
        cache_key = self._generate_cache_key(role_id, user_input, context)
        if cache_key in self.response_cache and (time.time() - self.response_cache[cache_key]['timestamp'] < self.config.cache_ttl):
            self.performance_metrics['cache_hits'] += 1
            return self.response_cache[cache_key]['response'], True

        full_prompt = self._build_prompt(role_id, user_input, context)
        if not full_prompt:
             return self._get_fallback_response(role_id, context), False

        try:
            response = await asyncio.wait_for(
                self._call_api_async(full_prompt, api_preference),
                timeout=self.config.max_response_time
            )
            if response:
                self.response_cache[cache_key] = {'response': response, 'timestamp': time.time()}
                self.performance_metrics['successful_calls'] += 1
                return response, True
            else:
                raise Exception("API returned an empty response.")
        except asyncio.TimeoutError:
            self.performance_metrics['timeouts'] += 1
            self.logger.warning(f"Timeout for role '{role_id}', using fallback.")
            return self._get_fallback_response(role_id, context), False
        except Exception as e:
            self.performance_metrics['errors'] += 1
            self.logger.error(f"Error in generate_response_async for '{role_id}': {str(e)}")
            return self._get_fallback_response(role_id, context), False

    async def _call_api_async(self, prompt: str, api_preference: str) -> Optional[str]:
        """API calling logic, preserved from C's design."""
        if api_preference == 'gemini' and self.gemini_client:
            return await self._call_gemini_async(prompt)
        elif api_preference == 'claude' and self.claude_client:
            return await self._call_claude_async(prompt)
        elif self.gemini_client:
            return await self._call_gemini_async(prompt)
        elif self.claude_client:
            return await self._call_claude_async(prompt)
        else:
            self.logger.error("No available or configured API client.")
            return None

    async def _call_gemini_async(self, prompt: str) -> Optional[str]:
        """Async Gemini call, preserved from C's design."""
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: self.gemini_client.generate_content(prompt))
            return response.text.strip() if response and hasattr(response, 'text') else None
        except Exception as e:
            self.logger.error(f"Gemini API call failed: {str(e)}")
            return None

    async def _call_claude_async(self, prompt: str) -> Optional[str]:
        """Async Claude call, preserved from C's design."""
        # This logic remains for multi-api support in the future
        try:
            loop = asyncio.get_running_loop()
            def call_claude_sync():
                response = self.claude_client.messages.create(
                    model=self.config.api_config['claude']['model'],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.config.api_config['claude']['max_tokens']
                )
                return response.content[0].text.strip() if response.content else None
            return await loop.run_in_executor(None, call_claude_sync)
        except Exception as e:
            self.logger.error(f"Claude API call failed: {str(e)}")
            return None

    def _build_prompt(self, role_id: str, user_input: str, context: Dict[str, Any]) -> Optional[str]:
        """Prompt building logic, now correctly uses loaded JSON configs."""
        role = self.roles.get(role_id)
        if not role:
            self.logger.error(f"Prompt config for role '{role_id}' not found.")
            return None
        
        context_info = json.dumps(context, ensure_ascii=False, indent=2)
        
        # Using a more robust formatting
        return role.system_prompt.format(
            context=context_info,
            user_input=user_input
        )

    def _generate_cache_key(self, role_id: str, user_input: str, context: Dict[str, Any]) -> str:
        """Cache key generation, preserved from C's design."""
        return f"{role_id}|{user_input[:100]}|{context.get('current_step')}"

    def _get_fallback_response(self, role_id: str, context: Dict[str, Any]) -> str:
        """Fallback logic, preserved from C's design."""
        role = self.roles.get(role_id)
        if role and role.fallback_responses:
            return role.fallback_responses.get('technical_issue', "AI服务暂时繁忙，请稍后再试。")
        return "AI服务暂时繁忙，请稍后再试。"

    # All other utility methods from C's design are preserved below...
    def get_available_apis(self) -> List[str]:
        available = []
        if self.gemini_client: available.append('gemini')
        if self.claude_client: available.append('claude')
        return available
    def clear_cache(self): self.response_cache.clear()
    def get_cache_stats(self): return {'cache_size': len(self.response_cache), 'performance': self.performance_metrics}

# Global instance, as designed by C
ai_engine = EnhancedAIEngine()
