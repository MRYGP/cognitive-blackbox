"""
Cognitive Black Box - AI Role Engine (Debug Version)
Manages four AI characters: Host, Investor, Mentor, Assistant
Handles role switching, prompt management, and API calls
"""

import streamlit as st
import os
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime

# AI API imports
try:
    import google.generativeai as genai
    from anthropic import Anthropic
except ImportError:
    st.warning("AI API libraries not installed. Please install google-generativeai and anthropic.")

class AIRoleEngine:
    """
    AI role engine
    Manages four role characters, handles API calls and role switching
    """
    
    def __init__(self):
        """Initialize AI role engine"""
        # Define four core roles
        self.roles = {
            'host': {
                'name': 'Professional Host',
                'description': 'guide decision analysis and build case immersion',
                'color_theme': 'blue',
                'expertise': 'business decision analysis, user guidance'
            },
            'investor': {
                'name': 'Wall Street Investor', 
                'description': 'expose cognitive blind spots through sharp questioning',
                'color_theme': 'red',
                'expertise': 'investment analysis, reality disruption'
            },
            'mentor': {
                'name': 'Cognitive Science Mentor',
                'description': 'provide theoretical frameworks and insights',
                'color_theme': 'green', 
                'expertise': 'behavioral economics, cognitive science'
            },
            'assistant': {
                'name': 'Executive Assistant',
                'description': 'transform insights into actionable tools',
                'color_theme': 'cyan',
                'expertise': 'decision tools, practical implementation'
            }
        }
        
        # API configuration
        self.api_config = {
            'gemini': {
                'model': 'gemini-2.0-flash-exp',
                'temperature': 0.7,
                'max_tokens': 2048
            },
            'claude': {
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.7,
                'max_tokens': 2048
            }
        }
        
        # Initialize API clients
        self.gemini_client = None
        self.claude_client = None
        self._initialize_clients()
        
        # Cache mechanism
        self.response_cache = {}
        self.cache_enabled = True
    
    def _initialize_clients(self) -> None:
        """Initialize AI API clients"""
        try:
            # Initialize Gemini
            gemini_api_key = os.getenv('GEMINI_API_KEY') or st.secrets.get('GEMINI_API_KEY')
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                self.gemini_client = genai.GenerativeModel('gemini-2.0-flash-exp')
                st.success("🔧 DEBUG: Gemini client initialized successfully")
            else:
                st.warning("🔧 DEBUG: Gemini API key not found")
            
            # Initialize Claude
            claude_api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY')
            if claude_api_key:
                self.claude_client = Anthropic(api_key=claude_api_key)
                st.success("🔧 DEBUG: Claude client initialized successfully")
            else:
                st.warning("🔧 DEBUG: Claude API key not found")
                
        except Exception as e:
            st.error(f"🔧 DEBUG: API client initialization failed: {str(e)}")
    
    def load_role_prompt(self, role_name: str, case_name: str) -> str:
        """
        Load role-specific prompt templates
        
        Args:
            role_name: Role name (host/investor/mentor/assistant)
            case_name: Case name (madoff/ltcm/lehman)
        
        Returns:
            str: Role-specific prompt
        """
        
        # 🔧 调试信息：检查输入参数
        st.write("🔍 DEBUG: load_role_prompt调试信息")
        st.write(f"🎭 加载角色: '{role_name}', 案例: '{case_name}'")
        
        # Base role prompt templates
        base_prompts = {
            'host': f"""
You are the host of Cognitive Black Box, professional and authoritative. Your task is to guide users into {case_name} case analysis.

Core Responsibilities:
1. Create a professional decision analysis atmosphere
2. Collect user background information through structured questions
3. Build user immersion into the case
4. Set the stage for subsequent cognitive shock

Communication Style:
- Professional yet approachable, authoritative but accessible
- Use business decision-making terminology
- Maintain clear logical expression
- Show respect for user's decision-making experience

Current Stage: Act 1 - Decision Immersion
""",
            
            'investor': f"""
You are a seasoned Wall Street investor, using sharp questioning and harsh data to shatter user's cognitive assumptions.

Core Responsibilities:
1. Use shocking data to reveal the true consequences of {case_name} case
2. Expose cognitive blind spots in user's decisions through professional questioning
3. Create strong cognitive dissonance and reflection
4. Prepare emotional foundation for theoretical explanation stage

Communication Style:
- Direct and sharp, no mercy
- Use extensive specific numbers and comparisons
- Rhetorical questions and challenging expressions
- Create tension and pressure

Current Stage: Act 2 - Reality Disruption
""",
            
            'mentor': f"""
You are a mentor well-versed in behavioral economics and cognitive science, responsible for explaining the cognitive mechanisms behind {case_name} case from a theoretical perspective.

Core Responsibilities:
1. Provide authoritative theoretical explanations and scientific evidence
2. Build systematic cognitive frameworks
3. Transform shock into profound insights
4. Lay theoretical foundation for practical tool application

Communication Style:
- Profound and inspiring, theory connected to practice
- Quote authoritative research and classic theories
- Logical rigor with clear hierarchy
- Demonstrate wisdom and insight

Current Stage: Act 3 - Framework Reconstruction
""",
            
            'assistant': f"""
You are a professional executive assistant, responsible for transforming theory into actionable decision-making tools.

Core Responsibilities:
1. Design personalized decision safety systems
2. Provide specific application guidance
3. Strengthen user capability building
4. Ensure practical value transformation

Communication Style:
- Practical and professional, focus on actionability
- Clear structure with definite steps
- Encouraging but not exaggerating
- Demonstrate execution and support

Current Stage: Act 4 - Capability Armament
"""
        }
        
        # 🔧 调试信息：检查生成的prompt
        final_prompt = base_prompts.get(role_name, "")
        st.write(f"📝 角色是否存在于模板中: {role_name in base_prompts}")
        st.write(f"📝 生成的prompt长度: {len(final_prompt)}")
        
        if final_prompt:
            st.write(f"📝 Prompt开头100字符: {final_prompt[:100]}...")
        else:
            st.error(f"⚠️ ERROR: 角色'{role_name}'没有对应的prompt模板!")
            
        return final_prompt
    
    def generate_response(self, 
                         role_name: str, 
                         user_input: str, 
                         context: Dict[str, Any],
                         api_preference: str = 'gemini') -> Tuple[str, bool]:
        """
        Generate role response
        
        Args:
            role_name: Role name
            user_input: User input
            context: Current context
            api_preference: API preference ('gemini' or 'claude')
        
        Returns:
            Tuple[str, bool]: (response content, success flag)
        """
        try:
            # 🔧 调试信息：检查输入参数
            st.write("🔍 DEBUG: generate_response调试信息")
            st.write(f"🎭 角色: '{role_name}'")
            st.write(f"💬 用户输入长度: {len(user_input) if user_input else 0}")
            st.write(f"🔧 API偏好: {api_preference}")
            st.write(f"📋 上下文键: {list(context.keys()) if context else []}")
            
            if user_input:
                st.write(f"💬 用户输入前50字符: '{user_input[:50]}...'")
            else:
                st.warning("⚠️ 用户输入为空")
            
            # Build complete prompt
            role_prompt = self.load_role_prompt(role_name, context.get('case_name', 'madoff'))
            
            # Add context information
            context_prompt = self._build_context_prompt(context)
            
            # 🔧 调试信息：检查context prompt
            st.write(f"📋 Context prompt长度: {len(context_prompt)}")
            if context_prompt:
                st.write(f"📋 Context prompt内容: {context_prompt[:200]}...")
            
            # Build final prompt
            full_prompt = f"""
{role_prompt}

{context_prompt}

User Input: {user_input}

Please generate a response that fits the role characteristics based on role settings and current context. The response should:
1. Match the role's communication style and responsibilities
2. Advance the overall experience flow
3. Adjust content based on user's personalized information
4. Maintain professionalism and impact
"""
            
            # 🔧 调试信息：检查最终prompt
            st.write(f"📝 最终prompt长度: {len(full_prompt)}")
            if full_prompt.strip():
                st.write(f"📝 最终prompt前200字符: {full_prompt[:200]}...")
            else:
                st.error("⚠️ ERROR: 最终prompt为空!")
                return self._get_fallback_response(role_name), False
            
            # Check cache
            cache_key = self._generate_cache_key(role_name, user_input, context)
            if self.cache_enabled and cache_key in self.response_cache:
                st.info("🔧 DEBUG: 使用缓存响应")
                return self.response_cache[cache_key], True
            
            # Call API to generate response
            st.write(f"🔧 DEBUG: 准备调用API ({api_preference})")
            response = self._call_api(full_prompt, api_preference)
            
            if response:
                # Cache response
                if self.cache_enabled:
                    self.response_cache[cache_key] = response
                
                # Log API call
                self._log_api_call(role_name, api_preference, True)
                st.success("🔧 DEBUG: API调用成功")
                
                return response, True
            else:
                st.warning("🔧 DEBUG: API调用返回空响应，使用fallback")
                return self._get_fallback_response(role_name), False
                
        except Exception as e:
            st.error(f"🔧 DEBUG: generate_response异常: {str(e)}")
            self._log_api_call(role_name, api_preference, False, str(e))
            return self._get_fallback_response(role_name), False
    
    def switch_role(self, new_role: str, context: Dict[str, Any]) -> bool:
        """
        Role switching logic
        
        Args:
            new_role: New role name
            context: Current context
        
        Returns:
            bool: Whether switching was successful
        """
        try:
            if new_role not in self.roles:
                raise ValueError(f"Unknown role: {new_role}")
            
            # Update current role in context
            context['current_role'] = new_role
            
            # Generate role transition message
            transition_message = self._generate_transition_message(new_role, context)
            
            return True
            
        except Exception as e:
            st.error(f"Role switching failed: {str(e)}")
            return False
    
    def _build_context_prompt(self, context: Dict[str, Any]) -> str:
        """Build context prompt"""
        context_lines = []
        
        # Basic information
        context_lines.append(f"Case: {context.get('case_name', 'madoff')}")
        context_lines.append(f"Current Step: {context.get('current_step', 1)}/4")
        
        # Personalization information
        if context.get('personalization_active', False):
            user_inputs = context.get('user_inputs', {})
            if user_inputs:
                context_lines.append("User Personalization Info:")
                for key, value in user_inputs.items():
                    context_lines.append(f"- {key}: {value}")
        
        # Conversation history (recent 3 turns)
        conversation_history = context.get('conversation_history', [])
        if conversation_history:
            context_lines.append("Recent Conversation:")
            for turn in conversation_history[-3:]:
                context_lines.append(f"- {turn['role']}: {turn['message'][:100]}...")
        
        return "\n".join(context_lines)
    
    def _call_api(self, prompt: str, api_preference: str) -> Optional[str]:
        """Call AI API"""
        try:
            st.write(f"🔧 DEBUG: _call_api 开始，偏好: {api_preference}")
            st.write(f"🔧 DEBUG: Gemini client存在: {self.gemini_client is not None}")
            st.write(f"🔧 DEBUG: Claude client存在: {self.claude_client is not None}")
            
            if api_preference == 'gemini' and self.gemini_client:
                st.write("🔧 DEBUG: 调用Gemini API")
                return self._call_gemini(prompt)
            elif api_preference == 'claude' and self.claude_client:
                st.write("🔧 DEBUG: 调用Claude API")
                return self._call_claude(prompt)
            else:
                # Fallback to available API
                if self.gemini_client:
                    st.write("🔧 DEBUG: 回退到Gemini API")
                    return self._call_gemini(prompt)
                elif self.claude_client:
                    st.write("🔧 DEBUG: 回退到Claude API")
                    return self._call_claude(prompt)
                else:
                    st.error("🔧 DEBUG: 没有可用的API客户端")
                    raise Exception("No available API client")
                    
        except Exception as e:
            st.error(f"🔧 DEBUG: _call_api异常: {str(e)}")
            return None
    
    def _call_gemini(self, prompt: str) -> Optional[str]:
        """Call Gemini API"""
        try:
            # 🔧 调试信息：检查prompt内容
            st.write("🔍 DEBUG: Gemini API调用调试信息")
            st.write(f"📝 Prompt长度: {len(prompt) if prompt else 0}")
            st.write(f"📝 Prompt是否为空: {not prompt or prompt.strip() == ''}")
            
            if prompt:
                st.write(f"📝 Prompt前100字符: {prompt[:100]}...")
            else:
                st.error("⚠️ ERROR: Prompt完全为空!")
                return None
            
            if not prompt.strip():
                st.error("⚠️ ERROR: Prompt只包含空白字符!")
                return None
            
            st.write("🔧 DEBUG: 开始调用Gemini API...")
            
            response = self.gemini_client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.api_config['gemini']['temperature'],
                    max_output_tokens=self.api_config['gemini']['max_tokens']
                )
            )
            
            st.write(f"🔧 DEBUG: Gemini响应对象: {response is not None}")
            
            if response and response.text:
                st.write(f"🔧 DEBUG: Gemini响应长度: {len(response.text)}")
                st.write(f"🔧 DEBUG: Gemini响应前100字符: {response.text[:100]}...")
                return response.text.strip()
            else:
                st.warning("🔧 DEBUG: Gemini响应为空或无文本")
                return None
                
        except Exception as e:
            st.error(f"🔧 DEBUG: Gemini API call failed: {str(e)}")
            return None
    
    def _call_claude(self, prompt: str) -> Optional[str]:
        """Call Claude API"""
        try:
            # 🔧 调试信息：检查prompt内容
            st.write("🔍 DEBUG: Claude API调用调试信息")
            st.write(f"📝 Prompt长度: {len(prompt) if prompt else 0}")
            
            if not prompt or not prompt.strip():
                st.error("⚠️ ERROR: Claude API - Prompt为空!")
                return None
            
            st.write("🔧 DEBUG: 开始调用Claude API...")
            
            response = self.claude_client.messages.create(
                model=self.api_config['claude']['model'],
                messages=[{"role": "user", "content": prompt}],
                temperature=self.api_config['claude']['temperature'],
                max_tokens=self.api_config['claude']['max_tokens']
            )
            
            st.write(f"🔧 DEBUG: Claude响应对象: {response is not None}")
            
            if response and response.content:
                response_text = response.content[0].text.strip()
                st.write(f"🔧 DEBUG: Claude响应长度: {len(response_text)}")
                st.write(f"🔧 DEBUG: Claude响应前100字符: {response_text[:100]}...")
                return response_text
            else:
                st.warning("🔧 DEBUG: Claude响应为空")
                return None
                
        except Exception as e:
            st.error(f"🔧 DEBUG: Claude API call failed: {str(e)}")
            return None
    
    def _generate_cache_key(self, role_name: str, user_input: str, context: Dict[str, Any]) -> str:
        """Generate cache key"""
        key_components = [
            role_name,
            user_input[:50] if user_input else "",  # First 50 characters of user input
            context.get('current_step', 1),
            context.get('personalization_active', False)
        ]
        return "|".join(str(comp) for comp in key_components)
    
    def _get_fallback_response(self, role_name: str) -> str:
        """Get fallback response for roles"""
        fallback_responses = {
            'host': "Thank you for your participation. Let's continue analyzing this important case...",
            'investor': "Let's look at the real data behind this decision...",
            'mentor': "From a cognitive science perspective, let's analyze this phenomenon...",
            'assistant': "Let's transform these insights into practical tools..."
        }
        
        response = fallback_responses.get(role_name, "Let's continue our analysis...")
        st.info(f"🔧 DEBUG: 使用fallback响应 ({role_name}): {response[:50]}...")
        return response
    
    def _generate_transition_message(self, new_role: str, context: Dict[str, Any]) -> str:
        """Generate role transition message"""
        role_info = self.roles[new_role]
        return f"Now let me invite {role_info['name']} to {role_info['description']} for you..."
    
    def _log_api_call(self, role_name: str, api_used: str, success: bool, error_message: str = "") -> None:
        """Log API call information"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'role': role_name,
            'api': api_used,
            'success': success,
            'error': error_message
        }
        
        # This can be extended to a more complete logging system
        if not success:
            st.error(f"🔧 DEBUG: API call failed: {role_name} - {error_message}")
        else:
            st.success(f"🔧 DEBUG: API call successful: {role_name} - {api_used}")
    
    def get_role_info(self, role_name: str) -> Dict[str, str]:
        """Get role information"""
        return self.roles.get(role_name, {})
    
    def get_available_apis(self) -> List[str]:
        """Get list of available APIs"""
        available = []
        if self.gemini_client:
            available.append('gemini')
        if self.claude_client:
            available.append('claude')
        st.write(f"🔧 DEBUG: 可用APIs: {available}")
        return available
    
    def clear_cache(self) -> None:
        """Clear response cache"""
        self.response_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            'cache_size': len(self.response_cache),
            'cache_enabled': self.cache_enabled
        }

# Global instance
ai_engine = AIRoleEngine()
