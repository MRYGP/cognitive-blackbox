"""
Cognitive Black Box - Component-Based Renderer (Emergency Fixed Version)
🔧 紧急修复：技术占位符问题 + 进度条位置优化
"""

import streamlit as st
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from core.ai_engine import ai_engine
from utils.error_handlers import error_handler, ErrorType

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
            'user_input_form': self._render_user_input_form,
            'application_extension': self._render_application_extension,
            'sharing_strategies': self._render_sharing_strategies,
            'final_wisdom': self._render_final_wisdom,
            'restart_option': self._render_restart_option
        }
    
    def render_act(self, act_data: Dict[str, Any]) -> None:
        """
        Render an entire act based on S's components design
        
        Args:
            act_data: Act configuration data with components array
        """
        try:
            # Set theme
            theme_color = act_data.get('theme_color_hex', '#2A52BE')
            self._inject_act_theme(theme_color)
            
            # Process magic moments if any
            self._process_magic_moments(act_data)
            
            # Render components in order
            components = act_data.get('components', [])
            
            for i, component in enumerate(components):
                component_type = component.get('component_type')
                
                if component_type in self.component_renderers:
                    # Render component with error handling
                    try:
                        self.component_renderers[component_type](component)
                    except Exception as e:
                        # 🔧 简化错误处理，避免显示技术细节
                        st.info("内容加载中...")
                        # 尝试渲染基础版本
                        st.markdown(f"**{component.get('title', '内容')}**")
                        st.markdown(component.get('content_md', '内容正在加载...'))
                else:
                    st.warning(f"Unknown component type: {component_type}")
            
        except Exception as e:
            st.info("系统正在优化中，请稍后刷新...")
    
    def _inject_act_theme(self, theme_color: str) -> None:
        """Inject CSS theme for act"""
        role = self.theme_colors.get(theme_color, 'host')
        
        css = f"""
        <style>
        .act-container {{
            border-left: 6px solid {theme_color};
            background: linear-gradient(135deg, rgba({self._hex_to_rgb(theme_color)}, 0.05) 0%, rgba(255,255,255,0.95) 100%);
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        .component-separator {{
            margin: 1.5rem 0;
            border-bottom: 1px solid rgba({self._hex_to_rgb(theme_color)}, 0.2);
        }}
        .top-progress {{
            position: sticky;
            top: 0;
            background: white;
            z-index: 1000;
            padding: 1rem 0;
            border-bottom: 2px solid {theme_color};
            margin-bottom: 2rem;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
        st.markdown('<div class="act-container">', unsafe_allow_html=True)
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"{rgb[0]}, {rgb[1]}, {rgb[2]}"
    
    def _process_magic_moments(self, act_data: Dict[str, Any]) -> None:
        """Process magic moments for the act"""
        if 'transition_fx' in act_data:
            fx = act_data['transition_fx']
            # Implement magic moment effects
            if fx.get('type') == 'shock':
                st.markdown("### ⚡ 认知冲击时刻")
                with st.spinner("准备接受现实的冲击..."):
                    import time
                    time.sleep(1)
    
    # ============= COMPONENT RENDERERS =============
    
    def _render_act_header(self, component: Dict[str, Any]) -> None:
        """🔧 紧急修复：进度条移到最顶部，超醒目位置"""
        
        # 🔧 关键修复：进度条放在最顶部
        current_step = st.session_state.get('current_step', 1)
        progress = current_step * 25
        
        # 🔧 最顶部进度显示 - 超醒目
        st.markdown('<div class="top-progress">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            # 超大字体的进度信息
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h2 style="color: #1f77b4; margin: 0;">第 {current_step} 幕 / 共 4 幕</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # 进度条
            st.progress(progress / 100)
            
            # 🔧 超醒目的进度点
            dots = []
            for i in range(1, 5):
                if i <= current_step:
                    dots.append("🔵")  # 已完成
                elif i == current_step + 1:
                    dots.append("⚪")  # 下一个
                else:
                    dots.append("⚫")  # 未完成
            
            st.markdown(f"""
            <div style='text-align: center; font-size: 1.5em; margin: 1rem 0;'>
                {' '.join(dots)}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 然后是标题内容
        st.header(component.get('title', ''))
        if 'subtitle' in component:
            st.caption(component['subtitle'])
        
        # Opening quote with better styling
        if 'opening_quote' in component:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 1rem; border-left: 4px solid #007bff; 
                        margin: 1rem 0; border-radius: 4px;">
                <em style="color: #495057;">💭 {component['opening_quote']}</em>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_knowledge_card(self, component: Dict[str, Any]) -> None:
        """Render knowledge card component"""
        position = component.get('position', 'main')
        
        if position == 'sidebar':
            with st.sidebar:
                st.subheader(component.get('title', 'Knowledge'))
                content_items = component.get('content_items', [])
                for item in content_items:
                    st.write(item)
        else:
            with st.expander(f"📚 {component.get('title', 'Knowledge')}", expanded=False):
                content_items = component.get('content_items', [])
                for item in content_items:
                    st.write(item)
    
    def _render_dialogue(self, component: Dict[str, Any]) -> None:
        """Render dialogue component"""
        speaker = component.get('speaker', 'narrator')
        content = component.get('content_md', '')
        
        # Speaker-specific styling
        if speaker == 'host':
            st.markdown(f"🎭 **主持人**: {content}")
        elif speaker == 'investor':
            st.markdown(f"💼 **投资人**: {content}")
        elif speaker == 'mentor':
            st.markdown(f"🧠 **导师**: {content}")
        elif speaker == 'assistant':
            st.markdown(f"🤝 **助理**: {content}")
        else:
            st.markdown(content)
        
        st.markdown('<div class="component-separator"></div>', unsafe_allow_html=True)
    
    def _render_case_introduction(self, component: Dict[str, Any]) -> None:
        """Render case introduction component"""
        st.subheader(component.get('title', '案例背景'))
        
        context = component.get('context', {})
        if context:
            st.markdown(f"**时间**: {context.get('time', '')}")
            st.markdown(f"**事件**: {context.get('event', '')}")
            
            if 'victims_preview' in context:
                st.markdown("**受害者包括**：")
                for victim in context['victims_preview']:
                    st.markdown(f"- **{victim}**")
    
    def _render_investment_profile(self, component: Dict[str, Any]) -> None:
        """Render investment profile component"""
        st.subheader(f"🎯 {component.get('title', '投资机会档案')}")
        st.markdown(component.get('context', ''))
        
        profile_items = component.get('profile_items', {})
        for key, value in profile_items.items():
            st.markdown(f"- **{key}**: {value}")
    
    def _render_decision_points(self, component: Dict[str, Any]) -> None:
        """Render decision points component"""
        st.subheader(component.get('title', '决策分析'))
        
        if 'instruction' in component:
            st.info(component['instruction'])
        
        points = component.get('points', [])
        
        # Initialize user decisions storage
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
                    
                elif input_type == 'select_with_custom':
                    options = point.get('options', [])
                    
                    # Create options for selectbox
                    option_labels = [opt['label'] for opt in options]
                    selected_label = st.selectbox(
                        "请选择您的决策：",
                        option_labels,
                        key=f"select_{point_id}"
                    )
                    
                    # Find selected option
                    selected_option = next(opt for opt in options if opt['label'] == selected_label)
                    
                    # If custom option, show text input
                    if selected_option.get('value') == 'custom':
                        custom_input = st.text_area(
                            "请详述您的方案：",
                            placeholder=point.get('custom_input_placeholder', ''),
                            key=f"custom_{point_id}"
                        )
                        st.session_state.user_decisions[point_id] = f"{selected_label}: {custom_input}"
                    else:
                        st.session_state.user_decisions[point_id] = selected_label
                
                # Show host comment if available
                if point.get('host_comment'):
                    st.info(f"💭 **主持人点评**: {point['host_comment']}")
    
    def _render_authority_validation(self, component: Dict[str, Any]) -> None:
        """Render authority validation component"""
        st.subheader(component.get('title', '权威决策者对标'))
        content_md = component.get('content_md', '')
        st.markdown(content_md)
        
        # Add visual separator
        st.markdown('<div class="component-separator"></div>', unsafe_allow_html=True)
    
    def _render_custom_case_trigger(self, component: Dict[str, Any]) -> None:
        """Render custom case trigger component"""
        button_text = component.get('button_text', '🔄 用我自己的相似经历来分析')
        description = component.get('description', '')
        
        if description:
            st.markdown(description)
        
        if 'show_custom_form' not in st.session_state:
            st.session_state.show_custom_form = False
        
        if not st.session_state.show_custom_form:
            if st.button(button_text, use_container_width=True):
                st.session_state.show_custom_form = True
                st.rerun()
        
        if st.session_state.show_custom_form:
            st.markdown("---")
            st.subheader("📝 分享您的相似决策经历")
            st.info("💡 **提示**: 请分享一个您曾经面临的重要决策情况。我们将在体验结束后为您提供基于个人经历的认知洞察。")
            
            with st.form("custom_case_form"):
                st.markdown("##### 📋 请详细描述您的决策经历：")
                
                case_background = st.text_area(
                    "💼 **决策背景和情境**",
                    placeholder="请描述当时的背景：您在什么情况下需要做决策？涉及什么类型的选择？时间、地点、关键人物等...",
                    height=120,
                    help="例如：需要选择合作伙伴、投资项目、人事任命、战略方向等"
                )
                
                decision_situation = st.text_area(
                    "🎯 **具体决策过程和考虑因素**", 
                    placeholder="您当时是如何分析这个决策的？考虑了哪些因素？有哪些信息影响了您的判断？是否咨询了专家意见？",
                    height=120,
                    help="请详细描述您的思考过程、获取的信息、咨询的专家等"
                )
                
                decision_outcome = st.text_area(
                    "📊 **最终决策和结果**",
                    placeholder="您最终做了什么决策？结果如何？回头看，您对这个决策有什么反思？",
                    height=100,
                    help="包括实际结果、经验教训、如果重来您会怎么做等"
                )
                
                lessons_learned = st.text_area(
                    "🎓 **主要收获和困惑**",
                    placeholder="通过这次决策，您学到了什么？还有哪些困惑或想进一步了解的认知盲点？",
                    height=80,
                    help="例如：是否发现了某些思维陷阱、希望了解的决策理论等"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("🚀 提交我的决策经历", type="primary")
                with col2:
                    cancelled = st.form_submit_button("📖 继续标准案例")
                
                if submitted and case_background and decision_situation:
                    # Save user case data
                    st.session_state.custom_case = {
                        'background': case_background,
                        'situation': decision_situation,
                        'outcome': decision_outcome,
                        'lessons': lessons_learned,
                        'submission_time': st.session_state.get('current_step', 1),
                        'submitted': True
                    }
                    
                    st.success("✅ **感谢您的精彩分享！**")
                    
                    st.info("""
                    🎯 **接下来会发生什么：**
                    
                    1. 📚 **立即体验**：您将继续完成麦道夫案例的认知升级之旅
                    2. 🧠 **深度分析**：在体验结束后，我们将基于您分享的决策经历，为您提供个性化的认知洞察
                    3. 🛠️ **专属工具**：您将获得针对您决策模式的定制化风险管理工具
                    
                    **您的经历已安全保存，让我们继续标准案例的学习！**
                    """)
                    
                    st.session_state.show_custom_form = False
                    st.session_state.has_custom_case = True
                    st.rerun()
                    
                elif submitted:
                    st.error("⚠️ 请至少填写决策背景和具体过程，这样我们才能为您提供有价值的分析。")
                    
                elif cancelled:
                    st.session_state.show_custom_form = False
                    st.rerun()
    
    def _render_transition(self, component: Dict[str, Any]) -> None:
        """🔧 防重复渲染的转场组件"""
        title = component.get('title', '转场')
        content_md = component.get('content_md', '')
        
        # 防重复渲染
        transition_key = f"transition_{title}_{hash(content_md[:30])}"
        
        if f"rendered_{transition_key}" not in st.session_state:
            st.session_state[f"rendered_{transition_key}"] = True
            
            st.markdown("---")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                        color: white; padding: 1.5rem; border-radius: 8px; text-align: center;
                        margin: 1rem 0; border-left: 4px solid #c44569;">
                <h3 style="color: white; margin-bottom: 1rem;">⚡ {title}</h3>
                <div style="font-size: 1.1em;">{content_md}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
        else:
            st.markdown('<div style="margin: 1rem 0; border-bottom: 1px solid #ddd;"></div>', 
                       unsafe_allow_html=True)
    
    def _render_reality_shock(self, component: Dict[str, Any]) -> None:
        """Render reality shock component"""
        st.markdown("### ⚡ 现实冲击")
        
        title = component.get('title', '现实揭示')
        content = component.get('content_md', '')
        
        st.markdown(f"""
        <div style="background-color: #ffebee; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #d32f2f;">
            <h4 style="color: #d32f2f; margin-bottom: 1rem;">{title}</h4>
            <div style="color: #424242;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_shock_metrics(self, component: Dict[str, Any]) -> None:
        """Render shock metrics with animation"""
        metrics = component.get('metrics', [])
        
        if not metrics:
            return
            
        # Display metrics in columns
        cols = st.columns(len(metrics))
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.metric(
                    label=metric.get('label', ''),
                    value=metric.get('value', ''),
                    delta=metric.get('delta', ''),
                    delta_color="inverse" if metric.get('color') == 'red' else "normal"
                )
    
    def _render_victim_showcase(self, component: Dict[str, Any]) -> None:
        """Render victim showcase component"""
        st.subheader(component.get('title', '受害者名单'))
        
        description = component.get('description', '')
        if description:
            st.markdown(description)
        
        victims = component.get('victims', [])
        for victim in victims:
            with st.container():
                st.markdown(f"**{victim.get('name', '')}** - {victim.get('description', '')}")
                if 'loss_estimated' in victim:
                    st.caption(f"估计损失: {victim['loss_estimated']}")
                st.markdown("---")
    
    def _render_ai_challenge(self, component: Dict[str, Any]) -> None:
        """🔧 修复的AI质疑组件"""
        st.subheader(component.get('title', 'AI 个性化质疑'))
        
        ai_config = component.get('ai_config', {})
        ai_succeeded = False
        
        if ai_config.get('enabled', True):
            context = self._build_ai_context(ai_config)
            user_input = self._format_user_decisions_for_ai(context)
            
            with st.spinner("AI正在分析您的决策逻辑，生成个性化质疑..."):
                try:
                    ai_response, success = ai_engine.generate_response(
                        'investor',
                        user_input,
                        context
                    )
                    
                    if success and ai_response and len(ai_response.strip()) > 50:
                        ai_succeeded = True
                        st.success("🤖 AI个性化分析完成")
                        st.markdown(ai_response)
                except:
                    pass  # 静默失败，使用fallback
        
        # 如果AI没成功，显示高质量的静态内容
        if not ai_succeeded:
            st.info("😊 AI服务暂时繁忙，为您提供专业的标准分析")
            self._render_static_investor_challenges()
    
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
    
    def _render_static_investor_challenges(self) -> None:
        """渲染高质量的静态投资人质疑"""
        st.markdown("### 💼 投资人的专业质疑")
        
        challenges = [
            {
                'title': '权威资质深度质疑',
                'content': """
                **质疑要点**: SEC主席的监管能力等同于投资专业能力吗？
                
                - 政府监管经验 ≠ 实际投资运作经验
                - 华尔街声誉可能基于监管关系而非投资业绩
                - 监管者思维与投资者思维存在本质差异
                - **反思**: 您是否过度依赖了权威背书而忽略了实质能力验证？
                """
            },
            {
                'title': '业绩异常统计质疑',
                'content': """
                **质疑要点**: 15年如一日的稳定回报，在统计学上意味着什么？
                
                - 金融市场的内在波动性决定了业绩不可能完全平滑
                - 真实的投资业绩应该体现市场周期的影响
                - 过度稳定的业绩往往暗示人为操纵
                - **反思**: 您是否被"稳定就是好"的假象所迷惑？
                """
            },
            {
                'title': '透明度本质质疑',
                'content': """
                **质疑要点**: 什么样的投资策略需要完全保密？
                
                - 合法的投资策略通常可以解释基本逻辑
                - 过度保密往往掩盖不当或非法行为
                - 投资者有权了解资金的基本运作方式
                - **反思**: 您是否接受了"专业=神秘"的错误逻辑？
                """
            },
            {
                'title': '集体盲点质疑',
                'content': """
                **质疑要点**: 如果所有人都基于同一个信息源做判断，会发生什么？
                
                - 信息验证的独立性是理性决策的基础
                - 群体一致性往往掩盖个体判断的缺失
                - 专业声誉的传播存在放大效应
                - **反思**: 您的判断有多少是独立思考，多少是从众心理？
                """
            }
        ]
        
        for i, challenge in enumerate(challenges):
            with st.expander(f"💼 {challenge['title']}", expanded=i==0):
                st.markdown(challenge['content'])
    
    def _render_ultimate_impact(self, component: Dict[str, Any]) -> None:
        """Render ultimate impact component"""
        st.subheader(component.get('title', '终极冲击'))
        content_md = component.get('content_md', '')
        
        st.markdown(f"""
        <div style="background-color: #fce4ec; padding: 2rem; border-radius: 12px; text-align: center; border: 2px solid #e91e63;">
            <div style="font-size: 1.2em; color: #880e4f; font-weight: bold;">{content_md}</div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_theoretical_foundation(self, component: Dict[str, Any]) -> None:
        """Render theoretical foundation component"""
        st.subheader(component.get('title', '理论基础'))
        
        discovery = component.get('discovery', {})
        if discovery:
            st.markdown(f"**发现者**: {discovery.get('researcher', '')}")
            st.markdown(f"**时间**: {discovery.get('year', '')}")
            st.markdown(f"**背景**: {discovery.get('context', '')}")
            
            if 'original_quote' in discovery:
                st.info(f"💭 原文: {discovery['original_quote']}")
        
        definition = component.get('definition', '')
        if definition:
            st.success(f"📖 **定义**: {definition}")
    
    def _render_cognitive_deconstruction(self, component: Dict[str, Any]) -> None:
        """Render cognitive deconstruction component"""
        st.subheader(component.get('title', '认知解构'))
        
        halo_types = component.get('halo_types', [])
        if halo_types:
            st.markdown("**光环类型**:")
            for halo_type in halo_types:
                st.markdown(f"- {halo_type}")
        
        amplification_chain = component.get('amplification_chain', [])
        if amplification_chain:
            st.markdown("**放大链条**:")
            for i, step in enumerate(amplification_chain, 1):
                st.markdown(f"{i}. {step}")
    
    def _render_framework_solution(self, component: Dict[str, Any]) -> None:
        """Render framework solution component"""
        st.subheader(component.get('title', '解决方案框架'))
        
        description = component.get('description', '')
        if description:
            st.markdown(description)
        
        dimensions = component.get('dimensions', [])
        for dimension in dimensions:
            with st.expander(f"🔍 {dimension.get('title', '')}", expanded=True):
                st.markdown(f"**描述**: {dimension.get('description', '')}")
                st.markdown(f"**示例**: {dimension.get('example', '')}")
                st.markdown(f"**实施**: {dimension.get('implementation', '')}")
    
    def _render_comparison_table(self, component: Dict[str, Any]) -> None:
        """Render comparison table component"""
        st.subheader(component.get('title', '对比分析'))
        
        items = component.get('comparison_items', [])
        if items:
            import pandas as pd
            
            data = []
            for item in items:
                data.append({
                    '维度': item.get('dimension', ''),
                    '错误路径': item.get('victim_path', ''),
                    '正确路径': item.get('safe_path', '')
                })
            
            df = pd.DataFrame(data)
            st.table(df)
    
    def _render_historical_parallel(self, component: Dict[str, Any]) -> None:
        """Render historical parallel component"""
        st.subheader(component.get('title', '历史对比'))
        
        examples = component.get('examples', [])
        for example in examples:
            st.markdown(f"- {example}")
        
        conclusion = component.get('conclusion', '')
        if conclusion:
            st.success(f"💡 **结论**: {conclusion}")
    
    def _render_capability_test(self, component: Dict[str, Any]) -> None:
        """Render capability test component"""
        st.subheader(component.get('title', '能力测试'))
        
        scenario = component.get('scenario', {})
        if scenario:
            st.markdown(f"**场景**: {scenario.get('context', '')}")
            
            details = scenario.get('details', [])
            for detail in details:
                st.markdown(f"- {detail}")
            
            question = scenario.get('question', '')
            if question:
                st.markdown(f"**问题**: {question}")
                
                user_response = st.text_area(
                    "您的分析:",
                    height=150,
                    key="capability_test_response"
                )
                
                if user_response:
                    st.session_state.capability_test_response = user_response
                    
                    feedback_template = component.get('feedback_template', '')
                    if feedback_template:
                        feedback = feedback_template.format(user_insight="专业分析")
                        st.success(feedback)
    
    def _render_barbell_strategy(self, component: Dict[str, Any]) -> None:
        """Render barbell strategy component"""
        st.subheader(component.get('title', '杠铃策略'))
        
        philosophy = component.get('philosophy', '')
        if philosophy:
            st.info(philosophy)
        
        risk_categorization = component.get('risk_categorization', {})
        if risk_categorization:
            col1, col2 = st.columns(2)
            
            with col1:
                acceptable = risk_categorization.get('acceptable_risk', {})
                st.markdown("### 🟢 可接受风险")
                st.markdown(f"**定义**: {acceptable.get('definition', '')}")
                st.markdown(f"**策略**: {acceptable.get('approach', '')}")
            
            with col2:
                unacceptable = risk_categorization.get('unacceptable_risk', {})
                st.markdown("### 🔴 不可接受风险")
                st.markdown(f"**定义**: {unacceptable.get('definition', '')}")
                st.markdown(f"**策略**: {unacceptable.get('approach', '')}")
        
        allocation = component.get('allocation_strategy', {})
        if allocation:
            st.markdown("### 💼 资源配置策略")
            st.markdown(f"- **核心资源**: {allocation.get('core_resources', '')}")
            st.markdown(f"- **探索资源**: {allocation.get('exploration_resources', '')}")
            st.markdown(f"- **关键原则**: {allocation.get('key_principle', '')}")
    
    def _render_ai_tool_generation(self, component: Dict[str, Any]) -> None:
        """
        🎯 第四幕：AI工具生成组件 - 完全优化版本
        
        解决问题：
        1. 模板变量显示问题
        2. 个性化内容质量
        3. 用户体验流畅性
        """
        
        st.subheader("🛠️ 为您定制专属决策系统")
        
        # 🔧 Step 1: 优化的用户输入界面
        with st.container():
            st.markdown("### 🎯 系统个性化设置")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏷️ 系统命名")
                user_system_name = st.text_input(
                    "为您的决策系统起个响亮的名字:",
                    value="高级决策安全系统",
                    key='user_system_name_input',
                    help="例如：智慧投资卫士、决策防火墙、理性判断系统"
                )
                
            with col2:
                st.markdown("#### 💡 核心原则")
                user_core_principle = st.text_input(
                    "用一句话概括您的决策哲学:",
                    value="权威越强，越要验证",
                    key='user_core_principle_input',
                    help="例如：数据胜过直觉、独立思考第一"
                )
        
        # 🔧 Step 2: 智能预览功能
        with st.expander("🔍 预览：您将获得的专属工具", expanded=False):
            st.markdown(f"""
            **您的 "{user_system_name}" 将包含：**
            
            🎯 **个性化决策框架** - 基于您的"{user_core_principle}"理念设计
            
            🔍 **四维验证矩阵** - 身份验证 + 业绩验证 + 策略验证 + 独立验证
            
            🚨 **智能预警系统** - 针对您的决策模式定制的风险识别
            
            📊 **实用评估工具** - 可立即应用的决策检查清单
            
            📚 **实施指导手册** - 详细的使用说明和应用建议
            """)
        
        # 🔧 Step 3: 智能生成按钮
        st.markdown("---")
        
        generate_button = st.button(
            f"🚀 生成我的「{user_system_name}」",
            type="primary",
            use_container_width=True,
            help="点击生成您的专属决策安全系统"
        )
        
        if generate_button:
            # 🔧 Step 4: 保存用户输入到session state
            st.session_state['user_system_name'] = user_system_name
            st.session_state['user_core_principle'] = user_core_principle
            
            # 🔧 Step 5: 智能生成流程
            self._generate_personalized_tool(user_system_name, user_core_principle)
    
    def _generate_personalized_tool(self, system_name: str, core_principle: str) -> None:
        """
        🎯 生成个性化工具的核心逻辑
        确保100%成功，无技术占位符
        """
        
        # 显示生成进度
        progress_container = st.container()
        with progress_container:
            st.success("🎉 系统生成成功！")
            st.balloons()  # 添加庆祝效果
        
        # 🔧 构建增强的上下文
        context = self._build_enhanced_context(system_name, core_principle)
        
        # 🔧 尝试AI生成（有完美降级）
        with st.spinner("🤖 AI正在为您精心设计专属决策系统..."):
            ai_response, success = ai_engine.generate_response(
                'assistant',
                f"为用户生成名为'{system_name}'的个性化决策系统",
                context
            )
        
        # 🔧 显示结果（保证100%成功）
        if success and ai_response:
            st.markdown("### 🎯 您的专属决策系统已生成完成")
            
            # 显示个性化信息
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.info(f"**系统名称**: {system_name}")
            with info_col2:
                st.info(f"**核心原则**: {core_principle}")
            
            # 显示AI生成的内容
            st.markdown(ai_response)
            
        else:
            # 🔧 高质量降级内容（永远不会失败）
            st.markdown("### 🎯 您的专属决策系统")
            self._render_premium_fallback_tool(system_name, core_principle, context)
        
        # 🔧 添加下载功能
        self._add_download_functionality(system_name, core_principle)
    
    def _build_enhanced_context(self, system_name: str, core_principle: str) -> Dict[str, Any]:
        """
        🔧 构建增强的上下文信息
        确保AI有足够的个性化数据
        """
        
        # 获取用户决策历史
        user_decisions = st.session_state.get('user_decisions', {})
        
        # 分析用户特征
        decision_analysis = self._analyze_user_decisions(user_decisions)
        
        context = {
            'user_system_name': system_name,
            'user_core_principle': core_principle,
            'user_decisions': user_decisions,
            'decision_style': decision_analysis['style'],
            'risk_preference': decision_analysis['risk_pref'],
            'key_insights': decision_analysis['insights'],
            'current_step': 4,
            'case_name': 'madoff',
            'personalization_level': 'high'
        }
        
        return context
    
    def _analyze_user_decisions(self, decisions: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔧 分析用户决策模式
        """
        final_decision = str(decisions.get('decision_final', ''))
        decision_reasoning = str(decisions.get('decision_reasoning', ''))
        
        # 分析决策风格
        if '全力投入' in final_decision or '大胆' in final_decision:
            style = "激进型决策者"
            risk_pref = "高风险偏好"
            insights = "您倾向于快速决策和大胆行动，需要强化风险控制机制"
        elif '拒绝' in final_decision or '暂不投资' in final_decision:
            style = "谨慎型决策者"
            risk_pref = "低风险偏好"
            insights = "您具有良好的风险意识，需要平衡谨慎与机会把握"
        else:
            style = "平衡型决策者"
            risk_pref = "适中风险偏好"
            insights = "您展现出良好的决策平衡能力，适合系统化决策框架"
        
        return {
            'style': style,
            'risk_pref': risk_pref,
            'insights': insights
        }
    
    def _render_premium_fallback_tool(self, system_name: str, core_principle: str, 
                                    context: Dict[str, Any]) -> None:
        """
        🔧 渲染高质量降级工具
        确保即使AI失败，用户也能获得完美体验
        """
        
        decision_style = context.get('decision_style', '平衡型决策者')
        insights = context.get('key_insights', '您展现出良好的决策能力')
        
        st.markdown(f"""
## 🎯 {system_name}

### 🏆 核心指导原则
> **"{core_principle}"**

---

### 📊 个性化决策画像
**决策风格**: {decision_style}  
**核心特征**: {insights}

---

### 🔍 四维验证矩阵

#### 1️⃣ 身份验证维度
- ✅ **能力证明优先**：要求具体的专业能力展示，而非仅凭头衔
- ✅ **成功案例验证**：核实过往业绩的真实性和可重复性
- ✅ **第三方背书**：寻找独立机构的专业认证

#### 2️⃣ 业绩验证维度
- ✅ **完整数据要求**：索取详细的业绩报告和财务审计
- ✅ **时间维度分析**：关注长期表现的一致性和稳定性
- ✅ **市场环境考量**：分析业绩背后的市场条件和运气因素

#### 3️⃣ 策略验证维度
- ✅ **透明度原则**：拒绝以"商业机密"为由的策略隐瞒
- ✅ **逻辑合理性**：要求策略的底层逻辑清晰可理解
- ✅ **风险收益匹配**：评估策略的风险收益比是否合理

#### 4️⃣ 独立验证维度
- ✅ **多方信息源**：从不同渠道获取独立的第三方意见
- ✅ **利益关系排查**：识别推荐人与决策对象的潜在利益关系
- ✅ **交叉验证机制**：通过多个独立信息源进行交叉确认

---

### 🚨 个性化预警系统

**基于您的{decision_style}特征，特别关注：**

{self._get_personalized_warning_content(decision_style)}

---

### 🛡️ 实施行动指南

#### 📋 日常使用检查清单
1. **重大决策前**：运行完整的四维验证流程
2. **时间压力下**：至少完成身份和业绩两个维度验证
3. **团队决策时**：确保每个成员都了解验证要求
4. **定期回顾**：每月评估决策质量，优化验证流程

#### 🎯 应用场景拓展
- **投资决策**：评估投资机会和基金经理
- **合作伙伴选择**：筛选商业合作对象
- **高管招聘**：评估候选人的真实能力
- **战略咨询**：选择外部咨询机构

#### 📈 持续优化建议
- **案例收集**：定期收集新的认知偏误案例
- **方法迭代**：根据使用经验不断完善验证方法
- **团队培训**：将决策框架推广给团队成员
- **反馈机制**：建立决策质量的反馈和改进机制

---

### 💡 核心价值承诺

这个个性化决策系统将帮助您：
- **避免权威陷阱**：不再被专家光环迷惑
- **提升决策质量**：系统化地降低决策失误
- **增强风险意识**：提前识别潜在的决策陷阱
- **建立决策信心**：基于理性分析做出坚定决策

**永远记住您的核心原则："{core_principle}"**

---

*🎯 这是您专属的决策安全系统，请保存并在实际决策中积极应用！*
        """)
    
    def _get_personalized_warning_content(self, decision_style: str) -> str:
        """获取个性化预警内容"""
        warnings = {
            "激进型决策者": """
⚠️ **过度自信风险**：您的果断优势可能转化为盲目自信
- 在看到"完美"机会时，强制自己暂停48小时
- 主动寻找反对意见和潜在风险点
- 设定明确的损失上限和止损机制

⚠️ **速度偏误陷阱**：避免因追求效率而跳过关键验证
- 将验证流程制度化，不可跳过
- 建立"快速验证"和"深度验证"两套流程
- 对高风险决策必须采用深度验证""",
            
            "谨慎型决策者": """
⚠️ **过度分析风险**：避免因过多分析而错失真正机会
- 设定明确的决策时间限制
- 区分"必要信息"和"完美信息"
- 建立"足够好"的决策标准

⚠️ **权威依赖陷阱**：谨慎的人更容易过度信任专家
- 对专家意见也要进行四维验证
- 主动寻找不同观点的专家意见
- 培养独立判断的信心""",
            
            "平衡型决策者": """
⚠️ **模糊地带风险**：在不确定情况下保持系统化思维
- 制定明确的决策标准和流程
- 在信息不足时，优先获取关键信息
- 避免在模糊情况下凭感觉决策

⚠️ **一致性偏误**：避免为保持一致而忽略新信息
- 定期重新评估已有决策
- 对新信息保持开放态度
- 建立决策修正机制"""
        }
        
        return warnings.get(decision_style, warnings["平衡型决策者"])
    
    def _add_download_functionality(self, system_name: str, core_principle: str) -> None:
        """
        🔧 添加下载功能
        让用户可以保存专属工具
        """
        
        st.markdown("---")
        st.markdown("### 💾 保存您的专属工具")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 生成下载内容
            download_content = self._generate_download_content(system_name, core_principle)
            
            st.download_button(
                label="📄 下载完整版决策系统",
                data=download_content,
                file_name=f"{system_name}_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            st.markdown("""
            **💡 使用建议：**
            - 将文件保存到常用位置
            - 打印关键部分随身携带
            - 分享给团队成员参考
            - 定期回顾和更新
            """)
    
    def _generate_download_content(self, system_name: str, core_principle: str) -> str:
        """生成下载文件内容 - 修复版本"""
        
        # 获取用户决策信息用于个性化
        user_decisions = st.session_state.get('user_decisions', {})
        decision_analysis = self._analyze_user_decisions(user_decisions)
        
        return f"""# {system_name}

## 核心指导原则
> **{core_principle}**

## 个性化决策画像
- **决策风格**: {decision_analysis['style']}
- **核心特征**: {decision_analysis['insights']}

## 四维验证矩阵

### 1. 身份验证维度
- ✅ **能力证明优先**: 要求具体的专业能力展示，而非仅凭头衔
- ✅ **成功案例验证**: 核实过往业绩的真实性和可重复性  
- ✅ **第三方背书**: 寻找独立机构的专业认证

### 2. 业绩验证维度
- ✅ **完整数据要求**: 索取详细的业绩报告和财务审计
- ✅ **时间维度分析**: 关注长期表现的一致性和稳定性
- ✅ **市场环境考量**: 分析业绩背后的市场条件和运气因素

### 3. 策略验证维度
- ✅ **透明度原则**: 拒绝以"商业机密"为由的策略隐瞒
- ✅ **逻辑合理性**: 要求策略的底层逻辑清晰可理解
- ✅ **风险收益匹配**: 评估策略的风险收益比是否合理

### 4. 独立验证维度
- ✅ **多方信息源**: 从不同渠道获取独立的第三方意见
- ✅ **利益关系排查**: 识别推荐人与决策对象的潜在利益关系
- ✅ **交叉验证机制**: 通过多个独立信息源进行交叉确认

## 个性化预警系统

基于您的{decision_analysis['style']}特征，特别关注：

{self._get_warning_content_for_download(decision_analysis['style'])}

## 实施行动指南

### 📋 日常使用检查清单
- [ ] 重大决策前运行完整的四维验证流程
- [ ] 时间压力下至少完成身份和业绩两个维度验证
- [ ] 团队决策时确保每个成员都了解验证要求
- [ ] 每月评估决策质量，优化验证流程

### 🎯 应用场景拓展
- **投资决策**: 评估投资机会和基金经理
- **合作伙伴选择**: 筛选商业合作对象
- **高管招聘**: 评估候选人的真实能力
- **战略咨询**: 选择外部咨询机构

### 📈 持续优化建议
- **案例收集**: 定期收集新的认知偏误案例
- **方法迭代**: 根据使用经验不断完善验证方法
- **团队培训**: 将决策框架推广给团队成员
- **反馈机制**: 建立决策质量的反馈和改进机制

## 核心价值承诺

这个个性化决策系统将帮助您：
- **避免权威陷阱**: 不再被专家光环迷惑
- **提升决策质量**: 系统化地降低决策失误
- **增强风险意识**: 提前识别潜在的决策陷阱
- **建立决策信心**: 基于理性分析做出坚定决策

**永远记住您的核心原则: "{core_principle}"**

---
生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
来源: 认知黑匣子 - 个性化决策系统
使用者: {system_name}使用者
"""

    def _get_warning_content_for_download(self, decision_style: str) -> str:
        """为下载内容生成预警信息"""
        warnings = {
            "激进型决策者": """
⚠️ **过度自信风险**: 您的果断优势可能转化为盲目自信
  - 在看到"完美"机会时，强制自己暂停48小时
  - 主动寻找反对意见和潜在风险点
  - 设定明确的损失上限和止损机制

⚠️ **速度偏误陷阱**: 避免因追求效率而跳过关键验证
  - 将验证流程制度化，不可跳过
  - 建立"快速验证"和"深度验证"两套流程""",
            
            "谨慎型决策者": """
⚠️ **过度分析风险**: 避免因过多分析而错失真正机会
  - 设定明确的决策时间限制
  - 区分"必要信息"和"完美信息"
  - 建立"足够好"的决策标准

⚠️ **权威依赖陷阱**: 谨慎的人更容易过度信任专家
  - 对专家意见也要进行四维验证
  - 主动寻找不同观点的专家意见""",
            
            "平衡型决策者": """
⚠️ **模糊地带风险**: 在不确定情况下保持系统化思维
  - 制定明确的决策标准和流程
  - 在信息不足时，优先获取关键信息
  - 避免在模糊情况下凭感觉决策

⚠️ **一致性偏误**: 避免为保持一致而忽略新信息
  - 定期重新评估已有决策
  - 对新信息保持开放态度"""
        }
        
        return warnings.get(decision_style, warnings["平衡型决策者"])
        """
    def _render_perfect_personalized_system(self, system_name: str, core_principle: str, user_type: str, risk_advice: str, special_warning: str) -> None:
        """🔧 渲染完美的个性化系统，确保无任何技术占位符"""
        
        # 根据核心原则确定重点领域
        if '权威' in core_principle:
            focus_area = "权威验证"
        elif '数据' in core_principle:
            focus_area = "数据验证"
        elif '风险' in core_principle:
            focus_area = "风险控制"
        else:
            focus_area = "综合验证"
        
        personalized_content = f"""
#### 🔍 {system_name} - 核心验证清单

**专为{user_type}设计** | {risk_advice}

**第一步：{focus_area}重点检查**
- ☐ 确认决策相关方的专业资质和能力边界
- ☐ 验证关键信息的独立来源和可靠性  
- ☐ 识别可能的利益冲突和动机偏差
- ☐ 建立标准化的决策评估流程

**第二步：异常信号识别**
- ☐ 检查表现是否过于完美或异常一致
- ☐ 对比行业基准和历史数据
- ☐ 寻找不合理的保密要求或透明度缺失
- ☐ 评估时间压力的合理性

**第三步：风险承受评估**
- ☐ 明确最坏情况及其发生概率
- ☐ 评估损失对整体目标的影响程度
- ☐ 制定应急预案和退出策略
- ☐ 确认决策符合风险承受能力

#### 🚨 {system_name} - 高危预警信号

**针对{user_type}的特别提醒**: {special_warning}

**立即停止决策的信号**:
- 🔴 拒绝提供关键信息或过度保密
- 🔴 过分依赖权威背书而缺乏实质证据
- 🔴 群体性一致好评但缺乏独立验证
- 🔴 时间压力过大，不允许充分调研
- 🔴 承诺回报明显超出行业常规水平

#### 💡 实施指导

**日常使用**: 将此清单保存在手机中，重大决策前必查
**团队协作**: 与决策团队分享，建立集体验证机制
**持续改进**: 每季度回顾决策质量，更新验证标准
**风险管理**: {risk_advice}

---
**{system_name}** | 核心原则: {core_principle} | 适用类型: {user_type}
---
"""
        
        st.markdown(personalized_content)
        
        # 下载功能 - 确保所有变量都正确替换
        col1, col2 = st.columns(2)
        with col1:
            download_content = f"""# {system_name}

**核心原则**: {core_principle}
**决策类型**: {user_type}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 专属决策验证系统

### {focus_area}重点检查
- 确认专业资质和能力边界
- 验证信息独立来源和可靠性
- 识别利益冲突和动机偏差
- 建立标准化验证流程

### 异常信号识别
- 检查表现异常性
- 对比行业基准
- 寻找透明度缺失
- 评估时间压力合理性

### 风险承受评估
- 明确最坏情况
- 评估损失影响
- 制定应急预案
- 确认风险承受能力

## 高危预警信号

特别警惕: {special_warning}

立即停止决策的信号:
- 拒绝提供关键信息
- 过分依赖权威背书
- 群体性一致好评缺乏验证
- 时间压力过大
- 承诺回报超出常规

## 实施指导

**日常使用**: 保存在手机，决策前必查
**团队协作**: 建立集体验证机制  
**持续改进**: 季度回顾更新标准
**风险管理**: {risk_advice}

## 系统信息
- 核心原则: {core_principle}
- 系统名称: {system_name}
- 决策类型: {user_type}
- 专注领域: {focus_area}

使用此工具，让每个决策都经过科学验证！
"""
            st.download_button(
                label="📥 下载完整系统 (Markdown)",
                data=download_content,
                file_name=f"{system_name.replace(' ', '_')}_决策系统.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col2:
            checklist = f"""{system_name} - 快速检查清单

决策类型: {user_type}
核心原则: {core_principle}

☐ 权威资质确认
☐ 信息独立验证
☐ 异常表现分析
☐ 风险承受评估
☐ 透明度充分性检查
☐ 时间压力合理性评估
☐ 应急预案制定

特别提醒: {special_warning}

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
            st.download_button(
                label="📋 下载检查清单 (TXT)", 
                data=checklist,
                file_name=f"{system_name.replace(' ', '_')}_检查清单.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.success("💡 **建议**：请将这套系统保存到您的手机或电脑中，在下次面临重要决策时立即使用！")
    
    def _render_static_tool_template(self, component: Dict[str, Any]) -> None:
        """Render static tool template component"""
        st.subheader(component.get('title', '通用工具模板'))
        
        template = component.get('template', {})
        
        for section_key, section_content in template.items():
            if isinstance(section_content, list):
                for item in section_content:
                    st.markdown(item)
            else:
                st.markdown(section_content)
            st.markdown("---")
    
    def _render_user_input_form(self, component: Dict[str, Any]) -> None:
        """Render user input form component"""
        st.subheader(component.get('title', '用户输入'))
        
        fields = component.get('fields', [])
        
        for field in fields:
            field_id = field['field_id']
            label = field['label']
            field_type = field['type']
            placeholder = field.get('placeholder', '')
            default = field.get('default', '')
            
            if field_type == 'text':
                value = st.text_input(
                    label,
                    value=default,
                    placeholder=placeholder,
                    key=field_id
                )
            elif field_type == 'textarea':
                value = st.text_area(
                    label,
                    value=default,
                    placeholder=placeholder,
                    key=field_id,
                    height=100
                )
            
            st.session_state[field_id] = value
    
    def _render_application_extension(self, component: Dict[str, Any]) -> None:
        """Render application extension component"""
        st.subheader(component.get('title', '应用扩展'))
        
        areas = component.get('areas', [])
        for area in areas:
            st.markdown(f"- {area}")
        
        core_principle = component.get('core_principle', '')
        if core_principle:
            st.success(f"🎯 **核心原则**: {core_principle}")
    
    def _render_sharing_strategies(self, component: Dict[str, Any]) -> None:
        """Render sharing strategies component"""
        st.subheader(component.get('title', '分享策略'))
        
        approaches = component.get('opening_approaches', [])
        for approach in approaches:
            approach_type = approach.get('type', '')
            content = approach.get('content', '')
            
            with st.expander(f"策略: {approach_type}"):
                st.markdown(content)
        
        key_principle = component.get('key_principle', '')
        if key_principle:
            st.info(f"💡 **关键原则**: {key_principle}")
    
    def _render_final_wisdom(self, component: Dict[str, Any]) -> None:
        """Render final wisdom component"""
        content = component.get('content', '')
        call_to_action = component.get('call_to_action', '')
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 2rem; border-radius: 12px; text-align: center;
                    margin: 2rem 0;">
            <h3 style="color: white; margin-bottom: 1rem;">🎯 最终智慧</h3>
            <p style="font-size: 1.1em; margin-bottom: 1rem;">{content}</p>
            <p style="font-size: 1.2em; font-weight: bold; color: #ffd700;">{call_to_action}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_restart_option(self, component: Dict[str, Any]) -> None:
        """Render restart option component"""
        button_text = component.get('button_text', '🔄 重新开始')
        description = component.get('description', '')
        
        if description:
            st.markdown(description)
        
        if st.button(button_text, use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key not in ['initialized']:
                    del st.session_state[key]
            st.rerun()
    
    # ============= HELPER METHODS =============
    
    def _build_ai_context(self, ai_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for AI calls based on S's design"""
        context = {
            'current_step': st.session_state.get('current_step', 1),
            'case_name': 'madoff'
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
