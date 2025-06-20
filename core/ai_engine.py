# core/ai_engine.py - Enhanced Version by C (架构师)
"""
Cognitive Black Box - 优化后的AI引擎
解决个性化工具生成中的模板变量问题和质量问题
"""

import streamlit as st
import asyncio
import os
import time
import json
import re
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
    st.warning("AI API libraries not installed. Running in fallback mode.")

class EnhancedAIEngine:
    """
    🔧 优化后的AI引擎 - 解决个性化质量问题
    
    主要改进：
    1. 智能变量替换系统
    2. 增强的个性化prompt工程
    3. 高质量降级机制
    4. 用户输入智能分析
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        self.roles = self._load_roles()
        self.response_cache = {}
        self.performance_metrics = {}
        
        # 初始化AI客户端
        self._initialize_ai_clients()
        
        # 🔧 新增：个性化分析器
        self.personalization_analyzer = PersonalizationAnalyzer()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载AI引擎配置"""
        return {
            'max_response_time': 8.0,  # 优化后的超时设置
            'cache_ttl': 3600,
            'max_retries': 2,
            'fallback_enabled': True,
            'api_config': {
                'gemini': {
                    'model': 'gemini-2.5-pro', 
                    'temperature': 0.7, 
                    'max_tokens': 2048
                }
            }
        }
    
    def _load_roles(self) -> Dict[str, Any]:
        """加载AI角色配置"""
        roles = {}
        try:
            from config import load_prompt_config
            
            role_ids = ['host', 'investor', 'mentor', 'assistant']
            for role_id in role_ids:
                role_config = load_prompt_config(role_id)
                if role_config:
                    roles[role_id] = AIRole(role_id, role_config)
                    
        except Exception as e:
            self.logger.error(f"Failed to load roles: {e}")
            
        return roles
    
    def _initialize_ai_clients(self):
        """初始化AI客户端"""
        self.gemini_client = None
        self.claude_client = None
        
        if APIS_AVAILABLE:
            try:
                # 初始化Gemini
                api_key = os.getenv('GEMINI_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    self.gemini_client = genai.GenerativeModel('gemini-2.5-pro')
                    
                # 初始化Claude
                claude_key = os.getenv('ANTHROPIC_API_KEY')
                if claude_key:
                    self.claude_client = Anthropic(api_key=claude_key)
                    
            except Exception as e:
                self.logger.error(f"Failed to initialize AI clients: {e}")
    
    def generate_response(self, role_id: str, user_input: str, context: Dict[str, Any]) -> Tuple[str, bool]:
        """
        🔧 增强的响应生成 - 核心优化方法
        
        改进：
        1. 智能个性化分析
        2. 高质量prompt构建
        3. 完美的降级机制
        """
        try:
            # 🔧 Step 1: 分析用户个性化数据
            personalization_data = self.personalization_analyzer.analyze_user_context(context)
            
            # 🔧 Step 2: 构建高质量prompt
            enhanced_prompt = self._build_enhanced_prompt(role_id, user_input, context, personalization_data)
            
            # 🔧 Step 3: 尝试AI生成
            if self.gemini_client and role_id == 'assistant':
                ai_response = self._call_gemini_api(enhanced_prompt)
                if ai_response and self._validate_response_quality(ai_response, context):
                    return ai_response, True
            
            # 🔧 Step 4: 高质量降级
            fallback_response = self._generate_enhanced_fallback(role_id, context, personalization_data)
            return fallback_response, True
            
        except Exception as e:
            self.logger.error(f"Error in generate_response: {e}")
            return self._generate_enhanced_fallback(role_id, context, {}), False
    
    def _build_enhanced_prompt(self, role_id: str, user_input: str, context: Dict[str, Any], 
                             personalization_data: Dict[str, Any]) -> str:
        """
        🔧 构建增强的个性化prompt
        """
        role = self.roles.get(role_id)
        if not role:
            return ""
            
        # 获取用户输入数据
        user_system_name = context.get('user_system_name', '高级决策安全系统')
        user_core_principle = context.get('user_core_principle', '权威越强，越要验证')
        user_decisions = context.get('user_decisions', {})
        
        # 构建个性化prompt
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
        else:
            prompt = role.system_prompt
            
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """调用Gemini API"""
        try:
            if not self.gemini_client:
                return None
                
            response = self.gemini_client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,
                    temperature=0.7,
                )
            )
            
            if response and response.text:
                return response.text.strip()
                
        except Exception as e:
            self.logger.error(f"Gemini API call failed: {e}")
            
        return None
    
    def _validate_response_quality(self, response: str, context: Dict[str, Any]) -> bool:
        """验证AI响应质量"""
        if not response or len(response) < 100:
            return False
            
        # 检查是否包含未替换的变量
        if '[user_system_name]' in response or '[user_core_principle]' in response:
            return False
            
        # 检查个性化程度
        user_system_name = context.get('user_system_name', '')
        if user_system_name and user_system_name not in response:
            return False
            
        return True
    
    def _generate_enhanced_fallback(self, role_id: str, context: Dict[str, Any], 
                                  personalization_data: Dict[str, Any]) -> str:
        """
        🔧 生成高质量的个性化降级内容
        """
        if role_id != 'assistant':
            role = self.roles.get(role_id)
            if role and role.fallback_responses:
                return role.fallback_responses.get('technical_issue', 
                    "系统正在为您准备个性化内容，请稍候...")
        
        # 🔧 为助理角色生成完美的个性化降级内容
        user_system_name = context.get('user_system_name', '高级决策安全系统')
        user_core_principle = context.get('user_core_principle', '权威越强，越要验证')
        
        # 分析用户决策类型
        user_decisions = context.get('user_decisions', {})
        decision_style = self._analyze_decision_style(user_decisions)
        
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
4. **持续学习**：收集新的认知偏误案例，完善系统

### 🎯 核心价值
这个系统将帮助您在面临类似麦道夫式的"完美"投资机会时，保持理性和警觉，避免被权威光环迷惑。

**记住：{user_core_principle}**
"""
        
        return fallback_content
    
    def _analyze_decision_style(self, user_decisions: Dict[str, Any]) -> str:
        """分析用户决策风格"""
        final_decision = str(user_decisions.get('decision_final', ''))
        
        if '全力投入' in final_decision or '大胆' in final_decision:
            return "激进型决策者"
        elif '拒绝' in final_decision or '暂不投资' in final_decision:
            return "谨慎型决策者"
        else:
            return "平衡型决策者"
    
    def _get_personalized_warnings(self, decision_style: str) -> str:
        """获取个性化预警内容"""
        warnings = {
            "激进型决策者": """
- ⚠️ **过度自信陷阱**：您的果断优势可能变成盲目自信
- ⚠️ **速度压力**：避免因追求效率而跳过验证步骤
- ⚠️ **机会成本焦虑**：不要因为害怕错过而降低标准
""",
            "谨慎型决策者": """
- ⚠️ **过度谨慎**：不要因为太多验证而错失真正的机会
- ⚠️ **分析瘫痪**：避免无休止的信息收集而不决策
- ⚠️ **权威依赖**：谨慎的人更容易过度信任专家意见
""",
            "平衡型决策者": """
- ⚠️ **模糊地带**：在模棱两可时，倾向于系统性验证
- ⚠️ **一致性偏误**：避免为了保持一致而忽略新信息
- ⚠️ **社会证明依赖**：不要因为"大家都在做"而降低标准
"""
        }
        
        return warnings.get(decision_style, warnings["平衡型决策者"])


class PersonalizationAnalyzer:
    """
    🔧 个性化分析器 - 分析用户特征和偏好
    """
    
    def analyze_user_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """分析用户上下文，提取个性化特征"""
        user_decisions = context.get('user_decisions', {})
        
        # 分析决策风格
        decision_style = self._analyze_decision_style(user_decisions)
        
        # 分析风险偏好
        risk_preference = self._analyze_risk_preference(user_decisions)
        
        # 提取关键决策
        key_decision = user_decisions.get('decision_final', '未知决策')
        
        return {
            'decision_style': decision_style,
            'risk_preference': risk_preference,
            'key_decision': key_decision,
            'personalization_level': 'high'
        }
    
    def _analyze_decision_style(self, decisions: Dict[str, Any]) -> str:
        """分析决策风格"""
        final_decision = str(decisions.get('decision_final', ''))
        
        if '全力投入' in final_decision:
            return "激进型"
        elif '拒绝' in final_decision or '暂不' in final_decision:
            return "谨慎型"
        else:
            return "平衡型"
    
    def _analyze_risk_preference(self, decisions: Dict[str, Any]) -> str:
        """分析风险偏好"""
        decision_reasons = str(decisions.get('decision_reasoning', ''))
        
        if '风险' in decision_reasons and '控制' in decision_reasons:
            return "风险控制"
        elif '机会' in decision_reasons and '收益' in decision_reasons:
            return "收益导向"
        else:
            return "适中平衡"


class AIRole:
    """AI角色定义"""
    def __init__(self, role_id: str, config: Dict[str, Any]):
        self.role_id = role_id
        self.name = config.get('name', '')
        self.system_prompt = config.get('system_prompt', '')
        self.fallback_responses = config.get('fallback_responses', {})


# 全局AI引擎实例
ai_engine = EnhancedAIEngine()
