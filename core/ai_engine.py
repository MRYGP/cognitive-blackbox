"""
Cognitive Black Box - Enhanced AI Engine (Refactored)
Supports async calls, error degradation, caching, and timeout control
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
    st.warning("AI API libraries not fully installed. Running in fallback mode.")

class AIEngineConfig:
    """AI Engine configuration"""
    def __init__(self):
        self.max_response_time = 3.0  # seconds
        self.cache_ttl = 3600  # 1 hour
        self.max_retries = 2
        self.fallback_enabled = True
        
        # API model configurations
        self.api_config = {
            'gemini': {
                'model': 'gemini-2.0-flash-exp',
                'temperature': 0.7,
                'max_tokens': 2048,
                'timeout': 10
            },
            'claude': {
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.7,
                'max_tokens': 2048,
                'timeout': 10
            }
        }

class AIRole:
    """AI Role definition with prompt management"""
    def __init__(self, role_id: str, config: Dict[str, Any]):
        self.role_id = role_id
        self.name = config.get('name', '')
        self.description = config.get('description', '')
        self.color_theme = config.get('color_theme', 'blue')
        self.expertise = config.get('expertise', '')
        self.system_prompt = config.get('system_prompt', '')
        self.fallback_responses = config.get('fallback_responses', {})

class EnhancedAIEngine:
    """
    Enhanced AI Engine with async support, error handling, and caching
    """
    
    def __init__(self, prompts_dir: str = "config/prompts"):
        """Initialize enhanced AI engine"""
        self.config = AIEngineConfig()
        self.prompts_dir = Path(prompts_dir)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize API clients
        self.gemini_client = None
        self.claude_client = None
        self._initialize_clients()
        
        # Role management
        self.roles = {}
        self._load_roles()
        
        # Cache and performance tracking
        self.response_cache = {}
        self.performance_metrics = {
            'total_calls': 0,
            'successful_calls': 0,
            'cache_hits': 0,
            'timeouts': 0,
            'errors': 0
        }
    
    def _setup_logging(self) -> None:
        """Setup logging for AI engine"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _initialize_clients(self) -> None:
        """Initialize AI API clients with error handling"""
        if not APIS_AVAILABLE:
            self.logger.warning("AI APIs not available, using fallback mode")
            return
        
        try:
            # Initialize Gemini
            gemini_api_key = os.getenv('GEMINI_API_KEY') or st.secrets.get('GEMINI_API_KEY')
            if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
                genai.configure(api_key=gemini_api_key)
                self.gemini_client = genai.GenerativeModel('gemini-2.0-flash-exp')
                self.logger.info("Gemini client initialized successfully")
            
            # Initialize Claude
            claude_api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY')
            if claude_api_key and claude_api_key != "your_anthropic_api_key_here":
                self.claude_client = Anthropic(api_key=claude_api_key)
                self.logger.info("Claude client initialized successfully")
                
        except Exception as e:
            self.logger.error(f"API client initialization failed: {str(e)}")
    
    def _load_roles(self) -> None:
        """Load AI roles from configuration files"""
        # Default roles with fallback content
        default_roles = {
            'host': {
                'name': 'Professional Host',
                'description': 'Guide decision analysis and build case immersion',
                'color_theme': 'blue',
                'expertise': 'business decision analysis, user guidance',
                'system_prompt': self._get_default_host_prompt(),
                'fallback_responses': {
                    'greeting': '欢迎来到认知黑匣子，让我们开始这次重要的认知升级之旅。',
                    'transition': '感谢您的参与，让我们继续分析这个重要的案例。'
                }
            },
            'investor': {
                'name': 'Wall Street Investor',
                'description': 'Expose cognitive blind spots through sharp questioning',
                'color_theme': 'red',
                'expertise': 'investment analysis, reality disruption',
                'system_prompt': self._get_default_investor_prompt(),
                'fallback_responses': {
                    'challenge': '让我们看看这个决策背后的真实数据和风险。',
                    'shock': '现实往往比我们想象的更残酷，让我告诉您真相。'
                }
            },
            'mentor': {
                'name': 'Cognitive Science Mentor',
                'description': 'Provide theoretical frameworks and insights',
                'color_theme': 'green',
                'expertise': 'behavioral economics, cognitive science',
                'system_prompt': self._get_default_mentor_prompt(),
                'fallback_responses': {
                    'framework': '让我从认知科学的角度为您分析这个现象。',
                    'wisdom': '理解认知偏误是提升决策能力的第一步。'
                }
            },
            'assistant': {
                'name': 'Executive Assistant',
                'description': 'Transform insights into actionable tools',
                'color_theme': 'cyan',
                'expertise': 'decision tools, practical implementation',
                'system_prompt': self._get_default_assistant_prompt(),
                'fallback_responses': {
                    'tool': '让我为您量身定制实用的决策工具。',
                    'implementation': '现在让我们将理论转化为实际的行动指南。'
                }
            }
        }
        
        # Load roles from files or use defaults
        for role_id, role_config in default_roles.items():
            try:
                role_file = self.prompts_dir / f"{role_id}.json"
                if role_file.exists():
                    with open(role_file, 'r', encoding='utf-8') as f:
                        file_config = json.load(f)
                        role_config.update(file_config)
                
                self.roles[role_id] = AIRole(role_id, role_config)
                
            except Exception as e:
                self.logger.warning(f"Failed to load role '{role_id}' from file, using default: {str(e)}")
                self.roles[role_id] = AIRole(role_id, role_config)
    
    async def generate_response_async(self, 
                                    role_id: str, 
                                    user_input: str, 
                                    context: Dict[str, Any],
                                    api_preference: str = 'gemini') -> Tuple[str, bool]:
        """
        Generate AI response asynchronously with timeout and error handling
        
        Args:
            role_id: Role identifier
            user_input: User input text
            context: Current context
            api_preference: Preferred API ('gemini' or 'claude')
        
        Returns:
            Tuple[str, bool]: (response content, success flag)
        """
        start_time = time.time()
        self.performance_metrics['total_calls'] += 1
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(role_id, user_input, context)
            if cache_key in self.response_cache:
                cache_entry = self.response_cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.config.cache_ttl:
                    self.performance_metrics['cache_hits'] += 1
                    self.logger.info(f"Cache hit for role '{role_id}'")
                    return cache_entry['response'], True
            
            # Build prompt
            full_prompt = self._build_prompt(role_id, user_input, context)
            
            # Call API with timeout
            try:
                response = await asyncio.wait_for(
                    self._call_api_async(full_prompt, api_preference),
                    timeout=self.config.max_response_time
                )
                
                if response:
                    # Cache successful response
                    self.response_cache[cache_key] = {
                        'response': response,
                        'timestamp': time.time()
                    }
                    
                    self.performance_metrics['successful_calls'] += 1
                    
                    response_time = time.time() - start_time
                    self.logger.info(f"AI response generated for '{role_id}' in {response_time:.2f}s")
                    
                    return response, True
                else:
                    raise Exception("Empty response from API")
                    
            except asyncio.TimeoutError:
                self.performance_metrics['timeouts'] += 1
                self.logger.warning(f"Timeout for role '{role_id}', using fallback")
                return self._get_fallback_response(role_id, context), False
            
        except Exception as e:
            self.performance_metrics['errors'] += 1
            self.logger.error(f"Error generating response for '{role_id}': {str(e)}")
            return self._get_fallback_response(role_id, context), False
    
    def generate_response(self, 
                         role_id: str, 
                         user_input: str, 
                         context: Dict[str, Any],
                         api_preference: str = 'gemini') -> Tuple[str, bool]:
        """
        Synchronous wrapper for async response generation
        """
        try:
            # Try to run in existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, use fallback
                self.logger.info("Event loop already running, using fallback response")
                return self._get_fallback_response(role_id, context), False
            else:
                return loop.run_until_complete(
                    self.generate_response_async(role_id, user_input, context, api_preference)
                )
        except RuntimeError:
            # No event loop, create new one
            return asyncio.run(
                self.generate_response_async(role_id, user_input, context, api_preference)
            )
    
    async def _call_api_async(self, prompt: str, api_preference: str) -> Optional[str]:
        """Call AI API asynchronously"""
        if not APIS_AVAILABLE:
            return None
        
        try:
            if api_preference == 'gemini' and self.gemini_client:
                return await self._call_gemini_async(prompt)
            elif api_preference == 'claude' and self.claude_client:
                return await self._call_claude_async(prompt)
            else:
                # Fallback to available API
                if self.gemini_client:
                    return await self._call_gemini_async(prompt)
                elif self.claude_client:
                    return await self._call_claude_async(prompt)
                else:
                    raise Exception("No available API client")
                    
        except Exception as e:
            self.logger.error(f"API call failed: {str(e)}")
            return None
    
    async def _call_gemini_async(self, prompt: str) -> Optional[str]:
        """Call Gemini API asynchronously"""
        try:
            # Gemini doesn't have native async support, so we run in executor
            loop = asyncio.get_event_loop()
            
            def call_gemini():
                response = self.gemini_client.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.config.api_config['gemini']['temperature'],
                        max_output_tokens=self.config.api_config['gemini']['max_tokens']
                    )
                )
                return response.text.strip() if response and response.text else None
            
            response = await loop.run_in_executor(None, call_gemini)
            return response
            
        except Exception as e:
            self.logger.error(f"Gemini API call failed: {str(e)}")
            return None
    
    async def _call_claude_async(self, prompt: str) -> Optional[str]:
        """Call Claude API asynchronously"""
        try:
            # Claude client doesn't have native async, so we run in executor
            loop = asyncio.get_event_loop()
            
            def call_claude():
                response = self.claude_client.messages.create(
                    model=self.config.api_config['claude']['model'],
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.api_config['claude']['temperature'],
                    max_tokens=self.config.api_config['claude']['max_tokens']
                )
                return response.content[0].text.strip() if response and response.content else None
            
            response = await loop.run_in_executor(None, call_claude)
            return response
            
        except Exception as e:
            self.logger.error(f"Claude API call failed: {str(e)}")
            return None
    
    def _build_prompt(self, role_id: str, user_input: str, context: Dict[str, Any]) -> str:
        """Build complete prompt for AI"""
        role = self.roles.get(role_id)
        if not role:
            return f"Please respond as {role_id}: {user_input}"
        
        # Build context information
        context_info = self._build_context_info(context)
        
        # Build complete prompt
        prompt_parts = [
            f"Role: {role.name}",
            f"Description: {role.description}",
            f"Expertise: {role.expertise}",
            "",
            "System Instructions:",
            role.system_prompt,
            "",
            "Context:",
            context_info,
            "",
            "User Input:",
            user_input,
            "",
            "Please generate a response that:",
            "1. Matches the role's expertise and communication style",
            "2. Advances the overall experience flow", 
            "3. Incorporates relevant context information",
            "4. Maintains professionalism and impact",
            "5. Uses Chinese language naturally and professionally"
        ]
        
        return "\n".join(prompt_parts)
    
    def _build_context_info(self, context: Dict[str, Any]) -> str:
        """Build context information string"""
        context_lines = []
        
        # Basic session info
        context_lines.append(f"Case: {context.get('case_name', 'madoff')}")
        context_lines.append(f"Current Step: {context.get('current_step', 1)}/4")
        context_lines.append(f"Current Role: {context.get('current_role', 'host')}")
        
        # User decisions
        user_decisions = context.get('user_decisions', {})
        if user_decisions:
            context_lines.append("")
            context_lines.append("User's Previous Decisions:")
            for decision_id, decision_content in user_decisions.items():
                context_lines.append(f"- {decision_id}: {decision_content[:100]}...")
        
        # Conversation history (recent items)
        conversation_history = context.get('conversation_history', [])
        if conversation_history:
            context_lines.append("")
            context_lines.append("Recent Conversation:")
            for turn in conversation_history[-3:]:
                role = turn.get('role', 'unknown')
                message = turn.get('message', '')[:100]
                context_lines.append(f"- {role}: {message}...")
        
        return "\n".join(context_lines)
    
    def _generate_cache_key(self, role_id: str, user_input: str, context: Dict[str, Any]) -> str:
        """Generate cache key for response"""
        key_components = [
            role_id,
            user_input[:50],  # First 50 characters
            str(context.get('current_step', 1)),
            str(len(context.get('user_decisions', {})))
        ]
        return "|".join(key_components)
    
    def _get_fallback_response(self, role_id: str, context: Dict[str, Any]) -> str:
        """Get fallback response for role"""
        role = self.roles.get(role_id)
        if not role:
            return "让我们继续我们的分析和讨论。"
        
        # Get context-appropriate fallback
        current_step = context.get('current_step', 1)
        
        fallback_map = {
            1: role.fallback_responses.get('greeting', '欢迎参与这次重要的认知体验。'),
            2: role.fallback_responses.get('challenge', '让我们深入分析这个案例的关键问题。'),
            3: role.fallback_responses.get('framework', '现在让我为您提供理论框架和分析工具。'),
            4: role.fallback_responses.get('tool', '让我们将学到的知识转化为实用的工具。')
        }
        
        return fallback_map.get(current_step, role.fallback_responses.get('greeting', '让我们继续这次重要的学习之旅。'))
    
    def _get_default_host_prompt(self) -> str:
        """Get default host system prompt"""
        return """
你是认知黑匣子的专业主持人，负责引导用户进行深度的决策分析。

核心职责：
1. 创建专业的决策分析氛围
2. 通过结构化提问收集用户背景信息
3. 构建用户对案例的沉浸感
4. 为后续认知冲击做好铺垫

沟通风格：
- 专业而亲和，权威但不失亲近感
- 使用商业决策相关术语
- 保持清晰的逻辑表达
- 体现对用户决策经验的尊重

当前阶段：第一幕 - 决策代入
"""
    
    def _get_default_investor_prompt(self) -> str:
        """Get default investor system prompt"""
        return """
你是一位经验丰富的华尔街投资人，用犀利的质疑和残酷的数据击碎用户的认知假设。

核心职责：
1. 用震撼性数据揭示案例的真实后果
2. 通过专业质疑暴露用户决策中的认知盲点
3. 创造强烈的认知失调和反思
4. 为理论解释阶段做好情感铺垫

沟通风格：
- 直接犀利，毫不留情
- 大量使用具体数字和对比
- 反问句和挑战性表达
- 制造紧张感和压力感

当前阶段：第二幕 - 现实击穿
"""
    
    def _get_default_mentor_prompt(self) -> str:
        """Get default mentor system prompt"""  
        return """
你是一位精通行为经济学和认知科学的导师，负责从理论角度解释案例背后的认知机制。

核心职责：
1. 提供权威的理论解释和科学证据
2. 构建系统性的认知框架
3. 将震撼转化为深刻洞察
4. 为实用工具应用奠定理论基础

沟通风格：
- 深刻启发，理论联系实践
- 引用权威研究和经典理论
- 逻辑严密，层次清晰
- 体现智慧和洞察力

当前阶段：第三幕 - 框架重构
"""
    
    def _get_default_assistant_prompt(self) -> str:
        """Get default assistant system prompt"""
        return """
你是一位专业的执行助理，负责将理论转化为可操作的决策工具。

核心职责：
1. 设计个性化的决策安全系统
2. 提供具体的应用指导
3. 强化用户的能力建设
4. 确保实用价值的转化

沟通风格：
- 实用专业，注重可操作性
- 结构清晰，步骤明确
- 鼓励但不夸大
- 体现执行力和支持感

当前阶段：第四幕 - 能力武装
"""
    
    def get_role_info(self, role_id: str) -> Dict[str, Any]:
        """Get role information"""
        role = self.roles.get(role_id)
        if not role:
            return {}
        
        return {
            'name': role.name,
            'description': role.description,
            'color_theme': role.color_theme,
            'expertise': role.expertise
        }
    
    def get_available_apis(self) -> List[str]:
        """Get list of available APIs"""
        available = []
        if self.gemini_client:
            available.append('gemini')
        if self.claude_client:
            available.append('claude')
        return available
    
    def clear_cache(self) -> None:
        """Clear response cache"""
        self.response_cache.clear()
        self.logger.info("Response cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache and performance statistics"""
        return {
            'cache_size': len(self.response_cache),
            'performance_metrics': self.performance_metrics.copy(),
            'available_apis': self.get_available_apis(),
            'total_roles': len(self.roles),
            'config': {
                'max_response_time': self.config.max_response_time,
                'cache_ttl': self.config.cache_ttl,
                'fallback_enabled': self.config.fallback_enabled
            }
        }
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update engine configuration"""
        if 'max_response_time' in new_config:
            self.config.max_response_time = new_config['max_response_time']
        if 'cache_ttl' in new_config:
            self.config.cache_ttl = new_config['cache_ttl']
        if 'fallback_enabled' in new_config:
            self.config.fallback_enabled = new_config['fallback_enabled']
        
        self.logger.info("AI engine configuration updated")

# Global enhanced AI engine instance
ai_engine = EnhancedAIEngine()
