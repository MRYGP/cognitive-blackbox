# cognitive-blackbox/app.py (Version with Hoshino's Diagnostic Probe)
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
# We wrap this in a try-except to provide better feedback if modules are missing
try:
    from core.case_manager import case_manager
    from utils.session_manager import session_manager
    from core.ai_engine import ai_engine
    from views.component_renderer import component_renderer
    # Assuming these modules exist as per C's design
    from config import get_app_config
    from utils.error_handlers import error_handler, ErrorType
    from utils.validators import input_validator
    MODULES_LOADED = True
except ImportError as e:
    st.error(f"FATAL: A core module failed to import: {str(e)}")
    st.error("Please ensure all project files are correctly deployed and named. The application cannot start.")
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
            self.app_config = {'show_debug_ui': True} # Simple fallback

    def run(self):
        """Run main application with new architecture"""
        # This is the main execution flow
        self._configure_page()
        
        # --- HOSHINO'S DIAGNOSTIC PROBE ---
        # This probe runs at the very beginning to check critical system states
        # before the main application logic starts.
        self._run_diagnostic_probe()
        # ------------------------------------

        self._initialize_session()
        self._inject_theme_css()
        self._show_header()
        self._main_app_logic()
        
        if self.app_config.get('show_debug_ui', False):
            self._show_debug_info()

    def _run_diagnostic_probe(self):
        """
        A dedicated function to run system diagnostics and display them at the top.
        This helps to debug issues without interfering with the main app flow.
        """
        st.subheader("🕵️‍♂️ 星野的诊断探针")
        with st.expander("点击展开，查看系统内部状态", expanded=True):
            st.info("这个诊断模块用于检查应用启动时的关键状态，帮助我们快速定位问题。")
            
            # --- Probe 1: Check Streamlit Secrets ---
            st.markdown("**1. API密钥加载状态:**")
            api_key_from_secrets = st.secrets.get("GEMINI_API_KEY")
            if api_key_from_secrets and len(api_key_from_secrets) > 10:
                st.success("✅ 成功从Streamlit Secrets中读取到GEMINI_API_KEY。")
                st.code(f"密钥片段: {api_key_from_secrets[:5]}...{api_key_from_secrets[-4:]}", language=None)
            else:
                st.error("❌ 严重故障: 未能从Streamlit Secrets中读取到有效的GEMINI_API_KEY！这是导致AI不工作的首要原因。")

            # --- Probe 2: Check AI Engine Client Initialization ---
            st.markdown("**2. AI引擎客户端初始化状态:**")
            if hasattr(ai_engine, 'gemini_client') and ai_engine.gemini_client is not None:
                st.success("✅ AI引擎的Gemini客户端已成功初始化。")
            else:
                st.error("❌ 严重故障: AI引擎的Gemini客户端未能初始化！请检查API密钥或SDK版本兼容性。")
                if not GENAI_AVAILABLE:
                     st.warning("เพิ่มเติม: `google-genai` 库导入失败。")

            # --- Probe 3: Check Prompt & Case Config Loading ---
            st.markdown("**3. 配置文件加载状态:**")
            # Check Prompts
            if hasattr(ai_engine, 'roles_prompts') and ai_engine.roles_prompts:
                loaded_roles = list(ai_engine.roles_prompts.keys())
                st.success(f"✅ 成功加载了 {len(loaded_roles)} 个角色的Prompt配置: {loaded_roles}")
            else:
                st.error("❌ 严重故障: 未能从 `config/prompts/` 目录加载任何Prompt！请检查文件路径和JSON格式。")
            
            # Check Cases
            # Assuming case_manager has a way to report loaded cases
            try:
                loaded_cases = case_manager.list_available_cases()
                st.success(f"✅ 成功加载了 {len(loaded_cases)} 个案例配置: {loaded_cases}")
            except Exception as e:
                st.error(f"❌ 严重故障: 加载 `config/cases/` 目录失败: {e}")
        st.markdown("---")


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
            case_data = case_manager.load_case(self.default_case)
            if not case_data:
                st.error("案例配置加载失败，请刷新页面重试")
                st.stop()
            
            success = session_manager.initialize_session(self.default_case)
            if success:
                st.session_state.initialized = True
                st.session_state.case_data = case_data
                if 'user_decisions' not in st.session_state:
                    st.session_state.user_decisions = {}
            else:
                st.error("应用初始化失败,请刷新页面重试")
                st.stop()

    def _inject_theme_css(self):
        """Inject base CSS styles"""
        # This CSS is a merge of C's and S's final designs
        st.markdown("""
        <style>
            /* The same complete CSS from previous discussions */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Lato:wght@400;700&family=Lora:wght@400;700&family=Merriweather:wght@400;700&display=swap');
            .stApp { background-color: #F0F2F6; }
            .block-container { max-width: 800px; padding-top: 1rem; }
            .role-container, .act-container {
                border-radius: 12px; padding: 2rem; margin-bottom: 2rem;
                border-left: 6px solid; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            }
            .role-host { background-color: #FFFFFF; border-color: #2A52BE; font-family: 'Lora', serif; }
            .role-investor { background-color: #FFF5F5; border-color: #D93025; font-family: 'Inter', sans-serif; }
            .role-mentor { background-color: #F3F9F3; border-color: #059669; font-family: 'Merriweather', serif; }
            .role-assistant { background-color: #F1FAFA; border-color: #0891B2; font-family: 'Lato', sans-serif; }
        </style>
        """, unsafe_allow_html=True)
    
    def _show_header(self):
        """Show application header with case info"""
        # This logic remains the same as Claude's implementation
        st.title(self.app_title)
        st.caption(self.app_description)
        case_metadata = case_manager.get_case_metadata(self.default_case)
        if case_metadata:
            col1, col2, col3 = st.columns(3)
            col1.metric("案例", case_metadata.get('title', '').split("：")[0])
            col2.metric("认知偏误", case_metadata.get('target_bias', {}).get('name_cn', ''))
            col3.metric("体验时长", f"{case_metadata.get('duration_minutes', 18)}分钟")
    
    def _main_app_logic(self):
        """Main application logic using S's component-based architecture"""
        # This logic remains the same as Claude's implementation
        current_step = st.session_state.get('current_step', 1)
        case_data = st.session_state.get('case_data', {})
        if not case_data:
            st.error("案例数据未加载，请刷新。")
            return
            
        acts = case_data.get('acts', [])
        current_act = next((act for act in acts if act.get('act_id') == current_step), None)
        
        if current_act:
            try:
                # Assuming component_renderer exists and works as designed by C
                component_renderer.render_act(current_act)
                self._render_navigation(current_act, len(acts))
            except Exception as e:
                st.error(f"渲染第 {current_step} 幕时出现错误: {e}")
                st.exception(e) # Show full traceback for debugging
        else:
            st.error(f"未找到步骤 {current_step} 的内容配置。")

    def _render_navigation(self, current_act: Dict[str, Any], total_acts: int) -> None:
        """Render navigation based on S's design"""
        # This logic remains the same as Claude's implementation
        current_step = current_act.get('act_id', 1)
        progress = (current_step / total_acts) * 100
        st.progress(int(progress))
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        if current_step > 1:
            if col1.button("⬅️ 上一幕"):
                st.session_state.current_step -= 1
                st.rerun()
        
        col2.markdown(f"<div style='text-align: center'>第 {current_step} 幕 / 共 {total_acts} 幕</div>", unsafe_allow_html=True)

        if current_step < total_acts:
            if col3.button("下一幕 ➡️", type="primary"):
                st.session_state.current_step += 1
                st.rerun()
        else:
            if col3.button("🔄 重新开始"):
                self._reset_session()
                st.rerun()

    def _reset_session(self):
        """Reset session to start"""
        # This logic remains the same as Claude's implementation
        keys_to_clear = list(st.session_state.keys())
        for key in keys_to_clear:
            del st.session_state[key]
    
    def _show_debug_info(self):
        """Show debug information in sidebar"""
        # This logic remains the same as Claude's implementation
        st.sidebar.subheader("🔧 调试信息")
        st.sidebar.write(st.session_state)


# --- Main Execution Block ---
def main():
    """Main function to run the Streamlit application."""
    try:
        app = CognitiveBlackBoxApp()
        app.run()
    except Exception as e:
        st.error(f"应用启动失败: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
