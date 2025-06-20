"""
Cognitive Black Box - Streamlit Main Application (Safe Multi-Case Update)
Architecture: Modular + Configurable + AI-Intelligent + Multi-Case Support
Based on existing app.py structure with minimal changes for case selection
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
    
    # Import case selection interface (NEW)
    try:
        from case_selection_interface import render_case_selection_page, get_case_metadata
        CASE_SELECTION_AVAILABLE = True
    except ImportError:
        CASE_SELECTION_AVAILABLE = False
        st.warning("案例选择界面模块未找到，将使用默认案例")
    
    MODULES_LOADED = True
    
except ImportError as e:
    st.error(f"模块导入失败: {str(e)}")
    st.error("请确保所有必要的文件都已正确部署到对应目录")
    st.stop()

class CognitiveBlackBoxApp:
    """
    Cognitive Black Box main application class (Safe Multi-Case Update)
    Maintains existing functionality while adding case selection capability
    """
    
    def __init__(self):
        """Initialize application with enhanced architecture"""
        self.app_title = "🧠 认知黑匣子"
        self.app_description = "18分钟认知升级体验"
        self.default_case = "madoff"
        
        # Available cases for selection (NEW)
        self.available_cases = ["madoff", "ltcm"]
        
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
        """Run main application with conditional case selection"""
        self._configure_page()
        self._initialize_session()
        
        # NEW: Check if we should show case selection or run case experience
        if self._should_show_case_selection():
            self._run_case_selection_mode()
        else:
            self._run_single_case_mode()
        
        if self.app_config.get('show_debug_ui', False):
            self._show_debug_info()

    def _should_show_case_selection(self) -> bool:
        """
        Determine if we should show case selection interface
        
        Returns:
            bool: True if case selection should be shown
        """
        # Show case selection if:
        # 1. Case selection module is available
        # 2. User hasn't selected a case yet, OR wants to return to selection
        return (CASE_SELECTION_AVAILABLE and 
                (not st.session_state.get('case_selection_made', False) or
                 st.session_state.get('return_to_selection', False)))

    def _run_case_selection_mode(self):
        """Run the application in case selection mode (NEW)"""
        # Apply case selection specific styling
        self._inject_case_selection_css()
        
        # Render case selection interface
        render_case_selection_page()
        
        # Check if a case was selected
        if st.session_state.get('case_selection_made', False):
            selected_case = st.session_state.get('selected_case', self.default_case)
            self._initialize_case_for_experience(selected_case)

    def _run_single_case_mode(self):
        """Run the application in single case mode (EXISTING LOGIC)"""
        # Use selected case or default
        current_case = st.session_state.get('selected_case', self.default_case)
        
        # Apply case-specific theme (NEW)
        self._apply_case_theme(current_case)
        
        # Run existing application logic
        self._inject_theme_css()
        self._show_header()
        self._main_app_logic()

    def _initialize_case_for_experience(self, case_id: str):
        """Initialize session for case experience (NEW)"""
        try:
            # Clear return to selection flag
            st.session_state.return_to_selection = False
            
            # Load case configuration
            case_data = case_manager.load_case(case_id)
            if not case_data:
                st.error(f"案例 {case_id} 配置加载失败")
                st.session_state.case_selection_made = False
                return
            
            # Initialize session with case data
            success = session_manager.initialize_session(case_id)
            if success:
                st.session_state.initialized = True
                st.session_state.case_data = case_data
                st.session_state.current_case = case_id
                
                # Initialize user decisions storage for this case
                if 'user_decisions' not in st.session_state:
                    st.session_state.user_decisions = {}
                    
                st.rerun()  # Refresh to show case experience
            else:
                st.error("案例初始化失败，请重新选择")
                st.session_state.case_selection_made = False
                
        except Exception as e:
            st.error(f"案例初始化错误: {str(e)}")
            st.session_state.case_selection_made = False

    def _apply_case_theme(self, case_id: str):
        """Apply case-specific theme CSS (NEW)"""
        if case_id == "ltcm":
            self._inject_ltcm_theme()
        elif case_id == "madoff":
            self._inject_madoff_theme()
        # Add more case themes as needed

    def _inject_ltcm_theme(self):
        """Inject LTCM-specific theme CSS (NEW)"""
        st.markdown("""
        <style>
            /* LTCM Quant Green Theme */
            .stApp {
                background-color: #0A141A !important;
            }
            
            /* Headers */
            .main h1, .main h2, .main h3 {
                color: #00FF41 !important;
                font-family: 'Roboto Mono', monospace !important;
                text-shadow: 0 0 8px rgba(0, 255, 65, 0.6);
            }
            
            /* Text */
            .main p, .main li, .main div {
                color: #E0E0E0 !important;
                font-family: 'Roboto Mono', monospace !important;
            }
            
            /* Buttons */
            .main .stButton > button {
                border: 2px solid #00FF41 !important;
                color: #00FF41 !important;
                background-color: transparent !important;
                font-family: 'Roboto Mono', monospace !important;
            }
            
            .main .stButton > button:hover {
                background-color: #00FF41 !important;
                color: #0A141A !important;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.6) !important;
            }
            
            /* Role containers for LTCM */
            .main .role-container {
                background: linear-gradient(135deg, rgba(0, 255, 65, 0.05) 0%, rgba(10, 20, 26, 0.95) 100%);
                border: 1px solid #00CC33;
                color: #E0E0E0;
            }
        </style>
        """, unsafe_allow_html=True)

    def _inject_madoff_theme(self):
        """Inject Madoff-specific theme CSS (EXISTING)"""
        # Keep existing madoff theme (classic blue theme)
        pass

    def _inject_case_selection_css(self):
        """Inject CSS for case selection interface (NEW)"""
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
            
            /* Case selection specific styles */
            .case-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                padding: 2rem 0;
            }

            .case-card {
                aspect-ratio: 3 / 4;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                overflow: hidden;
                position: relative;
                cursor: pointer;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                background-size: cover;
                background-position: center;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }

            .case-card:hover {
                transform: translateY(-10px) scale(1.02);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                border-color: rgba(255, 255, 255, 0.8);
            }

            .selection-header {
                text-align: center;
                margin-bottom: 3rem;
            }

            .selection-title {
                font-size: 3rem;
                font-weight: 700;
                background: linear-gradient(135deg, #2A52BE, #059669);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1rem;
            }
        </style>
        """, unsafe_allow_html=True)

    def _configure_page(self):
        """Configure Streamlit page settings (EXISTING)"""
        st.set_page_config(
            page_title=self.app_title,
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="auto"
        )

    def _initialize_session(self):
        """Initialize session with enhanced multi-case support (ENHANCED)"""
        if 'initialized' not in st.session_state:
            # Initialize basic session state
            st.session_state.app_version = "2.1.0-safe-multi-case"
            st.session_state.architecture = "Safe_Multi_Case_Update"
            
            # Initialize case selection state (NEW)
            if 'case_selection_made' not in st.session_state:
                st.session_state.case_selection_made = False
            
            if 'selected_case' not in st.session_state:
                st.session_state.selected_case = None
            
            if 'return_to_selection' not in st.session_state:
                st.session_state.return_to_selection = False
            
            # If no case selection interface, use default case (FALLBACK)
            if not CASE_SELECTION_AVAILABLE:
                self._initialize_default_case()

    def _initialize_default_case(self):
        """Initialize default case when case selection is not available (FALLBACK)"""
        # Load case configuration using existing architecture
        case_data = case_manager.load_case(self.default_case)
        if not case_data:
            st.error("案例配置加载失败，请刷新页面重试")
            st.stop()
        
        # Initialize session with case data
        success = session_manager.initialize_session(self.default_case)
        if success:
            st.session_state.initialized = True
            st.session_state.case_data = case_data
            st.session_state.current_case = self.default_case
            
            # Initialize user decisions storage
            if 'user_decisions' not in st.session_state:
                st.session_state.user_decisions = {}
                
        else:
            st.error("应用初始化失败,请刷新页面重试")
            st.stop()

    def _inject_theme_css(self):
        """Inject base CSS styles (EXISTING)"""
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
        """Show application header with case info (ENHANCED)"""
        # Add return to case selection button if available (NEW)
        if CASE_SELECTION_AVAILABLE and st.session_state.get('case_selection_made', False):
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("← 案例选择", key="return_to_selection_btn"):
                    st.session_state.return_to_selection = True
                    st.rerun()
            with col2:
                st.title(self.app_title)
        else:
            st.title(self.app_title)
        
        st.caption(self.app_description)
        
        # Show case metadata (ENHANCED)
        current_case = st.session_state.get('current_case', self.default_case)
        case_metadata = case_manager.get_case_metadata(current_case)
        
        if case_metadata:
            col1, col2, col3 = st.columns(3)
            col1.metric("案例", case_metadata.title.split("：")[0])
            col2.metric("认知偏误", case_metadata.target_bias)
            col3.metric("体验时长", f"{case_metadata.duration_minutes}分钟")
    
    def _main_app_logic(self):
        """Main application logic using S's component-based architecture (EXISTING)"""
        current_step = st.session_state.get('current_step', 1)
        current_case = st.session_state.get('current_case', self.default_case)
        
        # Load case data using new schema
        case_data = case_manager.load_case(current_case)
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
                
                # Add navigation (ENHANCED)
                self._render_navigation(current_act, len(acts))
                
            except Exception as e:
                error_handler.handle_error(
                    ErrorType.COMPONENT_ERROR,
                    f"组件渲染失败: {str(e)}",
                    {"act_id": current_act.get('act_id'), "step": current_step}
                )
        else:
            st.error(f"未找到第 {current_step} 幕")

    def _render_navigation(self, current_act: Dict[str, Any], total_acts: int):
        """Render navigation controls (EXISTING)"""
        current_step = st.session_state.get('current_step', 1)
        
        st.divider()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_step > 1:
                if st.button("← 上一幕", key="prev_step"):
                    st.session_state.current_step = current_step - 1
                    st.rerun()
        
        with col2:
            # Progress indicator
            progress = current_step / total_acts
            st.progress(progress, text=f"进度: {current_step}/{total_acts}")
        
        with col3:
            if current_step < total_acts:
                if st.button("下一幕 →", key="next_step"):
                    st.session_state.current_step = current_step + 1
                    st.rerun()
            else:
                if st.button("完成体验", key="complete_experience"):
                    st.success("🎉 恭喜完成案例体验！")
                    st.balloons()
                    
                    # Option to return to case selection (NEW)
                    if CASE_SELECTION_AVAILABLE:
                        time.sleep(2)
                        if st.button("选择其他案例", key="select_another_case"):
                            st.session_state.return_to_selection = True
                            st.session_state.current_step = 1
                            st.rerun()

    def _show_debug_info(self):
        """Show debug information if enabled (ENHANCED)"""
        if self.app_config.get('show_debug_ui', False):
            with st.sidebar:
                st.subheader("🔧 调试信息")
                st.json({
                    "app_version": st.session_state.get('app_version', 'unknown'),
                    "case_selection_available": CASE_SELECTION_AVAILABLE,
                    "case_selection_made": st.session_state.get('case_selection_made', False),
                    "selected_case": st.session_state.get('selected_case', None),
                    "current_case": st.session_state.get('current_case', None),
                    "current_step": st.session_state.get('current_step', 1),
                    "return_to_selection": st.session_state.get('return_to_selection', False),
                    "available_cases": self.available_cases
                })
                
                if st.button("重置应用状态"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

# Application entry point
def main():
    """Main application entry point"""
    try:
        app = CognitiveBlackBoxApp()
        app.run()
    except Exception as e:
        st.error(f"应用启动失败: {str(e)}")
        st.error("请刷新页面重试，如果问题持续存在请联系技术支持")

if __name__ == "__main__":
    main()
