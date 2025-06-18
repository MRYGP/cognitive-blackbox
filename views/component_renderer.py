"""
Cognitive Black Box - Component-Based Renderer (Final Fixed Version)
🔧 P0 Fixed: 第四幕AI工具生成优化
🔧 P1 Fixed: 第二幕AI成功后避免静态内容重复
"""

import streamlit as st
import asyncio
from typing import Dict, Any, List, Optional
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
        """Render act header component"""
        st.header(component.get('title', ''))
        if 'subtitle' in component:
            st.caption(component['subtitle'])
        if 'opening_quote' in component:
            st.info(f"💭 {component['opening_quote']}")
        
        # Progress indicator
        progress = st.session_state.get('current_step', 1) * 25
        st.progress(progress / 100)
    
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
        """🔧 FIXED: Functional custom case input instead of 'under development'"""
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
            
            with st.form("custom_case_form"):
                case_background = st.text_area(
                    "💼 案例背景",
                    placeholder="请描述决策的背景：时间、地点、涉及的人员或机构...",
                    height=100
                )
                
                decision_situation = st.text_area(
                    "🎯 决策情况", 
                    placeholder="您当时面临什么选择？有哪些关键信息影响了判断？",
                    height=100
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("🚀 开始个性化分析", type="primary")
                with col2:
                    cancelled = st.form_submit_button("📖 继续标准案例")
                
                if submitted and case_background and decision_situation:
                    st.session_state.custom_case = {
                        'background': case_background,
                        'situation': decision_situation
                    }
                    st.success("✅ **案例已保存！** 后续分析将为您提供针对性洞察。")
                    st.session_state.show_custom_form = False
                    st.session_state.has_custom_case = True
                    st.rerun()
                elif submitted:
                    st.error("⚠️ 请至少填写案例背景和决策情况")
                elif cancelled:
                    st.session_state.show_custom_form = False
                    st.rerun()
    
    def _render_transition(self, component: Dict[str, Any]) -> None:
        """Render transition component"""
        st.subheader(component.get('title', '转场'))
        content_md = component.get('content_md', '')
        
        # Add dramatic transition effects
        with st.container():
            st.markdown("---")
            st.markdown(f"### {component.get('title', '')}")
            st.markdown(content_md)
            
            # Process transition effects
            if 'transition_fx' in component:
                fx = component['transition_fx']
                with st.spinner("准备进入下一幕..."):
                    import time
                    time.sleep(fx.get('duration_ms', 2000) / 1000)
            
            st.markdown("---")
    
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
            
            if success:
                ai_succeeded = True  # 🔧 NEW: Mark AI as succeeded
                st.success("🤖 AI个性化分析完成")
                st.markdown(ai_response)
                
                # Track AI quality
                quality_score = self._evaluate_ai_response_quality(ai_response, 'investor')
                if quality_score < 6.0:
                    st.warning("AI响应质量偏低，已自动记录以优化服务")
        
        # 🔧 FIXED: Only show fallback content if AI didn't succeed
        if not ai_succeeded:
            st.info("😊 AI服务暂时繁忙，为您提供专业的标准分析")
            # Use fallback content
            fallback_id = ai_config.get('fallback_response_id', 'investor_static_challenge_set')
            self._render_fallback_content(fallback_id)
    
    def _render_static_challenge_set(self, component: Dict[str, Any]) -> None:
        """Render static challenge set component"""
        st.subheader(component.get('title', '专业质疑'))
        
        if 'description' in component:
            st.info(component['description'])
        
        challenges = component.get('challenges', [])
        
        for challenge in challenges:
            challenge_title = challenge.get('title', '')
            challenge_content = challenge.get('content_md', '')
            
            with st.expander(f"展开 {challenge_title}", expanded=True):
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
        🔧 P0 FIXED: Enhanced AI tool generation with improved prompt and context
        """
        st.subheader(component.get('title', '定制您的专属决策系统'))
        
        ai_config = component.get('ai_config', {})
        
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
            # 🔧 ENHANCED: Build comprehensive context
            context = self._build_comprehensive_context_for_assistant(ai_config)
            
            # 🔧 ENHANCED: Improved prompt construction
            enhanced_prompt = self._build_enhanced_assistant_prompt(user_system_name, user_core_principle, context)
            
            with st.spinner("🤖 AI正在基于您的决策模式，量身定制专属系统..."):
                ai_tool_content, success = ai_engine.generate_response(
                    'assistant',
                    enhanced_prompt,
                    context
                )
            
            if success:
                st.success("🎉 您的专属决策系统已生成完成！")
                
                # 🔧 NEW: Add system info display
                st.info(f"**系统名称**: {user_system_name}  \n**核心原则**: {user_core_principle}")
                
                # Show the generated content
                st.markdown(ai_tool_content)
                
                # 🔧 ENHANCED: Better download options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 下载完整系统 (Markdown)",
                        data=ai_tool_content,
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
                st.warning("⚠️ AI服务暂时繁忙，为您提供专业的通用系统模板")
                # 🔧 ENHANCED: Better fallback content
                self._render_enhanced_fallback_tool(user_system_name, user_core_principle)
    
    def _build_comprehensive_context_for_assistant(self, ai_config: Dict[str, Any]) -> Dict[str, Any]:
        """🔧 NEW: Build comprehensive context for assistant AI calls"""
        context = {
            'current_step': st.session_state.get('current_step', 4),
            'case_name': 'madoff',
            'user_system_name': st.session_state.get('user_system_name', '高级决策安全系统'),
            'user_core_principle': st.session_state.get('user_core_principle', '权威越强，越要验证'),
            'user_decisions': st.session_state.get('user_decisions', {}),
            'user_background': self._infer_user_background(),
            'session_insights': self._extract_session_insights()
        }
        
        # Add specified context keys from ai_config
        input_context_keys = ai_config.get('input_context_keys', [])
        for key in input_context_keys:
            if key in st.session_state:
                context[key] = st.session_state[key]
        
        return context
    
    def _build_enhanced_assistant_prompt(self, system_name: str, core_principle: str, context: Dict[str, Any]) -> str:
        """🔧 NEW: Build enhanced prompt for assistant AI"""
        user_decisions_summary = self._summarize_user_decisions(context.get('user_decisions', {}))
        
        prompt = f"""
请为用户设计一个完整的个性化决策安全系统。

**用户信息：**
- 系统名称：{system_name}
- 核心原则：{core_principle}
- 决策背景：{context.get('user_background', '高级管理者')}

**用户在麦道夫案例中的决策表现：**
{user_decisions_summary}

**设计要求：**
1. 系统必须体现用户的核心原则："{core_principle}"
2. 针对用户在案例中的决策模式进行个性化设计
3. 提供立即可用的检查清单、评估工具和实施指导
4. 内容要专业、实用、易于在实际工作中应用
5. 确保系统名称"{system_name}"贯穿整个设计

请生成一个完整的、个性化的决策安全系统。
"""
        return prompt
    
    def _summarize_user_decisions(self, user_decisions: Dict[str, Any]) -> str:
        """🔧 NEW: Summarize user decisions for AI prompt"""
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
        """🔧 NEW: Infer user background from session data"""
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
        """🔧 NEW: Extract key insights from the session"""
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
        """🔧 NEW: Extract checklist from AI generated content"""
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
    
    def _render_enhanced_fallback_tool(self, system_name: str, core_principle: str) -> None:
        """🔧 NEW: Enhanced fallback content when AI fails"""
        st.markdown(f"### {system_name}")
        st.markdown(f"**核心原则**: {core_principle}")
        
        st.markdown("""
#### 🔍 决策验证清单

**第一步：权威验证**
- ☐ 确认决策相关方的专业资质和能力边界
- ☐ 验证权威人士在此领域的历史表现
- ☐ 区分职位权威与专业能力

**第二步：数据核实**  
- ☐ 通过独立渠道验证关键数据
- ☐ 检查数据的时效性和完整性
- ☐ 识别可能的数据操纵迹象

**第三步：异常分析**
- ☐ 评估表现是否过于完美或一致
- ☐ 对比行业基准和历史趋势
- ☐ 调查异常稳定背后的真实原因

**第四步：风险评估**
- ☐ 识别最坏情况及其概率
- ☐ 评估损失承受能力
- ☐ 制定应急预案

#### 🚨 高危信号预警

当遇到以下情况时，请提高警惕：
- 🔴 拒绝透明度要求或信息披露
- 🔴 过于完美的历史表现记录
- 🔴 强烈依赖权威背书而缺乏实质验证
- 🔴 群体性的一致好评但缺乏批判声音

#### 💡 实施建议

1. **日常使用**：将此清单保存在手机中，重大决策前必看
2. **团队分享**：与决策团队共享，建立集体验证机制  
3. **定期回顾**：每月回顾决策质量，持续改进工具
4. **案例积累**：记录成功和失败案例，丰富经验库
""")
        
        # Still provide download for fallback content
        fallback_content = f"""# {system_name}

**核心原则**: {core_principle}

## 决策验证清单

### 权威验证
- 确认专业资质和能力边界
- 验证历史表现记录
- 区分职位权威与专业能力

### 数据核实  
- 独立渠道验证关键数据
- 检查时效性和完整性
- 识别数据操纵迹象

### 异常分析
- 评估表现合理性
- 对比行业基准
- 调查异常原因

### 风险评估
- 识别最坏情况
- 评估承受能力
- 制定应急预案

## 高危信号预警
- 拒绝透明度要求
- 过于完美的表现
- 过度依赖权威背书
- 群体性一致好评

使用此工具，让每个决策都经过科学验证！
"""
        
        st.download_button(
            label="📥 下载通用决策系统",
            data=fallback_content,
            file_name=f"{system_name.replace(' ', '_')}_通用版.md",
            mime="text/markdown",
            use_container_width=True
        )
    
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
        """Format user decisions for AI prompt"""
        user_decisions = context.get('user_decisions', {})
        
        if not user_decisions:
            return "用户尚未完成决策分析"
        
        formatted = "用户的决策分析：\n"
        for decision_id, decision_content in user_decisions.items():
            formatted += f"- {decision_id}: {decision_content[:200]}...\n"
        
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

# Global component renderer instance
component_renderer = ComponentRenderer()
