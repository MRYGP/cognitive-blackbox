# cognitive-blackbox/app.py
"""
Cognitive Black Box - Streamlit Main Application (Complete Refactored Version)
Architecture: Modular + Configurable + AI-Intelligent
Based on S's component schema design
"""

import streamlit as st
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root directory to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import refactored modules with error handling
try:
    from core.case_manager import case_manager, case_renderer
    from utils.session_manager import session_manager
    from core.ai_engine import ai_engine
    from views.component_renderer import component_renderer
    from config import get_app_config
    from utils.error_handlers import error_handler, ErrorType
    from utils.validators import input_validator
    
    MODULES_LOADED = True
    
except ImportError as e:
    st.error(f"模块导入失败: {str(e)}")
    st.error("请确保所有必要的文件都已正确部署到对应目录")
    st.stop()

class CognitiveBlackBoxApp:
    """
    Cognitive Black Box main application class (Complete Refactored)
    Implements S's component-based architecture with AI integration
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
                'show_debug_ui': True,
                'ai_enabled': True,
                'fallback_mode': False
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
            # Load case configuration using new architecture
            case_data = case_manager.load_case(self.default_case)
            if not case_data:
                st.error("案例配置加载失败，请刷新页面重试")
                st.stop()
            
            # Initialize session with case data
            success = session_manager.initialize_session(self.default_case)
            if success:
                st.session_state.initialized = True
                st.session_state.case_data = case_data
                st.session_state.app_version = "2.0.0-complete"
                st.session_state.architecture = "S_schema_based"
                
                # Initialize user decisions storage
                if 'user_decisions' not in st.session_state:
                    st.session_state.user_decisions = {}
                    
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
                border-color: #059669; 
                font-family: 'Merriweather', serif; 
            }
            
            .role-assistant { 
                background-color: #F1FAFA; 
                border-color: #0891B2; 
                font-family: 'Lato', sans-serif; 
            }
            
            .act-container {
                border-left: 6px solid;
                background: linear-gradient(135deg, rgba(42, 82, 190, 0.05) 0%, rgba(255,255,255,0.95) 100%);
                padding: 2rem;
                margin-bottom: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }
            
            .component-separator {
                margin: 1.5rem 0;
                border-bottom: 1px solid rgba(42, 82, 190, 0.2);
            }
            
            .magic-moment {
                animation: fadeIn 1s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
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
        """Main application logic using S's component-based architecture"""
        current_step = st.session_state.get('current_step', 1)
        
        # Load case data using new schema
        case_data = case_manager.load_case(self.default_case)
        if not case_data:
            st.error("案例配置加载失败")
            return
        
        # Find current act using S's schema structure
        acts = case_data.get('acts', [])
        current_act = next((act for act in acts if act['act_id'] == current_step), None)
        
        if current_act:
            # Use S's component-based rendering
            try:
                component_renderer.render_act(current_act)
                
                # Add navigation
                self._render_navigation(current_act, len(acts))
                
            except Exception as e:
                error_handler.handle_error(
                    e,
                    ErrorType.SYSTEM_ERROR,
                    context={'current_step': current_step, 'act_id': current_act.get('act_id')},
                    user_visible=True
                )
                
                # Fallback to basic display
                st.error("内容渲染出现问题，正在使用备用模式...")
                self._render_fallback_content(current_act)
        else:
            st.error(f"未找到步骤 {current_step} 的内容")

    def _render_navigation(self, current_act: Dict[str, Any], total_acts: int) -> None:
        """Render navigation based on S's design"""
        current_step = current_act.get('act_id', 1)
        
        # Progress indicator
        progress = (current_step / total_acts) * 100
        st.progress(progress / 100)
        
        # Navigation buttons
        st.markdown("---")
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
                # Smart navigation - check if user has completed current step
                can_advance = self._check_step_completion(current_step)
                
                if can_advance:
                    if st.button("下一幕 ➡️", type="primary"):
                        st.session_state.current_step = current_step + 1
                        st.rerun()
                else:
                    st.button("下一幕 ➡️", disabled=True, help="请完成当前步骤的内容")
            else:
                # Final step - restart option
                if st.button("🔄 重新开始", type="secondary"):
                    self._reset_session()
                    st.rerun()

    def _check_step_completion(self, current_step: int) -> bool:
        """Check if current step is completed and user can advance"""
        if current_step == 1:
            # Check if user has made at least some decisions
            user_decisions = st.session_state.get('user_decisions', {})
            return len(user_decisions) > 0
        elif current_step == 2:
            # User can always advance from reality check
            return True
        elif current_step == 3:
            # User can always advance from framework building
            return True
        else:
            return True

    def _render_fallback_content(self, current_act: Dict[str, Any]) -> None:
        """Render fallback content when component renderer fails"""
        st.subheader(current_act.get('act_name', f"第 {current_act.get('act_id', 1)} 幕"))
        
        role = current_act.get('role', 'narrator')
        st.info(f"当前角色: {role}")
        
        # Basic component rendering
        components = current_act.get('components', [])
        for component in components:
            component_type = component.get('component_type', 'unknown')
            
            if component_type == 'dialogue':
                content = component.get('content_md', '')
                if content:
                    st.markdown(content)
                    
            elif component_type == 'decision_points':
                st.subheader("决策分析")
                points = component.get('points', [])
                
                for i, point in enumerate(points):
                    question = point.get('question', f'决策点 {i+1}')
                    with st.expander(question, expanded=i==0):
                        user_input = st.text_area(
                            "您的分析:",
                            key=f"fallback_decision_{i}",
                            height=100
                        )
                        if user_input:
                            point_id = point.get('point_id', f'dp_{i}')
                            st.session_state.user_decisions[point_id] = user_input
                            
            else:
                st.info(f"组件类型: {component_type}")

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
            
            # Architecture status
            st.sidebar.subheader("📊 架构状态")
            try:
                # Import main package to get status
                import cognitive_black_box
                system_status = cognitive_black_box.get_system_status()
                
                st.sidebar.json({
                    'overall_health': system_status.get('overall_health', 'unknown'),
                    'app_version': st.session_state.get('app_version', 'unknown'),
                    'architecture': st.session_state.get('architecture', 'unknown')
                })
                
            except Exception as e:
                st.sidebar.error(f"状态检查失败: {str(e)}")
            
            # Session information
            st.sidebar.subheader("📱 会话信息")
            session_summary = session_manager.get_session_summary()
            st.sidebar.json(session_summary)
            
            # Case management information
            st.sidebar.subheader("📁 案例管理")
            try:
                case_info = case_manager.get_cache_info()
                st.sidebar.json(case_info)
            except Exception as e:
                st.sidebar.error(f"案例管理状态获取失败: {str(e)}")
            
            # AI engine status
            st.sidebar.subheader("🤖 AI引擎状态")
            try:
                ai_stats = ai_engine.get_cache_stats()
                st.sidebar.json({
                    'available_apis': ai_engine.get_available_apis(),
                    'cache_stats': ai_stats
                })
                
                if st.sidebar.button("测试AI引擎"):
                    test_context = {'current_step': 1, 'case_name': 'madoff'}
                    response, success = ai_engine.generate_response(
                        'host', 
                        '测试消息', 
                        test_context
                    )
                    if success:
                        st.sidebar.success("AI引擎测试成功")
                    else:
                        st.sidebar.warning("AI引擎使用降级模式")
                        
            except Exception as e:
                st.sidebar.error(f"AI引擎状态获取失败: {str(e)}")
            
            # Component renderer status
            st.sidebar.subheader("🎨 渲染器状态")
            try:
                from views import get_renderer_info
                renderer_info = get_renderer_info()
                st.sidebar.json(renderer_info)
            except Exception as e:
                st.sidebar.error(f"渲染器状态获取失败: {str(e)}")
            
            # System actions
            st.sidebar.subheader("🔧 系统操作")
            
            if st.sidebar.button("清除缓存"):
                try:
                    case_manager.clear_cache()
                    ai_engine.clear_cache()
                    st.sidebar.success("缓存已清除")
                except Exception as e:
                    st.sidebar.error(f"缓存清除失败: {str(e)}")
            
            if st.sidebar.button("重置会话"):
                self._reset_session()
                st.sidebar.success("会话已重置")
                st.rerun()
            
            # Error statistics
            st.sidebar.subheader("🚨 错误统计")
            try:
                error_stats = error_handler.get_error_stats()
                st.sidebar.json(error_stats)
                
                if error_stats.get('total_errors', 0) > 0:
                    if st.sidebar.button("清除错误历史"):
                        error_handler.clear_error_history()
                        st.sidebar.success("错误历史已清除")
                        st.rerun()
                        
            except Exception as e:
                st.sidebar.error(f"错误统计获取失败: {str(e)}")

def main():
    """Main function to run the Streamlit application"""
    try:
        # Show startup message
        startup_placeholder = st.empty()
        startup_placeholder.info("🚀 认知黑匣子正在启动...")
        
        # Initialize and run app
        app = CognitiveBlackBoxApp()
        
        # Clear startup message
        startup_placeholder.empty()
        
        # Run the application
        app.run()
        
    except Exception as e:
        st.error(f"应用运行出现严重错误: {str(e)}")
        
        # Show error details in debug mode
        if st.checkbox("显示错误详情"):
            import traceback
            st.text(traceback.format_exc())
        
        # Provide recovery options
        st.subheader("🔧 恢复选项")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 重新加载应用"):
                st.rerun()
        
        with col2:
            if st.button("🧹 清除所有数据"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Show help information
        with st.expander("📖 故障排除指南"):
            st.markdown("""
            **常见问题解决方案:**
            
            1. **模块导入失败**: 确保所有文件都已正确部署到对应目录
            2. **配置文件缺失**: 检查 config/cases/ 和 config/prompts/ 目录
            3. **API密钥问题**: 在 Streamlit Cloud Secrets 中配置 GEMINI_API_KEY
            4. **权限问题**: 确保所有文件都有正确的读取权限
            
            **如果问题持续存在:**
            - 检查 GitHub 仓库中的文件完整性
            - 运行 `python test_architecture.py` 进行系统诊断
            - 查看 Streamlit Cloud 的日志输出
            """)

if __name__ == "__main__":
    main()
