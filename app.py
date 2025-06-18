# cognitive-blackbox/app.py (Final Diagnostic Version v2 - Complete File)
"""
Cognitive Black Box - Streamlit Main Application (Complete Refactored Version)
This version includes Hoshino's diagnostic probe to identify startup issues.
"""

import streamlit as st
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

# --- 1. Project Setup & Module Imports ---
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# We wrap imports in a try-except to provide better startup feedback
try:
    from core.case_manager import case_manager
    from utils.session_manager import session_manager
    from core.ai_engine import ai_engine
    from views.component_renderer import component_renderer
    # This variable is defined in ai_engine.py, we need it for diagnostics
    from core.ai_engine import GENAI_AVAILABLE
    MODULES_LOADED = True
except ImportError as e:
    st.error(f"FATAL: A core module failed to import: {str(e)}")
    st.error("Please ensure all project files (like core/ai_engine.py) are correctly deployed.")
    st.stop()


class CognitiveBlackBoxApp:
    """
    Main application class orchestrating the user experience.
    """
    
    def __init__(self):
        """Initialize application."""
        self.app_title = "🧠 认知黑匣子"
        self.app_description = "18分钟认知升级体验"
        self.default_case = "madoff"

    def run(self):
        """Run the main application flow."""
        self._configure_page()
        
        # --- HOSHINO'S DIAGNOSTIC PROBE ---
        # This probe runs first to check critical system states.
        self._run_diagnostic_probe()
        # ------------------------------------

        # Initialize session state if it's the first run
        self._initialize_session()

        # Render the main UI
        self._show_header()
        self._main_app_logic()
        self._show_debug_info()

    def _run_diagnostic_probe(self):
        """Displays a diagnostic panel to help debug startup issues."""
        with st.expander("🕵️‍♂️ 星野的诊断探针 (点击展开)", expanded=True):
            st.info("这个诊断模块用于检查应用启动时的关键状态，帮助我们快速定位问题。")
            
            # Probe 1: Check Streamlit Secrets for API Key
            st.markdown("**1. API密钥加载状态:**")
            api_key_from_secrets = st.secrets.get("GEMINI_API_KEY")
            if api_key_from_secrets and isinstance(api_key_from_secrets, str) and len(api_key_from_secrets) > 10:
                st.success("✅ 成功从Streamlit Secrets中读取到GEMINI_API_KEY。")
                st.code(f"密钥片段: {api_key_from_secrets[:5]}...{api_key_from_secrets[-4:]}", language=None)
            else:
                st.error("❌ 严重故障: 未能从Streamlit Secrets中读取到有效的GEMINI_API_KEY！这是导致AI不工作的首要原因。")
                st.warning("请检查：1. Secrets名称是否为`GEMINI_API_KEY` 2. 密钥是否用英文双引号包裹。")

            # Probe 2: Check AI Engine Client Initialization
            st.markdown("**2. AI引擎客户端初始化状态:**")
            if not GENAI_AVAILABLE:
                 st.error("❌ 严重故障: `google-generativeai` 库导入失败。请检查 `requirements.txt`。")
            elif hasattr(ai_engine, 'gemini_client') and ai_engine.gemini_client is not None:
                st.success("✅ AI引擎的Gemini客户端已成功初始化。")
            else:
                st.error("❌ 严重故障: AI引擎的Gemini客户端未能初始化！主要原因可能是API密钥未能正确加载。")

            # Probe 3: Check Prompt & Case Config Loading
            st.markdown("**3. 配置文件加载状态:**")
            if hasattr(ai_engine, 'roles_prompts') and ai_engine.roles_prompts:
                loaded_roles = list(ai_engine.roles_prompts.keys())
                st.success(f"✅ 成功加载了 {len(loaded_roles)} 个角色的Prompt配置: {loaded_roles}")
            else:
                st.error("❌ 严重故障: 未能从 `config/prompts/` 目录加载任何Prompt！请检查文件路径和JSON格式。")
        st.divider()

    def _configure_page(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=self.app_title,
            page_icon="🧠",
            layout="centered",
            initial_sidebar_state="auto"
        )
        self._inject_theme_css()

    def _initialize_session(self):
        """Initialize session state."""
        if 'initialized' not in st.session_state:
            # For simplicity, we assume case_manager and session_manager are available if MODULES_LOADED is True
            case_data = case_manager.load_case(self.default_case)
            success = session_manager.initialize_session(self.default_case)
            if success and case_data:
                st.session_state.initialized = True
                st.session_state.case_data = case_data
                if 'user_decisions' not in st.session_state:
                    st.session_state.user_decisions = {}
            else:
                st.error("应用初始化失败，请刷新页面重试。")
                st.stop()
    
    def _inject_theme_css(self):
        """Inject CSS styles."""
        st.markdown("""
        <style>
            /* The same complete CSS from previous discussions */
            @import url('https://fonts.googleapis.com/css2?family=Inter,Lato,Lora,Merriweather&display=swap');
            .stApp { background-color: #F0F2F6; }
            .block-container { max-width: 800px; padding-top: 1rem; }
            .role-container {
                border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
                border-left: 5px solid; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            }
            .role-host { background-color: #FFFFFF; border-color: #2A52BE; font-family: 'Lora', serif; }
            .role-investor { background-color: #FFF5F5; border-color: #D93025; font-family: 'Inter', sans-serif; }
            .role-mentor { background-color: #F3F9F3; border-color: #059669; font-family: 'Merriweather', serif; }
            .role-assistant { background-color: #F1FAFA; border-color: #0891B2; font-family: 'Lato', sans-serif; }
        </style>
        """, unsafe_allow_html=True)
    
    def _show_header(self):
        """Show application header."""
        st.title(self.app_title)
        st.caption(self.app_description)

    def _main_app_logic(self):
        """Main application logic using the component-based renderer."""
        current_step = st.session_state.get('current_step', 1)
        case_data = st.session_state.get('case_data', {})
        
        acts = case_data.get('acts', [])
        current_act = next((act for act in acts if act.get('act_id') == current_step), None)
        
        if current_act:
            st.header(current_act.get('act_name', f'第 {current_step} 幕'))
            st.progress(current_act.get('progress_percentage', 25) / 100)

            try:
                # Let the component renderer do its job
                component_renderer.render_act(current_act)
                self._render_navigation(current_act, len(acts))
            except Exception as e:
                st.error(f"渲染第 {current_step} 幕时出现错误。")
                st.exception(e)
        else:
            st.error(f"未找到步骤 {current_step} 的内容配置。")

    def _render_navigation(self, current_act: Dict[str, Any], total_acts: int):
        """Render navigation buttons."""
        st.markdown("---")
        col1, col2 = st.columns(2)
        current_step = current_act.get('act_id', 1)

        if current_step > 1:
            if col1.button("⬅️ 上一幕"):
                st.session_state.current_step -= 1
                st.rerun()
        
        if current_step < total_acts:
            if col2.button("下一幕 ➡️", type="primary"):
                st.session_state.current_step += 1
                st.rerun()
        else:
            if col2.button("🔄 重新开始体验"):
                self._reset_session()
                st.rerun()
    
    def _reset_session(self):
        """Resets the session state to start over."""
        keys_to_clear = list(st.session_state.keys())
        for key in keys_to_clear:
            del st.session_state[key]
    
    def _show_debug_info(self):
        """Shows debug info in the sidebar."""
        if st.sidebar.checkbox("显示调试信息"):
            st.sidebar.subheader("🔧 调试信息")
            st.sidebar.write("Session State:", st.session_state)

# --- Main Execution Block ---
def main():
    """Main function to run the application."""
    if MODULES_LOADED:
        try:
            app = CognitiveBlackBoxApp()
            app.run()
        except Exception as e:
            st.error("应用启动时发生严重错误。")
            st.exception(e)
    else:
        st.error("核心模块加载失败，应用无法启动。")

if __name__ == "__main__":
    main()
