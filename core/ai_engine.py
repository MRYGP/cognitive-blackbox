"""
Cognitive Black Box - Enhanced AI Engine (Debug Version)
Manages AI responses with intelligent fallback mechanisms
"""

import streamlit as st
import os
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

# Import AI libraries
try:
    import google.generativeai as genai
    from anthropic import Anthropic
    APIS_AVAILABLE = True
except ImportError:
    st.warning("AI API libraries not available. Running in fallback mode.")
    APIS_AVAILABLE = False

class PersonalizationAnalyzer:
    """Analyzes user context for personalization"""
    
    def analyze_user_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user context for personalization"""
        user_decisions = context.get('user_decisions', {})
        
        # Simple analysis based on user inputs
        decision_style = "balanced"
        if len(user_decisions) > 2:
            decision_style = "analytical"
        elif any("risk" in str(v).lower() for v in user_decisions.values()):
            decision_style = "risk-aware"
        
        return {
            'decision_style': decision_style,
            'risk_preference': 'moderate',
            'key_decision': list(user_decisions.keys())[0] if user_decisions else 'unknown'
        }

class AIRole:
    """Represents an AI role with its configuration"""
    
    def __init__(self, role_id: str, config: Dict[str, Any]):
        self.role_id = role_id
        self.system_prompt = config.get('system_prompt', '')
        self.fallback_responses = config.get('fallback_responses', {})

class EnhancedAIEngine:
    """
    🔧 Enhanced AI Engine with Debug Capabilities
    
    Main improvements:
    1. Intelligent variable replacement system
    2. Enhanced personalization prompt engineering
    3. High-quality fallback mechanism
    4. User input intelligent analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        self.roles = self._load_roles()
        self.response_cache = {}
        self.performance_metrics = {}
        
        # Initialize AI clients
        self._initialize_ai_clients()
        
        # 🔧 New: Personalization analyzer
        self.personalization_analyzer = PersonalizationAnalyzer()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load AI engine configuration"""
        return {
            'max_response_time': 8.0,  # Optimized timeout setting
            'cache_ttl': 3600,
            'max_retries': 2,
            'fallback_enabled': True,
            'api_config': {
                'gemini': {
                    'model': 'gemini-2.0-flash-exp', 
                    'temperature': 0.7, 
                    'max_tokens': 2048
                }
            }
        }
    
    def _load_roles(self) -> Dict[str, Any]:
        """Load AI role configurations"""
        roles = {}
        try:
            # Create basic role configurations
            role_configs = {
                'host': {
                    'system_prompt': 'You are a professional host...',
                    'fallback_responses': {'technical_issue': 'Thank you for your participation...'}
                },
                'investor': {
                    'system_prompt': 'You are a Wall Street investor...',
                    'fallback_responses': {'technical_issue': 'Let me look at the data...'}
                },
                'mentor': {
                    'system_prompt': 'You are a cognitive science mentor...',
                    'fallback_responses': {'technical_issue': 'From a cognitive perspective...'}
                },
                'assistant': {
                    'system_prompt': 'You are an executive assistant...',
                    'fallback_responses': {'technical_issue': 'Let me create tools for you...'}
                }
            }
            
            for role_id, config in role_configs.items():
                roles[role_id] = AIRole(role_id, config)
                    
        except Exception as e:
            self.logger.error(f"Failed to load roles: {e}")
            st.error(f"🔧 DEBUG: Failed to load roles: {e}")
            
        return roles
    
    def _initialize_ai_clients(self):
        """Initialize AI clients"""
        self.gemini_client = None
        self.claude_client = None
        
        st.write("🔧 DEBUG: Initializing AI clients...")
        
        if APIS_AVAILABLE:
            try:
                # Initialize Gemini
                api_key = os.getenv('GEMINI_API_KEY') or st.secrets.get('GEMINI_API_KEY')
                st.write(f"🔧 DEBUG: Gemini API key found: {bool(api_key)}")
                
                if api_key:
                    genai.configure(api_key=api_key)
                    self.gemini_client = genai.GenerativeModel('gemini-2.0-flash-exp')
                    st.success("🔧 DEBUG: Gemini client initialized successfully")
                else:
                    st.warning("🔧 DEBUG: No Gemini API key found")
                    
                # Initialize Claude
                claude_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY')
                st.write(f"🔧 DEBUG: Claude API key found: {bool(claude_key)}")
                
                if claude_key:
                    self.claude_client = Anthropic(api_key=claude_key)
                    st.success("🔧 DEBUG: Claude client initialized successfully")
                else:
                    st.warning("🔧 DEBUG: No Claude API key found")
                    
            except Exception as e:
                self.logger.error(f"Failed to initialize AI clients: {e}")
                st.error(f"🔧 DEBUG: Failed to initialize AI clients: {e}")
        else:
            st.warning("🔧 DEBUG: API libraries not available")
    
    def generate_response(self, role_id: str, user_input: str, context: Dict[str, Any]) -> Tuple[str, bool]:
        """
        🔧 Enhanced response generation - Core optimized method
        
        Improvements:
        1. Intelligent personalization analysis
        2. High-quality prompt construction
        3. Perfect fallback mechanism
        """
        try:
            # 🔧 DEBUG: Check input parameters
            st.write("🔍 DEBUG: generate_response input analysis")
            st.write(f"🎭 Role ID: '{role_id}'")
            st.write(f"💬 User input length: {len(user_input) if user_input else 0}")
            st.write(f"📋 Context keys: {list(context.keys()) if context else []}")
            
            if user_input:
                st.write(f"💬 User input preview: '{user_input[:100]}...'")
            else:
                st.warning("⚠️ User input is empty!")
            
            # 🔧 Step 1: Analyze user personalization data
            st.write("🔧 DEBUG: Step 1 - Analyzing personalization data...")
            personalization_data = self.personalization_analyzer.analyze_user_context(context)
            st.write(f"📊 Personalization data: {personalization_data}")
            
            # 🔧 Step 2: Build high-quality prompt
            st.write("🔧 DEBUG: Step 2 - Building enhanced prompt...")
            enhanced_prompt = self._build_enhanced_prompt(role_id, user_input, context, personalization_data)
            
            # 🔧 DEBUG: Check prompt quality
            st.write(f"📝 Enhanced prompt length: {len(enhanced_prompt)}")
            if enhanced_prompt:
                st.write(f"📝 Enhanced prompt preview: {enhanced_prompt[:200]}...")
            else:
                st.error("⚠️ ERROR: Enhanced prompt is empty!")
                return self._generate_enhanced_fallback(role_id, context, personalization_data), False
            
            # 🔧 Step 3: Try AI generation
            st.write("🔧 DEBUG: Step 3 - Attempting AI generation...")
            if self.gemini_client and role_id in ['assistant', 'investor']:
                st.write("🔧 DEBUG: Using Gemini client...")
                ai_response = self._call_gemini_api(enhanced_prompt)
                if ai_response and self._validate_response_quality(ai_response, context):
                    st.success("🔧 DEBUG: AI response validated successfully")
                    return ai_response, True
                else:
                    st.warning("🔧 DEBUG: AI response validation failed")
            else:
                st.write("🔧 DEBUG: Gemini client not available or role not supported")
            
            # 🔧 Step 4: High-quality fallback
            st.write("🔧 DEBUG: Step 4 - Using enhanced fallback...")
            fallback_response = self._generate_enhanced_fallback(role_id, context, personalization_data)
            st.info(f"🔧 DEBUG: Generated fallback response length: {len(fallback_response)}")
            return fallback_response, True
            
        except Exception as e:
            self.logger.error(f"Error in generate_response: {e}")
            st.error(f"🔧 DEBUG: Exception in generate_response: {e}")
            return self._generate_enhanced_fallback(role_id, context, {}), False
    
    def _build_enhanced_prompt(self, role_id: str, user_input: str, context: Dict[str, Any], 
                             personalization_data: Dict[str, Any]) -> str:
        """
        🔧 Build enhanced personalized prompt
        """
        st.write(f"🔧 DEBUG: Building prompt for role '{role_id}'")
        
        role = self.roles.get(role_id)
        if not role:
            st.error(f"⚠️ ERROR: Role '{role_id}' not found in roles")
            return ""
            
        # Get user input data
        user_system_name = context.get('user_system_name', '高级决策安全系统')
        user_core_principle = context.get('user_core_principle', '权威越强，越要验证')
        user_decisions = context.get('user_decisions', {})
        
        st.write(f"🔧 DEBUG: User system name: '{user_system_name}'")
        st.write(f"🔧 DEBUG: User core principle: '{user_core_principle}'")
        st.write(f"🔧 DEBUG: User decisions count: {len(user_decisions)}")
        
        # Build personalized prompt
        if role_id == 'assistant':
            prompt = f"""
你是专业的高级执行助理，为用户创建个性化的决策安全系统。

用户背景分析：
- 决策风格：{personalization_data.get('decision_style', '平衡型')}
- 风险偏好：{personalization_data.get('risk_preference', '适中')}
- 主要决策：{personalization_data.get('key_decision', '未知')}

用户输入：
- 系统名称：{user_system_name}
- 核心原则：{user_core_principle}

请创建一个完整的个性化决策安全系统，包括：
1. 系统概述（使用用户的系统名称）
2. 核心原则（基于用户输入）
3. 四维验证矩阵
4. 个性化预警系统
5. 实施指导

要求：
- 必须使用用户提供的系统名称和核心原则
- 内容要具体实用，不要使用占位符
- 基于用户的决策风格进行个性化
- 语言专业且易于理解
"""
        elif role_id == 'investor':
            case_name = context.get('case_name', 'madoff')
            prompt = f"""
你是华尔街资深投资人，专门用尖锐质疑和残酷数据击穿用户的认知假设。

案例背景：{case_name}案例
用户输入：{user_input}

基于用户的选择，进行四重专业质疑：
1. 职能边界混淆质疑
2. 信息不对称陷阱质疑  
3. 统计异常忽视质疑
4. 独立尽调缺失质疑

要求：
- 直接尖锐，不留情面
- 使用大量具体数字和对比
- 反问句和挑战性表达
- 营造紧张感和压力
"""
        else:
            prompt = role.system_prompt + f"\n\nUser Input: {user_input}\nContext: {context.get('case_name', 'madoff')}"
            
        st.write(f"🔧 DEBUG: Built prompt length: {len(prompt)}")
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """Call Gemini API with debug information"""
        try:
            # 🔧 DEBUG: Check prompt before API call
            st.write("🔍 DEBUG: Gemini API call analysis")
            st.write(f"📝 Prompt length: {len(prompt) if prompt else 0}")
            st.write(f"📝 Prompt is empty: {not prompt or prompt.strip() == ''}")
            st.write(f"🔧 Gemini client exists: {self.gemini_client is not None}")
            
            if not prompt or not prompt.strip():
                st.error("⚠️ ERROR: Cannot call Gemini API - prompt is empty!")
                return None
            
            if not self.gemini_client:
                st.error("⚠️ ERROR: Gemini client is not initialized!")
                return None
                
            st.write("🔧 DEBUG: Making Gemini API call...")
            
            response = self.gemini_client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,
                    temperature=0.7,
                )
            )
            
            st.write(f"🔧 DEBUG: Gemini response object exists: {response is not None}")
            
            if response and response.text:
                response_text = response.text.strip()
                st.write(f"🔧 DEBUG: Gemini response length: {len(response_text)}")
                st.write(f"🔧 DEBUG: Gemini response preview: {response_text[:150]}...")
                return response_text
            else:
                st.warning("🔧 DEBUG: Gemini response is empty or has no text")
                return None
                
        except Exception as e:
            self.logger.error(f"Gemini API call failed: {e}")
            st.error(f"🔧 DEBUG: Gemini API call exception: {e}")
            return None
    
    def _validate_response_quality(self, response: str, context: Dict[str, Any]) -> bool:
        """Validate AI response quality"""
        st.write("🔧 DEBUG: Validating response quality...")
        
        if not response or len(response) < 100:
            st.warning(f"🔧 DEBUG: Response too short: {len(response) if response else 0} chars")
            return False
            
        # Check for unreplaced variables
        if '[user_system_name]' in response or '[user_core_principle]' in response:
            st.warning("🔧 DEBUG: Response contains unreplaced variables")
            return False
            
        # Check personalization level
        user_system_name = context.get('user_system_name', '')
        if user_system_name and user_system_name not in response:
            st.warning(f"🔧 DEBUG: Response doesn't contain user system name: '{user_system_name}'")
            return False
        
        st.success("🔧 DEBUG: Response quality validation passed")
        return True
    
    def _generate_enhanced_fallback(self, role_id: str, context: Dict[str, Any], 
                                  personalization_data: Dict[str, Any]) -> str:
        """
        🔧 Generate high-quality personalized fallback content
        """
        st.write(f"🔧 DEBUG: Generating fallback for role '{role_id}'")
        
        if role_id != 'assistant':
            role = self.roles.get(role_id)
            if role and role.fallback_responses:
                fallback = role.fallback_responses.get('technical_issue', 
                    "系统正在为您准备个性化内容，请稍候...")
                st.info(f"🔧 DEBUG: Using basic fallback for {role_id}")
                return fallback
        
        # 🔧 Generate perfect personalized fallback content for assistant role
        user_system_name = context.get('user_system_name', '高级决策安全系统')
        user_core_principle = context.get('user_core_principle', '权威越强，越要验证')
        
        # Analyze user decision type
        user_decisions = context.get('user_decisions', {})
        decision_style = self._analyze_decision_style(user_decisions)
        
        st.write(f"🔧 DEBUG: User system name: '{user_system_name}'")
        st.write(f"🔧 DEBUG: Decision style: '{decision_style}'")
        
        fallback_content = f"""
## 🎯 {user_system_name}

### 核心指导原则
> **{user_core_principle}**

### 📋 四维验证清单

#### 1. 身份验证维度
- ✅ 要求具体的能力证明，而非仅凭头衔
- ✅ 验证过往成功案例的真实性
- ✅ 寻找第三方独立验证

#### 2. 业绩验证维度  
- ✅ 要求完整的业绩报告和审计证明
- ✅ 关注业绩的持续性和稳定性
- ✅ 分析业绩背后的市场环境因素

#### 3. 策略验证维度
- ✅ 拒绝"商业机密"为由的策略隐瞒
- ✅ 要求策略的逻辑合理性解释
- ✅ 评估策略的风险收益比

#### 4. 独立验证维度
- ✅ 寻找真正独立的第三方意见
- ✅ 避免利益相关者的"推荐"
- ✅ 进行多渠道信息交叉验证

### 🚨 个性化预警系统

**基于您的{decision_style}特征，特别注意：**

{self._get_personalized_warnings(decision_style)}

### 🛡️ 实施指导

1. **日常决策检查**：每个重要决策前运行四维验证
2. **团队共享**：将此系统分享给决策团队成员
3. **定期回顾**：每月回顾决策质量，优化系统
4. **持续改进**：根据实际使用效果调整验证标准

### 📊 成功指标

- 重要决策前进行验证的比例（目标：100%）
- 因提前发现风险而避免的损失
- 团队决策质量的整体提升

### 💡 核心原则
**{user_core_principle}** - 这将成为您决策安全的基石。
"""
        
        st.success(f"🔧 DEBUG: Generated enhanced fallback content ({len(fallback_content)} chars)")
        return fallback_content
    
    def _analyze_decision_style(self, user_decisions: Dict[str, Any]) -> str:
        """Analyze user decision style"""
        if not user_decisions:
            return "平衡型决策者"
        
        # Simple analysis based on decision content
        decision_text = " ".join(str(v) for v in user_decisions.values()).lower()
        
        if "数据" in decision_text or "分析" in decision_text:
            return "数据驱动型决策者"
        elif "直觉" in decision_text or "感觉" in decision_text:
            return "直觉驱动型决策者"
        elif "团队" in decision_text or "讨论" in decision_text:
            return "协作型决策者"
        else:
            return "平衡型决策者"
    
    def _get_personalized_warnings(self, decision_style: str) -> str:
        """Get personalized warnings based on decision style"""
        warnings = {
            "数据驱动型决策者": """
- 🚨 **数据完整性陷阱**：过度依赖历史数据，忽视突发变化
- 🚨 **分析瘫痪风险**：追求完美数据而错失时机
- 🚨 **量化偏见**：将不可量化的重要因素排除在外
""",
            "直觉驱动型决策者": """
- 🚨 **确认偏误风险**：只看到支持直觉的信息
- 🚨 **过度自信陷阱**：高估个人判断的准确性
- 🚨 **情绪决策风险**：在压力下做出冲动决定
""",
            "协作型决策者": """
- 🚨 **群体思维陷阱**：团队一致性掩盖个体理性
- 🚨 **责任分散效应**：集体决策导致个人责任感下降
- 🚨 **决策延迟风险**：过度协商错失最佳时机
""",
            "平衡型决策者": """
- 🚨 **决策摇摆风险**：在不同方法间摇摆不定
- 🚨 **表面平衡陷阱**：看似全面实则缺乏深度
- 🚨 **关键时刻犹豫**：在紧急情况下缺乏果断性
"""
        }
        
        return warnings.get(decision_style, warnings["平衡型决策者"])


# Global instance
ai_engine = EnhancedAIEngine()
