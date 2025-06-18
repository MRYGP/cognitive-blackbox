# cognitive-blackbox/app.py
"""
Cognitive Black Box - Streamlit Main Application Entry (Refactored)
Architecture: Modular + Configurable + AI-Intelligent
"""

import streamlit as st
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root directory to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import refactored modules
try:
    from core.case_manager import case_manager, case_renderer
    from utils.session_manager import session_manager
    from utils.ai_roles import ai_engine
    from config import get_app_config
except ImportError as e:
    st.error(f"模块导入失败: {str(e)}")
    st.stop()

class CognitiveBlackBoxApp:
    """
    Cognitive Black Box main application class (Refactored)
    Architecture-first design with configuration-driven content
    """
    
    def __init__(self):
        """Initialize application with new architecture"""
        self.app_title = "🧠 认知黑匣子"
        self.app_description = "18分钟认知升级体验"
        self.default_case = "madoff"
        
        # Load app configuration
        try:
            self.app_config = get_app_config()
        except:
            # Fallback configuration
            self.app_config = {
                'debug_mode': True,
                'show_debug_ui': True
            }
    
    def run(self):
        """Run main application with new architecture"""
        self._configure_page()
        self._initialize_session()
        self._inject_theme_css()
        self._show_header()
        self._main_app_logic()
        
        if self.app_config.get('show_debug_ui', False):
            self._show_debug_info()

    def _configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title=self.app_title,
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="auto"
        )

    def _initialize_session(self):
        """Initialize session with case configuration"""
        if 'initialized' not in st.session_state:
            # Load case configuration
            case_data = case_manager.load_case(self.default_case)
            if not case_data:
                st.error("案例配置加载失败，请刷新页面重试")
                st.stop()
            
            # Initialize session with case data
            success = session_manager.initialize_session(self.default_case)
            if success:
                st.session_state.initialized = True
                st.session_state.case_data = case_data
                st.session_state.app_version = "0.2.0-refactored"
            else:
                st.error("应用初始化失败,请刷新页面重试")
                st.stop()

    def _inject_theme_css(self):
        """Inject base CSS styles"""
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Lato:wght@400;700&family=Lora:wght@400;700&family=Merriweather:wght@400;700&display=swap');
            
            .stApp { 
                background-color: #F0F2F6; 
            }
            
            .block-container { 
                max-width: 800px; 
                padding-top: 2rem; 
            }
            
            .role-container {
                border-radius: 12px; 
                padding: 2rem; 
                margin-bottom: 2rem;
                border-left: 6px solid; 
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            }
            
            .role-host { 
                background-color: #FFFFFF; 
                border-color: #2A52BE; 
                font-family: 'Lora', serif; 
            }
            
            .role-investor { 
                background-color: #FFF5F5; 
                border-color: #D93025; 
                font-family: 'Inter', sans-serif; 
            }
            
            .role-mentor { 
                background-color: #F3F9F3; 
                border-color: #006A4E; 
                font-family: 'Merriweather', serif; 
            }
            
            .role-assistant { 
                background-color: #F1FAFA; 
                border-color: #007B7C; 
                font-family: 'Lato', sans-serif; 
            }
        </style>
        """, unsafe_allow_html=True)
    
    def _show_header(self):
        """Show application header with case info"""
        st.title(self.app_title)
        st.caption(self.app_description)
        
        # Show case metadata
        case_metadata = case_manager.get_case_metadata(self.default_case)
        if case_metadata:
            col1, col2, col3 = st.columns(3)
            col1.metric("案例", case_metadata.title.split("：")[0])
            col2.metric("认知偏误", case_metadata.target_bias)
            col3.metric("体验时长", f"{case_metadata.duration_minutes}分钟")
    
    def _main_app_logic(self):
        """Main application logic using S's components architecture"""
        from views.component_renderer import component_renderer
        
        current_step = st.session_state.get('current_step', 1)
        
        # Load case data using new schema
        case_data = case_manager.load_case(self.default_case)
        if not case_data:
            st.error("案例配置加载失败")
            return
        
        # Find current act
        acts = case_data.get('acts', [])
        current_act = next((act for act in acts if act['act_id'] == current_step), None)
        
        if current_act:
            # Use S's component-based rendering
            component_renderer.render_act(current_act)
            
            # Add navigation
            self._render_navigation(current_act, len(acts))
        else:
            st.error(f"未找到步骤 {current_step} 的内容")

    def _show_act1_host(self):
        """Act 1: Host - Decision Immersion (Configuration-driven)"""
        case_id = self.default_case
        act_content = case_manager.get_act_content(case_id, 'act1_host')
        
        if not act_content:
            st.error("第一幕内容加载失败")
            return
        
        # Render header and theme
        case_renderer.render_act_header(case_id, 'act1_host')
        case_renderer.render_knowledge_card(case_id, 'act1_host')
        
        with st.container():
            st.markdown('<div class="role-container role-host">', unsafe_allow_html=True)
            
            # Opening content
            opening_text = act_content.get('opening_text', [])
            for paragraph in opening_text:
                if paragraph.strip():
                    st.markdown(paragraph)
                else:
                    st.markdown("")
            
            # Case introduction
            case_intro = act_content.get('case_introduction', {})
            if case_intro:
                st.markdown("---")
                st.subheader(f"**{case_intro.get('year', '')}**")
                st.markdown(case_intro.get('event', ''))
                
                if 'victims' in case_intro:
                    st.markdown("**受害者名单让所有人震惊：**")
                    for victim in case_intro['victims']:
                        st.markdown(f"- **{victim}**")
            
            # Investment opportunity
            investment_opp = act_content.get('investment_opportunity', {})
            if investment_opp:
                st.markdown("---")
                st.subheader("🎯 " + investment_opp.get('title', '投资机会档案'))
                st.markdown(investment_opp.get('context', ''))
                
                details = investment_opp.get('details', {})
                for key, value in details.items():
                    st.markdown(f"- **{self._format_field_name(key)}**: {value}")
            
            # Decision points (editable)
            decision_points = case_manager.get_decision_points(case_id)
            if decision_points:
                st.markdown("---")
                st.subheader("专业决策分析")
                
                # User decision tracking
                if 'user_decisions' not in st.session_state:
                    st.session_state.user_decisions = {}
                
                for i, dp in enumerate(decision_points):
                    with st.expander(f"决策点 {i+1}: {dp.get('question', '')}", expanded=i==0):
                        
                        if dp.get('editable', True):
                            # Allow user to edit the typical logic
                            default_logic = dp.get('typical_logic', '')
                            user_logic = st.text_area(
                                "您的专业判断：",
                                value=default_logic,
                                key=f"decision_{i}",
                                height=100
                            )
                            st.session_state.user_decisions[dp.get('id', f'dp{i}')] = user_logic
                        else:
                            st.markdown(f"**典型思维**: {dp.get('typical_logic', '')}")
                        
                        if dp.get('host_comment'):
                            st.info(f"💭 **主持人点评**: {dp['host_comment']}")
            
            # Authority validation
            authority_validation = act_content.get('authority_validation', {})
            if authority_validation:
                st.markdown("---")
                st.subheader(authority_validation.get('title', ''))
                content = authority_validation.get('content', [])
                for paragraph in content:
                    if paragraph.strip():
                        st.markdown(paragraph)
                    else:
                        st.markdown("")
            
            # Transition
            transition = act_content.get('transition_to_act2', {})
            if transition:
                st.markdown("---")
                st.markdown(transition.get('revelation', ''))
                st.markdown(transition.get('teaser', ''))
                
            # Advance button
            if st.button("完成判断，进入下一幕", type="primary", use_container_width=True):
                if session_manager.advance_step():
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _show_act2_investor(self):
        """Act 2: Investor - Reality Disruption (Configuration-driven)"""
        case_id = self.default_case
        act_content = case_manager.get_act_content(case_id, 'act2_investor')
        
        if not act_content:
            st.error("第二幕内容加载失败")
            return
        
        # Render header and theme
        case_renderer.render_act_header(case_id, 'act2_investor')
        case_renderer.render_knowledge_card(case_id, 'act2_investor')
        
        with st.container():
            st.markdown('<div class="role-container role-investor">', unsafe_allow_html=True)
            
            # Opening revelation
            opening_revelation = act_content.get('opening_revelation', {})
            if opening_revelation:
                st.subheader(opening_revelation.get('title', ''))
                content = opening_revelation.get('content', [])
                for paragraph in content:
                    if paragraph.strip():
                        st.markdown(paragraph)
                    else:
                        st.markdown("")
            
            # Victim showcase
            victim_showcase = act_content.get('victim_showcase', {})
            if victim_showcase:
                st.markdown("**受害者包括：**")
                for victim in victim_showcase.get('notable_victims', []):
                    st.markdown(f"- **{victim}**")
                
                st.markdown("")
                st.markdown(victim_showcase.get('challenge_question', ''))
            
            # Four challenges (can be AI-generated in future)
            four_challenges = act_content.get('four_challenges', {})
            if four_challenges:
                st.markdown("---")
                st.subheader("现在，让我用投资人的视角，问你四个专业问题：")
                
                # Check if AI generation is enabled
                ai_config = act_content.get('ai_generation', {})
                user_decisions = st.session_state.get('user_decisions', {})
                
                if ai_config.get('enabled', False) and user_decisions:
                    # TODO: AI generation will be implemented here
                    # For now, use configuration-based content with personalization
                    self._render_personalized_challenges(four_challenges, user_decisions)
                else:
                    # Use static challenges from configuration
                    self._render_static_challenges(four_challenges)
            
            # Data metrics
            data_metrics = act_content.get('data_metrics', {})
            if data_metrics:
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                metrics = list(data_metrics.items())
                
                if len(metrics) >= 3:
                    col1.metric(list(metrics[0])[0].replace('_', ' ').title(), metrics[0][1])
                    col2.metric(list(metrics[1])[0].replace('_', ' ').title(), metrics[1][1])
                    col3.metric(list(metrics[2])[0].replace('_', ' ').title(), metrics[2][1])
            
            # Ultimate impact
            ultimate_impact = act_content.get('ultimate_impact', {})
            if ultimate_impact:
                st.markdown("---")
                st.subheader(ultimate_impact.get('title', ''))
                content = ultimate_impact.get('content', [])
                for paragraph in content:
                    if paragraph.strip():
                        st.markdown(paragraph)
                    else:
                        st.markdown("")
            
            # Advance button
            if st.button("我明白了...进入下一步，学习如何防范", type="primary", use_container_width=True):
                if session_manager.advance_step():
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _show_act3_mentor(self):
        """Act 3: Mentor - Framework Reconstruction (Configuration-driven)"""
        case_id = self.default_case
        act_content = case_manager.get_act_content(case_id, 'act3_mentor')
        
        if not act_content:
            st.error("第三幕内容加载失败")
            return
        
        # Render header and theme
        case_renderer.render_act_header(case_id, 'act3_mentor')
        case_renderer.render_knowledge_card(case_id, 'act3_mentor')
        
        with st.container():
            st.markdown('<div class="role-container role-mentor">', unsafe_allow_html=True)
            
            # Theoretical foundation
            theoretical_foundation = act_content.get('theoretical_foundation', {})
            if theoretical_foundation:
                st.subheader(theoretical_foundation.get('title', ''))
                
                discovery = theoretical_foundation.get('discovery', {})
                if discovery:
                    st.markdown(f"**发现者**: {discovery.get('researcher', '')} ({discovery.get('year', '')})")
                    st.markdown(f"**背景**: {discovery.get('context', '')}")
                    
                    if 'original_quote' in discovery:
                        st.info(f"💬 **原始发现**: {discovery['original_quote']}")
                
                if 'definition' in theoretical_foundation:
                    st.markdown(f"**定义**: {theoretical_foundation['definition']}")
            
            # Cognitive deconstruction
            cognitive_deconstruction = act_content.get('cognitive_deconstruction', {})
            if cognitive_deconstruction:
                st.markdown("---")
                st.subheader(cognitive_deconstruction.get('title', ''))
                
                halo_types = cognitive_deconstruction.get('halo_types', [])
                if halo_types:
                    st.markdown("**在麦道夫案例中的具体表现**：")
                    for halo_type in halo_types:
                        st.markdown(f"- {halo_type}")
            
            # Framework solution
            framework_solution = act_content.get('framework_solution', {})
            if framework_solution:
                st.markdown("---")
                st.subheader(framework_solution.get('title', ''))
                st.markdown(framework_solution.get('description', ''))
                
                dimensions = framework_solution.get('dimensions', [])
                for dim in dimensions:
                    with st.expander(f"{dim.get('title', '')}", expanded=False):
                        st.markdown(dim.get('description', ''))
                        if 'example' in dim:
                            st.example(f"**示例**: {dim['example']}")
            
            # Decision comparison table
            decision_comparison = act_content.get('decision_comparison', {})
            if decision_comparison:
                st.markdown("---")
                st.subheader(decision_comparison.get('title', ''))
                
                comparison_table = decision_comparison.get('comparison_table', [])
                if comparison_table:
                    import pandas as pd
                    
                    df_data = []
                    for row in comparison_table:
                        df_data.append({
                            '维度': row.get('dimension', ''),
                            '麦道夫受害者路径': row.get('victim_path', ''),
                            '专业验证路径': row.get('safe_path', '')
                        })
                    
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True)
            
            # Advance button
            if st.button("我掌握了。请给我实用的工具", type="primary", use_container_width=True):
                if session_manager.advance_step():
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _show_act4_assistant(self):
        """Act 4: Assistant - Capability Armament (Configuration-driven)"""
        case_id = self.default_case
        act_content = case_manager.get_act_content(case_id, 'act4_assistant')
        
        if not act_content:
            st.error("第四幕内容加载失败")
            return
        
        # Render header and theme
        case_renderer.render_act_header(case_id, 'act4_assistant')
        case_renderer.render_knowledge_card(case_id, 'act4_assistant')
        
        with st.container():
            st.markdown('<div class="role-container role-assistant">', unsafe_allow_html=True)
            
            # Capability test
            capability_test = act_content.get('capability_test', {})
            if capability_test:
                st.subheader(capability_test.get('title', ''))
                
                scenario = capability_test.get('scenario', {})
                if scenario:
                    st.markdown(f"**场景**: {scenario.get('context', '')}")
                    
                    details = scenario.get('details', [])
                    for detail in details:
                        st.markdown(f"- {detail}")
                    
                    st.markdown(f"**问题**: {scenario.get('question', '')}")
                    
                    # User input for test
                    user_analysis = st.text_area(
                        "请输入您的分析：",
                        height=150,
                        key="capability_test_analysis"
                    )
                    
                    if user_analysis and st.button("提交分析"):
                        feedback_template = capability_test.get('feedback_template', '')
                        # Simple feedback for now - can be enhanced with AI
                        st.success(f"出色的分析！您展现了高级决策者应有的认知警觉性。")
            
            # Barbell strategy
            barbell_strategy = act_content.get('barbell_strategy', {})
            if barbell_strategy:
                st.markdown("---")
                st.subheader(barbell_strategy.get('title', ''))
                st.markdown(barbell_strategy.get('philosophy', ''))
                
                risk_categorization = barbell_strategy.get('risk_categorization', {})
                if risk_categorization:
                    col1, col2 = st.columns(2)
                    
                    acceptable_risk = risk_categorization.get('acceptable_risk', {})
                    col1.success(f"**可承受风险**: {acceptable_risk.get('definition', '')}")
                    col1.markdown(acceptable_risk.get('approach', ''))
                    
                    unacceptable_risk = risk_categorization.get('unacceptable_risk', {})
                    col2.error(f"**不可承受风险**: {unacceptable_risk.get('definition', '')}")
                    col2.markdown(unacceptable_risk.get('approach', ''))
            
            # Personalized system generation
            personalized_system = act_content.get('personalized_system', {})
            if personalized_system:
                st.markdown("---")
                st.subheader(personalized_system.get('title', ''))
                
                # User inputs for personalization
                system_name = st.text_input(
                    personalized_system.get('tool_name_prompt', '系统名称：'),
                    value="高级决策安全系统",
                    key="user_system_name"
                )
                
                user_principle = st.text_input(
                    personalized_system.get('principle_prompt', '核心原则：'),
                    value="权威越强，越要验证",
                    key="user_principle"
                )
                
                if system_name and user_principle:
                    # Generate personalized tool
                    self._generate_personalized_tool(personalized_system, system_name, user_principle)
            
            # Application extension
            application_extension = act_content.get('application_extension', {})
            if application_extension:
                st.markdown("---")
                st.subheader(application_extension.get('title', ''))
                
                areas = application_extension.get('areas', [])
                for area in areas:
                    st.markdown(f"- {area}")
                
                if 'core_principle' in application_extension:
                    st.info(f"**核心原则**: {application_extension['core_principle']}")
            
            # Final wisdom
            final_wisdom = act_content.get('final_wisdom', '')
            if final_wisdom:
                st.markdown("---")
                st.info(final_wisdom)
            
            # Restart button
            if st.button("重新开始体验", use_container_width=True):
                self._reset_session()
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    def _render_static_challenges(self, four_challenges: Dict[str, Any]) -> None:
        """Render static challenges from configuration"""
        for challenge_key, challenge_data in four_challenges.items():
            with st.expander(f"展开 {challenge_data.get('title', challenge_key)}", expanded=True):
                content = challenge_data.get('content', [])
                for paragraph in content:
                    if paragraph.strip():
                        st.markdown(paragraph)
                    else:
                        st.markdown("")

    def _render_personalized_challenges(self, four_challenges: Dict[str, Any], user_decisions: Dict[str, str]) -> None:
        """Render challenges with basic personalization"""
        # Basic personalization - can be enhanced with AI
        user_decision_summary = list(user_decisions.values())[0][:100] if user_decisions else "谨慎分析"
        
        for challenge_key, challenge_data in four_challenges.items():
            with st.expander(f"展开 {challenge_data.get('title', challenge_key)}", expanded=True):
                st.info(f"💭 基于您刚才的分析：'{user_decision_summary}...'，让我质疑您的判断。")
                
                content = challenge_data.get('content', [])
                for paragraph in content:
                    if paragraph.strip():
                        st.markdown(paragraph)
                    else:
                        st.markdown("")

    def _generate_personalized_tool(self, personalized_system: Dict[str, Any], system_name: str, user_principle: str) -> None:
        """Generate personalized decision tool"""
        system_template = personalized_system.get('system_template', {})
        
        tool_content = f"""
### 🛡️ {system_name}

**💡 核心决策原则**: {user_principle}

#### 🧠 四维独立验证矩阵：
1. **身份验证**: 区分职位权威 vs 专业权威
2. **能力验证**: 要求第三方审计的业绩证明  
3. **信息验证**: 拒绝任何不合理的信息黑盒
4. **独立验证**: 获取真正独立的专业意见

#### ⚖️ 杠铃风险管理策略：
- **90%资源**: 完全可验证、可控制的核心机会
- **10%资源**: 高风险高回报的探索性尝试
- **核心认知**: 明确区分"理性决策"与"风险博弈"
- **麦道夫教训**: 永远不要把核心资源押在无法验证的机会上

#### ⚠️ 高危信号预警系统：
- "这涉及商业机密，无法透露细节"
- 过于完美的历史业绩表现
- 拒绝第三方审计或托管分离
- 基于权威身份的信任请求
- "所有聪明人都在参与"的群体暗示

#### 🎯 高级决策者认知升级：
- 权威光环 ≠ 专业能力（区分职能边界）
- 异常稳定 = 最大风险信号（统计常识）
- 信息透明 = 可信度基础（尽调原则）
- 独立验证 > 集体共识（避免群体盲从）
- 系统思维 > 直觉判断（认知升级）
"""
        
        st.success("您的专属决策工具已生成！")
        st.markdown(tool_content)
        
        # Download option
        st.download_button(
            label="下载决策工具",
            data=tool_content,
            file_name=f"{system_name}.md",
            mime="text/markdown"
        )

    def _render_navigation(self, current_act: Dict[str, Any], total_acts: int) -> None:
        """Render navigation based on S's design"""
        current_step = current_act.get('act_id', 1)
        
        # Progress indicator
        progress = (current_step / total_acts) * 100
        st.progress(progress / 100)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_step > 1:
                if st.button("⬅️ 上一幕"):
                    st.session_state.current_step = current_step - 1
                    st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center'>第 {current_step} 幕 / 共 {total_acts} 幕</div>", 
                       unsafe_allow_html=True)
        
        with col3:
            if current_step < total_acts:
                if st.button("下一幕 ➡️", type="primary"):
                    st.session_state.current_step = current_step + 1
                    st.rerun()

    def _reset_session(self):
        """Reset session to start"""
        keys_to_clear = ['initialized', 'current_step', 'user_decisions', 'case_data']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

    def _show_debug_info(self):
        """Show debug information in sidebar"""
        if st.sidebar.checkbox("显示调试信息", key="debug_toggle"):
            st.sidebar.subheader("🔧 调试信息")
            
            # Session information
            session_summary = session_manager.get_session_summary()
            st.sidebar.json(session_summary)
            
            # Case management information
            case_info = case_manager.get_cache_info()
            st.sidebar.subheader("📁 案例管理")
            st.sidebar.json(case_info)
            
            # AI engine test
            if st.sidebar.button("测试AI引擎"):
                try:
                    available_apis = ai_engine.get_available_apis()
                    st.sidebar.success(f"可用API: {available_apis}")
                except Exception as e:
                    st.sidebar.error(f"AI引擎错误: {str(e)}")

def main():
    """Main function to run the Streamlit application"""
    try:
        app = CognitiveBlackBoxApp()
        app.run()
    except Exception as e:
        st.error(f"应用运行出现严重错误: {str(e)}")
        if st.button("重新加载应用"):
            st.rerun()

if __name__ == "__main__":
    main()
