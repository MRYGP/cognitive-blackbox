"""
Cognitive Black Box - Component-Based Renderer (Complete Fixed Version)
🔧 完整修复：AI调用问题 + 组件渲染优化

Architecture: 遵循C的三原则
- 前瞻性架构：统一AI调用接口
- 代码即文档：清晰的方法命名和注释
- 防御性编程：完善的错误处理和fallback
"""

import streamlit as st
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

class ComponentRenderer:
    """
    Component-based renderer implementing S's schema design
    Each component_type maps to a specific render function
    """
    
    def __init__(self):
        """Initialize component renderer"""
        self.theme_colors = {
            "#2A52BE": "host",      # Blue
            "#D93025": "investor",  # Red  
            "#059669": "mentor",    # Green
            "#0891B2": "assistant"  # Cyan
        }
        
        # Component renderer mapping - ALL METHODS IMPLEMENTED
        self.component_renderers = {
            'act_header': self._render_act_header,
            'knowledge_card': self._render_knowledge_card,
            'dialogue': self._render_dialogue,
            'case_introduction': self._render_case_introduction,
            'investment_profile': self._render_investment_profile,
            'decision_points': self._render_decision_points,
            'authority_validation': self._render_authority_validation,
            'custom_case_trigger': self._render_custom_case_trigger,
            'transition': self._render_transition,
            'reality_shock': self._render_reality_shock,
            'shock_metrics': self._render_shock_metrics,
            'victim_showcase': self._render_victim_showcase,
            'ai_challenge': self._render_ai_challenge,
            'static_challenge_set': self._render_static_challenge_set,
            'ultimate_impact': self._render_ultimate_impact,
            'theoretical_foundation': self._render_theoretical_foundation,
            'cognitive_deconstruction': self._render_cognitive_deconstruction,
            'framework_solution': self._render_framework_solution,
            'comparison_table': self._render_comparison_table,
            'historical_parallel': self._render_historical_parallel,
            'capability_test': self._render_capability_test,
            'barbell_strategy': self._render_barbell_strategy,
            'ai_tool_generation': self._render_ai_tool_generation,
            'static_tool_template': self._render_static_tool_template,
            'progress_indicator': self._render_progress_indicator,
            'custom_input': self._render_custom_input,
            'navigation': self._render_navigation,
            # 🔧 新增缺失的组件类型
            'user_input_form': self._render_user_input_form,
            'application_extension': self._render_application_extension,
            'sharing_strategies': self._render_sharing_strategies,
            'final_wisdom': self._render_final_wisdom,
            'restart_option': self._render_restart_option
        }

    # ============= MAIN RENDER METHODS =============
    
    def render_component(self, component: Dict[str, Any]) -> bool:
        """Main component rendering entry point"""
        try:
            component_type = component.get('component_type')
            
            if not component_type:
                st.error("组件类型未定义")
                return False
            
            if component_type not in self.component_renderers:
                st.warning(f"不支持的组件类型: {component_type}")
                return False
            
            # Render the component
            render_function = self.component_renderers[component_type]
            render_function(component)
            return True
            
        except Exception as e:
            st.error(f"组件渲染错误: {str(e)}")
            return False

    def render_act(self, act_data: Dict[str, Any]) -> bool:
        """Render complete act with all components"""
        try:
            components = act_data.get('components', [])
            
            for component in components:
                self.render_component(component)
                
            return True
            
        except Exception as e:
            st.error(f"幕次渲染错误: {str(e)}")
            return False

    # ============= 🔧 核心修复方法 =============
    
    def _render_dialogue(self, component: Dict[str, Any]) -> None:
        """Render dialogue component with proper AI integration"""
        
        # 🔧 修复：确保使用正确的AI引擎
        try:
            # 导入修复后的AI引擎
            from core.ai_engine import ai_engine
            
            # 获取角色和用户输入
            role = component.get('role', 'host')
            user_input = component.get('user_input', '')
            
            # 构建上下文
            context = {
                'case_name': st.session_state.get('selected_case', 'madoff'),
                'current_step': st.session_state.get('current_step', 1),
                'user_decisions': st.session_state.get('user_decisions', {}),
                'user_system_name': st.session_state.get('user_system_name', '高级决策安全系统'),
                'user_core_principle': st.session_state.get('user_core_principle', '权威越强，越要验证')
            }
            
            # 🔧 关键修复：使用修复后的AI引擎
            if role in ['investor', 'assistant'] and user_input:
                ai_response, success = ai_engine.generate_response(role, user_input, context)
                if success and ai_response:
                    st.markdown(ai_response)
                    return
            
            # Fallback: 显示组件的静态内容
            content_md = component.get('content_md', '')
            if content_md:
                st.markdown(content_md)
            else:
                st.info("😊 AI服务暂时繁忙，为您提供专业的标准分析")
                
        except Exception as e:
            # 错误处理：显示fallback内容
            content_md = component.get('content_md', '内容加载中...')
            st.markdown(content_md)

    def _render_ai_tool_generation(self, component: Dict[str, Any]) -> None:
        """
        🎯 修复AI工具生成组件
        """
        try:
            st.subheader(component.get('title', '定制你的专属决策系统'))
            
            # 获取用户输入数据
            user_system_name = st.session_state.get('user_system_name', '高级决策安全系统')
            user_core_principle = st.session_state.get('user_core_principle', '权威越强，越要验证')
            user_decisions = st.session_state.get('user_decisions', {})
            
            # 构建上下文
            context = {
                'user_system_name': user_system_name,
                'user_core_principle': user_core_principle,
                'user_decisions': user_decisions,
                'case_name': st.session_state.get('selected_case', 'madoff'),
                'current_step': st.session_state.get('current_step', 4)
            }
            
            # 🔧 关键修复：构建正确的用户输入
            user_input = f"为用户生成名为'{user_system_name}'的个性化决策系统"
            
            # 尝试调用AI引擎
            ai_succeeded = False
            try:
                # 🔧 确保正确导入AI引擎
                from core.ai_engine import ai_engine
                
                ai_response, success = ai_engine.generate_response('assistant', user_input, context)
                
                if success and ai_response:
                    ai_succeeded = True
                    st.success("🎉 系统生成成功！")
                    st.markdown(ai_response)
                    
            except Exception as e:
                st.error(f"🔧 调试信息: AI工具生成失败 - {str(e)}")
            
            if not ai_succeeded:
                # 使用高质量的fallback
                st.info("🔧 正在为您生成个性化系统...")
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

### 💡 核心原则
**{user_core_principle}** - 这将成为您决策安全的基石。
"""
                st.markdown(fallback_content)
                
        except Exception as e:
            st.error(f"⚠️ 系统生成遇到问题: {str(e)}")
            st.error("请稍后重试或联系技术支持")

    def _render_decision_points(self, component: Dict[str, Any]) -> None:
        """修复决策点组件"""
        st.subheader(component.get('title', '决策分析'))
        
        if 'instruction' in component:
            st.info(component['instruction'])
        
        points = component.get('points', [])
        
        # 如果没有决策点，显示默认内容
        if not points:
            st.markdown("""
            ### 💼 投资决策要点分析
            
            基于麦道夫案例，请思考以下关键问题：
            
            1. **权威背景验证**：如何验证投资管理人的真实能力？
            2. **业绩可信度**：如何判断投资业绩的真实性？
            3. **策略透明度**：什么程度的策略保密是合理的？
            4. **独立尽职调查**：如何进行真正独立的风险评估？
            """)
            return
        
        # 正常的决策点渲染逻辑
        if 'user_decisions' not in st.session_state:
            st.session_state.user_decisions = {}
        
        for i, point in enumerate(points):
            point_id = point.get('point_id', f'dp_{i}')
            question = point.get('question', '')
            
            with st.expander(f"决策点 {i+1}: {question}", expanded=i==0):
                input_type = point.get('input_type', 'textarea')
                placeholder = point.get('placeholder', '')
                
                if input_type == 'textarea':
                    user_input = st.text_area(
                        "您的专业判断：",
                        value=placeholder,
                        key=f"decision_{point_id}",
                        height=100
                    )
                    st.session_state.user_decisions[point_id] = user_input
                
                # 显示主持人点评
                if point.get('host_comment'):
                    st.info(f"💭 **主持人点评**: {point['host_comment']}")

    # ============= 🔧 通用AI调用方法 =============

    def _call_ai_for_component(self, role: str, user_input: str, component_data: Dict[str, Any]) -> str:
        """
        通用AI调用方法，确保所有组件都使用修复后的引擎
        """
        try:
            # 🔧 确保正确导入AI引擎
            from core.ai_engine import ai_engine
            
            # 构建上下文
            context = {
                'case_name': st.session_state.get('selected_case', 'madoff'),
                'current_step': st.session_state.get('current_step', 1),
                'user_decisions': st.session_state.get('user_decisions', {}),
                'user_system_name': st.session_state.get('user_system_name', '高级决策安全系统'),
                'user_core_principle': st.session_state.get('user_core_principle', '权威越强，越要验证')
            }
            
            # 调用AI引擎
            ai_response, success = ai_engine.generate_response(role, user_input, context)
            
            if success and ai_response:
                return ai_response
            else:
                # 返回组件的fallback内容
                return component_data.get('fallback_content', '内容正在加载...')
                
        except Exception as e:
            st.error(f"🔧 调试信息: AI调用异常 - {str(e)}")
            return component_data.get('fallback_content', '系统暂时繁忙，请稍后重试')

    # ============= 其他组件渲染方法 =============
    
    def _render_act_header(self, component: Dict[str, Any]) -> None:
        """Render act header component"""
        title = component.get('title', '')
        subtitle = component.get('subtitle', '')
        
        st.markdown(f"# {title}")
        if subtitle:
            st.markdown(f"*{subtitle}*")
        
        st.markdown("---")

    def _render_knowledge_card(self, component: Dict[str, Any]) -> None:
        """Render knowledge card component"""
        title = component.get('title', '')
        content = component.get('content_md', '')
        card_type = component.get('card_type', 'info')
        
        if card_type == 'warning':
            st.warning(f"**{title}**\n\n{content}")
        elif card_type == 'success':
            st.success(f"**{title}**\n\n{content}")
        elif card_type == 'error':
            st.error(f"**{title}**\n\n{content}")
        else:
            st.info(f"**{title}**\n\n{content}")

    def _render_case_introduction(self, component: Dict[str, Any]) -> None:
        """Render case introduction component"""
        title = component.get('title', '')
        content = component.get('content_md', '')
        
        st.subheader(title)
        st.markdown(content)

    def _render_investment_profile(self, component: Dict[str, Any]) -> None:
        """Render investment profile component"""
        title = component.get('title', '')
        profile_data = component.get('profile_data', {})
        
        st.subheader(title)
        
        if profile_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 基本信息")
                for key, value in profile_data.get('basic_info', {}).items():
                    st.markdown(f"**{key}**: {value}")
            
            with col2:
                st.markdown("### 投资策略")
                strategy = profile_data.get('strategy', '')
                st.markdown(strategy)

    def _render_authority_validation(self, component: Dict[str, Any]) -> None:
        """Render authority validation component"""
        title = component.get('title', '')
        validation_points = component.get('validation_points', [])
        
        st.subheader(title)
        
        for point in validation_points:
            st.markdown(f"- {point}")

    def _render_custom_case_trigger(self, component: Dict[str, Any]) -> None:
        """Render custom case trigger component"""
        title = component.get('title', '')
        description = component.get('description', '')
        button_text = component.get('button_text', '开始案例')
        
        st.subheader(title)
        if description:
            st.markdown(description)
        
        if st.button(button_text, use_container_width=True):
            # Trigger case start logic
            st.session_state.case_started = True
            st.rerun()

    def _render_transition(self, component: Dict[str, Any]) -> None:
        """Render transition component"""
        content = component.get('content_md', '')
        transition_type = component.get('transition_type', 'normal')
        
        if transition_type == 'dramatic':
            st.markdown("---")
            st.markdown(f"## {content}")
            st.markdown("---")
        else:
            st.markdown(content)

    def _render_reality_shock(self, component: Dict[str, Any]) -> None:
        """Render reality shock component"""
        title = component.get('title', '')
        shock_content = component.get('shock_content', '')
        
        st.error(f"**{title}**")
        st.markdown(shock_content)

    def _render_shock_metrics(self, component: Dict[str, Any]) -> None:
        """Render shock metrics component"""
        title = component.get('title', '')
        metrics = component.get('metrics', [])
        
        st.subheader(title)
        
        cols = st.columns(len(metrics))
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.metric(
                    label=metric.get('label', ''),
                    value=metric.get('value', ''),
                    delta=metric.get('delta', '')
                )

    def _render_victim_showcase(self, component: Dict[str, Any]) -> None:
        """Render victim showcase component"""
        title = component.get('title', '')
        victims = component.get('victims', [])
        
        st.subheader(title)
        
        for victim in victims:
            with st.expander(f"{victim.get('name', '')} - {victim.get('title', '')}"):
                st.markdown(victim.get('story', ''))

    def _render_ai_challenge(self, component: Dict[str, Any]) -> None:
        """
        🎯 最简化的AI质疑组件 - 确保逻辑清晰
        """
        st.subheader(component.get('title', 'AI 个性化质疑'))
        
        # 🔧 简化变量，只用布尔值控制
        ai_success = False
        ai_content = ""
        debug_messages = []
        
        # 🔧 步骤1: 尝试AI调用
        try:
            debug_messages.append("✅ 开始AI调用流程")
            
            # 导入AI引擎
            from core.ai_engine import ai_engine
            debug_messages.append("✅ AI引擎导入成功")
            
            # 构建简单的中文prompt
            user_decisions = st.session_state.get('user_decisions', {})
            simple_prompt = "请用中文对麦道夫投资案例进行四重专业质疑：1.职能边界混淆 2.信息不对称陷阱 3.统计异常忽视 4.独立尽调缺失。要求严厉专业，每个质疑至少100字。"
            
            debug_messages.append(f"✅ Prompt构建: {len(simple_prompt)} 字符")
            
            # 🔧 关键：直接调用，不使用复杂逻辑
            with st.spinner("🤖 AI正在生成质疑内容..."):
                if hasattr(ai_engine, '_call_gemini_api'):
                    ai_response = ai_engine._call_gemini_api(simple_prompt)
                else:
                    context = {'case_name': 'madoff', 'user_decisions': user_decisions}
                    ai_response, _ = ai_engine.generate_response('investor', simple_prompt, context)
                
                debug_messages.append(f"✅ AI调用完成")
                
                # 🔧 关键：立即检查并设置
                if ai_response and len(str(ai_response).strip()) > 50:
                    ai_content = str(ai_response).strip()
                    ai_success = True
                    debug_messages.append(f"✅ AI成功: {len(ai_content)} 字符")
                else:
                    debug_messages.append(f"❌ AI失败: 回复为空或过短")
        
        except Exception as e:
            debug_messages.append(f"❌ AI调用异常: {str(e)}")
        
        # 🔧 调试信息
        with st.expander("🔧 调试信息", expanded=False):
            for msg in debug_messages:
                st.text(msg)
            if ai_content:
                st.text(f"📄 AI内容预览: {ai_content[:100]}...")
        
        # 🔧 关键：最简单的显示逻辑
        if ai_success and ai_content:
            # 只显示AI内容
            st.success("🤖 AI个性化质疑分析完成")
            st.markdown(ai_content)
        else:
            # 只显示静态内容
            st.info("😊 AI服务暂时繁忙，为您提供专业的标准分析")
            self._render_static_investor_challenges()

    def _render_madoff_specific_challenges(self) -> None:
        """
        专门为麦道夫案例定制的四重质疑内容
        """
        st.markdown("""
        ### 💼 华尔街投资人的四重专业质疑
        
        #### 🔍 第一重：职能边界混淆质疑
        **"您确定自己有能力评估这种投资吗？"**
        
        您刚才说'前纳斯达克主席值得信任'。让我问您一个专业问题：**市场监管者 = 资产管理专家吗？**
        
        - 纳斯达克主席的核心职责：制定交易规则、监督市场秩序、确保信息披露
        - 这和选股、择时、风险控制有什么关系？
        - 这就像说'银监会主席一定是最好的银行家'，'证监会主席一定是最好的基金经理'
        
        **您为什么把监管能力，等同于投资能力？这是什么级别的逻辑错误？**
        
        ---
        
        #### 📊 第二重：信息不对称陷阱质疑
        **"您获得的信息足够做出判断吗？"**
        
        您接受了'投资策略商业机密'的说辞。作为管理资金的专业人士，这合理吗？
        
        真正的投资大师怎么做？
        - **巴菲特**：每年写股东信详细解释投资逻辑
        - **达利欧**：把《原则》写成书公开分享  
        - **西蒙斯**：虽然不透露具体算法，但量化策略的基本原理是公开的
        
        **什么样的'策略'需要完全黑盒操作？什么样的基金经理拒绝任何外部审计？**
        
        麦道夫连最基本的托管分离都拒绝！**这是策略保密还是欺诈隐瞒？**
        
        ---
        
        #### 🚨 第三重：统计异常忽视质疑
        **"您注意到那些'不可能'的数据了吗？"**
        
        **15年年均11-12%，波动极小。** 作为专业投资人，您不觉得这在统计学上是不可能的吗？
        
        - **巴菲特50年平均收益20%**，但1974年亏损48%，2008年亏损32%
        - 市场有周期，有黑天鹅，这是金融常识
        - **什么样的策略能完全规避系统性风险？**
        - **什么样的投资组合能15年如一日的稳定？**
        
        **答案只有一个：用新投资者的钱支付老投资者的收益！** 这就是庞氏骗局的数学特征。
        
        **您为什么忽视了这个最明显的红旗？**
        
        ---
        
        #### 🔍 第四重：独立尽调缺失质疑
        **"您进行过真正独立的尽职调查吗？"**
        
        您说'汇丰银行、瑞士银行都投资了，应该安全'。
        
        请问：
        - 汇丰的投委会亲自去麦道夫的办公室查看了交易记录吗？
        - 瑞士银行的风控团队验证过他声称的期权持仓吗？
        
        **答案是没有。** 他们都是通过feeder fund（导管基金）投资的，都是看了同一份业绩报告，都是被同一个'前纳斯达克主席'的光环忽悠。
        
        **如果所有人的判断都基于同一个虚假信息，那么人数越多，错误越大！**
        
        **这不是集体智慧，这是集体愚蠢！**
        
        ---
        
        ### 🎯 终极击穿
        
        有一个房地产大亨叫Norman Levy，93岁临终前还对家人说：
        
        > *"假如世界上只有一位诚实的人，那就是伯尼。"*
        
        **结果呢？他的投资全部化为乌有。**
        
        现在我问您：**连这些世界级的聪明人都被骗了，您凭什么认为自己不会犯同样的错误？**
        """)

    # 使用说明：
    # 1. 在 views/component_renderer.py 中找到 _render_ai_challenge 方法
    # 2. 完全替换为上面的代码  
    # 3. 在 ComponentRenderer 类的末尾添加 _render_madoff_specific_challenges 方法
    # 4. 保存文件并重启应用
    # 5. 测试麦道夫案例的第二幕"四重专业质疑"功能
    def _render_static_investor_challenges(self) -> None:
        """渲染高质量的静态投资人质疑内容"""
        st.markdown("""
        ### 💼 专业投资人的四重质疑
        
        #### 🔍 职能边界混淆质疑
        **"您确定自己有能力评估这种投资吗？"**
        
        - 麦道夫的策略涉及复杂的期权套利，需要专业的量化金融背景
        - 大多数投资者缺乏验证此类策略的技术能力
        - 您凭什么认为自己能看出问题所在？
        
        #### 📊 信息不对称陷阱质疑
        **"您获得的信息足够做出判断吗？"**
        
        - 麦道夫提供的业绩报告看似完美，但缺乏详细的交易记录
        - 作为外部投资者，您无法获得内部运营的真实数据
        - 您怎么确定看到的不是精心包装的假象？
        
        #### 🚨 统计异常忽视质疑
        **"您注意到那些'不可能'的数据了吗？"**
        
        - 连续多年无月度亏损，这在金融市场中几乎不可能
        - 收益率曲线过于平滑，缺乏正常的市场波动
        - 您为什么选择忽视这些明显的统计异常？
        
        #### 🔍 独立尽调缺失质疑
        **"您进行过真正独立的尽职调查吗？"**
        
        - 推荐人都是受益者，存在明显的利益冲突
        - 缺乏独立第三方的审计验证
        - 您有没有寻求过真正中立的专业意见？
        """)

    def _render_static_challenge_set(self, component: Dict[str, Any]) -> None:
        """Render static challenge set component"""
        title = component.get('title', '专业质疑')
        description = component.get('description', '')
        
        st.subheader(title)
        if description:
            st.info(description)
        
        challenges = component.get('challenges', [])
        for i, challenge in enumerate(challenges):
            challenge_title = challenge.get('title', '')
            challenge_content = challenge.get('content_md', '')
            
            with st.expander(f"💼 {challenge_title}", expanded=i==0):
                st.markdown(challenge_content)

    def _render_ultimate_impact(self, component: Dict[str, Any]) -> None:
        """Render ultimate impact component"""
        title = component.get('title', '')
        impact_data = component.get('impact_data', {})
        
        st.subheader(title)
        
        if impact_data:
            financial_impact = impact_data.get('financial_impact', '')
            human_impact = impact_data.get('human_impact', '')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💰 财务影响")
                st.markdown(financial_impact)
            
            with col2:
                st.markdown("### 👥 人员影响")
                st.markdown(human_impact)

    def _render_theoretical_foundation(self, component: Dict[str, Any]) -> None:
        """Render theoretical foundation component"""
        title = component.get('title', '')
        theories = component.get('theories', [])
        
        st.subheader(title)
        
        for theory in theories:
            st.markdown(f"### {theory.get('name', '')}")
            st.markdown(theory.get('description', ''))
            st.markdown(f"**应用**: {theory.get('application', '')}")

    def _render_cognitive_deconstruction(self, component: Dict[str, Any]) -> None:
        """Render cognitive deconstruction component"""
        title = component.get('title', '')
        biases = component.get('biases', [])
        
        st.subheader(title)
        
        for bias in biases:
            with st.expander(f"🧠 {bias.get('name', '')}"):
                st.markdown(f"**定义**: {bias.get('definition', '')}")
                st.markdown(f"**案例中的表现**: {bias.get('manifestation', '')}")
                st.markdown(f"**预防策略**: {bias.get('prevention', '')}")

    def _render_framework_solution(self, component: Dict[str, Any]) -> None:
        """Render framework solution component"""
        title = component.get('title', '')
        framework_steps = component.get('framework_steps', [])
        
        st.subheader(title)
        
        for i, step in enumerate(framework_steps, 1):
            st.markdown(f"### 步骤 {i}: {step.get('title', '')}")
            st.markdown(step.get('description', ''))
            st.markdown(f"**具体操作**: {step.get('action', '')}")

    def _render_comparison_table(self, component: Dict[str, Any]) -> None:
        """Render comparison table component"""
        title = component.get('title', '')
        comparison_data = component.get('comparison_data', [])
        
        st.subheader(title)
        
        if comparison_data:
            import pandas as pd
            df = pd.DataFrame(comparison_data)
            st.table(df)

    def _render_historical_parallel(self, component: Dict[str, Any]) -> None:
        """Render historical parallel component"""
        title = component.get('title', '')
        parallels = component.get('parallels', [])
        
        st.subheader(title)
        
        for parallel in parallels:
            st.markdown(f"### {parallel.get('name', '')}")
            st.markdown(parallel.get('description', ''))
            st.markdown(f"**相似点**: {parallel.get('similarity', '')}")

    def _render_capability_test(self, component: Dict[str, Any]) -> None:
        """Render capability test component"""
        title = component.get('title', '')
        test_scenario = component.get('test_scenario', {})
        
        st.subheader(title)
        
        if test_scenario:
            st.markdown(f"**场景**: {test_scenario.get('scenario', '')}")
            st.markdown(f"**问题**: {test_scenario.get('question', '')}")
            
            user_response = st.text_area(
                "您的分析:",
                height=150,
                key="capability_test_response"
            )
            
            if user_response:
                st.session_state.capability_test_response = user_response

    def _render_barbell_strategy(self, component: Dict[str, Any]) -> None:
        """Render barbell strategy component"""
        title = component.get('title', '')
        strategy_data = component.get('strategy_data', {})
        
        st.subheader(title)
        
        if strategy_data:
            safe_allocation = strategy_data.get('safe_allocation', '')
            risk_allocation = strategy_data.get('risk_allocation', '')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🛡️ 安全配置")
                st.markdown(safe_allocation)
            
            with col2:
                st.markdown("### 🚀 风险配置")
                st.markdown(risk_allocation)

    def _render_static_tool_template(self, component: Dict[str, Any]) -> None:
        """Render static tool template component"""
        title = component.get('title', '')
        template_content = component.get('template_content', '')
        
        st.subheader(title)
        st.markdown(template_content)

    def _render_progress_indicator(self, component: Dict[str, Any]) -> None:
        """Render progress indicator component"""
        current_step = st.session_state.get('current_step', 1)
        total_steps = component.get('total_steps', 4)
        
        progress = current_step / total_steps
        st.progress(progress)
        st.caption(f"进度: {current_step}/{total_steps}")

    def _render_custom_input(self, component: Dict[str, Any]) -> None:
        """Render custom input component"""
        input_type = component.get('input_type', 'text')
        label = component.get('label', '')
        key = component.get('key', 'custom_input')
        
        if input_type == 'text':
            user_input = st.text_input(label, key=key)
        elif input_type == 'textarea':
            user_input = st.text_area(label, key=key)
        elif input_type == 'selectbox':
            options = component.get('options', [])
            user_input = st.selectbox(label, options, key=key)
        
        if user_input:
            st.session_state[key] = user_input

    def _render_navigation(self, component: Dict[str, Any]) -> None:
        """Render navigation component"""
        nav_type = component.get('nav_type', 'next')
        button_text = component.get('button_text', '下一步')
        
        if st.button(button_text, use_container_width=True):
            if nav_type == 'next':
                current_step = st.session_state.get('current_step', 1)
                st.session_state.current_step = current_step + 1
            elif nav_type == 'back':
                current_step = st.session_state.get('current_step', 1)
                st.session_state.current_step = max(1, current_step - 1)
            
            st.rerun()

    # ============= 🔧 新增缺失的组件渲染方法 =============
    
    def _render_user_input_form(self, component: Dict[str, Any]) -> None:
        """Render user input form component"""
        title = component.get('title', '用户输入')
        fields = component.get('fields', [])
        
        st.subheader(title)
        
        form_data = {}
        for field in fields:
            field_id = field.get('field_id', '')
            label = field.get('label', '')
            field_type = field.get('type', 'text')
            placeholder = field.get('placeholder', '')
            default = field.get('default', '')
            required = field.get('required', False)
            
            if field_type == 'text':
                value = st.text_input(
                    label, 
                    value=default, 
                    placeholder=placeholder,
                    key=f"form_{field_id}"
                )
            elif field_type == 'textarea':
                value = st.text_area(
                    label, 
                    value=default, 
                    placeholder=placeholder,
                    key=f"form_{field_id}"
                )
            elif field_type == 'selectbox':
                options = field.get('options', [])
                value = st.selectbox(
                    label, 
                    options, 
                    key=f"form_{field_id}"
                )
            
            if value:
                form_data[field_id] = value
                st.session_state[field_id] = value
        
        submit_button_text = component.get('submit_button_text', '提交')
        if st.button(submit_button_text, use_container_width=True):
            # Trigger AI generation if enabled
            if component.get('ai_generation_trigger', False):
                st.session_state.trigger_ai_generation = True
                st.rerun()

    def _render_application_extension(self, component: Dict[str, Any]) -> None:
        """Render application extension component"""
        title = component.get('title', '应用扩展')
        description = component.get('description', '')
        extensions = component.get('extensions', [])
        
        st.subheader(title)
        if description:
            st.markdown(description)
        
        for extension in extensions:
            with st.expander(f"🎯 {extension.get('title', '')}", expanded=False):
                st.markdown(extension.get('description', ''))
                if extension.get('examples'):
                    st.markdown("**示例应用：**")
                    for example in extension['examples']:
                        st.markdown(f"- {example}")

    def _render_sharing_strategies(self, component: Dict[str, Any]) -> None:
        """Render sharing strategies component"""
        title = component.get('title', '分享策略')
        strategies = component.get('strategies', [])
        
        st.subheader(title)
        
        for strategy in strategies:
            with st.expander(f"📤 {strategy.get('title', '')}", expanded=False):
                st.markdown(strategy.get('description', ''))
                if strategy.get('steps'):
                    st.markdown("**实施步骤：**")
                    for i, step in enumerate(strategy['steps'], 1):
                        st.markdown(f"{i}. {step}")

    def _render_final_wisdom(self, component: Dict[str, Any]) -> None:
        """Render final wisdom component"""
        title = component.get('title', '最终智慧')
        wisdom_points = component.get('wisdom_points', [])
        call_to_action = component.get('call_to_action', '')
        
        st.subheader(title)
        
        for point in wisdom_points:
            st.success(f"💡 **{point}**")
        
        if call_to_action:
            st.info(call_to_action)

    def _render_restart_option(self, component: Dict[str, Any]) -> None:
        """Render restart option component"""
        title = component.get('title', '重新开始')
        description = component.get('description', '')
        button_text = component.get('button_text', '重新开始体验')
        
        st.subheader(title)
        if description:
            st.markdown(description)
        
        if st.button(button_text, use_container_width=True, type="primary"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key not in ['initialized']:
                    del st.session_state[key]
            st.rerun()

    # ============= 辅助方法 =============
    
    def _build_ai_context(self, ai_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for AI calls based on S's design"""
        context = {
            'current_step': st.session_state.get('current_step', 1),
            'case_name': st.session_state.get('selected_case', 'madoff')
        }
        
        input_context_keys = ai_config.get('input_context_keys', [])
        for key in input_context_keys:
            if key in st.session_state:
                context[key] = st.session_state[key]
            elif key == 'user_decisions':
                context[key] = st.session_state.get('user_decisions', {})
        
        return context
    
    def _format_user_decisions_for_ai(self, context: Dict[str, Any]) -> str:
        """Format user decisions for AI prompt"""
        user_decisions = context.get('user_decisions', {})
        
        if not user_decisions:
            return "用户尚未完成决策分析"
        
        formatted = "用户的具体决策分析：\n"
        
        final_decision = user_decisions.get('decision_final', '')
        if final_decision:
            formatted += f"\n**最终投资决策**: {final_decision}\n"
        
        for decision_id, decision_content in user_decisions.items():
            if decision_content and len(str(decision_content).strip()) > 0 and decision_id != 'decision_final':
                content = str(decision_content)[:150]
                if len(str(decision_content)) > 150:
                    content += "..."
                formatted += f"- {decision_id}: {content}\n"
        
        return formatted


# Global component renderer instance
component_renderer = ComponentRenderer()
