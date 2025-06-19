"""
Cognitive Black Box - Component-Based Renderer (Complete Fixed Version)
🔧 P0 Fixed: 第四幕AI工具生成优化
🔧 P1 Fixed: 第二幕AI成功后避免静态内容重复
🔧 P1 Fixed: 进度条位置优化
🔧 P0 Fixed: 内容重复渲染修复
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
                        error_handler.handle_error(
                            e, 
                            ErrorType.SYSTEM_ERROR,
                            context={
                                'component_type': component_type,
                                'component_index': i,
                                'act_id': act_data.get('act_id')
                            }
                        )
                        # Show fallback content
                        st.error(f"组件加载失败，正在使用备用内容...")
                else:
                    st.warning(f"Unknown component type: {component_type}")
            
        except Exception as e:
            error_handler.handle_error(
                e,
                ErrorType.SYSTEM_ERROR, 
                context={'act_data': str(act_data)[:200]}
            )
    
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
    
    # ============= COMPONENT RENDERERS - ALL METHODS IMPLEMENTED =============
    
    def _render_act_header(self, component: Dict[str, Any]) -> None:
        """🔧 P1 ENHANCED: Render act header component with optimized progress display"""
        # 🔧 P1 FIX: Move progress bar to top, more prominent position
        current_step = st.session_state.get('current_step', 1)
        progress = current_step * 25
        
        # Enhanced progress display
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"**第 {current_step} 幕 / 共 4 幕**")
            progress_bar = st.progress(progress / 100)
            
            # 🔧 ENHANCED: Add visual progress dots
            dots = []
            for i in range(1, 5):
                if i <= current_step:
                    dots.append("🔵")  # Completed
                elif i == current_step + 1:
                    dots.append("⚪")  # Next
                else:
                    dots.append("⚫")  # Future
            
            st.markdown(f"<div style='text-align: center; font-size: 1.2em; margin: 0.5rem 0;'>{''.join(dots)}</div>", 
                       unsafe_allow_html=True)
        
        # Main title
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
        """🔧 P2 COMPLETED: Functional custom case input with full experience closure"""
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
                    # 🔧 P2 NEW: Save comprehensive user case data
                    st.session_state.custom_case = {
                        'background': case_background,
                        'situation': decision_situation,
                        'outcome': decision_outcome,
                        'lessons': lessons_learned,
                        'submission_time': st.session_state.get('current_step', 1),
                        'submitted': True
                    }
                    
                    # 🔧 P2 NEW: Friendly confirmation with clear expectation management
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
                    st.session_state.personalization_active = True
                    
                    # 🔧 P2 NEW: Add custom case analysis to session for later use
                    if 'user_insights' not in st.session_state:
                        st.session_state.user_insights = []
                    
                    st.session_state.user_insights.append({
                        'type': 'custom_case_submission',
                        'data': st.session_state.custom_case,
                        'timestamp': case_background[:50] + "..." if len(case_background) > 50 else case_background
                    })
                    
                    st.rerun()
                    
                elif submitted:
                    st.error("⚠️ 请至少填写决策背景和具体过程，这样我们才能为您提供有价值的分析。")
                    
                elif cancelled:
                    st.session_state.show_custom_form = False
                    st.rerun()
    
    def _render_transition(self, component: Dict[str, Any]) -> None:
        """
        🔧 P0 FIXED: Render transition component with duplicate prevention
        """
        title = component.get('title', '转场')
        content_md = component.get('content_md', '')
        
        # 🔧 P0 FIX: Add unique key check to prevent duplicate rendering
        transition_key = f"transition_{title}_{hash(content_md[:50])}"
        
        if f"rendered_{transition_key}" not in st.session_state:
            st.session_state[f"rendered_{transition_key}"] = True
            
            # Add dramatic transition with unique styling
            with st.container():
                st.markdown("---")
                
                # 🔧 ENHANCED: More dramatic transition styling
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                            color: white; padding: 1.5rem; border-radius: 8px; text-align: center;
                            margin: 1rem 0; border-left: 4px solid #c44569;">
                    <h3 style="color: white; margin-bottom: 1rem;">⚡ {title}</h3>
                    <div style="font-size: 1.1em;">{content_md}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Process transition effects
                if 'transition_fx' in component:
                    fx = component['transition_fx']
                    with st.spinner("准备进入下一幕..."):
                        import time
                        time.sleep(min(fx.get('duration_ms', 2000) / 1000, 3.0))  # Cap at 3 seconds
                
                st.markdown("---")
        else:
            # 🔧 P0 FIX: If already rendered, just show a simple separator
            st.markdown('<div style="margin: 1rem 0; border-bottom: 1px solid #ddd;"></div>', 
                       unsafe_allow_html=True)
    
    def _render_reality_shock(self, component: Dict[str, Any]) -> None:
        """Render reality shock component"""
        st.markdown("### ⚡ 现实冲击")
        
        title = component.get('title', '现实揭示')
        content = component.get('content_md', '')
        
        # Dramatic reveal with color
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
        """
        🔧 P1 FIXED: Render AI challenge component with proper logic separation
        """
        st.subheader(component.get('title', 'AI 个性化质疑'))
        
        ai_config = component.get('ai_config', {})
        
        # 🔧 NEW: Add flag to track if AI succeeded
        ai_succeeded = False
        
        if ai_config.get('enabled', True):
            # Build context from user decisions
            context = self._build_ai_context(ai_config)
            
            # Generate AI response
            user_input = self._format_user_decisions_for_ai(context)
            
            with st.spinner("AI正在分析您的决策逻辑，生成个性化质疑..."):
                ai_response, success = ai_engine.generate_response(
                    'investor',
                    user_input,
                    context
                )
            
            if success and ai_response and len(ai_response.strip()) > 50:
                ai_succeeded = True  # 🔧 NEW: Mark AI as succeeded
                st.success("🤖 AI个性化分析完成")
                st.markdown(ai_response)
                
                # Track AI quality
                quality_score = self._evaluate_ai_response_quality(ai_response, 'investor')
                if quality_score < 6.0:
                    st.warning("AI响应质量偏低，已自动记录以优化服务")
                    
                # 🔧 P1 FIX: Add separator after successful AI content
                st.markdown('<div class="component-separator"></div>', unsafe_allow_html=True)
        
        # 🔧 FIXED: Only show fallback content if AI didn't succeed
        if not ai_succeeded:
            st.info("😊 AI服务暂时繁忙，为您提供专业的标准分析")
            # Use fallback content
            fallback_id = ai_config.get('fallback_response_id', 'investor_static_challenge_set')
            self._render_fallback_content(fallback_id)
        else:
            # 🔧 P1 NEW: Add a note about AI personalization success
            with st.expander("📊 个性化分析说明", expanded=False):
                st.markdown("""
                ✅ **AI已基于您的决策分析生成个性化质疑**
                
                这些质疑内容是根据您在第一幕中的具体选择和分析逻辑，量身定制的专业挑战。
                不同的决策选择会触发不同角度的专业质疑，帮助您更深入地认识决策中的潜在盲点。
                """)
    
    def _render_static_challenge_set(self, component: Dict[str, Any]) -> None:
        """🔧 P1 ENHANCED: Render static challenge set component with better styling"""
        title = component.get('title', '专业质疑')
        description = component.get('description', '')
        
        # 🔧 P1 FIX: Only show title if this is the primary content (not fallback)
        if not hasattr(st.session_state, 'ai_challenge_succeeded') or not st.session_state.ai_challenge_succeeded:
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
        st.subheader(component.get('title', '终极冲击'))
        content_md = component.get('content_md', '')
        
        # Dramatic styling
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
            # Create comparison table
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
                
                # Get user input
                user_response = st.text_area(
                    "您的分析:",
                    height=150,
                    key="capability_test_response"
                )
                
                if user_response:
                    st.session_state.capability_test_response = user_response
                    
                    # Provide feedback
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
        🔧 P0 CRITICAL FIX: AI tool generation with completely optimized prompt and calling
        """
        st.subheader(component.get('title', '定制您的专属决策系统'))
        
        # 🔧 ENHANCED: Better user input collection
        st.markdown("#### 为您的决策系统命名")
        user_system_name = st.text_input(
            "给您的决策系统起个名字：",
            value=st.session_state.get('user_system_name', '高级决策安全系统'),
            key='user_system_name_input'
        )
        st.session_state.user_system_name = user_system_name
        
        st.markdown("#### 确定您的核心原则")
        user_core_principle = st.text_input(
            "用一句话描述您的核心决策原则：",
            value=st.session_state.get('user_core_principle', '权威越强，越要验证'),
            key='user_core_principle_input'
        )
        st.session_state.user_core_principle = user_core_principle
        
        # 🔧 ENHANCED: Show what will be generated
        with st.expander("📋 预览：您将获得什么", expanded=False):
            st.markdown("""
            **您的专属决策系统将包含：**
            - 🎯 个性化的决策验证清单
            - 🔍 基于您经历设计的风险识别工具  
            - 🛡️ 针对您决策模式的预警系统
            - 📊 可立即使用的决策评估矩阵
            - 📚 实施指导和使用建议
            """)
        
        if st.button("🚀 生成我的专属决策系统", type="primary", use_container_width=True):
            # 🔧 P0 CRITICAL: Completely rewritten AI calling logic
            try:
                # Get user decisions
                user_decisions = st.session_state.get('user_decisions', {})
                
                # 🔧 CRITICAL FIX: Ultra-simplified prompt focused on success
                final_decision = user_decisions.get('decision_final', '谨慎投资')
                
                # Determine user type
                if '全力投入' in final_decision:
                    user_type = "激进型决策者"
                    risk_focus = "需要加强风险控制意识"
                elif '暂不投资' in final_decision or '放弃' in final_decision:
                    user_type = "谨慎型决策者"
                    risk_focus = "有良好的风险意识"
                else:
                    user_type = "平衡型决策者"
                    risk_focus = "有一定的风险控制意识"
                
                # 🔧 CRITICAL: Minimal, highly focused prompt
                ultra_simple_prompt = f"""为{user_type}设计专属决策系统。

系统名称：{user_system_name}
核心原则：{user_core_principle}
决策特点：{risk_focus}

请生成实用的决策工具，包含：
1. 验证清单（5项）
2. 预警信号（3项）
3. 使用建议

要求简洁实用，体现"{user_core_principle}"原则。"""

                # 🔧 CRITICAL: Minimal context to avoid issues
                minimal_context = {
                    'current_step': 4,
                    'case_name': 'madoff',
                    'user_type': user_type
                }
                
                with st.spinner("🤖 AI正在为您生成专属决策系统..."):
                    # 🔧 P0 FIX: Timeout handling and better error handling
                    import time
                    start_time = time.time()
                    
                    ai_tool_content, success = ai_engine.generate_response(
                        'assistant', 
                        ultra_simple_prompt, 
                        minimal_context
                    )
                    
                    response_time = time.time() - start_time
                    
                    # 🔧 DEBUG: Better debugging information
                    if not success:
                        st.error("🔧 **AI调用失败详情**")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.code(f"响应时间: {response_time:.2f}秒")
                            st.code(f"Prompt长度: {len(ultra_simple_prompt)}字符")
                        with col2:
                            st.code(f"用户类型: {user_type}")
                            st.code(f"上下文: {minimal_context}")
                
                # 🔧 ENHANCED: Better success criteria
                if success and ai_tool_content and len(ai_tool_content.strip()) > 100:
                    st.success("🎉 您的专属决策系统已生成完成！")
                    
                    # 🔧 NEW: Add system info display
                    st.info(f"**系统名称**: {user_system_name}  \n**核心原则**: {user_core_principle}  \n**决策类型**: {user_type}")
                    
                    # Show the generated content
                    st.markdown(ai_tool_content)
                    
                    # 🔧 ENHANCED: Better download options
                    col1, col2 = st.columns(2)
                    with col1:
                        download_content = f"# {user_system_name}\n\n核心原则: {user_core_principle}\n决策类型: {user_type}\n\n{ai_tool_content}"
                        st.download_button(
                            label="📥 下载完整系统 (Markdown)",
                            data=download_content,
                            file_name=f"{user_system_name.replace(' ', '_')}_决策系统.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    with col2:
                        # Create a simple checklist version
                        checklist_content = self._extract_checklist_from_content(ai_tool_content, user_system_name)
                        st.download_button(
                            label="📋 下载检查清单 (TXT)",
                            data=checklist_content,
                            file_name=f"{user_system_name.replace(' ', '_')}_检查清单.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    # 🔧 NEW: Usage encouragement
                    st.markdown("---")
                    st.success("💡 **建议**：请将这套系统保存到您的手机或电脑中，在下次面临重要决策时立即使用！")
                    
                else:
                    # 🔧 P0 CRITICAL: Enhanced fallback with perfect variable replacement
                    st.warning("⚠️ AI服务暂时繁忙，为您提供专业的个性化系统模板")
                    self._render_robust_fallback_tool(user_system_name, user_core_principle, user_type)
                    
            except Exception as e:
                # 🔧 P0 CRITICAL: Catch all exceptions and provide fallback
                st.error(f"🔧 **系统异常**: {str(e)[:100]}...")
                st.info("正在为您提供备用的专业系统模板")
                self._render_robust_fallback_tool(user_system_name, user_core_principle, "专业决策者")
    
    def _render_static_tool_template(self, component: Dict[str, Any]) -> None:
        """Render static tool template component"""
        st.subheader(component.get('title', '通用工具模板'))
        
        template = component.get('template', {})
        
        # Display template sections
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
            required = field.get('required', False)
            
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
            
            # Store in session state
            st.session_state[field_id] = value
            
            # Validate if required
            if required and not value:
                st.error(f"{label} 为必填项")
    
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
        
        # Dramatic final message
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
    
    # ============= HELPER METHODS FOR AI INTEGRATION =============
    
    def _build_ai_context(self, ai_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for AI calls based on S's design"""
        context = {
            'current_step': st.session_state.get('current_step', 1),
            'case_name': 'madoff'
        }
        
        # Add specified context keys
        input_context_keys = ai_config.get('input_context_keys', [])
        for key in input_context_keys:
            if key in st.session_state:
                context[key] = st.session_state[key]
            elif key == 'user_decisions':
                context[key] = st.session_state.get('user_decisions', {})
        
        return context
    
    def _format_user_decisions_for_ai(self, context: Dict[str, Any]) -> str:
        """🔧 P1 ENHANCED: Format user decisions for AI prompt with personalization"""
        user_decisions = context.get('user_decisions', {})
        
        if not user_decisions:
            return "用户尚未完成决策分析"
        
        formatted = "用户的具体决策分析：\n"
        
        # 🔧 P1 NEW: Special handling for final decision to enable dynamic opening
        final_decision = user_decisions.get('decision_final', '')
        if final_decision:
            formatted += f"\n**最终投资决策**: {final_decision}\n"
            
            # Add decision pattern analysis for AI personalization
            if '全力投入' in final_decision or 'full_investment' in final_decision:
                formatted += "**决策模式**: 激进型投资者，容易被权威背书影响，风险控制意识需要加强\n"
            elif '暂不投资' in final_decision or 'decline_investment' in final_decision:
                formatted += "**决策模式**: 谨慎型投资者，展现了良好的风险意识，但需要验证拒绝的真正原因\n"
            elif '试水' in final_decision or '观察' in final_decision:
                formatted += "**决策模式**: 平衡型投资者，有一定风险控制意识，但可能对认知偏误的深度理解不足\n"
        
        # Add other decision points
        decision_order = ['decision_authority', 'decision_performance', 'decision_transparency', 'decision_social_proof', 'decision_risk_assessment']
        
        for decision_id in decision_order:
            if decision_id in user_decisions and decision_id != 'decision_final':
                decision_content = user_decisions[decision_id]
                if decision_content and len(str(decision_content).strip()) > 0:
                    content = str(decision_content)[:200]
                    if len(str(decision_content)) > 200:
                        content += "..."
                    formatted += f"- {decision_id}: {content}\n"
        
        # 🔧 P1 NEW: Add personalization instruction for AI
        formatted += "\n**AI指令**: 请根据用户的最终决策模式，定制开场白。如果用户选择了激进投资，要严厉质疑其风险控制；如果选择了拒绝投资，要验证其判断的真正原因。"
        
        return formatted
    
    def _evaluate_ai_response_quality(self, response: str, role: str) -> float:
        """Evaluate AI response quality (1-10 scale)"""
        # Simple quality evaluation
        if len(response) < 100:
            return 3.0
        
        # Role-specific keyword checks
        role_keywords = {
            'investor': ['投资', '风险', '数据', '分析', '质疑'],
            'assistant': ['工具', '系统', '实用', '指导', '专属', '决策', '检查']
        }
        
        keywords = role_keywords.get(role, [])
        keyword_count = sum(1 for keyword in keywords if keyword in response)
        
        quality_score = min(10.0, 5.0 + keyword_count * 1.0)
        return quality_score
    
    def _render_fallback_content(self, fallback_id: str) -> None:
        """Render fallback content when AI fails"""
        if fallback_id == 'investor_static_challenge_set':
            # Render static investor challenges
            st.markdown("### 投资人的专业质疑")
            st.markdown("""
            **权威资质质疑**：SEC主席的监管能力等同于投资专业能力吗？
            
            **业绩异常质疑**：15年如一日的稳定回报，在统计学上意味着什么？
            
            **透明度质疑**：什么样的投资策略需要完全保密？
            
            **集体盲点质疑**：如果所有人都基于同一个信息源做判断，会发生什么？
            """)
            
        elif fallback_id == 'assistant_static_tool_template':
            # Render static tool template
            st.markdown("### 通用决策安全系统")
            st.markdown("""
            **基础验证清单**：
            - 权威资质确认
            - 数据独立核实
            - 异常表现分析
            - 风险承受评估
            
            这是经过验证的决策工具模板，您可以直接使用并根据具体情况调整。
            """)
    
    def _build_simple_decision_summary(self, user_decisions: Dict[str, Any]) -> str:
        """🔧 P0 CRITICAL: Build simple decision summary for AI prompt"""
        if not user_decisions:
            return "谨慎的决策者，重视风险控制"
        
        # Get final decision to determine user type
        final_decision = user_decisions.get('decision_final', '')
        
        if '全力投入' in str(final_decision):
            return "激进型决策者，容易被权威影响"
        elif '暂不投资' in str(final_decision) or '拒绝' in str(final_decision):
            return "谨慎型决策者，有良好风险意识"
        else:
            return "平衡型决策者，有一定风险控制意识"
    
    def _render_robust_fallback_tool(self, system_name: str, core_principle: str, user_type: str = "专业决策者") -> None:
        """🔧 P0 CRITICAL: Robust fallback tool with perfect variable replacement"""
        st.markdown(f"### 🛡️ {system_name}")
        st.markdown(f"**核心原则**: {core_principle}")
        st.markdown(f"**决策类型**: {user_type}")
        
        # 🔧 CRITICAL: Generate personalized fallback based on principle and user type
        if '权威' in core_principle:
            focus_area = "权威验证"
            special_warning = "权威背书可能掩盖真实风险"
        elif '数据' in core_principle:
            focus_area = "数据验证"
            special_warning = "数据可能被操纵或选择性披露"
        elif '风险' in core_principle:
            focus_area = "风险控制"
            special_warning = "过度自信可能低估尾部风险"
        else:
            focus_area = "综合验证"
            special_warning = "认知偏误可能影响判断质量"
        
        # 🔧 ENHANCED: Add user type specific recommendations
        if "激进型" in user_type:
            risk_advice = "建议加强风险控制流程，避免过度自信"
            specific_check = "☐ 设置强制性的反对意见收集环节"
        elif "谨慎型" in user_type:
            risk_advice = "保持现有的谨慎态度，增强机会识别能力"
            specific_check = "☐ 平衡风险控制与机会把握"
        else:
            risk_advice = "保持平衡的决策风格，系统化验证流程"
            specific_check = "☐ 建立标准化的决策评估流程"
        
        # 🔧 PERSONALIZED: Generate completely personalized content
        personalized_content = f"""
#### 🔍 {system_name} - 核心验证清单

**专为{user_type}设计** | {risk_advice}

**第一步：{focus_area}重点检查**
- ☐ 确认决策相关方的专业资质和能力边界
- ☐ 验证关键信息的独立来源和可靠性  
- ☐ 识别可能的利益冲突和动机偏差
- {specific_check}

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
        
        # 🔧 ENHANCED: Provide perfect download with all variables replaced
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
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 下载完整系统 (Markdown)",
                data=download_content,
                file_name=f"{system_name.replace(' ', '_')}_决策系统.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col2:
            # Simple checklist version
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
    
    def _summarize_user_decisions(self, user_decisions: Dict[str, Any]) -> str:
        """🔧 P0 NEW: Summarize user decisions for AI prompt"""
        if not user_decisions:
            return "用户尚未完成决策分析，请提供通用的专业建议。"
        
        summary = "用户决策特点：\n"
        for decision_id, decision_content in user_decisions.items():
            if decision_content and len(str(decision_content).strip()) > 0:
                # Truncate long decisions
                content = str(decision_content)[:150]
                if len(str(decision_content)) > 150:
                    content += "..."
                summary += f"- {decision_id}: {content}\n"
        
        return summary
    
    def _infer_user_background(self) -> str:
        """🔧 P0 NEW: Infer user background from session data"""
        # Simple inference based on available data
        decisions = st.session_state.get('user_decisions', {})
        if decisions:
            # Look for professional terms in user responses
            all_text = " ".join(str(v) for v in decisions.values()).lower()
            if any(term in all_text for term in ['投资', '股票', '基金', '金融']):
                return '金融行业专业人士'
            elif any(term in all_text for term in ['技术', '产品', '开发', '创新']):
                return '科技行业管理者'
            elif any(term in all_text for term in ['咨询', '战略', '分析']):
                return '咨询行业专家'
        
        return '高级管理决策者'
    
    def _extract_session_insights(self) -> List[str]:
        """🔧 P0 NEW: Extract key insights from the session"""
        insights = []
        
        # Check what user learned
        if st.session_state.get('completed_acts', []):
            insights.append("已完成完整的认知升级体验")
        
        # Check decision patterns
        decisions = st.session_state.get('user_decisions', {})
        if decisions:
            insights.append("对权威和业绩验证有深度思考")
        
        return insights
    
    def _extract_checklist_from_content(self, content: str, system_name: str) -> str:
        """🔧 P0 NEW: Extract checklist from AI generated content"""
        checklist = f"{system_name} - 快速检查清单\n"
        checklist += "=" * 50 + "\n\n"
        
        # Look for numbered lists or bullet points in the content
        lines = content.split('\n')
        in_checklist = False
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['清单', '检查', '验证', '步骤']):
                in_checklist = True
                checklist += f"\n【{line}】\n"
            elif line.startswith(('- ', '* ', '1.', '2.', '3.', '4.', '5.')):
                if in_checklist:
                    checklist += f"☐ {line.lstrip('- *123456789.')}\n"
        
        # If no checklist found, create a basic one
        if len(checklist.split('\n')) < 5:
            checklist += """
基本决策验证：
☐ 权威资质确认 - 验证决策者的专业能力边界
☐ 数据独立核实 - 通过第三方渠道验证关键信息  
☐ 异常表现分析 - 检查是否存在统计学异常
☐ 透明度评估 - 评估信息披露的充分性
☐ 集体偏见识别 - 确认是否存在群体思维
☐ 长期风险评估 - 考虑决策的长期后果
"""
        
        return checklist

# Global component renderer instance
component_renderer = ComponentRenderer()
